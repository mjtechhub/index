#!/usr/bin/env python3
"""
MJ Tech Hub - Master Curriculum Architecture Generator (Phase 6.5A)
Builds the comprehensive long-term IT curriculum for MJ Tech Hub:
- 6 Core Domains: Networking, Windows, Linux, Servers, Cybersecurity, Cloud & AI
- >= 70 unique topics per domain (target: 75-85 topics per domain)
- 10 structured sections per category (7-10 topics per section)
- Maps all 76 existing published tutorials 1-to-1 (exact id, title, level, url, status="published")
- Distinguishes planned curriculum items (status="planned", no fake URL)
- Enforces globally unique subtopic IDs across the entire platform
- Strict duplicate checks: exact duplicates, normalized duplicates
- Reports difficulty progression per section and category
"""

import json
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_JSON_PATH = REPO_ROOT / "data" / "topics.json"
TUTORIALS_JSON_PATH = REPO_ROOT / "data" / "tutorials.json"

with open(TUTORIALS_JSON_PATH, "r", encoding="utf-8") as f:
    PUBLISHED_TUTORIALS = json.load(f)

PUB_BY_ID = {t["id"]: t for t in PUBLISHED_TUTORIALS}
PUB_BY_URL = {t["url"].replace("./", ""): t for t in PUBLISHED_TUTORIALS}

# Helper to build a published record from tutorials.json
def pub(tut_id, custom_name=None):
    if tut_id not in PUB_BY_ID:
        raise ValueError(f"Published tutorial ID '{tut_id}' not found in tutorials.json!")
    t = PUB_BY_ID[tut_id]
    return {
        "id": t["id"],
        "name": custom_name or t["title"],
        "level": t["level"],
        "status": "published",
        "url": t["url"].replace("./", "")
    }

# Helper to build a planned record
def plan(sub_id, name, level):
    if level not in ["Beginner", "Intermediate", "Advanced"]:
        raise ValueError(f"Invalid level '{level}' for '{sub_id}'")
    return {
        "id": sub_id,
        "name": name,
        "level": level,
        "status": "planned"
    }

# -------------------------------------------------------------
# 1. NETWORKING (84 topics: 61 published + 23 planned)
# -------------------------------------------------------------
NETWORKING_SECTIONS = [
    {
        "name": "Networking Fundamentals & Core Models",
        "subtopics": [
            pub("what-is-a-computer-network"),
            pub("lan-vs-wan"),
            pub("osi-model-explained"),
            pub("tcp-ip-model-explained"),
            pub("hub-vs-switch"),
            pub("router-vs-switch"),
            pub("what-is-a-mac-address"),
            plan("network-topologies-mesh-star-bus", "Network Topologies: Star, Mesh, Bus & Hybrid", "Beginner"),
            plan("collision-vs-broadcast-domains", "Collision Domains vs Broadcast Domains", "Beginner")
        ]
    },
    {
        "name": "IP Addressing, Subnetting & Next-Gen IP",
        "subtopics": [
            pub("what-is-an-ip-address"),
            pub("public-vs-private-ip-address"),
            pub("what-is-a-subnet-mask"),
            pub("subnetting-basics"),
            pub("ipv6-fundamentals"),
            plan("vlsm-variable-length-subnet-masking", "VLSM (Variable Length Subnet Masking) In Depth", "Intermediate"),
            plan("classful-vs-classless-addressing", "Classful vs Classless (CIDR) Addressing Architecture", "Intermediate"),
            plan("ipv6-addressing-and-slaac", "IPv6 Addressing, SLAAC & Global Unicast Architecture", "Intermediate"),
            plan("ipv6-transition-dual-stack-and-tunneling", "IPv6 Transition Strategies: Dual Stack, 6to4 & NAT64", "Advanced")
        ]
    },
    {
        "name": "Ethernet, Switching & VLAN Architecture",
        "subtopics": [
            pub("what-is-vlan"),
            pub("access-port-vs-trunk-port"),
            pub("spanning-tree-protocol-explained"),
            pub("lacp-link-aggregation-explained"),
            pub("advanced-vlan-troubleshooting"),
            plan("ieee-802-1q-vlan-tagging-deep-dive", "IEEE 802.1Q VLAN Tagging & Frame Encapsulation", "Intermediate"),
            plan("rapid-spanning-tree-rstp-802-1w", "Rapid Spanning Tree (RSTP 802.1w) & MSTP Explained", "Intermediate"),
            plan("switch-port-security-and-mac-filtering", "Switch Port Security & Dynamic MAC Limiting", "Intermediate"),
            plan("chassis-stacking-and-switch-virtualization", "Switch Stacking Architecture & Virtual Chassis", "Advanced")
        ]
    },
    {
        "name": "Routing Protocols, NAT & Gateway Redundancy",
        "subtopics": [
            pub("what-is-routing"),
            pub("routing-table-explained"),
            pub("what-is-a-default-gateway"),
            pub("static-vs-dynamic-routing"),
            pub("what-is-arp"),
            pub("what-is-nat"),
            pub("ospf-basics"),
            pub("bgp-basics"),
            pub("vrrp-hsrp-gateway-redundancy"),
            plan("port-address-translation-pat-deep-dive", "PAT (Port Address Translation / NAT Overload) Deep Dive", "Intermediate")
        ]
    },
    {
        "name": "Transport Protocols, Handshakes & Ports",
        "subtopics": [
            pub("tcp-vs-udp"),
            pub("common-network-ports"),
            pub("icmp-explained"),
            pub("mtu-and-mss-explained"),
            plan("tcp-three-way-handshake-and-teardown", "TCP Three-Way Handshake & Connection Teardown Flow", "Intermediate"),
            plan("tcp-flow-control-sliding-window-and-buffers", "TCP Flow Control, Window Sizing & Buffer Management", "Intermediate"),
            plan("tcp-congestion-control-algorithms", "TCP Congestion Control Algorithms (Tahoe, Reno, BBR)", "Advanced")
        ]
    },
    {
        "name": "DNS, DHCP & Core Network Services",
        "subtopics": [
            pub("what-is-dns"),
            pub("what-is-dhcp"),
            pub("dns-record-types-explained"),
            pub("dhcp-relay-ip-helper-explained"),
            plan("dns-resolution-iterative-vs-recursive-queries", "DNS Resolution Process: Iterative vs Recursive Queries", "Intermediate"),
            plan("dhcp-dora-process-and-options-architecture", "DHCP DORA Process & Essential Scope Options (Option 3, 6, 66)", "Intermediate"),
            plan("reverse-dns-and-ptr-record-architecture", "Reverse DNS Lookups, PTR Records & In-Addr.Arpa", "Intermediate"),
            plan("network-time-protocol-ntp-synchronization", "Network Time Protocol (NTP) Hierarchy & Stratum Layers", "Intermediate")
        ]
    },
    {
        "name": "Wireless Networking (Wi-Fi)",
        "subtopics": [
            pub("wi-fi-2-4-ghz-vs-5-ghz-vs-6-ghz"),
            plan("wi-fi-standards-evolution-802-11ax-wi-fi-6-6e-7", "Wi-Fi Standards Evolution: 802.11ax (Wi-Fi 6/6E) to Wi-Fi 7", "Beginner"),
            plan("wireless-access-points-and-controllers-wlc", "Wireless Access Points, CAPWAP & WLC Architecture", "Intermediate"),
            plan("wi-fi-security-wpa2-enterprise-vs-wpa3", "Wi-Fi Security: WPA2-Enterprise (802.1X) vs WPA3 SAE", "Intermediate"),
            plan("rf-channel-planning-and-interference-mitigation", "RF Channel Planning, Band Steering & Co-Channel Interference", "Intermediate"),
            plan("wireless-roaming-802-11r-k-v-standards", "Seamless Wireless Roaming Standards: 802.11r, 802.11k & 802.11v", "Advanced")
        ]
    },
    {
        "name": "Network Security, Firewalls & VPN Connectivity",
        "subtopics": [
            pub("access-control-lists-explained"),
            pub("stateful-firewall-explained"),
            pub("port-forwarding-and-dnat-explained"),
            pub("site-to-site-vpn-explained"),
            pub("remote-access-vpn-explained"),
            plan("next-generation-firewall-ngfw-deep-packet-inspection", "NGFW Architecture: Application Awareness & Deep Packet Inspection", "Intermediate"),
            plan("ipsec-protocol-suite-ah-esp-and-ikev2", "IPsec Protocol Suite: AH, ESP & IKEv2 Phase Negotiation", "Advanced"),
            plan("network-security-dmz-and-bastion-architecture", "DMZ Segmentation, Perimeter Security & Bastion Hosts", "Intermediate")
        ]
    },
    {
        "name": "Network Monitoring, Telemetry & Observability",
        "subtopics": [
            pub("snmp-explained"),
            pub("network-monitoring-fundamentals"),
            pub("wireshark-basics"),
            pub("syslog-explained"),
            pub("netflow-ipfix-explained"),
            pub("network-baseline-and-capacity-planning"),
            plan("snmp-v2c-vs-v3-security-and-usm", "SNMPv2c vs SNMPv3: Cryptographic Authentication & Privacy (USM)", "Intermediate"),
            plan("wireshark-tcp-packet-analysis-and-filter-syntax", "Wireshark Packet Analysis: Display Filters & TCP Stream Following", "Intermediate"),
            plan("flow-telemetry-sflow-vs-netflow-vs-ipfix", "Flow Telemetry Comparison: sFlow, NetFlow & IPFIX in Enterprise WAN", "Advanced")
        ]
    },
    {
        "name": "Network Performance & Diagnostic Troubleshooting",
        "subtopics": [
            pub("ping-explained"),
            pub("traceroute-explained"),
            pub("dns-troubleshooting-guide"),
            pub("dhcp-troubleshooting-guide"),
            pub("network-troubleshooting-workflow"),
            pub("packet-loss-troubleshooting"),
            pub("network-latency-troubleshooting"),
            pub("qos-explained"),
            pub("bandwidth-vs-throughput-explained"),
            pub("jitter-explained"),
            pub("duplex-mismatch-and-speed-negotiation"),
            pub("unicast-vs-broadcast-vs-multicast"),
            pub("vpn-troubleshooting-workflow"),
            pub("advanced-dns-troubleshooting"),
            pub("enterprise-network-troubleshooting-case-studies")
        ]
    }
]

