import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_PATH = ROOT_DIR / "data" / "topics.json"
TUTS_PATH = ROOT_DIR / "data" / "tutorials.json"

with open(TOPICS_PATH, "r", encoding="utf-8") as f:
    topics_data = json.load(f)

with open(TUTS_PATH, "r", encoding="utf-8") as f:
    tuts_data = json.load(f)

lines = []
lines.append(f"Total published in tutorials.json: {len(tuts_data)}")

audit_data = {}

for cat in topics_data["categories"][:6]:
    cname = cat["name"]
    cid = cat["id"]
    subtopics_all = []
    for s in cat.get("sections", []):
        subtopics_all.extend(s.get("subtopics", []))
    
    total = len(subtopics_all)
    pub = sum(1 for s in subtopics_all if s.get("status") == "published")
    plan = sum(1 for s in subtopics_all if s.get("status") == "planned")
    
    beg = sum(1 for s in subtopics_all if s.get("level") == "Beginner")
    inter = sum(1 for s in subtopics_all if s.get("level") == "Intermediate")
    adv = sum(1 for s in subtopics_all if s.get("level") == "Advanced")

    lines.append("\n" + "="*80)
    lines.append(f"CATEGORY: {cname} ({cid}) | Total: {total} | Published: {pub} | Planned: {plan}")
    lines.append(f"Levels: Beginner: {beg}, Intermediate: {inter}, Advanced: {adv}")
    lines.append("="*80)

    sec_stats = []
    for s_idx, sec in enumerate(cat.get("sections", [])):
        subs = sec.get("subtopics", [])
        stotal = len(subs)
        spub = sum(1 for s in subs if s.get("status") == "published")
        splan = sum(1 for s in subs if s.get("status") == "planned")
        ratio = spub / stotal if stotal > 0 else 0
        sec_stats.append({
            "index": s_idx,
            "name": sec["name"],
            "total": stotal,
            "published": spub,
            "planned": splan,
            "ratio": ratio,
            "subtopics": subs
        })
        lines.append(f"  Sec {s_idx+1:2d}: {sec['name']:<55} | Pub: {spub:2d}/{stotal:2d} ({ratio*100:5.1f}%) | Planned: {splan:2d}")

    zero_pub = [s for s in sec_stats if s["published"] == 0]
    one_pub = [s for s in sec_stats if s["published"] == 1]
    lines.append(f"\n  Sections with 0 published ({len(zero_pub)}): {[s['name'] for s in zero_pub]}")
    lines.append(f"  Sections with 1 published ({len(one_pub)}): {[s['name'] for s in one_pub]}")

    weakest = sorted(sec_stats, key=lambda s: (s["ratio"], -s["total"]))
    lines.append(f"  Weakest coverage sections:")
    for w in weakest[:5]:
        lines.append(f"    - {w['name']}: {w['published']}/{w['total']} ({w['ratio']*100:.1f}%) [planned: {w['planned']}]")

    audit_data[cid] = {
        "name": cname,
        "total": total,
        "published": pub,
        "planned": plan,
        "levels": {"Beginner": beg, "Intermediate": inter, "Advanced": adv},
        "sections": [{
            "name": s["name"],
            "total": s["total"],
            "published": s["published"],
            "planned": s["planned"],
            "ratio": s["ratio"]
        } for s in sec_stats],
        "zero_published": [s["name"] for s in zero_pub],
        "one_published": [s["name"] for s in one_pub]
    }

out_txt = Path(ROOT_DIR / "scripts" / "audit_summary.txt")
out_txt.write_text("\n".join(lines), encoding="utf-8")

out_json = Path(ROOT_DIR / "scripts" / "audit_results.json")
out_json.write_text(json.dumps(audit_data, indent=2), encoding="utf-8")
print(f"Wrote audit summary to {out_txt}")
