import os
import re
import json
from pathlib import Path

root = Path('.')
html_files = sorted(list(root.glob('**/*.html')))
# Filter out scratch, .git, .gemini, .agents, node_modules, components
html_files = [f for f in html_files if not any(part.startswith('.') or part in ('scratch', 'node_modules', 'components', 'archive') for part in f.parts)]
print(f'Filtered HTML files count: {len(html_files)}')

missing_titles = []
missing_canonicals = []
missing_descriptions = []
missing_h1 = []
multiple_h1 = []
json_ld_types = {}
invalid_json_ld = []
titles = {}
canonicals = {}
descriptions = {}

for f in html_files:
    rel_path = f.as_posix()
    content = f.read_text(encoding='utf-8', errors='ignore')
    
    # Title
    m_title = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if not m_title or not m_title.group(1).strip():
        missing_titles.append(rel_path)
    else:
        titles[rel_path] = m_title.group(1).strip()
        
    # Canonical
    m_can = re.search(r'<link[^>]+rel=[\'"]canonical[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
    if not m_can:
        m_can = re.search(r'<link[^>]+href=[\'"]([^\'"]+)[\'"][^>]+rel=[\'"]canonical[\'"]', content, re.IGNORECASE)
    if not m_can:
        if '404.html' not in rel_path:
            missing_canonicals.append(rel_path)
    else:
        canonicals[rel_path] = m_can.group(1).strip()
        
    # Description
    m_desc = re.search(r'<meta[^>]+name=[\'"]description[\'"][^>]+content=[\'"]([^\'"]*)[\'"]', content, re.IGNORECASE)
    if not m_desc:
        m_desc = re.search(r'<meta[^>]+content=[\'"]([^\'"]*)[\'"][^>]+name=[\'"]description[\'"]', content, re.IGNORECASE)
    if not m_desc:
        if '404.html' not in rel_path:
            missing_descriptions.append(rel_path)
    else:
        descriptions[rel_path] = m_desc.group(1).strip()
        
    # H1
    h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if len(h1s) == 0:
        missing_h1.append(rel_path)
    elif len(h1s) > 1:
        multiple_h1.append((rel_path, len(h1s)))
        
    # JSON-LD
    json_lds = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
    for j_str in json_lds:
        try:
            data = json.loads(j_str.strip())
            stype = data.get('@type', 'Unknown')
            if isinstance(stype, list):
                stype = ', '.join(stype)
            json_ld_types[stype] = json_ld_types.get(stype, 0) + 1
        except Exception as e:
            invalid_json_ld.append((rel_path, str(e)))

print(f'Missing titles: {len(missing_titles)}')
if missing_titles:
    print(' ', missing_titles)
print(f'Missing canonicals: {len(missing_canonicals)}')
if missing_canonicals:
    print(' ', missing_canonicals)
print(f'Missing descriptions: {len(missing_descriptions)}')
if missing_descriptions:
    print(' ', missing_descriptions)
print(f'Missing H1: {len(missing_h1)}')
if missing_h1:
    print(' ', missing_h1)
print(f'Multiple H1: {len(multiple_h1)}')
print(f'Invalid JSON-LD: {len(invalid_json_ld)}')
print(f'JSON-LD type counts: {json_ld_types}')
