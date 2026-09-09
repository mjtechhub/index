import json
from pathlib import Path

repo = Path('.')

with open(repo / 'data' / 'topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

with open(repo / 'data' / 'tutorials.json', 'r', encoding='utf-8') as f:
    tutorials = json.load(f)

with open(repo / 'data' / 'commands.json', 'r', encoding='utf-8') as f:
    commands = json.load(f)

with open(repo / 'data' / 'resources.json', 'r', encoding='utf-8') as f:
    resources = json.load(f)

print("=== DATA AUDIT ===")
print(f"Total Tutorials: {len(tutorials)}")
print(f"Total Commands: {len(commands)}")
print(f"Total Resources: {len(resources)}")

quiz_files = list(repo.glob("*quiz*")) + list((repo / "data").glob("*quiz*"))
print(f"Quiz files found: {[str(p) for p in quiz_files]}")

# Check quiz data in js/quiz.js or data
for qp in [repo / "data" / "quizzes.json", repo / "js" / "quiz.js", repo / "quiz.html"]:
    if qp.exists():
        print(f"Found {qp}")

# Tutorials per category in tutorials.json
tut_by_cat = {}
tut_urls = set()
for t in tutorials:
    c = t.get('category', 'Unknown')
    tut_by_cat[c] = tut_by_cat.get(c, 0) + 1
    tut_urls.add(t.get('url'))

print("\nTutorials in tutorials.json by category:")
for c, cnt in sorted(tut_by_cat.items()):
    print(f"  {c}: {cnt}")

print("\n=== TOPICS.JSON BREAKDOWN ===")
total_subtopics_all = 0
for cat in topics.get('categories', []):
    cid = cat.get('id')
    cname = cat.get('name')
    ctype = cat.get('type')
    sections = cat.get('sections', [])
    num_sections = len(sections)
    total_subs = sum(len(s.get('subtopics', [])) for s in sections)
    total_subtopics_all += total_subs
    print(f"\nCategory: id='{cid}', name='{cname}', type='{ctype}'")
    print(f"  Sections count: {num_sections}")
    print(f"  Total subtopics: {total_subs}")
    for s_idx, s in enumerate(sections):
        s_name = s.get('name') or s.get('title')
        subs = s.get('subtopics', [])
        pub_in_sec = sum(1 for sub in subs if sub.get('url') in tut_urls)
        print(f"    Sec {s_idx+1}: '{s_name}' ({len(subs)} subtopics, {pub_in_sec} published match)")

print(f"\nTotal subtopics across all categories: {total_subtopics_all}")
