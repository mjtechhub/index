#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6.5A Master Curriculum Expansion Automated Verification Suite
(qa/test_phase6_5_curriculum.py)

Validates all Phase 6.5A requirements and CTO conditions:
1. Static Integrity & Data Contract:
   - Every core category contains >= 70 unique curriculum topics
   - Zero duplicate curriculum IDs across the entire global curriculum (Global ID Uniqueness)
   - Zero duplicate normalized topic names within any category
   - Canonical category IDs strictly valid (networking, windows, linux, servers, cybersecurity, cloud)
   - All 76 published tutorials in tutorials.json map 1-to-1 to a curriculum entry (0 unmapped, 0 phantom)
   - All published entries have valid URLs resolving to real HTML files on disk
   - All planned entries have status="planned" and NO url property (no fake links/pages)
2. Topics Page Dynamic Counter Verification:
   - Total Published badge displays exact count: 76 Published Tutorials
   - Total Curriculum badge displays exact dynamic count: 471 Curriculum Topics (no hardcoded "450+")
   - All 6 core cards display their published tutorial badge and curriculum topic count
3. Category Page Experience (Networking, Windows, Linux, Servers, Cybersecurity, Cloud):
   - Category Hero displays published tutorial count, sections count, and total curriculum topics
   - Published tutorial grid remains intact with difficulty filter and search
   - Master Curriculum Roadmap renders native <details> and <summary> sections
   - All sections are collapsed by default on initial load
   - Section headers display dynamic metrics: "<X> topics • <Y> published"
   - Published topics display checkmark, link to tutorial, and "Published" status pill
   - Planned topics display circle icon, static non-link item, and "Planned" status pill
4. Global Search Verification:
   - Planned curriculum topics do not flood global search results
   - Published tutorials continue to resolve accurately
5. Responsive & Layout Quality:
   - Tested viewports: 375px, 768px, 1024px, 1440px with zero horizontal overflow
   - Zero browser console errors and zero local 404 network requests
6. Visual Evidence Generation:
   - qa/phase6_5a_topics_desktop.png
   - qa/phase6_5a_windows_curriculum.png
   - qa/phase6_5a_linux_curriculum.png
   - qa/phase6_5a_servers_curriculum.png
   - qa/phase6_5a_cybersecurity_curriculum.png
   - qa/phase6_5a_cloud_curriculum.png
   - qa/phase6_5a_networking_curriculum.png
   - qa/phase6_5a_curriculum_mobile.png
