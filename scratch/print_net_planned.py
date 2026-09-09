import json

with open('data/topics.json', encoding='utf-8') as f:
    topics = json.load(f)['categories']

net = next(c for c in topics if c['id'] == 'networking')
print(f"Total planned in networking: {sum(1 for s in net['sections'] for sub in s['subtopics'] if sub.get('status') == 'planned')}")
for s in net['sections']:
    sec_planned = [sub for sub in s['subtopics'] if sub.get('status') == 'planned']
    if sec_planned:
        print(f"\n[{s['name']}]")
        for sub in sec_planned:
            print(f"  id='{sub['id']}' | name='{sub['name']}' | level='{sub['level']}'")
