import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto('http://localhost/index/editor.html')
        
        # Fill in form
        await page.fill('#lesson-title', 'Template QA Test')
        await page.fill('#lesson-category', 'Networking')
        await page.fill('#lesson-level', 'Beginner')
        await page.fill('#lesson-markdown', '# Template QA Test\n\n## Introduction\nTemplate verification content.\n\n### Example\nTesting responsive formatting.')
        
        # Wait for preview to update
        await page.wait_for_timeout(2000)
        
        # Click export HTML
        async with page.expect_download() as download_info:
            await page.click('#btn-export-html')
            
        download = await download_info.value
        path = await download.path()
        
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Verify header, footer, class
        assert '<header>' in html, "Header is missing"
        assert '<footer>' in html, "Footer is missing"
        assert 'class="lesson-container py-4"' in html, "lesson-container class is missing"
        assert 'class="content lesson-content"' in html, "lesson-content class is missing"
        assert '../../assets/brand/mj-tech-hub-header.png' in html, "Relative paths not updated"
        
        # Verify duplicate H1 is removed
        # The title is "Template QA Test" which is rendered by the generator template.
        # But the markdown '# Template QA Test' should have been stripped out.
        h1_count = len(re.findall(r'<h1.*?>Template QA Test</h1>', html, re.IGNORECASE))
        assert h1_count == 1, f"Expected exactly 1 H1 title, found {h1_count}"
        
        print("PASS: Generator output is correct.")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
