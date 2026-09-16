import urllib.request
import json
import ssl
import re

ctx = ssl.create_default_context()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_json(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))

def fetch_text(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        return resp.read().decode('utf-8')

print("=== CHECKING LIVE JSON DATA PARITY ===")
try:
    live_tuts = fetch_json('https://themjtechhub.site/data/tutorials.json')
    print(f"Live tutorials.json count: {len(live_tuts)} (Repo: 148)")
except Exception as e:
    print("Error fetching live tutorials.json:", e)

try:
    live_cmds = fetch_json('https://themjtechhub.site/data/commands.json')
    print(f"Live commands.json count: {len(live_cmds)} (Repo: 42)")
except Exception as e:
    print("Error fetching live commands.json:", e)

try:
    live_quizzes = fetch_json('https://themjtechhub.site/data/quizzes.json')
    live_q_count = sum(len(q.get('questions', [])) for q in live_quizzes)
    print(f"Live quizzes.json count: {len(live_quizzes)} quizzes, {live_q_count} questions (Repo: 8 quizzes, 64 questions)")
except Exception as e:
    print("Error fetching live quizzes.json:", e)

try:
    live_resources = fetch_json('https://themjtechhub.site/data/resources.json')
    print(f"Live resources.json count: {len(live_resources)} (Repo: 26)")
except Exception as e:
    print("Error fetching live resources.json:", e)

try:
    live_labs = fetch_json('https://themjtechhub.site/data/troubleshooting-labs.json')
    print(f"Live troubleshooting-labs.json count: {len(live_labs)} (Repo: 6)")
except Exception as e:
    print("Error fetching live troubleshooting-labs.json:", e)

try:
    live_ports = fetch_json('https://themjtechhub.site/data/ports.json')
    print(f"Live ports.json count: {len(live_ports)} (Repo: 50)")
except Exception as e:
    print("Error fetching live ports.json:", e)

print("\n=== CHECKING LIVE HTML PARITY ===")
# Check header components
try:
    live_header = fetch_text('https://themjtechhub.site/components/header.html')
    has_tools_nav = 'tools.html' in live_header
    has_labs_nav = 'labs.html' in live_header
    has_quizzes_nav = 'quiz.html' in live_header
    print(f"Live header: Tools in nav: {has_tools_nav}, Labs in nav: {has_labs_nav}, Quizzes in nav: {has_quizzes_nav}")
except Exception as e:
    print("Error fetching live header.html:", e)

# Check footer components
try:
    live_footer = fetch_text('https://themjtechhub.site/components/footer.html')
    has_creator = 'Mayur Talsaniya' in live_footer
    has_res_link = 'resources.html' in live_footer
    print(f"Live footer: Mayur Talsaniya credit: {has_creator}, Resources link: {has_res_link}")
except Exception as e:
    print("Error fetching live footer.html:", e)

# Check topics badges
try:
    live_topics_html = fetch_text('https://themjtechhub.site/topics.html')
    print("Live topics.html badges:")
    badge148 = '148' in live_topics_html and 'Published' in live_topics_html
    badge471 = '471' in live_topics_html and 'Curriculum' in live_topics_html
    print(f"  148 Published Tutorials present: {badge148}")
    print(f"  471 Curriculum Topics present: {badge471}")
except Exception as e:
    print("Error fetching live topics.html:", e)

# Check sitemap.xml on live
try:
    live_sitemap = fetch_text('https://themjtechhub.site/sitemap.xml')
    live_sitemap_urls = re.findall(r'<loc>([^<]+)</loc>', live_sitemap)
    print(f"Live sitemap URL count: {len(live_sitemap_urls)}")
except Exception as e:
    print("Error fetching live sitemap.xml:", e)

# Check robots.txt on live
try:
    live_robots = fetch_text('https://themjtechhub.site/robots.txt')
    print(f"Live robots.txt lines:\n{live_robots.strip()}")
except Exception as e:
    print("Error fetching live robots.txt:", e)
