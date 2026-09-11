import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_PATH = ROOT_DIR / "data" / "topics.json"
TUTS_PATH = ROOT_DIR / "data" / "tutorials.json"

with open(TOPICS_PATH, "r", encoding="utf-8") as f:
    topics_data = json.load(f)

with open(TUTS_PATH, "r", encoding="utf-8") as f:
    tuts_data = json.load(f)

existing_ids = {t["id"] for t in tuts_data}
existing_urls = {t["url"] for t in tuts_data}

# Final 18 topics incorporating CTO corrections
final_topics = [
    # NETWORKING (3)
    {
        "cat_id": "networking",
        "id": "dhcp-dora-process-and-options-architecture",
        "title": "DHCP DORA Process & Common DHCP Options: Router, DNS and TFTP",
        "reason": "Tied for lowest coverage section in Networking (50.0%). Covers core network services, client discovery, broadcast vs unicast DORA semantics, and common options (3, 6, 66) with IP Helper PXE guidance.",
        "override": "None (Direct algorithm match)"
    },
    {
        "cat_id": "networking",
        "id": "wireless-roaming-802-11r-k-v-standards",
        "title": "Seamless Wireless Roaming Standards: 802.11r, 802.11k & 802.11v",
        "reason": "Tied for lowest coverage section in Networking (50.0%). Adds enterprise wireless depth covering 802.11k neighbor reports, 802.11v BSS transition management, and 802.11r Fast BSS Transition, maintaining client-decision primacy.",
        "override": "None (Direct algorithm match)"
    },
    {
        "cat_id": "networking",
        "id": "chassis-stacking-and-switch-virtualization",
        "title": "Switch Stacking Architecture, Virtual Chassis & Multi-Chassis Link Aggregation",
        "reason": "Enterprise switching & high availability depth (66.7% coverage). Differentiates physical stacking, virtual chassis, and MLAG/vPC/VSS control-plane architectures.",
        "override": "None (Direct algorithm match)"
    },

    # WINDOWS (3)
    {
        "cat_id": "windows",
        "id": "windows-remote-desktop-protocol-rdp-configuration",
        "title": "Remote Desktop Protocol (RDP) Configuration, Port & NLA Security",
        "reason": "Resolves zero-published Section 6 (Windows Networking & Remote Access). Establishes secure remote management standards (TCP/UDP 3389, NLA via CredSSP, TLS, firewall rules, Restricted Admin mode).",
        "override": "None (Resolves zero-published section)"
    },
    {
        "cat_id": "windows",
        "id": "windows-defender-firewall-with-advanced-security",
        "title": "Windows Defender Firewall with Advanced Security: Rules & Profiles",
        "reason": "Endpoint security coverage (12.5% ratio). Covers Domain/Private/Public profiles, rule precedence, program/service/port scopes, connection security rules (IPsec), and PowerShell automation.",
        "override": "None (Tied for lowest populated ratio: 12.5%)"
    },
    {
        "cat_id": "windows",
        "id": "windows-update-for-business-wufb-deployment-rings",
        "title": "Windows Update Client Policies: Deployment Rings, Deferrals & Deadlines",
        "reason": "Resolves zero-published Section 9 (Enterprise Updates, Deployment & Management). Details modern Windows 11 client policies (formerly WUfB), deployment rings, deferrals, deadlines, and WSUS/Intune contrast.",
        "override": "None (Resolves zero-published section)"
    },

    # LINUX (3)
    {
        "cat_id": "linux",
        "id": "linux-lvm-architecture-physical-volumes-volume-groups",
        "title": "Logical Volume Manager (LVM) Architecture: PV, VG and LV Provisioning",
        "reason": "Lowest ratio among populated Linux sections (11.1%). Details PV, VG, LV, PE/LE allocation, safe extension/reduction workflows, filesystem resizing constraints, and prominent shrink warnings.",
        "override": "None (Lowest ratio populated section: 11.1%)"
    },
    {
        "cat_id": "linux",
        "id": "linux-process-signaling-and-termination-kill-pkill",
        "title": "Process Termination & POSIX Signals: SIGTERM, SIGKILL, SIGHUP (kill/pkill)",
        "reason": "Process management fundamentals (14.3% ratio). Details PID/PPID, process states, job control, POSIX signals (SIGTERM 15, SIGKILL 9, SIGHUP 1), and why kill -9 should not be the default.",
        "override": "SELECTION OVERRIDE: Prioritizes foundational POSIX process lifecycle, job control, and signal management (Sec 5) over boot recovery (Sec 10) as an operational prerequisite mandated by Section 16 directives. Sec 10 boot recovery deferred to Batch 5."
    },
    {
        "cat_id": "linux",
        "id": "linux-systemd-journalctl-log-analysis-and-filtering",
        "title": "Systemd Journal Architecture & Advanced journalctl Filtering Queries",
        "reason": "System logging & telemetry (14.3% ratio). Details systemd-journald architecture, persistent storage, boot/unit/priority filtering, and vacuuming maintenance.",
        "override": "SELECTION OVERRIDE: Prioritizes centralized systemd journal analysis and logging architecture (Sec 8) over boot recovery (Sec 10) as an operational telemetry prerequisite mandated by Section 15 directives."
    },

    # SERVERS (3)
    {
        "cat_id": "servers",
        "id": "windows-server-core-headless-deployment-and-remote-management",
        "title": "Windows Server Core: Headless Installation & Remote Administration",
        "reason": "Modern Windows Server 2022/2025 Server Core administration via PowerShell, Windows Admin Center (WAC), Server Manager, and WinRM HTTPS remoting.",
        "override": "SELECTION OVERRIDE: Prioritizes foundational headless Windows Server 2022/2025 OS deployment and modern remote administration (WAC, PowerShell, WinRM) mandated by Section 19 directives before advanced telemetry and diagnostics. Sec 8, 9, 10 scheduled for Batches 5 and 6."
    },
    {
        "cat_id": "servers",
        "id": "enterprise-dhcp-failover-load-balancing-and-hot-standby",
        "title": "Windows Server DHCP Failover: Load Balance vs Hot Standby Modes",
        "reason": "Windows Server DHCP Failover in Load Balance (hash-based sharing) vs Hot Standby (Active/Standby with reserve), MCLT state machine, partner communication (TCP 647), and DHCPv4-only scope.",
        "override": "SELECTION OVERRIDE: Prioritizes enterprise IP core infrastructure resilience (DHCP failover, Load Balance vs Hot Standby, MCLT) mandated by Section 20 directives, complementing the Networking DORA expansion in this batch."
    },
    {
        "cat_id": "servers",
        "id": "windows-server-failover-clustering-wsfc-architecture",
        "title": "Windows Server Failover Clustering (WSFC) Architecture & Validation Tests",
        "reason": "Enterprise high availability foundations (WSFC clustering, quorum models, witness types, cluster networks/heartbeats, workload failover) mandated by Section 21 directives.",
        "override": "SELECTION OVERRIDE: Prioritizes enterprise high availability foundations (WSFC clustering, quorum models, witness types) mandated by Section 21 directives, establishing the infrastructure clustering baseline required prior to server security hardening."
    },

    # CYBERSECURITY (3)
    {
        "cat_id": "cybersecurity",
        "id": "single-sign-on-sso-architecture-saml-2-0-and-oidc",
        "title": "Enterprise Single Sign-On (SSO): SAML 2.0 Assertions vs OpenID Connect Tokens",
        "reason": "Rigorous separation: SAML 2.0 (federated assertions, IdP/SP), OAuth 2.0 (authorization framework, tokens), OIDC (identity/authentication layer over OAuth 2.0).",
        "override": "SELECTION OVERRIDE: Prioritizes enterprise federated identity and authentication protocol demarcation (SAML 2.0 vs OAuth 2.0 vs OIDC) mandated by Section 23 directives over Sec 1 risk governance (11.1%) and Sec 2 IAM (12.5%)."
    },
    {
        "cat_id": "cybersecurity",
        "id": "security-information-and-event-management-siem-architecture",
        "title": "Security Information and Event Management (SIEM): Log Ingestion, Parsing & Indexing",
        "reason": "Resolves zero-published Section 8 (Centralized Logging, SIEM & Security Monitoring). Collection, normalization (CEF/ECS), enrichment, correlation engines, detections, and SIEM/EDR/SOAR distinctions.",
        "override": "None (Resolves zero-published section)"
    },
    {
        "cat_id": "cybersecurity",
        "id": "nist-sp-800-61-computer-security-incident-handling-guide",
        "title": "NIST SP 800-61 Rev. 3: Incident Response with the CSF 2.0 Lifecycle",
        "reason": "Resolves zero-published Section 9 (Incident Response & Threat Containment). Implements current NIST SP 800-61 Rev. 3 (final April 2025) with CSF 2.0 lifecycle (Govern/Identify/Protect -> Detect/Respond/Recover).",
        "override": "None (Resolves zero-published section)"
    },

    # CLOUD & AI (3)
    {
        "cat_id": "cloud",
        "id": "serverless-computing-architecture-and-event-driven-design",
        "title": "Serverless Computing Concepts: Function-as-a-Service (FaaS) & Event Triggers",
        "reason": "Vendor-neutral serverless computing architecture, execution models, cold starts, concurrency, event sources, stateless design, and managed infrastructure.",
        "override": "SELECTION OVERRIDE: Prioritizes cloud serverless / FaaS execution model principles mandated by Section 27 directives over container orchestration (Sec 5) and AIOps (Sec 10)."
    },
    {
        "cat_id": "cloud",
        "id": "azure-virtual-networks-vnet-subnets-and-peering-architecture",
        "title": "Azure VNet Architecture: Subnet Delegation, Peering & Service Endpoints",
        "reason": "Azure virtual networking (12.5% ratio). Subnet delegation, NSGs, ASGs, Private Endpoints, and non-transitive VNet peering routing architecture.",
        "override": "SELECTION OVERRIDE: Prioritizes foundational Azure VNet architecture, subnet delegation, and peering mechanics mandated by Section 29 directives to achieve parity with existing AWS VPC coverage, before multi-cloud hybrid transit (Sec 6)."
    },
    {
        "cat_id": "cloud",
        "id": "finops-fundamentals-cloud-financial-management-and-cost-allocation",
        "title": "FinOps Fundamentals: Cloud Financial Governance, Chargeback & Showback Models",
        "reason": "Resolves zero-published Section 9 (Cloud Security, Governance, Compliance & FinOps). Implements FinOps Foundation framework (Inform/Optimize/Operate, tagging taxonomy, showback vs chargeback, rightsizing).",
        "override": "None (Resolves zero-published section)"
    }
]

