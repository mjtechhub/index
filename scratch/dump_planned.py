import json

with open('data/topics.json', encoding='utf-8') as f:
    topics = json.load(f)['categories']

def dump_cat(cat_id):
    cat = next(c for c in topics if c['id'] == cat_id)
    print(f"=== {cat['name']} ({cat_id}) ===")
    for s in cat['sections']:
        print(f"[{s['name']}]")
        for sub in s['subtopics']:
            if sub.get('status') == 'planned':
                print(f"  id='{sub['id']}' | name='{sub['name']}' | level='{sub['level']}'")

dump_cat('linux')
dump_cat('servers')
dump_cat('cybersecurity')
dump_cat('cloud')
dump_cat('windows')
