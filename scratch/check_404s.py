import asyncio
from playwright.async_api import async_playwright

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

async def check():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        page = await b.new_page()
        page.on('response', lambda resp: print('HTTP Response:', resp.status, resp.url) if resp.status == 404 else None)
        await page.goto('http://localhost/index/windows.html', wait_until='networkidle')
        await b.close()

asyncio.run(check())
