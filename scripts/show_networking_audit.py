import json
with open('data/topics.json', encoding='utf-8') as f:
    d = json.load(f)
c = d['categories'][0]
print(c['name'], 'Summary:')
for i, s in enumerate(c['sections']):
    pubs = sum(1 for t in s['subtopics'] if t.get('status') == 'published')
    plans = sum(1 for t in s['subtopics'] if t.get('status') != 'published')
    print(f"  Sec {i+1:2d} [{pubs} pub, {plans} plan]: {s['name']}")
