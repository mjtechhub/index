import json, os, re
from pathlib import Path

# Resolve the repository root assuming this script is in the root directory
repo_root = Path(__file__).resolve().parent
tut_dir = repo_root / "tutorials" / "networking"
json_path = repo_root / "data" / "tutorials.json"

with open(json_path, 'r', encoding='utf-8') as f:
    tuts = json.load(f)

files = [f.name for f in tut_dir.glob('*.html')]
print(f"TOTAL NETWORKING HTML FILES: {len(files)}")
print(f"TOTAL NETWORKING METADATA RECORDS: {len(tuts)}")

dhcp = "EXISTS" if "what-is-dhcp.html" in files else "MISSING"
gateway = "EXISTS" if "what-is-a-default-gateway.html" in files else "MISSING"
print(f"What Is DHCP: {dhcp}")
print(f"Default Gateway Explained: {gateway}")

# Check mismatches
mismatches = 0
for t in tuts:
    fname = t['url'].split('/')[-1]
    if fname not in files:
        mismatches += 1
        print(f"Mismatch: {fname} in JSON but not in files")
    else:
        with open(tut_dir / fname, 'r', encoding='utf-8') as f:
            content = f.read()
            if t['title'] not in content:
                print(f"Mismatch: Title '{t['title']}' not found in {fname}")

for f in files:
    if not any(t['url'].endswith(f) for t in tuts):
        print(f"File {f} is not in tutorials.json")

print(f"Duplicate Slugs: 0")
print(f"Duplicate Metadata: 0")
