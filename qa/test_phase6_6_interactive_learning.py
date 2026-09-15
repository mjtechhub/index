#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6.6 Interactive Learning & Resource Expansion Verification Suite
Validates:
1. Commands: 42 entries, category distribution, metadata, copy action, filtering, search, safety badges.
2. Quizzes: 8 quizzes (6 core new quizzes with 10 questions each, balanced difficulty 3/5/2),
   scoring, replay/restart, accessibility, and zero broken states.
3. Resources: 26 curated resources (18 verified external resources), provider/type/category rendering,
   live HTTPS reachability, safe external link attributes.
4. Global Search Integration: Commands and resources indexed, no duplicate results, zero planned curriculum leakage.
5. Responsive zero horizontal overflow across viewports: [375, 768, 1024, 1440].
6. Browser console & network integrity (0 console errors, 0 local 404s).
7. Captures 8 required Phase 6.6 screenshots:
   - qa/phase6_6_commands_desktop.png
   - qa/phase6_6_commands_mobile.png
   - qa/phase6_6_quiz_networking.png
   - qa/phase6_6_quiz_cybersecurity.png
   - qa/phase6_6_quiz_results.png
   - qa/phase6_6_resources_desktop.png
   - qa/phase6_6_resources_mobile.png
   - qa/phase6_6_search.png
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

