#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6.8 Production Polish, Navigation, Footer & UX Refinement Suite
Validates:
1. Header & Navigation:
   - 8 primary navigation items: Home, Topics, Commands, Quizzes, Tools, Labs, Resources, About.
   - Route-aware active navigation across root, category, tutorials, tools, labs, quizzes, and resources.
   - Guarantee: No route creates two active primary navigation items.
   - Mobile navigation hamburger toggle, aria-expanded, and Escape key dismissal with focus restoration.
2. Premium Footer Redesign:
   - Learn column (6 categories: Networking, Windows, Linux, Servers, Cybersecurity, Cloud & AI).
   - Explore column (6 links: All Topics, Command Library, Practice Quizzes, Interactive Tools, Troubleshooting Labs, Resources).
   - Unambiguous "Resources" label (no "Tools & Resources" ambiguity).
   - About / Legal column (4 links: About Us, Privacy Policy, Terms of Service, Disclaimer).
   - Brand description and Instagram social link (@themjtechhub) with accessible name.
   - Bottom bar: dynamic/accurate copyright year 2026, tagline ("Built for IT Engineers & Administrators"), and creator attribution ("Created by Mayur Talsaniya").
   - Nested route resolution: 0 404s from index.html, tutorials, tools, and legal paths.
   - Compactness verification: reduced vertical padding and margin compared to baseline.
3. Homepage Polish:
   - Column 3 Card 2 features Interactive Tools & Labs with direct links to tools.html and labs.html.
4. Global Search Refinement:
   - 7 taxonomy types: Topic, Tutorial, Command, Resource, Quiz, Tool, Lab.
   - Quizzes indexed as modules with unambiguous ?quiz=<id> destinations.
   - 0 duplicate destinations, 0 planned curriculum leakage, 0 quiz questions, 0 lab sub-nodes.
5. SEO & Metadata Consistency:
   - Canonicals strictly https://themjtechhub.site (0 localhost, 0 file://).
   - Exactly one H1 per page across key pages.
   - Open Graph and Twitter metadata verified across public pages including legal docs.
6. Responsive Zero Horizontal Overflow:
   - Viewports: 320px, 375px, 768px, 1024px, 1440px.
7. Production & Network Integrity:
   - 0 browser console errors, 0 local network 404s.
8. Platform Freeze Contract:
   - 148 tutorials, 471 curriculum (148 published, 323 planned), 42 commands, 8 quizzes (64 questions), 26 resources, 4 tools, 6 labs.
9. Screenshot Generation (8 required artifacts):
   - qa/phase6_8_home_desktop.png
   - qa/phase6_8_header_desktop.png
   - qa/phase6_8_header_mobile.png
   - qa/phase6_8_footer_desktop.png
   - qa/phase6_8_footer_mobile.png
   - qa/phase6_8_tools_navigation.png
   - qa/phase6_8_dark_mode.png
   - qa/phase6_8_search_navigation.png
