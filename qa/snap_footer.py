#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def snap():
    p = await async_playwright().start()
    b = await p.chromium.launch(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", headless=True)
    page = await b.new_page()
    await page.set_viewport_size({"width": 1440, "height": 900})
    await page.goto("http://localhost/index/index.html", wait_until="networkidle")
    await page.wait_for_selector(".site-footer", timeout=5000)
    footer = await page.query_selector(".site-footer")
    
    # Desktop Dark
    await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")
    await page.wait_for_timeout(300)
    await footer.screenshot(path="qa/phase3_footer_desktop_dark.png")
    
    # Desktop Light
    await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'light')")
    await page.wait_for_timeout(300)
    await footer.screenshot(path="qa/phase3_footer_desktop_light.png")
    
    # Mobile Dark
    await page.set_viewport_size({"width": 375, "height": 667})
    await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")
    await page.wait_for_timeout(300)
    await footer.screenshot(path="qa/phase3_footer_mobile_dark.png")
    
    # Mobile Light
    await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'light')")
    await page.wait_for_timeout(300)
    await footer.screenshot(path="qa/phase3_footer_mobile_light.png")
    
    await b.close()
    await p.stop()
    print("Footer screenshots captured successfully!")

if __name__ == "__main__":
    asyncio.run(snap())
