import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_PATH = ROOT_DIR / "data" / "topics.json"

with open(TOPICS_PATH, "r", encoding="utf-8") as f:
    topics_data = json.load(f)

candidates = [
    # Networking
    "lacp-link-aggregation-control-protocol-802-3ad",
    "bgp-path-selection-attributes-and-decision-process",
    "network-segmentation-with-vrf-virtual-routing-and-forwarding",
    # Windows
    "windows-storage-spaces-and-storage-pools-architecture",
    "windows-update-for-business-wufb-and-wsus-administration",
    "windows-firewall-with-advanced-security-wfas-rules",
    # Linux
    "linux-journalctl-and-systemd-journald-administration",
    "linux-process-lifecycle-ps-top-kill-and-signals",
    "linux-logical-volume-manager-lvm-pv-vg-lv-administration",
    # Servers
    "windows-server-core-administration-and-remote-management",
    "dhcp-failover-modes-load-balance-vs-hot-standby",
    "high-availability-failover-clustering-wsfc-principles",
    # Cybersecurity
    "siem-architecture-and-security-event-correlation-principles",
    "saml-2-0-vs-oauth-2-0-and-oidc-identity-federation",
    "dns-security-extensions-dnssec-signing-and-validation",
    # Cloud & AI
    "aws-lambda-serverless-architecture-execution-models",
    "cloud-finops-principles-cost-allocation-tags-and-budgets",
    "azure-virtual-network-vnet-peering-and-nsg-architecture"
]

cand_map = {}
for cat in topics_data["categories"][:6]:
    for s_idx, sec in enumerate(cat.get("sections", [])):
        subs = sec.get("subtopics", [])
        spub = sum(1 for s in subs if s.get("status") == "published")
        stotal = len(subs)
        for sub in subs:
            if sub["id"] in candidates:
                cand_map[sub["id"]] = {
                    "category": cat["name"],
                    "cat_id": cat["id"],
                    "section_idx": s_idx + 1,
                    "section_name": sec["name"],
                    "section_pub": spub,
                    "section_total": stotal,
                    "section_ratio": spub / stotal if stotal > 0 else 0,
                    "subtopic": sub
                }

print(f"Found {len(cand_map)} of {len(candidates)} candidates in topics.json")
for cid in candidates:
    if cid in cand_map:
        info = cand_map[cid]
        sub = info["subtopic"]
        print(f"[{info['cat_id']}] Sec {info['section_idx']} ({info['section_name']}): {sub['id']}")
        print(f"    Name: {sub['name']}")
        print(f"    Level: {sub['level']} | Status: {sub['status']}")
        print(f"    Section Coverage: {info['section_pub']}/{info['section_total']} ({info['section_ratio']*100:.1f}%)")
    else:
        print(f"MISSING CANDIDATE: {cid}")
