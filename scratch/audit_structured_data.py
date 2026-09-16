import json
import re
from pathlib import Path

root = Path('.')
html_files = [f for f in root.rglob('*.html') if 'backup' not in f.parts and 'public' not in f.parts and 'scratch' not in f.parts]

schema_types = {}
pages_by_type = {}
schema_issues = []

for hf in html_files:
    rel = str(hf.relative_to(root)).replace('\\', '/')
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    ld_matches = re.findall(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    for idx, ld in enumerate(ld_matches):
        try:
            data = json.loads(ld.strip())
            # Can be a single dict or a list or have @graph
            items = []
            if isinstance(data, list):
                items.extend(data)
            elif isinstance(data, dict):
                if '@graph' in data:
                    items.extend(data['@graph'])
                else:
                    items.append(data)

            for item in items:
                stype = item.get('@type', 'Unknown')
                schema_types[stype] = schema_types.get(stype, 0) + 1
                pages_by_type.setdefault(stype, set()).add(rel)

                # Check for localhost / placeholder
                item_str = json.dumps(item)
                if 'localhost' in item_str:
                    schema_issues.append((rel, stype, 'Contains localhost'))
                if 'example.com' in item_str:
                    schema_issues.append((rel, stype, 'Contains example.com'))
        except Exception as e:
            schema_issues.append((rel, 'SyntaxError', str(e)))

print("=== SCHEMA TYPES DETECTED ===")
for stype, count in schema_types.items():
    print(f"  {stype}: {count} occurrences across {len(pages_by_type[stype])} pages")

print(f"\nSchema issues found: {len(schema_issues)}")
for issue in schema_issues:
    print(" ", issue)

# Check specifically homepage, about, tools, labs
print("\n=== SPECIFIC PAGES ===")
for p in ['index.html', 'about.html', 'tools.html', 'labs.html', 'commands.html', 'quiz.html', 'resources.html']:
    with open(root / p, 'r', encoding='utf-8') as f:
        content = f.read()
    lds = re.findall(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    types_in_page = []
    for ld in lds:
        try:
            d = json.loads(ld.strip())
            if isinstance(d, dict):
                types_in_page.append(d.get('@type'))
        except:
            pass
    print(f"  {p}: {types_in_page}")
