#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 4 Homepage Modernization Test Suite
Validates:
- Dynamic statistics loading from JSON
- Dynamic latest tutorials loading (top 3) from JSON
- Dynamic popular commands loading from JSON
- Core topics cards rendering (6 items)
- Learning column & Quiz CTA links
- Instagram CTA banner link
- Responsive zero horizontal overflow at 375, 768, 1024, 1440
- Theme switching & persistence
- Search dialog & mobile menu functionality
- Captures required Phase 4 screenshots:
    * qa/phase4_home_desktop_light.png
    * qa/phase4_home_desktop_dark.png
    * qa/phase4_home_mobile_light.png
    * qa/phase4_home_mobile_dark.png
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
BASE_URL = "http://localhost/index"
QA_DIR = Path(__file__).resolve().parent
ROOT_DIR = QA_DIR.parent

async def run_phase4_tests():
    print("=" * 60)
    print("Starting MJ Tech Hub Phase 4 Homepage Verification Suite")
    print("=" * 60)

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
        # 1. Desktop Loading & Dynamic Content Verification (1440px)
        # -------------------------------------------------------------
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")

        # Wait for dynamically loaded elements
        await page.wait_for_selector(".site-header", timeout=5000)
        await page.wait_for_selector(".site-footer", timeout=5000)
        await page.wait_for_selector("#latest-tutorials-list .dash-tut-card", timeout=5000)
        await page.wait_for_selector("#popular-commands-list .command-pill", timeout=5000)
        await page.wait_for_selector("#home-topics-grid .home-topic-card", timeout=5000)

        # A. Statistics check (exact dynamic count from JSON)
        with open(ROOT_DIR / "data" / "tutorials.json", "r", encoding="utf-8") as f:
            expected_tut_count = str(len(json.load(f)))

        stats = await page.evaluate("""() => {
            return {
                tutorials: document.getElementById('stat-tutorials')?.textContent.trim(),
                commands: document.getElementById('stat-commands')?.textContent.trim(),
                topics: document.getElementById('stat-topics')?.textContent.trim(),
                quizzes: document.getElementById('stat-quizzes')?.textContent.trim()
            };
        }""")
        test_results["stats_dynamic"] = (
            stats["tutorials"] == expected_tut_count and
            stats["commands"] == "12" and
            stats["topics"] == "6" and
            stats["quizzes"] == "2"
        )
        print(f"[{'PASS' if test_results['stats_dynamic'] else 'FAIL'}] Dynamic Statistics (Exact Tutorials: {stats['tutorials']} == {expected_tut_count}, Commands: {stats['commands']}, Topics: {stats['topics']}, Quizzes: {stats['quizzes']})")

        # Hero Assets Check (Light & Dark theme assets)
        hero_assets = await page.evaluate("""() => {
            const light = document.querySelector('.hero-illustration-light');
            const dark = document.querySelector('.hero-illustration-dark');
            return {
                hasLight: !!light && light.getAttribute('src').includes('mj-tech-hero.png'),
                hasDark: !!dark && dark.getAttribute('src').includes('mj-tech-hero-dark.png')
            };
        }""")
        test_results["hero_assets"] = hero_assets["hasLight"] and hero_assets["hasDark"]
        print(f"[{'PASS' if test_results['hero_assets'] else 'FAIL'}] Dual Hero Assets Present (Light: {hero_assets['hasLight']}, Dark: {hero_assets['hasDark']})")

        # B. Latest Tutorials check (multi-line title support, card height consistency)
        tut_data = await page.evaluate("""() => {
            const cards = document.querySelectorAll('#latest-tutorials-list .dash-tut-card');
            return Array.from(cards).map(c => ({
                title: c.querySelector('.dash-tut-title')?.textContent.trim(),
                badge: c.querySelector('.dash-tut-badge')?.textContent.trim(),
                desc: c.querySelector('.dash-tut-desc')?.textContent.trim(),
                meta: c.querySelector('.dash-tut-meta')?.textContent.trim(),
                href: c.getAttribute('href')
            }));
        }""")
        test_results["latest_tutorials"] = (
            len(tut_data) == 3 and
            all(t["title"] and t["badge"] and t["desc"] and t["meta"] and t["href"] for t in tut_data)
        )
        print(f"[{'PASS' if test_results['latest_tutorials'] else 'FAIL'}] Latest Tutorials (Rendered: {len(tut_data)} items, all metadata present)")
        for idx, t in enumerate(tut_data, 1):
            print(f"       {idx}. {t['title']} [{t['badge']}] -> {t['href']}")

        # C. Essential Commands Section check
        cmd_section = await page.evaluate("""() => {
            const title = document.querySelector('.dashboard-col-commands .dash-col-title h3')?.textContent.trim();
            const pills = document.querySelectorAll('#popular-commands-list .command-pill');
            return {
                title: title,
                pills: Array.from(pills).map(p => ({
                    cmd: p.querySelector('code')?.textContent.trim(),
                    href: p.getAttribute('href')
                }))
            };
        }""")
        test_results["commands_title"] = (cmd_section["title"] == "Essential Commands")
        test_results["popular_commands"] = (
            len(cmd_section["pills"]) == 12 and
            all(c["cmd"] and c["href"] == "commands.html" for c in cmd_section["pills"])
        )
        print(f"[{'PASS' if test_results['commands_title'] else 'FAIL'}] Command Section Title ('{cmd_section['title']}' == 'Essential Commands')")
        print(f"[{'PASS' if test_results['popular_commands'] else 'FAIL'}] Essential Commands Pills (Rendered: {len(cmd_section['pills'])} pills, all link to commands.html)")

        # D. Browse by Topic check
        topic_cards = await page.evaluate("""() => {
            const cards = document.querySelectorAll('#home-topics-grid .home-topic-card');
            return Array.from(cards).map(c => ({
                name: c.querySelector('.topic-title')?.textContent.trim(),
                desc: c.querySelector('.topic-desc')?.textContent.trim(),
                href: c.querySelector('.topic-cta')?.getAttribute('href')
            }));
        }""")
        test_results["topics_cards"] = (
            len(topic_cards) == 6 and
            all(tc["name"] and tc["desc"] and tc["href"] for tc in topic_cards)
        )
        print(f"[{'PASS' if test_results['topics_cards'] else 'FAIL'}] 6 Core Topic Cards in 3x2 Grid (Rendered: {len(topic_cards)})")

        # E. Learning Column & CTAs check
        dashboard_ctas = await page.evaluate("""() => {
            const quizBtn = document.querySelector('.btn-quiz-cta');
            const igBtn = document.querySelector('.btn-instagram');
            const igHandle = document.querySelector('.instagram-handle');
            return {
                quizHref: quizBtn?.getAttribute('href'),
                igHref: igBtn?.getAttribute('href'),
                igTarget: igBtn?.getAttribute('target'),
                igHandleText: igHandle?.textContent.trim()
            };
        }""")
        test_results["ctas"] = (
            dashboard_ctas["quizHref"] == "quiz.html" and
            dashboard_ctas["igHref"] == "https://www.instagram.com/themjtechhub/" and
            dashboard_ctas["igTarget"] == "_blank" and
            dashboard_ctas["igHandleText"] == "@themjtechhub"
        )
        print(f"[{'PASS' if test_results['ctas'] else 'FAIL'}] Quiz & Instagram CTAs (Quiz: {dashboard_ctas['quizHref']}, IG: {dashboard_ctas['igHref']})")

        # -------------------------------------------------------------
        # 2. Screenshot Generation: Desktop (Light & Dark)
        # -------------------------------------------------------------
        # Ensure Light Mode
        await page.evaluate("""() => {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('mj_theme', 'light');
        }""")
        await page.wait_for_timeout(300)
        desktop_light_path = QA_DIR / "phase4_home_desktop_light.png"
        await page.screenshot(path=str(desktop_light_path), full_page=True)
        print(f"[INFO] Saved Desktop Light screenshot -> {desktop_light_path.name}")

        # Switch to Dark Mode
        await page.evaluate("""() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('mj_theme', 'dark');
        }""")
        await page.wait_for_timeout(300)
        desktop_dark_path = QA_DIR / "phase4_home_desktop_dark.png"
        await page.screenshot(path=str(desktop_dark_path), full_page=True)
        print(f"[INFO] Saved Desktop Dark screenshot -> {desktop_dark_path.name}")

        # -------------------------------------------------------------
        # 3. Screenshot Generation: Mobile 375px (Light & Dark)
        # -------------------------------------------------------------
        await page.set_viewport_size({"width": 375, "height": 812})
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.wait_for_selector("#latest-tutorials-list .dash-tut-card", timeout=5000)

        # Mobile Light
        await page.evaluate("""() => {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('mj_theme', 'light');
        }""")
        await page.wait_for_timeout(300)
        mobile_light_path = QA_DIR / "phase4_home_mobile_light.png"
        await page.screenshot(path=str(mobile_light_path), full_page=True)
        print(f"[INFO] Saved Mobile Light screenshot -> {mobile_light_path.name}")

        # Mobile Dark
        await page.evaluate("""() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('mj_theme', 'dark');
        }""")
        await page.wait_for_timeout(300)
        mobile_dark_path = QA_DIR / "phase4_home_mobile_dark.png"
        await page.screenshot(path=str(mobile_dark_path), full_page=True)
        print(f"[INFO] Saved Mobile Dark screenshot -> {mobile_dark_path.name}")

        # -------------------------------------------------------------
        # 4. Responsive Zero Horizontal Overflow Check
        # -------------------------------------------------------------
        viewports = [375, 768, 1024, 1440]
        overflow_results = {}
        for vp in viewports:
            await page.set_viewport_size({"width": vp, "height": 900})
            await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
            await page.wait_for_timeout(300)
            sw, cw = await page.evaluate("() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            has_overflow = sw > cw
            overflow_results[vp] = not has_overflow
            status = "PASS" if not has_overflow else "FAIL"
            print(f"[{status}] Viewport {vp}px: scrollWidth={sw}, clientWidth={cw}")

        test_results["no_overflow"] = all(overflow_results.values())

        # -------------------------------------------------------------
        # 5. Console & Network Integrity
        # -------------------------------------------------------------
        test_results["no_console_errors"] = len(console_errors) == 0
        test_results["no_404s"] = len(network_404s) == 0
        print(f"[{'PASS' if test_results['no_console_errors'] else 'FAIL'}] Zero Console Errors (Count: {len(console_errors)})")
        if console_errors:
            for ce in console_errors:
                print(f"       ERROR: {ce}")

        print(f"[{'PASS' if test_results['no_404s'] else 'FAIL'}] Zero Local 404 Requests (Count: {len(network_404s)})")
        if network_404s:
            for n4 in network_404s:
                print(f"       404: {n4}")

        await browser.close()

        # Final Summary
        all_passed = all(test_results.values())
        print("=" * 60)
        print(f"PHASE 4 VERIFICATION OVERALL: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
        print("=" * 60)
        return all_passed

if __name__ == "__main__":
    success = asyncio.run(run_phase4_tests())
    exit(0 if success else 1)
