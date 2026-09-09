#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6 Tutorial Migration Script (scripts/migrate_phase6_tutorials.py)
Standardizes all 61 published tutorials with:
- Static SEO metadata (unique title, description, canonical, OG article, Twitter, TechArticle JSON-LD)
- Canonical domain origin: https://themjtechhub.site (from CNAME)
- Accessible Skip Link
- Standardized hero with breadcrumbs, metadata, and exactly one H1
- Two-column technical reading layout (article column max-width 72ch + sticky TOC aside)
- Normalization of legacy monospace divs to <div class="tutorial-command">
- Removal of legacy inline navigation blocks
- Clean script loading and toast markup
- Fully idempotent and supports --dry-run
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TUTS_DIR = ROOT_DIR / "tutorials" / "networking"
TUTS_JSON_PATH = ROOT_DIR / "data" / "tutorials.json"
CANONICAL_DOMAIN = "https://themjtechhub.site"

def parse_date(date_str):
    if not date_str or date_str == "UNKNOWN":
        return datetime.today().strftime("%b %d, %Y")
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return date_str

def extract_lesson_content(html_str):
    """
    Extracts the inner HTML of the lesson content, removing any legacy
    navigation blocks at the bottom, and normalizes legacy monospace divs.
    Supports both legacy markup and already modernized Phase 6 markup.
    """
    # 1. Check if already modernized with <article class="tutorial-article content lesson-content">
    match = re.search(r'<article class="tutorial-article content lesson-content"[^>]*>([\s\S]*?)</article>', html_str, re.IGNORECASE)
    if match:
        raw_body = match.group(1).strip()
    else:
        # Match content between <div class="content lesson-content"...> and the closing tag
        # Some files have an extra </div> due to legacy generator issues
        match = re.search(r'<div class="content lesson-content"[^>]*>([\s\S]*?)</div>\s*(?:</div>)?\s*<!-- Navigation -->', html_str, re.IGNORECASE)
        if not match:
            # Fallback search before </main>
            match = re.search(r'<div class="content lesson-content"[^>]*>([\s\S]*?)(?:<!-- Navigation -->|<div style="display: flex; justify-content: space-between"|</main>)', html_str, re.IGNORECASE)

        if match:
            raw_body = match.group(1).strip()
        else:
            # Emergency fallback: match inner content
            m2 = re.search(r'<div class="content lesson-content"[^>]*>([\s\S]*?)</div>\s*</main>', html_str, re.IGNORECASE)
            raw_body = m2.group(1).strip() if m2 else ""

        # Remove any trailing extra closing tags or legacy navigation
        raw_body = re.sub(r'</div>\s*<!-- Navigation -->[\s\S]*$', '', raw_body, flags=re.IGNORECASE)
        raw_body = re.sub(r'<!-- Navigation -->[\s\S]*$', '', raw_body, flags=re.IGNORECASE)
        raw_body = re.sub(r'<div style="display:\s*flex;\s*justify-content:\s*space-between[\s\S]*?</div>', '', raw_body, flags=re.IGNORECASE)

    # 2. Normalize legacy monospace divs to <div class="tutorial-command">
    # Legacy pattern: <div style="...font-family: monospace;...">
    def normalize_mono(m):
        inner_code = m.group(1)
        return f'<div class="tutorial-command">{inner_code}</div>'

    raw_body = re.sub(
        r'<div[^>]*style="[^"]*font-family:\s*monospace[^"]*"[^>]*>([\s\S]*?)</div>',
        normalize_mono,
        raw_body,
        flags=re.IGNORECASE
    )

    return raw_body.strip()

