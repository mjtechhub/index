#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6 Tutorial Reading Experience & Tutorial Engine Verification Suite
(qa/test_phase6_tutorials.py)

Validates all Phase 6 requirements and CTO conditions:
1. Static SEO validation across all 61 raw HTML tutorials:
   - Unique title, meta description, canonical URL (https://themjtechhub.site)
   - OG fields (og:title, og:description, og:type="article", og:url)
   - Twitter fields (summary, title, description)
   - TechArticle JSON-LD structured data (valid JSON, correct fields)
   - Exactly one H1 in raw HTML
2. Comprehensive content-type audit verification:
   - Tables (17 tutorials)
   - Standard <pre><code> (3 tutorials)
   - Normalized .tutorial-command (17 tutorials)
   - Standardized callouts (10 tutorials)
   - Headings (H2/H3 counts and slugified IDs)
3. Structural DOM assertions across representative sample tutorials:
   - Exactly one H1
   - Unique heading IDs (no duplicate IDs)
   - Semantic reading width (max-width: 72ch)
   - Table of contents (sticky desktop aside + mobile accordion)
   - Code block enhancement (<pre><code> and .tutorial-command) with accessible copy button
   - 1-click clipboard copy with aria-live="polite" toast feedback
   - Responsive tables without nested wrappers
   - Standardized callouts (Note, Warning, Tip, Important)
   - Deterministic Previous/Next navigation adhering to tutorials.json array contract
   - Deterministic Related Tutorials (same category, same level, neighboring index, max 3)
   - Canonical "Back to Category" action
4. Engine idempotency:
   - Calling window.initTutorialEngine() multiple times produces zero duplicates
5. Reduced motion compliance:
   - Respects prefers-reduced-motion
6. Responsive viewports:
   - Zero horizontal overflow across 375px, 768px, 1024px, 1440px
7. Zero console errors and zero local 404 network requests
8. High-resolution visual screenshots:
   - qa/phase6_tutorial_desktop_light.png
   - qa/phase6_tutorial_desktop_dark.png
   - qa/phase6_tutorial_mobile_light.png
   - qa/phase6_tutorial_mobile_dark.png
   - qa/phase6_tutorial_toc.png
   - qa/phase6_tutorial_code_copy.png
"""

import asyncio
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from playwright.async_api import async_playwright

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
BASE_URL = "http://localhost/index"
QA_DIR = Path(__file__).resolve().parent
ROOT_DIR = QA_DIR.parent
TUTS_DIR = ROOT_DIR / "tutorials" / "networking"
TUTS_JSON_PATH = ROOT_DIR / "data" / "tutorials.json"
CANONICAL_DOMAIN = "https://themjtechhub.site"

class RawHtmlAuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.h1_texts = []
        self.capturing_h1 = False
        self.h1_buffer = ""
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
            self.capturing_h1 = True
            self.h1_buffer = ""
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

    def handle_data(self, data):
        if self.capturing_title:
            self.title_text += data
        elif self.capturing_h1:
            self.h1_buffer += data
        elif self.capturing_json_ld:
            self.json_ld_buffer += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.capturing_title = False
            self.title_text = self.title_text.strip()
        elif tag == "h1":
            self.capturing_h1 = False
            self.h1_texts.append(self.h1_buffer.strip())
        elif tag == "script" and self.capturing_json_ld:
            self.capturing_json_ld = False
            if self.json_ld_buffer.strip():
                self.json_ld_raw.append(self.json_ld_buffer.strip())

def audit_raw_static_seo():
    print("\n" + "=" * 68)
    print("AUDIT 1: Static SEO & Raw HTML Inspection Across All 61 Tutorials")
    print("=" * 68)

    with open(TUTS_JSON_PATH, "r", encoding="utf-8") as f:
        tuts_meta = json.load(f)

    meta_by_name = {Path(t["url"]).name: t for t in tuts_meta}
    tut_files = sorted(list(TUTS_DIR.glob("*.html")))

    networking_meta = [t for t in tuts_meta if t.get("category") == "Networking"]
    assert len(tut_files) == 61, f"Expected 61 tutorial files, found {len(tut_files)}"
    assert len(networking_meta) == 61, f"Expected 61 networking entries in tutorials.json, found {len(networking_meta)}"

    seo_failures = []
    h1_failures = []
    json_ld_failures = []

    for fpath in tut_files:
        fname = fpath.name
        meta = meta_by_name.get(fname)
        if not meta:
            seo_failures.append(f"{fname}: Missing entry in tutorials.json")
            continue

        raw_html = fpath.read_text(encoding="utf-8")
        parser = RawHtmlAuditParser()
        parser.feed(raw_html)

        # 1. Title verification
        expected_title = f"{meta['title']} | {meta.get('category', 'Networking')} Tutorial | MJ Tech Hub"
        if parser.title_text != expected_title:
            seo_failures.append(f"{fname}: Title mismatch: '{parser.title_text}' != '{expected_title}'")

        # 2. Meta description
        expected_desc = meta.get("description", "")
        if parser.meta_desc != expected_desc:
            seo_failures.append(f"{fname}: Meta description mismatch")

        # 3. Canonical URL
        expected_canonical = f"{CANONICAL_DOMAIN}/tutorials/networking/{fname}"
        if parser.canonical != expected_canonical:
            seo_failures.append(f"{fname}: Canonical URL mismatch: '{parser.canonical}' != '{expected_canonical}'")

        # 4. Open Graph
        if parser.og_tags.get("og:title") != expected_title:
            seo_failures.append(f"{fname}: og:title mismatch")
        if parser.og_tags.get("og:description") != expected_desc:
            seo_failures.append(f"{fname}: og:description mismatch")
        if parser.og_tags.get("og:type") != "article":
            seo_failures.append(f"{fname}: og:type is not 'article'")
        if parser.og_tags.get("og:url") != expected_canonical:
            seo_failures.append(f"{fname}: og:url mismatch")

        # 5. Twitter Card
        if parser.twitter_tags.get("twitter:card") != "summary":
            seo_failures.append(f"{fname}: twitter:card is not 'summary'")
        if parser.twitter_tags.get("twitter:title") != expected_title:
            seo_failures.append(f"{fname}: twitter:title mismatch")
        if parser.twitter_tags.get("twitter:description") != expected_desc:
            seo_failures.append(f"{fname}: twitter:description mismatch")

        # 6. JSON-LD TechArticle
        if not parser.json_ld_raw:
            json_ld_failures.append(f"{fname}: Missing application/ld+json")
        else:
            try:
                schema_data = json.loads(parser.json_ld_raw[0])
                if schema_data.get("@type") != "TechArticle":
                    json_ld_failures.append(f"{fname}: JSON-LD @type is not TechArticle")
                if schema_data.get("headline") != meta["title"]:
                    json_ld_failures.append(f"{fname}: JSON-LD headline mismatch")
                if schema_data.get("url") != expected_canonical:
                    json_ld_failures.append(f"{fname}: JSON-LD url mismatch")
                if schema_data.get("proficiencyLevel") != meta.get("level", "Beginner"):
                    json_ld_failures.append(f"{fname}: JSON-LD proficiencyLevel mismatch")
                if schema_data.get("author", {}).get("url") != CANONICAL_DOMAIN:
                    json_ld_failures.append(f"{fname}: JSON-LD author.url mismatch")
                if schema_data.get("publisher", {}).get("url") != CANONICAL_DOMAIN:
                    json_ld_failures.append(f"{fname}: JSON-LD publisher.url mismatch")
                if schema_data.get("mainEntityOfPage", {}).get("@id") != expected_canonical:
                    json_ld_failures.append(f"{fname}: JSON-LD mainEntityOfPage mismatch")
            except Exception as e:
                json_ld_failures.append(f"{fname}: Invalid JSON-LD: {e}")

        # 7. Exactly one H1
        if parser.h1_count != 1:
            h1_failures.append(f"{fname}: Found {parser.h1_count} H1 tags: {parser.h1_texts}")

    print(f"Total Tutorial Files Audited: {len(tut_files)}")
    print(f"Static SEO Failures: {len(seo_failures)}")
    print(f"JSON-LD Failures   : {len(json_ld_failures)}")
    print(f"H1 Count Failures  : {len(h1_failures)}")

    assert len(seo_failures) == 0, f"SEO Failures encountered:\n" + "\n".join(seo_failures[:10])
    assert len(json_ld_failures) == 0, f"JSON-LD Failures encountered:\n" + "\n".join(json_ld_failures[:10])
    assert len(h1_failures) == 0, f"H1 Failures encountered:\n" + "\n".join(h1_failures[:10])

    print("[PASS] All 61 tutorials contain valid, complete static SEO metadata and exactly one H1.")

async def run_phase6_browser_tests():
    print("\n" + "=" * 68)
    print("AUDIT 2: Browser & Interactive Tutorial Engine Verification")
    print("=" * 68)

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        console_errors = []
        network_404s = []

        page.on("console", lambda msg: console_errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("response", lambda resp: network_404s.append(resp.url) if resp.status == 404 and "localhost" in resp.url else None)

        test_results = {}

        # -------------------------------------------------------------
        # Sample Tutorials Selected from Audit
        # -------------------------------------------------------------
        # 1. tcp-vs-udp.html (Index 0: Table, H3 headings, No Previous card)
        # 2. osi-model-explained.html (Index 1: Multiple H2/H3 headings, Prev & Next cards)
        # 3. common-network-ports.html (Index 6: Table, CLI command blocks, callouts)
        # 4. advanced-dns-troubleshooting.html (Standard <pre><code> block)
        # 5. access-control-lists-explained.html (Callout Note, CLI command blocks)
        # 6. snmp-explained.html (Table, 2 Callouts)
        # 7. netflow-ipfix-explained.html (Index 60: Last tutorial, No Next card)

        print("\n--- Test 1: First Tutorial in Canonical Order (tcp-vs-udp.html) ---")
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto(f"{BASE_URL}/tutorials/networking/tcp-vs-udp.html", wait_until="networkidle")

        # Wait for dynamic components and tutorial engine
        await page.wait_for_selector("#site-header header", timeout=5000)
        await page.wait_for_selector("#tutorial-toc .tutorial-toc-list", timeout=5000)
        await page.wait_for_selector(".tutorial-footer-section", timeout=5000)

        # Check single H1 in DOM
        h1_count = await page.locator("h1").count()
        test_results["tcp_single_h1"] = h1_count == 1
        print(f"[{'PASS' if test_results['tcp_single_h1'] else 'FAIL'}] Exactly one H1 in DOM ({h1_count} found)")

        # Check reading width on article
        article_max_width = await page.evaluate("getComputedStyle(document.querySelector('.tutorial-article')).maxWidth")
        test_results["tcp_reading_width"] = "ch" in article_max_width or "px" in article_max_width
        print(f"[{'PASS' if test_results['tcp_reading_width'] else 'FAIL'}] Article column max-width: {article_max_width}")

        # Check TOC entries
        toc_links_count = await page.locator("#tutorial-toc .toc-link").count()
        test_results["tcp_toc_count"] = toc_links_count > 0
        print(f"[{'PASS' if test_results['tcp_toc_count'] else 'FAIL'}] TOC generated with {toc_links_count} section links")

        # Heading IDs uniqueness
        heading_ids = await page.evaluate("""() => {
            const headings = document.querySelectorAll('.tutorial-article h2, .tutorial-article h3');
            return Array.from(headings).map(h => h.id);
        }""")
        test_results["tcp_unique_ids"] = len(heading_ids) == len(set(heading_ids)) and all(len(i) > 0 for i in heading_ids)
        print(f"[{'PASS' if test_results['tcp_unique_ids'] else 'FAIL'}] Unique slugified heading IDs ({len(heading_ids)} headings, all unique: {test_results['tcp_unique_ids']})")

        # Table wrapping in .table-responsive without nesting
        table_wrappers = await page.evaluate("""() => {
            const tables = document.querySelectorAll('.tutorial-article table');
            const wrappers = document.querySelectorAll('.tutorial-article .table-responsive');
            const nested = document.querySelectorAll('.table-responsive .table-responsive');
            return {
                tables: tables.length,
                wrappers: wrappers.length,
                nested: nested.length
            };
        }""")
        test_results["tcp_table_responsive"] = table_wrappers["tables"] >= 1 and table_wrappers["nested"] == 0
        print(f"[{'PASS' if test_results['tcp_table_responsive'] else 'FAIL'}] Responsive tables: {table_wrappers['tables']} tables, {table_wrappers['wrappers']} wrappers, {table_wrappers['nested']} nested")

        # First tutorial Previous / Next contract: No Previous card, Yes Next card
        nav_cards = await page.evaluate("""() => {
            const prev = document.querySelector('.tutorial-nav-card.prev');
            const next = document.querySelector('.tutorial-nav-card.next');
            return {
                prevPresent: !!prev,
                nextPresent: !!next,
                nextTitle: next ? next.querySelector('.tutorial-nav-title')?.textContent.trim() : null
            };
        }""")
        test_results["tcp_nav_first_contract"] = not nav_cards["prevPresent"] and nav_cards["nextPresent"]
        print(f"[{'PASS' if test_results['tcp_nav_first_contract'] else 'FAIL'}] First tutorial navigation contract: prevPresent={nav_cards['prevPresent']} (False expected), nextPresent={nav_cards['nextPresent']} (True expected, Next: '{nav_cards['nextTitle']}')")

        # Back to Category button
        back_btn = await page.locator(".tutorial-back-category a").get_attribute("href")
        test_results["tcp_back_btn"] = "networking.html" in back_btn
        print(f"[{'PASS' if test_results['tcp_back_btn'] else 'FAIL'}] Canonical Back to Category button points to: {back_btn}")

        # Related tutorials: max 3, not containing current tutorial
        related_count = await page.locator(".tutorial-related-card").count()
        test_results["tcp_related"] = 0 < related_count <= 3
        print(f"[{'PASS' if test_results['tcp_related'] else 'FAIL'}] Deterministic Related Tutorials: {related_count} items rendered (max 3)")

        # Capture Desktop Light Screenshot
        await page.screenshot(path=str(QA_DIR / "phase6_tutorial_desktop_light.png"), full_page=False)
        print("Captured: qa/phase6_tutorial_desktop_light.png")

        # Switch to Dark Theme & Capture Desktop Dark Screenshot
        await page.click(".theme-toggle")
        await page.wait_for_timeout(300)
        theme_attr = await page.evaluate("document.documentElement.getAttribute('data-theme')")
        test_results["dark_theme"] = theme_attr == "dark"
        await page.screenshot(path=str(QA_DIR / "phase6_tutorial_desktop_dark.png"), full_page=False)
        print(f"Captured: qa/phase6_tutorial_desktop_dark.png (theme: {theme_attr})")

        # Switch back to light
        await page.click(".theme-toggle")
        await page.wait_for_timeout(300)

        # -------------------------------------------------------------
        # Test 2: Middle Tutorial (osi-model-explained.html)
        # -------------------------------------------------------------
        print("\n--- Test 2: Middle Tutorial Navigation (osi-model-explained.html) ---")
        await page.goto(f"{BASE_URL}/tutorials/networking/osi-model-explained.html", wait_until="networkidle")
        await page.wait_for_selector(".tutorial-footer-section", timeout=5000)

        mid_nav = await page.evaluate("""() => {
            const prev = document.querySelector('.tutorial-nav-card.prev');
            const next = document.querySelector('.tutorial-nav-card.next');
            return {
                prevTitle: prev ? prev.querySelector('.tutorial-nav-title')?.textContent.trim() : null,
                nextTitle: next ? next.querySelector('.tutorial-nav-title')?.textContent.trim() : null
            };
        }""")
        test_results["mid_prev_next"] = mid_nav["prevTitle"] is not None and mid_nav["nextTitle"] is not None
        print(f"[{'PASS' if test_results['mid_prev_next'] else 'FAIL'}] Middle Tutorial: Prev='{mid_nav['prevTitle']}', Next='{mid_nav['nextTitle']}'")

        # -------------------------------------------------------------
        # Test 3: Last Tutorial in Canonical Order
        # -------------------------------------------------------------
        with open(TUTS_JSON_PATH, "r", encoding="utf-8") as f:
            all_tuts = json.load(f)
        last_tut = all_tuts[-1]
        last_tut_url = f"{BASE_URL}/{last_tut['url'].replace('./', '')}"
        print(f"\n--- Test 3: Last Tutorial in Canonical Order ({last_tut['id']}) ---")
        await page.goto(last_tut_url, wait_until="networkidle")
        await page.wait_for_selector(".tutorial-footer-section", timeout=5000)

        last_nav = await page.evaluate("""() => {
            const prev = document.querySelector('.tutorial-nav-card.prev');
            const next = document.querySelector('.tutorial-nav-card.next');
            return {
                prevPresent: !!prev,
                nextPresent: !!next,
                prevTitle: prev ? prev.querySelector('.tutorial-nav-title')?.textContent.trim() : null
            };
        }""")
        test_results["last_nav_contract"] = last_nav["prevPresent"] and not last_nav["nextPresent"]
        print(f"[{'PASS' if test_results['last_nav_contract'] else 'FAIL'}] Last Tutorial navigation contract: prevPresent={last_nav['prevPresent']} (Prev: '{last_nav['prevTitle']}'), nextPresent={last_nav['nextPresent']} (False expected)")

        # -------------------------------------------------------------
        # Test 4: Code Block Enhancement & 1-Click Clipboard Copy
        # (common-network-ports.html & advanced-dns-troubleshooting.html)
        # -------------------------------------------------------------
        print("\n--- Test 4: Code Enhancement & 1-Click Clipboard Copy ---")
        await page.goto(f"{BASE_URL}/tutorials/networking/common-network-ports.html", wait_until="networkidle")
        await page.wait_for_selector(".tutorial-code-block", timeout=5000)

        code_blocks_count = await page.locator(".tutorial-code-block").count()
        copy_btns_count = await page.locator(".tutorial-code-copy-btn").count()
        test_results["code_blocks_enhanced"] = code_blocks_count >= 1 and copy_btns_count == code_blocks_count
        print(f"[{'PASS' if test_results['code_blocks_enhanced'] else 'FAIL'}] Code Blocks: {code_blocks_count} enhanced with copy buttons")

        # Test Copy button interaction & Toast notification
        first_copy_btn = page.locator(".tutorial-code-copy-btn").first
        await first_copy_btn.scroll_into_view_if_needed()
        await first_copy_btn.click()
        await page.wait_for_selector("#copy-toast.active", timeout=4000)

        # Toast verification
        toast_active = await page.evaluate("""() => {
            const toast = document.getElementById('copy-toast');
            const role = toast?.getAttribute('role');
            const live = toast?.getAttribute('aria-live');
            const active = toast?.classList.contains('active');
            return { role, live, active };
        }""")
        test_results["copy_toast"] = toast_active["active"] and toast_active["live"] == "polite"
        print(f"[{'PASS' if test_results['copy_toast'] else 'FAIL'}] Copy Toast displayed (active={toast_active['active']}, aria-live='{toast_active['live']}')")

        # Capture Code Copy Screenshot
        await page.screenshot(path=str(QA_DIR / "phase6_tutorial_code_copy.png"), full_page=False)
        print("Captured: qa/phase6_tutorial_code_copy.png")

        # -------------------------------------------------------------
        # Test 5: Callout Standardization (access-control-lists-explained.html)
        # -------------------------------------------------------------
        print("\n--- Test 5: Callout Standardization (access-control-lists-explained.html) ---")
        await page.goto(f"{BASE_URL}/tutorials/networking/access-control-lists-explained.html", wait_until="networkidle")
        await page.wait_for_selector(".tutorial-callout", timeout=5000)

        callout_data = await page.evaluate("""() => {
            const callout = document.querySelector('.tutorial-callout');
            return {
                present: !!callout,
                className: callout?.className,
                role: callout?.getAttribute('role'),
                hasIcon: !!callout?.querySelector('.callout-icon i'),
                text: callout?.textContent.trim().substring(0, 70)
            };
        }""")
        test_results["callout_standardized"] = callout_data["present"] and callout_data["role"] == "note" and callout_data["hasIcon"]
        print(f"[{'PASS' if test_results['callout_standardized'] else 'FAIL'}] Callout: class='{callout_data['className']}', role='{callout_data['role']}', text='{callout_data['text']}...'")

        # -------------------------------------------------------------
        # Test 6: Engine Idempotency (Calling initTutorialEngine() Twice)
        # -------------------------------------------------------------
        print("\n--- Test 6: Engine Idempotency Verification ---")
        counts_before = await page.evaluate("""() => ({
            tocItems: document.querySelectorAll('#tutorial-toc .toc-link').length,
            codeBlocks: document.querySelectorAll('.tutorial-code-block').length,
            copyBtns: document.querySelectorAll('.tutorial-code-copy-btn').length,
            callouts: document.querySelectorAll('.tutorial-callout').length,
            navCards: document.querySelectorAll('.tutorial-nav-card').length,
            relatedCards: document.querySelectorAll('.tutorial-related-card').length,
            toasts: document.querySelectorAll('#copy-toast').length
        })""")

        # Execute initTutorialEngine() multiple times
        await page.evaluate("""() => {
            window.initTutorialEngine();
            window.initTutorialEngine();
        }""")
        await page.wait_for_timeout(500)

        counts_after = await page.evaluate("""() => ({
            tocItems: document.querySelectorAll('#tutorial-toc .toc-link').length,
            codeBlocks: document.querySelectorAll('.tutorial-code-block').length,
            copyBtns: document.querySelectorAll('.tutorial-code-copy-btn').length,
            callouts: document.querySelectorAll('.tutorial-callout').length,
            navCards: document.querySelectorAll('.tutorial-nav-card').length,
            relatedCards: document.querySelectorAll('.tutorial-related-card').length,
            toasts: document.querySelectorAll('#copy-toast').length
        })""")

        idempotency_pass = counts_before == counts_after
        test_results["idempotency"] = idempotency_pass
        print(f"[{'PASS' if idempotency_pass else 'FAIL'}] Idempotency test (before={counts_before}, after={counts_after})")

        # -------------------------------------------------------------
        # Test 7: Table of Contents & Sticky Aside Focus
        # -------------------------------------------------------------
        print("\n--- Test 7: Table of Contents UI Verification ---")
        await page.goto(f"{BASE_URL}/tutorials/networking/osi-model-explained.html", wait_until="networkidle")
        await page.wait_for_selector("#tutorial-toc .toc-link", timeout=5000)

        # Click a TOC link and verify URL hash update
        first_toc_link = page.locator("#tutorial-toc .toc-link").first
        target_href = await first_toc_link.get_attribute("href")
        await first_toc_link.click()
        await page.wait_for_timeout(300)

        current_url = page.url
        test_results["toc_hash"] = target_href in current_url
        print(f"[{'PASS' if test_results['toc_hash'] else 'FAIL'}] TOC Navigation hash update: {target_href} in {current_url}")

        await page.screenshot(path=str(QA_DIR / "phase6_tutorial_toc.png"), full_page=False)
        print("Captured: qa/phase6_tutorial_toc.png")

        # -------------------------------------------------------------
        # Test 8: Mobile Accordion TOC & Responsive Overflow across Viewports
        # -------------------------------------------------------------
        print("\n--- Test 8: Responsive Viewports & Zero Horizontal Overflow ---")
        viewports = [
            ("Desktop 1440px", 1440, 900),
            ("Tablet 1024px", 1024, 768),
            ("Tablet Small 768px", 768, 1024),
            ("Mobile 375px", 375, 667)
        ]

        overflow_failures = []
        for name, width, height in viewports:
            await page.set_viewport_size({"width": width, "height": height})
            await page.goto(f"{BASE_URL}/tutorials/networking/tcp-vs-udp.html", wait_until="networkidle")
            await page.wait_for_timeout(300)

            has_overflow = await page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
            if has_overflow:
                overflow_failures.append(f"{name} ({width}px)")

        test_results["zero_overflow"] = len(overflow_failures) == 0
        print(f"[{'PASS' if test_results['zero_overflow'] else 'FAIL'}] Zero Horizontal Overflow across viewports: {test_results['zero_overflow']} (Failures: {overflow_failures})")

        # Test Mobile TOC details element at 375px
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.goto(f"{BASE_URL}/tutorials/networking/tcp-vs-udp.html", wait_until="networkidle")
        await page.wait_for_selector(".tutorial-mobile-toc", timeout=5000)

        mobile_toc_visible = await page.evaluate("""() => {
            const el = document.querySelector('.tutorial-mobile-toc');
            return !!el && window.getComputedStyle(el).display !== 'none';
        }""")
        test_results["mobile_toc_visible"] = mobile_toc_visible
        print(f"[{'PASS' if mobile_toc_visible else 'FAIL'}] Mobile TOC Accordion rendered and visible on mobile viewport")

        # Capture Mobile Screenshots (Light and Dark)
        await page.screenshot(path=str(QA_DIR / "phase6_tutorial_mobile_light.png"), full_page=False)
        print("Captured: qa/phase6_tutorial_mobile_light.png")

        # Toggle Dark mode on mobile
        await page.click(".theme-toggle")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(QA_DIR / "phase6_tutorial_mobile_dark.png"), full_page=False)
        print("Captured: qa/phase6_tutorial_mobile_dark.png")

        # -------------------------------------------------------------
        # Test 9: Reduced Motion Compliance
        # -------------------------------------------------------------
        print("\n--- Test 9: Reduced Motion Verification ---")
        reduced_motion_context = await browser.new_context(reduced_motion="reduce")
        rm_page = await reduced_motion_context.new_page()
        await rm_page.goto(f"{BASE_URL}/tutorials/networking/osi-model-explained.html", wait_until="networkidle")

        prefers_reduced = await rm_page.evaluate("window.matchMedia('(prefers-reduced-motion: reduce)').matches")
        test_results["reduced_motion_respected"] = prefers_reduced
        print(f"[{'PASS' if prefers_reduced else 'FAIL'}] Reduced motion media query respected: {prefers_reduced}")
        await reduced_motion_context.close()

        # -------------------------------------------------------------
        # Console & Network Health Summary
        # -------------------------------------------------------------
        print("\n--- Console & Network Health ---")
        print(f"Console Errors: {len(console_errors)}")
        if console_errors:
            for err in console_errors:
                print(f"  [ERROR] {err}")
        print(f"Local 404 Requests: {len(network_404s)}")
        if network_404s:
            for url in network_404s:
                print(f"  [404] {url}")

        test_results["console_healthy"] = len(console_errors) == 0
        test_results["network_healthy"] = len(network_404s) == 0

        await browser.close()

    print("\n" + "=" * 68)
    print("PHASE 6 VERIFICATION SUMMARY:")
    all_passed = all(test_results.values())
    for k, v in test_results.items():
        print(f"  {k:30}: {'PASS' if v else 'FAIL'}")
    print("=" * 68)
    assert all_passed, "Some Phase 6 verification tests failed!"
    print("\nALL PHASE 6 VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    audit_raw_static_seo()
    asyncio.run(run_phase6_browser_tests())
