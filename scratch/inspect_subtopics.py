import json
from pathlib import Path

repo = Path('.')

with open(repo / 'data' / 'topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

for cat in topics.get('categories', []):
    if cat.get('id') in ['windows', 'linux', 'servers', 'cybersecurity', 'cloud']:
        print(f"\n=== {cat.get('name')} ({cat.get('id')}) ===")
        for sec in cat.get('sections', []):
            print(f"  Section: {sec.get('name')}")
            for sub in sec.get('subtopics', []):
                print(f"    - {sub.get('name')} | id: {sub.get('id')} | url: {sub.get('url')} | level: {sub.get('level')} | keys: {list(sub.keys())}")
