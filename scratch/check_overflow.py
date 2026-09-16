import asyncio
from playwright.async_api import async_playwright

test_pages = [
    'tools/vlsm-planner.html',
    'tools/network-diagnostic-workbench.html',
    'tools/port-reference.html',
    'labs.html'
]

async def check():
    p = await async_playwright().start()
    browser = await p.chromium.launch(executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', headless=True)
    page = await browser.new_page()
    await page.set_viewport_size({'width': 320, 'height': 800})
    for p_rel in test_pages:
        await page.goto(f'http://localhost/index/{p_rel}', wait_until='networkidle')
        res = await page.evaluate("""() => {
            const sw = document.documentElement.scrollWidth;
            const iw = window.innerWidth;
            const overflowing = [];
            document.querySelectorAll('*').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.right > iw + 1 || el.scrollWidth > iw + 1) {
                    overflowing.push({
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        right: r.right,
                        scrollWidth: el.scrollWidth
                    });
                }
            });
            return { sw, iw, overflowing };
        }""")
        print(f"=== {p_rel} ===")
        print(f"ScrollWidth: {res['sw']} InnerWidth: {res['iw']}")
        for item in res['overflowing'][:8]:
            print("  ", item)
    await browser.close()
    await p.stop()

asyncio.run(check())
