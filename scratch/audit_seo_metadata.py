import os
import re
import json
from pathlib import Path
import xml.etree.ElementTree as ET

root = Path('.')
html_files = [f for f in root.rglob('*.html') if 'backup' not in f.parts and 'public' not in f.parts and 'scratch' not in f.parts]

print(f"Total HTML files found: {len(html_files)}")

# Load sitemap.xml
tree = ET.parse('sitemap.xml')
sitemap_urls = set()
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
for url_tag in tree.getroot().findall('sm:url', ns):
    loc = url_tag.find('sm:loc', ns)
    if loc is not None and loc.text:
        sitemap_urls.add(loc.text.strip())

print(f"Total URLs in sitemap.xml: {len(sitemap_urls)}")

canonicals = {}
missing_canonicals = []
wrong_host_canonicals = []
titles = {}
missing_titles = []
descriptions = {}
missing_descriptions = []
json_lds = {}
json_ld_errors = []
og_data = {}
twitter_data = {}

for hf in html_files:
    rel = str(hf.relative_to(root)).replace('\\', '/')
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # canonical
    can_match = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not can_match:
        can_match = re.search(r'<link\s+[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', content, re.IGNORECASE)
    if can_match:
        can_url = can_match.group(1)
        canonicals[rel] = can_url
        if not can_url.startswith('https://themjtechhub.site'):
            wrong_host_canonicals.append((rel, can_url))
    else:
        missing_canonicals.append(rel)

    # title
    t_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    if t_match:
        titles[rel] = t_match.group(1).strip()
    else:
        missing_titles.append(rel)

    # description
    d_match = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not d_match:
        d_match = re.search(r'<meta\s+[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']description["\']', content, re.IGNORECASE)
    if d_match:
        descriptions[rel] = d_match.group(1).strip()
    else:
        missing_descriptions.append(rel)

    # Open Graph
    og_title = re.search(r'<meta\s+[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    og_desc = re.search(r'<meta\s+[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    og_url = re.search(r'<meta\s+[^>]*property=["\']og:url["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    og_type = re.search(r'<meta\s+[^>]*property=["\']og:type["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    og_img = re.search(r'<meta\s+[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    og_data[rel] = {
        'title': og_title.group(1) if og_title else None,
        'description': og_desc.group(1) if og_desc else None,
        'url': og_url.group(1) if og_url else None,
        'type': og_type.group(1) if og_type else None,
        'image': og_img.group(1) if og_img else None,
    }

    # Twitter
    tw_card = re.search(r'<meta\s+[^>]*name=["\']twitter:card["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    tw_title = re.search(r'<meta\s+[^>]*name=["\']twitter:title["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    tw_desc = re.search(r'<meta\s+[^>]*name=["\']twitter:description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    tw_img = re.search(r'<meta\s+[^>]*name=["\']twitter:image["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    twitter_data[rel] = {
        'card': tw_card.group(1) if tw_card else None,
        'title': tw_title.group(1) if tw_title else None,
        'description': tw_desc.group(1) if tw_desc else None,
        'image': tw_img.group(1) if tw_img else None,
    }

    # json-ld
    ld_matches = re.findall(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    for ld in ld_matches:
        try:
            parsed = json.loads(ld.strip())
            json_lds.setdefault(rel, []).append(parsed)
        except Exception as e:
            json_ld_errors.append((rel, str(e)))

print('Missing canonicals:', len(missing_canonicals), missing_canonicals)
print('Wrong host canonicals:', len(wrong_host_canonicals), wrong_host_canonicals)
print('Missing titles:', len(missing_titles), missing_titles)
print('Missing descriptions:', len(missing_descriptions), missing_descriptions)
print('JSON-LD syntax errors:', len(json_ld_errors), json_ld_errors)
print('Pages with JSON-LD:', len(json_lds))

# Indexable files analysis
# Which files are indexable public pages?
# Exclude 404.html, tools/editor.html (admin/dev editor), and components
excluded = {'404.html', 'tools/editor.html'}
indexable_files = [f for f in html_files if str(f.relative_to(root)).replace('\\', '/') not in excluded]
print(f"Total indexable files: {len(indexable_files)}")

missing_from_sitemap = []
for hf in indexable_files:
    rel = str(hf.relative_to(root)).replace('\\', '/')
    can = canonicals.get(rel)
    # Note: index.html canonical is https://themjtechhub.site/
    if can and can not in sitemap_urls:
        missing_from_sitemap.append((rel, can))

print(f"Indexable pages missing from sitemap.xml: {len(missing_from_sitemap)}")
for rel, can in missing_from_sitemap[:20]:
    print(f"  Missing: {rel} -> {can}")
if len(missing_from_sitemap) > 20:
    print(f"  ... and {len(missing_from_sitemap) - 20} more")

# Check if any sitemap URL points to nonexistent file or planned topic
all_og_images = set(d['image'] for d in og_data.values() if d['image'])
all_tw_images = set(d['image'] for d in twitter_data.values() if d['image'])
print("Unique og:images:", len(all_og_images), all_og_images)
print("Unique twitter:images:", len(all_tw_images), all_tw_images)

pages_without_og_image = [rel for rel, d in og_data.items() if not d['image'] and rel not in ('components/header.html', 'components/footer.html', 'tools/editor.html')]
print(f"Indexable pages without og:image: {len(pages_without_og_image)}")

