import xml.etree.ElementTree as ET
import re
from pathlib import Path
from collections import Counter

root = Path('.')
sitemap_path = root / 'sitemap.xml'
tree = ET.parse(sitemap_path)
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs = [el.text.strip() for el in tree.getroot().findall('sm:url/sm:loc', ns)]

print(f'Total sitemap URLs: {len(locs)}')
base_url = 'https://themjtechhub.site'

titles = {}
descriptions = {}
h1s = {}
canonicals = {}
og_titles = {}
og_descs = {}
twitter_titles = {}

for u in locs:
    rel = u.replace(base_url, '').lstrip('/')
    if rel == '':
        file_path = root / 'index.html'
    else:
        file_path = root / rel
        
    assert file_path.exists(), f'File does not exist: {file_path} for URL {u}'
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    
    # Title
    m_t = re.search(r'<title>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
    t = m_t.group(1).strip() if m_t else ''
    titles[u] = t
    
    # Description
    m_d = re.search(r'<meta[^>]+name=[\'"]description[\'"][^>]+content=[\'"]([^\'"]*)[\'"]', content, re.IGNORECASE)
    if not m_d:
        m_d = re.search(r'<meta[^>]+content=[\'"]([^\'"]*)[\'"][^>]+name=[\'"]description[\'"]', content, re.IGNORECASE)
    d = m_d.group(1).strip() if m_d else ''
    descriptions[u] = d
    
    # Canonical
    m_c = re.search(r'<link[^>]+rel=[\'"]canonical[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
    if not m_c:
        m_c = re.search(r'<link[^>]+href=[\'"]([^\'"]+)[\'"][^>]+rel=[\'"]canonical[\'"]', content, re.IGNORECASE)
    c = m_c.group(1).strip() if m_c else ''
    canonicals[u] = c
    
    # H1
    h1_matches = re.findall(r'<h1\b[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    h1s[u] = [re.sub(r'<[^>]+>', '', h).strip() for h in h1_matches]

print('\n--- Canonical Check ---')
canonical_mismatches = []
for u, c in canonicals.items():
    if u != c:
        canonical_mismatches.append((u, c))
print(f'Canonical URL matches sitemap URL: {len(canonicals) - len(canonical_mismatches)} / {len(canonicals)}')
if canonical_mismatches:
    print('  Mismatches:', canonical_mismatches[:5])

print('\n--- Titles Check ---')
empty_titles = [u for u, t in titles.items() if not t]
print(f'Empty titles: {len(empty_titles)}')
title_counts = Counter(titles.values())
duplicate_titles = {t: cnt for t, cnt in title_counts.items() if cnt > 1}
print(f'Unique titles: {len(title_counts)} out of {len(titles)}')
print(f'Duplicate titles: {len(duplicate_titles)}')
if duplicate_titles:
    for t, cnt in duplicate_titles.items():
        print(f'  "{t}": {cnt} times')

print('\n--- Descriptions Check ---')
empty_descs = [u for u, d in descriptions.items() if not d]
print(f'Empty descriptions: {len(empty_descs)}')
desc_counts = Counter(descriptions.values())
duplicate_descs = {d: cnt for d, cnt in desc_counts.items() if cnt > 1}
print(f'Unique descriptions: {len(desc_counts)} out of {len(descriptions)}')
print(f'Duplicate descriptions: {len(duplicate_descs)}')
if duplicate_descs:
    for d, cnt in duplicate_descs.items():
        print(f'  "{d}": {cnt} times')

print('\n--- H1 Check ---')
missing_h1 = [u for u, hs in h1s.items() if len(hs) == 0]
multiple_h1 = [u for u, hs in h1s.items() if len(hs) > 1]
print(f'Pages with 0 static H1s: {len(missing_h1)}')
if missing_h1:
    print('  Missing static H1:', missing_h1)
print(f'Pages with >1 static H1s: {len(multiple_h1)}')