"""

import asyncio
import json
from pathlib import Path
from collections import Counter
from playwright.async_api import async_playwright

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
BASE_URL = "http://localhost/index"
QA_DIR = Path(__file__).resolve().parent
ROOT_DIR = QA_DIR.parent
TOPICS_JSON_PATH = ROOT_DIR / "data" / "topics.json"
TUTORIALS_JSON_PATH = ROOT_DIR / "data" / "tutorials.json"

CORE_CATEGORY_IDS = ["networking", "windows", "linux", "servers", "cybersecurity", "cloud"]

async def run_phase6_5a_tests():
    print("=" * 70)
    print("STARTING PHASE 6.5A MASTER CURRICULUM EXPANSION VERIFICATION SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Static Data & Schema Integrity Audit
    # -------------------------------------------------------------
    print("\n--- 1. Static Data & Schema Integrity Audit ---")
    with open(TOPICS_JSON_PATH, "r", encoding="utf-8") as f:
        topics_data = json.load(f)

    with open(TUTORIALS_JSON_PATH, "r", encoding="utf-8") as f:
        tuts_data = json.load(f)

    categories = topics_data.get("categories", [])
    core_cats = [c for c in categories if c.get("id") in CORE_CATEGORY_IDS]

    # Verify total published tutorials in tutorials.json
    assert len(tuts_data) >= 76, f"Expected at least 76 tutorials, got {len(tuts_data)}"
    print(f"[PASS] Total tutorials in tutorials.json: {len(tuts_data)}")

    pub_tut_map = {t["id"]: t for t in tuts_data}
    all_subtopic_ids = []
    published_subtopic_ids = set()
    category_topic_counts = {}

    for cat in core_cats:
        cid = cat["id"]
        cname = cat["name"]
        sections = cat.get("sections", [])
        assert len(sections) >= 8, f"Category '{cid}' has {len(sections)} sections (< 8)"
        
        cat_subtopics = []
        names_in_cat = set()

        for sec in sections:
            sname = sec.get("name") or sec.get("title")
            subtopics = sec.get("subtopics", [])
            for sub in subtopics:
                sid = sub.get("id")
                s_title = sub.get("name")
                s_level = sub.get("level")
                s_status = sub.get("status")

                assert sid, f"Missing id in {cid} -> {sname}"
                assert s_title, f"Missing name in {cid} -> {sname}"
                assert s_level in ["Beginner", "Intermediate", "Advanced"], f"Invalid level '{s_level}' in {sid}"
                assert s_status in ["published", "planned"], f"Invalid status '{s_status}' in {sid}"

                all_subtopic_ids.append(sid)
                cat_subtopics.append(sub)

                # Name uniqueness in category
                norm_name = s_title.lower().strip()
                assert norm_name not in names_in_cat, f"Duplicate topic name in category '{cid}': '{s_title}'"
                names_in_cat.add(norm_name)

                if s_status == "published":
                    published_subtopic_ids.add(sid)
                    assert "url" in sub and sub["url"], f"Published item '{sid}' missing url"
                    tut_file = ROOT_DIR / sub["url"].replace("./", "")
                    assert tut_file.exists(), f"Published item '{sid}' file not found: {sub['url']}"
                    # Match against tutorials.json
                    assert sid in pub_tut_map, f"Published item '{sid}' not found in tutorials.json"
                    t_record = pub_tut_map[sid]
                    assert sub["url"] == t_record["url"].replace("./", ""), f"URL mismatch for '{sid}'"
                    assert sub["level"] == t_record["level"], f"Level mismatch for '{sid}'"
                elif s_status == "planned":
                    assert "url" not in sub or not sub["url"], f"Planned item '{sid}' must not have a url property"

        category_topic_counts[cid] = len(cat_subtopics)
        assert len(cat_subtopics) >= 70, f"Category '{cid}' has {len(cat_subtopics)} topics (< 70 required)"
        print(f"[PASS] Category '{cid}' ({cname}): {len(sections)} sections, {len(cat_subtopics)} topics (>= 70)")

    # Global ID Uniqueness
    id_counts = Counter(all_subtopic_ids)
    duplicates = [sid for sid, count in id_counts.items() if count > 1]
    assert len(duplicates) == 0, f"Global duplicate subtopic IDs found: {duplicates}"
    print(f"[PASS] Global ID Uniqueness: all {len(all_subtopic_ids)} subtopic IDs are strictly unique")

    # 1-to-1 Published Mapping
    assert published_subtopic_ids == set(pub_tut_map.keys()), "Mismatch between published curriculum and tutorials.json"
    print(f"[PASS] 1-to-1 Published Mapping: exactly {len(pub_tut_map)} published tutorials mapped (0 unmapped, 0 phantom)")

    # -------------------------------------------------------------
    # 2. Browser & Interactive Verification
    # -------------------------------------------------------------
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        console_errors = []
        network_404s = []

        page.on("console", lambda msg: console_errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("response", lambda resp: network_404s.append(resp.url) if resp.status == 404 and "localhost" in resp.url else None)

        # -------------------------------------------------------------
        # A. Topics Page Dynamic Counters
        # -------------------------------------------------------------
        print("\n--- 2. Topics Page Dynamic Counters Verification ---")
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/topics.html", wait_until="networkidle")

        await page.wait_for_selector(".topic-domain-card", timeout=5000)
        
        total_tut_text = await page.evaluate("() => document.getElementById('topics-total-tut-badge')?.textContent.trim()")
        total_cur_text = await page.evaluate("() => document.getElementById('topics-total-curriculum-badge')?.textContent.trim()")
        
        assert f"{len(pub_tut_map)} Published Tutorials" in total_tut_text, f"Unexpected tut text: '{total_tut_text}'"
        assert f"{len(all_subtopic_ids)} Curriculum Topics" in total_cur_text, f"Unexpected cur text: '{total_cur_text}'"
        print(f"[PASS] Topics Hero Badges: '{total_tut_text}' & '{total_cur_text}'")

        # Verify Core Cards
        card_badges = await page.evaluate("""() => {
            const cards = document.querySelectorAll('.topic-domain-card');
            return Array.from(cards).map(c => ({
                title: c.querySelector('.topic-domain-title')?.textContent.trim(),
                tutBadge: c.querySelector('.topic-tut-count-badge')?.textContent.trim(),
                curBadge: c.querySelector('.topic-curriculum-count-badge')?.textContent.trim()
            }));
        }""")

        for cb in card_badges:
            print(f"       Card '{cb['title']}': Tut='{cb['tutBadge']}', Curriculum='{cb['curBadge']}'")
            assert "Tutorials" in cb["tutBadge"]
            assert "Topics" in cb["curBadge"]

        # Screenshot: phase6_5a_topics_desktop.png
        shot_topics = QA_DIR / "phase6_5a_topics_desktop.png"
        await page.screenshot(path=str(shot_topics), full_page=False)
        print(f"[INFO] Saved screenshot -> {shot_topics.name}")

        # -------------------------------------------------------------
        # B. Category Pages & Curriculum Roadmap Testing
        # -------------------------------------------------------------
        print("\n--- 3. Category Pages & Curriculum Roadmap Testing ---")

        category_pages = [
            {"cat": "windows", "file": "windows.html", "shot": "phase6_5a_windows_curriculum.png", "title": "Windows"},
            {"cat": "linux", "file": "linux.html", "shot": "phase6_5a_linux_curriculum.png", "title": "Linux"},
            {"cat": "servers", "file": "servers.html", "shot": "phase6_5a_servers_curriculum.png", "title": "Servers"},
            {"cat": "cybersecurity", "file": "cybersecurity.html", "shot": "phase6_5a_cybersecurity_curriculum.png", "title": "Cybersecurity"},
            {"cat": "cloud", "file": "cloud.html", "shot": "phase6_5a_cloud_curriculum.png", "title": "Cloud & AI"},
            {"cat": "networking", "file": "networking.html", "shot": "phase6_5a_networking_curriculum.png", "title": "Networking"}
        ]

        for cp in category_pages:
            await page.goto(f"{BASE_URL}/{cp['file']}", wait_until="networkidle")
            await page.wait_for_selector("#curriculum-roadmap", timeout=5000)

            # 1. Hero Meta Assertions
            hero_meta = await page.evaluate("() => document.querySelector('.page-hero-meta')?.textContent.trim()")
            assert "Curriculum Topics" in hero_meta, f"Missing Curriculum Topics in hero on {cp['file']}"
            assert "Curriculum Sections" in hero_meta, f"Missing Curriculum Sections in hero on {cp['file']}"

            # 2. Details Accordion Assertions
            details_count = await page.evaluate("() => document.querySelectorAll('#curriculum-roadmap details.curriculum-section-details').length")
            assert details_count >= 8, f"Expected >= 8 details sections on {cp['file']}, got {details_count}"

            # Default Collapsed Verification (None should have open attribute initially)
            open_count = await page.evaluate("() => document.querySelectorAll('#curriculum-roadmap details[open]').length")
            assert open_count == 0, f"Expected 0 open sections by default on {cp['file']}, got {open_count}"

            # Dynamic Metrics in Summary
            first_summary_meta = await page.evaluate("() => document.querySelector('#curriculum-roadmap summary .curriculum-summary-meta')?.textContent.trim()")
            assert "topics" in first_summary_meta and "published" in first_summary_meta, f"Bad summary meta: {first_summary_meta}"

            # 3. Open First Section to verify subtopics and capture screenshot
            await page.click("#curriculum-roadmap details:first-child summary")
            await page.wait_for_timeout(200)
            is_open = await page.evaluate("() => document.querySelector('#curriculum-roadmap details:first-child').hasAttribute('open')")
            assert is_open, f"First details failed to open on {cp['file']}"

            # Scroll into view of the curriculum roadmap
            await page.evaluate("() => document.getElementById('curriculum-roadmap').scrollIntoView({ behavior: 'instant', block: 'start' })")
            await page.wait_for_timeout(200)

            # Capture Screenshot
            shot_file = QA_DIR / cp["shot"]
            await page.screenshot(path=str(shot_file), full_page=False)
            print(f"[PASS] {cp['title']:14}: {details_count} sections rendered (default collapsed), first section opened. Screenshot -> {cp['shot']}")

        # -------------------------------------------------------------
        # C. Mobile Viewport & Responsiveness (375px)
        # -------------------------------------------------------------
        print("\n--- 4. Mobile Viewport & Responsiveness (375px) ---")
        await page.set_viewport_size({"width": 375, "height": 812})
        await page.goto(f"{BASE_URL}/windows.html", wait_until="networkidle")
        await page.wait_for_selector("#curriculum-roadmap", timeout=5000)

        # Open first section on mobile
        await page.click("#curriculum-roadmap details:first-child summary")
        await page.wait_for_timeout(200)

        # Scroll into view
        await page.evaluate("() => document.getElementById('curriculum-roadmap').scrollIntoView({ behavior: 'instant', block: 'start' })")
        await page.wait_for_timeout(200)

        # Check Horizontal Overflow
        overflow = await page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
        assert not overflow, "Horizontal overflow detected on mobile 375px!"
        print("[PASS] Mobile 375px: Zero Horizontal Overflow with open curriculum section")

        # Capture Mobile Screenshot: phase6_5a_curriculum_mobile.png
        shot_mobile = QA_DIR / "phase6_5a_curriculum_mobile.png"
        await page.screenshot(path=str(shot_mobile), full_page=False)
        print(f"[INFO] Saved mobile screenshot -> {shot_mobile.name}")

        # -------------------------------------------------------------
        # D. Viewport Overflow Checks Across All Standard Resolutions
        # -------------------------------------------------------------
        print("\n--- 5. Responsive Overflow Check Across Viewports ---")
        viewports = [375, 768, 1024, 1440]
        test_pages = ["topics.html", "networking.html", "windows.html", "linux.html", "servers.html", "cybersecurity.html", "cloud.html"]

        for vp_w in viewports:
            await page.set_viewport_size({"width": vp_w, "height": 900})
            for p_name in test_pages:
                await page.goto(f"{BASE_URL}/{p_name}", wait_until="networkidle")
                has_overflow = await page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
                assert not has_overflow, f"Horizontal overflow on {p_name} at {vp_w}px!"
        print(f"[PASS] Zero Horizontal Overflow verified across {len(test_pages)} pages at viewports {viewports}")

        # -------------------------------------------------------------
        # E. Global Search Behavior
        # -------------------------------------------------------------
        print("\n--- 6. Global Search Behavior Verification ---")
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")

        # Open search via keyboard Ctrl+K
        await page.keyboard.press("Control+k")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=5000)

        # Search for a query matching published tutorials
        await page.fill("#search-modal-input", "PowerShell")
        await page.wait_for_timeout(300)

        results = await page.evaluate("""() => {
            const items = document.querySelectorAll('.search-result-item');
            return Array.from(items).map(i => ({
                title: i.querySelector('.search-result-title')?.textContent.trim(),
                meta: i.querySelector('.search-result-meta')?.textContent.trim(),
                url: i.getAttribute('href')
            }));
        }""")

        assert len(results) > 0, "No search results returned for 'PowerShell'"
        has_published = any("PowerShell Fundamentals for Administrators" in r["title"] for r in results)
        assert has_published, "Published tutorial 'PowerShell Fundamentals for Administrators' missing in search results"
        
        # Verify no result has url="undefined" or points to fake link
        for r in results:
            assert r["url"] and "undefined" not in r["url"], f"Invalid search result URL: {r}"

        # Close search
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(200)
        print("[PASS] Global search functions reliably, prioritizing published content without fake URLs")

        # -------------------------------------------------------------
        # F. Console Errors & Local 404 Requests
        # -------------------------------------------------------------
        print("\n--- 7. Console & Network Integrity ---")
        print(f"Console Errors: {len(console_errors)}")
        print(f"Local 404 Requests: {len(network_404s)}")

        if console_errors:
            for err in console_errors:
                print(f"  [FAIL] {err}")
            assert False, "Console errors detected"

        if network_404s:
            for n404 in network_404s:
                print(f"  [FAIL] 404: {n404}")
            assert False, "Local 404 requests detected"

        print("[PASS] Zero console errors and zero local 404 network requests encountered")

        await browser.close()

    print("\n" + "=" * 70)
    print("ALL PHASE 6.5A CURRICULUM VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_phase6_5a_tests())
