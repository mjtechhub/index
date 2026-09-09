import json
from pathlib import Path

with open('data/topics.json', encoding='utf-8') as f:
    d = json.load(f)

with open('scripts/planned_topics.txt', 'w', encoding='utf-8') as out:
    for cat in d['categories'][:6]:
        out.write("=" * 60 + "\n")
        out.write(f"CATEGORY: {cat['name']} ({cat['id']})\n")
        out.write("=" * 60 + "\n")
        for s_idx, sec in enumerate(cat['sections']):
            subtopics = sec.get('subtopics', [])
            pub_count = sum(1 for s in subtopics if s.get('status') == 'published')
            planned = [s for s in subtopics if s.get('status') != 'published']
            out.write(f"\n--- Sec {s_idx+1}: {sec['name']} (Pub: {pub_count}, Planned: {len(planned)}) ---\n")
            for p in planned:
                out.write(f"    [{p['level']}] id: '{p['id']}' | title: '{p['name']}'\n")