# -------------------------------------------------------------
# 2. WINDOWS (78 topics: 3 published + 75 planned)
# -------------------------------------------------------------
WINDOWS_SECTIONS = [
    {
        "name": "Windows Architecture & Operating System Fundamentals",
        "subtopics": [
            pub("windows-operating-system-fundamentals"),
            plan("windows-user-mode-vs-kernel-mode-architecture", "User Mode vs Kernel Mode Architecture in Windows", "Intermediate"),
            plan("windows-nt-kernel-and-executive-subsystems", "Windows NT Kernel, HAL & Executive Subsystems", "Advanced"),
            plan("windows-uefi-boot-process-from-post-to-login", "Windows UEFI Boot Process: From POST to Desktop Login", "Intermediate"),
            plan("windows-registry-architecture-and-root-hives", "Windows Registry Architecture: Root Hives & System Keys", "Intermediate"),
            plan("windows-syswow64-and-64bit-os-redirection", "32-bit vs 64-bit Windows Architecture: SysWOW64 & Redirection", "Intermediate"),
            plan("windows-system-environment-variables-configuration", "Windows System & User Environment Variables Configuration", "Beginner"),
            plan("windows-filesystems-ntfs-vs-refs-architecture", "Windows Filesystems Architecture: NTFS vs ReFS", "Intermediate")
        ]
    },
    {
        "name": "Command Prompt & Administrative Utilities",
        "subtopics": [
            pub("windows-command-prompt-basics"),
            plan("windows-batch-scripting-fundamentals-for-sysadmins", "Windows Batch (.bat) Scripting Fundamentals for Sysadmins", "Beginner"),
            plan("windows-diskpart-command-line-disk-management", "DiskPart Command-Line Disk Management & Partitioning", "Intermediate"),
            plan("windows-robocopy-advanced-file-replication-guide", "Robocopy Advanced File Replication, Mirroring & Multithreading", "Intermediate"),
            plan("windows-netsh-command-line-network-administration", "Netsh Command-Line Network Interface & Firewall Administration", "Intermediate"),
            plan("windows-system-file-checker-sfc-and-dism-repair", "System File Checker (SFC) and DISM Component Store Repair", "Beginner"),
            plan("windows-chkdsk-and-filesystem-integrity-management", "Chkdsk & Volume Dirty Bit Filesystem Integrity Diagnostics", "Beginner"),
            plan("windows-wmic-and-command-line-management", "Windows Management Instrumentation Command-Line (WMIC) Essentials", "Intermediate")
        ]
    },
    {
        "name": "PowerShell Administration & Automation",
        "subtopics": [
            pub("powershell-fundamentals-for-administrators"),
            plan("powershell-pipeline-object-manipulation-and-filtering", "PowerShell Pipeline Architecture & Object Filtering (Where/Select)", "Intermediate"),
            plan("powershell-providers-and-psdrives-management", "PowerShell Providers & PSDrives: Interfacing with Registry & Certs", "Intermediate"),
            plan("powershell-execution-policies-and-script-signing", "PowerShell Execution Policies, Scope & Code Signing", "Intermediate"),
            plan("powershell-remoting-winrm-and-pssession-architecture", "PowerShell Remoting: WinRM Configuration & Enter-PSSession", "Intermediate"),
            plan("powershell-modules-and-psgallery-package-management", "PowerShell Modules, Repositories & PSGallery Package Management", "Intermediate"),
            plan("powershell-robust-error-handling-try-catch-finally", "Robust Error Handling in PowerShell: Try/Catch/Finally & ErrorAction", "Intermediate"),
            plan("powershell-advanced-functions-and-custom-cmdlet-authoring", "Authoring Advanced Functions & Reusable Cmdlets in PowerShell", "Advanced"),
            plan("powershell-cim-wmi-queries-with-get-ciminstance", "Querying Windows Telemetry with Get-CimInstance & CIM Sessions", "Intermediate")
        ]
    },
    {
        "name": "Identity, Local Security & NTFS Permissions",
        "subtopics": [
            plan("windows-local-users-and-groups-sam-database", "Windows Local Accounts & Security Accounts Manager (SAM) Database", "Beginner"),
            plan("windows-user-account-control-uac-architecture", "User Account Control (UAC) Architecture & Token Elevation", "Intermediate"),
            plan("windows-ntfs-permissions-vs-share-permissions", "NTFS Permissions vs Share Permissions: Calculating Effective Access", "Intermediate"),
            plan("windows-ntfs-inheritance-ownership-and-takeown", "NTFS Inheritance, Explicit ACLs, Ownership & Takeown Workflows", "Intermediate"),
            plan("windows-credential-manager-and-stored-vaults", "Windows Credential Manager Architecture & Stored Enterprise Vaults", "Beginner"),
            plan("windows-encrypting-file-system-efs-and-recovery-agent", "Encrypting File System (EFS) Architecture & Data Recovery Agents", "Intermediate"),
            plan("windows-local-security-policy-secpol-hardening", "Windows Local Security Policy (secpol.msc) Hardening Baselines", "Intermediate"),
            plan("windows-access-control-lists-icacls-command-line", "Managing File ACLs from the Command Line with icacls", "Intermediate")
        ]
    },
    {
        "name": "Processes, Services & Task Scheduling",
        "subtopics": [
            plan("windows-services-architecture-and-sc-utility", "Windows Services Architecture & Service Controller (sc.exe)", "Intermediate"),
            plan("windows-task-scheduler-automation-and-triggers", "Windows Task Scheduler: Advanced Triggers, Actions & Automation", "Beginner"),
            plan("windows-process-threads-handles-and-lifecycle", "Windows Process Lifecycle: Threads, Handles & Memory Allocations", "Intermediate"),
            plan("windows-task-manager-advanced-analysis-for-admins", "Task Manager Advanced Metrics, Startup Impact & Resource Allocation", "Beginner"),
            plan("windows-managed-service-accounts-and-virtual-accounts", "Virtual Accounts & Group Managed Service Accounts (gMSA)", "Advanced"),
            plan("windows-sysinternals-autoruns-deep-dive", "Sysinternals Autoruns: Inspecting Startup Persistence & Malware Hooks", "Intermediate"),
            plan("windows-resource-monitor-deep-dive-for-sysadmins", "Resource Monitor Deep Dive: Disk I/O, Network & CPU Contention", "Intermediate")
        ]
    },
    {
        "name": "Windows Networking & Remote Access",
        "subtopics": [
            plan("windows-tcp-ip-stack-and-adapter-configuration", "Windows TCP/IP Stack Configuration & Adapter Binding Order", "Beginner"),
            plan("windows-dns-client-resolution-and-hosts-file", "Windows DNS Client Cache, Hosts File Behavior & Multi-Homing", "Intermediate"),
            plan("windows-dhcp-client-lifecycle-and-autonet-apipa", "Windows DHCP Client Lease Renewal & APIPA (169.254.x.x) Fallback", "Beginner"),
            plan("windows-server-message-block-smb-file-sharing", "Server Message Block (SMB 3.1.1) Architecture, Shares & Signing", "Intermediate"),
            plan("windows-remote-desktop-protocol-rdp-configuration", "Remote Desktop Protocol (RDP) Configuration, Port & NLA Security", "Intermediate"),
            plan("windows-network-location-profiles-domain-private-public", "Windows Network Location Profiles: Domain, Private & Public Rules", "Beginner"),
            plan("windows-remote-management-winrm-https-listener-setup", "Configuring Secure WinRM HTTPS Listeners with Certificates", "Advanced"),
            plan("windows-remote-assistance-and-quick-assist-administration", "Enterprise Remote Assistance & Quick Assist Support Architecture", "Beginner")
        ]
    },
    {
        "name": "Endpoint Security, Defender & BitLocker",
        "subtopics": [
            plan("windows-defender-antivirus-enterprise-configuration", "Microsoft Defender Antivirus: Scanning Engines & Exclusions", "Intermediate"),
            plan("windows-defender-firewall-with-advanced-security", "Windows Defender Firewall with Advanced Security: Rules & Profiles", "Intermediate"),
            plan("windows-bitlocker-drive-encryption-and-tpm-architecture", "BitLocker Drive Encryption Architecture & TPM 2.0 Integration", "Intermediate"),
            plan("windows-bitlocker-recovery-keys-and-ad-backup", "BitLocker Recovery Password Backup to Active Directory and Entra ID", "Intermediate"),
            plan("windows-attack-surface-reduction-asr-rules-implementation", "Attack Surface Reduction (ASR) Rules Implementation & Tuning", "Advanced"),
            plan("windows-credential-guard-and-virtualization-based-security", "Credential Guard & Virtualization-Based Security (VBS) Architecture", "Advanced"),
            plan("windows-applocker-and-application-control-policies", "Windows AppLocker & Windows Defender Application Control (WDAC)", "Advanced"),
            plan("windows-hello-for-business-and-fido2-authentication", "Windows Hello for Business Architecture & FIDO2 Enterprise Sign-in", "Intermediate")
        ]
    },
    {
        "name": "Active Directory Domain Join & Group Policy",
        "subtopics": [
            plan("windows-active-directory-domain-join-prerequisites-workflow", "Active Directory Domain Join: Prerequisites, DNS & Troubleshooting", "Intermediate"),
            plan("windows-group-policy-processing-order-lsdou", "Group Policy Processing Order: Local, Site, Domain & OU (LSDOU)", "Intermediate"),
            plan("windows-group-policy-troubleshooting-gpupdate-gpresult", "Group Policy Diagnostics: gpupdate /force & gpresult /h Reports", "Intermediate"),
            plan("windows-local-group-policy-editor-gpedit-configuration", "Local Group Policy Editor (gpedit.msc) Configuration & Staging", "Beginner"),
            plan("windows-roaming-profiles-and-folder-redirection", "Enterprise User Profiles: Roaming Profiles & Folder Redirection", "Intermediate"),
            plan("windows-ad-domain-controller-discovery-dc-locator", "Domain Controller Locator (DC Locator) Process & SRV Records", "Advanced"),
            plan("windows-group-policy-preferences-vs-policies-architecture", "Group Policy Preferences (GPP) vs Traditional Administrative Policies", "Intermediate")
        ]
    },
    {
        "name": "Enterprise Updates, Deployment & Management",
        "subtopics": [
            plan("windows-update-architecture-and-servicing-channels", "Windows Update Architecture: Component-Based Servicing & Cumulative Updates", "Beginner"),
            plan("windows-wsus-client-configuration-and-group-policies", "WSUS Client Group Policy Configuration & Reporting Frequency", "Intermediate"),
            plan("windows-update-for-business-wufb-deployment-rings", "Windows Update for Business (WUfB) Deployment Rings & Deferral Policies", "Intermediate"),
            plan("windows-admin-center-installation-and-gateway-setup", "Windows Admin Center (WAC) Installation, Gateway Setup & Extensions", "Intermediate"),
            plan("windows-sysprep-and-generalize-imaging-workflow", "Sysprep System Preparation Tool: Generalizing Images for Cloning", "Intermediate"),
            plan("windows-unattended-installation-answer-files-unattend-xml", "Automated Windows Deployment: Authoring Unattend.xml Answer Files", "Advanced"),
            plan("windows-print-management-and-print-spooler-architecture", "Windows Print Management: Print Spooler Architecture & Isolation", "Intermediate")
        ]
    },
    {
        "name": "Diagnostics, Event Logs & System Troubleshooting",
        "subtopics": [
            plan("windows-event-viewer-architecture-and-standard-logs", "Windows Event Viewer: System, Application & Security Log Architecture", "Beginner"),
            plan("windows-event-log-custom-views-and-xml-queries", "Authoring Event Viewer Custom Views & XPath XML Filtering Queries", "Intermediate"),
            plan("windows-reliability-monitor-for-stability-trending", "Windows Reliability Monitor for Hardware & Software Stability Indexing", "Beginner"),
            plan("windows-performance-monitor-perfmon-data-collector-sets", "Performance Monitor (PerfMon): Counter Logs & Data Collector Sets", "Intermediate"),
            plan("windows-bsod-analysis-and-memory-dump-configuration", "Windows BSOD Crash Dump Configuration: Small, Kernel & Complete Dumps", "Intermediate"),
            plan("windows-windbg-basics-for-analyzing-kernel-memory-dumps", "WinDbg Crash Analysis: Symbol Configuration & !analyze -v Debugging", "Advanced"),
            plan("windows-recovery-environment-winre-command-prompt-tools", "Windows Recovery Environment (WinRE) Diagnostics & BCD Repair", "Intermediate"),
            plan("windows-safe-mode-and-clean-boot-troubleshooting", "Safe Mode vs Clean Boot: Isolating Third-Party Driver Conflicts", "Beginner")
        ]
    }
]

