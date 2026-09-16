import re
from pathlib import Path

ROOT = Path('.')
pages = [
    ROOT / 'tools.html',
    ROOT / 'labs.html',
    ROOT / 'tools' / 'subnet-calculator.html',
    ROOT / 'tools' / 'vlsm-planner.html',
    ROOT / 'tools' / 'network-diagnostic-workbench.html',
    ROOT / 'tools' / 'port-reference.html'
]

titles = set()

for p in pages:
    assert p.exists(), f"{p} does not exist"
    content = p.read_text(encoding='utf-8')
    
    # Title
    t_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    assert t_match, f"Missing title in {p}"
    title = t_match.group(1).strip()
    assert title not in titles, f"Duplicate title '{title}' in {p}"
    titles.add(title)
    
    # Meta description
    d_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
    assert d_match, f"Missing meta description in {p}"
    assert len(d_match.group(1).strip()) > 20, f"Description too short in {p}"
    
    # Canonical
    c_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](https://themjtechhub\.site.*?)["\']', content, re.IGNORECASE)
    assert c_match, f"Missing or invalid canonical in {p}"
    
    # OpenGraph
    assert re.search(r'<meta\s+property=["\']og:title["\']', content, re.IGNORECASE), f"Missing og:title in {p}"
    assert re.search(r'<meta\s+property=["\']og:description["\']', content, re.IGNORECASE), f"Missing og:description in {p}"
    assert re.search(r'<meta\s+property=["\']og:url["\']\s+content=["\']https://themjtechhub\.site', content, re.IGNORECASE), f"Missing og:url in {p}"
    assert re.search(r'<meta\s+property=["\']og:site_name["\']', content, re.IGNORECASE), f"Missing og:site_name in {p}"
    assert re.search(r'<meta\s+property=["\']og:type["\']', content, re.IGNORECASE), f"Missing og:type in {p}"
    
    # Twitter
    assert re.search(r'<meta\s+name=["\']twitter:card["\']', content, re.IGNORECASE), f"Missing twitter:card in {p}"
    assert re.search(r'<meta\s+name=["\']twitter:title["\']', content, re.IGNORECASE), f"Missing twitter:title in {p}"
    assert re.search(r'<meta\s+name=["\']twitter:description["\']', content, re.IGNORECASE), f"Missing twitter:description in {p}"
    
    # Exactly one H1 in raw HTML
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    assert len(h1s) == 1, f"Expected exactly 1 H1 in {p}, found {len(h1s)}: {h1s}"
    
    print(f"[PASS] {p.name}: title='{title}', H1='{h1s[0].strip()}'")

print("\nALL 6 PAGES PASSED STATIC SEO AUDIT PERFECTLY!")
