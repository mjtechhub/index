import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_PATH = ROOT_DIR / "data" / "topics.json"
TUTS_PATH = ROOT_DIR / "data" / "tutorials.json"

with open(TOPICS_PATH, "r", encoding="utf-8") as f:
    topics_data = json.load(f)

with open(TUTS_PATH, "r", encoding="utf-8") as f:
    tuts_data = json.load(f)

pub_ids = {t["id"]: t for t in tuts_data}

for cat in topics_data["categories"][:6]:
    cid = cat["id"]
    cname = cat["name"]
    print("\n" + "#"*80)
    print(f"ANALYSIS FOR CATEGORY: {cname} ({cid})")
    print("#"*80)
    
    sec_stats = []
    for s_idx, sec in enumerate(cat.get("sections", [])):
        subs = sec.get("subtopics", [])
        spub = sum(1 for s in subs if s.get("status") == "published")
        splan = sum(1 for s in subs if s.get("status") == "planned")
        stotal = len(subs)
        ratio = spub / stotal if stotal > 0 else 0
        planned_subs = [s for s in subs if s.get("status") == "planned"]
        sec_stats.append({
            "idx": s_idx + 1,
            "name": sec["name"],
            "total": stotal,
            "pub": spub,
            "plan": splan,
            "ratio": ratio,
            "planned_subs": planned_subs
        })
    
    # Sort sections by (pub_count == 0 desc, ratio asc, -total)
    sorted_secs = sorted(sec_stats, key=lambda s: (0 if s["pub"] == 0 else 1, s["ratio"], -s["total"]))
    for s in sorted_secs:
        zero_mark = " *** 0 PUBLISHED ***" if s["pub"] == 0 else ""
        print(f"Sec {s['idx']:2d}: {s['name']:<55} | Pub: {s['pub']:2d}/{s['total']:2d} ({s['ratio']*100:4.1f}%){zero_mark}")
        for p in s["planned_subs"]:
            print(f"    - [{p['level']:<12}] {p['id']:<55} | {p['name']}")
