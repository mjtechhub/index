import json
import re
from pathlib import Path

root = Path('.')

with open('data/tutorials.json', 'r', encoding='utf-8') as f:
    tuts_data = json.load(f)

print(f'Total tutorials in tutorials.json: {len(tuts_data)}')

tut_files = {}
for t in tuts_data:
    url = t['url'] # e.g. "tutorials/networking/tcp-vs-udp.html"
    p = root / url
    tut_files[url] = {
        'id': t['id'],
        'exists': p.exists(),
        'title': t.get('title'),
        'category': t.get('category'),
        'inbound_from_tuts': 0,
        'inbound_from_pages': 0,
        'has_breadcrumbs': False,
        'has_json_ld': False,
        'json_ld_type': None,
        'canonical': None
    }

# Check all HTML files for links to these tutorials
all_html = [f for f in root.glob('**/*.html') if not any(part.startswith('.') or part in ('scratch', 'backup', 'node_modules', 'components') for part in f.parts)]

for hf in all_html:
    rel_hf = hf.as_posix()
    content = hf.read_text(encoding='utf-8', errors='ignore')
    
    # Find all hrefs
    hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', content)
    for h in hrefs:
        clean_h = h.split('#')[0].split('?')[0].lstrip('./').replace('../', '')
        for t_url in tut_files:
            if clean_h == t_url or t_url.endswith(clean_h) or clean_h.endswith(t_url):
                if 'tutorials/' in rel_hf:
                    tut_files[t_url]['inbound_from_tuts'] += 1
                else:
                    tut_files[t_url]['inbound_from_pages'] += 1

# Inspect each tutorial HTML file
for t_url, info in tut_files.items():
    p = root / t_url
    if not p.exists():
        continue
    content = p.read_text(encoding='utf-8', errors='ignore')
    
    # Breadcrumbs
    if 'breadcrumb' in content.lower():
        info['has_breadcrumbs'] = True
        
    # JSON-LD
    m_ld = re.search(r'<script\s+type=[\'"]application/ld\+json[\'"]>(.*?)</script>', content, re.DOTALL)
    if m_ld:
        info['has_json_ld'] = True
        try:
            ld_obj = json.loads(m_ld.group(1).strip())
            info['json_ld_type'] = ld_obj.get('@type')
        except Exception:
            pass
            
    # Canonical
    m_can = re.search(r'<link[^>]+rel=[\'"]canonical[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', content)
    if m_can:
        info['canonical'] = m_can.group(1)

# Summary
orphans = [u for u, info in tut_files.items() if info['inbound_from_tuts'] == 0 and info['inbound_from_pages'] == 0]
print(f'Orphan tutorials (0 inbound links anywhere in static HTML): {len(orphans)}')
if orphans:
    print('  Sample orphans in static HTML:', orphans[:5])

# Inbound link distribution
print(f'Tutorials with inbound links from other tutorials: {sum(1 for u, i in tut_files.items() if i["inbound_from_tuts"] > 0)}')
print(f'Tutorials with inbound links from hub pages (topics/categories static): {sum(1 for u, i in tut_files.items() if i["inbound_from_pages"] > 0)}')
print(f'Tutorials with JSON-LD: {sum(1 for u, i in tut_files.items() if i["has_json_ld"])}')
print(f'Tutorials with Breadcrumbs markup/element: {sum(1 for u, i in tut_files.items() if i["has_breadcrumbs"])}')
