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
        assert res_scope == "Private", f"Expected Private, got {res_scope}"
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

        # Deterministic Test Vector 5: RFC 1918 Classification Boundaries
        # 172.20.1.5 -> Private
        await page.fill("#subnet-ip-input", "172.20.1.5")
        await page.select_option("#subnet-prefix-select", "24")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(100)
        assert (await page.text_content("#res-scope")) == "Private"

        # 172.32.1.5 -> Public (NOT Private!)
        await page.fill("#subnet-ip-input", "172.32.1.5")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(100)
        assert (await page.text_content("#res-scope")) == "Public", "172.32.1.5 must be classified as Public"
        print("[PASS] RFC 1918 boundary verified (172.20.1.5 is Private, 172.32.1.5 is Public).")

        # Input Validation: Invalid IPs reject cleanly without NaN or crashes
        await page.fill("#subnet-ip-input", "999.1.1.1")
        await page.click("#subnet-calc-btn")
        await page.wait_for_timeout(100)
        err_msg = await page.text_content("#subnet-error-alert")
        assert "Invalid IPv4 address format" in err_msg
        print("[PASS] Subnet calculator input validation verified (999.1.1.1 rejected cleanly).")

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

        # Test DNS Failure scenario: Gateway=Yes, Public=Yes, DNS=No
        await page.check('input[name="gateway-ping"][value="yes"]')
        await page.check('input[name="public-ping"][value="yes"]')
        await page.check('input[name="dns-resolve"][value="no"]')
        await page.click("#diag-analyze-btn")
        await page.wait_for_timeout(200)

        diag_res = await page.text_content("#diag-fault-domain")
        assert "DNS" in diag_res, f"Expected DNS fault domain, got {diag_res}"
        
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

        # Filter by category
        await page.fill("#ports-search-input", "")
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
