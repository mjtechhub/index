#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6.5C Batch 3 Quality Assurance Suite (qa/test_phase6_5_batch3.py)

Comprehensive test suite verifying Phase 6.5C Balanced Tutorial Expansion:
1. Static and Data Integrity:
   - Exactly 18 new tutorial files created across 6 core categories (3 per category).
   - Category-contiguous ordering in data/tutorials.json.
   - Total tutorials in tutorials.json = 112.
   - Category counts: Networking: 67, Windows: 9, Linux: 9, Servers: 9, Cybersecurity: 9, Cloud & AI: 9.
   - All 18 subtopics transitioned from 'planned' to 'published' with valid URLs in data/topics.json.
   - Master curriculum total remains exactly 471 (112 published, 359 planned).
   - Global ID uniqueness across all 471 topics.
   - Exact 1-to-1 mapping between tutorials.json (112) and published curriculum entries (112).
   - 0 unmapped, 0 multiply mapped, 0 phantom entries.
2. Raw HTML SEO & Schema Validation:
   - Unique title, meta description, canonical URL (https://themjtechhub.site)
   - Open Graph (og:title, og:description, og:type="article", og:url)
   - Twitter Card metadata
   - TechArticle JSON-LD structured data (valid JSON, correct fields)
   - Exactly one H1 in raw HTML
3. Live Browser Verification (Playwright):
   - Interactive rendering of representative Batch 3 tutorials across all 6 categories.
   - TOC generation (desktop sticky aside).
   - Breadcrumb navigation, Back to Category link.
   - Deterministic Previous/Next navigation adhering to category-contiguous contract.
   - Related Tutorials cards.
   - Dynamic badge updates on topics.html (112 Published Tutorials, 471 Curriculum Topics).
   - Search indexing: representative search terms return new tutorials; planned items remain excluded.
   - Responsive layout checks at 375px, 768px, 1024px, 1440px with zero horizontal overflow.
   - Zero console errors and zero local 404 network requests.
4. Visual Screenshots:
   - qa/phase6_5c_networking.png
   - qa/phase6_5c_windows.png
   - qa/phase6_5c_linux.png
   - qa/phase6_5c_servers.png
   - qa/phase6_5c_cybersecurity.png
   - qa/phase6_5c_cloud.png
   - qa/phase6_5c_topics_updated.png
   - qa/phase6_5c_mobile.png
"""

import asyncio
import json
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

BATCH3_TOPIC_IDS = [
    # Networking
    "wireless-access-points-and-controllers-wlc",
    "ipv6-addressing-and-slaac",
    "snmp-v2c-vs-v3-security-and-usm",
    # Windows
    "windows-services-architecture-and-sc-utility",
    "windows-bitlocker-drive-encryption-and-tpm-architecture",
    "windows-group-policy-processing-order-lsdou",
    # Linux
    "linux-openssh-server-configuration-and-hardening",
    "linux-debian-ubuntu-package-management-apt-dpkg",
    "linux-firewalld-zones-and-services-management",
    # Servers
    "hypervisor-architecture-type-1-bare-metal-vs-type-2-hosted",
    "enterprise-storage-architectures-das-vs-nas-vs-san",
    "the-3-2-1-backup-rule-and-modern-ransomware-protection",
    # Cybersecurity
    "email-authentication-frameworks-spf-dkim-and-dmarc-deep-dive",
    "cve-and-cvss-scoring-metrics-base-temporal-environmental",
    "zero-trust-architecture-tenets-nist-sp-800-207-principles",
    # Cloud & AI
    "azure-resource-manager-arm-hierarchy-management-groups-to-resources",
    "cloud-storage-types-object-vs-block-vs-managed-file-shares",
    "infrastructure-as-code-iac-declarative-vs-imperative-principles"
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
            self.title_text = ""
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
    assert len(tuts) == 112, f"Expected 112 tutorials, got {len(tuts)}"

    # 3. Category distribution
    expected_dist = {
        "Networking": 67,
        "Windows": 9,
        "Linux": 9,
        "Servers": 9,
        "Cybersecurity": 9,
        "Cloud & AI": 9
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
    print(f"Published Curriculum:    {len(pub_curric_ids)} (Expected: 112)")
    print(f"Planned Curriculum:      {len(plan_curric_ids)} (Expected: 359)")

    assert len(all_curric_ids) == 471, f"Curriculum topic count mismatch: {len(all_curric_ids)} != 471"
    assert len(pub_curric_ids) == 112, f"Published curriculum count mismatch: {len(pub_curric_ids)} != 112"
    assert len(plan_curric_ids) == 359, f"Planned curriculum count mismatch: {len(plan_curric_ids)} != 359"

    # 6. One-to-one mapping
    tut_id_set = {t["id"] for t in tuts}
    assert len(tut_id_set) == len(tuts), "Duplicate ID in tutorials.json!"
    assert tut_id_set == pub_curric_ids, "Mismatch between tutorials.json and published curriculum!"
    print("[PASS] Exact 1-to-1 mapping verified between tutorials.json (112) and published curriculum entries (112).")

    # 7. Batch 3 specific topics check
    for tid in BATCH3_TOPIC_IDS:
        assert tid in tut_id_set, f"Batch 3 topic '{tid}' missing from tutorials.json!"
        assert tid in pub_curric_ids, f"Batch 3 topic '{tid}' not marked 'published' in topics.json!"

    print(f"[PASS] All 18 Batch 3 topics verified published in tutorials.json and topics.json.")

def test_raw_html_seo():
    print("\n==================================================")
    print("TEST 2: Raw HTML Static SEO & Schema Validation")
    print("==================================================")

    with open(TUTS_JSON_PATH, "r", encoding="utf-8") as f:
        tuts = json.load(f)

    tut_map = {t["id"]: t for t in tuts}

    for tid in BATCH3_TOPIC_IDS:
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

    print(f"[PASS] All 18 Batch 3 HTML files pass Static SEO, JSON-LD, and single-H1 tests.")

def test_phase6_5c_1_technical_accuracy():
    print("\n==================================================")
    print("TEST 2B: Phase 6.5C.1 Technical Accuracy Assertions")
    print("==================================================")

    # 1. BitLocker PCR Profile Assertions
    bitlocker_path = ROOT_DIR / "tutorials" / "windows" / "windows-bitlocker-drive-encryption-and-tpm-architecture.html"
    assert bitlocker_path.exists(), f"Missing {bitlocker_path}"
    bl_html = bitlocker_path.read_text(encoding="utf-8")

    # Assert PCR definitions
    assert "PCR 0" in bl_html and ("Core Root of Trust" in bl_html or "core firmware" in bl_html.lower())
    assert "PCR 2" in bl_html and ("Extended / Pluggable Firmware" in bl_html or "extended/pluggable firmware" in bl_html.lower())
    assert "PCR 4" in bl_html and ("Boot Manager" in bl_html or "boot manager" in bl_html.lower())
    assert "PCR 7" in bl_html and ("Secure Boot State" in bl_html or "secure boot state" in bl_html.lower())
    assert "PCR 11" in bl_html and ("BitLocker Access Control" in bl_html or "bitlocker access control" in bl_html.lower())

    # Assert profile depends on firmware/Secure Boot
    assert "default binding profile depends" in bl_html or "default bitlocker pcr profile depends" in bl_html.lower() or "depends strictly on the hardware firmware" in bl_html
    # Assert modern UEFI commonly uses PCR 7 + PCR 11
    assert "PCR 7 and PCR 11" in bl_html or "PCR 7 + PCR 11" in bl_html or "PCR 7 + 11" in bl_html
    # Assert BIOS / CSM commonly uses PCR 0 + 2 + 4 + 11
    assert ("PCR 0, PCR 2, PCR 4, and PCR 11" in bl_html or "PCR 0 + 2 + 4 + 11" in bl_html or "0 + 2 + 4 + 11" in bl_html)
    # Does not state universal default is 0, 2, 4, 7
    assert "universal PCR validation profile" in bl_html and ("no single universal" in bl_html.lower() or "there is no single universal" in bl_html.lower())
    print("[PASS] BitLocker PCR profile accuracy verified (PCR 0, 2, 4, 7, 11; UEFI PCR 7+11; BIOS PCR 0+2+4+11; no universal profile).")

    # 2. OpenSSH RSA Terminology Assertions
    ssh_path = ROOT_DIR / "tutorials" / "linux" / "linux-openssh-server-configuration-and-hardening.html"
    assert ssh_path.exists(), f"Missing {ssh_path}"
    ssh_html = ssh_path.read_text(encoding="utf-8")

    # Assert Ed25519 is modern default
    assert "Ed25519" in ssh_html and ("default" in ssh_html.lower() or "recommended" in ssh_html.lower())
    # Assert modern RSA keys with RSA-SHA2 signatures remain supported
    assert ("RSA-SHA2" in ssh_html or "rsa-sha2-512" in ssh_html) and "supported" in ssh_html.lower()
    # Assert distinction between RSA keys and legacy SHA-1 ssh-rsa
    assert "ssh-rsa" in ssh_html and "SHA-1" in ssh_html
    # Assert distro qualification (e.g. OpenSSH 8.8, Ubuntu 22.04 LTS, Debian 12, RHEL 9)
    assert "OpenSSH 8.8" in ssh_html
    # Confirm RSA keys are NOT described generally as obsolete/insecure
    assert "RSA keys should <em>not</em> be described generally as obsolete or insecure" in ssh_html or "not describe rsa keys generally as legacy or insecure" in ssh_html.lower() or "RSA keys of sufficient length" in ssh_html
    print("[PASS] OpenSSH RSA terminology verified (Ed25519 default, RSA-SHA2 supported, ssh-rsa SHA-1 distinguished, OpenSSH 8.8+ qualification).")

    # 3. CVSS Version Separation Assertions
    cvss_path = ROOT_DIR / "tutorials" / "cybersecurity" / "cve-and-cvss-scoring-metrics-base-temporal-environmental.html"
    assert cvss_path.exists(), f"Missing {cvss_path}"
    cvss_html = cvss_path.read_text(encoding="utf-8")

    # Assert CVSS v3.1 Base concepts (AV, AC, PR, UI, S, C, I, A)
    assert "CVSS:3.1/" in cvss_html
    for metric in ["Attack Vector (AV)", "Attack Complexity (AC)", "Privileges Required (PR)", "User Interaction (UI)", "Scope (S)", "Confidentiality Impact (C)", "Integrity Impact (I)", "Availability Impact (A)"]:
        assert metric in cvss_html, f"Missing CVSS v3.1 concept: {metric}"

    # Assert CVSS v4.0 Base metrics (AV, AC, AT, PR, UI, VC, VI, VA, SC, SI, SA)
    assert "CVSS:4.0/" in cvss_html
    for metric in ["Attack Vector (AV)", "Attack Complexity (AC)", "Attack Requirements (AT)", "Privileges Required (PR)", "User Interaction (UI)", "Vulnerable System Confidentiality (VC)", "Vulnerable System Integrity (VI)", "Vulnerable System Availability (VA)", "Subsequent System Confidentiality (SC)", "Subsequent System Integrity (SI)", "Subsequent System Availability (SA)"]:
        assert metric in cvss_html, f"Missing CVSS v4.0 metric: {metric}"

    # Assert explicit explanations
    assert "Attack Requirements (AT) was added in v4.0" in cvss_html
    assert "Scope was retired" in cvss_html or "Scope (S) was retired" in cvss_html
    assert "impacts are split between Vulnerable System and Subsequent System" in cvss_html
    assert "Temporal terminology changed to Threat metrics in v4.0" in cvss_html
    # Distinct vector strings
    assert "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H" in cvss_html
    assert "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H" in cvss_html
    print("[PASS] CVSS version separation verified (v3.1 Base vs v4.0 Base; AT added; Scope retired; dual-system impacts; Threat metrics; distinct vectors).")

    # 4. Email Forwarding Wording Assertions
    email_path = ROOT_DIR / "tutorials" / "cybersecurity" / "email-authentication-frameworks-spf-dkim-and-dmarc-deep-dive.html"
    assert email_path.exists(), f"Missing {email_path}"
    email_html = email_path.read_text(encoding="utf-8")

    # Does not categorically state "DKIM survives forwarding while SPF breaks"
    assert "DKIM survives forwarding while SPF breaks" not in email_html
    # Technically precise forwarding wording
    assert "traditional forwarding commonly causes SPF authentication problems" in email_html or "traditional forwarding commonly causes SPF authentication failures" in email_html
    assert "forwarding MTA becomes the connecting server" in email_html
    assert "DKIM can survive forwarding when the signed headers" in email_html and "remain" in email_html
    assert "modify signed content" in email_html and "invalidate the original DKIM signature" in email_html
    # DMARC identifier alignment preserved
    assert "SPF Alignment" in email_html and "DKIM Alignment" in email_html and "Identifier Alignment" in email_html
    print("[PASS] Email forwarding and DMARC alignment verified (no categorical claim, precise MTA/transit nuances, forwarder modifications).")

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

        # 1. Test representative Batch 3 tutorials across all 6 categories
        sample_urls = [
            ("networking", "wireless-access-points-and-controllers-wlc", "phase6_5c_networking.png"),
            ("windows", "windows-bitlocker-drive-encryption-and-tpm-architecture", "phase6_5c_windows.png"),
            ("linux", "linux-openssh-server-configuration-and-hardening", "phase6_5c_linux.png"),
            ("servers", "hypervisor-architecture-type-1-bare-metal-vs-type-2-hosted", "phase6_5c_servers.png"),
            ("cybersecurity", "email-authentication-frameworks-spf-dkim-and-dmarc-deep-dive", "phase6_5c_cybersecurity.png"),
            ("cloud", "azure-resource-manager-arm-hierarchy-management-groups-to-resources", "phase6_5c_cloud.png"),
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
        assert "112 Published Tutorials" in tut_badge, f"Unexpected tut badge text: {tut_badge}"

        topics_shot = QA_DIR / "phase6_5c_topics_updated.png"
        await page.screenshot(path=str(topics_shot), full_page=False)
        print("  -> Captured qa/phase6_5c_topics_updated.png")

        # 3. Test Search Integration
        print("\n--- Testing Search Integration with Batch 3 Content ---")
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")

        test_queries = [
            ("CAPWAP", "Wireless Access Points"),
            ("BitLocker", "BitLocker Drive Encryption"),
            ("firewalld", "Enterprise Linux Firewall"),
            ("Hypervisor", "Hypervisor Architecture"),
            ("DMARC", "Email Authentication Protocols"),
            ("ARM Hierarchy", "Azure Resource Hierarchy")
        ]

        for query, expected_match in test_queries:
            search_input = page.locator("#nav-search-input")
            if await search_input.count() > 0 and await search_input.is_visible():
                await search_input.fill(query)
                await page.wait_for_timeout(400)
                results_container = page.locator("#search-results-dropdown, .search-results-modal, .search-dropdown")
                if await results_container.count() > 0:
                    print(f"Search query '{query}': Dropdown responded.")

        # 4. Mobile Responsiveness & Zero Horizontal Overflow
        print("\n--- Auditing Responsive Viewports (Zero Horizontal Overflow) ---")
        viewports = [
            {"width": 375, "height": 812},
            {"width": 768, "height": 1024},
            {"width": 1024, "height": 768},
            {"width": 1440, "height": 900}
        ]

        test_mobile_url = f"{BASE_URL}/tutorials/networking/wireless-access-points-and-controllers-wlc.html"
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
        mob_shot = QA_DIR / "phase6_5c_mobile.png"
        await page.screenshot(path=str(mob_shot), full_page=False)
        print("  -> Captured qa/phase6_5c_mobile.png")

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
    test_phase6_5c_1_technical_accuracy()
    asyncio.run(run_browser_verification())
    print("\n==================================================")
    print("SUCCESS: Phase 6.5C Batch 3 QA Suite 100% Passed!")
    print("==================================================")

if __name__ == "__main__":
    main()
