import json
from pathlib import Path

repo = Path('.')

with open(repo / 'data' / 'tutorials.json', 'r', encoding='utf-8') as f:
    tuts = json.load(f)

for c in ['Windows', 'Linux', 'Servers', 'Cybersecurity', 'Cloud & AI']:
    cat_tuts = [t for t in tuts if t['category'] == c]
    print(f"\nCategory: {c} ({len(cat_tuts)} tutorials)")
    for t in cat_tuts:
        print(f"  id='{t['id']}' | title='{t['title']}' | level='{t['level']}' | url='{t['url']}'")