# -------------------------------------------------------------
# 3. LINUX (78 topics: 3 published + 75 planned)
# -------------------------------------------------------------
LINUX_SECTIONS = [
    {
        "name": "Linux Architecture & System Fundamentals",
        "subtopics": [
            pub("linux-operating-system-fundamentals"),
            plan("linux-kernel-space-vs-user-space-architecture", "Kernel Space vs User Space Architecture & System Call Interface", "Intermediate"),
            plan("linux-system-initialization-grub-to-systemd-boot-flow", "Linux Boot Process Flow: UEFI, GRUB2, Vmlinuz, Initramfs & Systemd", "Intermediate"),
            plan("linux-proc-and-sys-virtual-filesystems-architecture", "Virtual Filesystems: Understanding /proc, /sys and Kernel Parameters", "Intermediate"),
            plan("linux-shared-libraries-and-ldconfig-management", "Shared Libraries, Dynamic Linker (ld.so) & ldconfig Administration", "Intermediate"),
            plan("linux-kernel-modules-management-lsmod-modprobe", "Managing Kernel Modules: lsmod, modprobe, insmod & /etc/modules-load.d", "Intermediate"),
            plan("linux-systemd-targets-and-runlevels-migration", "Systemd Targets vs Traditional SysV Runlevels (multi-user vs graphical)", "Beginner"),
            plan("linux-sysctl-kernel-runtime-parameter-tuning", "Tuning Kernel Runtime Parameters with sysctl and /etc/sysctl.conf", "Advanced")
        ]
    },
    {
        "name": "Filesystem, Storage & Volume Management",
        "subtopics": [
            pub("linux-filesystem-hierarchy-explained"),
            plan("linux-disk-partitioning-fdisk-gdisk-parted-guide", "Disk Partitioning Architecture: fdisk, gdisk (GPT) and parted", "Intermediate"),
            plan("linux-filesystems-comparison-ext4-xfs-btrfs", "Linux Native Filesystems Compared: ext4, XFS and Btrfs Features", "Intermediate"),
            plan("linux-mounting-filesystems-and-etc-fstab-syntax", "Mounting Filesystems, UUIDs & /etc/fstab Configuration Rules", "Beginner"),
            plan("linux-lvm-architecture-physical-volumes-volume-groups", "Logical Volume Manager (LVM) Architecture: PV, VG and LV Provisioning", "Intermediate"),
            plan("linux-lvm-dynamic-volume-resizing-and-snapshots", "LVM Dynamic Volume Extension, Filesystem Resizing & Snapshots", "Intermediate"),
            plan("linux-disk-usage-monitoring-df-du-and-inode-exhaustion", "Storage Space & Inode Monitoring: df, du, ncdu & Inode Exhaustion", "Beginner"),
            plan("linux-swap-space-creation-tuning-and-swappiness", "Linux Swap Space Provisioning, Swap Files & Swappiness Optimization", "Intermediate"),
            plan("linux-filesystem-integrity-checking-with-fsck", "Filesystem Integrity Diagnostics & Repair with fsck and e2fsck", "Intermediate")
        ]
    },
    {
        "name": "Bash Shell Scripting & Command-Line Utilities",
        "subtopics": [
            pub("essential-linux-terminal-commands"),
            plan("linux-standard-streams-redirection-and-pipes", "Standard Streams (stdin, stdout, stderr), Pipes & Redirection Operators", "Beginner"),
            plan("linux-text-processing-grep-cut-sort-uniq-tr", "Core Text Processing Utilities: grep, cut, sort, uniq, and tr", "Beginner"),
            plan("linux-stream-editor-sed-practical-guide", "Stream Editor (sed) Fundamentals: Search, Replace & In-Place Editing", "Intermediate"),
            plan("linux-awk-text-processing-and-data-extraction", "Pattern Scanning & Text Processing Language (awk) for Sysadmins", "Intermediate"),
            plan("bash-variables-environment-variables-and-scoping", "Bash Variables, Quoting Rules, Export & Subshell Environment Scoping", "Beginner"),
            plan("bash-control-structures-conditionals-loops-case", "Bash Script Control Flow: if/elif/else, for/while loops, and case statements", "Intermediate"),
            plan("bash-script-exit-codes-and-robust-error-handling", "Exit Codes, Error Handling (set -euo pipefail) & Trap Signals in Bash", "Intermediate"),
            plan("bash-shell-environment-customization-bashrc-profile", "Customizing the Shell: Command Aliases, Functions & ~/.bashrc vs /etc/profile", "Beginner")
        ]
    },
    {
        "name": "Users, Groups & Linux Access Controls",
        "subtopics": [
            plan("linux-user-and-group-account-administration", "User and Group Account Administration: useradd, usermod, groupadd & /etc/passwd", "Beginner"),
            plan("linux-standard-file-permissions-chmod-chown", "Standard Linux File Permissions: Read, Write, Execute (chmod & chown)", "Beginner"),
            plan("linux-default-permissions-and-umask-calculation", "Default Permission Masking: Understanding and Calculating umask Values", "Intermediate"),
            plan("linux-special-permissions-suid-sgid-and-sticky-bit", "Special Permissions Deep Dive: SUID, SGID & the Sticky Bit on Directories", "Intermediate"),
            plan("linux-sudo-configuration-and-visudo-administration", "Sudoers Administration: Configuring Least Privilege Rules with visudo", "Intermediate"),
            plan("linux-posix-access-control-lists-getfacl-setfacl", "POSIX Access Control Lists (ACLs): Fine-Grained Permissions with setfacl", "Intermediate"),
            plan("linux-pluggable-authentication-modules-pam-basics", "Pluggable Authentication Modules (PAM) Architecture & Configuration Stack", "Advanced")
        ]
    },
    {
        "name": "Process Management, Systemd & Scheduling",
        "subtopics": [
            plan("linux-process-monitoring-with-ps-top-and-htop", "Process Monitoring & Resource Inspection with ps, top, and htop", "Beginner"),
            plan("linux-process-signaling-and-termination-kill-pkill", "Process Termination & POSIX Signals: SIGTERM, SIGKILL, SIGHUP (kill/pkill)", "Beginner"),
            plan("linux-systemd-service-units-creation-and-control", "Authoring Systemd Service Units: Unit Files, Dependencies & systemctl", "Intermediate"),
            plan("linux-cron-scheduled-tasks-and-crontab-syntax", "Automating Scheduled Tasks with Cron, Crontab Syntax & /etc/cron.*", "Beginner"),
            plan("linux-systemd-timer-units-vs-traditional-cron", "Modern Scheduling with Systemd Timer Units vs Traditional Cron", "Intermediate"),
            plan("linux-process-prioritization-nice-and-renice", "Process Scheduling Priority: Nice Values, Renice & Kernel Niceness", "Intermediate"),
            plan("linux-background-job-control-nohup-screen-tmux", "Terminal Multiplexers & Persistent Background Jobs: nohup, screen & tmux", "Intermediate")
        ]
    },
    {
        "name": "Linux Networking, DNS & Remote Access (SSH)",
        "subtopics": [
            plan("linux-iproute2-network-configuration-ip-addr-link", "Modern Network Configuration with iproute2: ip addr, ip link & ip route", "Intermediate"),
            plan("linux-socket-inspection-with-ss-and-netstat", "Network Socket Inspection & Port Listening States with ss and lsof", "Beginner"),
            plan("linux-dns-client-configuration-resolv-conf-systemd-resolved", "DNS Client Configuration: /etc/resolv.conf, nsswitch & systemd-resolved", "Intermediate"),
            plan("linux-openssh-server-configuration-and-hardening", "OpenSSH Server Administration: sshd_config Configuration & Port Hardening", "Intermediate"),
            plan("linux-ssh-key-based-authentication-and-agent-forwarding", "SSH Key-Based Authentication: Ed25519 Keys, ssh-copy-id & Agent Forwarding", "Intermediate"),
            plan("linux-secure-file-transfer-scp-sftp-rsync", "Secure Remote File Transfer: scp, sftp & High-Performance rsync Over SSH", "Beginner"),
            plan("linux-network-troubleshooting-tools-traceroute-mtr-nc", "Linux Network Diagnostics: mtr, traceroute, dig, and netcat (nc)", "Intermediate")
        ]
    },
    {
        "name": "Package Management & Software Repositories",
        "subtopics": [
            plan("linux-debian-ubuntu-package-management-apt-dpkg", "Debian/Ubuntu Package Management: apt, apt-cache & dpkg Administration", "Beginner"),
            plan("linux-rhel-rocky-package-management-dnf-rpm", "RHEL/Rocky Linux Package Management: dnf, yum, and rpm Commands", "Beginner"),
            plan("linux-custom-software-repositories-and-gpg-keys", "Managing Custom Software Repositories, PPA Keys & Third-Party Repos", "Intermediate"),
            plan("linux-compiling-software-from-source-make-gcc", "Compiling Software from Source: tarballs, ./configure, make, and make install", "Intermediate"),
            plan("linux-archive-utilities-tar-gzip-bzip2-xz", "Archive & Compression Utilities: Mastering tar, gzip, bzip2, and xz", "Beginner"),
            plan("linux-snap-and-flatpak-containerized-package-management", "Containerized Application Packages: Snap and Flatpak Administration", "Intermediate"),
            plan("linux-kernel-upgrades-and-old-kernel-cleanup", "Enterprise Kernel Updates, DKMS Drivers & Safe Old Kernel Cleanup", "Intermediate")
        ]
    },
    {
        "name": "System Monitoring, Logging & Performance Tuning",
        "subtopics": [
            plan("linux-systemd-journalctl-log-analysis-and-filtering", "Systemd Journal Architecture & Advanced journalctl Filtering Queries", "Intermediate"),
            plan("linux-traditional-syslog-and-logrotate-management", "System Logging with rsyslog & Log File Rotation Policies with logrotate", "Intermediate"),
            plan("linux-system-resource-monitoring-vmstat-iostat-sar", "System Telemetry Tools: vmstat, iostat, mpstat, and sysstat (sar)", "Intermediate"),
            plan("linux-memory-management-buffers-caches-oom-killer", "Linux Memory Management: Buffers, Page Cache & Out-Of-Memory (OOM) Killer", "Intermediate"),
            plan("linux-cpu-load-average-analysis-and-bottlenecks", "Demystifying Linux CPU Load Averages & Identifying Performance Bottlenecks", "Intermediate"),
            plan("linux-io-schedulers-and-storage-performance-tuning", "Linux Storage I/O Schedulers (mq-deadline, bfq, none) & SSD Optimization", "Advanced"),
            plan("linux-network-performance-tuning-tcp-buffer-sizes", "Linux Network Stack Performance Tuning: TCP Window & Socket Buffer Sizes", "Advanced")
        ]
    },
    {
        "name": "Linux Security, Firewalls & Hardening",
        "subtopics": [
            plan("linux-ufw-uncomplicated-firewall-administration", "Uncomplicated Firewall (UFW) Administration & Port Rule Management", "Beginner"),
            plan("linux-firewalld-zones-and-services-management", "Enterprise Firewall Management with firewalld: Zones, Services & Rich Rules", "Intermediate"),
            plan("linux-selinux-fundamentals-modes-contexts-booleans", "SELinux Fundamentals: Enforcing Modes, Security Contexts & Booleans", "Intermediate"),
            plan("linux-apparmor-profiles-and-enforcement-in-ubuntu", "AppArmor Security Profiles: Complain vs Enforce Modes in Debian/Ubuntu", "Intermediate"),
            plan("linux-fail2ban-brute-force-protection-setup", "Defending SSH & Web Services from Brute-Force Attacks with Fail2ban", "Intermediate"),
            plan("linux-securing-grub-bootloader-password-protection", "Hardening the Bootloader: Securing GRUB2 with Password Authentication", "Intermediate"),
            plan("linux-file-integrity-monitoring-with-aide", "Host-Based File Integrity Monitoring with Advanced Intrusion Detection (AIDE)", "Advanced")
        ]
    },
    {
        "name": "Boot Process, Recovery & Advanced Troubleshooting",
        "subtopics": [
            plan("linux-troubleshooting-boot-failures-grub-emergency-mode", "Troubleshooting Boot Failures: Navigating GRUB Rescue & Emergency Mode", "Intermediate"),
            plan("linux-rescue-target-and-single-user-mode-boot", "Booting into Linux Rescue Target, Emergency Mode & Single-User Mode", "Intermediate"),
            plan("linux-root-password-recovery-via-grub-init-sh", "Root Password Reset Workflow: Kernel Parameter Editing (rd.break / init=/bin/sh)", "Intermediate"),
            plan("linux-diagnosing-read-only-filesystem-remounts", "Diagnosing and Resolving Read-Only Filesystem Remounts & Disk Errors", "Intermediate"),
            plan("linux-troubleshooting-ssh-connection-failures-verbose-mode", "Troubleshooting SSH Failures: Diagnosing Permissions & Verbose Mode (ssh -vvv)", "Beginner"),
            plan("linux-chroot-environment-repair-from-live-usb", "Chrooting into Broken Linux Installations from Live Rescue Media", "Intermediate"),
            plan("linux-system-crash-dump-analysis-kdump-and-crash", "Analyzing Kernel Panic Dumps with kdump and the crash Utility", "Advanced")
        ]
    }
]

