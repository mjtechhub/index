import os
import re
from pathlib import Path

root = Path('.')
html_files = [f for f in root.rglob('*.html') if 'backup' not in f.parts and 'public' not in f.parts and 'scratch' not in f.parts]
js_files = [f for f in root.rglob('*.js') if 'backup' not in f.parts and 'public' not in f.parts and 'scratch' not in f.parts]
css_files = [f for f in root.rglob('*.css') if 'backup' not in f.parts and 'public' not in f.parts and 'scratch' not in f.parts]

print("=== 1. TARGET=_BLANK REL CHECK ===")
missing_rel = []
for hf in html_files:
    rel = str(hf.relative_to(root)).replace('\\', '/')
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    # match <a> tags with target="_blank"
    tags = re.findall(r'<a\s+[^>]*target=[\'"]_blank[\'"][^>]*>', content, re.IGNORECASE)
    for t in tags:
        if 'rel=' not in t.lower() or ('noopener' not in t.lower() and 'noreferrer' not in t.lower()):
            missing_rel.append((rel, t))

print(f"Missing rel on target=_blank: {len(missing_rel)}")
for m in missing_rel[:10]:
    print(" ", m)

print("\n=== 2. RISKY CLIENT-SIDE APIS ===")
risky_api_findings = []
for jf in js_files:
    rel = str(jf.relative_to(root)).replace('\\', '/')
    with open(jf, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check eval(, new Function(, document.write(
    if re.search(r'\beval\s*\(', content):
        risky_api_findings.append((rel, "eval() detected"))
    if re.search(r'new\s+Function\s*\(', content):
        risky_api_findings.append((rel, "new Function() detected"))
    if re.search(r'document\.write\s*\(', content):
        risky_api_findings.append((rel, "document.write() detected"))

print(f"Risky API findings: {len(risky_api_findings)}")
for r in risky_api_findings:
    print(" ", r)

print("\n=== 3. SECRETS SCAN ===")
secret_patterns = [
    (r'(?i)(api[_-]?key|apikey|secret[_-]?key|access[_-]?token|auth[_-]?token)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{16,}["\']', "Potential API Key / Token"),
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', "Private Key Block"),
    (r'(?i)ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token"),
    (r'(?i)AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
]

secrets_found = []
all_text_files = html_files + js_files + css_files + list(root.glob('data/*.json'))
for tf in all_text_files:
    rel = str(tf.relative_to(root)).replace('\\', '/')
    with open(tf, 'r', encoding='utf-8') as f:
        content = f.read()
    for pat, label in secret_patterns:
        matches = re.findall(pat, content)
        if matches:
            secrets_found.append((rel, label))

print(f"Secrets found: {len(secrets_found)}")
for s in secrets_found:
    print(" ", s)

print("\n=== 4. CASE-SENSITIVITY OF LOCAL LINKS AND ASSETS ===")
# Build exact case map of all files in repo
exact_files = {}
for p in root.rglob('*'):
    if 'backup' in p.parts or 'public' in p.parts or 'scratch' in p.parts or '.git' in p.parts:
        continue
    if p.is_file():
        rel = str(p.relative_to(root)).replace('\\', '/')
        exact_files[rel.lower()] = rel

case_mismatches = []
for hf in html_files:
    rel_h = str(hf.relative_to(root)).replace('\\', '/')
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    refs = re.findall(r'(?:src|href)=[\'"]([^\'"]+)[\'"]', content)
    for r in refs:
        if r.startswith(('http://', 'https://', '//', '#', 'mailto:', 'tel:', 'data:')):
            continue
        clean_r = r.split('?')[0].split('#')[0]
        if not clean_r:
            continue
        # Resolve target relative to file parent
        target = (hf.parent / clean_r).resolve()
        try:
            rel_target = str(target.relative_to(root.resolve())).replace('\\', '/')
        except ValueError:
            continue
        lower_t = rel_target.lower()
        if lower_t in exact_files:
            if exact_files[lower_t] != rel_target:
                case_mismatches.append((rel_h, r, exact_files[lower_t], rel_target))

print(f"Case mismatches found: {len(case_mismatches)}")
for cm in case_mismatches:
    print(" ", cm)
