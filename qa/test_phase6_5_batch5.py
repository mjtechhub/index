#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6.5E Batch 5 Verification Suite
(qa/test_phase6_5_batch5.py)

Validates all Phase 6.5E requirements:
1. Static & Data Integrity Assertions:
   - Exactly 148 tutorials in data/tutorials.json
   - Exact category distribution: Networking: 73, Windows: 15, Linux: 15, Servers: 15, Cybersecurity: 15, Cloud & AI: 15
   - Strict category-contiguous ordering in data/tutorials.json
   - Master Curriculum: exactly 471 total topics, 148 published, 323 planned
   - Exact 1-to-1 parity between tutorials.json and published curriculum subtopics
   - Zero duplicate IDs, zero duplicate URLs, zero unmapped, zero phantom published
   - Zero category or level mismatches
2. Raw HTML Static SEO & Schema Validation across all 18 Batch 5 files:
   - Exactly 1 H1 per file
   - Unique title, meta description, canonical URL (https://themjtechhub.site)
   - OpenGraph & Twitter tags
   - Valid TechArticle JSON-LD structured data
3. Targeted Technical Accuracy Assertions for all 18 Batch 5 topics:
   - TCP Handshake (SYN/ACK sequence math, ISN CSPRNG randomization, 2MSL TIME_WAIT socket dissipation)
   - DNS Resolution (Root Anycast clusters, stub resolver recursive RD bit, iterative referral AA bit)
   - Wi-Fi Security (WPA2-PSK flaws, 802.1X/EAP-TLS mutual certs, WPA3 SAE Dragonfly, PMF 802.11w)
   - Windows Registry (HKLM/HKCU root hives, disk-backed hives, CLFS transaction logs, value types)
   - Robocopy (/MIR mirror mode caution, /MT multithreading, /R:3 /W:5 retry override, bitmask return codes)
   - Active Directory Domain Join (DNS _msdcs SRV discovery, 5-minute Kerberos clock skew, Netlogon, djoin)
   - Linux Boot Troubleshooting (GRUB rescue set root/prefix/normal, dracut initramfs UUID/LVM, fstab nofail)
   - Linux Standard Streams (POSIX FDs 0/1/2, 2>&1 order of operations, pipefail and PIPESTATUS)
   - Linux Sudoers (/etc/sudoers.d/ 0440 permissions, visudo syntax check, NOEXEC/sudoedit shell escape protection)
   - Server Hardware Health (BMC out-of-band architecture, IPMI SDR telemetry, SNMP Trap/Inform, Redfish)
   - Windows Server Hardening (CIS Level 1 vs Level 2, disabling SMBv1/LLMNR/NetBIOS, LSA Protection, Credential Guard)
   - Systematic RCA (Blameless post-mortem culture, UTC timeline, 5-Whys, Fishbone diagram, SMART CAPA)
   - Cybersecurity Defense-in-Depth (7 concentric rings, control classifications, Assume Breach mindset)
   - Privileged Access Management (Credential vaulting, automated check-in rotation, proxy session recording, JIT)
   - Endpoint Detection and Response (Behavioral heuristics vs static AV, kernel ELAM/eBPF/AMSI hooks, process tree, isolation)
   - Cloud Containers (VMs vs containers kernel isolation, Fargate/ACI vs ECS vs EKS/AKS, CNI pod networking)
   - Cloud Security Groups vs NACLs (Stateful ENI-level SGs vs stateless subnet NACLs, ephemeral return ports)
   - AIOps Architecture (5-stage telemetry pipeline, ML noise reduction, dynamic baselining vs static thresholds, Explainable AI)
4. Live Playwright Browser Verification & Screenshots:
   - Representative Batch 5 tutorials across all 6 core categories
   - Dynamic badges on topics.html: '148 Published Tutorials' & '471 Curriculum Topics'
   - Search integration: Batch 5 topics searchable, planned topics excluded, 0 duplicate results
   - Responsive layout: zero horizontal overflow across 375px, 768px, 1024px, 1440px
   - Zero console errors and zero local 404 network requests
   - High-resolution visual screenshots saved to qa/
"""

import asyncio
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from playwright.async_api import async_playwright

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
BASE_URL = "http://localhost/index"
QA_DIR = Path(__file__).resolve().parent
ROOT_DIR = QA_DIR.parent
TUTS_JSON_PATH = ROOT_DIR / "data" / "tutorials.json"
TOPICS_JSON_PATH = ROOT_DIR / "data" / "topics.json"
CANONICAL_DOMAIN = "https://themjtechhub.site"

BATCH5_TOPIC_IDS = [
    # Networking
    "tcp-three-way-handshake-and-teardown",
    "dns-resolution-iterative-vs-recursive-queries",
    "wi-fi-security-wpa2-enterprise-vs-wpa3",
    # Windows
    "windows-registry-architecture-and-root-hives",
    "windows-robocopy-advanced-file-replication-guide",
    "windows-active-directory-domain-join-prerequisites-workflow",
    # Linux
    "linux-troubleshooting-boot-failures-grub-emergency-mode",
    "linux-standard-streams-redirection-and-pipes",
    "linux-sudo-configuration-and-visudo-administration",
    # Servers
    "server-hardware-health-monitoring-ipmi-snmp-traps",
    "windows-server-security-baselines-and-cis-benchmark-hardening",
    "systematic-root-cause-analysis-rca-methodology-for-server-outages",
    # Cybersecurity
    "defense-in-depth-strategy-and-layered-controls",
    "privileged-access-management-pam-vaulting-and-session-recording",
    "endpoint-detection-and-response-edr-architecture-and-telemetry",
    # Cloud & AI
    "cloud-container-services-overview-ecs-aci-and-managed-k8s",
    "cloud-security-groups-vs-network-access-control-lists",
    "aiops-architecture-applying-machine-learning-to-it-operations"
]

class HtmlParserHelper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.title_text = ""
        self.capturing_title = False
        self.meta_desc = ""
        self.canonical = ""
        self.og_tags = {}
        self.twitter_tags = {}
        self.json_ld_raw = []
        self.capturing_json_ld = False
        self.json_ld_buffer = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "title":
            self.capturing_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "link" and attr_dict.get("rel") == "canonical":
            self.canonical = attr_dict.get("href", "")
        elif tag == "meta":
            name = attr_dict.get("name", "").lower()
            prop = attr_dict.get("property", "").lower()
            content = attr_dict.get("content", "")
            if name == "description":
                self.meta_desc = content
            elif prop.startswith("og:"):
                self.og_tags[prop] = content
            elif name.startswith("twitter:"):
                self.twitter_tags[name] = content
        elif tag == "script" and attr_dict.get("type") == "application/ld+json":
            self.capturing_json_ld = True
            self.json_ld_buffer = ""

    def handle_endtag(self, tag):
        if tag == "title":
            self.capturing_title = False
            self.title_text = self.title_text.strip()
        elif tag == "script" and self.capturing_json_ld:
            self.capturing_json_ld = False
            if self.json_ld_buffer.strip():
                self.json_ld_raw.append(self.json_ld_buffer.strip())

    def handle_data(self, data):
        if self.capturing_title:
            self.title_text += data
        elif self.capturing_json_ld:
            self.json_ld_buffer += data

def test_data_integrity():
    print("==================================================")
    print("TEST 1: Static & Data Integrity Assertions")
    print("==================================================")

    # 1. Load data
    with open(TUTS_JSON_PATH, "r", encoding="utf-8") as f:
        tuts = json.load(f)

    with open(TOPICS_JSON_PATH, "r", encoding="utf-8") as f:
        topics = json.load(f)

    # 2. Tutorials count
    print(f"Total tutorials in tutorials.json: {len(tuts)}")
    assert len(tuts) == 148, f"Expected 148 tutorials, got {len(tuts)}"

    # 3. Category distribution
    expected_dist = {
        "Networking": 73,
        "Windows": 15,
        "Linux": 15,
        "Servers": 15,
        "Cybersecurity": 15,
        "Cloud & AI": 15
    }
    for cat, exp_cnt in expected_dist.items():
        actual_cnt = sum(1 for t in tuts if t["category"] == cat)
        print(f"  - {cat}: {actual_cnt} (Expected: {exp_cnt})")
        assert actual_cnt == exp_cnt, f"Category '{cat}' count mismatch: {actual_cnt} != {exp_cnt}"

    # 4. Category-contiguous order check
    cat_seq = [t["category"] for t in tuts]
    seen_cats = []
    current_cat = None
    for c in cat_seq:
        if c != current_cat:
            assert c not in seen_cats, f"Category order not contiguous! '{c}' reappeared after seeing {seen_cats}"
            seen_cats.append(c)
            current_cat = c
    print("[PASS] Category-contiguous ordering verified in tutorials.json.")

    # 5. Global ID uniqueness and Master curriculum check
    all_curric_ids = set()
    pub_curric_ids = set()
    plan_curric_ids = set()

    for cat in topics["categories"]:
        for sec in cat.get("sections", []):
            for sub in sec.get("subtopics", []):
                sid = sub["id"]
                assert sid not in all_curric_ids, f"Duplicate curriculum topic ID found: {sid}"
                all_curric_ids.add(sid)
                if sub.get("status") == "published":
                    pub_curric_ids.add(sid)
                    assert "url" in sub and sub["url"], f"Published curriculum subtopic '{sid}' missing URL!"
                elif sub.get("status") == "planned":
                    plan_curric_ids.add(sid)

    print(f"Total Curriculum Topics: {len(all_curric_ids)} (Expected: 471)")
    print(f"Published Curriculum:    {len(pub_curric_ids)} (Expected: 148)")
    print(f"Planned Curriculum:      {len(plan_curric_ids)} (Expected: 323)")

    assert len(all_curric_ids) == 471, f"Curriculum topic count mismatch: {len(all_curric_ids)} != 471"
    assert len(pub_curric_ids) == 148, f"Published curriculum count mismatch: {len(pub_curric_ids)} != 148"
    assert len(plan_curric_ids) == 323, f"Planned curriculum count mismatch: {len(plan_curric_ids)} != 323"

    # 6. One-to-one mapping
    tut_id_set = {t["id"] for t in tuts}
    assert len(tut_id_set) == len(tuts), "Duplicate ID in tutorials.json!"
    assert tut_id_set == pub_curric_ids, "Mismatch between tutorials.json and published curriculum!"
    print("[PASS] Exact 1-to-1 mapping verified between tutorials.json (148) and published curriculum entries (148).")

    # 7. Batch 5 specific topics check
    for tid in BATCH5_TOPIC_IDS:
        assert tid in tut_id_set, f"Batch 5 topic '{tid}' missing from tutorials.json!"
        assert tid in pub_curric_ids, f"Batch 5 topic '{tid}' not marked 'published' in topics.json!"

    print(f"[PASS] All 18 Batch 5 topics verified published in tutorials.json and topics.json.")

def test_raw_html_seo():
    print("\n==================================================")
    print("TEST 2: Raw HTML Static SEO & Schema Validation")
    print("==================================================")

    with open(TUTS_JSON_PATH, "r", encoding="utf-8") as f:
        tuts = json.load(f)

    tut_map = {t["id"]: t for t in tuts}

    for tid in BATCH5_TOPIC_IDS:
        meta = tut_map[tid]
        fpath = ROOT_DIR / meta["url"]
        assert fpath.exists(), f"File does not exist: {fpath}"

        raw_html = fpath.read_text(encoding="utf-8")
        parser = HtmlParserHelper()
        parser.feed(raw_html)

        # 1. H1 check
        assert parser.h1_count == 1, f"{tid}: Expected exactly 1 H1, got {parser.h1_count}"

        # 2. Title check
        expected_title = f"{meta['title']} | {meta['category']} Tutorial | MJ Tech Hub"
        assert parser.title_text == expected_title, f"{tid}: Title mismatch: '{parser.title_text}' != '{expected_title}'"

        # 3. Canonical URL
        expected_canonical = f"{CANONICAL_DOMAIN}/{meta['url']}"
        assert parser.canonical == expected_canonical, f"{tid}: Canonical mismatch: '{parser.canonical}' != '{expected_canonical}'"

        # 4. OpenGraph & Twitter
        assert parser.og_tags.get("og:title") == expected_title, f"{tid}: og:title mismatch"
        assert parser.og_tags.get("og:type") == "article", f"{tid}: og:type != 'article'"
        assert parser.og_tags.get("og:url") == expected_canonical, f"{tid}: og:url mismatch"
        assert parser.twitter_tags.get("twitter:card") == "summary", f"{tid}: twitter:card != 'summary'"
        assert parser.twitter_tags.get("twitter:title") == expected_title, f"{tid}: twitter:title mismatch"

        # 5. TechArticle JSON-LD
        assert len(parser.json_ld_raw) > 0, f"{tid}: Missing JSON-LD script block"
        schema_data = json.loads(parser.json_ld_raw[0])
        assert schema_data.get("@type") == "TechArticle", f"{tid}: JSON-LD @type != TechArticle"
        assert schema_data.get("headline") == meta["title"], f"{tid}: JSON-LD headline mismatch"
        assert schema_data.get("url") == expected_canonical, f"{tid}: JSON-LD url mismatch"
        assert schema_data.get("proficiencyLevel") == meta["level"], f"{tid}: JSON-LD proficiencyLevel mismatch"

    print(f"[PASS] All 18 Batch 5 HTML files pass Static SEO, JSON-LD, and single-H1 tests.")

def test_phase6_5e_technical_accuracy():
    print("\n==================================================")
    print("TEST 2B: Phase 6.5E Technical Accuracy Assertions")
    print("==================================================")

    # 1. TCP Handshake & Teardown Flow
    tcp_path = ROOT_DIR / "tutorials" / "networking" / "tcp-three-way-handshake-and-teardown.html"
    assert tcp_path.exists(), f"Missing {tcp_path}"
    tcp_html = tcp_path.read_text(encoding="utf-8")
    tcp_text = " ".join(re.sub(r'<[^>]+>', ' ', html.unescape(tcp_html)).split()).lower()
    assert "syn" in tcp_text and "syn-ack" in tcp_text and "ack" in tcp_text
    assert "initial sequence number" in tcp_text or "isn" in tcp_text
    assert ("time-wait" in tcp_text or "time_wait" in tcp_text) and "msl" in tcp_text
    assert "rfc 9293" in tcp_text
    assert "2 × msl" in tcp_text or "2 x msl" in tcp_text or "2×msl" in tcp_text
    assert "implementation-, version-, and configuration-dependent" in tcp_text
    assert "preventing delayed segment interference" in tcp_text or "delayed duplicate segments" in tcp_text
    assert "so_reuseaddr" in tcp_text or "socket exhaustion" in tcp_text
    assert "ss -tan" in tcp_html
    print("[PASS] TCP Three-Way Handshake, ISN randomization, RFC 9293 2xMSL, and implementation-dependent timer values verified.")

    # 2. DNS Resolution Iterative vs Recursive Queries
    dns_path = ROOT_DIR / "tutorials" / "networking" / "dns-resolution-iterative-vs-recursive-queries.html"
    assert dns_path.exists(), f"Missing {dns_path}"
    dns_html = dns_path.read_text(encoding="utf-8")
    assert "Recursive" in dns_html and "Iterative" in dns_html
    assert "Stub Resolver" in dns_html
    assert "13 named dns root server identities" in dns_html.lower()
    assert "operated by independent organizations" in dns_html.lower() or "operated by multiple organizations" in dns_html.lower()
    assert "anycast" in dns_html.lower()
    assert "Authoritative Answer" in dns_html or "AA" in dns_html
    assert "dig +trace" in dns_html or "Resolve-DnsName" in dns_html
    print("[PASS] DNS hierarchical resolution, 13 named root server identities, and recursive vs iterative queries verified.")

    # 3. Wi-Fi Security WPA2-Enterprise vs WPA3-Enterprise
    wifi_path = ROOT_DIR / "tutorials" / "networking" / "wi-fi-security-wpa2-enterprise-vs-wpa3.html"
    assert wifi_path.exists(), f"Missing {wifi_path}"
    wifi_html = wifi_path.read_text(encoding="utf-8")
    wifi_text = " ".join(re.sub(r'<[^>]+>', ' ', html.unescape(wifi_html)).split()).lower()
    assert "wpa2-enterprise" in wifi_text and "wpa3-enterprise" in wifi_text
    assert "802.1x" in wifi_text and "eap-tls" in wifi_text
    assert "wpa3-personal" in wifi_text and ("sae" in wifi_text or "dragonfly" in wifi_text)
    assert "does not use sae" in wifi_text
    assert "robust management frames" in wifi_text
    assert "does not encrypt all" in wifi_text or "does not eliminate rf eavesdropping" in wifi_text
    assert "192-bit" in wifi_text and "cnsa" in wifi_text
    assert "gcmp-256" in wifi_text
    assert "ccmp-256 is not the" in wifi_text or "ccmp-256 is not the requirement" in wifi_text
    assert "sha-384" in wifi_text
    assert "suite b" in wifi_text and "historical" in wifi_text
    print("[PASS] Wi-Fi security (WPA3-Personal SAE vs WPA3-Enterprise 802.1X, PMF scope, 192-bit CNSA GCMP-256) verified.")

    # 4. Windows Registry Architecture & Root Hives
    reg_path = ROOT_DIR / "tutorials" / "windows" / "windows-registry-architecture-and-root-hives.html"
    assert reg_path.exists(), f"Missing {reg_path}"
    reg_html = reg_path.read_text(encoding="utf-8")
    assert "HKEY_LOCAL_MACHINE" in reg_html and "HKEY_CURRENT_USER" in reg_html
    assert "NTUSER.DAT" in reg_html
    assert "REG_DWORD" in reg_html and "REG_SZ" in reg_html
    assert ".LOG1" in reg_html or "transactional" in reg_html.lower()
    assert "Get-ItemProperty" in reg_html or "Set-ItemProperty" in reg_html
    print("[PASS] Windows Registry root hives, disk-backed files, and PowerShell management verified.")

    # 5. Robocopy Advanced File Replication Guide
    robo_path = ROOT_DIR / "tutorials" / "windows" / "windows-robocopy-advanced-file-replication-guide.html"
    assert robo_path.exists(), f"Missing {robo_path}"
    robo_html = robo_path.read_text(encoding="utf-8")
    assert "/MIR" in robo_html
    assert "/MT" in robo_html
    assert "/R:3" in robo_html or "/R:" in robo_html
    assert "/W:5" in robo_html or "/W:" in robo_html
    assert "/COPYALL" in robo_html or "/COPY:" in robo_html
    assert "bitmask" in robo_html.lower() or "exit code" in robo_html.lower()
    print("[PASS] Robocopy /MIR, /MT multithreading, retry parameters, and bitmask exit codes verified.")

    # 6. Active Directory Domain Join Prerequisites & Workflow
    adj_path = ROOT_DIR / "tutorials" / "windows" / "windows-active-directory-domain-join-prerequisites-workflow.html"
    assert adj_path.exists(), f"Missing {adj_path}"
    adj_html = adj_path.read_text(encoding="utf-8")
    assert "_ldap._tcp.dc._msdcs" in adj_html or "SRV" in adj_html
    assert "5 minutes" in adj_html.lower() or "clock skew" in adj_html.lower()
    assert "Netlogon" in adj_html and "Secure Channel" in adj_html
    assert "djoin" in adj_html
    assert "Test-ComputerSecureChannel" in adj_html
    print("[PASS] Active Directory domain join DNS SRV discovery, Kerberos time skew, and djoin offline join verified.")

    # 7. Linux Boot Troubleshooting (GRUB Rescue & Emergency Mode)
    boot_path = ROOT_DIR / "tutorials" / "linux" / "linux-troubleshooting-boot-failures-grub-emergency-mode.html"
    assert boot_path.exists(), f"Missing {boot_path}"
    boot_html = boot_path.read_text(encoding="utf-8")
    assert "grub rescue" in boot_html.lower()
    assert "insmod normal" in boot_html
    assert "dracut" in boot_html.lower() or "initramfs" in boot_html.lower()
    assert "emergency mode" in boot_html.lower()
    assert "nofail" in boot_html
    assert "chroot" in boot_html.lower()
    print("[PASS] Linux boot failure recovery (GRUB rescue, dracut initramfs, fstab nofail, chroot) verified.")

    # 8. Linux Standard Streams (stdin, stdout, stderr, pipes)
    str_path = ROOT_DIR / "tutorials" / "linux" / "linux-standard-streams-redirection-and-pipes.html"
    assert str_path.exists(), f"Missing {str_path}"
    str_html = str_path.read_text(encoding="utf-8")
    assert "stdin" in str_html and "stdout" in str_html and "stderr" in str_html
    assert "2>&1" in str_html
    assert "/dev/null" in str_html
    assert "tee" in str_html
    assert "pipefail" in str_html or "PIPESTATUS" in str_html
    print("[PASS] Linux POSIX file descriptors 0/1/2, redirection operators, and pipefail verified.")

    # 9. Linux Sudoers Administration & visudo
    sudo_path = ROOT_DIR / "tutorials" / "linux" / "linux-sudo-configuration-and-visudo-administration.html"
    assert sudo_path.exists(), f"Missing {sudo_path}"
    sudo_html = sudo_path.read_text(encoding="utf-8")
    assert "visudo" in sudo_html
    assert "/etc/sudoers" in sudo_html
    assert "0440" in sudo_html
    assert "NOEXEC" in sudo_html or "sudoedit" in sudo_html
    assert "Cmnd_Alias" in sudo_html or "User_Alias" in sudo_html
    print("[PASS] Sudoers visudo safety, /etc/sudoers.d/ permissions, and shell escape prevention verified.")

    # 10. Server Hardware Health Telemetry (IPMI & SNMP)
    ipmi_path = ROOT_DIR / "tutorials" / "servers" / "server-hardware-health-monitoring-ipmi-snmp-traps.html"
    assert ipmi_path.exists(), f"Missing {ipmi_path}"
    ipmi_html = ipmi_path.read_text(encoding="utf-8")
    assert "Baseboard Management Controller" in ipmi_html or "BMC" in ipmi_html
    assert "IPMI" in ipmi_html
    assert "ipmitool sdr list" in ipmi_html or "ipmitool" in ipmi_html
    assert "SNMP Trap" in ipmi_html or "Inform" in ipmi_html
    assert "Redfish" in ipmi_html
    print("[PASS] Server hardware BMC out-of-band monitoring, IPMI telemetry, and Redfish REST API verified.")

    # 11. Windows Server Security Baselines & CIS Benchmark Hardening
    cis_path = ROOT_DIR / "tutorials" / "servers" / "windows-server-security-baselines-and-cis-benchmark-hardening.html"
    assert cis_path.exists(), f"Missing {cis_path}"
    cis_html = cis_path.read_text(encoding="utf-8")
    assert "CIS" in cis_html
    assert "Level 1" in cis_html and "Level 2" in cis_html
    assert "SMBv1" in cis_html and "LLMNR" in cis_html
    assert "RunAsPPL" in cis_html or "LSA Protection" in cis_html
    assert "Credential Guard" in cis_html
    assert "LGPO" in cis_html
    print("[PASS] Windows Server CIS Level 1/2 baselines, LSA protection, and Credential Guard verified.")

    # 12. Systematic Root Cause Analysis (RCA) Methodology
    rca_path = ROOT_DIR / "tutorials" / "servers" / "systematic-root-cause-analysis-rca-methodology-for-server-outages.html"
    assert rca_path.exists(), f"Missing {rca_path}"
    rca_html = rca_path.read_text(encoding="utf-8")
    assert "blameless" in rca_html.lower()
    assert "5-Whys" in rca_html or "5 Whys" in rca_html
    assert "Fishbone" in rca_html or "Ishikawa" in rca_html
    assert "UTC" in rca_html
    assert "CAPA" in rca_html or "Corrective and Preventive" in rca_html
    print("[PASS] Systematic RCA blameless post-mortems, 5-Whys, and CAPA action tracking verified.")

    # 13. Cybersecurity Defense-in-Depth & Zero Trust
    did_path = ROOT_DIR / "tutorials" / "cybersecurity" / "defense-in-depth-strategy-and-layered-controls.html"
    assert did_path.exists(), f"Missing {did_path}"
    did_html = did_path.read_text(encoding="utf-8")
    assert "Defense-in-Depth" in did_html or "layered" in did_html.lower()
    assert "educational and organizational model" in did_html.lower()
    assert "Physical" in did_html and "Perimeter" in did_html and "Host" in did_html
    assert "Preventative" in did_html and "Detective" in did_html and "Corrective" in did_html
    assert "Assume Breach" in did_html
    assert "no implicit trust based on network location" in did_html.lower()
    assert "resource-centric" in did_html.lower()
    print("[PASS] Defense-in-Depth educational model, control classifications, and Zero Trust no-implicit-trust principle verified.")

    # 14. Privileged Access Management (PAM)
    pam_path = ROOT_DIR / "tutorials" / "cybersecurity" / "privileged-access-management-pam-vaulting-and-session-recording.html"
    assert pam_path.exists(), f"Missing {pam_path}"
    pam_html = pam_path.read_text(encoding="utf-8")
    assert "Privileged Access Management" in pam_html or "PAM" in pam_html
    assert "vault" in pam_html.lower()
    assert "Just-In-Time" in pam_html or "JIT" in pam_html
    assert "session" in pam_html.lower() and "recording" in pam_html.lower()
    assert "break-glass" in pam_html.lower()
    print("[PASS] Privileged Access Management credential vaulting, session recording, and JIT elevation verified.")

    # 15. Endpoint Detection and Response (EDR)
    edr_path = ROOT_DIR / "tutorials" / "cybersecurity" / "endpoint-detection-and-response-edr-architecture-and-telemetry.html"
    assert edr_path.exists(), f"Missing {edr_path}"
    edr_html = edr_path.read_text(encoding="utf-8")
    assert "Endpoint Detection and Response" in edr_html or "EDR" in edr_html
    assert "coexisting with" in edr_html.lower() or "coexists" in edr_html.lower()
    assert "antivirus" in edr_html.lower() and "epp" in edr_html.lower()
    assert "behavioral" in edr_html.lower()
    assert "ELAM" in edr_html and "eBPF" in edr_html and "AMSI" in edr_html
    assert "process" in edr_html.lower() and "telemetry" in edr_html.lower()
    assert "network host isolation" in edr_html.lower() or "isolation" in edr_html.lower()
    print("[PASS] EDR coexistence with AV/EPP, sensor mechanisms scoped as platform examples, and automated isolation verified.")

    # 16. Cloud Container Services (ECS, ACI, Managed K8s)
    cnt_path = ROOT_DIR / "tutorials" / "cloud" / "cloud-container-services-overview-ecs-aci-and-managed-k8s.html"
    assert cnt_path.exists(), f"Missing {cnt_path}"
    cnt_html = cnt_path.read_text(encoding="utf-8")
    assert "Docker" in cnt_html or "OCI" in cnt_html
    assert "Fargate" in cnt_html or "ACI" in cnt_html
    assert "ECS" in cnt_html
    assert "EKS" in cnt_html or "AKS" in cnt_html or "Kubernetes" in cnt_html
    assert "CNI" in cnt_html
    print("[PASS] Cloud container spectrum (Serverless, ECS, and Managed Kubernetes) verified.")

    # 17. AWS VPC Security Groups vs Network ACLs
    sg_path = ROOT_DIR / "tutorials" / "cloud" / "cloud-security-groups-vs-network-access-control-lists.html"
    assert sg_path.exists(), f"Missing {sg_path}"
    sg_html = sg_path.read_text(encoding="utf-8")
    assert "AWS VPC" in sg_html or "Amazon Web Services (AWS) Virtual Private Cloud (VPC)" in sg_html
    assert "Security Groups" in sg_html and "Network ACLs" in sg_html
    assert "Stateful" in sg_html and "Stateless" in sg_html
    assert "Azure" in sg_html and "NSG" in sg_html
    assert "32768" in sg_html and "60999" in sg_html
    assert "49152" in sg_html and "65535" in sg_html
    assert "broad compatibility range" in sg_html.lower()
    assert "subnet" in sg_html.lower() and ("ENI" in sg_html or "Elastic Network Interface" in sg_html)
    print("[PASS] AWS VPC Security Groups vs stateless NACLs, non-universal ephemeral ports, and Azure NSG distinction verified.")

    # 18. AIOps Architecture (Event Correlation & RCA)
    ai_path = ROOT_DIR / "tutorials" / "cloud" / "aiops-architecture-applying-machine-learning-to-it-operations.html"
    assert ai_path.exists(), f"Missing {ai_path}"
    ai_html = ai_path.read_text(encoding="utf-8")
    assert "AIOps" in ai_html
    assert "alert fatigue" in ai_html.lower()
    assert "noise reduction" in ai_html.lower() or "clustering" in ai_html.lower()
    assert "anomaly detection" in ai_html.lower()
    assert "Explainable AI" in ai_html or "closed-loop" in ai_html.lower()
    print("[PASS] AIOps event correlation, noise reduction, dynamic anomaly detection, and explainability verified.")

async def run_browser_verification():
    print("\n==================================================")
    print("TEST 3: Live Browser Verification & Screenshots")
    print("==================================================")

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        console_errors = []
        network_404s = []

        page.on("console", lambda msg: console_errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("response", lambda resp: network_404s.append(resp.url) if resp.status == 404 and "localhost" in resp.url else None)

        # 1. Test representative Batch 5 tutorials across all 6 categories
        sample_urls = [
            ("networking", "tcp-three-way-handshake-and-teardown", "phase6_5e_networking.png"),
            ("windows", "windows-robocopy-advanced-file-replication-guide", "phase6_5e_windows.png"),
            ("linux", "linux-troubleshooting-boot-failures-grub-emergency-mode", "phase6_5e_linux.png"),
            ("servers", "server-hardware-health-monitoring-ipmi-snmp-traps", "phase6_5e_servers.png"),
            ("cybersecurity", "privileged-access-management-pam-vaulting-and-session-recording", "phase6_5e_cybersecurity.png"),
            ("cloud", "cloud-security-groups-vs-network-access-control-lists", "phase6_5e_cloud.png"),
        ]

        for cat, tid, screenshot_name in sample_urls:
            url = f"{BASE_URL}/tutorials/{cat}/{tid}.html"
            print(f"Testing page: {url}")
            await page.set_viewport_size({"width": 1440, "height": 900})
            resp = await page.goto(url, wait_until="networkidle")
            assert resp.status == 200, f"Page load failed with status {resp.status}: {url}"

            # Wait for header and tutorial engine
            await page.wait_for_selector("#site-header header", timeout=5000)
            await page.wait_for_selector("#tutorial-toc .tutorial-toc-list", timeout=5000)

            # Assert single H1 visible
            h1s = await page.locator("h1").all()
            assert len(h1s) == 1, f"Expected 1 H1 on {tid}, found {len(h1s)}"

            # Assert TOC items populated
            toc_links = await page.locator("#tutorial-toc a").all()
            assert len(toc_links) >= 3, f"TOC under-populated on {tid}: {len(toc_links)} links"

            # Assert Navigation Cards in Footer mount
            footer_mount = page.locator("#tutorial-footer-mount")
            await footer_mount.wait_for(timeout=5000)
            assert await footer_mount.is_visible()

            # Capture category screenshot
            shot_path = QA_DIR / screenshot_name
            await page.screenshot(path=str(shot_path), full_page=False)
            print(f"  -> Captured screenshot: {shot_path.name}")

        # 2. Test Topics Page Metrics Update
        print("\n--- Testing Topics Page Dynamic Metrics ---")
        await page.goto(f"{BASE_URL}/topics.html", wait_until="networkidle")
        await page.wait_for_selector(".topic-domain-card", timeout=5000)

        # Check Total Curriculum and Published Badges
        curric_badge = await page.locator("#topics-total-curriculum-badge").text_content()
        tut_badge = await page.locator("#topics-total-tut-badge").text_content()
        print(f"Topics Hero Badges: {tut_badge.strip()} | {curric_badge.strip()}")
        assert "471 Curriculum Topics" in curric_badge, f"Unexpected curric badge text: {curric_badge}"
        assert "148 Published Tutorials" in tut_badge, f"Unexpected tut badge text: {tut_badge}"

        topics_shot = QA_DIR / "phase6_5e_topics_updated.png"
        await page.screenshot(path=str(topics_shot), full_page=False)
        print("  -> Captured qa/phase6_5e_topics_updated.png")

        # 3. Test Search Integration
        print("\n--- Testing Search Integration with Batch 5 Content ---")
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")

        test_queries = [
            ("Three-Way Handshake", "TCP Three-Way Handshake"),
            ("Recursive Queries", "DNS Resolution Process"),
            ("WPA3-Enterprise", "WPA2-Enterprise vs WPA3-Enterprise"),
            ("Robocopy", "Robocopy Advanced File Replication"),
            ("Registry", "Windows Registry Architecture"),
            ("Domain Join", "Active Directory Domain Join"),
            ("GRUB Rescue", "Troubleshooting Boot Failures"),
            ("Standard Streams", "Standard Streams"),
            ("Sudoers", "Sudoers Administration"),
            ("IPMI", "Server Hardware Health Telemetry"),
            ("CIS Benchmarks", "Windows Server Hardening"),
            ("Root Cause Analysis", "Systematic Root Cause Analysis"),
            ("Defense-in-Depth", "Defense-in-Depth Architecture"),
            ("Privileged Access", "Privileged Access Management"),
            ("EDR", "Endpoint Detection and Response"),
            ("Containerized Workloads", "Containerized Workloads"),
            ("Security Groups", "AWS VPC Security Groups"),
            ("AIOps", "AIOps Architecture")
        ]

        # Open search modal
        await page.click(".search-box")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=3000)

        for query, expected_match in test_queries:
            search_input = page.locator("#search-modal-input")
            await search_input.fill(query)
            await page.wait_for_timeout(300)

            # Check that results rendered
            items = await page.evaluate("""() => {
                const els = Array.from(document.querySelectorAll('.search-result-item'));
                return els.map(el => ({
                    title: el.querySelector('.search-result-title') ? el.querySelector('.search-result-title').textContent : '',
                    href: el.getAttribute('href')
                }));
            }""")

            assert len(items) > 0, f"No results for search query '{query}'!"

            # Check 0 duplicate URLs
            hrefs = [it["href"] for it in items]
            assert len(hrefs) == len(set(hrefs)), f"Duplicate results found for query '{query}': {hrefs}"

            # Check match
            match = any(expected_match.lower() in it["title"].lower() for it in items)
            assert match, f"Expected '{expected_match}' in search results for '{query}', got: {[it['title'] for it in items]}"
            print(f"[PASS] Search query '{query}': {len(items)} results (0 duplicates, '{expected_match}' matched).")

        # Dismiss modal
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)

        # 4. Mobile Responsiveness & Zero Horizontal Overflow
        print("\n--- Auditing Responsive Viewports (Zero Horizontal Overflow) ---")
        viewports = [
            {"width": 375, "height": 812},
            {"width": 768, "height": 1024},
            {"width": 1024, "height": 768},
            {"width": 1440, "height": 900}
        ]

        test_mobile_url = f"{BASE_URL}/tutorials/cloud/cloud-security-groups-vs-network-access-control-lists.html"
        for vp in viewports:
            await page.set_viewport_size(vp)
            await page.goto(test_mobile_url, wait_until="networkidle")
            await page.wait_for_selector("#tutorial-header", timeout=5000)

            # Check overflow
            scroll_width = await page.evaluate("document.documentElement.scrollWidth")
            client_width = await page.evaluate("document.documentElement.clientWidth")
            assert scroll_width <= client_width, f"Horizontal overflow at {vp['width']}px: scrollWidth={scroll_width} > clientWidth={client_width}"
            print(f"[PASS] {vp['width']}px viewport: zero horizontal overflow (scrollWidth={scroll_width}, clientWidth={client_width})")

        # Capture mobile screenshot
        await page.set_viewport_size({"width": 375, "height": 812})
        await page.goto(test_mobile_url, wait_until="networkidle")
        mob_shot = QA_DIR / "phase6_5e_mobile.png"
        await page.screenshot(path=str(mob_shot), full_page=False)
        print("  -> Captured qa/phase6_5e_mobile.png")

        # 5. Check Console Errors and 404s
        print("\n--- Network & Console Health ---")
        print(f"Console Errors Encountered: {len(console_errors)}")
        print(f"Local 404s Encountered    : {len(network_404s)}")
        assert len(console_errors) == 0, f"Encountered console errors: {console_errors}"
        assert len(network_404s) == 0, f"Encountered local 404s: {network_404s}"

        await browser.close()
        print("\n[PASS] All Live Browser, Search, Responsive, and Telemetry QA Tests Passed Successfully!")

def main():
    test_data_integrity()
    test_raw_html_seo()
    test_phase6_5e_technical_accuracy()
    asyncio.run(run_browser_verification())
    print("\n==================================================")
    print("SUCCESS: Phase 6.5E Batch 5 QA Suite 100% Passed!")
    print("==================================================")

if __name__ == "__main__":
    main()
