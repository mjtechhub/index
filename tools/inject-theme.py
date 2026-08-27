import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'js/theme-init.js' in content:
        return

    # Find the relative path from the themes.css link
    match = re.search(r'href="([^"]*)css/themes\.css"', content)
    if not match:
        return

    relative_prefix = match.group(1)
    script_tag = f'<script src="{relative_prefix}js/theme-init.js"></script>'

    if '<head>' in content:
        content = content.replace('<head>', f'<head>\n    {script_tag}', 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected into {filepath}")

for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root or 'tools' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))