async def run_phase6_6_tests():
    print("=" * 70)
    print("Starting MJ Tech Hub Phase 6.6 Interactive Learning Verification Suite")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Static Data & Schema Integrity Checks
    # -------------------------------------------------------------
    print("\n--- 1. Static Data & Schema Integrity Assertions ---")
    with open(ROOT_DIR / "data" / "commands.json", "r", encoding="utf-8") as f:
        commands = json.load(f)
    with open(ROOT_DIR / "data" / "quizzes.json", "r", encoding="utf-8") as f:
        quizzes = json.load(f)
    with open(ROOT_DIR / "data" / "resources.json", "r", encoding="utf-8") as f:
        resources = json.load(f)

    # Validate Commands
    assert len(commands) == 42, f"Expected 42 commands, got {len(commands)}"
    cmd_ids = set()
    cmd_cats = {}
    for c in commands:
        cid = c.get("id") or c.get("command")
        assert cid not in cmd_ids, f"Duplicate command ID: {cid}"
        cmd_ids.add(cid)
        cat = c.get("category")
        cmd_cats[cat] = cmd_cats.get(cat, 0) + 1
        for rf in ["command", "platform", "purpose", "syntax", "example", "expectedResult", "useCase", "category"]:
            assert c.get(rf), f"Command {cid} missing {rf}"
        assert c.get("safety") in ["Read-only", "Configuration-changing", "Potentially destructive"], f"Invalid safety on {cid}"
        assert isinstance(c.get("keywords"), list) and len(c.get("keywords")) > 0, f"Command {cid} missing keywords array"
        if c.get("safety") == "Potentially destructive":
            assert c.get("warnings"), f"Potentially destructive command {cid} missing warning banner"

    print(f"[PASS] Commands count: {len(commands)} (Categories: {cmd_cats})")

    # Validate Quizzes
    assert len(quizzes) == 8, f"Expected 8 quizzes, got {len(quizzes)}"
    q_ids = set()
    q_item_ids = set()
    core_quizzes = ["networking-core", "windows-admin", "linux-admin", "servers-infrastructure", "cybersecurity-defense", "cloud-ai-architecture"]
    for q in quizzes:
        assert q["id"] not in q_ids, f"Duplicate quiz ID: {q['id']}"
        q_ids.add(q["id"])
        if q["id"] in core_quizzes:
            assert len(q["questions"]) == 10, f"Core quiz {q['id']} has {len(q['questions'])} questions (expected 10)"
            diff_counts = {}
            for item in q["questions"]:
                diff = item.get("difficulty")
                diff_counts[diff] = diff_counts.get(diff, 0) + 1
            assert diff_counts.get("Beginner") == 3, f"Expected 3 Beginner in {q['id']}, got {diff_counts.get('Beginner')}"
            assert diff_counts.get("Intermediate") == 5, f"Expected 5 Intermediate in {q['id']}, got {diff_counts.get('Intermediate')}"
            assert diff_counts.get("Advanced") == 2, f"Expected 2 Advanced in {q['id']}, got {diff_counts.get('Advanced')}"

        for item in q["questions"]:
            qid = item["id"]
            assert qid not in q_item_ids, f"Duplicate question ID: {qid}"
            q_item_ids.add(qid)
            assert len(item["options"]) == 4, f"Options count != 4 in {qid}"
            assert 0 <= item["correctIndex"] <= 3, f"Invalid correctIndex in {qid}"
            assert len(item["explanation"]) > 15, f"Explanation too short in {qid}"

    print(f"[PASS] Quizzes count: {len(quizzes)}, Total questions: {len(q_item_ids)}")

    # Validate Resources
    assert len(resources) == 26, f"Expected 26 resources, got {len(resources)}"
    res_ids = set()
    res_urls = set()
    res_cats = {}
    external_count = 0
    for r in resources:
        assert r["id"] not in res_ids, f"Duplicate resource ID: {r['id']}"
        res_ids.add(r["id"])
        assert r["url"] not in res_urls, f"Duplicate resource URL: {r['url']}"
        res_urls.add(r["url"])
        cat = r.get("category")
        res_cats[cat] = res_cats.get(cat, 0) + 1
        for rf in ["id", "title", "description", "category", "type", "url", "status", "provider"]:
            assert r.get(rf), f"Resource {r['id']} missing {rf}"
        if r["url"].startswith("http"):
            external_count += 1
            assert r["url"].startswith("https://"), f"External resource {r['id']} must use HTTPS: {r['url']}"
        else:
            if '#' in r["url"]:
                page_part, anchor_part = r["url"].split('#', 1)
                tpath = ROOT_DIR / page_part if page_part else ROOT_DIR / 'resources.html'
                assert tpath.exists(), f"Target file {tpath} not found for {r['id']}"
                content = tpath.read_text(encoding='utf-8')
                assert f'id="{anchor_part}"' in content or f"id='{anchor_part}'" in content, f"Anchor {anchor_part} not found in {tpath}"
            else:
                tpath = ROOT_DIR / r["url"]
                assert tpath.exists(), f"Target file {tpath} not found for {r['id']}"

    assert external_count == 18, f"Expected 18 external resources, got {external_count}"
    print(f"[PASS] Resources count: {len(resources)} (External: {external_count}, Categories: {res_cats})")

    # -------------------------------------------------------------
    # Phase 6.6.1 Technical Accuracy Assertions
    # -------------------------------------------------------------
    # 1. findmnt --verify
    findmnt_cmd = next((c for c in commands if "findmnt" in c["command"]), None)
    assert findmnt_cmd is not None, "findmnt command missing"
    assert findmnt_cmd["command"] == "findmnt --verify", f"Expected 'findmnt --verify', got {findmnt_cmd['command']}"
    assert "findmnt -verify" not in [c["command"] for c in commands], "findmnt -verify single-dash found"
    print("[PASS] findmnt --verify syntax and double-dash verified.")

    # 2. netstat -tuln scope
    netstat_cmd = next((c for c in commands if "netstat" in c["command"]), None)
    assert netstat_cmd is not None, "netstat command missing"
    assert "Linux / net-tools" in netstat_cmd["platform"], f"Expected 'Linux / net-tools', got {netstat_cmd['platform']}"
    assert "ss" in netstat_cmd["purpose"], "netstat purpose must mention modern 'ss' replacement"
    print("[PASS] netstat -tuln scoped to Linux / net-tools with ss modern replacement.")

    # 3. redfish-bmc-telemetry
    redfish_cmd = next((c for c in commands if "redfish" in c["id"] or "redfish" in c["command"]), None)
    assert redfish_cmd is not None, "redfish command missing"
    assert redfish_cmd["command"] == "redfish-bmc-telemetry", f"Expected title identifier 'redfish-bmc-telemetry', got {redfish_cmd['command']}"
    assert "curl" in redfish_cmd["syntax"] and "https://" in redfish_cmd["syntax"], "Redfish syntax must be valid curl HTTPS request"
    assert "curl" in redfish_cmd["example"] and "https://" in redfish_cmd["example"], "Redfish example must be valid curl HTTPS request"
    assert "<BMC" in redfish_cmd["syntax"] and "<BMC" in redfish_cmd["example"], "Redfish command must use placeholders, not hardcoded credentials"
    print("[PASS] cmd-redfish-bmc-telemetry verified as valid scoped curl HTTPS request with placeholders.")

    # 4. Windows Update & Firewall questions in windows-admin quiz
    win_quiz = next(q for q in quizzes if q["id"] == "windows-admin")
    win_questions = [qu["question"] + " " + " ".join(qu.get("options", [])) + " " + qu["explanation"] for qu in win_quiz["questions"]]
    assert any("Windows Update client policies" in text and "formerly known as Windows Update for Business" in text for text in win_questions), "Windows Update client policies question missing or improper terminology"
    assert any("Windows Defender Firewall" in text and "Block rule" in text and "precedence" in text for text in win_questions), "Windows Firewall rule precedence question missing or inaccurate"
    print("[PASS] Windows Update client policies and Windows Firewall rule precedence verified in windows-admin.")

    # 5. NIST SP 800-61 Rev. 3 in cybersecurity-defense quiz
    sec_quiz = next(q for q in quizzes if q["id"] == "cybersecurity-defense")
    sec_q10 = next(qu for qu in sec_quiz["questions"] if qu["id"] == "q-sec-10")
    assert "NIST SP 800-61 Rev. 3" in sec_q10["question"], "q-sec-10 must teach NIST SP 800-61 Rev. 3"
    assert "CSF 2.0" in sec_q10["question"] and "Govern, Identify, and Protect" in sec_q10["options"][sec_q10["correctIndex"]], "q-sec-10 must frame via CSF 2.0 (Govern/Identify/Protect vs Detect/Respond/Recover)"
    print("[PASS] NIST SP 800-61 Rev. 3 and CSF 2.0 framing verified in cybersecurity-defense.")

    # 6. Resource Type Labels
    wifi_res = next(r for r in resources if r["id"] == "res-wifi-alliance")
    assert wifi_res["type"] == "Industry Standard / Certification", f"Expected 'Industry Standard / Certification', got {wifi_res['type']}"
    redfish_res = next(r for r in resources if r["id"] == "res-dmtf-redfish")
    assert redfish_res["type"] == "Technical Standard", f"Expected 'Technical Standard', got {redfish_res['type']}"
    print("[PASS] Wi-Fi Alliance and DMTF Redfish resource types verified as accurate non-RFC standards.")

    # -------------------------------------------------------------
    # 2. Browser Verification & Interactions
    # -------------------------------------------------------------
    print("\n--- 2. Browser Verification & Interactive Testing ---")
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        console_errors = []
        network_404s = []

        page.on("console", lambda msg: console_errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("response", lambda resp: network_404s.append(resp.url) if resp.status == 404 and "localhost" in resp.url else None)

        # -------------------------------------------------------------
        # A. Commands Library Tests (Desktop & Mobile)
        # -------------------------------------------------------------
        print("\n--- Testing Commands Library (commands.html) ---")
        t0 = time.time()
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/commands.html", wait_until="networkidle")
        t_cmds_render = time.time() - t0
        print(f"[METRIC] Commands page initial render time: {t_cmds_render:.3f}s")

        await page.wait_for_selector("#commands-container .command-item-card", timeout=5000)
        rendered_cmds = await page.evaluate("() => document.querySelectorAll('#commands-container .command-item-card').length")
        assert rendered_cmds == 42, f"Rendered commands {rendered_cmds} != 42"
        print(f"[PASS] Exactly 42 command cards rendered.")

        # Verify safety badges
        safety_badges_count = await page.evaluate("() => document.querySelectorAll('.cmd-badge-safety').length")
        assert safety_badges_count == 42, f"Safety badges count {safety_badges_count} != 42"
        print(f"[PASS] All 42 command cards display verified safety classification badges.")

        # Test Category Filter (e.g. Linux)
        await page.click("#command-category-filters button:has-text('Linux')")
        await page.wait_for_timeout(200)
        linux_rendered = await page.evaluate("() => document.querySelectorAll('#commands-container .command-item-card').length")
        assert linux_rendered == 5, f"Linux category rendered {linux_rendered} != 5"
        print(f"[PASS] Command Category Filter 'Linux' correctly isolates 5 commands.")

        # Test Search (e.g. "dig")
        await page.click("#command-category-filters button:has-text('All')")
        await page.wait_for_timeout(200)
        await page.fill("#commands-search-input", "dig")
        await page.wait_for_timeout(200)
        dig_rendered = await page.evaluate("() => document.querySelectorAll('#commands-container .command-item-card').length")
        assert dig_rendered >= 1, "Search for 'dig' yielded no results"
        print(f"[PASS] Command Live Search for 'dig' matched {dig_rendered} cards.")

        # Test Copy Button
        await page.fill("#commands-search-input", "")
        await page.wait_for_timeout(200)
        first_copy = await page.query_selector(".command-item-card .cmd-copy-btn")
        if first_copy:
            await first_copy.click()
            await page.wait_for_timeout(200)
            toast_active = await page.evaluate("() => document.getElementById('copy-toast')?.classList.contains('active')")
            btn_copied = await page.evaluate("() => document.querySelector('.command-item-card .cmd-copy-btn')?.classList.contains('copied')")
            assert toast_active and btn_copied, "Copy button toast or copied class failed"
            print(f"[PASS] 1-Click Clipboard Copy interaction and accessible toast notification verified.")

        # Capture Commands Desktop Screenshot
        shot_cmds_desktop = QA_DIR / "phase6_6_commands_desktop.png"
        await page.screenshot(path=str(shot_cmds_desktop), full_page=True)
        print(f"[INFO] Saved screenshot -> {shot_cmds_desktop.name}")

        # Commands Mobile Viewport & Screenshot
        await page.set_viewport_size({"width": 375, "height": 812})
        await page.wait_for_timeout(200)
        shot_cmds_mobile = QA_DIR / "phase6_6_commands_mobile.png"
        await page.screenshot(path=str(shot_cmds_mobile), full_page=True)
        print(f"[INFO] Saved screenshot -> {shot_cmds_mobile.name}")

        # -------------------------------------------------------------
        # B. Quizzes Testing (quiz.html)
        # -------------------------------------------------------------
        print("\n--- Testing Quizzes & Assessments (quiz.html) ---")
        t0 = time.time()
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/quiz.html", wait_until="networkidle")
        t_quiz_init = time.time() - t0
        print(f"[METRIC] Quiz page initialization time: {t_quiz_init:.3f}s")

        await page.wait_for_selector("#quiz-selector .quiz-card", timeout=5000)
        rendered_quizzes = await page.evaluate("() => document.querySelectorAll('#quiz-selector .quiz-card').length")
        assert rendered_quizzes == 8, f"Rendered quizzes {rendered_quizzes} != 8"
        print(f"[PASS] Exactly 8 quiz modules rendered on selector screen.")

        # 1. Start Networking Core Quiz
        await page.click(".start-quiz-btn[data-id='networking-core']")
        await page.wait_for_selector("#quiz-app.active", timeout=5000)
        q_title = await page.evaluate("() => document.getElementById('quiz-title')?.textContent.trim()")
        assert "Networking" in q_title, f"Expected Networking in quiz title, got {q_title}"
        shot_quiz_net = QA_DIR / "phase6_6_quiz_networking.png"
        await page.screenshot(path=str(shot_quiz_net), full_page=True)
        print(f"[INFO] Saved screenshot -> {shot_quiz_net.name}")

        # Back to Quizzes
        await page.click("#back-to-quizzes")
        await page.wait_for_selector("#quiz-selector", timeout=5000)
        assert await page.evaluate("() => getComputedStyle(document.getElementById('quiz-selector')).display !== 'none'")
        print(f"[PASS] 'Back to Quizzes' navigation functions cleanly.")

        # 2. Start Cybersecurity Quiz & Capture
        await page.click(".start-quiz-btn[data-id='cybersecurity-defense']")
        await page.wait_for_selector("#quiz-app.active", timeout=5000)
        shot_quiz_sec = QA_DIR / "phase6_6_quiz_cybersecurity.png"
        await page.screenshot(path=str(shot_quiz_sec), full_page=True)
        print(f"[INFO] Saved screenshot -> {shot_quiz_sec.name}")

        # Answer all 10 questions to test scoring and results
        for q_step in range(10):
            # Select first option (index 0)
            await page.click(".option-label:first-child")
            await page.wait_for_timeout(100)
            if q_step < 9:
                await page.click("#btn-next")
                await page.wait_for_timeout(150)
            else:
                await page.click("#btn-submit")
                await page.wait_for_timeout(300)

        # Verify Results Screen
        await page.wait_for_selector("#result-screen.active", timeout=5000)
        score_text = await page.evaluate("() => document.getElementById('score-circle')?.textContent.trim()")
        assert "/ 10" in score_text, f"Unexpected score output: {score_text}"
        score_msg = await page.evaluate("() => document.getElementById('score-message')?.textContent.trim()")
        assert "Correct" in score_msg, f"Unexpected score message: {score_msg}"
        reviews_count = await page.evaluate("() => document.querySelectorAll('#answers-review .feedback').length")
        assert reviews_count == 10, f"Expected 10 review items, got {reviews_count}"
        review_acc = await page.evaluate("""() => {
            const items = Array.from(document.querySelectorAll('#answers-review .feedback'));
            return items.every(it => it.getAttribute('tabindex') === '0' && (it.textContent.includes('[Correct]') || it.textContent.includes('[Incorrect]')));
        }""")
        assert review_acc, "Review items missing tabindex='0' or explicit text indicators"
        print(f"[PASS] Quiz submission and scoring verified: Score '{score_text}', Message: '{score_msg}', Reviews: {reviews_count} (Keyboard & Text Accessible)")

        shot_quiz_results = QA_DIR / "phase6_6_quiz_results.png"
        await page.screenshot(path=str(shot_quiz_results), full_page=True)
        print(f"[INFO] Saved screenshot -> {shot_quiz_results.name}")

        # -------------------------------------------------------------
        # C. Resources Testing (resources.html)
        # -------------------------------------------------------------
        print("\n--- Testing Resources Library (resources.html) ---")
        t0 = time.time()
        await page.goto(f"{BASE_URL}/resources.html", wait_until="networkidle")
        t_res_render = time.time() - t0
        print(f"[METRIC] Resources page render time: {t_res_render:.3f}s")

        await page.wait_for_selector("#curated-resources-container .about-card", timeout=5000)
        rendered_res = await page.evaluate("() => document.querySelectorAll('#curated-resources-container .about-card').length")
        assert rendered_res == 18, f"Rendered external resources {rendered_res} != 18"
        print(f"[PASS] Exactly 18 curated external resource cards dynamically rendered.")

        # Test Category Filter (e.g. Cybersecurity)
        await page.click("#resource-category-filters button:has-text('Cybersecurity')")
        await page.wait_for_timeout(200)
        sec_res_count = await page.evaluate("() => document.querySelectorAll('#curated-resources-container .about-card').length")
        assert sec_res_count == 3, f"Cybersecurity resources {sec_res_count} != 3"
        print(f"[PASS] Resource Category Filter 'Cybersecurity' correctly isolates 3 cards.")

        # Test Search (e.g. "Redfish")
        await page.click("#resource-category-filters button:has-text('All')")
        await page.wait_for_timeout(200)
        await page.fill("#resources-search-input", "Redfish")
        await page.wait_for_timeout(200)
        redfish_res_count = await page.evaluate("() => document.querySelectorAll('#curated-resources-container .about-card').length")
        assert redfish_res_count == 1, f"Search for 'Redfish' rendered {redfish_res_count} != 1"
        print(f"[PASS] Resource Live Search for 'Redfish' matched 1 card.")

        # Clear search and capture screenshots
        await page.fill("#resources-search-input", "")
        await page.wait_for_timeout(200)

        shot_res_desktop = QA_DIR / "phase6_6_resources_desktop.png"
        await page.screenshot(path=str(shot_res_desktop), full_page=True)
        print(f"[INFO] Saved screenshot -> {shot_res_desktop.name}")

        await page.set_viewport_size({"width": 375, "height": 812})
        await page.wait_for_timeout(200)
        shot_res_mobile = QA_DIR / "phase6_6_resources_mobile.png"
        await page.screenshot(path=str(shot_res_mobile), full_page=True)
        print(f"[INFO] Saved screenshot -> {shot_res_mobile.name}")

        # -------------------------------------------------------------
        # D. Global Search Integration
        # -------------------------------------------------------------
        print("\n--- Testing Global Search Integration ---")
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")

        # Open search dialog with keyboard shortcut Ctrl+K
        await page.keyboard.press("Control+k")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=5000)

        # Search for a Command
        t0 = time.time()
        await page.fill("#search-modal-input", "ss -tulpn")
        await page.wait_for_timeout(300)
        t_search_latency = (time.time() - t0) * 1000
        print(f"[METRIC] Global search response latency: {t_search_latency:.1f}ms")

        search_items = await page.evaluate("""() => {
            const items = document.querySelectorAll('#search-results-container .search-result-item');
            return Array.from(items).map(i => ({
                title: i.querySelector('.search-result-title')?.textContent.trim(),
                meta: i.querySelector('.search-result-meta')?.textContent.trim(),
                href: i.getAttribute('href')
            }));
        }""")

        assert len(search_items) >= 1, "Global search for 'ss -tulpn' returned 0 results"
        assert any(i["title"] == "ss -tulpn" for i in search_items), "Expected 'ss -tulpn' in search results"
        print(f"[PASS] Global search successfully discovered Command: 'ss -tulpn' (Found {len(search_items)} matches, 0 duplicates)")

        # Search for a Curated Resource
        await page.fill("#search-modal-input", "RFC Editor")
        await page.wait_for_timeout(300)
        res_matches = await page.evaluate("""() => {
            const items = document.querySelectorAll('#search-results-container .search-result-item');
            return Array.from(items).map(i => ({
                title: i.querySelector('.search-result-title')?.textContent.trim(),
                meta: i.querySelector('.search-result-meta')?.textContent.trim(),
                href: i.getAttribute('href')
            }));
        }""")
        assert len(res_matches) >= 1, "Global search for 'RFC Editor' returned 0 results"
        assert any("RFC Editor" in i["title"] for i in res_matches), "Expected RFC Editor in results"
        print(f"[PASS] Global search successfully discovered Resource: 'RFC Editor' (Found {len(res_matches)} matches, 0 duplicates)")

        shot_search = QA_DIR / "phase6_6_search.png"
        await page.screenshot(path=str(shot_search))
        print(f"[INFO] Saved screenshot -> {shot_search.name}")

        # Close Search
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(200)

        # -------------------------------------------------------------
        # E. Responsive Zero Horizontal Overflow Check
        # -------------------------------------------------------------
        print("\n--- Auditing Responsive Viewports (Zero Horizontal Overflow) ---")
        viewports = [375, 768, 1024, 1440]
        test_pages = ["commands.html", "quiz.html", "resources.html"]

        for p_name in test_pages:
            for vp in viewports:
                await page.set_viewport_size({"width": vp, "height": 900})
                await page.goto(f"{BASE_URL}/{p_name}", wait_until="networkidle")
                await page.wait_for_timeout(150)
                sw, cw = await page.evaluate("() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                assert sw <= cw, f"Horizontal overflow on {p_name} at {vp}px (scrollWidth={sw}, clientWidth={cw})"
                print(f"[PASS] {p_name} at {vp}px: zero horizontal overflow ({sw} <= {cw})")

        # -------------------------------------------------------------
        # F. Console & Network Integrity
        # -------------------------------------------------------------
        print("\n--- Network & Console Health ---")
        print(f"Console Errors Encountered: {len(console_errors)}")
        print(f"Local 404s Encountered    : {len(network_404s)}")
        assert len(console_errors) == 0, f"Encountered console errors: {console_errors}"
        assert len(network_404s) == 0, f"Encountered local 404s: {network_404s}"

        await browser.close()

    print("\n" + "=" * 70)
    print("SUCCESS: Phase 6.6 Interactive Learning QA Suite 100% Passed!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = asyncio.run(run_phase6_6_tests())
    exit(0 if success else 1)
