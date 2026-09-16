#!/usr/bin/env python3
"""
MJ Tech Hub - Canonical Sitemap Generator
Generates a complete, standard sitemap.xml for all canonical, indexable production URLs:
- Homepage
- Core pages (About, Topics, Commands, Quizzes, Resources, Tools, Labs)
- 6 Category pages (Networking, Windows, Linux, Servers, Cybersecurity, Cloud)
- 4 Interactive Tools
- 3 Legal pages (Privacy, Terms, Disclaimer)
- 148 Published Tutorials with reliable lastmod dates from data/tutorials.json

Excludes:
- 404.html (marked noindex)
- tools/editor.html (internal editor, marked noindex)
- Planned curriculum topics without dedicated pages
- Query-string or hash variants
"""

import json
import os
from pathlib import Path
import xml.dom.minidom

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://themjtechhub.site"

def generate_sitemap():
    # 1. Core Pages
    core_pages = [
        {"loc": f"{BASE_URL}/", "lastmod": None},
        {"loc": f"{BASE_URL}/about.html", "lastmod": None},
        {"loc": f"{BASE_URL}/topics.html", "lastmod": None},
        {"loc": f"{BASE_URL}/commands.html", "lastmod": None},
        {"loc": f"{BASE_URL}/quiz.html", "lastmod": None},
        {"loc": f"{BASE_URL}/resources.html", "lastmod": None},
        {"loc": f"{BASE_URL}/tools.html", "lastmod": None},
        {"loc": f"{BASE_URL}/labs.html", "lastmod": None},
    ]

    # 2. Category Pages
    category_pages = [
        {"loc": f"{BASE_URL}/networking.html", "lastmod": None},
        {"loc": f"{BASE_URL}/windows.html", "lastmod": None},
        {"loc": f"{BASE_URL}/linux.html", "lastmod": None},
        {"loc": f"{BASE_URL}/servers.html", "lastmod": None},
        {"loc": f"{BASE_URL}/cybersecurity.html", "lastmod": None},
        {"loc": f"{BASE_URL}/cloud.html", "lastmod": None},
    ]

    # 3. Interactive Tools
    tool_pages = [
        {"loc": f"{BASE_URL}/tools/subnet-calculator.html", "lastmod": None},
        {"loc": f"{BASE_URL}/tools/vlsm-planner.html", "lastmod": None},
        {"loc": f"{BASE_URL}/tools/network-diagnostic-workbench.html", "lastmod": None},
        {"loc": f"{BASE_URL}/tools/port-reference.html", "lastmod": None},
    ]

    # 4. Legal Pages
    legal_pages = [
        {"loc": f"{BASE_URL}/legal/privacy.html", "lastmod": None},
        {"loc": f"{BASE_URL}/legal/terms.html", "lastmod": None},
        {"loc": f"{BASE_URL}/legal/disclaimer.html", "lastmod": None},
    ]

    # 5. Published Tutorials from data/tutorials.json
    tut_file = REPO_ROOT / "data" / "tutorials.json"
    with open(tut_file, "r", encoding="utf-8") as f:
        tutorials = json.load(f)

    tutorial_pages = []
    for tut in tutorials:
        tut_url = tut.get("url", "").replace("./", "")
        # Verify file exists
        local_path = REPO_ROOT / tut_url
        if not local_path.exists():
            raise FileNotFoundError(f"Tutorial file not found: {local_path}")

        # Reliable date from updatedAt or publishedAt
        date_str = tut.get("updatedAt") or tut.get("publishedAt")
        tutorial_pages.append({
            "loc": f"{BASE_URL}/{tut_url}",
            "lastmod": date_str if date_str else None
        })

    all_entries = core_pages + category_pages + tool_pages + legal_pages + tutorial_pages

    # Deduplicate while preserving order
    seen = set()
    unique_entries = []
    for entry in all_entries:
        if entry["loc"] not in seen:
            seen.add(entry["loc"])
            unique_entries.append(entry)

    # Build XML
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for e in unique_entries:
        lines.append('  <url>')
        lines.append(f'    <loc>{e["loc"]}</loc>')
        if e.get("lastmod"):
            lines.append(f'    <lastmod>{e["lastmod"]}</lastmod>')
        lines.append('  </url>')
    lines.append('</urlset>')
    lines.append('')

    output_path = REPO_ROOT / "sitemap.xml"
    content = '\n'.join(lines)
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    print(f"Generated {output_path.name} with {len(unique_entries)} URLs ({len(tutorial_pages)} tutorials with lastmod).")
    return len(unique_entries)

if __name__ == "__main__":
    generate_sitemap()