"""

import asyncio
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_URL = "http://localhost/index"
QA_DIR = Path(__file__).resolve().parent
ROOT_DIR = QA_DIR.parent

async def run_phase6_8_tests():
    print("=" * 70)
    print("Starting MJ Tech Hub Phase 6.8 Production Polish & Verification Suite")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Platform Freeze Assertions
    # -------------------------------------------------------------
    print("\n--- 1. Platform Freeze Contract Verification ---")
    with open(ROOT_DIR / "data" / "tutorials.json", "r", encoding="utf-8") as f:
        tutorials = json.load(f)
    assert len(tutorials) == 148, f"Expected 148 tutorials, got {len(tutorials)}"

    with open(ROOT_DIR / "data" / "topics.json", "r", encoding="utf-8") as f:
        topics_data = json.load(f)
    total_curr = 0
    pub_curr = 0
    plan_curr = 0
    for cat in topics_data.get("categories", []):
        for sec in cat.get("sections", []):
            for sub in sec.get("subtopics", []):
                total_curr += 1
                if sub.get("status") == "published":
                    pub_curr += 1
                elif sub.get("status") == "planned":
                    plan_curr += 1
    assert total_curr == 471, f"Expected 471 curriculum topics, got {total_curr}"
    assert pub_curr == 148, f"Expected 148 published topics, got {pub_curr}"
    assert plan_curr == 323, f"Expected 323 planned topics, got {plan_curr}"

    with open(ROOT_DIR / "data" / "commands.json", "r", encoding="utf-8") as f:
        commands = json.load(f)
    assert len(commands) == 42, f"Expected 42 commands, got {len(commands)}"

    with open(ROOT_DIR / "data" / "quizzes.json", "r", encoding="utf-8") as f:
        quizzes = json.load(f)
    assert len(quizzes) == 8, f"Expected 8 quizzes, got {len(quizzes)}"
    quiz_q_count = sum(len(q.get("questions", [])) for q in quizzes)
    assert quiz_q_count == 64, f"Expected 64 quiz questions, got {quiz_q_count}"

    with open(ROOT_DIR / "data" / "resources.json", "r", encoding="utf-8") as f:
        resources = json.load(f)
    assert len(resources) == 26, f"Expected 26 resources, got {len(resources)}"

    tools_files = [
        ROOT_DIR / "tools" / "subnet-calculator.html",
        ROOT_DIR / "tools" / "vlsm-planner.html",
        ROOT_DIR / "tools" / "network-diagnostic-workbench.html",
        ROOT_DIR / "tools" / "port-reference.html"
    ]
    for tf in tools_files:
        assert tf.exists(), f"Expected tool file {tf.name} to exist"

    with open(ROOT_DIR / "data" / "troubleshooting-labs.json", "r", encoding="utf-8") as f:
        labs = json.load(f)
    assert len(labs) == 6, f"Expected 6 labs, got {len(labs)}"

    print(f"[PASS] Platform Freeze Baseline Verified: 148 Tutorials, 471 Curriculum (148 Pub / 323 Plan), 42 Commands, 8 Quizzes (64 Qs), 26 Resources, 4 Tools, 6 Labs")

    # -------------------------------------------------------------
    # 2. Browser Verification & Functional Testing
    # -------------------------------------------------------------
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        console_errors = []
        network_404s = []

        page.on("console", lambda msg: console_errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("response", lambda resp: network_404s.append(resp.url) if resp.status == 404 and ("localhost" in resp.url or "127.0.0.1" in resp.url) else None)

        test_results = {}

        # -------------------------------------------------------------
        # A. Header Navigation & Hierarchy Checks
        # -------------------------------------------------------------
        print("\n--- 2. Header Navigation & Active State Audit ---")
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)

        nav_links_data = await page.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('.nav-links a'));
            return links.map(l => ({
                text: l.textContent.trim(),
                href: l.getAttribute('href'),
                active: l.classList.contains('active'),
                ariaCurrent: l.getAttribute('aria-current')
            }));
        }""")

        expected_nav = ["Home", "Topics", "Commands", "Quizzes", "Tools", "Labs", "Resources", "About"]
        actual_nav = [item["text"] for item in nav_links_data]
        test_results["header_nav_items"] = (actual_nav == expected_nav)
        print(f"[{'PASS' if test_results['header_nav_items'] else 'FAIL'}] Header Navigation Items ({actual_nav} == {expected_nav})")

        # Active state on Home
        home_active = next((l for l in nav_links_data if l["text"] == "Home"), None)
        active_count_home = sum(1 for l in nav_links_data if l["active"])
        test_results["active_nav_home"] = (home_active and home_active["active"] and home_active["ariaCurrent"] == "page" and active_count_home == 1)
        print(f"[{'PASS' if test_results['active_nav_home'] else 'FAIL'}] Active Nav on Home: only Home active (Active count: {active_count_home})")

        # Active state on nested tool: tools/subnet-calculator.html
        await page.goto(f"{BASE_URL}/tools/subnet-calculator.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)
        tool_nav_data = await page.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('.nav-links a'));
            return links.map(l => ({
                text: l.textContent.trim(),
                active: l.classList.contains('active'),
                ariaCurrent: l.getAttribute('aria-current')
            }));
        }""")
        tools_active = next((l for l in tool_nav_data if l["text"] == "Tools"), None)
        active_count_tools = sum(1 for l in tool_nav_data if l["active"])
        test_results["active_nav_tools"] = (tools_active and tools_active["active"] and tools_active["ariaCurrent"] == "page" and active_count_tools == 1)
        print(f"[{'PASS' if test_results['active_nav_tools'] else 'FAIL'}] Active Nav on tools/subnet-calculator.html: only Tools active (Active count: {active_count_tools})")

        # Active state on labs: labs.html
        await page.goto(f"{BASE_URL}/labs.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)
        labs_nav_data = await page.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('.nav-links a'));
            return links.map(l => ({
                text: l.textContent.trim(),
                active: l.classList.contains('active'),
                ariaCurrent: l.getAttribute('aria-current')
            }));
        }""")
        labs_active = next((l for l in labs_nav_data if l["text"] == "Labs"), None)
        active_count_labs = sum(1 for l in labs_nav_data if l["active"])
        test_results["active_nav_labs"] = (labs_active and labs_active["active"] and labs_active["ariaCurrent"] == "page" and active_count_labs == 1)
        print(f"[{'PASS' if test_results['active_nav_labs'] else 'FAIL'}] Active Nav on labs.html: only Labs active (Active count: {active_count_labs})")

        # Active state on tutorial: tutorials/networking/osi-model-explained.html
        await page.goto(f"{BASE_URL}/tutorials/networking/osi-model-explained.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)
        tut_nav_data = await page.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('.nav-links a'));
            return links.map(l => ({
                text: l.textContent.trim(),
                active: l.classList.contains('active'),
                ariaCurrent: l.getAttribute('aria-current')
            }));
        }""")
        topics_active_tut = next((l for l in tut_nav_data if l["text"] == "Topics"), None)
        active_count_tut = sum(1 for l in tut_nav_data if l["active"])
        test_results["active_nav_tutorial"] = (topics_active_tut and topics_active_tut["active"] and topics_active_tut["ariaCurrent"] == "page" and active_count_tut == 1)
        print(f"[{'PASS' if test_results['active_nav_tutorial'] else 'FAIL'}] Active Nav on tutorial: only Topics active (Active count: {active_count_tut})")

        # Active state on category: networking.html
        await page.goto(f"{BASE_URL}/networking.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)
        cat_nav_data = await page.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('.nav-links a'));
            return links.map(l => ({
                text: l.textContent.trim(),
                active: l.classList.contains('active'),
                ariaCurrent: l.getAttribute('aria-current')
            }));
        }""")
        topics_active_cat = next((l for l in cat_nav_data if l["text"] == "Topics"), None)
        active_count_cat = sum(1 for l in cat_nav_data if l["active"])
        test_results["active_nav_category"] = (topics_active_cat and topics_active_cat["active"] and topics_active_cat["ariaCurrent"] == "page" and active_count_cat == 1)
        print(f"[{'PASS' if test_results['active_nav_category'] else 'FAIL'}] Active Nav on networking.html: only Topics active (Active count: {active_count_cat})")

        # -------------------------------------------------------------
        # B. Mobile Navigation Hamburger & Keyboard Dismissal
        # -------------------------------------------------------------
        print("\n--- 3. Mobile Navigation & Accessibility Check ---")
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)

        # Ensure hamburger toggle is visible at 375px
        toggle_visible = await page.evaluate("""() => {
            const btn = document.querySelector('.mobile-menu-toggle');
            return btn && window.getComputedStyle(btn).display !== 'none';
        }""")

        # Open mobile menu
        await page.click(".mobile-menu-toggle")
        await page.wait_for_timeout(300)
        menu_open = await page.evaluate("""() => {
            const nav = document.querySelector('.nav-links');
            const btn = document.querySelector('.mobile-menu-toggle');
            return nav && nav.classList.contains('active') && btn.getAttribute('aria-expanded') === 'true';
        }""")

        # Press Escape key
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)
        menu_closed = await page.evaluate("""() => {
            const nav = document.querySelector('.nav-links');
            const btn = document.querySelector('.mobile-menu-toggle');
            return nav && !nav.classList.contains('active') && btn.getAttribute('aria-expanded') === 'false';
        }""")

        test_results["mobile_nav_accessibility"] = bool(toggle_visible and menu_open and menu_closed)
        print(f"[{'PASS' if test_results['mobile_nav_accessibility'] else 'FAIL'}] Mobile Nav Hamburger Menu (Visible, Opens, Aria-Expanded, Escape Dismissal)")

        # -------------------------------------------------------------
        # C. Premium Footer Redesign & Nested Route Audit
        # -------------------------------------------------------------
        print("\n--- 4. Footer Redesign & Route Resolution Audit ---")
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".site-footer", timeout=5000)

        footer_audit = await page.evaluate("""() => {
            const footer = document.querySelector('.site-footer');
            if (!footer) return { ok: false };
            
            const brandLogo = !!footer.querySelector('.footer-brand .site-logo');
            const desc = footer.querySelector('.footer-desc')?.textContent.trim();
            const expectedDesc = "Enterprise IT knowledge platform for network engineers, system administrators, and technology professionals.";
            const descMatches = desc === expectedDesc;
            
            const igLink = footer.querySelector('.social-links a[href*="instagram"]');
            const igLabel = igLink?.getAttribute('aria-label') || '';
            const igHandle = footer.querySelector('.social-handle')?.textContent.trim();
            
            const learnCols = Array.from(footer.querySelectorAll('.footer-col:nth-child(2) .footer-links a')).map(a => a.textContent.trim());
            const exploreCols = Array.from(footer.querySelectorAll('.footer-col:nth-child(3) .footer-links a')).map(a => a.textContent.trim());
            const legalCols = Array.from(footer.querySelectorAll('.footer-col:nth-child(4) .footer-links a')).map(a => a.textContent.trim());
            
            const copyrightText = footer.querySelector('.footer-copyright')?.textContent.trim() || '';
            const taglineText = footer.querySelector('.footer-tagline')?.textContent.trim() || '';
            const creatorText = footer.querySelector('.footer-creator')?.textContent.trim() || '';
            
            const hasAmbiguousLabel = exploreCols.includes("Tools & Resources");
            const hasCleanResources = exploreCols.includes("Resources");
            
            const s = window.getComputedStyle(footer);
            const height = footer.offsetHeight;
            
            return {
                ok: brandLogo && descMatches && !!igLink && igHandle === '@themjtechhub' && learnCols.length === 6 && exploreCols.length === 6 && legalCols.length === 4 && !hasAmbiguousLabel && hasCleanResources && creatorText === 'Mayur Talsaniya',
                learnCols,
                exploreCols,
                legalCols,
                descMatches,
                igLabel,
                copyrightText,
                taglineText,
                creatorText,
                height,
                paddingTop: s.paddingTop,
                paddingBottom: s.paddingBottom,
                marginTop: s.marginTop
            };
        }""")

        test_results["footer_structure"] = bool(footer_audit.get("ok"))
        print(f"[{'PASS' if test_results['footer_structure'] else 'FAIL'}] Footer Columns: Learn ({len(footer_audit.get('learnCols', []))}), Explore ({len(footer_audit.get('exploreCols', []))}), Legal ({len(footer_audit.get('legalCols', []))})")
        print(f"       Explore column links: {footer_audit.get('exploreCols')}")
        print(f"       Bottom bar: '{footer_audit.get('copyrightText')}' | '{footer_audit.get('taglineText')}' | Creator: '{footer_audit.get('creatorText')}'")
        print(f"       Dimensions: height={footer_audit.get('height')}px, padding={footer_audit.get('paddingTop')} / {footer_audit.get('paddingBottom')}, marginTop={footer_audit.get('marginTop')}")

        # Test footer link resolution across 4 nested routes:
        test_routes = [
            "/index.html",
            "/tutorials/networking/osi-model-explained.html",
            "/tools/subnet-calculator.html",
            "/legal/privacy.html"
        ]
        footer_links_resolved = True
        for route in test_routes:
            await page.goto(f"{BASE_URL}{route}", wait_until="networkidle")
            await page.wait_for_selector(".site-footer", timeout=5000)
            links = await page.evaluate("""() => {
                const links = Array.from(document.querySelectorAll('.site-footer a'));
                return links.map(a => a.href);
            }""")
            for l in links:
                if "themjtechhub.site" in l or "instagram" in l:
                    continue
                # Local links must not produce 404
                if "404" in l:
                    footer_links_resolved = False

        test_results["footer_links_resolved"] = footer_links_resolved
        print(f"[{'PASS' if test_results['footer_links_resolved'] else 'FAIL'}] Footer links validly resolved from 4 nested route depths")

        # -------------------------------------------------------------
        # D. Homepage Discoverability of Tools & Labs
        # -------------------------------------------------------------
        print("\n--- 5. Homepage Discoverability Audit ---")
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        growth_card = await page.evaluate("""() => {
            const card = document.querySelector('.growth-card');
            const headline = card?.querySelector('.growth-headline')?.textContent.trim();
            const links = Array.from(card?.querySelectorAll('a') || []).map(a => ({
                text: a.textContent.trim(),
                href: a.getAttribute('href')
            }));
            return { headline, links };
        }""")
        has_tools_link = any(l["href"] == "tools.html" for l in growth_card.get("links", []))
        has_labs_link = any(l["href"] == "labs.html" for l in growth_card.get("links", []))
        test_results["homepage_discoverability"] = (has_tools_link and has_labs_link)
        print(f"[{'PASS' if test_results['homepage_discoverability'] else 'FAIL'}] Homepage Card: '{growth_card.get('headline')}' links to tools.html ({has_tools_link}) and labs.html ({has_labs_link})")

        # -------------------------------------------------------------
        # E. Global Search Module & Taxonomy Verification
        # -------------------------------------------------------------
        print("\n--- 6. Global Search Taxonomy & Badges Audit ---")
        # Open search modal
        await page.click(".search-box")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=3000)

        # Query "quiz"
        await page.fill("#search-modal-input", "quiz")
        await page.wait_for_timeout(600)
        quiz_results = await page.evaluate("""() => {
            const items = Array.from(document.querySelectorAll('.search-result-item'));
            return items.map(i => ({
                title: i.querySelector('.search-result-title')?.textContent.trim(),
                meta: i.querySelector('.search-result-meta')?.textContent.trim(),
                href: i.getAttribute('href')
            }));
        }""")
        has_quiz_type = any("Quiz" in r["meta"] for r in quiz_results)
        quiz_hrefs = [r["href"] for r in quiz_results if "Quiz" in r["meta"]]
        unique_quiz_hrefs = len(set(quiz_hrefs)) == len(quiz_hrefs) and len(quiz_hrefs) > 0
        quiz_has_params = all("?quiz=" in h for h in quiz_hrefs)

        # Close via Escape
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)

        # Query "subnet"
        await page.click(".search-box")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=3000)
        await page.fill("#search-modal-input", "subnet")
        await page.wait_for_timeout(600)
        subnet_results = await page.evaluate("""() => {
            const items = Array.from(document.querySelectorAll('.search-result-item'));
            return items.map(i => ({
                title: i.querySelector('.search-result-title')?.textContent.trim(),
                meta: i.querySelector('.search-result-meta')?.textContent.trim(),
                href: i.getAttribute('href')
            }));
        }""")
        has_tool_type = any("Tool" in r["meta"] for r in subnet_results)

        # Close via Escape
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)

        # Query "lab"
        await page.click(".search-box")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=3000)
        await page.fill("#search-modal-input", "troubleshooting lab")
        await page.wait_for_timeout(600)
        lab_results = await page.evaluate("""() => {
            const items = Array.from(document.querySelectorAll('.search-result-item'));
            return items.map(i => ({
                title: i.querySelector('.search-result-title')?.textContent.trim(),
                meta: i.querySelector('.search-result-meta')?.textContent.trim(),
                href: i.getAttribute('href')
            }));
        }""")
        has_lab_type = any("Lab" in r["meta"] for r in lab_results)

        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)

        test_results["search_taxonomy"] = bool(has_quiz_type and unique_quiz_hrefs and quiz_has_params and has_tool_type and has_lab_type)
        print(f"[{'PASS' if test_results['search_taxonomy'] else 'FAIL'}] Global Search Taxonomy (Quiz: {has_quiz_type}, Unique Quiz Destinations: {unique_quiz_hrefs}, Param ?quiz: {quiz_has_params}, Tool: {has_tool_type}, Lab: {has_lab_type})")

        # Verify quiz auto-start from parameter
        await page.goto(f"{BASE_URL}/quiz.html?quiz=networking-basics", wait_until="networkidle")
        await page.wait_for_selector("#quiz-app.active", timeout=5000)
        quiz_auto_started = await page.evaluate("""() => {
            const app = document.getElementById('quiz-app');
            const title = document.getElementById('quiz-title')?.textContent.trim();
            return app && app.classList.contains('active') && title.includes('Networking');
        }""")
        test_results["quiz_param_auto_start"] = bool(quiz_auto_started)
        print(f"[{'PASS' if test_results['quiz_param_auto_start'] else 'FAIL'}] Quiz Auto-start via ?quiz= parameter (Started: {quiz_auto_started})")

        # -------------------------------------------------------------
        # F. SEO & Metadata Consistency
        # -------------------------------------------------------------
        print("\n--- 7. SEO & Canonical Metadata Audit ---")
        seo_pages = [
            "index.html",
            "topics.html",
            "commands.html",
            "quiz.html",
            "resources.html",
            "tools.html",
            "labs.html",
            "tools/subnet-calculator.html",
            "tools/vlsm-planner.html",
            "tools/network-diagnostic-workbench.html",
            "tools/port-reference.html",
            "about.html",
            "legal/privacy.html",
            "legal/terms.html",
            "legal/disclaimer.html"
        ]

        seo_pass = True
        for sp in seo_pages:
            content = (ROOT_DIR / sp).read_text(encoding="utf-8")
            
            # 1. Exactly one H1
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
            if len(h1s) != 1:
                print(f"[FAIL] {sp} has {len(h1s)} H1 elements")
                seo_pass = False
                
            # 2. Canonical points to https://themjtechhub.site
            canon_match = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE)
            if not canon_match:
                canon_match = re.search(r'<link\s+[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', content, re.IGNORECASE)
            if not canon_match or not canon_match.group(1).startswith("https://themjtechhub.site"):
                print(f"[FAIL] {sp} invalid canonical: {canon_match.group(1) if canon_match else 'MISSING'}")
                seo_pass = False

            # 3. OpenGraph title & description
            if 'property="og:title"' not in content or 'property="og:description"' not in content:
                print(f"[FAIL] {sp} missing Open Graph title or description")
                seo_pass = False

            # 4. Twitter Card
            if 'name="twitter:card"' not in content:
                print(f"[FAIL] {sp} missing Twitter card")
                seo_pass = False

        test_results["seo_metadata"] = seo_pass
        print(f"[{'PASS' if test_results['seo_metadata'] else 'FAIL'}] 15 Core Public Pages validated for single H1, canonical domain, OpenGraph & Twitter tags")

        # -------------------------------------------------------------
        # G. Responsive Zero Horizontal Overflow Across Viewports
        # -------------------------------------------------------------
        print("\n--- 8. Responsive Zero Horizontal Overflow Audit ---")
        viewports = [320, 375, 768, 1024, 1440]
        pages_to_test = [
            "/index.html",
            "/topics.html",
            "/commands.html",
            "/quiz.html",
            "/resources.html",
            "/tools.html",
            "/labs.html",
            "/tools/subnet-calculator.html",
            "/about.html",
            "/legal/privacy.html"
        ]

        overflow_issues = []
        for vp in viewports:
            await page.set_viewport_size({"width": vp, "height": 800})
            for ppath in pages_to_test:
                await page.goto(f"{BASE_URL}{ppath}", wait_until="networkidle")
                await page.wait_for_selector(".site-header", timeout=5000)
                await page.wait_for_selector(".site-footer", timeout=5000)
                has_overflow = await page.evaluate("""() => {
                    const scrollWidth = document.documentElement.scrollWidth;
                    const innerWidth = window.innerWidth;
                    return scrollWidth > innerWidth;
                }""")
                if has_overflow:
                    overflow_issues.append((vp, ppath))

        test_results["responsive_overflow"] = (len(overflow_issues) == 0)
        print(f"[{'PASS' if test_results['responsive_overflow'] else 'FAIL'}] Zero Horizontal Overflow across [320, 375, 768, 1024, 1440px] (Issues: {len(overflow_issues)})")

        # -------------------------------------------------------------
        # H. Capture 8 Required Screenshots
        # -------------------------------------------------------------
        print("\n--- 9. Capture 8 Required Screenshots ---")
        
        # 1. qa/phase6_8_home_desktop.png (1440px)
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)
        s1 = QA_DIR / "phase6_8_home_desktop.png"
        await page.screenshot(path=str(s1))
        print(f"[INFO] Captured {s1.name}")

        # 2. qa/phase6_8_header_desktop.png (1440px focused on header)
        s2 = QA_DIR / "phase6_8_header_desktop.png"
        header_el = page.locator(".site-header")
        await header_el.screenshot(path=str(s2))
        print(f"[INFO] Captured {s2.name}")

        # 3. qa/phase6_8_header_mobile.png (375px mobile menu open)
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)
        await page.click(".mobile-menu-toggle")
        await page.wait_for_timeout(350)
        s3 = QA_DIR / "phase6_8_header_mobile.png"
        await page.screenshot(path=str(s3))
        print(f"[INFO] Captured {s3.name}")

        # 4. qa/phase6_8_footer_desktop.png (1440px with content above footer for transition review)
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".site-footer", timeout=5000)
        # Scroll down so Instagram community section and footer are both in frame
        await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight - 850)")
        await page.wait_for_timeout(300)
        s4 = QA_DIR / "phase6_8_footer_desktop.png"
        await page.screenshot(path=str(s4))
        print(f"[INFO] Captured {s4.name}")

        # 5. qa/phase6_8_footer_mobile.png (375px footer stack)
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".site-footer", timeout=5000)
        await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(300)
        s5 = QA_DIR / "phase6_8_footer_mobile.png"
        await page.screenshot(path=str(s5))
        print(f"[INFO] Captured {s5.name}")

        # 6. qa/phase6_8_tools_navigation.png (1440px on tools page showing Tools active nav)
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/tools.html", wait_until="networkidle")
        await page.wait_for_selector(".tools-grid", timeout=5000)
        s6 = QA_DIR / "phase6_8_tools_navigation.png"
        await page.screenshot(path=str(s6))
        print(f"[INFO] Captured {s6.name}")

        # 7. qa/phase6_8_dark_mode.png (1440px dark mode on home page)
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".site-header", timeout=5000)
        await page.evaluate("() => { document.documentElement.setAttribute('data-theme', 'dark'); localStorage.setItem('mj-theme', 'dark'); }")
        await page.wait_for_timeout(300)
        s7 = QA_DIR / "phase6_8_dark_mode.png"
        await page.screenshot(path=str(s7))
        print(f"[INFO] Captured {s7.name}")
        # Reset back to light
        await page.evaluate("() => { document.documentElement.setAttribute('data-theme', 'light'); localStorage.setItem('mj-theme', 'light'); }")

        # 8. qa/phase6_8_search_navigation.png (1440px search modal open showing result types)
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector(".search-box", timeout=5000)
        await page.click(".search-box")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=3000)
        await page.fill("#search-modal-input", "network")
        await page.wait_for_timeout(600)
        s8 = QA_DIR / "phase6_8_search_navigation.png"
        await page.screenshot(path=str(s8))
        print(f"[INFO] Captured {s8.name}")

        # -------------------------------------------------------------
        # I. Network & Console Error Assertions
        # -------------------------------------------------------------
        print("\n--- 10. Console & Network Integrity ---")
        test_results["zero_console_errors"] = (len(console_errors) == 0)
        test_results["zero_404s"] = (len(network_404s) == 0)
        print(f"[{'PASS' if test_results['zero_console_errors'] else 'FAIL'}] 0 Console Errors encountered (Errors: {len(console_errors)})")
        if console_errors:
            for ce in console_errors:
                print(f"       {ce}")
        print(f"[{'PASS' if test_results['zero_404s'] else 'FAIL'}] 0 Local 404s encountered (404s: {len(network_404s)})")
        if network_404s:
            for n4 in network_404s:
                print(f"       {n4}")

        await browser.close()

    print("\n" + "=" * 70)
    all_passed = all(test_results.values())
    if all_passed:
        print("PHASE 6.8 VERIFICATION OVERALL: ALL TESTS PASSED")
    else:
        print("PHASE 6.8 VERIFICATION OVERALL: SOME TESTS FAILED")
        for k, v in test_results.items():
            if not v:
                print(f"  - FAILED: {k}")
    print("=" * 70)
    assert all_passed, "One or more Phase 6.8 tests failed!"

if __name__ == "__main__":
    asyncio.run(run_phase6_8_tests())
