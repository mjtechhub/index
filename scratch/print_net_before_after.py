import json

with open('data/tutorials.json', encoding='utf-8') as f:
    tuts = json.load(f)
with open('data/topics.json', encoding='utf-8') as f:
    topics = json.load(f)['categories']

net_cat = next(c for c in topics if c['id'] == 'networking')
net_tuts = [t for t in tuts if t['category'] == 'Networking']

mapping = []
for s in net_cat['sections']:
    sec_name = s['name']
    for sub in s['subtopics']:
        if sub.get('status') == 'published':
            tut_item = next(t for t in net_tuts if t['id'] == sub['id'])
            mapping.append({
                'id': sub['id'],
                'title': sub['name'],
                'section': sec_name,
                'url': sub['url'],
                'level': sub['level']
            })

with open('scratch/net_mapping_table.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=2)

print(f"Mapped {len(mapping)} networking tutorials across {len(net_cat['sections'])} sections.")
for s in net_cat['sections']:
    sec_pubs = [sub for sub in s['subtopics'] if sub.get('status') == 'published']
    print(f"- {s['name']}: {len(sec_pubs)} published tutorials")
