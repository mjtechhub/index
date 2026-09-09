import json

with open('data/topics.json', encoding='utf-8') as f:
    topics = json.load(f)['categories']

with open('data/tutorials.json', encoding='utf-8') as f:
    tuts = json.load(f)

existing_ids = {t['id'] for t in tuts}
existing_urls = {t['url'].replace('./', '') for t in tuts}

print("=== AUDITING CANDIDATES ===")

def find_planned(cat_id, keywords):
    cat = next(c for c in topics if c['id'] == cat_id)
    matches = []
    for s in cat['sections']:
        for sub in s['subtopics']:
            if sub.get('status') == 'planned':
                for kw in keywords:
                    if kw.lower() in sub['name'].lower() or kw.lower() in sub['id'].lower():
                        matches.append((s['name'], sub))
                        break
    return matches

with open('scratch/candidates_all.txt', 'w', encoding='utf-8') as out_f:
    for cat_id in ['networking', 'windows', 'linux', 'servers', 'cybersecurity', 'cloud']:
        out_f.write(f"\n=== {cat_id.upper()} ===\n")
        matches = find_planned(cat_id, [
            'wifi', 'wi-fi', 'channel', 'lacp', 'link aggregation', 'sd-wan', 'etherchannel',
            'ntfs', 'permission', 'event viewer', 'log', 'powershell', 'automation',
            'chmod', 'chown', 'systemd', 'service', 'cpu', 'memory', 'performance',
            'active directory', 'domain controller', 'dns', 'dhcp', 'raid',
            'password', 'credential', 'edr', 'antivirus', 'segmentation', 'microsegmentation', 'mfa',
            'ec2', 'virtual machine', 'vpc', 'vnet', 'iam', 'least privilege'
        ])
        for sec, sub in matches:
            out_f.write(f"[{sec}] id='{sub['id']}' | name='{sub['name']}' | level='{sub['level']}'\n")

print("\n--- WINDOWS ---")
for sec, sub in find_planned('windows', ['ntfs', 'permission', 'event viewer', 'log', 'powershell', 'automation']):
    print(f"[{sec}] id='{sub['id']}' | name='{sub['name']}' | level='{sub['level']}'")

print("\n--- LINUX ---")
for sec, sub in find_planned('linux', ['chmod', 'permission', 'systemd', 'service', 'cpu', 'memory', 'performance']):
    print(f"[{sec}] id='{sub['id']}' | name='{sub['name']}' | level='{sub['level']}'")

print("\n--- SERVERS ---")
for sec, sub in find_planned('servers', ['active directory', 'domain controller', 'dns', 'dhcp', 'raid']):
    print(f"[{sec}] id='{sub['id']}' | name='{sub['name']}' | level='{sub['level']}'")

print("\n--- CYBERSECURITY ---")
for sec, sub in find_planned('cybersecurity', ['password', 'credential', 'edr', 'antivirus', 'segmentation', 'microsegmentation', 'mfa']):
    print(f"[{sec}] id='{sub['id']}' | name='{sub['name']}' | level='{sub['level']}'")

print("\n--- CLOUD & AI ---")
for sec, sub in find_planned('cloud', ['ec2', 'virtual machine', 'vpc', 'vnet', 'iam', 'least privilege']):
    print(f"[{sec}] id='{sub['id']}' | name='{sub['name']}' | level='{sub['level']}'")
