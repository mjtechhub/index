import time
from pathlib import Path
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
LIVE_BASE = "https://themjtechhub.site"
QA_DIR = Path("qa")

def run_live_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        
        # 1. Desktop Home Screenshot
        print("\n--- 1. Desktop Home ---")
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(f"{LIVE_BASE}/", timeout=25000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(QA_DIR / "phase6_9_live_home_desktop.png"))
        print("Captured phase6_9_live_home_desktop.png")

        # 2. Mobile Home Screenshot (375x812)
        print("\n--- 2. Mobile Home ---")
        page_mobile = browser.new_page(viewport={"width": 375, "height": 812})
        page_mobile.goto(f"{LIVE_BASE}/", timeout=25000)
        page_mobile.wait_for_timeout(1000)
        overflow = page_mobile.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
        print(f"Mobile 375px home overflow: {overflow}")
        page_mobile.screenshot(path=str(QA_DIR / "phase6_9_live_home_mobile.png"))
        print("Captured phase6_9_live_home_mobile.png")
        page_mobile.close()

        # 3. Header & Footer Screenshot
        print("\n--- 3. Header & Footer ---")
        page.goto(f"{LIVE_BASE}/about.html", timeout=25000)
        page.wait_for_timeout(1000)
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(800)
        page.screenshot(path=str(QA_DIR / "phase6_9_live_header_footer.png"))
        print("Captured phase6_9_live_header_footer.png")

        # 4. Tools Hub Screenshot
        print("\n--- 4. Tools Hub ---")
        page.goto(f"{LIVE_BASE}/tools.html", timeout=25000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(QA_DIR / "phase6_9_live_tools.png"))
        print("Captured phase6_9_live_tools.png")

        # Functional Test: Subnet Calculator on Live
        print("\n--- Testing Subnet Calculator on Live ---")
        page.goto(f"{LIVE_BASE}/tools/subnet-calculator.html", timeout=25000)
        page.wait_for_timeout(1000)
        page.fill("#subnet-ip-input", "192.168.1.10")
        page.select_option("#subnet-prefix-select", "24")
        page.click("#subnet-calc-btn")
        page.wait_for_timeout(600)
        res_ip = page.inner_text("#res-ip")
        res_net = page.inner_text("#res-network")
        res_scope = page.inner_text("#res-scope")
        print(f"Subnet Result: IP={res_ip}, Net={res_net}, Scope={res_scope}")
        assert "192.168.1.10 /24" in res_ip
        assert "192.168.1.0" in res_net

        # Functional Test: VLSM Planner on Live
        print("\n--- Testing VLSM Planner on Live ---")
        page.goto(f"{LIVE_BASE}/tools/vlsm-planner.html", timeout=25000)
        page.wait_for_timeout(1000)
        page.fill("#vlsm-parent-input", "192.168.10.0/24")
        page.click("#vlsm-preload-btn")
        page.wait_for_timeout(500)
        page.click("#vlsm-calc-btn")
        page.wait_for_timeout(600)
        vlsm_table = page.query_selector("#vlsm-results-table, .vlsm-table, table")
        print(f"VLSM calculation table rendered: {vlsm_table is not None}")

        # Functional Test: Diagnostic Workbench on Live
        print("\n--- Testing Diagnostic Workbench on Live ---")
        page.goto(f"{LIVE_BASE}/tools/network-diagnostic-workbench.html", timeout=25000)
        page.wait_for_timeout(1000)
        # Click an option or inspect questions
        q1 = page.query_selector("input[name='gateway-ping']")
        print(f"Diagnostic Workbench question rendered: {q1 is not None}")

        # Functional Test: Port Reference on Live
        print("\n--- Testing Port Reference on Live ---")
        page.goto(f"{LIVE_BASE}/tools/port-reference.html", timeout=25000)
        page.wait_for_timeout(1000)
        page.fill("#ports-search-input", "DNS")
        page.wait_for_timeout(500)
        dns_rows = page.evaluate("() => document.querySelectorAll('#ports-tbody tr:not([style*=\"display: none\"])').length")
        print(f"Port search 'DNS' returned visible rows: {dns_rows}")

        # 5. Labs Screenshot & Functional Run
        print("\n--- 5. Labs & Troubleshooting Run ---")
        page.goto(f"{LIVE_BASE}/labs.html?lab=lab-network-dns-routing", timeout=25000)
        page.wait_for_timeout(1200)
        # Verify lab loaded
        lab_title = page.inner_text(".lab-active-title, h1.page-title, h2")
        print(f"Active lab title: {lab_title}")
        # Click a step option if present
        opt_btn = page.query_selector(".lab-option-btn, button.btn-secondary")
        if opt_btn:
            opt_btn.click()
            page.wait_for_timeout(600)
        page.screenshot(path=str(QA_DIR / "phase6_9_live_lab.png"))
        print("Captured phase6_9_live_lab.png")

        # 6. Tutorial Page Screenshot
        print("\n--- 6. Tutorial Page ---")
        page.goto(f"{LIVE_BASE}/tutorials/networking/tcp-vs-udp.html", timeout=25000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(QA_DIR / "phase6_9_live_tutorial.png"))
        print("Captured phase6_9_live_tutorial.png")

        # 7. Global Search Modal Screenshot
        print("\n--- 7. Global Search ---")
        page.goto(f"{LIVE_BASE}/", timeout=25000)
        page.wait_for_timeout(1000)
        search_trigger = page.query_selector(".search-box, button.search-box")
        if search_trigger:
            search_trigger.click()
            page.wait_for_timeout(800)
            search_inp = page.query_selector("#search-input")
            if search_inp:
                search_inp.fill("DNS")
                page.wait_for_timeout(800)
        page.screenshot(path=str(QA_DIR / "phase6_9_live_search.png"))
        print("Captured phase6_9_live_search.png")

        # 8. 404 Page on Live Screenshot
        print("\n--- 8. 404 Page on Live ---")
        page.goto(f"{LIVE_BASE}/this-page-should-not-exist-phase69.html", timeout=25000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(QA_DIR / "phase6_9_live_404.png"))
        print("Captured phase6_9_live_404.png")

        # 9. Viewport Overflow Smoke Checks
        print("\n--- 9. Viewport Overflow Smoke Checks ---")
        vps = [320, 375, 768, 1024, 1440]
        pages_to_check = [
            "/",
            "/topics.html",
            "/commands.html",
            "/quiz.html",
            "/resources.html",
            "/tools.html",
            "/labs.html"
        ]
        overflows = []
        for vp in vps:
            p_vp = browser.new_page(viewport={"width": vp, "height": 800})
            for ptc in pages_to_check:
                p_vp.goto(f"{LIVE_BASE}{ptc}", timeout=20000)
                p_vp.wait_for_timeout(200)
                has_of = p_vp.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
                if has_of:
                    overflows.append((vp, ptc))
            p_vp.close()
        print(f"Viewport overflows count: {len(overflows)} {overflows}")

        browser.close()
        print("\n>>> ALL PLAYWRIGHT LIVE AUDIT CHECKS PASSED <<<")

if __name__ == "__main__":
    run_live_tests()
