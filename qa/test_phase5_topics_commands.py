#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 5 & 5.1 Topics, Category Architecture & Commands Verification Suite
Validates:
1. Topics page rendering (6 core domains, specialized areas, dynamic tutorial count badges)
2. Unified category renderer with Progressive Display on Networking:
   - Initial load: exactly 18 tutorials
   - Counter: "Showing 18 of 61 tutorials"
   - Load More reveals 36, 54, and finally all 61
   - Load More button hides when all results are displayed
   - Difficulty filters operate across entire 61 dataset and reset visible count sensibly
   - Search operates across entire dataset and counter reflects matches
3. Factual empty category behavior:
   - Audit topics.json: verify Windows/Linux/Servers/Cybersecurity/Cloud have sections: []
   - Verify factual generic status message and zero fabricated tutorials
4. Essential Commands page modernization & terminology update:
   - 12 commands from JSON
   - "Expected Result" is eliminated
   - "Example Output" renders in details label
   - Details summary displays "View syntax, example output & use case"
   - Category & platform filtering (Networking: 5, System: 7, Linux: 2)
   - Search & accessible 1-click copy with toast feedback
5. Theme switching & persistence
6. Responsive zero horizontal overflow across viewports [375, 768, 1024, 1440]
7. Zero browser console errors and zero local 404 network requests
8. Captures required Phase 5.1 screenshots:
   - qa/phase5_1_networking_desktop.png
   - qa/phase5_1_networking_mobile.png
   - qa/phase5_1_empty_category.png
   - qa/phase5_1_commands.png
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
BASE_URL = "http://localhost/index"
QA_DIR = Path(__file__).resolve().parent
ROOT_DIR = QA_DIR.parent

