#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def test_search():
    CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        page = await browser.new_page()
        browser_errors = []
        page.on("console", lambda msg: browser_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: browser_errors.append(str(err)))
        
        await page.goto("http://localhost/index/index.html", wait_until="networkidle")
        
        # Test 1: Open Search via Ctrl+K
        await page.keyboard.press("Control+KeyK")
        await page.wait_for_selector("#search-modal-backdrop.active", timeout=3000)
        print("PASS: Search modal opened via Ctrl+K")

        # Debug getSearchData in page context
        search_data_count = await page.evaluate("""async () => {
            const res = await fetch('./data/topics.json');
            const data = await res.json();
            return { ok: res.ok, count: (data.categories || []).length };
        }""")
        print(f"Debug topics.json fetch inside browser: {search_data_count}")
        
        # Type into input
        await page.click("#search-modal-input")
        await page.type("#search-modal-input", "Networking", delay=100)
        await page.wait_for_timeout(1000)

        # Inspect resultsContainer
        results_html = await page.evaluate("() => document.getElementById('search-results-container').innerHTML")
        print(f"resultsContainer HTML: {results_html[:200]}")

        items = await page.query_selector_all(".search-result-item")
        results = []
        for it in items:
            title_el = await it.query_selector(".search-result-title")
            meta_el = await it.query_selector(".search-result-meta")
            t_text = await title_el.inner_text() if title_el else ""
            m_text = await meta_el.inner_text() if meta_el else ""
            results.append(f"{t_text} ({m_text})")
        print(f"Results for 'Networking': {len(results)} found")
        assert any("Topic" in r for r in results), "Failed: No Topic found for 'Networking'"
        print("PASS: Topics successfully indexed in search results")

        # Test 3: Search for Command ("ipconfig")
        await page.fill("#search-modal-input", "ipconfig")
        await page.wait_for_timeout(500)
        items = await page.query_selector_all(".search-result-item")
        results = [await (await it.query_selector(".search-result-title")).inner_text() for it in items]
        print(f"Results for 'ipconfig': {results}")
        assert any("ipconfig" in r.lower() for r in results), "Failed: ipconfig not found"
        print("PASS: Commands successfully indexed in search results")

        # Test 4: Search for Resource ("Cheat Sheet")
        await page.fill("#search-modal-input", "Cheat Sheet")
        await page.wait_for_timeout(500)
        items = await page.query_selector_all(".search-result-item")
        results = [await (await it.query_selector(".search-result-title")).inner_text() for it in items]
        print(f"Results for 'Cheat Sheet': {results}")
        assert any("Cheat Sheet" in r for r in results), "Failed: Cheat Sheet resource not found"
        print("PASS: Resources successfully indexed in search results")

        # Test 5: Check console errors
        print(f"Recorded browser errors: {browser_errors}")
        assert len(browser_errors) == 0, f"Console errors detected: {browser_errors}"
        print("PASS: Zero console errors during search operations")

        await browser.close()
        print("\nALL SEARCH TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(test_search())
