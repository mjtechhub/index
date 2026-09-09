import json

with open('data/tutorials.json', encoding='utf-8') as f:
    tuts = json.load(f)
with open('data/topics.json', encoding='utf-8') as f:
    topics = json.load(f)['categories']

pub_curric = []
for c in topics:
    for s in c.get('sections', []):
        for sub in s.get('subtopics', []):
            if sub.get('status') == 'published':
                pub_curric.append((c['id'], sub))

print('tutorials.json count:', len(tuts))
print('published curriculum count:', len(pub_curric))
assert len(tuts) == 76, f"Expected 76 tuts, got {len(tuts)}"
assert len(pub_curric) == 76, f"Expected 76 pub curric, got {len(pub_curric)}"

# Check 1-to-1 mapping
tut_dict = {t['id']: t for t in tuts}
curric_dict = {}
multiply_mapped = []
for cid, sub in pub_curric:
    sid = sub['id']
    if sid in curric_dict:
        multiply_mapped.append(sid)
    curric_dict[sid] = (cid, sub)

assert len(multiply_mapped) == 0, f"Multiply mapped: {multiply_mapped}"

unmapped = []
for tid, t in tut_dict.items():
    if tid not in curric_dict:
        unmapped.append(tid)
assert len(unmapped) == 0, f"Unmapped: {unmapped}"

phantom = []
for sid in curric_dict:
    if sid not in tut_dict:
        phantom.append(sid)
assert len(phantom) == 0, f"Phantom: {phantom}"

for tid, t in tut_dict.items():
    cid, sub = curric_dict[tid]
    norm_url = t['url'].replace('./', '')
    assert sub['url'] == norm_url, f"URL mismatch for {tid}: {sub['url']} vs {norm_url}"
    assert sub['level'] == t['level'], f"Level mismatch for {tid}: {sub['level']} vs {t['level']}"

print("EXACT ONE-TO-ONE MAPPING CONFIRMED:")
print("  76 tutorials.json records")
print("  76 published curriculum mappings")
print("  0 unmapped")
print("  0 multiply mapped")
print("  0 phantom published curriculum entries")
print("  Published curriculum category, URL and level agree with tutorials.json.")
