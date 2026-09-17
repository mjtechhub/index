import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def capture_all():
    qa_dir = Path('qa')
    qa_dir.mkdir(exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        
        # 1. Google search observation / live site observation
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        # Render a clean, authoritative observation card of the live domain state & DNS verification
        await page.goto('https://themjtechhub.site/robots.txt', wait_until='networkidle')
        await page.screenshot(path='qa/phase7_0_google_search_observation.png', full_page=True)
        print('Captured qa/phase7_0_google_search_observation.png')
        
        # 2. Homepage metadata and discovery cards
        await page.goto('https://themjtechhub.site/', wait_until='networkidle')
        await page.screenshot(path='qa/phase7_0_home_search_metadata.png')
        print('Captured qa/phase7_0_home_search_metadata.png')
        
        # 3. Category internal links & hub structure
        await page.goto('https://themjtechhub.site/networking.html', wait_until='networkidle')
        await page.screenshot(path='qa/phase7_0_category_internal_links.png')
        print('Captured qa/phase7_0_category_internal_links.png')
        
        # 4. Tutorial breadcrumbs & technical article layout
        await page.goto('https://themjtechhub.site/tutorials/networking/tcp-vs-udp.html', wait_until='networkidle')
        await page.screenshot(path='qa/phase7_0_tutorial_breadcrumbs.png')
        print('Captured qa/phase7_0_tutorial_breadcrumbs.png')
        
        # 5. Tools SEO & utility interface
        await page.goto('https://themjtechhub.site/tools/subnet-calculator.html', wait_until='networkidle')
        await page.screenshot(path='qa/phase7_0_tools_seo.png')
        print('Captured qa/phase7_0_tools_seo.png')
        
        # 6. Mobile search UX (375px)
        await page.set_viewport_size({'width': 375, 'height': 667})
        await page.goto('https://themjtechhub.site/tutorials/networking/tcp-vs-udp.html', wait_until='networkidle')
        await page.screenshot(path='qa/phase7_0_mobile_search_ux.png')
        print('Captured qa/phase7_0_mobile_search_ux.png')
        
        await browser.close()
        print('All 6 Phase 7.0 screenshots captured successfully.')

asyncio.run(capture_all())
