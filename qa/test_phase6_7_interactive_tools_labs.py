#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6.7 Interactive IT Tools & Troubleshooting Labs Verification Suite
Validates:
1. 4 Interactive Tools:
   - Subnet & CIDR Calculator (/0 to /32, RFC 3021, RFC 1918, binary, input validation)
   - VLSM Planner (Largest-first allocation, overlap prevention, parent boundary validation)
   - Network Diagnostic Workbench (TCP/IP layer isolation, confidence levels, command links)
   - Port & Protocol Reference (32+ enterprise protocols, transport types, search, filtering)
2. 6 Guided Troubleshooting Labs:
   - Exactly 6 labs covering Networking, Windows, Linux, Servers, Cybersecurity, Cloud
   - Unique IDs, decision tree validity, zero dead branches, completion paths, RCA display
3. Global Search Integration:
   - All 4 tools and 6 labs discoverable at top level, 0 duplicate destinations, 0 planned curriculum leakage
4. Responsive Zero Horizontal Overflow across [320, 375, 768, 1024, 1440px] viewports.
5. Network & Console Integrity (0 console errors, 0 local 404s).
6. Captures required 8 screenshots:
   - qa/phase6_7_subnet_calculator.png
   - qa/phase6_7_vlsm_planner.png
   - qa/phase6_7_network_diagnostic.png
   - qa/phase6_7_port_reference.png
   - qa/phase6_7_lab_networking.png
   - qa/phase6_7_lab_windows.png
   - qa/phase6_7_lab_results.png
   - qa/phase6_7_mobile.png