# -------------------------------------------------------------
# 4. SERVERS (78 topics: 3 published + 75 planned)
# -------------------------------------------------------------
SERVERS_SECTIONS = [
    {
        "name": "Server Hardware & Enterprise Architecture",
        "subtopics": [
            pub("what-is-a-server"),
            plan("server-raid-levels-explained-0-1-5-6-10", "RAID Levels Explained: 0, 1, 5, 6, 10 & Nested Arrays", "Beginner"),
            plan("server-form-factors-rack-blade-and-tower-systems", "Server Form Factors: 1U/2U/4U Rack Servers, Blades & Pedestals", "Beginner"),
            plan("server-redundant-power-supplies-and-pdu-distribution", "Redundant Power Supplies (PSU, 1+1, 2+2) & Rack PDU Power Phase Balancing", "Beginner"),
            plan("server-ecc-memory-and-registered-rdimms-architecture", "Enterprise Memory Architecture: ECC, Registered RDIMMs & Memory Sparing", "Intermediate"),
            plan("server-numa-nodes-and-cpu-socket-memory-affinity", "Non-Uniform Memory Access (NUMA) Architecture & Socket Memory Affinity", "Advanced"),
            plan("server-out-of-band-management-ipmi-idrac-ilo", "Out-of-Band Remote Management: IPMI, Dell iDRAC & HPE iLO", "Intermediate"),
            plan("server-hardware-raid-controllers-cache-and-bbu", "Hardware RAID Controllers: Write-Back Caching, Battery Backup (BBU) & Flash", "Intermediate"),
            plan("server-bios-uefi-firmware-updates-and-secure-boot", "Server BIOS/UEFI Firmware Upgrades & Enterprise Secure Boot Policies", "Intermediate")
        ]
    },
    {
        "name": "Operating System Platforms & Server Deployment",
        "subtopics": [
            pub("windows-server-fundamentals"),
            pub("linux-server-fundamentals"),
            plan("windows-server-editions-datacenter-vs-standard-licensing", "Windows Server Editions: Datacenter vs Standard Licensing & CALs", "Beginner"),
            plan("windows-server-core-headless-deployment-and-remote-management", "Windows Server Core: Headless Installation & Remote Administration", "Intermediate"),
            plan("bare-metal-server-provisioning-pxe-boot-and-wds", "Bare-Metal Server Provisioning via PXE Boot & Windows Deployment Services", "Intermediate"),
            plan("linux-enterprise-server-distributions-rhel-vs-ubuntu-server", "Enterprise Linux Server Platforms Compared: RHEL vs Ubuntu Server", "Beginner"),
            plan("automated-linux-server-deployment-with-cloud-init-and-kickstart", "Automated Linux Server Provisioning with Kickstart and Cloud-Init", "Intermediate"),
            plan("server-storage-pools-and-direct-attached-storage-das", "Managing Direct-Attached Storage (DAS) Enclosures & Storage Pools", "Intermediate")
        ]
    },
    {
        "name": "Active Directory Domain Services & Enterprise Identity",
        "subtopics": [
            plan("active-directory-domain-services-ad-ds-architecture", "Active Directory Domain Services (AD DS) Architectural Components", "Intermediate"),
            plan("active-directory-domain-controller-promotion-and-demotion", "Domain Controller Promotion (dcpromo), Staging & Demotion Workflows", "Intermediate"),
            plan("active-directory-fsmo-roles-and-seizure-procedures", "Flexible Single Master Operation (FSMO) Roles & Emergency Role Seizure", "Intermediate"),
            plan("active-directory-replication-topology-sites-and-bridgehead-servers", "AD Replication Topology: Sites, Subnets, Cost & Bridgehead Servers", "Intermediate"),
            plan("active-directory-global-catalog-and-schema-partitions", "Active Directory Directory Partitions: Schema, Configuration & Global Catalog", "Advanced"),
            plan("active-directory-group-policy-central-store-admx-templates", "Group Policy Central Store Setup with Administrative Templates (.admx)", "Intermediate"),
            plan("active-directory-recycle-bin-and-authoritative-restore", "Active Directory Recycle Bin & Authoritative vs Non-Authoritative Restore", "Intermediate"),
            plan("active-directory-read-only-domain-controllers-rodc-in-branch-offices", "Read-Only Domain Controllers (RODC) & Password Replication Policies", "Intermediate")
        ]
    },
    {
        "name": "Core Infrastructure Services (DNS & DHCP)",
        "subtopics": [
            plan("enterprise-dns-server-architecture-and-zone-types", "Enterprise DNS Server Architecture: Forward, Reverse, Primary & Secondary Zones", "Intermediate"),
            plan("active-directory-integrated-dns-zones-and-secure-dynamic-updates", "AD-Integrated DNS Zones, Multi-Master Replication & Secure Dynamic Updates", "Intermediate"),
            plan("dns-server-forwarders-root-hints-and-conditional-forwarding", "DNS Forwarders, Root Hints & Conditional Forwarding for Cross-Domain Resolution", "Intermediate"),
            plan("enterprise-dhcp-server-installation-and-scope-options", "Enterprise DHCP Server Installation, Scope Design & Essential Options", "Beginner"),
            plan("enterprise-dhcp-failover-load-balancing-and-hot-standby", "DHCP Server Failover Architecture: Load Balancing vs Hot Standby Modes", "Intermediate"),
            plan("enterprise-dhcp-relay-agents-ip-helper-in-routed-networks", "DHCP Relay Agents & Cisco IP Helper Configuration in Routed Networks", "Intermediate"),
            plan("ip-address-management-ipam-architecture-and-capacity", "IP Address Management (IPAM) Architecture, Discovery & Tracking", "Intermediate")
        ]
    },
    {
        "name": "Virtualization & Enterprise Hypervisors",
        "subtopics": [
            plan("hypervisor-architecture-type-1-bare-metal-vs-type-2-hosted", "Hypervisor Architecture: Type 1 (Bare-Metal) vs Type 2 (Hosted)", "Beginner"),
            plan("vmware-esxi-installation-initial-setup-and-dcui", "VMware ESXi Installation, DCUI Setup & Direct Web Client Management", "Intermediate"),
            plan("vmware-vcenter-server-appliance-vcsa-architecture", "VMware vCenter Server Appliance (VCSA) Architecture & Single-Pane Management", "Intermediate"),
            plan("vmware-vsphere-clustering-drs-high-availability-and-vmotion", "VMware vSphere Clustering: vMotion, DRS Resource Balancing & High Availability", "Advanced"),
            plan("microsoft-hyper-v-architecture-and-virtual-switch-types", "Microsoft Hyper-V Architecture: Generation 2 VMs & Virtual Switch Types", "Intermediate"),
            plan("hyper-v-clustering-live-migration-and-csv-storage", "Hyper-V Failover Clustering, Cluster Shared Volumes (CSV) & Live Migration", "Advanced"),
            plan("proxmox-ve-cluster-architecture-and-kvm-lxc-management", "Proxmox VE Cluster Architecture, KVM Virtual Machines & LXC Containers", "Intermediate"),
            plan("virtual-machine-snapshots-vs-proper-enterprise-backups", "Virtual Machine Snapshots vs Enterprise Backups: Performance Pitfalls", "Beginner")
        ]
    },
    {
        "name": "Enterprise Storage, File Services & SAN/NAS",
        "subtopics": [
            plan("enterprise-storage-architectures-das-vs-nas-vs-san", "Enterprise Storage Architectures Compared: DAS vs NAS vs SAN", "Beginner"),
            plan("storage-area-networks-iscsi-targets-initiators-and-iqn", "iSCSI SAN Architecture: IQN Naming, LUN Provisioning & Initiator Setup", "Intermediate"),
            plan("fibre-channel-san-architecture-hba-zoning-and-wwn", "Fibre Channel (FC) SAN: HBAs, WWN Addressing & Fabric Switch Zoning", "Advanced"),
            plan("windows-file-server-smb-shares-caching-and-quota-management", "Windows File Server Resource Manager (FSRM): Quotas & File Screening", "Intermediate"),
            plan("linux-file-server-nfs-v3-v4-export-configuration", "Linux Network File System (NFS v3/v4) Exports & Client Mount Options", "Intermediate"),
            plan("distributed-file-system-dfs-namespaces-and-dfs-replication", "Distributed File System (DFS): Unified Namespaces & Multi-Site Replication", "Intermediate"),
            plan("storage-spaces-direct-s2d-and-hyper-converged-infrastructure", "Storage Spaces Direct (S2D) & Microsoft Hyper-Converged Infrastructure (HCI)", "Advanced"),
            plan("multipath-io-mpio-configuration-for-redundant-storage-paths", "Multipath I/O (MPIO) Configuration for Redundant SAN Path Failover", "Intermediate")
        ]
    },
    {
        "name": "High Availability, Clustering & Disaster Recovery",
        "subtopics": [
            plan("high-availability-clustering-principles-active-passive-vs-active-active", "High Availability Principles: Active-Passive vs Active-Active Architectures", "Intermediate"),
            plan("windows-server-failover-clustering-wsfc-architecture", "Windows Server Failover Clustering (WSFC) Architecture & Validation Tests", "Intermediate"),
            plan("cluster-quorum-models-witness-types-cloud-disk-file-share", "Cluster Quorum Models & Witness Architecture (Disk, File Share, Cloud Witness)", "Advanced"),
            plan("linux-high-availability-clustering-pacemaker-and-corosync", "Linux High Availability Clustering with Pacemaker, Corosync & Fencing (STONITH)", "Advanced"),
            plan("the-3-2-1-backup-rule-and-modern-ransomware-protection", "The 3-2-1-1-0 Backup Rule & Immutable Storage for Ransomware Protection", "Beginner"),
            plan("enterprise-backup-solutions-veeam-commvault-and-image-backups", "Enterprise Backup Methodologies: Full, Incremental, Differential & CBT", "Intermediate"),
            plan("disaster-recovery-planning-rto-rpo-and-business-continuity", "Disaster Recovery Planning: RTO, RPO & Business Impact Analysis (BIA)", "Intermediate"),
            plan("backup-verification-sandbox-recovery-testing-and-dr-drills", "Automated Backup Verification, Sandbox Testing & Disaster Recovery Drills", "Intermediate")
        ]
    },
    {
        "name": "Server Monitoring, Telemetry & Capacity Planning",
        "subtopics": [
            plan("server-hardware-health-monitoring-ipmi-snmp-traps", "Server Hardware Health Telemetry via IPMI Sensors & SNMP Traps", "Intermediate"),
            plan("centralized-server-metrics-collection-prometheus-and-grafana", "Centralized Metrics Collection with Prometheus Exporters & Grafana Dashboards", "Intermediate"),
            plan("windows-server-performance-baselines-perfmon-counters", "Windows Server Performance Baselines: Core Counters (CPU, Memory, Disk, Net)", "Intermediate"),
            plan("linux-server-performance-monitoring-sysstat-and-atop", "Linux Server Historical Performance Telemetry with atop and sysstat", "Intermediate"),
            plan("server-capacity-planning-forecasting-cpu-ram-storage-growth", "Server Capacity Planning: Modeling CPU, Memory & Storage Growth Curves", "Intermediate"),
            plan("hypervisor-resource-contention-cpu-ready-and-memory-ballooning", "Hypervisor Resource Contention: Diagnosing CPU Ready Time & Memory Ballooning", "Advanced"),
            plan("automated-server-alerting-incident-thresholds-and-pagerduty", "Automated Server Alerting: Threshold Configuration & On-Call Escalation", "Intermediate")
        ]
    },
    {
        "name": "Server Security, Hardening & Compliance",
        "subtopics": [
            plan("windows-server-security-baselines-and-cis-benchmark-hardening", "Windows Server Hardening via CIS Benchmarks & Microsoft Security Baselines", "Intermediate"),
            plan("linux-server-hardening-best-practices-and-system-bastioning", "Enterprise Linux Server Hardening: Disabling Unused Services & SUID Auditing", "Intermediate"),
            plan("group-managed-service-accounts-gmsa-architecture-and-setup", "Group Managed Service Accounts (gMSA): Passwordless Service Security", "Advanced"),
            plan("securing-server-remote-management-interfaces-winrm-and-ssh", "Securing Server Administrative Interfaces: TLS Listeners & Jump Boxes", "Intermediate"),
            plan("enterprise-server-patch-management-and-maintenance-windows", "Enterprise Server Patch Management Strategies & Zero-Downtime Rolling Updates", "Intermediate"),
            plan("active-directory-certificate-services-ad-cs-and-private-pki", "Active Directory Certificate Services (AD CS): Internal Enterprise PKI Hierarchy", "Advanced"),
            plan("server-firmware-security-tpm-and-hardware-root-of-trust", "Hardware Root of Trust: TPM 2.0, Secure Boot & Supply Chain Security", "Intermediate")
        ]
    },
    {
        "name": "Root-Cause Diagnostics & Server Troubleshooting",
        "subtopics": [
            plan("server-hardware-diagnostics-ecc-memory-errors-and-thermal-throttling", "Diagnosing Server Hardware Faults: Correctable ECC Errors & Thermal Throttling", "Intermediate"),
            plan("server-blue-screen-bsod-and-kernel-panic-root-cause-analysis", "Server Crash Post-Mortem: Analyzing Kernel Memory Dumps & Panic Stacks", "Advanced"),
            plan("troubleshooting-active-directory-replication-failures-repadmin", "Troubleshooting AD Replication Failures with repadmin & dcdiag", "Intermediate"),
            plan("troubleshooting-domain-controller-promotion-and-kerberos-errors", "Troubleshooting Domain Controller Promotion, DNS Failures & Kerberos Tickets", "Intermediate"),
            plan("diagnosing-hypervisor-host-and-virtual-disk-latency", "Diagnosing Storage Bottlenecks: Disk Latency (davg/cmd, kavg/cmd) in Hypervisors", "Advanced"),
            plan("resolving-cluster-split-brain-and-quorum-loss-scenarios", "Resolving Cluster Split-Brain, Fencing Loops & Quorum Loss Scenarios", "Advanced"),
            plan("systematic-root-cause-analysis-rca-methodology-for-server-outages", "Systematic Root Cause Analysis (RCA) Methodology & 5-Whys for System Outages", "Intermediate")
        ]
    }
]

