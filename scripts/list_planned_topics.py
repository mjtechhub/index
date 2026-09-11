import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_PATH = ROOT_DIR / "data" / "topics.json"

with open(TOPICS_PATH, "r", encoding="utf-8") as f:
    topics_data = json.load(f)

for cat in topics_data["categories"][:6]:
    cname = cat["name"]
    cid = cat["id"]
    print("\n" + "="*90)
    print(f"PLANNED TOPICS FOR CATEGORY: {cname} ({cid})")
    print("="*90)
    for s_idx, sec in enumerate(cat.get("sections", [])):
        subs = sec.get("subtopics", [])
        spub = sum(1 for s in subs if s.get("status") == "published")
        stotal = len(subs)
        planned = [s for s in subs if s.get("status") == "planned"]
        if not planned:
            continue
        print(f"\n--- Section {s_idx+1}: {sec['name']} (Published: {spub}/{stotal}, Planned: {len(planned)}) ---")
        for p in planned:
            print(f"  [{p['level']:<12}] ID: {p['id']:<50} | Name: {p['name']}")
