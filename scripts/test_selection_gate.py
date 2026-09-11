import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_PATH = ROOT_DIR / "data" / "topics.json"
TUTS_PATH = ROOT_DIR / "data" / "tutorials.json"

with open(TOPICS_PATH, "r", encoding="utf-8") as f:
    topics_data = json.load(f)

with open(TUTS_PATH, "r", encoding="utf-8") as f:
    tuts_data = json.load(f)

existing_ids = {t["id"] for t in tuts_data}
existing_urls = {t["url"] for t in tuts_data}

# Proposed 18 topics (3 per core category)
proposed = [
    # NETWORKING (3)
    {"cat_id": "networking", "id": "chassis-stacking-and-switch-virtualization"},
    {"cat_id": "networking", "id": "dhcp-dora-process-and-options-architecture"},
    {"cat_id": "networking", "id": "wireless-roaming-802-11r-k-v-standards"},

    # WINDOWS (3)
    {"cat_id": "windows", "id": "windows-remote-desktop-protocol-rdp-configuration"},
    {"cat_id": "windows", "id": "windows-defender-firewall-with-advanced-security"},
    {"cat_id": "windows", "id": "windows-update-for-business-wufb-deployment-rings"},

    # LINUX (3)
    {"cat_id": "linux", "id": "linux-lvm-architecture-physical-volumes-volume-groups"},
    {"cat_id": "linux", "id": "linux-process-signaling-and-termination-kill-pkill"},
    {"cat_id": "linux", "id": "linux-systemd-journalctl-log-analysis-and-filtering"},

    # SERVERS (3)
    {"cat_id": "servers", "id": "windows-server-core-headless-deployment-and-remote-management"},
    {"cat_id": "servers", "id": "enterprise-dhcp-failover-load-balancing-and-hot-standby"},
    {"cat_id": "servers", "id": "windows-server-failover-clustering-wsfc-architecture"},

    # CYBERSECURITY (3)
    {"cat_id": "cybersecurity", "id": "single-sign-on-sso-architecture-saml-2-0-and-oidc"},
    {"cat_id": "cybersecurity", "id": "security-information-and-event-management-siem-architecture"},
    {"cat_id": "cybersecurity", "id": "nist-sp-800-61-computer-security-incident-handling-guide"},

    # CLOUD & AI (3)
    {"cat_id": "cloud", "id": "serverless-computing-architecture-and-event-driven-design"},
    {"cat_id": "cloud", "id": "azure-virtual-networks-vnet-subnets-and-peering-architecture"},
    {"cat_id": "cloud", "id": "finops-fundamentals-cloud-financial-management-and-cost-allocation"}
]

print("="*90)
print("TESTING PROPOSED 18 BATCH 4 TOPICS AGAINST TOPICS.JSON AND TUTORIALS.JSON")
print("="*90)

assert len(proposed) == 18, f"Expected 18, got {len(proposed)}"

errors = []
rows = []

for item in proposed:
    cid = item["cat_id"]
    tid = item["id"]
    
    # 1. Find topic in topics_data
    found = None
    target_cat = next((c for c in topics_data["categories"] if c["id"] == cid), None)
    if not target_cat:
        errors.append(f"Category {cid} not found in topics.json")
        continue

    for s_idx, sec in enumerate(target_cat.get("sections", [])):
        subs = sec.get("subtopics", [])
        spub = sum(1 for s in subs if s.get("status") == "published")
        stotal = len(subs)
        ratio = spub / stotal if stotal > 0 else 0
        for sub in subs:
            if sub["id"] == tid:
                found = {
                    "subtopic": sub,
                    "section_idx": s_idx + 1,
                    "section_name": sec["name"],
                    "section_pub": spub,
                    "section_total": stotal,
                    "section_ratio": ratio,
                    "cat_name": target_cat["name"]
                }
                break
        if found:
            break
            
    if not found:
        errors.append(f"Topic {tid} NOT FOUND in category {cid} in topics.json!")
        continue

    sub = found["subtopic"]
    
    # Check status == planned
    if sub.get("status") != "planned":
        errors.append(f"Topic {tid} status is '{sub.get('status')}', expected 'planned'!")

    # Check collision in tutorials.json
    if tid in existing_ids:
        errors.append(f"Collision: Topic {tid} is ALREADY in tutorials.json!")

    expected_url = f"tutorials/{cid}/{tid}.html"
    if expected_url in existing_urls:
        errors.append(f"Collision: URL {expected_url} is ALREADY in tutorials.json!")

    rows.append({
        "category": found["cat_name"],
        "id": tid,
        "title": sub["name"],
        "level": sub["level"],
        "section": f"Sec {found['section_idx']}: {found['section_name']}",
        "sec_pub": found["section_pub"],
        "sec_total": found["section_total"],
        "ratio": f"{found['section_ratio']*100:.1f}%",
        "status": sub.get("status")
    })

print(f"{'Category':<15} | {'Topic ID':<45} | {'Level':<12} | {'Section (Pub/Total)':<40} | {'Status'}")
print("-" * 130)
for r in rows:
    sec_str = f"{r['section'][:25]} ({r['sec_pub']}/{r['sec_total']} = {r['ratio']})"
    print(f"{r['category']:<15} | {r['id']:<45} | {r['level']:<12} | {sec_str:<40} | {r['status']}")

print("\nERRORS DETECTED:", len(errors))
for e in errors:
    print("  ERROR:", e)

if not errors:
    print("\nALL 18 CANDIDATES PASSED THE MANDATORY SELECTION GATE INTEGRITY CHECKS!")