# -------------------------------------------------------------
# 5. CYBERSECURITY (78 topics: 3 published + 75 planned)
# Strictly defensive enterprise security
# -------------------------------------------------------------
CYBERSECURITY_SECTIONS = [
    {
        "name": "Security Principles, Risk & Governance",
        "subtopics": [
            pub("cybersecurity-fundamentals"),
            plan("cia-triad-and-parkerian-hexad-in-enterprise-security", "The CIA Triad & Parkerian Hexad in Modern Enterprise Defense", "Beginner"),
            plan("threat-vulnerability-and-risk-mathematical-equation", "Threat, Vulnerability, and Risk: The Fundamental Calculation", "Beginner"),
            plan("defense-in-depth-strategy-and-layered-controls", "Defense-in-Depth Architecture: Layered Perimeter, Network & Host Controls", "Beginner"),
            plan("security-control-categories-preventative-detective-corrective", "Security Control Categories: Administrative, Technical, Physical & Compensating", "Beginner"),
            plan("nist-cybersecurity-framework-csf-2-0-core-functions", "NIST Cybersecurity Framework (CSF 2.0): Govern, Identify, Protect, Detect, Respond, Recover", "Intermediate"),
            plan("iso-iec-27001-isms-standard-and-compliance-overview", "ISO/IEC 27001 Standard: Information Security Management Systems (ISMS) Overview", "Intermediate"),
            plan("enterprise-attack-surface-management-and-discovery", "Enterprise Attack Surface Management (ASM) & Shadow IT Discovery", "Intermediate"),
            plan("data-classification-levels-and-sensitive-asset-inventory", "Data Classification Frameworks, Retention Rules & Asset Inventorying", "Beginner")
        ]
    },
    {
        "name": "Enterprise Identity & Access Management (IAM)",
        "subtopics": [
            pub("authentication-vs-authorization"),
            plan("principle-of-least-privilege-and-separation-of-duties", "Principle of Least Privilege (PoLP) and Separation of Duties in Administration", "Beginner"),
            plan("role-based-access-control-rbac-enterprise-architecture", "Role-Based Access Control (RBAC): Role Engineering & Permission Inheritance", "Beginner"),
            plan("attribute-based-access-control-abac-and-dynamic-policies", "Attribute-Based Access Control (ABAC): Contextual & Dynamic Access Policies", "Intermediate"),
            plan("privileged-access-management-pam-vaulting-and-session-recording", "Privileged Access Management (PAM): Credential Vaulting & Session Monitoring", "Intermediate"),
            plan("just-in-time-jit-privileged-access-and-ephemeral-credentials", "Just-In-Time (JIT) Administrative Elevation & Ephemeral Credential Provisioning", "Advanced"),
            plan("active-directory-administrative-tiering-and-bastion-models", "Active Directory Administrative Tiering (Tier 0, 1, 2) & Bastion Forest Architecture", "Advanced"),
            plan("service-account-security-and-automated-key-rotation", "Service Account Hardening, Kerberos SPN Security & Automated Key Rotation", "Intermediate")
        ]
    },
    {
        "name": "Authentication Protocols, MFA & Credential Security",
        "subtopics": [
            pub("multi-factor-authentication-explained"),
            plan("modern-password-policies-and-nist-800-63-guidelines", "Modern Password Security Policies: NIST SP 800-63B Passphrase Guidelines", "Beginner"),
            plan("mfa-vulnerabilities-totp-vs-sms-and-mfa-fatigue-attacks", "Evaluating MFA Strengths: TOTP vs Push Notifications vs SMS Interception", "Intermediate"),
            plan("fido2-webauthn-and-passwordless-authentication-architecture", "FIDO2 & WebAuthn Architecture: Phishing-Resistant Passwordless Authentication", "Intermediate"),
            plan("single-sign-on-sso-architecture-saml-2-0-and-oidc", "Enterprise Single Sign-On (SSO): SAML 2.0 Assertions vs OpenID Connect Tokens", "Intermediate"),
            plan("kerberos-authentication-architecture-and-tickets-flow", "Kerberos Authentication Protocol Flow: AS-REQ, TGT, TGS-REQ & Service Tickets", "Intermediate"),
            plan("defending-against-pass-the-hash-and-kerberoasting-attacks", "Defending Active Directory: Mitigating Pass-the-Hash & Kerberoasting Attacks", "Advanced"),
            plan("credential-stuffing-defense-and-password-spraying-mitigation", "Detecting and Mitigating Credential Stuffing & Low-and-Slow Password Spraying", "Intermediate")
        ]
    },
    {
        "name": "Endpoint Protection, Antivirus & EDR Architecture",
        "subtopics": [
            plan("next-generation-antivirus-ngav-vs-traditional-signatures", "Next-Gen Antivirus (NGAV): Behavioral Heuristics vs Traditional Signatures", "Beginner"),
            plan("endpoint-detection-and-response-edr-architecture-and-telemetry", "Endpoint Detection and Response (EDR): Sensor Architecture & Process Telemetry", "Intermediate"),
            plan("extended-detection-and-response-xdr-cross-domain-telemetry", "Extended Detection and Response (XDR): Correlating Identity, Cloud & Endpoint Signals", "Advanced"),
            plan("host-based-firewalls-and-endpoint-network-isolation", "Host-Based Firewalls & Automated Dynamic Endpoint Network Isolation", "Intermediate"),
            plan("endpoint-device-control-and-usb-removable-media-lockdown", "USB Peripheral Lockdown & Removable Media Encryption Policies", "Beginner"),
            plan("application-allowlisting-and-software-execution-policies", "Application Allowlisting (Default-Deny) Architecture and Software Whitelisting", "Intermediate"),
            plan("operating-system-security-baselines-and-cis-benchmark-auditing", "Implementing CIS Security Benchmarks for Automated Endpoint Hardening", "Intermediate")
        ]
    },
    {
        "name": "Network Defense, Firewalls & Microsegmentation",
        "subtopics": [
            plan("next-generation-firewall-ngfw-deep-packet-inspection-architecture", "Next-Generation Firewall (NGFW): Application Visibility & TLS Decryption", "Intermediate"),
            plan("network-microsegmentation-and-software-defined-perimeters", "Network Microsegmentation Architecture & Host-to-Host Encryption", "Advanced"),
            plan("demilitarized-zones-dmz-and-secure-perimeter-architecture", "Demilitarized Zone (DMZ) Architecture: Multi-Homed Firewalls & Bastion Proxies", "Intermediate"),
            plan("intrusion-detection-systems-ids-vs-intrusion-prevention-ips", "Intrusion Detection (IDS) vs Intrusion Prevention (IPS): Signature vs Anomaly Engines", "Intermediate"),
            plan("web-application-firewalls-waf-architecture-and-owasp-rules", "Web Application Firewalls (WAF): ModSecurity & Defending Against OWASP Top 10", "Intermediate"),
            plan("vpn-security-ipsec-vs-wireguard-vs-ssl-tls-tunnels", "VPN Cryptographic Security Compared: IPsec IKEv2, WireGuard, and OpenVPN", "Intermediate"),
            plan("securing-remote-desktop-gateway-and-bastion-access", "Hardening RDP Gateways, Guacamole Jumpboxes & Privileged Access Proxies", "Intermediate")
        ]
    },
    {
        "name": "Email Security & Anti-Phishing Defense",
        "subtopics": [
            plan("email-authentication-frameworks-spf-dkim-and-dmarc-deep-dive", "Email Authentication Protocols Deep Dive: SPF Syntax, DKIM Keys & DMARC Policies", "Intermediate"),
            plan("phishing-attack-vectors-spear-phishing-and-bec-anatomy", "Anatomy of Social Engineering: Spear Phishing, Whaling & Business Email Compromise", "Beginner"),
            plan("secure-email-gateways-seg-and-heuristic-filtering", "Secure Email Gateways (SEG): Behavioral Heuristics, URL Rewriting & Sandbox Inspection", "Intermediate"),
            plan("analyzing-malicious-email-headers-and-phishing-indicators", "Analyzing Email RFC 5322 Headers, Received Paths & Spoofed Return-Paths", "Intermediate"),
            plan("content-disarm-and-reconstruction-cdr-and-attachment-sandboxing", "Attachment Security: Dynamic Sandboxing & Content Disarm and Reconstruction (CDR)", "Intermediate"),
            plan("enterprise-phishing-reporting-and-automated-triage-workflows", "Enterprise Phishing Reporting Pipelines & Automated SOAR Mailbox Purging", "Intermediate"),
            plan("defending-against-lookalike-domains-and-typosquatting", "Defending Against Typosquatting, IDN Homograph Attacks & Lookalike Domains", "Intermediate")
        ]
    },
    {
        "name": "Vulnerability Management & Threat Intelligence",
        "subtopics": [
            plan("vulnerability-management-lifecycle-discovery-to-remediation", "The Vulnerability Management Lifecycle: Discovery, Prioritization, Remediation & Verification", "Beginner"),
            plan("cve-and-cvss-scoring-metrics-base-temporal-environmental", "Understanding CVE Identifiers, CVSS v3/v4 Vectors & Severity Scoring", "Beginner"),
            plan("vulnerability-scanning-architecture-authenticated-vs-unauthenticated", "Vulnerability Scanning Methodologies: Agent-Based vs Authenticated Network Scans", "Intermediate"),
            plan("vulnerability-prioritization-epss-and-known-exploited-vulnerabilities", "Prioritizing CVEs with Exploit Prediction Scoring (EPSS) & CISA KEV Catalog", "Intermediate"),
            plan("cyber-threat-intelligence-cti-strategic-tactical-operational", "Cyber Threat Intelligence (CTI): Strategic, Operational & Tactical Indicators", "Intermediate"),
            plan("mitre-att-ck-framework-navigating-tactics-techniques-procedures", "Navigating the MITRE ATT&CK Framework: Tactics, Techniques & Procedures (TTPs)", "Intermediate"),
            plan("indicators-of-compromise-iocs-vs-indicators-of-attack-ioas", "Indicators of Compromise (IoCs) vs Indicators of Attack (IoAs): Hash, IP & Behavioral Rules", "Intermediate")
        ]
    },
    {
        "name": "Centralized Logging, SIEM & Security Monitoring",
        "subtopics": [
            plan("centralized-security-logging-architecture-and-chain-of-custody", "Centralized Security Logging Architecture, WORM Storage & Integrity Sealing", "Intermediate"),
            plan("security-information-and-event-management-siem-architecture", "Security Information and Event Management (SIEM): Log Ingestion, Parsing & Indexing", "Intermediate"),
            plan("authoring-high-fidelity-siem-detection-rules-and-correlation-logic", "Authoring High-Fidelity Detection Rules, Thresholds & Multi-Stage Correlation Logic", "Advanced"),
            plan("user-and-entity-behavior-analytics-ueba-for-insider-threats", "User and Entity Behavior Analytics (UEBA): Baselines, Anomalies & Insider Risk", "Advanced"),
            plan("security-orchestration-automation-and-response-soar-playbooks", "SOAR Architecture: Authoring Automated Incident Enrichment & Response Playbooks", "Advanced"),
            plan("windows-security-event-log-auditing-best-practices", "Windows Security Auditing: Critical Event IDs (4624, 4625, 4688, 4720, 7045)", "Intermediate"),
            plan("linux-auditd-framework-and-syscall-auditing-architecture", "Linux Audit Daemon (auditd): System Call Monitoring & File Integrity Auditing", "Intermediate")
        ]
    },
    {
        "name": "Incident Response & Threat Containment",
        "subtopics": [
            plan("nist-sp-800-61-computer-security-incident-handling-guide", "NIST SP 800-61 Incident Handling Guide: The Four IR Lifecycle Phases", "Beginner"),
            plan("incident-response-phases-preparation-detection-containment-recovery", "Incident Response Playbook: Preparation, Triaging, Containment, Eradication & Recovery", "Intermediate"),
            plan("digital-forensics-and-evidence-preservation-chain-of-custody", "Digital Forensics & Evidence Preservation: Order of Volatility & Chain of Custody", "Intermediate"),
            plan("ransomware-incident-response-and-emergency-containment-playbook", "Emergency Ransomware Playbook: Network Isolation, Blast Radius & Recovery", "Intermediate"),
            plan("account-compromise-incident-response-and-token-revocation", "Account Compromise Triage: Session Revocation, Password Resets & MFA Re-enrollment", "Intermediate"),
            plan("authoring-post-incident-reports-and-lessons-learned-workshops", "Authoring Post-Incident Reports (PIR) & Conducting Blameless Post-Mortems", "Intermediate"),
            plan("incident-communication-escalation-and-regulatory-disclosure", "Security Incident Communications, Escalation Matrices & Regulatory Disclosure Rules", "Intermediate")
        ]
    },
    {
        "name": "Zero Trust Architecture & Enterprise Baselines",
        "subtopics": [
            plan("zero-trust-architecture-tenets-nist-sp-800-207-principles", "Zero Trust Architecture Core Tenets: NIST SP 800-207 Guiding Principles", "Beginner"),
            plan("zero-trust-continuous-verification-and-context-aware-access", "Continuous Authentication & Dynamic Risk-Based Access Evaluation", "Intermediate"),
            plan("zero-trust-network-access-ztna-vs-traditional-vpn", "Zero Trust Network Access (ZTNA) Architecture vs Legacy Perimeter VPNs", "Intermediate"),
            plan("secure-access-service-edge-sase-and-sse-architecture", "Secure Access Service Edge (SASE) & Security Service Edge (SSE) Explained", "Advanced"),
            plan("data-loss-prevention-dlp-endpoint-and-network-controls", "Data Loss Prevention (DLP): Content Inspection, Tagging & Exfiltration Blocking", "Intermediate"),
            plan("cryptography-fundamentals-symmetric-asymmetric-and-hashing", "Cryptography Fundamentals for Defenders: Symmetric, Asymmetric & Hashing Algorithms", "Beginner"),
            plan("public-key-infrastructure-pki-certificates-ca-and-crl", "Public Key Infrastructure (PKI): X.509 Certificates, CRL, OCSP & Trust Chains", "Intermediate")
        ]
    }
]

