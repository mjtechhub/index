#!/usr/bin/env python3
"""
MJ Tech Hub - Canonical Tutorial HTML Renderer (scripts/tutorial_renderer.py)

Single authoritative rendering engine for all tutorial pages on MJ Tech Hub.
Used by Phase 6.5, Phase 6.5B, and all future publication batches.
Ensures 100% adherence to:
- Static SEO & TechArticle JSON-LD with canonical domain https://themjtechhub.site
- Standardized Phase 6 reader layout: Breadcrumb, Hero metadata, 72ch reading column
- Responsive sticky Table of Contents (TOC)
- Accessible Code Copy buttons & feedback toasts
- Semantic callouts & responsive tables
- Dynamic Prev/Next, Related Tutorials, and Back to Category footer mounts
"""

import json
import re
from datetime import datetime
from pathlib import Path

CANONICAL_DOMAIN = "https://themjtechhub.site"

def calculate_word_count(html_content: str) -> int:
    """Strips HTML tags and returns word count."""
    clean_text = re.sub(r"<[^>]+>", " ", html_content)
    words = clean_text.split()
    return len(words)

def calculate_read_time(html_content: str, words_per_minute: int = 200) -> str:
    """Calculates read time in minutes based on word count (minimum 5 min read)."""
    words = calculate_word_count(html_content)
    minutes = max(5, round(words / words_per_minute))
    return f"{minutes} min read"

def build_tutorial_html(tut: dict, cat_dir: str, cat_page: str, publish_date: str = "2026-09-09", update_date: str = None) -> str:
    """
    Renders a complete, standalone, production-ready tutorial HTML page.
    """
    title = tut["title"]
    desc = tut["description"]
    category = tut["category"]
    level = tut["level"]
    level_class = level.lower()
    slug = tut["id"]
    body_content = tut["html"]
    
    # Use declared readTime or compute dynamically
    read_time = tut.get("readTime") or calculate_read_time(body_content)
    
    pub_date = tut.get("publishedAt") or publish_date
    up_date = tut.get("updatedAt") or update_date or pub_date

    canonical_url = f"{CANONICAL_DOMAIN}/tutorials/{cat_dir}/{slug}.html"
    
    # Format date for display: e.g. "Sep 09, 2026"
    try:
        formatted_date = datetime.strptime(up_date, "%Y-%m-%d").strftime("%b %d, %Y")
    except Exception:
        formatted_date = up_date

    json_ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": desc,
        "url": canonical_url,
        "datePublished": pub_date,
        "dateModified": up_date,
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
                <a href="../../{cat_page}">{category}</a>
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
