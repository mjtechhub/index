import json

with open('data/topics.json', encoding='utf-8') as f:
    topics = json.load(f)['categories']

with open('data/tutorials.json', encoding='utf-8') as f:
    tuts = json.load(f)

existing_tut_ids = {t['id'] for t in tuts}
existing_tut_urls = {t['url'].replace('./', '') for t in tuts}

# Proposed selection of 18 planned topics:
proposed_selection = [
    # 1. NETWORKING (3)
    # - Wireless: rf-channel-planning-and-interference-mitigation ("RF Channel Planning, Band Steering & Co-Channel Interference")
    # - Switching: rapid-spanning-tree-rstp-802-1w ("Rapid Spanning Tree (RSTP 802.1w) & MSTP Explained")
    # - Resilience/Security: next-generation-firewall-ngfw-deep-packet-inspection ("NGFW Architecture: Application Awareness & Deep Packet Inspection")
    {"cat_id": "networking", "id": "rf-channel-planning-and-interference-mitigation"},
    {"cat_id": "networking", "id": "rapid-spanning-tree-rstp-802-1w"},
    {"cat_id": "networking", "id": "next-generation-firewall-ngfw-deep-packet-inspection"},

    # 2. WINDOWS (3)
    # - Permissions: windows-ntfs-permissions-vs-share-permissions ("NTFS Permissions vs Share Permissions: Calculating Effective Access")
    # - Diagnostics/Logs: windows-event-viewer-architecture-and-standard-logs ("Windows Event Viewer: System, Application & Security Log Architecture")
    # - Automation: powershell-pipeline-object-manipulation-and-filtering ("PowerShell Pipeline Architecture & Object Filtering (Where/Select)")
    {"cat_id": "windows", "id": "windows-ntfs-permissions-vs-share-permissions"},
    {"cat_id": "windows", "id": "windows-event-viewer-architecture-and-standard-logs"},
    {"cat_id": "windows", "id": "powershell-pipeline-object-manipulation-and-filtering"},

    # 3. LINUX (3)
    # - Permissions: linux-standard-file-permissions-chmod-chown ("Standard Linux File Permissions: Read, Write, Execute (chmod & chown)")
    # - Services: linux-systemd-service-units-creation-and-control ("Authoring Systemd Service Units: Unit Files, Dependencies & systemctl")
    # - Performance/Memory: linux-memory-management-buffers-caches-oom-killer ("Linux Memory Management: Buffers, Page Cache & Out-Of-Memory (OOM) Killer")
    {"cat_id": "linux", "id": "linux-standard-file-permissions-chmod-chown"},
    {"cat_id": "linux", "id": "linux-systemd-service-units-creation-and-control"},
    {"cat_id": "linux", "id": "linux-memory-management-buffers-caches-oom-killer"},

    # 4. SERVERS (3)
    # - Active Directory: active-directory-domain-controller-promotion-and-demotion ("Domain Controller Promotion (dcpromo), Staging & Demotion Workflows")
    # - Core Services: enterprise-dns-server-architecture-and-zone-types ("Enterprise DNS Server Architecture: Forward, Reverse, Primary & Secondary Zones")
    # - Storage/Hardware: server-raid-levels-explained-0-1-5-6-10 ("RAID Levels Explained: 0, 1, 5, 6, 10 & Nested Arrays")
    {"cat_id": "servers", "id": "active-directory-domain-controller-promotion-and-demotion"},
    {"cat_id": "servers", "id": "enterprise-dns-server-architecture-and-zone-types"},
    {"cat_id": "servers", "id": "server-raid-levels-explained-0-1-5-6-10"},

    # 5. CYBERSECURITY (3)
    # - Authentication: modern-password-policies-and-nist-800-63-guidelines ("Modern Password Security Policies: NIST SP 800-63B Passphrase Guidelines")
    # - Endpoint Protection: next-generation-antivirus-ngav-vs-traditional-signatures ("Next-Gen Antivirus (NGAV): Behavioral Heuristics vs Traditional Signatures")
    # - Network Defense: network-microsegmentation-and-software-defined-perimeters ("Network Microsegmentation Architecture & Host-to-Host Encryption")
    {"cat_id": "cybersecurity", "id": "modern-password-policies-and-nist-800-63-guidelines"},
    {"cat_id": "cybersecurity", "id": "next-generation-antivirus-ngav-vs-traditional-signatures"},
    {"cat_id": "cybersecurity", "id": "network-microsegmentation-and-software-defined-perimeters"},

    # 6. CLOUD & AI (3)
    # - Compute: aws-ec2-instance-families-and-purchasing-models ("Amazon EC2 Architecture: Instance Types, Savings Plans & Spot Instances")
    # - Networking: aws-vpc-architecture-subnets-route-tables-and-internet-gateways ("Amazon VPC Architecture: Public/Private Subnets, Route Tables & Internet Gateways")
    # - IAM: cloud-iam-policy-syntax-json-statements-and-least-privilege ("Authoring Cloud IAM Policies: JSON Statement Syntax & Principle of Least Privilege")
    {"cat_id": "cloud", "id": "aws-ec2-instance-families-and-purchasing-models"},
    {"cat_id": "cloud", "id": "aws-vpc-architecture-subnets-route-tables-and-internet-gateways"},
    {"cat_id": "cloud", "id": "cloud-iam-policy-syntax-json-statements-and-least-privilege"}
]

print(f"Auditing {len(proposed_selection)} candidate topics:")
all_valid = True
for item in proposed_selection:
    cat_id = item["cat_id"]
    sub_id = item["id"]
    cat = next((c for c in topics if c["id"] == cat_id), None)
    if not cat:
        print(f"ERROR: Category {cat_id} not found!")
        all_valid = False
        continue

    found = None
    sec_name = None
    for s in cat["sections"]:
        for sub in s["subtopics"]:
            if sub["id"] == sub_id:
                found = sub
                sec_name = s["name"]
                break
        if found:
            break

    if not found:
        print(f"ERROR: Topic {sub_id} not found in {cat_id}!")
        all_valid = False
        continue

    if found.get("status") != "planned":
        print(f"ERROR: Topic {sub_id} status is '{found.get('status')}', expected 'planned'!")
        all_valid = False
        continue

    if sub_id in existing_tut_ids:
        print(f"ERROR: Topic {sub_id} already exists in tutorials.json!")
        all_valid = False
        continue

    target_url = f"tutorials/{cat_id}/{sub_id}.html"
    if target_url in existing_tut_urls:
        print(f"ERROR: Target URL {target_url} already exists in tutorials.json!")
        all_valid = False
        continue

    print(f"OK: [{cat['name']}] [{sec_name}] id='{sub_id}' | name='{found['name']}' | level='{found['level']}'")

if all_valid:
    print("\nALL 18 CANDIDATES VERIFIED 100% VALID IN TOPICS.JSON AND TUTORIALS.JSON!")