# -------------------------------------------------------------
# 6. CLOUD & AI (78 topics: 3 published + 75 planned)
# Canonical ID: "cloud", Display Name: "Cloud & AI"
# Cloud-primary; AI focused on ITOps/governance
# -------------------------------------------------------------
CLOUD_SECTIONS = [
    {
        "name": "Cloud Computing Architecture & Service Models",
        "subtopics": [
            pub("cloud-computing-fundamentals"),
            pub("iaas-vs-paas-vs-saas"),
            plan("cloud-shared-responsibility-model-across-tiers", "The Cloud Shared Responsibility Model: Provider vs Customer Responsibilities", "Beginner"),
            plan("cloud-deployment-models-public-private-hybrid-multi-cloud", "Cloud Deployment Models Compared: Public, Private, Hybrid, and Multi-Cloud", "Beginner"),
            plan("cloud-global-infrastructure-regions-availability-zones-edge", "Cloud Global Architecture: Regions, Availability Zones & Edge Point-of-Presence", "Beginner"),
            plan("cloud-high-availability-fault-tolerance-and-disaster-recovery", "Designing for High Availability: Active-Active vs Active-Passive Across AZs", "Intermediate"),
            plan("cloud-total-cost-of-ownership-tco-capex-vs-opex", "Cloud Financial Economics: Capital Expenditure (CapEx) vs Operational (OpEx)", "Beginner"),
            plan("cloud-migration-strategies-the-6-rs-framework", "Cloud Migration Strategies: Understanding the 6 R's Migration Framework", "Intermediate"),
            plan("serverless-computing-architecture-and-event-driven-design", "Serverless Computing Concepts: Function-as-a-Service (FaaS) & Event Triggers", "Intermediate")
        ]
    },
    {
        "name": "AWS Core Infrastructure & Foundational Services",
        "subtopics": [
            pub("aws-vs-azure-cloud-fundamentals"),
            plan("aws-global-infrastructure-regions-availability-zones-local-zones", "AWS Global Infrastructure: Regions, Availability Zones & Local Zones", "Beginner"),
            plan("aws-management-console-cli-and-sdk-architecture", "Interacting with AWS: Management Console, AWS CLI v2 & Boto3 SDKs", "Beginner"),
            plan("aws-ec2-instance-families-and-purchasing-models", "Amazon EC2 Architecture: Instance Types, Savings Plans & Spot Instances", "Intermediate"),
            plan("aws-vpc-architecture-subnets-route-tables-and-internet-gateways", "Amazon VPC Architecture: Public/Private Subnets, Route Tables & Internet Gateways", "Intermediate"),
            plan("aws-iam-identities-policies-roles-and-permission-boundaries", "AWS IAM Architecture: Users, Groups, Roles, Policies & Permission Boundaries", "Intermediate"),
            plan("aws-s3-bucket-architecture-storage-tiers-and-lifecycle-rules", "Amazon S3 Storage Architecture: Classes (Standard, Glacier) & Lifecycle Rules", "Beginner"),
            plan("aws-elastic-load-balancing-alb-nlb-and-auto-scaling-groups", "AWS Elastic Load Balancing (ALB vs NLB) & Auto Scaling Group Policies", "Intermediate"),
            plan("aws-rds-relational-database-service-multi-az-and-read-replicas", "Amazon RDS Architecture: Automated Backups, Multi-AZ & Read Replicas", "Intermediate")
        ]
    },
    {
        "name": "Microsoft Azure Core Infrastructure & Services",
        "subtopics": [
            plan("azure-global-infrastructure-geographies-regions-and-availability-zones", "Azure Global Infrastructure: Geographies, Paired Regions & Availability Zones", "Beginner"),
            plan("azure-resource-manager-arm-hierarchy-management-groups-to-resources", "Azure Resource Hierarchy: Management Groups, Subscriptions & Resource Groups", "Beginner"),
            plan("azure-virtual-machines-sizing-disks-and-availability-sets", "Azure Virtual Machines: Compute Sizing, Managed Disks & Availability Sets", "Intermediate"),
            plan("azure-virtual-networks-vnet-subnets-and-peering-architecture", "Azure VNet Architecture: Subnet Delegation, Peering & Service Endpoints", "Intermediate"),
            plan("microsoft-entra-id-vs-on-premises-active-directory-architecture", "Microsoft Entra ID (Azure AD) Architecture vs On-Premises Active Directory", "Intermediate"),
            plan("azure-blob-storage-tiers-redundancy-lrs-zrs-grs", "Azure Blob Storage: Hot, Cool, Archive Tiers & Redundancy (LRS, ZRS, GRS)", "Beginner"),
            plan("azure-virtual-network-gateway-and-site-to-site-vpn", "Azure Virtual Network Gateways: Site-to-Site VPN & ExpressRoute Connectivity", "Intermediate"),
            plan("azure-bastion-secure-rdp-and-ssh-without-public-ips", "Azure Bastion: Secure Browser-Based RDP/SSH Management Without Public IPs", "Intermediate")
        ]
    },
    {
        "name": "Cloud Identity & Access Management (IAM)",
        "subtopics": [
            plan("cloud-iam-policy-syntax-json-statements-and-least-privilege", "Authoring Cloud IAM Policies: JSON Statement Syntax & Principle of Least Privilege", "Intermediate"),
            plan("cloud-role-based-access-control-rbac-and-custom-roles", "Cloud Role-Based Access Control (RBAC): Built-In vs Custom Role Scoping", "Intermediate"),
            plan("cloud-cross-account-and-cross-subscription-role-delegation", "Cross-Account / Cross-Subscription IAM Delegation via AssumeRole Workflows", "Advanced"),
            plan("cloud-identity-federation-saml-oidc-and-enterprise-idps", "Enterprise Cloud Identity Federation: Integrating On-Premises IdPs with SAML/OIDC", "Advanced"),
            plan("cloud-managed-identities-and-service-principals", "Eliminating Static Credentials: AWS IAM Roles for EC2 & Azure Managed Identities", "Intermediate"),
            plan("cloud-privileged-identity-management-pim-and-just-in-time-access", "Privileged Identity Management (PIM): Approval Workflows & Just-In-Time Elevation", "Advanced"),
            plan("cloud-secrets-management-best-practices-and-key-vaulting", "Cloud Secrets Management: Automated Rotation with AWS Secrets Manager & Azure Key Vault", "Intermediate")
        ]
    },
    {
        "name": "Cloud Compute, Scaling & Container Infrastructure",
        "subtopics": [
            plan("cloud-virtual-machine-sizing-and-performance-optimization", "Virtual Machine Sizing: Balancing vCPU, Memory, IOPS & Network Bandwidth", "Intermediate"),
            plan("cloud-virtual-machine-storage-os-disks-data-disks-ephemeral", "Cloud VM Disk Architecture: Premium SSDs, Ultra Disks & Ephemeral Local Storage", "Intermediate"),
            plan("cloud-golden-images-and-custom-machine-image-pipelines", "Automated Golden Image Pipelines: AWS AMI Builder, Azure Image Gallery & Packer", "Intermediate"),
            plan("cloud-vm-auto-scaling-policies-metric-vs-schedule-triggers", "Cloud Auto Scaling Architecture: Dynamic Target Tracking vs Predictive Scaling", "Intermediate"),
            plan("cloud-container-services-overview-ecs-aci-and-managed-k8s", "Containerized Workloads in the Cloud: Docker, Amazon ECS, Azure ACI & Managed Kubernetes", "Intermediate"),
            plan("cloud-vm-snapshot-and-backup-automation-policies", "Automating VM Snapshots & Cloud Backup Policies with AWS Backup and Azure Backup", "Beginner"),
            plan("cloud-spot-instances-and-preemptible-vms-for-batch-workloads", "Cost Optimization with Spot Instances & Preemptible VMs: Handling Interruptions", "Intermediate")
        ]
    },
    {
        "name": "Cloud Networking, Hybrid Connectivity & Traffic Routing",
        "subtopics": [
            plan("cloud-routing-architecture-route-tables-and-user-defined-routes", "Cloud Routing Architecture: VPC Route Tables & Azure User-Defined Routes (UDR)", "Intermediate"),
            plan("cloud-security-groups-vs-network-access-control-lists", "Stateful Cloud Security Groups vs Stateless Network ACLs (NACLs)", "Intermediate"),
            plan("cloud-virtual-network-peering-intra-region-and-cross-region", "Virtual Network Peering: Inter-Region Transit, Routing & Transitive Peering Limits", "Intermediate"),
            plan("hybrid-cloud-dedicated-circuits-aws-direct-connect-and-azure-expressroute", "Dedicated Hybrid Cloud Links: AWS Direct Connect & Azure ExpressRoute Architecture", "Advanced"),
            plan("cloud-dns-architecture-amazon-route-53-and-azure-dns", "Enterprise Cloud DNS: Route 53 & Azure DNS (Private Hosted Zones & Split-Horizon)", "Intermediate"),
            plan("cloud-nat-gateways-and-outbound-internet-egress", "Cloud NAT Gateways: Architecting Secure Outbound Egress for Private Subnets", "Intermediate"),
            plan("cloud-content-delivery-networks-cloudfront-and-azure-cdn", "Content Delivery Networks (CDN): Edge Caching, TLS Termination & Origin Shielding", "Intermediate")
        ]
    },
    {
        "name": "Cloud Storage, Data Protection & Disaster Recovery",
        "subtopics": [
            plan("cloud-storage-types-object-vs-block-vs-managed-file-shares", "Cloud Storage Typologies Compared: Object (S3/Blob), Block (EBS/Disk) & File (EFS/Azure Files)", "Beginner"),
            plan("cloud-object-storage-versioning-immutability-and-retention-locks", "Object Storage Immutability: Versioning, S3 Object Lock & Azure Immutable Blob", "Intermediate"),
            plan("cloud-storage-encryption-sse-s3-customer-managed-keys-and-kms", "Cloud Data Encryption at Rest: Server-Side Encryption (SSE) & Customer-Managed KMS Keys", "Intermediate"),
            plan("cloud-cross-region-data-replication-for-business-continuity", "Cross-Region Object Replication (CRR) for High-Resilience Disaster Recovery", "Intermediate"),
            plan("cloud-disaster-recovery-architectures-pilot-light-to-multi-region", "Cloud DR Topologies: Backup/Restore, Pilot Light, Warm Standby & Multi-Region Active", "Advanced"),
            plan("cloud-data-ingestion-and-migration-appliances-snowball-data-box", "Large-Scale Data Migration: Offline Transfer Appliances (AWS Snowball, Azure Data Box)", "Intermediate"),
            plan("cloud-managed-file-services-amazon-fsx-and-azure-netapp-files", "Enterprise Managed File Systems: Amazon FSx for Windows & Azure NetApp Files", "Advanced")
        ]
    },
    {
        "name": "Cloud Monitoring, Telemetry & Infrastructure as Code (IaC)",
        "subtopics": [
            plan("aws-cloudwatch-metrics-logs-dashboards-and-composite-alarms", "AWS CloudWatch Architecture: Metric Filters, Log Groups & Composite Alarms", "Intermediate"),
            plan("azure-monitor-and-log-analytics-kql-query-fundamentals", "Azure Monitor Architecture: Metrics, Application Insights & KQL Querying", "Intermediate"),
            plan("cloud-audit-trail-governance-aws-cloudtrail-and-azure-activity-log", "Centralized Cloud Auditing: AWS CloudTrail Trails & Azure Activity Log Diagnostics", "Intermediate"),
            plan("infrastructure-as-code-iac-declarative-vs-imperative-principles", "Infrastructure as Code (IaC) Principles: Declarative vs Imperative Configuration", "Beginner"),
            plan("hashicorp-terraform-architecture-providers-state-and-hcl-syntax", "Terraform Architecture: Providers, State Management, Resource Blocks & HCL Syntax", "Intermediate"),
            plan("terraform-variables-outputs-and-modular-code-design", "Terraform Project Structure: Input Variables, Outputs & Reusable Child Modules", "Intermediate"),
            plan("azure-bicep-and-arm-templates-declarative-azure-iac", "Azure Bicep vs ARM Templates: Modular Declarative Deployment for Azure", "Intermediate"),
            plan("aws-cloudformation-templates-and-stack-lifecycle-management", "AWS CloudFormation: YAML Templates, Drift Detection & Stack Lifecycle Management", "Intermediate")
        ]
    },
    {
        "name": "Cloud Security, Governance, Compliance & FinOps",
        "subtopics": [
            plan("cloud-security-posture-management-cspm-and-misconfigurations", "Cloud Security Posture Management (CSPM): Continuous Baseline Auditing", "Intermediate"),
            plan("cloud-compliance-frameworks-and-cis-cloud-foundations-benchmarks", "Implementing CIS Cloud Foundations Benchmarks & Regulatory Compliance in the Cloud", "Intermediate"),
            plan("finops-fundamentals-cloud-financial-management-and-cost-allocation", "FinOps Fundamentals: Cloud Financial Governance, Chargeback & Showback Models", "Beginner"),
            plan("cloud-cost-allocation-resource-tagging-strategies-and-cost-centers", "Enterprise Resource Tagging Taxonomy & Cost Allocation Reporting", "Beginner"),
            plan("cloud-cost-optimization-reserved-instances-savings-plans-rightsizing", "Cloud Cost Optimization: Reserved Instances, Savings Plans & Workload Rightsizing", "Intermediate"),
            plan("microsoft-365-tenant-administration-fundamentals-for-sysadmins", "Microsoft 365 Tenant Administration: Licensing, Admin Roles & Exchange Online Basics", "Intermediate"),
            plan("microsoft-365-security-and-compliance-center-administration", "Microsoft Defender for Office 365, Purview Compliance & Safe Links/Attachments", "Intermediate")
        ]
    },
    {
        "name": "Enterprise AI for IT Operations (AIOps) & AI Governance",
        "subtopics": [
            plan("aiops-architecture-applying-machine-learning-to-it-operations", "AIOps Architecture: Machine Learning for Event Correlation & Root Cause Analysis", "Intermediate"),
            plan("ai-powered-anomaly-detection-in-metrics-and-log-streams", "Real-Time Anomaly Detection in System Metrics & Telemetry Log Streams Using AI", "Intermediate"),
            plan("ai-assisted-it-incident-triage-and-automated-remediation", "AI-Assisted Incident Triage, Ticket Classification & Automated Remediation", "Intermediate"),
            plan("natural-language-system-administration-and-cli-copilots", "Natural Language Querying & AI Copilots in Systems Administration", "Beginner"),
            plan("responsible-enterprise-ai-security-privacy-and-intellectual-property", "Responsible Enterprise AI: Data Privacy, Model Confidentiality & Intellectual Property", "Beginner"),
            plan("data-governance-and-sanitization-for-enterprise-ai-workloads", "Data Governance for Enterprise AI: RAG Pipeline Data Hygiene & Redaction", "Intermediate"),
            plan("security-risks-of-generative-ai-prompt-injection-and-data-poisoning", "Defending Enterprise AI: Mitigating Prompt Injection, Jailbreaks & Data Poisoning", "Intermediate"),
            plan("infrastructure-readiness-and-compute-requirements-for-enterprise-ai", "Infrastructure Architecture for AI: GPU Virtualization, Compute Clusters & Storage Throughput", "Advanced")
        ]
    }
]

