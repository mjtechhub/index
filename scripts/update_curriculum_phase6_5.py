#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6.5 Curriculum Architecture Update (scripts/update_curriculum_phase6_5.py)
Populates comprehensive enterprise curriculum sections in data/topics.json for:
- Windows (5 sections, 15 subtopics)
- Linux (5 sections, 15 subtopics)
- Servers (5 sections, 14 subtopics)
- Cybersecurity (5 sections, 16 subtopics)
- Cloud & AI (5 sections, 15 subtopics)
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_PATH = ROOT_DIR / "data" / "topics.json"

CURRICULUM_DATA = {
    "windows": [
        {
            "name": "Windows Operating System Fundamentals",
            "title": "Windows Operating System Fundamentals",
            "subtopics": [
                {
                    "id": "windows-operating-system-fundamentals",
                    "name": "Windows Operating System Fundamentals",
                    "level": "Beginner",
                    "url": "tutorials/windows/windows-operating-system-fundamentals.html"
                },
                {
                    "id": "windows-file-systems-ntfs-vs-refs",
                    "name": "Windows File Systems: NTFS vs ReFS",
                    "level": "Beginner",
                    "url": "windows.html"
                },
                {
                    "id": "windows-services-architecture",
                    "name": "Windows Services & Background Architecture",
                    "level": "Intermediate",
                    "url": "windows.html"
                }
            ]
        },
        {
            "name": "Command Line & Automation",
            "title": "Command Line & Automation",
            "subtopics": [
                {
                    "id": "windows-command-prompt-basics",
                    "name": "Windows Command Prompt Basics",
                    "level": "Beginner",
                    "url": "tutorials/windows/windows-command-prompt-basics.html"
                },
                {
                    "id": "powershell-fundamentals-for-administrators",
                    "name": "PowerShell Fundamentals for Administrators",
                    "level": "Intermediate",
                    "url": "tutorials/windows/powershell-fundamentals-for-administrators.html"
                },
                {
                    "id": "powershell-scripting-and-automation",
                    "name": "PowerShell Scripting & Pipeline Automation",
                    "level": "Advanced",
                    "url": "windows.html"
                }
            ]
        },
        {
            "name": "Access Control & Security",
            "title": "Access Control & Security",
            "subtopics": [
                {
                    "id": "ntfs-permissions-and-share-security",
                    "name": "NTFS Permissions & Share Security",
                    "level": "Intermediate",
                    "url": "windows.html"
                },
                {
                    "id": "local-users-and-groups-management",
                    "name": "Local Users & Groups Management",
                    "level": "Beginner",
                    "url": "windows.html"
                },
                {
                    "id": "windows-defender-firewall-configuration",
                    "name": "Windows Defender Firewall Configuration",
                    "level": "Intermediate",
                    "url": "windows.html"
                },
                {
                    "id": "bitlocker-drive-encryption-administration",
                    "name": "BitLocker Drive Encryption Administration",
                    "level": "Intermediate",
                    "url": "windows.html"
                }
            ]
        },
        {
            "name": "Enterprise Administration & Directory Services",
            "title": "Enterprise Administration & Directory Services",
            "subtopics": [
                {
                    "id": "group-policy-fundamentals-and-gpos",
                    "name": "Group Policy Fundamentals & GPOs",
                    "level": "Intermediate",
                    "url": "windows.html"
                },
                {
                    "id": "active-directory-domain-services-basics",
                    "name": "Active Directory Domain Services Basics",
                    "level": "Intermediate",
                    "url": "windows.html"
                },
                {
                    "id": "windows-update-for-business-and-wsus",
                    "name": "Windows Update for Business & WSUS",
                    "level": "Intermediate",
                    "url": "windows.html"
                }
            ]
        },
        {
            "name": "Troubleshooting & Diagnostics",
            "title": "Troubleshooting & Diagnostics",
            "subtopics": [
                {
                    "id": "windows-event-viewer-diagnostics",
                    "name": "Windows Event Viewer & Log Diagnostics",
                    "level": "Intermediate",
                    "url": "windows.html"
                },
                {
                    "id": "task-manager-and-resource-monitor",
                    "name": "Task Manager & Resource Monitor Analysis",
                    "level": "Beginner",
                    "url": "windows.html"
                },
                {
                    "id": "sysinternals-suite-for-administrators",
                    "name": "Sysinternals Suite for Administrators",
                    "level": "Advanced",
                    "url": "windows.html"
                }
            ]
        }
    ],
    "linux": [
        {
            "name": "Linux Fundamentals",
            "title": "Linux Fundamentals",
            "subtopics": [
                {
                    "id": "linux-operating-system-fundamentals",
                    "name": "Linux Operating System Fundamentals",
                    "level": "Beginner",
                    "url": "tutorials/linux/linux-operating-system-fundamentals.html"
                },
                {
                    "id": "linux-filesystem-hierarchy-explained",
                    "name": "Linux Filesystem Hierarchy Explained",
                    "level": "Beginner",
                    "url": "tutorials/linux/linux-filesystem-hierarchy-explained.html"
                },
                {
                    "id": "understanding-the-linux-kernel-and-shells",
                    "name": "Understanding the Linux Kernel & Shells",
                    "level": "Intermediate",
                    "url": "linux.html"
                }
            ]
        },
        {
            "name": "Terminal & Administration",
            "title": "Terminal & Administration",
            "subtopics": [
                {
                    "id": "essential-linux-terminal-commands",
                    "name": "Essential Linux Terminal Commands",
                    "level": "Intermediate",
                    "url": "tutorials/linux/essential-linux-terminal-commands.html"
                },
                {
                    "id": "linux-file-permissions-and-ownership",
                    "name": "Linux File Permissions & Ownership (chmod/chown)",
                    "level": "Beginner",
                    "url": "linux.html"
                },
                {
                    "id": "user-and-group-management-in-linux",
                    "name": "User & Group Management in Linux",
                    "level": "Beginner",
                    "url": "linux.html"
                },
                {
                    "id": "package-management-apt-dnf-and-yum",
                    "name": "Package Management: APT, DNF & YUM",
                    "level": "Intermediate",
                    "url": "linux.html"
                }
            ]
        },
        {
            "name": "Service & Process Management",
            "title": "Service & Process Management",
            "subtopics": [
                {
                    "id": "systemd-service-and-unit-management",
                    "name": "systemd Service & Unit Management",
                    "level": "Intermediate",
                    "url": "linux.html"
                },
                {
                    "id": "linux-process-monitoring-and-signals",
                    "name": "Linux Process Monitoring & Signals (ps, top, kill)",
                    "level": "Intermediate",
                    "url": "linux.html"
                },
                {
                    "id": "cron-jobs-and-scheduled-tasks",
                    "name": "Cron Jobs & Scheduled Automation",
                    "level": "Beginner",
                    "url": "linux.html"
                }
            ]
        },
        {
            "name": "Storage & System Logging",
            "title": "Storage & System Logging",
            "subtopics": [
                {
                    "id": "linux-disk-management-lvm-and-mounts",
                    "name": "Linux Disk Management, LVM & Mounts",
                    "level": "Intermediate",
                    "url": "linux.html"
                },
                {
                    "id": "journalctl-and-system-logging-in-linux",
                    "name": "journalctl & System Logging in Linux",
                    "level": "Intermediate",
                    "url": "linux.html"
                }
            ]
        },
        {
            "name": "Linux Networking & Security",
            "title": "Linux Networking & Security",
            "subtopics": [
                {
                    "id": "linux-network-configuration-with-ip-and-ss",
                    "name": "Linux Network Configuration with ip & ss",
                    "level": "Intermediate",
                    "url": "linux.html"
                },
                {
                    "id": "ssh-server-hardening-and-key-authentication",
                    "name": "SSH Server Hardening & Key Authentication",
                    "level": "Intermediate",
                    "url": "linux.html"
                },
                {
                    "id": "linux-firewalls-ufw-and-firewalld",
                    "name": "Linux Firewalls: UFW & Firewalld",
                    "level": "Intermediate",
                    "url": "linux.html"
                }
            ]
        }
    ],
    "servers": [
        {
            "name": "Server Architecture Fundamentals",
            "title": "Server Architecture Fundamentals",
            "subtopics": [
                {
                    "id": "what-is-a-server",
                    "name": "What Is a Server?",
                    "level": "Beginner",
                    "url": "tutorials/servers/what-is-a-server.html"
                },
                {
                    "id": "server-hardware-chassis-and-redundancy",
                    "name": "Server Hardware Architecture: Rack, Tower & Blade",
                    "level": "Beginner",
                    "url": "servers.html"
                },
                {
                    "id": "raid-levels-and-storage-redundancy",
                    "name": "RAID Levels & Storage Redundancy Explained",
                    "level": "Intermediate",
                    "url": "servers.html"
                }
            ]
        },
        {
            "name": "Operating System Platforms",
            "title": "Operating System Platforms",
            "subtopics": [
                {
                    "id": "windows-server-fundamentals",
                    "name": "Windows Server Fundamentals",
                    "level": "Intermediate",
                    "url": "tutorials/servers/windows-server-fundamentals.html"
                },
                {
                    "id": "linux-server-fundamentals",
                    "name": "Linux Server Fundamentals",
                    "level": "Intermediate",
                    "url": "tutorials/servers/linux-server-fundamentals.html"
                },
                {
                    "id": "headless-server-management-and-remote-consoles",
                    "name": "Headless Server Management & Out-of-Band IPMI/iDRAC",
                    "level": "Intermediate",
                    "url": "servers.html"
                }
            ]
        },
        {
            "name": "Core Infrastructure Services",
            "title": "Core Infrastructure Services",
            "subtopics": [
                {
                    "id": "enterprise-dns-server-administration",
                    "name": "Enterprise DNS Server Administration",
                    "level": "Intermediate",
                    "url": "servers.html"
                },
                {
                    "id": "enterprise-dhcp-server-and-relay-agents",
                    "name": "Enterprise DHCP Server & Relay Agents",
                    "level": "Intermediate",
                    "url": "servers.html"
                },
                {
                    "id": "file-server-architecture-smb-nfs-and-dfs",
                    "name": "File Server Architecture: SMB, NFS & DFS",
                    "level": "Intermediate",
                    "url": "servers.html"
                }
            ]
        },
        {
            "name": "Virtualization & Hypervisors",
            "title": "Virtualization & Hypervisors",
            "subtopics": [
                {
                    "id": "hypervisor-fundamentals-type-1-vs-type-2",
                    "name": "Hypervisor Fundamentals: Type 1 vs Type 2",
                    "level": "Beginner",
                    "url": "servers.html"
                },
                {
                    "id": "vmware-esxi-and-vsphere-basics",
                    "name": "VMware ESXi & vSphere Architecture",
                    "level": "Intermediate",
                    "url": "servers.html"
                },
                {
                    "id": "proxmox-ve-cluster-administration",
                    "name": "Proxmox VE Cluster Administration",
                    "level": "Intermediate",
                    "url": "servers.html"
                }
            ]
        },
        {
            "name": "Resilience, Backup & Monitoring",
            "title": "Resilience, Backup & Monitoring",
            "subtopics": [
                {
                    "id": "server-backup-strategies-and-disaster-recovery",
                    "name": "Server Backup Strategies (3-2-1) & Disaster Recovery",
                    "level": "Intermediate",
                    "url": "servers.html"
                },
                {
                    "id": "server-health-monitoring-snmp-and-metrics",
                    "name": "Server Health Monitoring & Proactive Alerting",
                    "level": "Intermediate",
                    "url": "servers.html"
                }
            ]
        }
    ],
    "cybersecurity": [
        {
            "name": "Security Principles & Governance",
            "title": "Security Principles & Governance",
            "subtopics": [
                {
                    "id": "cybersecurity-fundamentals",
                    "name": "Cybersecurity Fundamentals",
                    "level": "Beginner",
                    "url": "tutorials/cybersecurity/cybersecurity-fundamentals.html"
                },
                {
                    "id": "the-cia-triad-in-enterprise-it",
                    "name": "The CIA Triad in Enterprise IT",
                    "level": "Beginner",
                    "url": "cybersecurity.html"
                },
                {
                    "id": "defense-in-depth-architecture",
                    "name": "Defense-in-Depth Architecture",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                }
            ]
        },
        {
            "name": "Identity & Access Control",
            "title": "Identity & Access Control",
            "subtopics": [
                {
                    "id": "authentication-vs-authorization",
                    "name": "Authentication vs Authorization",
                    "level": "Beginner",
                    "url": "tutorials/cybersecurity/authentication-vs-authorization.html"
                },
                {
                    "id": "multi-factor-authentication-explained",
                    "name": "Multi-Factor Authentication (MFA) Explained",
                    "level": "Intermediate",
                    "url": "tutorials/cybersecurity/multi-factor-authentication-explained.html"
                },
                {
                    "id": "role-based-access-control-and-least-privilege",
                    "name": "Role-Based Access Control (RBAC) & Least Privilege",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                },
                {
                    "id": "privileged-access-management-pam-basics",
                    "name": "Privileged Access Management (PAM) Basics",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                }
            ]
        },
        {
            "name": "Threat Defense & Endpoint Hardening",
            "title": "Threat Defense & Endpoint Hardening",
            "subtopics": [
                {
                    "id": "malware-types-and-enterprise-prevention",
                    "name": "Malware Types & Enterprise Prevention",
                    "level": "Beginner",
                    "url": "cybersecurity.html"
                },
                {
                    "id": "phishing-attack-vectors-and-email-security",
                    "name": "Phishing Attack Vectors & Email Security (SPF, DKIM, DMARC)",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                },
                {
                    "id": "endpoint-detection-and-response-edr-fundamentals",
                    "name": "Endpoint Detection & Response (EDR) Fundamentals",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                },
                {
                    "id": "operating-system-hardening-checklists",
                    "name": "Operating System Hardening Checklists",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                }
            ]
        },
        {
            "name": "Network Defense & Architecture",
            "title": "Network Defense & Architecture",
            "subtopics": [
                {
                    "id": "network-segmentation-and-dmz-architecture",
                    "name": "Network Segmentation & DMZ Architecture",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                },
                {
                    "id": "next-generation-firewalls-ngfw-explained",
                    "name": "Next-Generation Firewalls (NGFW) Explained",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                },
                {
                    "id": "zero-trust-security-model-fundamentals",
                    "name": "Zero Trust Architecture Fundamentals",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                }
            ]
        },
        {
            "name": "Security Operations & Incident Response",
            "title": "Security Operations & Incident Response",
            "subtopics": [
                {
                    "id": "vulnerability-management-lifecycle",
                    "name": "Vulnerability Management Lifecycle (CVE/CVSS)",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                },
                {
                    "id": "security-information-and-event-management-siem",
                    "name": "SIEM Fundamentals & Centralized Audit Logging",
                    "level": "Intermediate",
                    "url": "cybersecurity.html"
                },
                {
                    "id": "incident-response-frameworks-for-sysadmins",
                    "name": "Incident Response Frameworks for Sysadmins",
                    "level": "Advanced",
                    "url": "cybersecurity.html"
                }
            ]
        }
    ],
    "cloud": [
        {
            "name": "Cloud Computing Foundations",
            "title": "Cloud Computing Foundations",
            "subtopics": [
                {
                    "id": "cloud-computing-fundamentals",
                    "name": "Cloud Computing Fundamentals",
                    "level": "Beginner",
                    "url": "tutorials/cloud/cloud-computing-fundamentals.html"
                },
                {
                    "id": "iaas-vs-paas-vs-saas",
                    "name": "IaaS vs PaaS vs SaaS Explained",
                    "level": "Beginner",
                    "url": "tutorials/cloud/iaas-vs-paas-vs-saas.html"
                },
                {
                    "id": "public-private-and-hybrid-cloud-models",
                    "name": "Public, Private & Hybrid Cloud Models",
                    "level": "Beginner",
                    "url": "cloud.html"
                }
            ]
        },
        {
            "name": "Major Cloud Platforms & Architecture",
            "title": "Major Cloud Platforms & Architecture",
            "subtopics": [
                {
                    "id": "aws-vs-azure-cloud-fundamentals",
                    "name": "AWS vs Azure Cloud Fundamentals",
                    "level": "Intermediate",
                    "url": "tutorials/cloud/aws-vs-azure-cloud-fundamentals.html"
                },
                {
                    "id": "cloud-regions-availability-zones-and-resilience",
                    "name": "Cloud Regions, Availability Zones & High Availability",
                    "level": "Intermediate",
                    "url": "cloud.html"
                },
                {
                    "id": "cloud-virtual-machines-ec2-and-azure-vms",
                    "name": "Cloud Compute: AWS EC2 & Azure Virtual Machines",
                    "level": "Intermediate",
                    "url": "cloud.html"
                }
            ]
        },
        {
            "name": "Cloud Networking & Security Controls",
            "title": "Cloud Networking & Security Controls",
            "subtopics": [
                {
                    "id": "virtual-private-clouds-vpc-and-vnets-explained",
                    "name": "Cloud Virtual Networks: AWS VPC & Azure VNet",
                    "level": "Intermediate",
                    "url": "cloud.html"
                },
                {
                    "id": "cloud-security-groups-and-network-acls",
                    "name": "Cloud Security Groups & Network Security Groups (NSGs)",
                    "level": "Intermediate",
                    "url": "cloud.html"
                },
                {
                    "id": "cloud-iam-identities-policies-and-roles",
                    "name": "Cloud Identity & Access Management (IAM): Roles & Policies",
                    "level": "Intermediate",
                    "url": "cloud.html"
                }
            ]
        },
        {
            "name": "Cloud Storage, Backup & Modern Workplace",
            "title": "Cloud Storage, Backup & Modern Workplace",
            "subtopics": [
                {
                    "id": "cloud-object-storage-aws-s3-and-azure-blob",
                    "name": "Cloud Object Storage: AWS S3 & Azure Blob Storage",
                    "level": "Beginner",
                    "url": "cloud.html"
                },
                {
                    "id": "cloud-backup-and-disaster-recovery-patterns",
                    "name": "Cloud Backup & Snapshot Strategies",
                    "level": "Intermediate",
                    "url": "cloud.html"
                },
                {
                    "id": "microsoft-365-tenant-administration-fundamentals",
                    "name": "Microsoft 365 Tenant Administration Fundamentals",
                    "level": "Intermediate",
                    "url": "cloud.html"
                }
            ]
        },
        {
            "name": "Automation & Enterprise AI",
            "title": "Automation & Enterprise AI",
            "subtopics": [
                {
                    "id": "infrastructure-as-code-iac-basics-terraform",
                    "name": "Infrastructure as Code (IaC) Basics with Terraform",
                    "level": "Intermediate",
                    "url": "cloud.html"
                },
                {
                    "id": "ai-for-it-operations-aiops-and-automated-alerting",
                    "name": "AIOps: Machine Learning in System Observability",
                    "level": "Intermediate",
                    "url": "cloud.html"
                },
                {
                    "id": "responsible-enterprise-ai-security-and-data-privacy",
                    "name": "Responsible Enterprise AI: Security & Data Privacy",
                    "level": "Intermediate",
                    "url": "cloud.html"
                }
            ]
        }
    ]
}

def update_topics_curriculum():
    with open(TOPICS_PATH, "r", encoding="utf-8") as f:
        topics_data = json.load(f)

    categories = topics_data.get("categories", [])
    updated_counts = {}

    for cat in categories:
        cid = cat.get("id")
        if cid in CURRICULUM_DATA:
            cat["sections"] = CURRICULUM_DATA[cid]
            updated_counts[cid] = len(cat["sections"])
            print(f"[SUCCESS] Updated '{cid}' ({cat['name']}) with {len(cat['sections'])} structured curriculum sections.")

    with open(TOPICS_PATH, "w", encoding="utf-8") as f:
        json.dump(topics_data, f, indent=4)

    print(f"\nSuccessfully wrote updated curriculum to {TOPICS_PATH}")
    return True

if __name__ == "__main__":
    update_topics_curriculum()