assert len(final_topics) == 18, f"Expected 18, got {len(final_topics)}"

errors = []
rows = []
zero_pub_resolved = 0

for item in final_topics:
    cid = item["cat_id"]
    tid = item["id"]
    target_cat = next((c for c in topics_data["categories"] if c["id"] == cid), None)
    if not target_cat:
        errors.append(f"Category {cid} not found")
        continue

    found = None
    for s_idx, sec in enumerate(target_cat.get("sections", [])):
        subs = sec.get("subtopics", [])
        spub = sum(1 for s in subs if s.get("status") == "published")
        stotal = len(subs)
        ratio = spub / stotal if stotal > 0 else 0
        for sub in subs:
            if sub["id"] == tid:
                found = {
                    "subtopic": sub,
                    "section_idx": s_idx + 1,
                    "section_name": sec["name"],
                    "section_pub": spub,
                    "section_total": stotal,
                    "section_ratio": ratio,
                    "cat_name": target_cat["name"]
                }
                break
        if found:
            break

    if not found:
        errors.append(f"Topic {tid} NOT FOUND in category {cid}")
        continue

    sub = found["subtopic"]
    if sub.get("status") != "planned":
        errors.append(f"Topic {tid} status is '{sub.get('status')}', expected 'planned'")
    if tid in existing_ids:
        errors.append(f"Collision: {tid} in tutorials.json")
    expected_url = f"tutorials/{cid}/{tid}.html"
    if expected_url in existing_urls:
        errors.append(f"Collision: URL {expected_url} in tutorials.json")

    if found["section_pub"] == 0:
        zero_pub_resolved += 1

    rows.append({
        "category": found["cat_name"],
        "id": tid,
        "title": item["title"],
        "level": sub["level"],
        "section": f"Sec {found['section_idx']}: {found['section_name']}",
        "pub": found["section_pub"],
        "total": found["section_total"],
        "ratio": f"{found['section_ratio']*100:.1f}%",
        "reason": item["reason"],
        "override": item["override"]
    })

print(f"Total evaluated: {len(rows)} | Errors: {len(errors)} | Zero-published resolved: {zero_pub_resolved}")
for r in rows:
    print(f"[{r['category']}] {r['id']} ({r['level']}) | {r['section']} ({r['pub']}/{r['total']} = {r['ratio']})")
    print(f"  Title: {r['title']}")
    print(f"  Reason: {r['reason']}")
    print(f"  Override: {r['override']}\n")

if not errors:
    print("ALL 18 CANDIDATES FULLY VALIDATED AND READY FOR BATCH 4 AUTHORING!")