ALL_CORE_CATEGORIES = [
    {
        "id": "networking",
        "name": "Networking",
        "type": "core",
        "description": "IP addressing, DNS, DHCP, VLAN, Wi-Fi, VPN, routing, switching, and network troubleshooting.",
        "keywords": "network, ip, subnet, router, switch, wifi, cisco, vlan, vpn, dns, dhcp",
        "icon": "./assets/icons/networking.png",
        "url": "networking.html",
        "accent": "networking",
        "sections": NETWORKING_SECTIONS
    },
    {
        "id": "windows",
        "name": "Windows",
        "type": "core",
        "description": "Practical guides and tutorials for Windows administration, PowerShell scripting, CMD, Active Directory, and system troubleshooting.",
        "keywords": "windows, powershell, cmd, active directory, registry, gpo, bitlocker, sysadmin",
        "icon": "./assets/icons/windows.png",
        "url": "windows.html",
        "accent": "windows",
        "sections": WINDOWS_SECTIONS
    },
    {
        "id": "linux",
        "name": "Linux",
        "type": "core",
        "description": "Hands-on Linux tutorials covering bash scripting, server administration, permissions, systemd, networking, and security.",
        "keywords": "linux, bash, terminal, ubuntu, rhel, permissions, systemd, ssh, cron",
        "icon": "./assets/icons/linux.png",
        "url": "linux.html",
        "accent": "linux",
        "sections": LINUX_SECTIONS
    },
    {
        "id": "servers",
        "name": "Servers",
        "type": "core",
        "description": "Server administration, Active Directory, DNS/DHCP, virtualization, storage, and enterprise infrastructure.",
        "keywords": "server, windows server, linux server, active directory, virtualization, vmware, raid, backup",
        "icon": "./assets/icons/servers.png",
        "url": "servers.html",
        "accent": "servers",
        "sections": SERVERS_SECTIONS
    },
    {
        "id": "cybersecurity",
        "name": "Cybersecurity",
        "type": "core",
        "description": "Enterprise defensive security, identity and access management, MFA, endpoint hardening, network defense, and incident response.",
        "keywords": "cybersecurity, security, mfa, authentication, firewall, edr, incident response, zero trust",
        "icon": "./assets/icons/cybersecurity.png",
        "url": "cybersecurity.html",
        "accent": "cybersecurity",
        "sections": CYBERSECURITY_SECTIONS
    },
    {
        "id": "cloud",
        "name": "Cloud & AI",
        "type": "core",
        "description": "AWS, Azure, cloud infrastructure, virtualization, IaC, cost optimization, and responsible AI for IT operations.",
        "keywords": "cloud, aws, azure, iaas, paas, saas, terraform, ai, devops, virtualization",
        "icon": "./assets/icons/cloud-ai.png",
        "url": "cloud.html",
        "accent": "cloud",
        "sections": CLOUD_SECTIONS
    }
]