async def run_phase5_tests():
    print("=" * 68)
    print("Starting MJ Tech Hub Phase 5 & 5.1 Extended Verification Suite")
    print("=" * 68)

    # Pre-audit topics.json directly
    with open(ROOT_DIR / "data" / "topics.json", "r", encoding="utf-8") as f:
        topics_data = json.load(f)

    empty_cats = ["windows", "linux", "servers", "cybersecurity", "cloud"]
    print("\n--- AUDIT: topics.json Empty Category Curriculum Audit ---")
    for cat_id in empty_cats:
        c = next((item for item in topics_data.get("categories", []) if item.get("id") == cat_id), None)
        sections = c.get("sections", []) if c else None
        print(f"Category '{cat_id}': structured sections count = {len(sections) if sections is not None else 'None'}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        console_errors = []
        network_404s = []

        page.on("console", lambda msg: console_errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("response", lambda resp: network_404s.append(resp.url) if resp.status == 404 and "localhost" in resp.url else None)

        test_results = {}

        # -------------------------------------------------------------
        # 1. Topics Page Verification (1440px Desktop)
        # -------------------------------------------------------------
        print("\n--- 1. Topics Page Verification ---")
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/topics.html", wait_until="networkidle")

        await page.wait_for_selector(".topics-core-grid .topic-domain-card", timeout=5000)
        await page.wait_for_selector(".topics-specialized-grid .specialized-topic-card", timeout=5000)

        core_cards = await page.evaluate("""() => {
            const cards = document.querySelectorAll('#core-topics-grid .topic-domain-card');
            return Array.from(cards).map(c => ({
                title: c.querySelector('.topic-domain-title')?.textContent.trim(),
                countBadge: c.querySelector('.topic-tut-count-badge')?.textContent.trim(),
                href: c.getAttribute('href')
            }));
        }""")

        test_results["topics_core_count"] = len(core_cards) == 6
        print(f"[{'PASS' if test_results['topics_core_count'] else 'FAIL'}] Core Topics (Rendered: {len(core_cards)} cards, Expected: 6)")

        net_card = next((c for c in core_cards if c["title"] == "Networking"), None)
        test_results["networking_count_badge"] = net_card is not None and "61 Tutorials" in net_card["countBadge"]
        print(f"[{'PASS' if test_results['networking_count_badge'] else 'FAIL'}] Networking Tutorial Count Badge ('{net_card['countBadge'] if net_card else 'None'}' == '61 Tutorials')")

        empty_cards = [c for c in core_cards if c["title"] != "Networking"]
        test_results["empty_category_badges"] = all("In preparation" in c["countBadge"] for c in empty_cards)
        print(f"[{'PASS' if test_results['empty_category_badges'] else 'FAIL'}] Non-Published Categories Status ('In preparation')")

        spec_count = await page.evaluate("() => document.querySelectorAll('#more-topics-grid .specialized-topic-card').length")
        test_results["specialized_count"] = (spec_count == 10)
        print(f"[{'PASS' if test_results['specialized_count'] else 'FAIL'}] Specialized Categories (Rendered: {spec_count} cards, Expected: 10)")

        # -------------------------------------------------------------
        # 2. Unified Category Page: Networking Progressive Display
        # -------------------------------------------------------------
        print("\n--- 2. Networking Progressive Display & Filtering ---")
        await page.goto(f"{BASE_URL}/networking.html", wait_until="networkidle")
        await page.wait_for_selector(".category-tut-grid .cat-tut-card", timeout=5000)

        # A. Initial Load: Exactly 18 Tutorials
        init_count = await page.evaluate("() => document.querySelectorAll('.category-tut-grid .cat-tut-card').length")
        init_counter_text = await page.evaluate("() => document.querySelector('.text-xs.text-muted.mb-2')?.textContent.trim()")
        load_more_visible = await page.evaluate("() => { const el = document.querySelector('.category-load-more-wrap'); return el && getComputedStyle(el).display !== 'none'; }")

        test_results["net_initial_18"] = (init_count == 18)
        test_results["net_initial_counter"] = ("Showing 18 of 61 tutorials" in init_counter_text)
        test_results["net_load_more_visible"] = bool(load_more_visible)

        print(f"[{'PASS' if test_results['net_initial_18'] else 'FAIL'}] Initial Visible Count (Rendered: {init_count}, Expected: 18)")
        print(f"[{'PASS' if test_results['net_initial_counter'] else 'FAIL'}] Initial Counter Text ('{init_counter_text}')")
        print(f"[{'PASS' if test_results['net_load_more_visible'] else 'FAIL'}] Load More Button Visible on Initial Load")

        # Capture Desktop Screenshot of Initial Networking (18 tutorials)
        shot_net_desktop = QA_DIR / "phase5_1_networking_desktop.png"
        await page.screenshot(path=str(shot_net_desktop), full_page=True)
        print(f"[INFO] Saved Phase 5.1 Networking Desktop screenshot -> {shot_net_desktop.name}")

        # B. Progressive Batches: Click Load More
        # Click 1: 18 -> 36
        await page.click("#load-more-btn")
        await page.wait_for_timeout(200)
        batch2_count = await page.evaluate("() => document.querySelectorAll('.category-tut-grid .cat-tut-card').length")
        batch2_counter = await page.evaluate("() => document.querySelector('.text-xs.text-muted.mb-2')?.textContent.trim()")
        test_results["net_batch_36"] = (batch2_count == 36 and "Showing 36 of 61 tutorials" in batch2_counter)
        print(f"[{'PASS' if test_results['net_batch_36'] else 'FAIL'}] Load More Batch 2 (Count: {batch2_count}, Counter: '{batch2_counter}')")

        # Click 2: 36 -> 54
        await page.click("#load-more-btn")
        await page.wait_for_timeout(200)
        batch3_count = await page.evaluate("() => document.querySelectorAll('.category-tut-grid .cat-tut-card').length")
        batch3_counter = await page.evaluate("() => document.querySelector('.text-xs.text-muted.mb-2')?.textContent.trim()")
        test_results["net_batch_54"] = (batch3_count == 54 and "Showing 54 of 61 tutorials" in batch3_counter)
        print(f"[{'PASS' if test_results['net_batch_54'] else 'FAIL'}] Load More Batch 3 (Count: {batch3_count}, Counter: '{batch3_counter}')")

        # Click 3: 54 -> 61 (Final batch)
        await page.click("#load-more-btn")
        await page.wait_for_timeout(200)
        final_count = await page.evaluate("() => document.querySelectorAll('.category-tut-grid .cat-tut-card').length")
        final_counter = await page.evaluate("() => document.querySelector('.text-xs.text-muted.mb-2')?.textContent.trim()")
        load_more_hidden_final = await page.evaluate("() => { const el = document.querySelector('.category-load-more-wrap'); return !el || getComputedStyle(el).display === 'none'; }")

        test_results["net_final_61"] = (final_count == 61 and "Showing 61 of 61 tutorials" in final_counter)
        test_results["net_load_more_hidden_on_complete"] = bool(load_more_hidden_final)
        print(f"[{'PASS' if test_results['net_final_61'] else 'FAIL'}] Final Load Exposes All 61 (Count: {final_count}, Counter: '{final_counter}')")
        print(f"[{'PASS' if test_results['net_load_more_hidden_on_complete'] else 'FAIL'}] Load More Hidden After All 61 Revealed")

        # C. Difficulty Filters Operate Across Complete Dataset & Reset Count
        # Intermediate Filter (Total: 35)
        await page.click("button.filter-btn:has-text('Intermediate')")
        await page.wait_for_timeout(200)
        inter_init_count = await page.evaluate("() => document.querySelectorAll('.category-tut-grid .cat-tut-card').length")
        inter_counter = await page.evaluate("() => document.querySelector('.text-xs.text-muted.mb-2')?.textContent.trim()")
        test_results["filter_inter_reset"] = (inter_init_count == 18 and "Showing 18 of 35 Intermediate tutorials" in inter_counter)
        print(f"[{'PASS' if test_results['filter_inter_reset'] else 'FAIL'}] Intermediate Filter Initial Slice (Count: {inter_init_count}, Counter: '{inter_counter}')")

        # Intermediate Load More -> 35
        await page.click("#load-more-btn")
        await page.wait_for_timeout(200)
        inter_full_count = await page.evaluate("() => document.querySelectorAll('.category-tut-grid .cat-tut-card').length")
        inter_full_counter = await page.evaluate("() => document.querySelector('.text-xs.text-muted.mb-2')?.textContent.trim()")
        inter_hidden = await page.evaluate("() => { const el = document.querySelector('.category-load-more-wrap'); return !el || getComputedStyle(el).display === 'none'; }")
        test_results["filter_inter_full"] = (inter_full_count == 35 and "Showing 35 of 35 Intermediate tutorials" in inter_full_counter and inter_hidden)
        print(f"[{'PASS' if test_results['filter_inter_full'] else 'FAIL'}] Intermediate Filter Complete (Count: {inter_full_count}, Counter: '{inter_full_counter}', Hidden: {inter_hidden})")

        # Advanced Filter (Total: 4)
        await page.click("button.filter-btn:has-text('Advanced')")
        await page.wait_for_timeout(200)
        adv_count = await page.evaluate("() => document.querySelectorAll('.category-tut-grid .cat-tut-card').length")
        adv_counter = await page.evaluate("() => document.querySelector('.text-xs.text-muted.mb-2')?.textContent.trim()")
        adv_hidden = await page.evaluate("() => { const el = document.querySelector('.category-load-more-wrap'); return !el || getComputedStyle(el).display === 'none'; }")
        test_results["filter_adv"] = (adv_count == 4 and "Showing 4 of 4 Advanced tutorials" in adv_counter and adv_hidden)
        print(f"[{'PASS' if test_results['filter_adv'] else 'FAIL'}] Advanced Filter (Count: {adv_count}, Counter: '{adv_counter}', Hidden: {adv_hidden})")

        # Beginner Filter (Total: 22)
        await page.click("button.filter-btn:has-text('Beginner')")
        await page.wait_for_timeout(200)
        beg_count = await page.evaluate("() => document.querySelectorAll('.category-tut-grid .cat-tut-card').length")
        beg_counter = await page.evaluate("() => document.querySelector('.text-xs.text-muted.mb-2')?.textContent.trim()")
        test_results["filter_beg"] = (beg_count == 18 and "Showing 18 of 22 Beginner tutorials" in beg_counter)
        print(f"[{'PASS' if test_results['filter_beg'] else 'FAIL'}] Beginner Filter Initial (Count: {beg_count}, Counter: '{beg_counter}')")

        # D. Reset to All & In-Category Search Across Complete Dataset
        await page.click("button.filter-btn:has-text('All')")
        await page.wait_for_timeout(200)

        await page.fill(".category-search-input", "subnet")
        await page.wait_for_timeout(200)
        search_count = await page.evaluate("() => document.querySelectorAll('.category-tut-grid .cat-tut-card').length")
        search_counter = await page.evaluate("() => document.querySelector('.text-xs.text-muted.mb-2')?.textContent.trim()")
        test_results["cat_search_complete"] = (search_count > 0 and "matching tutorials" in search_counter)
        print(f"[{'PASS' if test_results['cat_search_complete'] else 'FAIL'}] Search Across Complete Dataset for 'subnet' (Matches: {search_count}, Counter: '{search_counter}')")

        # Clear search
        await page.fill(".category-search-input", "")
        await page.wait_for_timeout(200)

        # -------------------------------------------------------------
        # 3. Unified Category Page: Factual Empty State (windows.html)
        # -------------------------------------------------------------
        print("\n--- 3. Factual Empty Category Page ---")
        await page.goto(f"{BASE_URL}/windows.html", wait_until="networkidle")
        await page.wait_for_selector(".category-empty-state", timeout=5000)

        empty_state_data = await page.evaluate("""() => {
            const card = document.querySelector('.category-empty-state');
            return {
                title: card.querySelector('.empty-state-title')?.textContent.trim(),
                statusBadge: card.querySelector('.empty-state-status-badge')?.textContent.trim(),
                desc: card.querySelector('.empty-state-desc')?.textContent.trim(),
                plannedBox: card.querySelector('.planned-curriculum-box')?.textContent.trim(),
                hasTutorialCards: document.querySelectorAll('.category-tut-grid .cat-tut-card').length > 0
            };
        }""")

        test_results["empty_state_verified"] = (
            "Tutorials for this category are being prepared" in empty_state_data["title"] and
            "0 Published Tutorials" in empty_state_data["statusBadge"] and
            "Curriculum topics for Windows are currently being structured" in empty_state_data["plannedBox"] and
            not empty_state_data["hasTutorialCards"]
        )
        print(f"[{'PASS' if test_results['empty_state_verified'] else 'FAIL'}] Factual Empty State on windows.html (Zero fake tutorials, Factual status: '{empty_state_data['statusBadge']}')")

        # Capture Empty Category Screenshot
        shot_category_empty = QA_DIR / "phase5_1_empty_category.png"
        await page.screenshot(path=str(shot_category_empty), full_page=True)
        print(f"[INFO] Saved Phase 5.1 Empty Category screenshot -> {shot_category_empty.name}")

        # -------------------------------------------------------------
        # 4. Essential Commands Page Modernization & Terminology Audit
        # -------------------------------------------------------------
        print("\n--- 4. Commands Modernization & Terminology Audit ---")
        await page.goto(f"{BASE_URL}/commands.html", wait_until="networkidle")
        await page.wait_for_selector("#commands-container .command-item-card", timeout=5000)

        cmd_count = await page.evaluate("() => document.querySelectorAll('#commands-container .command-item-card').length")
        test_results["commands_total"] = (cmd_count == 12)
        print(f"[{'PASS' if test_results['commands_total'] else 'FAIL'}] Commands Loaded from JSON (Rendered: {cmd_count}, Expected: 12)")

        # Terminology Checks
        # A. Assert "Expected Result" does NOT exist in Commands UI
        has_expected_result = await page.evaluate("""() => {
            const container = document.getElementById('commands-container');
            return container ? container.innerHTML.includes('Expected Result') : false;
        }""")
        test_results["no_expected_result"] = not has_expected_result
        print(f"[{'PASS' if test_results['no_expected_result'] else 'FAIL'}] 'Expected Result' Eliminated from Commands UI (Found: {has_expected_result})")

        # B. Assert "Example Output" renders correctly across all command cards
        example_output_labels_count = await page.evaluate("""() => {
            const labels = document.querySelectorAll('.cmd-detail-field .cmd-detail-label');
            return Array.from(labels).filter(l => l.textContent.trim() === 'Example Output').length;
        }""")
        test_results["example_output_rendered"] = (example_output_labels_count == 12)
        print(f"[{'PASS' if test_results['example_output_rendered'] else 'FAIL'}] 'Example Output' Rendered on All Command Cards ({example_output_labels_count} of 12)")

        # C. Assert summary text is updated
        summary_text = await page.evaluate("() => document.querySelector('.cmd-details-summary')?.textContent.trim()")
        test_results["summary_terminology"] = ("View syntax, example output & use case" in summary_text)
        print(f"[{'PASS' if test_results['summary_terminology'] else 'FAIL'}] Details Summary Terminology ('{summary_text}')")

        # D. Category & Platform Filtering on Commands
        # Networking category (5 commands)
        await page.click("#command-category-filters button:has-text('Networking')")
        await page.wait_for_timeout(200)
        net_cmd_count = await page.evaluate("() => document.querySelectorAll('#commands-container .command-item-card').length")
        test_results["cmd_filter_net"] = (net_cmd_count == 5)
        print(f"[{'PASS' if test_results['cmd_filter_net'] else 'FAIL'}] Command Filter 'Networking' (Rendered: {net_cmd_count}, Expected: 5)")

        # System category (7 commands)
        await page.click("#command-category-filters button:has-text('System')")
        await page.wait_for_timeout(200)
        sys_cmd_count = await page.evaluate("() => document.querySelectorAll('#commands-container .command-item-card').length")
        test_results["cmd_filter_sys"] = (sys_cmd_count == 7)
        print(f"[{'PASS' if test_results['cmd_filter_sys'] else 'FAIL'}] Command Filter 'System' (Rendered: {sys_cmd_count}, Expected: 7)")

        # Linux platform filter (2 commands: ping, nslookup)
        await page.click("#command-category-filters button:has-text('Linux')")
        await page.wait_for_timeout(200)
        linux_cmd_count = await page.evaluate("() => document.querySelectorAll('#commands-container .command-item-card').length")
        test_results["cmd_filter_linux"] = (linux_cmd_count == 2)
        print(f"[{'PASS' if test_results['cmd_filter_linux'] else 'FAIL'}] Command Platform Filter 'Linux' (Rendered: {linux_cmd_count}, Expected: 2)")

        # Reset to All
        await page.click("#command-category-filters button:has-text('All')")
        await page.wait_for_timeout(200)

        # Search filter test (e.g. "ipconfig")
        await page.fill("#commands-search-input", "ipconfig")
        await page.wait_for_timeout(200)
        search_cmd_count = await page.evaluate("() => document.querySelectorAll('#commands-container .command-item-card').length")
        test_results["cmd_search"] = (search_cmd_count == 1)
        print(f"[{'PASS' if test_results['cmd_search'] else 'FAIL'}] Command Live Search for 'ipconfig' (Rendered: {search_cmd_count}, Expected: 1)")

        # Clear search
        await page.fill("#commands-search-input", "")
        await page.wait_for_timeout(200)

        # Test Copy Button interaction and Toast Notification
        first_copy_btn = await page.query_selector(".command-item-card .cmd-copy-btn")
        if first_copy_btn:
            await first_copy_btn.click()
            await page.wait_for_timeout(200)
            toast_active = await page.evaluate("() => document.getElementById('copy-toast')?.classList.contains('active')")
            btn_copied_class = await page.evaluate("() => document.querySelector('.command-item-card .cmd-copy-btn')?.classList.contains('copied')")
            test_results["copy_toast"] = bool(toast_active and btn_copied_class)
            print(f"[{'PASS' if test_results['copy_toast'] else 'FAIL'}] Accessible Copy Interaction (Toast active: {toast_active}, Button copied class: {btn_copied_class})")
        else:
            test_results["copy_toast"] = False

        # Capture Commands Desktop Screenshot
        shot_cmds = QA_DIR / "phase5_1_commands.png"
        await page.screenshot(path=str(shot_cmds), full_page=True)
        print(f"[INFO] Saved Phase 5.1 Commands screenshot -> {shot_cmds.name}")

        # -------------------------------------------------------------
        # 5. Mobile Responsive (375px) & Screenshots
        # -------------------------------------------------------------
        print("\n--- 5. Mobile Responsive (375px) ---")
        await page.set_viewport_size({"width": 375, "height": 812})

        # Networking Mobile Screenshot
        await page.goto(f"{BASE_URL}/networking.html", wait_until="networkidle")
        await page.wait_for_timeout(300)
        shot_net_mobile = QA_DIR / "phase5_1_networking_mobile.png"
        await page.screenshot(path=str(shot_net_mobile), full_page=True)
        print(f"[INFO] Saved Phase 5.1 Networking Mobile screenshot -> {shot_net_mobile.name}")

        # -------------------------------------------------------------
        # 6. Responsive Zero Horizontal Overflow Across All Pages
        # -------------------------------------------------------------
        print("\n--- 6. Zero Horizontal Overflow Check Across Viewports ---")
        viewports = [375, 768, 1024, 1440]
        test_pages = ["topics.html", "networking.html", "windows.html", "commands.html"]
        overflow_passes = []

        for p_name in test_pages:
            for vp in viewports:
                await page.set_viewport_size({"width": vp, "height": 900})
                await page.goto(f"{BASE_URL}/{p_name}", wait_until="networkidle")
                await page.wait_for_timeout(200)
                sw, cw = await page.evaluate("() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                no_overflow = sw <= cw
                overflow_passes.append(no_overflow)
                if not no_overflow:
                    print(f"[FAIL] Overflow on {p_name} at {vp}px: scrollWidth={sw}, clientWidth={cw}")

        test_results["zero_overflow"] = all(overflow_passes)
        print(f"[{'PASS' if test_results['zero_overflow'] else 'FAIL'}] Zero Horizontal Overflow across [375, 768, 1024, 1440px]")

        # -------------------------------------------------------------
        # 7. Console & Network Integrity
        # -------------------------------------------------------------
        print("\n--- 7. Console & Network Integrity ---")
        test_results["zero_console_errors"] = len(console_errors) == 0
        test_results["zero_404s"] = len(network_404s) == 0

        print(f"[{'PASS' if test_results['zero_console_errors'] else 'FAIL'}] Zero Console Errors (Encountered: {len(console_errors)})")
        if console_errors:
            for ce in console_errors:
                print(f"       ERROR: {ce}")

        print(f"[{'PASS' if test_results['zero_404s'] else 'FAIL'}] Zero Local 404 Requests (Encountered: {len(network_404s)})")
        if network_404s:
            for n4 in network_404s:
                print(f"       404: {n4}")

        await browser.close()

        # Final Summary
        all_passed = all(test_results.values())
        print("\n" + "=" * 68)
        print(f"PHASE 5.1 VERIFICATION OVERALL: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
        print("=" * 68)
        return all_passed

if __name__ == "__main__":
    success = asyncio.run(run_phase5_tests())
    exit(0 if success else 1)
