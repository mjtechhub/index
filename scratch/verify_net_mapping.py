import json
from pathlib import Path

repo = Path('.')

with open(repo / 'data' / 'tutorials.json', 'r', encoding='utf-8') as f:
    tuts = json.load(f)

with open(repo / 'data' / 'topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

net_cat = next(c for c in topics['categories'] if c['id'] == 'networking')

# Current sections in topics.json
current_mapping = {}
for s in net_cat['sections']:
    sname = s['name']
    for sub in s['subtopics']:
        if sub['status'] == 'published':
            current_mapping[sub['id']] = {
                'name': sub['name'],
                'section': sname,
                'url': sub['url'],
                'level': sub['level']
            }

print(f"Total published networking tutorials mapped: {len(current_mapping)}")
assert len(current_mapping) == 61, f"Expected 61, got {len(current_mapping)}"

# Verify against tutorials.json
net_tuts = [t for t in tuts if t['category'] == 'Networking']
print(f"Total networking tutorials in tutorials.json: {len(net_tuts)}")
assert len(net_tuts) == 61

for t in net_tuts:
    tid = t['id']
    assert tid in current_mapping, f"Missing {tid} in current mapping!"
    m = current_mapping[tid]
    assert m['url'] == t['url'].replace('./', ''), f"URL mismatch for {tid}"
    assert m['level'] == t['level'], f"Level mismatch for {tid}"

print("All 61 Networking tutorials verified with exact ID, URL, and level!")