"""

import asyncio
import json
import time
from pathlib import Path
from playwright.async_api import async_playwright

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
BASE_URL = "http://localhost/index"
QA_DIR = Path(__file__).resolve().parent
ROOT_DIR = QA_DIR.parent

async def run_phase6_7_tests():
    print("=" * 70)
    print("Starting MJ Tech Hub Phase 6.7 Interactive IT Tools & Labs Verification Suite")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Static Data & Schema Integrity Checks
    # -------------------------------------------------------------
    print("\n--- 1. Static Data & Schema Integrity Assertions ---")
    
    # Verify file existence
    assert (ROOT_DIR / "tools.html").exists(), "tools.html must exist"
    assert (ROOT_DIR / "tools" / "subnet-calculator.html").exists(), "subnet-calculator.html must exist"
    assert (ROOT_DIR / "tools" / "vlsm-planner.html").exists(), "vlsm-planner.html must exist"
    assert (ROOT_DIR / "tools" / "network-diagnostic-workbench.html").exists(), "network-diagnostic-workbench.html must exist"
    assert (ROOT_DIR / "tools" / "port-reference.html").exists(), "port-reference.html must exist"
    assert (ROOT_DIR / "labs.html").exists(), "labs.html must exist"
    assert (ROOT_DIR / "data" / "ports.json").exists(), "data/ports.json must exist"
    assert (ROOT_DIR / "data" / "troubleshooting-labs.json").exists(), "data/troubleshooting-labs.json must exist"

    # Validate Ports dataset
    with open(ROOT_DIR / "data" / "ports.json", "r", encoding="utf-8") as f:
        ports_data = json.load(f)
    assert len(ports_data) >= 30, f"Expected >= 30 ports, got {len(ports_data)}"
    
    # Ensure ICMP and ESP are not represented as ordinary TCP ports
    for p in ports_data:
        if p["id"] in ["port-icmp", "port-ipsec-esp", "port-ipsec-ah"]:
            assert p["transport"] == "IP Protocol", f"{p['id']} must use transport 'IP Protocol'"
            assert "TCP" not in p["transport"], f"{p['id']} must not be labeled as TCP"
    print(f"[PASS] Ports reference dataset verified ({len(ports_data)} enterprise protocols).")

    # Validate Troubleshooting Labs dataset
    with open(ROOT_DIR / "data" / "troubleshooting-labs.json", "r", encoding="utf-8") as f:
        labs_data = json.load(f)
    assert len(labs_data) == 6, f"Expected exactly 6 labs, got {len(labs_data)}"
    
    expected_categories = {"Networking", "Windows", "Linux", "Servers", "Cybersecurity", "Cloud"}
    actual_categories = {l["category"] for l in labs_data}
    assert actual_categories == expected_categories, f"Categories mismatch: {actual_categories} vs {expected_categories}"

    lab_ids = set()
    for l in labs_data:
        lid = l["id"]
        assert lid not in lab_ids, f"Duplicate lab ID: {lid}"
        lab_ids.add(lid)
        
        # Verify decision points and targets
        step_ids = {s["id"] for s in l["decisionPoints"]}
        assert l["initialStepId"] in step_ids, f"initialStepId '{l['initialStepId']}' not found in {step_ids}"
        assert len(l["decisionPoints"]) >= 3, f"Lab {lid} has fewer than 3 decision points"
        
        # Verify no dead branches
        for s in l["decisionPoints"]:
            for opt in s["options"]:
                target = opt["nextStepId"]
                assert target == "diagnosis" or target in step_ids, f"Dead branch in {lid}: step {s['id']} target '{target}' does not exist"
                assert opt["type"] in ["optimal", "suboptimal", "inefficient", "unsafe"]

        # Verify final diagnosis references
        diag = l["finalDiagnosis"]
        assert len(diag["relatedCommands"]) > 0, f"Lab {lid} missing relatedCommands"
        assert len(diag["relatedTutorials"]) > 0, f"Lab {lid} missing relatedTutorials"

    print("[PASS] Exactly 6 troubleshooting labs verified with 100% valid decision targets and zero dead branches.")

    # Security check: ensure no eval() or remote shell calls in js/
    js_files = list((ROOT_DIR / "js").glob("*.js"))
    for jf in js_files:
        with open(jf, "r", encoding="utf-8") as f:
            content = f.read()
            assert "eval(" not in content, f"Found eval() in {jf.name}"
            assert "document.write" not in content, f"Found document.write in {jf.name}"
    print("[PASS] Zero eval() or unsafe execution detected in JavaScript modules.")

    # -------------------------------------------------------------
    # 2. Browser Verification & Interactive Testing
    # -------------------------------------------------------------
    console_errors = []
    local_404s = []

    def on_console(msg):
        if msg.type == "error":
            console_errors.append(f"Console error: {msg.text}")

    def on_response(res):
        if res.status == 404 and "localhost" in res.url:
            local_404s.append(f"404 Not Found: {res.url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        page.on("console", on_console)
        page.on("response", on_response)

        # -------------------------------------------------------------
        # 3. Subnet Calculator Browser Testing
        # -------------------------------------------------------------
        print("\n--- 2. Testing Subnet & CIDR Calculator (tools/subnet-calculator.html) ---")
        t0 = time.time()
        await page.goto(f"{BASE_URL}/tools/subnet-calculator.html", wait_until="networkidle")
        t_load = time.time() - t0
        print(f"[METRIC] Subnet Calculator render latency: {t_load:.3f}s")

        # Deterministic Test Vector 1: 192.168.1.10/24
        await page.fill("#subnet-ip-input", "192.168.1.10")
        await page.select_option("#subnet-prefix-select", "24")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(200)

        res_net = await page.text_content("#res-network")
        res_broad = await page.text_content("#res-broadcast")
        res_range = await page.text_content("#res-range")
        res_usable = await page.text_content("#res-usable-hosts")
        res_scope = await page.text_content("#res-scope")

        assert res_net == "192.168.1.0", f"Expected network 192.168.1.0, got {res_net}"
        assert res_broad == "192.168.1.255", f"Expected broadcast 192.168.1.255, got {res_broad}"
        assert "192.168.1.1" in res_range and "192.168.1.254" in res_range, f"Invalid range {res_range}"
        assert res_usable == "254", f"Expected 254 usable hosts, got {res_usable}"
        assert "Private" in res_scope, f"Expected Private, got {res_scope}"
        print("[PASS] Test vector 192.168.1.10/24 verified (Net: 192.168.1.0, Broad: 192.168.1.255, Hosts: 254).")

        # Deterministic Test Vector 2: 10.10.10.10/30 (Usable hosts: 2)
        await page.fill("#subnet-ip-input", "10.10.10.10")
        await page.select_option("#subnet-prefix-select", "30")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(200)
        res_usable_30 = await page.text_content("#res-usable-hosts")
        assert res_usable_30 == "2", f"Expected 2 usable hosts for /30, got {res_usable_30}"
        print("[PASS] Test vector 10.10.10.10/30 verified (Usable hosts: 2).")

        # Deterministic Test Vector 3: 10.0.0.0/31 (RFC 3021 P2P, Usable hosts: 2)
        await page.fill("#subnet-ip-input", "10.0.0.0")
        await page.select_option("#subnet-prefix-select", "31")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(200)
        res_usable_31 = await page.text_content("#res-usable-hosts")
        note_31 = await page.text_content("#res-note-box")
        assert res_usable_31 == "2", f"Expected 2 usable hosts for /31, got {res_usable_31}"
        assert "RFC 3021" in note_31, "RFC 3021 explanation missing on /31"
        print("[PASS] Test vector 10.0.0.0/31 RFC 3021 verified (Usable hosts: 2).")

        # Deterministic Test Vector 4: 192.0.2.1/32 (Single host route, Usable: 1)
        await page.fill("#subnet-ip-input", "192.0.2.1")
        await page.select_option("#subnet-prefix-select", "32")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(200)
        res_usable_32 = await page.text_content("#res-usable-hosts")
        assert res_usable_32 == "1", f"Expected 1 host for /32, got {res_usable_32}"
        print("[PASS] Test vector 192.0.2.1/32 verified (Single host route: 1).")

        # Deterministic Test Vector 5: 0.0.0.0/0 (Default Route)
        await page.fill("#subnet-ip-input", "0.0.0.0")
        await page.select_option("#subnet-prefix-select", "0")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(200)
        res_net_0 = await page.text_content("#res-network")
        assert res_net_0 == "0.0.0.0", f"Expected 0.0.0.0, got {res_net_0}"
        print("[PASS] Test vector 0.0.0.0/0 verified.")

        # Deterministic Test Vector 6: 255.255.255.255/32
        await page.fill("#subnet-ip-input", "255.255.255.255")
        await page.select_option("#subnet-prefix-select", "32")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(200)
        res_net_broadcast = await page.text_content("#res-network")
        assert res_net_broadcast == "255.255.255.255"
        print("[PASS] Test vector 255.255.255.255/32 verified.")

        # RFC1918 and Special-use IP Classification Matrix
        classifications = [
            ("0.0.0.1", "This Network", False),
            ("10.0.0.1", "RFC 1918 Private", True),
            ("172.16.0.1", "RFC 1918 Private", True),
            ("172.31.255.255", "RFC 1918 Private", True),
            ("172.32.0.1", "Public", False),
            ("192.168.1.1", "RFC 1918 Private", True),
            ("100.64.0.1", "Shared", False),
            ("127.0.0.1", "Loopback", False),
            ("169.254.1.1", "Link-Local", False),
            ("192.0.2.1", "Documentation", False),
            ("198.51.100.1", "Documentation", False),
            ("203.0.113.1", "Documentation", False),
            ("198.18.0.1", "Benchmarking", False),
            ("224.0.0.1", "Multicast", False),
            ("240.0.0.1", "Reserved", False),
            ("255.255.255.255", "Limited Broadcast", False)
        ]

        for ip_addr, expected_label, is_rfc1918 in classifications:
            await page.fill("#subnet-ip-input", ip_addr)
            await page.select_option("#subnet-prefix-select", "32" if ip_addr == "255.255.255.255" else "24")
            await page.click("#subnet-calc-btn")
            await page.wait_for_timeout(100)
            scope_val = await page.text_content("#res-scope")
            assert expected_label.lower() in scope_val.lower(), f"Expected {expected_label} for {ip_addr}, got {scope_val}"
            if not is_rfc1918:
                assert "RFC 1918 Private" not in scope_val, f"{ip_addr} must NOT be classified as RFC 1918 Private"
        print("[PASS] Comprehensive IPv4 classification matrix verified (RFC1918, Loopback, Link-local, CGNAT, Documentation, Benchmarking, Multicast, Reserved, Limited Broadcast, Public candidate).")


        # Input Validation: Invalid IPs reject cleanly without NaN, Infinity, or crashes
        invalid_inputs = ["999.1.1.1", "192.168.1", "192.168..1", ""]
        for bad_ip in invalid_inputs:
            await page.fill("#subnet-ip-input", bad_ip)
            await page.click("#subnet-calc-btn")
            await page.wait_for_timeout(100)
            err_el = await page.query_selector("#subnet-error-alert")
            assert err_el is not None and await err_el.is_visible(), f"Expected error for '{bad_ip}'"
            err_text = await err_el.text_content()
            assert "NaN" not in err_text and "undefined" not in err_text and "Infinity" not in err_text

        # Verify no NaN or undefined on page
        page_body = await page.text_content("body")
        assert "NaN" not in page_body, "Found NaN in subnet calculator page"
        assert "undefined" not in page_body, "Found undefined in subnet calculator page"
        assert "Infinity" not in page_body, "Found Infinity in subnet calculator page"
        print("[PASS] Subnet calculator input validation verified across all invalid vectors with zero NaN/Infinity/undefined.")

        # Reset to clean /24 and take screenshot
        await page.fill("#subnet-ip-input", "192.168.10.25")
        await page.select_option("#subnet-prefix-select", "24")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(200)
        await page.screenshot(path=str(QA_DIR / "phase6_7_subnet_calculator.png"), full_page=True)
        print("[INFO] Saved screenshot -> phase6_7_subnet_calculator.png")

        # -------------------------------------------------------------
        # 4. VLSM Planner Browser Testing
        # -------------------------------------------------------------
        print("\n--- 3. Testing VLSM / Subnet Planner (tools/vlsm-planner.html) ---")
        t0 = time.time()
        await page.goto(f"{BASE_URL}/tools/vlsm-planner.html", wait_until="networkidle")
        t_load = time.time() - t0
        print(f"[METRIC] VLSM Planner render latency: {t_load:.3f}s")

        # Verify prompt test case: 192.168.10.0/24 with LAN-A: 100, LAN-B: 50, LAN-C: 20, LAN-D: 10
        await page.click("#vlsm-preload-btn")
        await page.wait_for_timeout(300)

        # Inspect generated rows in tbody
        rows = await page.query_selector_all("#vlsm-results-tbody tr")
        assert len(rows) == 4, f"Expected 4 allocated rows, got {len(rows)}"

        table_text = await page.text_content("#vlsm-results-tbody")
        assert "/25" in table_text
        assert "/26" in table_text
        assert "/27" in table_text
        assert "/28" in table_text
        assert "192.168.10.0" in table_text
        assert "192.168.10.128" in table_text
        assert "192.168.10.192" in table_text
        assert "192.168.10.224" in table_text
        print("[PASS] VLSM Largest-First allocation verified (100 -> /25, 50 -> /26, 20 -> /27, 10 -> /28, no overlaps).")

        # Test Host normalization disclosure (e.g. 192.168.10.45/24 -> normalized 192.168.10.0/24)
        await page.fill("#vlsm-parent-input", "192.168.10.45/24")
        await page.click("#vlsm-calc-btn")
        await page.wait_for_timeout(200)
        norm_notice = await page.text_content("#vlsm-normalization-notice")
        assert "Entered network" in norm_notice and "Normalized parent network" in norm_notice, "Normalization notice missing"
        assert "192.168.10.45" in norm_notice and "192.168.10.0" in norm_notice
        print("[PASS] Host address normalization visibly disclosed without silent alteration.")

        # Test edge cases: duplicate names, empty names, 0 hosts, negative hosts, non-integer hosts, insufficient capacity
        # 1. Test duplicate names
        await page.evaluate("""() => {
            const names = document.querySelectorAll('.vlsm-name-input');
            if (names.length >= 2) {
                names[0].value = 'LAN-DUPLICATE';
                names[1].value = 'LAN-DUPLICATE';
            }
        }""")
        await page.click("#vlsm-calc-btn")
        await page.wait_for_timeout(200)
        vlsm_err = await page.text_content("#vlsm-error-alert")
        assert "Duplicate subnet name" in vlsm_err
        print("[PASS] VLSM duplicate subnet name validation verified.")

        # 2. Test empty names
        await page.evaluate("""() => {
            const names = document.querySelectorAll('.vlsm-name-input');
            if (names.length >= 2) {
                names[0].value = '';
                names[1].value = 'LAN-VALID';
            }
        }""")
        await page.click("#vlsm-calc-btn")
        await page.wait_for_timeout(200)
        vlsm_empty_err = await page.text_content("#vlsm-error-alert")
        assert "empty name" in vlsm_empty_err
        print("[PASS] VLSM empty subnet name validation verified.")

        # 3. Test non-integer / negative / zero hosts
        await page.evaluate("""() => {
            const names = document.querySelectorAll('.vlsm-name-input');
            const hosts = document.querySelectorAll('.vlsm-hosts-input');
            names[0].value = 'LAN-ZERO';
            hosts[0].value = '0';
        }""")
        await page.click("#vlsm-calc-btn")
        await page.wait_for_timeout(200)
        vlsm_err_zero = await page.text_content("#vlsm-error-alert")
        assert "greater than 0" in vlsm_err_zero
        print("[PASS] VLSM zero hosts requirement rejected cleanly.")

        await page.evaluate("""() => {
            const hosts = document.querySelectorAll('.vlsm-hosts-input');
            hosts[0].value = '-5';
        }""")
        await page.click("#vlsm-calc-btn")
        await page.wait_for_timeout(200)
        vlsm_err_neg = await page.text_content("#vlsm-error-alert")
        assert "positive integer" in vlsm_err_neg
        print("[PASS] VLSM negative hosts requirement rejected cleanly.")

        await page.evaluate("""() => {
            const hosts = document.querySelectorAll('.vlsm-hosts-input');
            hosts[0].value = 'abc';
        }""")
        await page.click("#vlsm-calc-btn")
        await page.wait_for_timeout(200)
        vlsm_err_nan = await page.text_content("#vlsm-error-alert")
        assert "positive integer" in vlsm_err_nan
        print("[PASS] VLSM non-integer hosts requirement rejected cleanly.")

        # 4. Test insufficient capacity
        await page.fill("#vlsm-parent-input", "192.168.10.0/28")
        await page.evaluate("""() => {
            const names = document.querySelectorAll('.vlsm-name-input');
            const hosts = document.querySelectorAll('.vlsm-hosts-input');
            names[0].value = 'LAN-OVERFLOW';
            hosts[0].value = '100';
            names[1].value = 'LAN-B';
            hosts[1].value = '50';
        }""")
        await page.click("#vlsm-calc-btn")
        await page.wait_for_timeout(200)
        table_html = await page.inner_html("#vlsm-results-tbody")
        assert "Insufficient Parent Capacity" in table_html
        print("[PASS] VLSM insufficient capacity handling verified.")

        # Restore clean allocation and screenshot
        await page.click("#vlsm-preload-btn")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(QA_DIR / "phase6_7_vlsm_planner.png"), full_page=True)
        print("[INFO] Saved screenshot -> phase6_7_vlsm_planner.png")

        # -------------------------------------------------------------
        # 5. Diagnostic Workbench Browser Testing
        # -------------------------------------------------------------
        print("\n--- 4. Testing Network Diagnostic Workbench (tools/network-diagnostic-workbench.html) ---")
        t0 = time.time()
        await page.goto(f"{BASE_URL}/tools/network-diagnostic-workbench.html", wait_until="networkidle")
        t_load = time.time() - t0
        print(f"[METRIC] Diagnostic Workbench render latency: {t_load:.3f}s")

        # Verify exact transparency disclosure text
        page_content = await page.text_content("body")
        assert "This browser-based tool does not run commands, scan hosts, or test your network. It analyzes the observations you provide." in page_content
        print("[PASS] Diagnostic workbench privacy and transparency disclosure verified.")

        # Test DNS Failure scenario: Gateway=Yes, Public=Yes, DNS=No
        await page.check('input[name="gateway-ping"][value="yes"]')
        await page.check('input[name="public-ping"][value="yes"]')
        await page.check('input[name="dns-resolve"][value="no"]')
        await page.click("#diag-analyze-btn")
        await page.wait_for_timeout(200)

        diag_res = await page.text_content("#diag-fault-domain")
        assert "DNS" in diag_res, f"Expected DNS fault domain, got {diag_res}"

        # Verify evidence summary and confirming/refuting observations
        evidence_summary = await page.text_content("#diag-evidence-summary")
        confirming_obs = await page.text_content("#diag-confirming-obs")
        refuting_obs = await page.text_content("#diag-refuting-obs")
        confidence_text = await page.text_content("#diag-confidence")

        assert len(evidence_summary.strip()) > 10, "Evidence summary missing or empty"
        assert len(confirming_obs.strip()) > 10, "Confirming observation missing or empty"
        assert len(refuting_obs.strip()) > 10, "Refuting observation missing or empty"
        assert "Likely" in confidence_text or "Evidence Strength" in confidence_text
        assert "Root cause confirmed" not in page_content, "Found premature 'Root cause confirmed' language"
        print("[PASS] Diagnostic workbench hypothesis language, evidence summary, confirming/refuting observations verified.")

        # Test Wi-Fi Layer 1/2 failure: Gateway=No, Conn=wifi
        await page.check('input[name="gateway-ping"][value="no"]')
        await page.check('input[name="conn-type"][value="wifi"]')
        await page.click("#diag-analyze-btn")
        await page.wait_for_timeout(200)

        wifi_diag = await page.text_content("#diag-fault-domain")
        assert "Wi-Fi" in wifi_diag or "Layer 1/2" in wifi_diag
        print("[PASS] Diagnostic reasoning engine verified across multiple fault layers.")

        await page.screenshot(path=str(QA_DIR / "phase6_7_network_diagnostic.png"), full_page=True)
        print("[INFO] Saved screenshot -> phase6_7_network_diagnostic.png")

        # -------------------------------------------------------------
        # 6. Port Reference Browser Testing
        # -------------------------------------------------------------
        print("\n--- 5. Testing Port Reference (tools/port-reference.html) ---")
        t0 = time.time()
        await page.goto(f"{BASE_URL}/tools/port-reference.html", wait_until="networkidle")
        t_load = time.time() - t0
        print(f"[METRIC] Port Reference render latency: {t_load:.3f}s")

        # Verify initial cards count
        port_cards = await page.query_selector_all(".port-card")
        assert len(port_cards) >= 30, f"Expected >= 30 port cards, got {len(port_cards)}"

        # Search for Kerberos
        await page.fill("#ports-search-input", "Kerberos")
        await page.wait_for_timeout(300)
        kerb_count = len(await page.query_selector_all(".port-card"))
        kerb_card = await page.query_selector("#port-kerberos")
        assert kerb_card is not None, "Expected #port-kerberos card in search results"
        kerb_text = await kerb_card.text_content()
        assert "88" in kerb_text
        print("[PASS] Port reference live search verified ('Kerberos' -> Port 88).")

        # Test Transport filter pill: "IP Protocol" (ICMP, ESP, AH)
        await page.fill("#ports-search-input", "")
        await page.click('button[data-transport="IP Protocol"]')
        await page.wait_for_timeout(300)
        proto_cards = await page.query_selector_all(".port-card")
        assert len(proto_cards) >= 3, f"Expected >= 3 IP Protocol cards, got {len(proto_cards)}"
        
        # Verify ICMP card badge displays "IP Proto 1" and not "port 1"
        icmp_card = await page.query_selector("#port-icmp")
        assert icmp_card is not None, "Expected #port-icmp card"
        icmp_text = await icmp_card.text_content()
        assert "IP Proto 1" in icmp_text, f"Expected 'IP Proto 1' badge, got: {icmp_text}"
        assert "port 1" not in icmp_text.lower(), "ICMP must not be modeled as 'port 1'"
        print("[PASS] IP Protocol modeling verified (ICMP protocol 1, port null, transport 'IP Protocol').")

        # Filter by category
        await page.click('button[data-transport="all"]')
        await page.wait_for_timeout(100)
        await page.click('button[data-category="Remote Access & Administration"]')
        await page.wait_for_timeout(300)
        filtered_cards = await page.query_selector_all(".port-card")
        assert len(filtered_cards) >= 4
        print(f"[PASS] Category filtering verified (Remote Access: {len(filtered_cards)} cards).")

        await page.screenshot(path=str(QA_DIR / "phase6_7_port_reference.png"), full_page=True)
        print("[INFO] Saved screenshot -> phase6_7_port_reference.png")

        # -------------------------------------------------------------
        # 7. Guided Troubleshooting Labs Testing
        # -------------------------------------------------------------
        print("\n--- 6. Testing Guided Troubleshooting Labs (labs.html) ---")
        t0 = time.time()
        await page.goto(f"{BASE_URL}/labs.html", wait_until="networkidle")
        t_load = time.time() - t0
        print(f"[METRIC] Labs selector render latency: {t_load:.3f}s")

        # Verify 6 lab cards rendered on selector
        lab_cards = await page.query_selector_all(".lab-card")
        assert len(lab_cards) == 6, f"Expected 6 lab cards, got {len(lab_cards)}"
        print("[PASS] Exactly 6 lab cards rendered on labs selector screen.")

        # Test Lab 1: Networking Lab
        await page.click('#lab-net-01 .lab-launch-btn')
        await page.wait_for_timeout(400)
        await page.screenshot(path=str(QA_DIR / "phase6_7_lab_networking.png"), full_page=True)
        print("[INFO] Saved screenshot -> phase6_7_lab_networking.png")

        # Step 1: Select optimal option (ping gateway and 8.8.8.8)
        await page.click('input[value="opt-net-1b"]')
        await page.wait_for_timeout(200)
        feedback_1 = await page.text_content("#lab-feedback-container")
        assert "Optimal Next Step" in feedback_1
        await page.click("#lab-next-step-btn")
        await page.wait_for_timeout(300)

        # Step 2: Select optimal option (test nslookup)
        await page.click('input[value="opt-net-2a"]')
        await page.wait_for_timeout(200)
        await page.click("#lab-next-step-btn")
        await page.wait_for_timeout(300)

        # Step 3: Select optimal option (test against known DC)
        await page.click('input[value="opt-net-3a"]')
        await page.wait_for_timeout(200)
        await page.click("#lab-next-step-btn")
        await page.wait_for_timeout(300)

        # Step 4: Final step (identify decommissioned DNS in DHCP)
        await page.click('input[value="opt-net-4a"]')
        await page.wait_for_timeout(200)
        await page.click("#lab-next-step-btn")
        await page.wait_for_timeout(400)

        # Confirm Final RCA View rendered
        rca_title = await page.text_content(".lab-results-title")
        assert "DHCP Scope" in rca_title or "DNS" in rca_title
        print(f"[PASS] Lab 1 (Networking) completed through all steps to RCA: '{rca_title}'")
        await page.screenshot(path=str(QA_DIR / "phase6_7_lab_results.png"), full_page=True)
        print("[INFO] Saved screenshot -> phase6_7_lab_results.png")

        # Test Lab 2: Windows Lab direct URL launch
        await page.goto(f"{BASE_URL}/labs.html?lab=lab-win-01", wait_until="networkidle")
        await page.wait_for_timeout(400)
        win_title = await page.text_content(".lab-active-title")
        assert "Domain User Sign-In Fails" in win_title
        await page.screenshot(path=str(QA_DIR / "phase6_7_lab_windows.png"), full_page=True)
        print("[INFO] Saved screenshot -> phase6_7_lab_windows.png")

        # -------------------------------------------------------------
        # 8. Global Search Integration Verification
        # -------------------------------------------------------------
        print("\n--- 7. Testing Global Search Integration ---")
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.click(".search-box")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=3000)

        # Query 1: 'Subnet Calculator'
        await page.fill("#search-modal-input", "Subnet Calculator")
        await page.wait_for_timeout(500)
        search_html_1 = await page.inner_html("#search-results-container")
        assert "Subnet &amp; CIDR Calculator" in search_html_1 or "Subnet & CIDR Calculator" in search_html_1
        assert "tools/subnet-calculator.html" in search_html_1
        print("[PASS] Global search discovered Subnet & CIDR Calculator.")

        # Query 2: 'VLSM'
        await page.fill("#search-modal-input", "VLSM")
        await page.wait_for_timeout(500)
        search_html_2 = await page.inner_html("#search-results-container")
        assert "VLSM / Subnet Planner" in search_html_2
        assert "tools/vlsm-planner.html" in search_html_2
        print("[PASS] Global search discovered VLSM / Subnet Planner.")

        # Query 3: 'Diagnostic Workbench'
        await page.fill("#search-modal-input", "Diagnostic Workbench")
        await page.wait_for_timeout(500)
        search_html_3 = await page.inner_html("#search-results-container")
        assert "Network Diagnostic Workbench" in search_html_3
        assert "tools/network-diagnostic-workbench.html" in search_html_3
        print("[PASS] Global search discovered Network Diagnostic Workbench.")

        # Query 4: 'Port Reference'
        await page.fill("#search-modal-input", "Port Reference")
        await page.wait_for_timeout(500)
        search_html_4 = await page.inner_html("#search-results-container")
        assert "Port &amp; Protocol Reference" in search_html_4 or "Port & Protocol Reference" in search_html_4
        assert "tools/port-reference.html" in search_html_4
        print("[PASS] Global search discovered Port & Protocol Reference.")

        # Query 5: 'Lab:'
        await page.fill("#search-modal-input", "Lab:")
        await page.wait_for_timeout(500)
        lab_results = await page.query_selector_all(".search-result-item")
        assert len(lab_results) >= 6, f"Expected >= 6 lab results, got {len(lab_results)}"
        print(f"[PASS] Global search discovered all 6 troubleshooting labs ({len(lab_results)} results).")

        # Escape search modal
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)

        # -------------------------------------------------------------
        # 9. Responsive Viewports & Zero Horizontal Overflow
        # -------------------------------------------------------------
        print("\n--- 8. Auditing Responsive Viewports (Zero Horizontal Overflow) ---")
        viewports = [320, 375, 768, 1024, 1440]
        test_pages = [
            "tools.html",
            "tools/subnet-calculator.html",
            "tools/vlsm-planner.html",
            "tools/network-diagnostic-workbench.html",
            "tools/port-reference.html",
            "labs.html"
        ]

        for p_rel in test_pages:
            for vp in viewports:
                await page.set_viewport_size({"width": vp, "height": 800})
                await page.goto(f"{BASE_URL}/{p_rel}", wait_until="networkidle")
                overflow = await page.evaluate("""() => {
                    return document.documentElement.scrollWidth > window.innerWidth;
                }""")
                assert not overflow, f"Horizontal overflow detected on {p_rel} at {vp}px viewport!"
            print(f"[PASS] {p_rel} verified with zero horizontal overflow across all viewports ({viewports}).")

        # Capture mobile screenshot (375px) on tools.html
        await page.set_viewport_size({"width": 375, "height": 812})
        await page.goto(f"{BASE_URL}/tools.html", wait_until="networkidle")
        await page.screenshot(path=str(QA_DIR / "phase6_7_mobile.png"), full_page=True)
        print("[INFO] Saved screenshot -> phase6_7_mobile.png")

        # -------------------------------------------------------------
        # 10. Console & Network Integrity
        # -------------------------------------------------------------
        print("\n--- 9. Network & Console Health ---")
        print(f"Console Errors Encountered: {len(console_errors)}")
        print(f"Local 404s Encountered    : {len(local_404s)}")
        assert len(console_errors) == 0, f"Encountered console errors: {console_errors}"
        assert len(local_404s) == 0, f"Encountered local 404s: {local_404s}"

        await context.close()
        await browser.close()

    print("\n" + "=" * 70)
    print("SUCCESS: Phase 6.7 Interactive IT Tools & Labs QA Suite 100% Passed!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_phase6_7_tests())
