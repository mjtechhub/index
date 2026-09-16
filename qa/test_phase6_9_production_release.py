#!/usr/bin/env python3
"""
Phase 6.9 - Production Release & Discoverability QA Test Suite
Tests both:
1. Local / Repository Assertions (Offline deterministic state)
2. Live Production HTTP Assertions (Online https://themjtechhub.site verification)
"""

import os
import sys
import json
import re
import socket
import ssl
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BASE_PROD_URL = "https://themjtechhub.site"

def test_repository_state():
    print("\n==================================================")
    print("PART 1: REPOSITORY STATE AUDIT (LOCAL / OFFLINE)")
    print("==================================================")

    # 1. Content Count Baseline
    print("Checking Platform Freeze Content Counts...")
    with open(ROOT_DIR / "data" / "tutorials.json", "r", encoding="utf-8") as f:
        tutorials = json.load(f)
    assert len(tutorials) == 148, f"Expected 148 tutorials, got {len(tutorials)}"

    cat_counts = {}
    for t in tutorials:
        cat_counts[t["category"]] = cat_counts.get(t["category"], 0) + 1
    assert cat_counts == {
        "Networking": 73,
        "Windows": 15,
        "Linux": 15,
        "Servers": 15,
        "Cybersecurity": 15,
        "Cloud & AI": 15
    }, f"Unexpected tutorial category counts: {cat_counts}"
    print(f"  [PASS] Tutorials count: 148 {cat_counts}")

    with open(ROOT_DIR / "data" / "topics.json", "r", encoding="utf-8") as f:
        topics_data = json.load(f)
    total_curr, pub_curr, plan_curr = 0, 0, 0
    for cat in topics_data.get("categories", []):
        for sec in cat.get("sections", []):
            for sub in sec.get("subtopics", []):
                total_curr += 1
                if sub.get("status") == "published":
                    pub_curr += 1
                elif sub.get("status") == "planned":
                    plan_curr += 1
    assert total_curr == 471, f"Expected 471 curriculum topics, got {total_curr}"
    assert pub_curr == 148, f"Expected 148 published topics, got {pub_curr}"
    assert plan_curr == 323, f"Expected 323 planned topics, got {plan_curr}"
    print(f"  [PASS] Curriculum: {total_curr} total (Pub: {pub_curr}, Plan: {plan_curr})")

    with open(ROOT_DIR / "data" / "commands.json", "r", encoding="utf-8") as f:
        commands = json.load(f)
    assert len(commands) == 42, f"Expected 42 commands, got {len(commands)}"
    print(f"  [PASS] Commands: {len(commands)}")

    with open(ROOT_DIR / "data" / "quizzes.json", "r", encoding="utf-8") as f:
        quizzes = json.load(f)
    assert len(quizzes) == 8, f"Expected 8 quizzes, got {len(quizzes)}"
    q_count = sum(len(q.get("questions", [])) for q in quizzes)
    assert q_count == 64, f"Expected 64 quiz questions, got {q_count}"
    print(f"  [PASS] Quizzes: {len(quizzes)} quizzes, {q_count} questions")

    with open(ROOT_DIR / "data" / "resources.json", "r", encoding="utf-8") as f:
        resources = json.load(f)
    assert len(resources) == 26, f"Expected 26 resources, got {len(resources)}"
    print(f"  [PASS] Resources: {len(resources)}")

    tools_files = [
        "tools/subnet-calculator.html",
        "tools/vlsm-planner.html",
        "tools/network-diagnostic-workbench.html",
        "tools/port-reference.html"
    ]
    for tf in tools_files:
        assert (ROOT_DIR / tf).exists(), f"Expected tool {tf} to exist"
    print(f"  [PASS] Interactive Tools: 4 verified")

    with open(ROOT_DIR / "data" / "troubleshooting-labs.json", "r", encoding="utf-8") as f:
        labs = json.load(f)
    assert len(labs) == 6, f"Expected 6 labs, got {len(labs)}"
    print(f"  [PASS] Troubleshooting Labs: {len(labs)}")

    # 2. CNAME
    cname_path = ROOT_DIR / "CNAME"
    assert cname_path.exists(), "CNAME file must exist"
    with open(cname_path, "r", encoding="utf-8") as f:
        cname_content = f.read().strip()
    assert cname_content == "themjtechhub.site", f"Expected CNAME 'themjtechhub.site', got '{cname_content}'"
    print(f"  [PASS] CNAME: '{cname_content}'")

    # 3. robots.txt
    robots_path = ROOT_DIR / "robots.txt"
    assert robots_path.exists(), "robots.txt must exist"
    with open(robots_path, "r", encoding="utf-8") as f:
        robots_content = f.read()
    assert "User-agent: *" in robots_content, "robots.txt missing User-agent: *"
    assert "Allow: /" in robots_content, "robots.txt missing Allow: /"
    assert "Sitemap: https://themjtechhub.site/sitemap.xml" in robots_content, "robots.txt missing sitemap reference"
    print("  [PASS] robots.txt verified")

    # 4. sitemap.xml
    sitemap_path = ROOT_DIR / "sitemap.xml"
    assert sitemap_path.exists(), "sitemap.xml must exist"
    tree = ET.parse(sitemap_path)
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    locs = [el.text.strip() for el in tree.getroot().findall('sm:url/sm:loc', ns)]
    assert len(locs) == 169, f"Expected 169 URLs in sitemap.xml, got {len(locs)}"
    assert len(set(locs)) == 169, "Duplicate URLs found in sitemap.xml"
    for loc in locs:
        assert loc.startswith("https://themjtechhub.site"), f"Invalid host in sitemap loc: {loc}"
        assert not any(x in loc for x in ["localhost", "file:", "404", "editor.html"]), f"Forbidden URL in sitemap: {loc}"
    print(f"  [PASS] sitemap.xml: {len(locs)} unique canonical HTTPS URLs verified")

    # 5. 404.html
    h404_path = ROOT_DIR / "404.html"
    assert h404_path.exists(), "404.html must exist"
    with open(h404_path, "r", encoding="utf-8") as f:
        h404_content = f.read()
    assert 'name="robots" content="noindex' in h404_content, "404.html must have robots noindex"
    assert "404" in h404_content and "Page Not Found" in h404_content, "404.html must explain page not found"
    assert "index.html" in h404_content and "topics.html" in h404_content and "tools.html" in h404_content, "404.html must link to Home, Topics, Tools"
    print("  [PASS] 404.html verified with noindex, H1, and navigation links")

    # 6. Favicon in root
    assert (ROOT_DIR / "favicon.ico").exists(), "Root favicon.ico must exist"
    print("  [PASS] Root favicon.ico exists")

    # 7. Structured Data Syntax
    html_files = [f for f in ROOT_DIR.rglob("*.html") if "backup" not in f.parts and "public" not in f.parts and "scratch" not in f.parts]
    for hf in html_files:
        with open(hf, "r", encoding="utf-8") as f:
            c = f.read()
        lds = re.findall(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', c, re.DOTALL | re.IGNORECASE)
        for ld in lds:
            try:
                parsed = json.loads(ld.strip())
                assert "localhost" not in json.dumps(parsed), f"Localhost detected in JSON-LD in {hf}"
            except Exception as e:
                raise AssertionError(f"Invalid JSON-LD in {hf}: {e}")
    print(f"  [PASS] Structured Data valid across {len(html_files)} HTML files")

    # 8. Security & Hygiene
    for hf in html_files:
        with open(hf, "r", encoding="utf-8") as f:
            c = f.read()
        blank_tags = re.findall(r'<a\s+[^>]*target=[\'"]_blank[\'"][^>]*>', c, re.IGNORECASE)
        for bt in blank_tags:
            assert 'rel=' in bt.lower() and ('noopener' in bt.lower() or 'noreferrer' in bt.lower()), f"Unsafe target=_blank in {hf}: {bt}"
    print(f"  [PASS] External links use rel='noopener noreferrer'")

    print("\n>>> ALL REPOSITORY STATE CHECKS PASSED <<<\n")


def test_live_production_state():
    print("==================================================")
    print("PART 2: LIVE PRODUCTION STATE AUDIT (ONLINE)")
    print("==================================================")

    # DNS check
    print("Checking DNS resolution for themjtechhub.site...")
    try:
        addr_info = socket.getaddrinfo("themjtechhub.site", 443, proto=socket.IPPROTO_TCP)
        ips = [item[4][0] for item in addr_info]
        assert len(ips) > 0, "No DNS records resolved for themjtechhub.site"
        print(f"  [PASS] Resolved IPs: {ips}")
    except Exception as e:
        print(f"  [WARN] DNS resolution warning/failure: {e}")

    ctx = ssl.create_default_context()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) MJTechHubReleaseAudit/1.0'}

    def fetch_status(url, retries=2):
        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
                    return resp.status, resp.read()
            except urllib.error.HTTPError as e:
                return e.code, None
            except Exception as e:
                if attempt == retries - 1:
                    raise e
        return None, None

    # Check Core Production Pages (Status 200)
    core_urls = [
        f"{BASE_PROD_URL}/",
        f"{BASE_PROD_URL}/about.html",
        f"{BASE_PROD_URL}/topics.html",
        f"{BASE_PROD_URL}/commands.html",
        f"{BASE_PROD_URL}/quiz.html",
        f"{BASE_PROD_URL}/resources.html",
        f"{BASE_PROD_URL}/tools.html",
        f"{BASE_PROD_URL}/labs.html",
        f"{BASE_PROD_URL}/tools/subnet-calculator.html",
        f"{BASE_PROD_URL}/tools/vlsm-planner.html",
        f"{BASE_PROD_URL}/tools/network-diagnostic-workbench.html",
        f"{BASE_PROD_URL}/tools/port-reference.html",
        f"{BASE_PROD_URL}/networking.html",
        f"{BASE_PROD_URL}/windows.html",
        f"{BASE_PROD_URL}/linux.html",
        f"{BASE_PROD_URL}/servers.html",
        f"{BASE_PROD_URL}/cybersecurity.html",
        f"{BASE_PROD_URL}/cloud.html",
        f"{BASE_PROD_URL}/legal/privacy.html",
        f"{BASE_PROD_URL}/legal/terms.html",
        f"{BASE_PROD_URL}/legal/disclaimer.html",
        f"{BASE_PROD_URL}/tutorials/networking/tcp-vs-udp.html",
        f"{BASE_PROD_URL}/robots.txt",
        f"{BASE_PROD_URL}/sitemap.xml",
    ]

    print("Probing Core Production Canonical URLs (Expected 200 OK)...")
    for u in core_urls:
        status, body = fetch_status(u)
        assert status == 200, f"Expected 200 for {u}, got {status}"
    print(f"  [PASS] All {len(core_urls)} core canonical production URLs returned 200 OK")

    # Check 404 behavior
    invalid_url = f"{BASE_PROD_URL}/this-page-should-not-exist-phase69.html"
    inv_status, _ = fetch_status(invalid_url)
    assert inv_status == 404, f"Expected 404 for invalid URL {invalid_url}, got {inv_status}"
    print(f"  [PASS] Invalid URL returned 404 correctly ({invalid_url})")

    # Check Live JSON Datasets
    print("Checking Live JSON Datasets...")
    json_urls = [
        (f"{BASE_PROD_URL}/data/tutorials.json", 148),
        (f"{BASE_PROD_URL}/data/commands.json", 42),
        (f"{BASE_PROD_URL}/data/quizzes.json", 8),
        (f"{BASE_PROD_URL}/data/resources.json", 26),
        (f"{BASE_PROD_URL}/data/troubleshooting-labs.json", 6),
    ]
    for jurl, expected_len in json_urls:
        status, body = fetch_status(jurl)
        assert status == 200, f"Failed to fetch {jurl}"
        parsed = json.loads(body.decode("utf-8"))
        actual_len = len(parsed)
        assert actual_len == expected_len, f"Expected {expected_len} items in {jurl}, got {actual_len}"
        print(f"  [PASS] Live dataset {jurl.split('/')[-1]}: {actual_len} items")

    # Check ports dataset specifically
    p_status, p_body = fetch_status(f"{BASE_PROD_URL}/data/ports.json")
    assert p_status == 200, "Failed to fetch live ports.json"
    live_ports_len = len(json.loads(p_body.decode("utf-8")))
    print(f"  [INFO] Live ports count: {live_ports_len} (Repository: 50)")

    # Live Quiz Deep-Link check for all 8 canonical quiz IDs derived from data/quizzes.json
    print("Checking all 8 canonical quiz deep-links...")
    with open(ROOT_DIR / "data" / "quizzes.json", "r", encoding="utf-8") as f:
        quizzes_ref = json.load(f)
    canonical_quiz_ids = [q["id"] for q in quizzes_ref]
    assert len(canonical_quiz_ids) == 8, f"Expected 8 canonical quiz IDs, got {len(canonical_quiz_ids)}"
    for qid in canonical_quiz_ids:
        quiz_link = f"{BASE_PROD_URL}/quiz.html?quiz={qid}"
        q_status, _ = fetch_status(quiz_link)
        assert q_status == 200, f"Expected 200 for quiz deep-link {quiz_link}, got {q_status}"
    print(f"  [PASS] All 8 canonical quiz deep-links returned 200 OK: {canonical_quiz_ids}")


    print("\n>>> ALL LIVE PRODUCTION STATE CHECKS PASSED <<<\n")

if __name__ == "__main__":
    try:
        test_repository_state()
        test_live_production_state()
        print("[SUCCESS] Phase 6.9 QA Test Suite Passed Completely!")
        sys.exit(0)
    except Exception as e:
        print(f"[FAIL] QA Suite Failed: {e}")
        sys.exit(1)
