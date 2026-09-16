import json
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
LIVE_BASE = "https://themjtechhub.site"

with open("data/quizzes.json", "r", encoding="utf-8") as f:
    quizzes = json.load(f)

print(f"Testing {len(quizzes)} canonical quizzes on live production...")

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
    for q in quizzes:
        qid = q["id"]
        qtitle = q["title"]
        url = f"{LIVE_BASE}/quiz.html?quiz={qid}"
        
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        
        page.goto(url, timeout=20000)
        page.wait_for_timeout(1000)
        
        # Verify auto-start:
        # 1. Selector screen should be hidden
        selector_visible = page.is_visible("#quiz-selector")
        # 2. Active quiz screen should be visible
        active_screen_visible = page.is_visible("#quiz-app")
        # 3. Active quiz title
        active_title = page.inner_text("#quiz-title") if active_screen_visible else "NOT VISIBLE"
        
        print(f"Quiz '{qid}':")
        print(f"  URL: {url}")
        print(f"  Selector hidden: {not selector_visible}")
        print(f"  Active screen visible: {active_screen_visible}")
        print(f"  Active title: '{active_title}' (Expected: '{qtitle}')")
        print(f"  Console errors: {len(console_errors)}")
        
        assert not selector_visible, f"Selector screen should be hidden for quiz {qid}"
        assert active_screen_visible, f"Active screen should be visible for quiz {qid}"
        assert active_title == qtitle, f"Expected title '{qtitle}', got '{active_title}'"
        assert len(console_errors) == 0, f"Console errors on {qid}: {console_errors}"
        
        page.close()
        
    browser.close()

print("\n>>> ALL 8 QUIZ DEEP-LINKS VERIFIED AUTO-STARTING ON LIVE PRODUCTION! <<<")
