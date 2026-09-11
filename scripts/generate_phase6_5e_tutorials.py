#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6.5E Batch 5 Tutorial Generator & Master Curriculum Synchronization
(scripts/generate_phase6_5e_tutorials.py)

Generates 18 new tutorials (3 per core category) across:
- Networking (70 -> 73)
- Windows (12 -> 15)
- Linux (12 -> 15)
- Servers (12 -> 15)
- Cybersecurity (12 -> 15)
- Cloud & AI (12 -> 15)
Total Published Tutorials: 130 -> 148

Adheres to:
- Reuses canonical renderer (scripts/tutorial_renderer.py)
- Category-contiguous ordering in data/tutorials.json:
  [Networking 73] -> [Windows 15] -> [Linux 15] -> [Servers 15] -> [Cybersecurity 15] -> [Cloud 15] = 148 total
- Master curriculum update in data/topics.json (planned -> published)
- Idempotency on multiple executions (0 duplicates, 0 timestamp drift)
- Word-count validation (800-1400 typical, >= 600 minimum)
"""

import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
TUTS_JSON_PATH = DATA_DIR / "tutorials.json"
TOPICS_JSON_PATH = DATA_DIR / "topics.json"
PUBLISH_DATE = "2026-09-11"

# Add scripts directory to sys.path for local module imports
sys.path.insert(0, str(ROOT_DIR / "scripts"))
from tutorial_renderer import build_tutorial_html, calculate_word_count, calculate_read_time
from content.batch5_networking import NETWORKING_TUTORIALS
from content.batch5_windows import WINDOWS_TUTORIALS
from content.batch5_linux import LINUX_TUTORIALS
from content.batch5_servers import SERVERS_TUTORIALS
from content.batch5_cybersecurity import CYBERSECURITY_TUTORIALS
from content.batch5_cloud import CLOUD_TUTORIALS

ALL_BATCH5_TUTORIALS = [
    ("networking", "networking.html", NETWORKING_TUTORIALS),
    ("windows", "windows.html", WINDOWS_TUTORIALS),
    ("linux", "linux.html", LINUX_TUTORIALS),
    ("servers", "servers.html", SERVERS_TUTORIALS),
    ("cybersecurity", "cybersecurity.html", CYBERSECURITY_TUTORIALS),
    ("cloud", "cloud.html", CLOUD_TUTORIALS)
]

def run_batch5_generation():
    print("==================================================")
    print("PHASE 6.5E BATCH 5 GENERATION & AUDIT")
    print("==================================================")

    # 1. Load existing data
    with open(TUTS_JSON_PATH, "r", encoding="utf-8") as f:
        existing_tuts = json.load(f)
    
    with open(TOPICS_JSON_PATH, "r", encoding="utf-8") as f:
        topics_data = json.load(f)

    existing_tut_map = {t["id"]: t for t in existing_tuts}
    print(f"Loaded {len(existing_tuts)} existing tutorials from tutorials.json")
    print(f"Loaded {len(topics_data['categories'])} categories from topics.json")

    # 2. Word Count & Content Audit
    print("\n--- Auditing Word Counts & Read Times ---")
    total_batch_tutorials = 0
    for cat_dir, cat_page, tut_list in ALL_BATCH5_TUTORIALS:
        for tut in tut_list:
            total_batch_tutorials += 1
            words = calculate_word_count(tut["html"])
            calc_rt = calculate_read_time(tut["html"])
            print(f"[{tut['category']}] {tut['title']}: {words} words -> {calc_rt}")
            assert words >= 600, f"Tutorial '{tut['id']}' word count too low ({words} words)!"
            # Synchronize verified readTime
            tut["readTime"] = calc_rt

    assert total_batch_tutorials == 18, f"Expected 18 tutorials, got {total_batch_tutorials}!"

    # 3. Generate HTML Files (Idempotent)
    print("\n--- Generating Tutorial HTML Pages ---")
    files_created = 0
    files_updated = 0
    files_unchanged = 0

    for cat_dir, cat_page, tut_list in ALL_BATCH5_TUTORIALS:
        target_dir = ROOT_DIR / "tutorials" / cat_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        for tut in tut_list:
            tid = tut["id"]
            target_file = target_dir / f"{tid}.html"
            
            # Preserve existing publishedAt if already present
            existing_rec = existing_tut_map.get(tid)
            pub_date = existing_rec["publishedAt"] if existing_rec else PUBLISH_DATE
            up_date = existing_rec["updatedAt"] if existing_rec else PUBLISH_DATE

            tut["publishedAt"] = pub_date
            tut["updatedAt"] = up_date

            rendered_html = build_tutorial_html(
                tut=tut,
                cat_dir=cat_dir,
                cat_page=cat_page,
                publish_date=pub_date,
                update_date=up_date
            )

            if not target_file.exists():
                target_file.write_text(rendered_html, encoding="utf-8")
                files_created += 1
            else:
                current_html = target_file.read_text(encoding="utf-8")
                if current_html != rendered_html:
                    target_file.write_text(rendered_html, encoding="utf-8")
                    files_updated += 1
                else:
                    files_unchanged += 1

    print(f"HTML Generation Summary: {files_created} created, {files_updated} updated, {files_unchanged} unchanged.")

    # 4. Structure Category-Contiguous tutorials.json
    print("\n--- Structuring Category-Contiguous tutorials.json ---")
    category_order = [
        "Networking",
        "Windows",
        "Linux",
        "Servers",
        "Cybersecurity",
        "Cloud & AI"
    ]

    buckets = {cat: [] for cat in category_order}
    for t in existing_tuts:
        cat = t["category"]
        if cat in buckets:
            buckets[cat].append(t)
        else:
            raise ValueError(f"Unknown category in tutorials.json: {cat}")

    new_records_added = 0
    for cat_dir, cat_page, tut_list in ALL_BATCH5_TUTORIALS:
        for tut in tut_list:
            cat_name = tut["category"]
            tid = tut["id"]
            cat_bucket = buckets[cat_name]

            existing_in_bucket = next((t for t in cat_bucket if t["id"] == tid), None)
            if not existing_in_bucket:
                new_record = {
                    "id": tid,
                    "title": tut["title"],
                    "description": tut["description"],
                    "category": tut["category"],
                    "level": tut["level"],
                    "readTime": tut["readTime"],
                    "keywords": tut["keywords"],
                    "url": f"tutorials/{cat_dir}/{tid}.html",
                    "publishedAt": PUBLISH_DATE,
                    "updatedAt": PUBLISH_DATE
                }
                cat_bucket.append(new_record)
                new_records_added += 1
            else:
                # Synchronize updated metadata (e.g. aligned level/title)
                existing_in_bucket["level"] = tut["level"]
                existing_in_bucket["title"] = tut["title"]
                existing_in_bucket["description"] = tut["description"]
                existing_in_bucket["readTime"] = tut["readTime"]
                existing_in_bucket["keywords"] = tut["keywords"]

    # Reconstruct category-contiguous array
    final_tutorials = []
    for cat in category_order:
        final_tutorials.extend(buckets[cat])

    print(f"Added {new_records_added} new records to tutorials.json")
    print(f"Final tutorials count: {len(final_tutorials)}")

    # Category counts validation
    for cat in category_order:
        count = sum(1 for t in final_tutorials if t["category"] == cat)
        print(f"  - {cat}: {count} tutorials")

    assert len(final_tutorials) == 148, f"Expected 148 tutorials, got {len(final_tutorials)}!"

    with open(TUTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(final_tutorials, f, indent=4)

    # 5. Update Master Curriculum in topics.json
    print("\n--- Updating Master Curriculum in topics.json ---")
    all_batch5_dict = {}
    for cat_dir, cat_page, tut_list in ALL_BATCH5_TUTORIALS:
        for tut in tut_list:
            all_batch5_dict[tut["id"]] = (cat_dir, tut)

    curriculum_updated = 0
    for cat in topics_data["categories"]:
        cid = cat["id"]
        for sec in cat.get("sections", []):
            for sub in sec.get("subtopics", []):
                sid = sub["id"]
                if sid in all_batch5_dict:
                    cat_dir, tut = all_batch5_dict[sid]
                    if sub.get("status") != "published" or sub.get("url") != f"tutorials/{cat_dir}/{sid}.html" or sub.get("name") != tut["title"]:
                        sub["status"] = "published"
                        sub["url"] = f"tutorials/{cat_dir}/{sid}.html"
                        sub["name"] = tut["title"]  # Synchronize refined title
                        curriculum_updated += 1

    print(f"Curriculum records updated to 'published': {curriculum_updated}")

    with open(TOPICS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(topics_data, f, indent=4)

    # 6. Verify Master Curriculum Totals
    total_curric = 0
    pub_curric = 0
    plan_curric = 0
    for cat in topics_data["categories"]:
        for sec in cat.get("sections", []):
            for sub in sec.get("subtopics", []):
                total_curric += 1
                if sub.get("status") == "published":
                    pub_curric += 1
                elif sub.get("status") == "planned":
                    plan_curric += 1

    print("\n--- Final Integrity Verification ---")
    print(f"Total Curriculum Topics: {total_curric}")
    print(f"Published Curriculum:    {pub_curric}")
    print(f"Planned Curriculum:      {plan_curric}")

    assert total_curric == 471, f"Expected 471 curriculum topics, got {total_curric}!"
    assert pub_curric == 148, f"Expected 148 published curriculum topics, got {pub_curric}!"
    assert plan_curric == 323, f"Expected 323 planned curriculum topics, got {plan_curric}!"

    print("\nSUCCESS: Phase 6.5E Batch 5 Generation Complete!")

if __name__ == "__main__":
    run_batch5_generation()