# Specialized categories (preserve existing metadata)
SPECIALIZED_CATEGORIES = [
    {
        "id": "it-support",
        "name": "IT Support",
        "type": "more",
        "description": "Help desk workflows, ticketing systems, user onboarding, remote support, and day-to-day desktop administration.",
        "keywords": "it support, help desk, ticketing, troubleshooting, desktop support",
        "icon": "./assets/icons/it-support.png",
        "url": "#",
        "accent": "it-support",
        "sections": []
    },
    {
        "id": "hardware",
        "name": "Hardware",
        "type": "more",
        "description": "PC components, diagnostics, BIOS/UEFI, peripheral interfaces, RAM, storage, and thermal troubleshooting.",
        "keywords": "hardware, pc, cpu, ram, ssd, motherboard, bios, uefi",
        "icon": "./assets/icons/hardware.png",
        "url": "#",
        "accent": "hardware",
        "sections": []
    },
    {
        "id": "virtualization",
        "name": "Virtualization",
        "type": "more",
        "description": "Hypervisors, VM configuration, clustering, resource allocation, and virtual networking.",
        "keywords": "virtualization, vmware, hyper-v, proxmox, kvm, virtual machine",
        "icon": "./assets/icons/virtualization.png",
        "url": "#",
        "accent": "virtualization",
        "sections": []
    },
    {
        "id": "monitoring",
        "name": "Monitoring",
        "type": "more",
        "description": "System monitoring tools, alerting thresholds, SNMP, log aggregation, and uptime metrics.",
        "keywords": "monitoring, zabbix, prometheus, grafana, snmp, uptime, alerts",
        "icon": "./assets/icons/monitoring.png",
        "url": "#",
        "accent": "monitoring",
        "sections": []
    },
    {
        "id": "backup-recovery",
        "name": "Backup & Recovery",
        "type": "more",
        "description": "Backup strategies, 3-2-1 rule, disaster recovery planning, shadow copies, and image-based backups.",
        "keywords": "backup, recovery, disaster recovery, veeam, rto, rpo, snapshots",
        "icon": "./assets/icons/backup-recovery.png",
        "url": "#",
        "accent": "backup-recovery",
        "sections": []
    },
    {
        "id": "storage",
        "name": "Storage",
        "type": "more",
        "description": "RAID levels, NAS, SAN, iSCSI, storage spaces, NTFS, ReFS, and filesystem management.",
        "keywords": "storage, raid, nas, san, iscsi, ntfs, zfs, disks",
        "icon": "./assets/icons/storage.png",
        "url": "#",
        "accent": "storage",
        "sections": []
    },
    {
        "id": "it-tools",
        "name": "IT Tools",
        "type": "more",
        "description": "Essential Sysinternals utilities, network scanners, diagnostics, and administrator toolkits.",
        "keywords": "it tools, sysinternals, wireshark, nmap, puty, winscp, utilities",
        "icon": "./assets/icons/it-tools.png",
        "url": "#",
        "accent": "it-tools",
        "sections": []
    },
    {
        "id": "command-line",
        "name": "Command Line",
        "type": "more",
        "description": "CMD, PowerShell, and Bash syntax guides, practical one-liners, and scripting workflows.",
        "keywords": "cli, cmd, powershell, bash, command line, terminal, scripts",
        "icon": "./assets/icons/command-line.png",
        "url": "#",
        "accent": "command-line",
        "sections": []
    },
    {
        "id": "troubleshooting",
        "name": "Troubleshooting",
        "type": "more",
        "description": "Methodologies, root cause analysis, error code lookup, and practical problem-solving flowcharts.",
        "keywords": "troubleshooting, methodology, root cause, error codes, diagnostics",
        "icon": "./assets/icons/troubleshooting.png",
        "url": "#",
        "accent": "troubleshooting",
        "sections": []
    },
    {
        "id": "interview-questions",
        "name": "Interview Questions",
        "type": "more",
        "description": "Technical interview preparation for IT Support, Sysadmin, and Network Engineering roles.",
        "keywords": "interview, questions, sysadmin, help desk, networking, preparation",
        "icon": "./assets/icons/interview-questions.png",
        "url": "#",
        "accent": "interview-questions",
        "sections": []
    }
]

def audit_curriculum():
    print("=" * 70)
    print("AUDITING MASTER CURRICULUM ARCHITECTURE (PRE-WRITE)")
    print("=" * 70)

    # 1. Global ID Uniqueness & Name Uniqueness inside categories
    all_subtopic_ids = []
    category_names_map = {}
    published_mapped_ids = set()
    errors = []
    warnings = []

    cat_counts = {}
    progression = {}

    for cat in ALL_CORE_CATEGORIES:
        cid = cat["id"]
        cname = cat["name"]
        sections = cat["sections"]
        cat_subs = []
        names_in_cat = set()
        progression[cid] = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}

        if len(sections) < 8 or len(sections) > 12:
            warnings.append(f"Category '{cid}' has {len(sections)} sections (recommended: 8-10)")

        for s_idx, sec in enumerate(sections):
            sec_name = sec["name"]
            sec_subs = sec["subtopics"]
            if len(sec_subs) < 5:
                warnings.append(f"Section '{sec_name}' in '{cid}' has only {len(sec_subs)} subtopics")

            for sub in sec_subs:
                sid = sub["id"]
                sname = sub["name"]
                slevel = sub["level"]
                sstatus = sub["status"]

                progression[cid][slevel] += 1
                all_subtopic_ids.append(sid)
                cat_subs.append(sub)

                # Name uniqueness in category
                norm_name = sname.lower().strip()
                if norm_name in names_in_cat:
                    errors.append(f"Duplicate topic name in category '{cid}': '{sname}'")
                names_in_cat.add(norm_name)

                # Published vs Planned integrity
                if sstatus == "published":
                    if "url" not in sub or not sub["url"]:
                        errors.append(f"Published item '{sid}' missing required 'url'")
                    else:
                        published_mapped_ids.add(sid)
                        # Verify file exists
                        target_file = REPO_ROOT / sub["url"]
                        if not target_file.exists():
                            errors.append(f"Published item '{sid}' target HTML file not found: {sub['url']}")
                elif sstatus == "planned":
                    if "url" in sub:
                        errors.append(f"Planned item '{sid}' should NOT have a 'url' property!")

        cat_counts[cid] = {
            "name": cname,
            "sections": len(sections),
            "total_topics": len(cat_subs),
            "published": sum(1 for s in cat_subs if s["status"] == "published"),
            "planned": sum(1 for s in cat_subs if s["status"] == "planned")
        }

    # 2. Check Global ID Uniqueness
    id_counts = Counter(all_subtopic_ids)
    for sid, count in id_counts.items():
        if count > 1:
            errors.append(f"GLOBAL DUPLICATE ID: '{sid}' appears {count} times across curriculum!")

    # 3. Verify Exact 1-to-1 Published Mapping with tutorials.json
    all_tut_ids = set(PUB_BY_ID.keys())
    unmapped_tuts = all_tut_ids - published_mapped_ids
    if unmapped_tuts:
        errors.append(f"Unmapped published tutorials ({len(unmapped_tuts)}): {unmapped_tuts}")

    extra_mapped = published_mapped_ids - all_tut_ids
    if extra_mapped:
        errors.append(f"Phantom published curriculum entries ({len(extra_mapped)}): {extra_mapped}")

    # Check that category, level, and url in published curriculum agree with tutorials.json
    for cat in ALL_CORE_CATEGORIES:
        cid = cat["id"]
        for sec in cat["sections"]:
            for sub in sec["subtopics"]:
                if sub["status"] == "published":
                    t = PUB_BY_ID[sub["id"]]
                    # check url
                    if sub["url"] != t["url"].replace("./", ""):
                        errors.append(f"Published url mismatch for '{sub['id']}': '{sub['url']}' vs '{t['url']}'")
                    # check level
                    if sub["level"] != t["level"]:
                        errors.append(f"Published level mismatch for '{sub['id']}': '{sub['level']}' vs '{t['level']}'")

    print("\n--- CATEGORY BREAKDOWN ---")
    total_curriculum = 0
    total_pub = 0
    total_plan = 0
    for cid, stats in cat_counts.items():
        print(f"{stats['name']:15} | {stats['sections']:2} sections | {stats['total_topics']:2} topics | {stats['published']:2} published | {stats['planned']:2} planned")
        total_curriculum += stats["total_topics"]
        total_pub += stats["published"]
        total_plan += stats["planned"]
        # Check target: >= 70
        if stats["total_topics"] < 70:
            errors.append(f"Category '{cid}' has {stats['total_topics']} topics (< 70 required!)")

    print("-" * 70)
    print(f"TOTALS          | {sum(s['sections'] for s in cat_counts.values()):2} sections | {total_curriculum:2} topics | {total_pub:2} published | {total_plan:2} planned")

    print("\n--- PROGRESSION AUDIT ---")
    for cid, p in progression.items():
        tot = sum(p.values())
        b_pct = (p['Beginner'] / tot) * 100
        i_pct = (p['Intermediate'] / tot) * 100
        a_pct = (p['Advanced'] / tot) * 100
        print(f"{cat_counts[cid]['name']:15} | Beg: {p['Beginner']:2} ({b_pct:4.1f}%) | Int: {p['Intermediate']:2} ({i_pct:4.1f}%) | Adv: {p['Advanced']:2} ({a_pct:4.1f}%)")

    print("\n--- AUDIT RESULTS ---")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN] {w}")

    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  [FAIL] {e}")
        return False

    print("ALL INTEGRITY CHECKS PASSED: Curriculum is clean, unique, and strictly mapped!")
    return True

def save_topics_json():
    final_data = {
        "categories": ALL_CORE_CATEGORIES + SPECIALIZED_CATEGORIES
    }
    with open(TOPICS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)
    print(f"\nSuccessfully wrote updated curriculum to {TOPICS_JSON_PATH}")

if __name__ == "__main__":
    success = audit_curriculum()
    if success:
        save_topics_json()
    else:
        print("Aborting save due to audit errors.")
        exit(1)
