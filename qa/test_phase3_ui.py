#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 3 Automated Verification Suite
Tests Shared Design System, Header, Footer, Accessibility, and Responsive Layout across viewports.
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
BASE_URL = "http://localhost/index"
OUTPUT_DIR = Path(__file__).resolve().parent

async def run_phase3_tests():
    print("=" * 60)
    print("Starting MJ Tech Hub Phase 3 Verification Suite")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        errors = []
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))

        test_results = {}

        # -------------------------------------------------------------
        # 1. Header & Navigation Component Loading (Desktop 1440px)
        # -------------------------------------------------------------
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")

        # Wait for dynamically loaded header and footer
        await page.wait_for_selector(".site-header", timeout=5000)
        await page.wait_for_selector(".site-footer", timeout=5000)

        # Check Skip Link
        skip_link = await page.query_selector(".skip-link")
        skip_href = await skip_link.get_attribute("href") if skip_link else None
        main_content = await page.query_selector("#main-content")
        test_results["skip_link"] = (skip_href == "#main-content" and main_content is not None)
        print(f"[{'PASS' if test_results['skip_link'] else 'FAIL'}] Accessibility Skip Link -> #main-content target")

        # Check Active Navigation on Home
        home_active = await page.evaluate("""() => {
            const link = document.querySelector('.nav-links a[href*="index.html"]');
            return link && link.classList.contains('active') && link.getAttribute('aria-current') === 'page';
        }""")
        test_results["active_nav_home"] = bool(home_active)
        print(f"[{'PASS' if test_results['active_nav_home'] else 'FAIL'}] Active Nav Indicator on Home (active + aria-current='page')")

        # Check Active Navigation on Category Page (networking.html -> Topics)
        await page.goto(f"{BASE_URL}/networking.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)
        topics_active_on_category = await page.evaluate("""() => {
            const link = document.querySelector('.nav-links a[href*="topics.html"]');
            return link && link.classList.contains('active') && link.getAttribute('aria-current') === 'page';
        }""")
        test_results["active_nav_category"] = bool(topics_active_on_category)
        print(f"[{'PASS' if test_results['active_nav_category'] else 'FAIL'}] Active Nav Indicator on Category Page (Topics active for networking.html)")

        # Return to Index
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)

        # -------------------------------------------------------------
        # 2. Accessible Search Button & Modal Trigger
        # -------------------------------------------------------------
        # Click search box button
        await page.click(".search-box")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=3000)
        
        # Check input is focused
        is_focused = await page.evaluate("() => document.activeElement.id === 'search-modal-input'")
        
        # Type search query
        await page.fill("#search-modal-input", "DNS")
        await page.wait_for_timeout(600)
        
        results_count = await page.evaluate("() => document.querySelectorAll('.search-result-item').length")
        
        # Close via Escape
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)
        modal_closed = await page.evaluate("() => !document.getElementById('search-modal-backdrop').classList.contains('active')")
        
        test_results["search_trigger"] = bool(results_count > 0 and modal_closed)
        print(f"[{'PASS' if test_results['search_trigger'] else 'FAIL'}] Search Button Modal Trigger, Query Execution & Escape Dismissal ({results_count} results)")

        # -------------------------------------------------------------
        # 3. Theme Toggle & Persistence
        # -------------------------------------------------------------
        initial_theme = await page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        await page.click(".theme-toggle")
        await page.wait_for_timeout(400)
        toggled_theme = await page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        saved_theme = await page.evaluate("() => localStorage.getItem('mj-theme')")
        
        # Toggle back to ensure test repeatability
        await page.click(".theme-toggle")
        await page.wait_for_timeout(400)
        restored_theme = await page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        
        test_results["theme_toggle"] = (initial_theme != toggled_theme and saved_theme == toggled_theme and restored_theme == initial_theme)
        print(f"[{'PASS' if test_results['theme_toggle'] else 'FAIL'}] Theme Toggle (Dark <-> Light) & localStorage Persistence (Theme was {initial_theme} -> {toggled_theme} -> {restored_theme})")

        # -------------------------------------------------------------
        # 4. Footer Structure Verification
        # -------------------------------------------------------------
        footer_checks = await page.evaluate("""() => {
            const footer = document.querySelector('.site-footer');
            if (!footer) return { ok: false };
            const brand = !!footer.querySelector('.footer-brand .site-logo');
            const desc = !!footer.querySelector('.footer-desc');
            const instagram = !!footer.querySelector('.social-links a[href*="instagram"]');
            const learnLinks = footer.querySelectorAll('.footer-col:nth-child(2) .footer-links li').length;
            const exploreLinks = footer.querySelectorAll('.footer-col:nth-child(3) .footer-links li').length;
            const legalLinks = footer.querySelectorAll('.footer-col:nth-child(4) .footer-links li').length;
            const copyright = !!footer.querySelector('.footer-copyright');
            return {
                ok: brand && desc && instagram && learnLinks >= 6 && exploreLinks >= 4 && legalLinks >= 4 && copyright,
                learnCount: learnLinks,
                exploreCount: exploreLinks,
                legalCount: legalLinks
            };
        }""")
        test_results["footer_structure"] = bool(footer_checks.get("ok"))
        print(f"[{'PASS' if test_results['footer_structure'] else 'FAIL'}] Footer Columns: Learn ({footer_checks.get('learnCount')}), Explore ({footer_checks.get('exploreCount')}), Legal ({footer_checks.get('legalCount')}), Social + Copyright")

        # -------------------------------------------------------------
        # 5. Capture Desktop Screenshots (1440px) - Dark & Light
        # -------------------------------------------------------------
        # Ensure dark theme
        await page.evaluate("() => { document.documentElement.setAttribute('data-theme', 'dark'); localStorage.setItem('mj-theme', 'dark'); }")
        await page.wait_for_timeout(300)
        desktop_dark_shot = OUTPUT_DIR / "phase3_desktop_dark.png"
        await page.screenshot(path=str(desktop_dark_shot), full_page=False)
        print(f"[INFO] Saved 1440px desktop dark screenshot to {desktop_dark_shot.name}")

        # Light theme
        await page.evaluate("() => { document.documentElement.setAttribute('data-theme', 'light'); localStorage.setItem('mj-theme', 'light'); }")
        await page.wait_for_timeout(300)
        desktop_light_shot = OUTPUT_DIR / "phase3_desktop_light.png"
        await page.screenshot(path=str(desktop_light_shot), full_page=False)
        print(f"[INFO] Saved 1440px desktop light screenshot to {desktop_light_shot.name}")

        # Restore dark default
        await page.evaluate("() => { document.documentElement.setAttribute('data-theme', 'dark'); localStorage.setItem('mj-theme', 'dark'); }")

        # -------------------------------------------------------------
        # 6. Mobile Navigation & Touch Behavior (375px)
        # -------------------------------------------------------------
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".mobile-menu-toggle", timeout=5000)

        menu_btn_visible = await page.evaluate("""() => {
            const btn = document.querySelector('.mobile-menu-toggle');
            if (!btn) return false;
            const style = window.getComputedStyle(btn);
            return style.display !== 'none';
        }""")

        # Open mobile menu
        await page.click(".mobile-menu-toggle")
        await page.wait_for_timeout(300)
        
        menu_opened = await page.evaluate("""() => {
            const nav = document.querySelector('.nav-links');
            const btn = document.querySelector('.mobile-menu-toggle');
            return nav && nav.classList.contains('active') && btn.getAttribute('aria-expanded') === 'true';
        }""")

        # Screenshot open mobile menu
        mobile_menu_shot = OUTPUT_DIR / "phase3_mobile_menu_open.png"
        await page.screenshot(path=str(mobile_menu_shot))
        print(f"[INFO] Saved 375px mobile menu open screenshot to {mobile_menu_shot.name}")

        # Press Escape to close mobile menu
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)
        
        menu_closed_by_escape = await page.evaluate("""() => {
            const nav = document.querySelector('.nav-links');
            const btn = document.querySelector('.mobile-menu-toggle');
            return nav && !nav.classList.contains('active') && btn.getAttribute('aria-expanded') === 'false';
        }""")

        test_results["mobile_nav"] = bool(menu_btn_visible and menu_opened and menu_closed_by_escape)
        print(f"[{'PASS' if test_results['mobile_nav'] else 'FAIL'}] Mobile Navigation Hamburger Menu (Toggle, Aria-Expanded, Escape dismissal)")

        # Capture 375px Mobile Screenshots (Dark & Light)
        mobile_dark_shot = OUTPUT_DIR / "phase3_mobile_dark.png"
        await page.screenshot(path=str(mobile_dark_shot))
        print(f"[INFO] Saved 375px mobile dark screenshot to {mobile_dark_shot.name}")

        await page.evaluate("() => { document.documentElement.setAttribute('data-theme', 'light'); }")
        await page.wait_for_timeout(300)
        mobile_light_shot = OUTPUT_DIR / "phase3_mobile_light.png"
        await page.screenshot(path=str(mobile_light_shot))
        print(f"[INFO] Saved 375px mobile light screenshot to {mobile_light_shot.name}")

        await page.evaluate("() => { document.documentElement.setAttribute('data-theme', 'dark'); }")

        # -------------------------------------------------------------
        # 7. Horizontal Overflow Verification Across Viewports
        # -------------------------------------------------------------
        viewports = [375, 768, 1024, 1440]
        pages_to_test = ["/index.html", "/topics.html", "/commands.html", "/about.html", "/legal/privacy.html"]
        overflow_issues = []

        for vp_width in viewports:
            await page.set_viewport_size({"width": vp_width, "height": 800})
            for page_path in pages_to_test:
                await page.goto(f"{BASE_URL}{page_path}", wait_until="networkidle")
                await page.wait_for_selector(".site-header", timeout=5000)
                await page.wait_for_selector(".site-footer", timeout=5000)
                
                has_overflow = await page.evaluate("""() => {
                    const docWidth = document.documentElement.clientWidth;
                    const scrollWidth = document.documentElement.scrollWidth;
                    return {
                        overflow: scrollWidth > docWidth,
                        docWidth: docWidth,
                        scrollWidth: scrollWidth,
                        diff: scrollWidth - docWidth
                    };
                }""")
                if has_overflow["overflow"]:
                    overflow_issues.append(f"{page_path} at {vp_width}px (scroll: {has_overflow['scrollWidth']}, client: {has_overflow['docWidth']})")

        test_results["no_horizontal_overflow"] = (len(overflow_issues) == 0)
        if test_results["no_horizontal_overflow"]:
            print(f"[PASS] Zero Horizontal Overflow across all viewports ({viewports}) on key platform pages")
        else:
            print(f"[FAIL] Horizontal Overflow detected: {overflow_issues}")

        # -------------------------------------------------------------
        # 8. Console Errors & Network Failures
        # -------------------------------------------------------------
        test_results["zero_console_errors"] = (len(errors) == 0)
        if test_results["zero_console_errors"]:
            print("[PASS] Zero browser console errors encountered")
        else:
            print(f"[FAIL] Console errors encountered: {errors}")

        await browser.close()

    print("=" * 60)
    all_passed = all(test_results.values())
    print(f"PHASE 3 VERIFICATION OVERALL: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 60)
    return all_passed

if __name__ == "__main__":
    asyncio.run(run_phase3_tests())
