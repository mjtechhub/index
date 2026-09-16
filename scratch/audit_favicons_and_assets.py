import re
from pathlib import Path

root = Path('.')
html_files = [f for f in root.rglob('*.html') if 'backup' not in f.parts and 'public' not in f.parts and 'scratch' not in f.parts]

fav_tags = {}
for hf in html_files:
    rel = str(hf.relative_to(root)).replace('\\', '/')
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'<link\s+[^>]*rel=["\'](?:icon|shortcut icon|apple-touch-icon)["\'][^>]*>', content, re.IGNORECASE)
    if matches:
        fav_tags[rel] = matches

print(f"Pages with favicon tags: {len(fav_tags)} / {len(html_files)}")
sample_tags = list(fav_tags.items())[:5]
for rel, tags in sample_tags:
    print(f"  {rel}: {tags}")

# Check if favicon files exist
favicon_files = [
    'assets/favicon/favicon.ico',
    'assets/favicon/favicon-16x16.png',
    'assets/favicon/favicon-32x32.png',
    'assets/favicon/apple-touch-icon.png',
    'assets/favicon/favicon-512x512.png',
]
for ff in favicon_files:
    print(f"File {ff} exists: {(root / ff).exists()} (size: {(root / ff).stat().st_size} bytes)")

# Check if favicon.ico exists in root
print(f"Root favicon.ico exists: {(root / 'favicon.ico').exists()}")
