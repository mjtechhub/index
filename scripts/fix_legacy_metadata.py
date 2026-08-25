import json
import os
import re

tut_dir = r"c:\xampp\htdocs\index\tutorials\networking"
json_path = r"c:\xampp\htdocs\index\data\tutorials.json"

with open(json_path, 'r', encoding='utf-8') as f:
    tuts = json.load(f)

existing_ids = {t['id'] for t in tuts}

# Fix VLAN Title
for t in tuts:
    if t['id'] == 'what-is-vlan':
        t['title'] = 'What Is VLAN?'

missing_files = [
    "lan-vs-wan.html",
    "ping-explained.html",
    "public-vs-private-ip-address.html",
    "traceroute-explained.html",
    "what-is-a-computer-network.html",
    "what-is-a-default-gateway.html",
    "what-is-an-ip-address.html",
    "what-is-dhcp.html"
]

added_count = 0

for fname in missing_files:
    tut_id = fname.replace('.html', '')
    if tut_id in existing_ids:
        continue
        
    filepath = os.path.join(tut_dir, fname)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Extract metadata
    title_match = re.search(r'<h1.*?>(.*?)</h1>', html)
    title = title_match.group(1).strip() if title_match else tut_id.replace('-', ' ').title()
    
    level_match = re.search(r'fa-signal.*?</i>\s*(.*?)</span>', html)
    level = level_match.group(1).strip() if level_match else "Beginner"
    
    time_match = re.search(r'fa-clock.*?</i>\s*(.*?)</span>', html)
    readTime = time_match.group(1).strip() if time_match else "5 min read"
    
    desc_match = re.search(r'<p>(.*?)</p>', html)
    desc = desc_match.group(1).strip() if desc_match else title
    # Strip HTML from description if any
    desc = re.sub(r'<[^>]+>', '', desc)
    
    new_entry = {
        "id": tut_id,
        "title": title,
        "description": desc[:150] + ("..." if len(desc) > 150 else ""),
        "category": "Networking",
        "level": level,
        "readTime": readTime,
        "keywords": "networking, " + tut_id.replace('-', ' '),
        "url": f"tutorials/networking/{fname}",
        "publishedAt": "2026-08-01",  # Use a date older than today to preserve Latest Tutorials sort
        "updatedAt": "2026-08-01"
    }
    tuts.append(new_entry)
    added_count += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(tuts, f, indent=4)

print(f"Legacy records added: {added_count}")