def build_modern_tutorial_html(tut, filename, body_content):
    title = tut.get("title", "")
    desc = tut.get("description", "")
    category = tut.get("category", "Networking")
    level = tut.get("level", "Beginner")
    level_class = level.lower()
    read_time = tut.get("readTime", "5 min read")
    pub_date = tut.get("publishedAt", "2026-08-25")
    upd_date = tut.get("updatedAt", pub_date)
    formatted_date = parse_date(upd_date)

    canonical_url = f"{CANONICAL_DOMAIN}/tutorials/networking/{filename}"

    # TechArticle JSON-LD structured data
    json_ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": desc,
        "url": canonical_url,
        "datePublished": pub_date,
        "dateModified": upd_date,
        "proficiencyLevel": level,
        "author": {
            "@type": "Organization",
            "name": "MJ Tech Hub",
            "url": CANONICAL_DOMAIN
        },
        "publisher": {
            "@type": "Organization",
            "name": "MJ Tech Hub",
            "url": CANONICAL_DOMAIN,
            "logo": {
                "@type": "ImageObject",
                "url": f"{CANONICAL_DOMAIN}/assets/logo/mj-tech-hub-logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        }
    }
    json_ld_str = json.dumps(json_ld, indent=4)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <script src="../../js/theme-init.js"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {category} Tutorial | MJ Tech Hub</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph -->
    <meta property="og:title" content="{title} | {category} Tutorial | MJ Tech Hub">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="MJ Tech Hub">
    <meta property="og:type" content="article">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title} | {category} Tutorial | MJ Tech Hub">
    <meta name="twitter:description" content="{desc}">

    <!-- Schema.org TechArticle JSON-LD -->
    <script type="application/ld+json">
{json_ld_str}
    </script>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../../css/themes.css">
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/responsive.css">
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <div id="site-header"></div>

    <main id="main-content" class="container py-4">
        <!-- Tutorial Hero Header -->
        <header id="tutorial-header" class="tutorial-hero">
            <nav aria-label="Breadcrumb" class="breadcrumb" style="margin-bottom: var(--space-4);">
                <a href="../../index.html">Home</a>
                <span class="breadcrumb-separator" aria-hidden="true">/</span>
                <a href="../../topics.html">Topics</a>
                <span class="breadcrumb-separator" aria-hidden="true">/</span>
                <a href="../../networking.html">{category}</a>
                <span class="breadcrumb-separator" aria-hidden="true">/</span>
                <span aria-current="page">{title}</span>
            </nav>

            <div class="tutorial-meta-row">
                <span class="cat-tut-badge {level_class}">{level}</span>
                <span class="tutorial-meta-item"><i class="fa-regular fa-clock" aria-hidden="true"></i> {read_time}</span>
                <span class="tutorial-meta-item"><i class="fa-regular fa-calendar" aria-hidden="true"></i> Updated: {formatted_date}</span>
            </div>

            <h1 class="tutorial-hero-title">{title}</h1>
            <p class="tutorial-hero-desc">{desc}</p>
        </header>

        <!-- Technical Reading Layout (Main Article + Sticky TOC) -->
        <div class="tutorial-reading-layout">
            <article class="tutorial-article content lesson-content">
{body_content}
            </article>

            <!-- Sticky Table of Contents Sidebar -->
            <aside class="tutorial-sidebar" aria-label="Table of Contents">
                <nav id="tutorial-toc" class="tutorial-toc">
                    <!-- Populated dynamically by tutorial.js -->
                </nav>
            </aside>
        </div>

        <!-- Dynamic Navigation Mount (Previous/Next, Back to Category, Related Tutorials) -->
        <div id="tutorial-footer-mount"></div>
    </main>

    <!-- Accessible Toast for Code Copy Feedback -->
    <div id="copy-toast" class="sr-toast" role="status" aria-live="polite">
        <i class="fa-solid fa-check text-success" aria-hidden="true"></i>
        <span id="copy-toast-msg">Code copied to clipboard!</span>
    </div>

    <div id="site-footer"></div>
    <script src="../../js/components.js"></script>
    <script src="../../js/tutorial.js" defer></script>
    <script src="../../js/main.js"></script>
    <script src="../../js/theme.js"></script>
</body>
</html>
"""

def migrate_tutorials(dry_run=False):
    print("=" * 68)
    print(f"MJ Tech Hub Phase 6 Tutorial Migration {'(DRY RUN)' if dry_run else '(LIVE RUN)'}")
    print("=" * 68)

    with open(TUTS_JSON_PATH, "r", encoding="utf-8") as f:
        tutorials_data = json.load(f)

    meta_by_filename = {}
    for item in tutorials_data:
        fname = Path(item["url"]).name
        meta_by_filename[fname] = item

    tutorial_files = sorted(list(TUTS_DIR.glob("*.html")))

    files_scanned = len(tutorial_files)
    files_changed = 0
    files_unchanged = 0
    errors = 0

    for fpath in tutorial_files:
        filename = fpath.name
        tut_meta = meta_by_filename.get(filename)

        if not tut_meta:
            print(f"[ERROR] No metadata found in tutorials.json for: {filename}")
            errors += 1
            continue

        try:
            current_content = fpath.read_text(encoding="utf-8")
            body_content = extract_lesson_content(current_content)

            if not body_content:
                print(f"[ERROR] Failed to extract lesson body for: {filename}")
                errors += 1
                continue

            new_html = build_modern_tutorial_html(tut_meta, filename, body_content)

            if current_content.strip() == new_html.strip():
                files_unchanged += 1
            else:
                files_changed += 1
                if not dry_run:
                    fpath.write_text(new_html, encoding="utf-8")
        except Exception as ex:
            print(f"[ERROR] Exception processing {filename}: {ex}")
            errors += 1

    print("\n" + "=" * 68)
    print("MIGRATION SUMMARY:")
    print(f"  Files scanned  : {files_scanned}")
    print(f"  Files changed  : {files_changed}")
    print(f"  Files unchanged: {files_unchanged}")
    print(f"  Errors         : {errors}")
    print("=" * 68)

    return errors == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 6 Tutorial Migration Script")
    parser.add_argument("--dry-run", action="store_true", help="Perform a trial run without making changes")
    args = parser.parse_args()

    success = migrate_tutorials(dry_run=args.dry_run)
    exit(0 if success else 1)
