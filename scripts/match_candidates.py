import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_PATH = ROOT_DIR / "data" / "topics.json"
TUTS_PATH = ROOT_DIR / "data" / "tutorials.json"

with open(TOPICS_PATH, "r", encoding="utf-8") as f:
    topics_data = json.load(f)

with open(TUTS_PATH, "r", encoding="utf-8") as f:
    tuts_data = json.load(f)

published_ids = {t["id"] for t in tuts_data}

keywords = {
    "networking": ["aggregation", "lacp", "bgp", "vrf", "802.1q", "stacking", "pat", "wireshark", "telemetry", "ipfix", "flow", "ipsec", "roaming", "wpa3", "wifi", "ntp", "dhcp", "dns", "vlsm"],
    "windows": ["storage", "pool", "wsus", "wufb", "update", "firewall", "wfas", "sysprep", "rdp", "smb", "winrm", "powershell", "uac", "registry", "sysinternals"],
    "linux": ["journalctl", "journald", "systemd", "process", "ps", "top", "kill", "signal", "lvm", "pv", "vg", "lv", "boot", "grub", "rescue", "fdisk", "parted", "sed", "awk", "auditd", "aide"],
    "servers": ["server-core", "core", "dhcp", "failover", "wsfc", "clustering", "hyper-v", "esxi", "san", "iscsi", "numa", "idrac", "ilo", "dfs", "quorum", "repadmin"],
    "cybersecurity": ["siem", "logging", "correlation", "saml", "oauth", "oidc", "dnssec", "incident", "csf", "edr", "xdr", "att&ck", "epss", "soar", "auditd"],
    "cloud": ["lambda", "serverless", "finops", "cost", "peering", "vnet", "nsg", "tag", "budget", "arm", "bicep", "terraform", "s3", "blob", "route", "iam", "aiops"]
}

for cat in topics_data["categories"][:6]:
    cid = cat["id"]
    print("\n" + "="*80)
    print(f"MATCHES FOR CATEGORY: {cat['name']} ({cid})")
    print("="*80)
    
    cat_kw = keywords.get(cid, [])
    for s_idx, sec in enumerate(cat.get("sections", [])):
        subs = sec.get("subtopics", [])
        spub = sum(1 for s in subs if s.get("status") == "published")
        stotal = len(subs)
        for sub in subs:
            sid = sub["id"]
            sname = sub["name"].lower()
            # check if matches any keyword
            matched = [kw for kw in cat_kw if kw in sid.lower() or kw in sname]
            if matched:
                is_pub = sid in published_ids or sub.get("status") == "published"
                status_str = "PUBLISHED" if is_pub else "PLANNED"
                print(f"  [{status_str}] Sec {s_idx+1} ({spub}/{stotal}): {sid} -> {sub['name']} (matched: {matched})")
