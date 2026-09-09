#!/usr/bin/env python3
"""
MJ Tech Hub - Phase 6.5 Content Expansion Generator (scripts/generate_phase6_5_tutorials.py)
Generates the initial 15 enterprise IT tutorials across:
- Windows (3 tutorials)
- Linux (3 tutorials)
- Servers (3 tutorials)
- Cybersecurity (3 tutorials)
- Cloud & AI (3 tutorials)

All tutorials strictly adhere to:
- Static SEO & TechArticle JSON-LD from https://themjtechhub.site
- Canonical Previous/Next order contract in data/tutorials.json
- Exactly one H1 in hero
- Semantic 72ch reading column
- Controlled code block styling (.tutorial-command, pre > code)
- Standardized callouts & responsive tables
- 100% Schema validation
"""

import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
TUTS_JSON_PATH = DATA_DIR / "tutorials.json"
CANONICAL_DOMAIN = "https://themjtechhub.site"
PUBLISH_DATE = "2026-09-09"

def build_tutorial_html(tut, cat_dir, cat_page):
    title = tut["title"]
    desc = tut["description"]
    category = tut["category"]
    level = tut["level"]
    level_class = level.lower()
    read_time = tut["readTime"]
    slug = tut["id"]
    body_content = tut["html"]
    
    canonical_url = f"{CANONICAL_DOMAIN}/tutorials/{cat_dir}/{slug}.html"
    
    # Format date for display: e.g. "Sep 09, 2026"
    formatted_date = datetime.strptime(PUBLISH_DATE, "%Y-%m-%d").strftime("%b %d, %Y")

    json_ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": desc,
        "url": canonical_url,
        "datePublished": PUBLISH_DATE,
        "dateModified": PUBLISH_DATE,
        "proficiencyLevel": level,
        "author": {
            "@type": "Organization",
            "name": "MJ Tech Hub",
            "url": CANONICAL_DOMAIN
        },
        "publisher": {
            "@type": "Organization",
            "name": "MJ Tech Hub",
            "url": CANONICAL_DOMAIN,
            "logo": {
                "@type": "ImageObject",
                "url": f"{CANONICAL_DOMAIN}/assets/logo/mj-tech-hub-logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        }
    }
    json_ld_str = json.dumps(json_ld, indent=4)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <script src="../../js/theme-init.js"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {category} Tutorial | MJ Tech Hub</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph -->
    <meta property="og:title" content="{title} | {category} Tutorial | MJ Tech Hub">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="MJ Tech Hub">
    <meta property="og:type" content="article">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title} | {category} Tutorial | MJ Tech Hub">
    <meta name="twitter:description" content="{desc}">

    <!-- Schema.org TechArticle JSON-LD -->
    <script type="application/ld+json">
{json_ld_str}
    </script>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../../css/themes.css">
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/responsive.css">
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <div id="site-header"></div>

    <main id="main-content" class="container py-4">
        <!-- Tutorial Hero Header -->
        <header id="tutorial-header" class="tutorial-hero">
            <nav aria-label="Breadcrumb" class="breadcrumb" style="margin-bottom: var(--space-4);">
                <a href="../../index.html">Home</a>
                <span class="breadcrumb-separator" aria-hidden="true">/</span>
                <a href="../../topics.html">Topics</a>
                <span class="breadcrumb-separator" aria-hidden="true">/</span>
                <a href="../../{cat_page}">{category}</a>
                <span class="breadcrumb-separator" aria-hidden="true">/</span>
                <span aria-current="page">{title}</span>
            </nav>

            <div class="tutorial-meta-row">
                <span class="cat-tut-badge {level_class}">{level}</span>
                <span class="tutorial-meta-item"><i class="fa-regular fa-clock" aria-hidden="true"></i> {read_time}</span>
                <span class="tutorial-meta-item"><i class="fa-regular fa-calendar" aria-hidden="true"></i> Updated: {formatted_date}</span>
            </div>

            <h1 class="tutorial-hero-title">{title}</h1>
            <p class="tutorial-hero-desc">{desc}</p>
        </header>

        <!-- Technical Reading Layout (Main Article + Sticky TOC) -->
        <div class="tutorial-reading-layout">
            <article class="tutorial-article content lesson-content">
{body_content}
            </article>

            <!-- Sticky Table of Contents Sidebar -->
            <aside class="tutorial-sidebar" aria-label="Table of Contents">
                <nav id="tutorial-toc" class="tutorial-toc">
                    <!-- Populated dynamically by tutorial.js -->
                </nav>
            </aside>
        </div>

        <!-- Dynamic Navigation Mount (Previous/Next, Back to Category, Related Tutorials) -->
        <div id="tutorial-footer-mount"></div>
    </main>

    <!-- Accessible Toast for Code Copy Feedback -->
    <div id="copy-toast" class="sr-toast" role="status" aria-live="polite">
        <i class="fa-solid fa-check text-success" aria-hidden="true"></i>
        <span id="copy-toast-msg">Code copied to clipboard!</span>
    </div>

    <div id="site-footer"></div>
    <script src="../../js/components.js"></script>
    <script src="../../js/tutorial.js" defer></script>
    <script src="../../js/main.js"></script>
    <script src="../../js/theme.js"></script>
</body>
</html>
"""

NEW_TUTORIALS = [
    # =========================================================================
    # WINDOWS BATCH (3 Tutorials)
    # =========================================================================
    {
        "id": "windows-operating-system-fundamentals",
        "title": "Windows Operating System Fundamentals",
        "category": "Windows",
        "category_dir": "windows",
        "category_page": "windows.html",
        "level": "Beginner",
        "readTime": "6 min read",
        "description": "Understand the core architecture of Microsoft Windows, including user mode, kernel mode, the NT executive, and system processes.",
        "keywords": "windows, operating system, os, kernel mode, user mode, nt executive, processes, hal, smss, csrss",
        "html": """<p>The <strong>Microsoft Windows</strong> operating system is built on a preemptive, reentrant, modular architecture developed from the Windows NT kernel. For system administrators, understanding the boundary between user applications and low-level kernel routines is critical when troubleshooting performance bottlenecks, blue screens (BSODs), and driver failures.</p>

<h2>User Mode vs Kernel Mode Architecture</h2>
<p>Windows enforces a hardware-backed security boundary separating unprivileged application execution from direct hardware access. The CPU operates in two distinct privilege states:</p>
<ul>
    <li><strong>User Mode (Ring 3):</strong> User applications, background services, and graphical shells run in isolated virtual address spaces. If an application crashes or generates an unhandled exception, it cannot corrupt memory belonging to other processes or the operating system kernel.</li>
    <li><strong>Kernel Mode (Ring 0):</strong> The core operating system code, Device Drivers, Hardware Abstraction Layer (HAL), and the Windows NT Executive execute in a single shared address space with complete access to physical memory and CPU instruction sets. A fatal crash in kernel mode results in a system halt (BugCheck).</li>
</ul>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Attribute</th>
                <th>User Mode (Ring 3)</th>
                <th>Kernel Mode (Ring 0)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Direct Hardware Access</strong></td>
                <td>Restricted via system call APIs</td>
                <td>Direct, unrestricted hardware access</td>
            </tr>
            <tr>
                <td><strong>Memory Space</strong></td>
                <td>Private 2GB/8TB virtual address space per process</td>
                <td>Shared single system virtual address space</td>
            </tr>
            <tr>
                <td><strong>Failure Impact</strong></td>
                <td>Process termination only; OS remains stable</td>
                <td>System crash (Blue Screen of Death / BSOD)</td>
            </tr>
            <tr>
                <td><strong>Key Components</strong></td>
                <td>Explorer.exe, Win32 apps, Windows services</td>
                <td>ntoskrnl.exe, HAL.dll, hardware drivers</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>The Windows NT Executive & HAL</h2>
<p>Kernel mode is divided into several foundational subsystems:</p>
<ul>
    <li><strong>Hardware Abstraction Layer (HAL):</strong> A low-level dynamic-link library (<code>hal.dll</code>) that isolates the kernel from differences in motherboard chipsets, CPU instruction extensions, and bus implementations.</li>
    <li><strong>The Kernel:</strong> Manages thread scheduling, CPU dispatching, multi-core synchronization, and hardware interrupt handling.</li>
    <li><strong>The NT Executive:</strong> Contains core subsystem managers including the Memory Manager (virtual paging), Object Manager (handles and securable objects), Process Manager, and I/O Manager (managing file and storage drivers).</li>
</ul>

<h2>Critical Core System Processes</h2>
<p>When Windows boots, a deterministic chain of native system processes initializes before user logons are permitted:</p>
<ul>
    <li><strong>System Idle Process:</strong> Represents unused CPU cycles; when running, it instructs the processor to enter power-saving C-states.</li>
    <li><strong>System (PID 4):</strong> The container for kernel-mode worker threads executing asynchronous background routines.</li>
    <li><strong>smss.exe (Session Manager Subsystem):</strong> The first user-mode process created. It configures virtual memory paging files, launches the graphical subsystem (<code>win32k.sys</code>), and spawns <code>csrss.exe</code> and <code>wininit.exe</code>.</li>
    <li><strong>csrss.exe (Client/Server Runtime Subsystem):</strong> Manages Win32 console windows and process creation/deletion.</li>
    <li><strong>wininit.exe:</strong> Initializes the secure Windows security infrastructure, spawning the Service Control Manager and Local Security Authority.</li>
    <li><strong>services.exe:</strong> The Service Control Manager (SCM), responsible for starting, stopping, and monitoring automatic background services.</li>
    <li><strong>lsass.exe:</strong> The Local Security Authority Subsystem Service, enforcing local security policy, password verification, and authentication token generation (Kerberos/NTLM).</li>
</ul>

<p><em>Important: The lsass.exe process is frequently targeted by credential dumping tools like Mimikatz. Enterprise Windows configurations must enforce LSA Protection (RunAsPPL) and Credential Guard to prevent unprivileged memory injection.</em></p>

<h2>Administrator Inspection Tools</h2>
<p>Administrators should leverage built-in and Sysinternals utilities to inspect process parentage, memory allocation, and thread stacks:</p>

<div class="tutorial-command">
REM Query running system processes with PID and session ID in CMD
tasklist /fo table /v | findstr /i "smss csrss lsass services"
</div>

<p>For deeper thread analysis, Microsoft Sysinternals <strong>Process Explorer</strong> displays a visual process tree showing exact child-parent relationships, verifying that <code>csrss.exe</code> and <code>lsass.exe</code> originate only from authentic parent processes.</p>

<h2>Summary</h2>
<p>Windows achieves enterprise reliability by strictly segregating User Mode applications from Kernel Mode hardware execution. Understanding the role of the HAL, the NT Executive, and foundational system processes like <code>lsass.exe</code> and <code>services.exe</code> enables IT professionals to diagnose application hangs, detect malicious process masquerading, and analyze system stability with confidence.</p>"""
    },
    {
        "id": "windows-command-prompt-basics",
        "title": "Windows Command Prompt Basics",
        "category": "Windows",
        "category_dir": "windows",
        "category_page": "windows.html",
        "level": "Beginner",
        "readTime": "7 min read",
        "description": "Master essential Windows CMD commands for file navigation, system configuration, network diagnostics, and administrator maintenance.",
        "keywords": "cmd, command prompt, windows cli, dir, cd, systeminfo, tasklist, sfc, dism, batch",
        "html": """<p>The <strong>Windows Command Prompt (cmd.exe)</strong> remains an indispensable tool for IT support engineers, system administrators, and infrastructure technicians. While PowerShell provides deep object-oriented scripting, CMD provides rapid, lightweight access to native utilities across every version of Windows without execution policy restrictions.</p>

<h2>Understanding Standard vs Elevated Privileges</h2>
<p>Windows User Account Control (UAC) runs Command Prompt sessions in standard user context by default. Commands modifying system state, repairing file system integrity, or adjusting firewall rules require an <strong>Elevated Command Prompt</strong> (Run as Administrator):</p>
<ul>
    <li><strong>Standard Context:</strong> Read-only operations, user profile directory navigation, basic network reachability tests (<code>ping</code>, <code>tracert</code>).</li>
    <li><strong>Elevated Context:</strong> Disk repair (<code>chkdsk</code>), servicing repairs (<code>sfc</code>, <code>dism</code>), network stack resets (<code>netsh</code>), and service state changes (<code>net start/stop</code>).</li>
</ul>

<h2>Filesystem Navigation & Directory Control</h2>
<p>CMD utilizes drive letters and standard pathing syntax. Unlike Unix environments, drive letter changes require entering the drive letter directly rather than using <code>cd</code>:</p>

<div class="tutorial-command">
REM Switch from C: to D: drive
D:

REM Change directory to Windows logs folder
cd C:\\Windows\\System32\\winevt\\Logs

REM List directory contents with file size and timestamp
dir /a /o:d

REM Create a new administrative maintenance directory
mkdir C:\\Support\\Diagnostics
</div>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Command</th>
                <th>Syntax / Arguments</th>
                <th>Primary Administrative Purpose</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>cd</code></td>
                <td><code>cd /d D:\\Logs</code></td>
                <td>Change directory (use <code>/d</code> to change drive and directory simultaneously)</td>
            </tr>
            <tr>
                <td><code>dir</code></td>
                <td><code>dir /a:h /s</code></td>
                <td>Display directory contents, including hidden files and subdirectories</td>
            </tr>
            <tr>
                <td><code>mkdir</code> / <code>rmdir</code></td>
                <td><code>rmdir /s /q temp_dir</code></td>
                <td>Create or remove directories recursively in quiet mode</td>
            </tr>
            <tr>
                <td><code>del</code></td>
                <td><code>del /f /q filename</code></td>
                <td>Delete files with force override on read-only files</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>System Information & Process Inspection</h2>
<p>When triaging a newly assigned server or workstation, gather operating system build details, BIOS version, memory totals, and active task lists directly:</p>

<div class="tutorial-command">
REM Display comprehensive OS build, memory, hotfixes, and NIC details
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"Total Physical Memory"

REM Display active processes sorted by memory usage
tasklist /fi "memusage gt 100000"

REM Terminate an unresponsive application by process name
taskkill /im notepad.exe /f
</div>

<h2>Network Diagnostics in CMD</h2>
<p>CMD hosts the core networking troubleshooting tools used in day-to-day help desk and NOC operations:</p>
<ul>
    <li><code>ipconfig /all</code>: Displays full TCP/IP configuration including DHCP lease dates, DNS servers, and MAC addresses.</li>
    <li><code>ipconfig /flushdns</code>: Clears the local DNS resolver cache to enforce new record lookups.</li>
    <li><code>ping -n 4 -l 1000 8.8.8.8</code>: Tests IP reachability and detects MTU fragmentation issues.</li>
    <li><code>tracert -d 1.1.1.1</code>: Traces router hops without performing reverse DNS lookups, speeding up path discovery.</li>
</ul>

<h2>System Health & Image Repair: SFC and DISM</h2>
<p>When Windows experiences system file corruption or application crashes following an update, administrators deploy System File Checker and Deployment Image Servicing and Management:</p>

<div class="tutorial-command">
REM 1. Check and repair the Windows Component Store image online
DISM.exe /Online /Cleanup-image /Restorehealth

REM 2. Scan and repair protected operating system files against known good cache
sfc /scannow
</div>

<p><em>Warning: Always execute DISM prior to SFC if corruption is suspected. SFC relies on the local Windows Component Store cache (WinSxS); if the store itself is corrupted, SFC will fail to repair affected system binaries.</em></p>

<h2>Summary</h2>
<p>Command Prompt remains a core administrative utility across Windows client and server operating systems. Mastering directory navigation, process management with <code>tasklist</code> and <code>taskkill</code>, network diagnostics with <code>ipconfig</code>, and recovery routines with <code>sfc</code> and <code>dism</code> provides immediate diagnostic leverage in enterprise troubleshooting.</p>"""
    },
    {
        "id": "powershell-fundamentals-for-administrators",
        "title": "PowerShell Fundamentals for Administrators",
        "category": "Windows",
        "category_dir": "windows",
        "category_page": "windows.html",
        "level": "Intermediate",
        "readTime": "8 min read",
        "description": "Learn how object-oriented pipelines, verb-noun cmdlet syntax, and provider drives empower modern enterprise Windows management.",
        "keywords": "powershell, posh, cmdlets, object pipeline, get-service, get-process, administration, automation, where-object",
        "html": """<p><strong>Windows PowerShell</strong> is a task-based command-line shell and scripting language designed specifically for system administrators. Unlike traditional text-based shells (such as CMD or Bash) where outputs are streams of raw characters that require regex parsing, PowerShell passes structured <strong>.NET objects</strong> through its execution pipeline.</p>

<h2>The Object Pipeline Concept</h2>
<p>In traditional shells, command output is plain text. To extract a specific column, administrators must manipulate text strings using tools like <code>awk</code>, <code>sed</code>, or <code>findstr</code>. In PowerShell, every command outputs rich objects containing strongly-typed properties and methods.</p>
<p>For example, when running <code>Get-Service</code>, PowerShell does not return text columns; it returns a collection of <code>System.ServiceProcess.ServiceController</code> objects. You can directly inspect, filter, or invoke actions on these objects without string manipulation:</p>

<div class="tutorial-command">
# Filter services where Status property equals 'Running'
Get-Service | Where-Object Status -eq 'Running' | Select-Object -Property Name, DisplayName, StartType
</div>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Feature</th>
                <th>Command Prompt (CMD)</th>
                <th>Windows PowerShell</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Data Type</strong></td>
                <td>Raw ASCII / Unicode Text strings</td>
                <td>Rich .NET structured objects</td>
            </tr>
            <tr>
                <td><strong>Syntax Pattern</strong></td>
                <td>Inconsistent legacy parameters (<code>/a</code>, <code>-s</code>)</td>
                <td>Standardized <code>Verb-Noun</code> pattern</td>
            </tr>
            <tr>
                <td><strong>Pipeline Handling</strong></td>
                <td>Streams characters; requires parsing</td>
                <td>Streams objects; preserves properties and data types</td>
            </tr>
            <tr>
                <td><strong>Extensibility</strong></td>
                <td>External binaries and batch files</td>
                <td>PowerShell modules, .NET classes, REST APIs</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>The Verb-Noun Cmdlet Structure</h2>
<p>PowerShell commands (cmdlets) follow a strict <code>Verb-Noun</code> naming convention. Microsoft maintains an approved list of verbs to ensure semantic consistency across modules:</p>
<ul>
    <li><code>Get</code>: Retrieves an object or data without modifying state (e.g., <code>Get-Process</code>, <code>Get-LocalUser</code>).</li>
    <li><code>Set</code>: Modifies an existing configuration or resource (e.g., <code>Set-Service -Name Spooler -StartupType Disabled</code>).</li>
    <li><code>New</code>: Creates a new resource (e.g., <code>New-Item -ItemType Directory -Path "C:\\Scripts"</code>).</li>
    <li><code>Remove</code>: Deletes a resource (e.g., <code>Remove-Item -Path "C:\\Temp\\old.log"</code>).</li>
    <li><code>Start / Stop / Restart</code>: Controls operational lifecycle (e.g., <code>Restart-Service -Name W32Time</code>).</li>
</ul>

<h2>Self-Discovery: Get-Help, Get-Command, and Get-Member</h2>
<p>PowerShell is designed to be self-documenting. Three core cmdlets allow administrators to discover syntax, discover available tools, and inspect object properties without external documentation:</p>

<div class="tutorial-command">
# 1. Find all cmdlets managing IP configuration
Get-Command -Noun *IPConfiguration*

# 2. View documentation and usage examples for a cmdlet
Get-Help Test-NetConnection -Examples

# 3. Inspect all properties and callable methods on an object
Get-Process -Name explorer | Get-Member
</div>

<h2>Working with PowerShell Providers and PSDrives</h2>
<p>PowerShell treats diverse hierarchical data stores like traditional filesystem drives. Using <strong>PSProviders</strong>, administrators navigate the Windows Registry, certificate stores, and environment variables using familiar commands like <code>cd</code> (Set-Location) and <code>dir</code> (Get-ChildItem):</p>

<div class="tutorial-command">
# View all active PowerShell drives
Get-PSDrive

# Navigate into the HKEY_LOCAL_MACHINE registry hive
Set-Location -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion

# List registry keys and values in this location
Get-ItemProperty -Path .
</div>

<h2>Essential Administrator Workflows</h2>
<p>Here are high-frequency enterprise administration commands executed during system provisioning and troubleshooting:</p>

<div class="tutorial-command">
# Test remote port connectivity (modern alternative to telnet)
Test-NetConnection -ComputerName "dc01.corp.local" -Port 389

# Identify the top 5 memory-consuming processes
Get-Process | Sort-Object -Property WorkingSet64 -Descending | Select-Object -First 5 -Property Name, Id, @{{Name="Memory(MB)";Expression={{[math]::Round($_.WorkingSet64 / 1MB, 2)}}}}

# Query system event log for recent disk errors
Get-WinEvent -FilterHashtable @{{LogName="System"; Level=2; ProviderName="disk"}} -MaxEvents 10
</div>

<p><em>Note: Windows 10/11 and Windows Server include Windows PowerShell 5.1 built-in. Modern enterprise environments increasingly adopt PowerShell 7 (pwsh), which runs cross-platform on .NET Core, offering enhanced performance and parallel pipeline processing via ForEach-Object -Parallel.</em></p>

<h2>Summary</h2>
<p>PowerShell transforms Windows system administration from repetitive GUI interactions into repeatable, automated pipelines. By mastering Verb-Noun cmdlet discovery, object filtering with <code>Where-Object</code>, and provider-based navigation, engineers gain complete programmatic control over enterprise environments.</p>"""
    },

    # =========================================================================
    # LINUX BATCH (3 Tutorials)
    # =========================================================================
    {
        "id": "linux-operating-system-fundamentals",
        "title": "Linux Operating System Fundamentals",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Beginner",
        "readTime": "6 min read",
        "description": "Explore the open-source Linux operating system architecture, the monolithic kernel, system libraries, shells, and enterprise distributions.",
        "keywords": "linux, kernel, shell, gnu, distribution, rhel, debian, ubuntu, monolithic kernel, sysadmin",
        "html": """<p><strong>Linux</strong> is a family of open-source Unix-like operating systems based on the Linux kernel, first released by Linus Torvalds in 1991. Today, Linux powers the overwhelming majority of public cloud infrastructure, enterprise servers, supercomputers, and containerized microservices worldwide.</p>

<h2>The Anatomy of a Linux Distribution</h2>
<p>When people refer to "Linux," they are usually referring to a <strong>GNU/Linux Distribution (distro)</strong>. A complete operating system combines several independent layers:</p>
<ul>
    <li><strong>The Linux Kernel:</strong> The core program that directly controls physical CPU scheduling, virtual memory management, device drivers, and network socket operations.</li>
    <li><strong>GNU System Utilities:</strong> Foundational command-line tools (such as <code>ls</code>, <code>cat</code>, <code>cp</code>, <code>grep</code>) and the standard C library (<code>glibc</code>) providing system call wrappers.</li>
    <li><strong>Init System & Service Manager:</strong> The parent process (PID 1), predominantly <code>systemd</code> in modern distros, responsible for bootstrapping the userspace and supervising daemons.</li>
    <li><strong>Shell Interface:</strong> Command interpreter (typically <code>bash</code>, <code>zsh</code>, or <code>sh</code>) allowing users to interact with the system via terminal or automated scripts.</li>
    <li><strong>Package Manager:</strong> Software installation and dependency resolution tools (e.g., <code>apt</code>, <code>dnf</code>, <code>pacman</code>).</li>
</ul>

<h2>Monolithic Kernel vs User Space</h2>
<p>The Linux kernel follows a <strong>monolithic architecture</strong>. In contrast to microkernels where drivers and filesystems run as isolated user processes, core Linux subsystems run inside a single privileged address space for maximum execution speed:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Component</th>
                <th>Execution Domain</th>
                <th>Primary Function</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Hardware</strong></td>
                <td>Physical Layer</td>
                <td>CPU, RAM, Storage Controllers, NICs</td>
            </tr>
            <tr>
                <td><strong>Linux Kernel</strong></td>
                <td>Kernel Space (Ring 0)</td>
                <td>Process scheduler, memory manager, VFS, network stack</td>
            </tr>
            <tr>
                <td><strong>Loadable Kernel Modules (LKM)</strong></td>
                <td>Kernel Space (Ring 0)</td>
                <td>Dynamically inserted hardware drivers and network filters (iptables/nftables)</td>
            </tr>
            <tr>
                <td><strong>System Calls (syscalls)</strong></td>
                <td>Boundary Interface</td>
                <td>Controlled gateway (read, write, open, fork) bridging User to Kernel space</td>
            </tr>
            <tr>
                <td><strong>User Applications & Daemons</strong></td>
                <td>User Space (Ring 3)</td>
                <td>Web servers (nginx), databases (PostgreSQL), SSH daemon (sshd), shells</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Major Enterprise Distribution Families</h2>
<p>Enterprise Linux deployments predominantly cluster around two primary packaging and release paradigms:</p>
<ul>
    <li><strong>Debian Family (Debian, Ubuntu LTS):</strong> Utilizes the <code>.deb</code> package format and the <code>apt</code> package manager. Renowned for massive package repositories and predictable Long-Term Support (LTS) release cadence.</li>
    <li><strong>Red Hat Family (RHEL, Rocky Linux, AlmaLinux, Fedora):</strong> Utilizes the <code>.rpm</code> format and <code>dnf</code> / <code>yum</code> package managers. Favored in corporate datacenters requiring strict enterprise compliance, SELinux security policies, and vendor support contracts.</li>
    <li><strong>SUSE Family (SLES, openSUSE):</strong> Enterprise distribution widely used in mission-critical SAP infrastructure, leveraging <code>zypper</code> and YaST.</li>
</ul>

<h2>Basic System Identification Commands</h2>
<p>To inspect your running kernel version, hardware architecture, and distribution details, run the following commands:</p>

<div class="tutorial-command">
# Inspect the Linux kernel release and architecture
uname -r -m

# Inspect distribution identity, release version, and codename
cat /etc/os-release

# Inspect currently loaded dynamic kernel modules
lsmod | head -n 10
</div>

<p><em>Note: Linux kernel versions follow a Major.Minor.Patch convention (e.g., 6.8.0-40-generic). Enterprise distributions often backport security patches into older, proven kernel versions to guarantee binary compatibility across years of deployment.</em></p>

<h2>Summary</h2>
<p>Linux combines a modular monolithic kernel with open-source GNU userland utilities and systemd process supervision. Whether managing Ubuntu servers in AWS or RHEL hypervisors in an on-premises datacenter, understanding how system calls connect user programs to kernel hardware controls is foundational to Linux system administration.</p>"""
    },
    {
        "id": "linux-filesystem-hierarchy-explained",
        "title": "Linux Filesystem Hierarchy Explained",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Beginner",
        "readTime": "7 min read",
        "description": "Demystify the Linux Filesystem Hierarchy Standard (FHS), covering /, /etc, /var, /home, /dev, /proc, and virtual filesystems.",
        "keywords": "linux, fhs, filesystem, hierarchy, root, etc, var, proc, sys, dev, mount, sysadmin",
        "html": """<p>Unlike Windows, which assigns separate drive letters (such as <code>C:</code> or <code>D:</code>) to physical partitions, Linux organizes all files and storage devices into a single unified inverted tree structure starting from the root directory: <code>/</code>. This standardized structure is codified by the <strong>Filesystem Hierarchy Standard (FHS)</strong>.</p>

<h2>The "Everything Is a File" Philosophy</h2>
<p>A central design tenet of Unix and Linux is that system resources are presented as files. Physical hard drives, terminal connections, network sockets, process memory tables, and hardware sensors are all accessible through standard filesystem paths using standard I/O system calls (<code>open</code>, <code>read</code>, <code>write</code>, <code>close</code>).</p>

<h2>Key Directory Breakdown</h2>
<p>Every standard Linux installation arranges core files into dedicated top-level directories according to their lifecycle, mutability, and sharing capabilities:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Directory</th>
                <th>Primary Purpose</th>
                <th>Administrator Examples</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>/</code></td>
                <td>Root directory; the anchor of the entire filesystem tree</td>
                <td>All paths originate here</td>
            </tr>
            <tr>
                <td><code>/bin</code>, <code>/sbin</code></td>
                <td>Essential binary executables (often symlinked to <code>/usr/bin</code>)</td>
                <td><code>/bin/ls</code>, <code>/sbin/ip</code>, <code>/sbin/fdisk</code></td>
            </tr>
            <tr>
                <td><code>/etc</code></td>
                <td>Host-specific system configuration files</td>
                <td><code>/etc/ssh/sshd_config</code>, <code>/etc/hosts</code>, <code>/etc/fstab</code></td>
            </tr>
            <tr>
                <td><code>/var</code></td>
                <td>Variable data that changes continuously during runtime</td>
                <td><code>/var/log/syslog</code>, <code>/var/spool/cron</code>, <code>/var/lib/docker</code></td>
            </tr>
            <tr>
                <td><code>/home</code></td>
                <td>User personal directories and environment configurations</td>
                <td><code>/home/john/.ssh/authorized_keys</code></td>
            </tr>
            <tr>
                <td><code>/root</code></td>
                <td>Home directory for the root superuser account</td>
                <td>Isolated from <code>/home</code> so root can log in even if <code>/home</code> is unmounted</td>
            </tr>
            <tr>
                <td><code>/dev</code></td>
                <td>Device nodes representing hardware peripherals</td>
                <td><code>/dev/sda</code> (disk), <code>/dev/nvme0n1</code> (NVMe drive), <code>/dev/urandom</code></td>
            </tr>
            <tr>
                <td><code>/proc</code></td>
                <td>Pseudo-filesystem reflecting kernel state and running processes</td>
                <td><code>/proc/cpuinfo</code>, <code>/proc/meminfo</code>, <code>/proc/[PID]/cmdline</code></td>
            </tr>
            <tr>
                <td><code>/sys</code></td>
                <td>Kernel pseudo-filesystem exposing hardware device parameters</td>
                <td><code>/sys/class/net/eth0/operstate</code></td>
            </tr>
            <tr>
                <td><code>/tmp</code></td>
                <td>Temporary storage cleared on system reboot</td>
                <td>Scratch files, temporary installation archives</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Virtual Filesystems: /proc and /sys</h2>
<p>Directories such as <code>/proc</code> and <code>/sys</code> do not occupy space on your hard drive. They are <strong>virtual filesystems</strong> dynamically generated in RAM by the Linux kernel. When you read a file inside <code>/proc</code>, the kernel intercepts the read request and generates formatted real-time telemetry:</p>

<div class="tutorial-command">
# View real-time CPU specifications directly from the kernel
cat /proc/cpuinfo | grep "model name" | head -n 1

# View system RAM utilization
cat /proc/meminfo | head -n 5

# Inspect the command line arguments of process PID 1 (systemd)
cat /proc/1/cmdline
</div>

<h2>Storage Mounting and the /etc/fstab File</h2>
<p>In Linux, storage devices are made accessible by attaching them to an empty directory known as a <strong>Mount Point</strong>. The <code>/etc/fstab</code> (File Systems Table) file defines which partitions automatically mount at boot time:</p>

<div class="tutorial-command">
# View all active disk partitions and mount points
lsblk -f

# Check filesystem disk space utilization in human-readable format
df -h
</div>

<p><em>Warning: Never edit /etc/fstab without testing syntax using mount -a beforehand. A syntax error or missing UUID in /etc/fstab can cause the system to drop into an emergency maintenance shell during reboot.</em></p>

<h2>Summary</h2>
<p>The Linux filesystem hierarchy organizes static executables, dynamic system configurations in <code>/etc</code>, variable log telemetry in <code>/var</code>, and kernel virtual structures in <code>/proc</code> into a clean, predictable structure. Understanding the FHS ensures administrators can locate configuration files, diagnose mounting failures, and safely manage enterprise storage.</p>"""
    },
    {
        "id": "essential-linux-terminal-commands",
        "title": "Essential Linux Terminal Commands",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Intermediate",
        "readTime": "8 min read",
        "description": "Master core command-line utilities for file manipulation, text processing, permission management, process inspection, and network diagnostics.",
        "keywords": "linux commands, terminal, bash, ls, grep, find, chmod, chown, systemctl, ps, top, journalctl",
        "html": """<p>The <strong>command-line interface (CLI)</strong> is the primary management interface for enterprise Linux servers. Operating headless systems requires fluency in text manipulation, process inspection, file permissions, and systemd service control.</p>

<h2>File Operations & Directory Navigation</h2>
<p>Standard file management relies on foundational POSIX utilities. Using command flags accelerates directory inspection:</p>

<div class="tutorial-command">
# Detailed directory listing showing hidden files, human sizes, and permissions
ls -lah

# Copy a directory recursively preserving file timestamps and ownership
cp -a /var/www/html /backup/html_backup

# Move or rename files
mv config.conf.bak config.conf

# Find all log files modified within the last 24 hours larger than 50MB
find /var/log -type f -name "*.log" -mtime -1 -size +50M
</div>

<h2>Text Processing: Grep, Tail, and Pipes</h2>
<p>Log inspection is a daily responsibility for infrastructure engineers. Linux provides high-performance pattern matching and stream filtering tools:</p>

<div class="tutorial-command">
# Search for error lines in all log files recursively, ignoring case
grep -ri "error" /var/log/

# Follow log output in real-time as new events append
tail -f /var/log/nginx/access.log

# Count how many times an IP appears in an authentication log
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr
</div>

<h2>File Permissions and Ownership: chmod and chown</h2>
<p>Linux enforces a strict permission model based on <strong>User (u)</strong>, <strong>Group (g)</strong>, and <strong>Others (o)</strong> across three access rights: <strong>Read (4)</strong>, <strong>Write (2)</strong>, and <strong>Execute (1)</strong>:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Numeric Mode</th>
                <th>Symbolic Mode</th>
                <th>Permissions Breakdown</th>
                <th>Common Enterprise Use Case</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>755</code></td>
                <td><code>rwxr-xr-x</code></td>
                <td>User: read/write/execute; Group/Other: read/execute</td>
                <td>Web server directories, executable scripts</td>
            </tr>
            <tr>
                <td><code>644</code></td>
                <td><code>rw-r--r--</code></td>
                <td>User: read/write; Group/Other: read-only</td>
                <td>Standard configuration files, web HTML files</td>
            </tr>
            <tr>
                <td><code>600</code></td>
                <td><code>rw-------</code></td>
                <td>User: read/write; Group/Other: no access</td>
                <td>SSH private keys (<code>id_rsa</code>), sensitive credentials</td>
            </tr>
            <tr>
                <td><code>700</code></td>
                <td><code>rwx------</code></td>
                <td>User: full access; Group/Other: no access</td>
                <td>User <code>.ssh</code> directories, private backup folders</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="tutorial-command">
# Set secure permissions on an SSH private key
chmod 600 ~/.ssh/id_ed25519

# Recursively change file ownership to user 'www-data' and group 'www-data'
chown -R www-data:www-data /var/www/html
</div>

<h2>Process and Service Management with systemd</h2>
<p>Modern Linux distributions use <code>systemd</code> as the init system and service manager. Administrators control daemon states and review system logs using <code>systemctl</code> and <code>journalctl</code>:</p>

<div class="tutorial-command">
# Check service status, active state, and recent log snippet
systemctl status sshd

# Restart an updated service and ensure it starts automatically on boot
systemctl restart nginx
systemctl enable nginx

# View real-time system logs for a specific service unit
journalctl -u nginx -f --no-pager
</div>

<h2>System Performance & Process Inspection</h2>
<p>When investigating high CPU or memory utilization, use process inspection tools:</p>

<div class="tutorial-command">
# List all running processes with full command lines and memory usage
ps aux --sort=-%mem | head -n 10

# Send a polite termination signal (SIGTERM) to a stuck process
kill -15 [PID]
</div>

<p><em>Important: Always prefer SIGTERM (kill -15) before resorting to SIGKILL (kill -9). SIGTERM allows the target process to close open database connections, flush memory buffers, and release file locks gracefully.</em></p>

<h2>Summary</h2>
<p>Mastering core terminal commands—navigating the filesystem, parsing logs with <code>grep</code> and <code>tail</code>, enforcing permissions with <code>chmod</code> and <code>chown</code>, and supervising daemons with <code>systemctl</code>—gives administrators the fundamental toolkit required to operate enterprise Linux servers securely and reliably.</p>"""
    },

    # =========================================================================
    # SERVERS BATCH (3 Tutorials)
    # =========================================================================
    {
        "id": "what-is-a-server",
        "title": "What Is a Server?",
        "category": "Servers",
        "category_dir": "servers",
        "category_page": "servers.html",
        "level": "Beginner",
        "readTime": "5 min read",
        "description": "Discover what defines server hardware and software, client-server models, high-availability components, and enterprise roles.",
        "keywords": "server, client-server, hardware, ecc ram, redundant power, datacenter, rack, tower, blade, ipmi, idrac",
        "html": """<p>In enterprise computing, the term <strong>server</strong> refers to both specialized hardware and dedicated software applications that provide centralized resources, services, or data to other computers—known as <strong>clients</strong>—across a local network or the Internet.</p>

<h2>The Client-Server Architecture</h2>
<p>The client-server model distributes computational tasks between service requestors (clients) and service providers (servers):</p>
<ul>
    <li><strong>Client:</strong> A workstation, laptop, mobile device, or browser that requests data or computational services (e.g., requesting a web page, authenticating a user, or querying a database).</li>
    <li><strong>Server:</strong> A high-availability system that continuously listens for incoming client requests on designated network ports, validates authorization, processes queries, and returns formatted responses.</li>
</ul>

<h2>Desktop vs Enterprise Server Hardware</h2>
<p>While a standard desktop computer can technically run server software, enterprise server hardware is specifically engineered for <strong>24/7/365 reliability</strong>, thermal efficiency, and fault tolerance:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Hardware Subsystem</th>
                <th>Consumer Desktop PC</th>
                <th>Enterprise Server</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Memory (RAM)</strong></td>
                <td>Non-ECC RAM (undetected bit-flips can crash OS)</td>
                <td><strong>ECC (Error-Correcting Code) RAM:</strong> Detects and automatically corrects memory bit-flip errors</td>
            </tr>
            <tr>
                <td><strong>Power Delivery</strong></td>
                <td>Single standard ATX Power Supply Unit (PSU)</td>
                <td><strong>Redundant Hot-Swap PSUs:</strong> Two power supplies connected to separate electrical circuits; one can fail without downtime</td>
            </tr>
            <tr>
                <td><strong>Storage Drives</strong></td>
                <td>Consumer SATA/NVMe SSDs; internal cables</td>
                <td><strong>Enterprise SAS/NVMe drives:</strong> Hot-swappable drive bays backed by Hardware RAID controllers with battery backup caches</td>
            </tr>
            <tr>
                <td><strong>Remote Management</strong></td>
                <td>Software remote desktop (requires OS running)</td>
                <td><strong>Out-of-Band Management (iDRAC / iLO / IPMI):</strong> Independent dedicated processor accessible even if OS is crashed or powered off</td>
            </tr>
            <tr>
                <td><strong>Cooling & Form Factor</strong></td>
                <td>Quiet consumer tower chassis</td>
                <td>High-CFM redundant fan arrays designed for standardized datacenter server racks (1U, 2U, 4U)</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Server Form Factors</h2>
<p>Datacenter infrastructure utilizes standardized physical packaging:</p>
<ul>
    <li><strong>Rackmount Servers:</strong> Measured in standard Rack Units (1U = 1.75 inches tall). Designed to bolt into 19-inch equipment racks, optimizing floor space, cable routing, and cooling airflow.</li>
    <li><strong>Tower Servers:</strong> Self-contained upright chassis resembling desktop towers. Popular in branch offices or small businesses where dedicated server racks and cooled server rooms are unavailable.</li>
    <li><strong>Blade Servers:</strong> Ultra-dense modular chassis housing multiple stripped-down server "blades" that share centralized power supplies, cooling fans, and network backplanes.</li>
</ul>

<h2>Common Enterprise Server Roles</h2>
<p>Servers are deployed to handle specific infrastructural responsibilities across organizations:</p>
<ul>
    <li><strong>Domain Controller (DC):</strong> Hosts Active Directory Domain Services to provide centralized identity authentication, password policy enforcement, and Kerberos ticket granting.</li>
    <li><strong>DNS & DHCP Server:</strong> Translates hostnames into IP addresses and dynamically leases network configurations to connecting endpoints.</li>
    <li><strong>File & Storage Server:</strong> Hosts corporate shares over SMB/NFS protocols, backed by access control lists and automated snapshots.</li>
    <li><strong>Hypervisor Host:</strong> Runs virtualization software (VMware ESXi, Proxmox VE, Microsoft Hyper-V) to host dozens of virtual machines on a single physical footprint.</li>
</ul>

<p><em>Note: Modern enterprise server administration heavily relies on Out-of-Band Management (OOBM) controllers, such as Dell iDRAC or HPE iLO. These hardware cards feature dedicated NICs, allowing administrators to mount virtual ISO media, change BIOS settings, and reboot unresponsive servers remotely over a secure network.</em></p>

<h2>Summary</h2>
<p>A server is defined by its operational role in answering client requests and its hardware resilience. Built with ECC memory, redundant hot-swappable power supplies, hardware RAID, and out-of-band management controllers, enterprise servers ensure mission-critical business services remain online continuously.</p>"""
    },
    {
        "id": "windows-server-fundamentals",
        "title": "Windows Server Fundamentals",
        "category": "Servers",
        "category_dir": "servers",
        "category_page": "servers.html",
        "level": "Intermediate",
        "readTime": "8 min read",
        "description": "An introductory guide to Microsoft Windows Server editions, roles and features, Server Manager, Windows Admin Center, and Server Core.",
        "keywords": "windows server, active directory, server manager, roles, features, server core, windows admin center, hyper-v, sysadmin",
        "html": """<p><strong>Microsoft Windows Server</strong> is the foundation of enterprise on-premises directory services, file storage, and hybrid infrastructure. Sharing the core Windows NT kernel with client versions of Windows, it includes specialized administrative tools, hardened network protocols, and multi-tenant enterprise server roles.</p>

<h2>Windows Server Editions & Licensing</h2>
<p>Modern releases (Windows Server 2019, 2022, 2025) are licensed per physical CPU core and categorized into two primary enterprise editions:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Edition</th>
                <th>Virtualization Rights</th>
                <th>Target Deployment Scenario</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Windows Server Standard</strong></td>
                <td>Includes licensing for <strong>2 Virtual Machines</strong> (or Hyper-V containers) per licensed host</td>
                <td>Physical branch office servers or lightly virtualized environments</td>
            </tr>
            <tr>
                <td><strong>Windows Server Datacenter</strong></td>
                <td>Includes <strong>Unlimited Virtual Machines</strong> on the licensed physical host</td>
                <td>Enterprise private clouds, high-density Hyper-V clusters, and Software-Defined Storage (Storage Spaces Direct)</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Server Core vs Desktop Experience</h2>
<p>During installation, administrators choose between two operating environments:</p>
<ul>
    <li><strong>Server Core (Recommended):</strong> Installs a stripped-down headless operating system without graphical desktop shells (Windows Explorer). Server Core consumes significantly less RAM (often under 1.5GB), requires approximately 40% fewer security patches, reboots faster, and dramatically minimizes the attack surface.</li>
    <li><strong>Server with Desktop Experience:</strong> Installs the full graphical user interface (GUI). Useful for legacy management tools, remote desktop session hosts, or specialized application prerequisites.</li>
</ul>

<h2>The Roles & Features Architecture</h2>
<p>Windows Server functionality is modularized into two distinct categories:</p>
<ul>
    <li><strong>Server Roles:</strong> Major software programs that define what the server does across the network (e.g., Active Directory Domain Services, DNS Server, DHCP Server, Hyper-V, Web Server IIS).</li>
    <li><strong>Features:</strong> Auxiliary utility programs that support or enhance server capabilities (e.g., Failover Clustering, BitLocker Drive Encryption, Windows Server Backup, Group Policy Management).</li>
</ul>

<h2>Central Management: Server Manager & Windows Admin Center</h2>
<p>Administrators manage server fleets using modern centralized orchestration platforms:</p>
<ul>
    <li><strong>Server Manager:</strong> The classic MMC-based console allowing administrators to provision roles, monitor event logs, and review service statuses across multiple servers from a single dashboard.</li>
    <li><strong>Windows Admin Center (WAC):</strong> A modern, browser-based management tool connecting over secure WinRM/PowerShell remoting. WAC consolidates certificate management, performance graphs, firewall rules, and hybrid Azure integrations into a lightweight HTML5 console.</li>
</ul>

<h2>PowerShell Administration for Windows Server</h2>
<p>Administrative workflows on Server Core are performed programmatically using PowerShell. The <code>ServerManager</code> module provides cmdlets to audit and install capabilities:</p>

<div class="tutorial-command">
# 1. Query all available roles and features matching 'DNS' or 'DHCP'
Get-WindowsFeature -Name *DNS*, *DHCP*

# 2. Install the DNS Server role including management command line tools
Install-WindowsFeature -Name DNS -IncludeManagementTools

# 3. View operational health and restart the DHCP Server service
Get-Service -Name DHCPServer | Restart-Service
</div>

<p><em>Warning: When deploying Server Core in enterprise environments, verify that Windows Defender Firewall permits remote administration traffic (specifically WinRM, RPC, and WMI) before disconnecting physical monitor access.</em></p>

<h2>Summary</h2>
<p>Windows Server delivers core infrastructure services through modular Roles and Features. By deploying Server Core to reduce attack surface and leveraging Windows Admin Center and PowerShell for centralized fleet administration, infrastructure teams establish a secure, reliable on-premises server foundation.</p>"""
    },
    {
        "id": "linux-server-fundamentals",
        "title": "Linux Server Fundamentals",
        "category": "Servers",
        "category_dir": "servers",
        "category_page": "servers.html",
        "level": "Intermediate",
        "readTime": "8 min read",
        "description": "Learn how to deploy, configure, and maintain headless enterprise Linux servers with SSH, systemd services, firewalls, and logging.",
        "keywords": "linux server, headless, ssh, systemd, ufw, firewalld, journalctl, rhel, ubuntu server, sysadmin",
        "html": """<p>An enterprise <strong>Linux Server</strong> is an operating system installation optimized for background service hosting, high network throughput, and continuous uptime without a graphical desktop interface. Deploying and maintaining headless Linux servers requires disciplined configuration of remote access, firewall policies, service daemons, and system telemetry.</p>

<h2>The Headless Server Architecture</h2>
<p>Production Linux servers operate in <strong>headless mode</strong> (Runlevel 3 / <code>multi-user.target</code>). By eliminating GUI display managers (like X11 or Wayland) and desktop environments (like GNOME):</p>
<ul>
    <li><strong>System Resources are Maximized:</strong> A base headless Linux server uses as little as 250MB to 500MB of RAM, reserving almost 100% of physical memory and CPU cycles for application workloads.</li>
    <li><strong>Attack Surface is Minimized:</strong> Eliminating graphical rendering libraries, browsers, and desktop packages removes thousands of potential software vulnerabilities.</li>
    <li><strong>Automation is Enforced:</strong> Configuration must be executed through command-line scripts, configuration files, and Infrastructure-as-Code tooling (Ansible, Terraform).</li>
</ul>

<h2>Hardening Secure Shell (SSH) Access</h2>
<p>Remote administration is conducted almost exclusively via the <strong>Secure Shell (SSH)</strong> protocol on TCP Port 22. Standard hardening best practices should be applied immediately upon provisioning in <code>/etc/ssh/sshd_config</code>:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Configuration Directive</th>
                <th>Recommended Setting</th>
                <th>Security Rationale</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>PermitRootLogin</code></td>
                <td><code>no</code> or <code>prohibit-password</code></td>
                <td>Prevents brute-force dictionary attacks against the primary root account</td>
            </tr>
            <tr>
                <td><code>PasswordAuthentication</code></td>
                <td><code>no</code></td>
                <td>Enforces asymmetric SSH public/private key authentication, neutralizing password theft</td>
            </tr>
            <tr>
                <td><code>MaxAuthTries</code></td>
                <td><code>3</code></td>
                <td>Disconnects sessions after repeated failed authentication attempts</td>
            </tr>
            <tr>
                <td><code>X11Forwarding</code></td>
                <td><code>no</code></td>
                <td>Disables graphical display forwarding across SSH tunnels</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="tutorial-command">
# Test SSH configuration file syntax before restarting the daemon
sshd -t

# Apply configuration changes safely
systemctl reload sshd
</div>

<h2>Host Firewall Implementation: UFW and Firewalld</h2>
<p>Every Linux server must enforce a host-based firewall to drop unauthorized ingress traffic:</p>

<div class="tutorial-command">
# --- On Ubuntu / Debian Servers (UFW) ---
# Default policy: drop all incoming, allow all outgoing
ufw default deny incoming
ufw default allow outgoing

# Explicitly permit SSH and HTTPS traffic
ufw allow 22/tcp
ufw allow 443/tcp
ufw enable

# --- On RHEL / Rocky Linux Servers (firewalld) ---
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
</div>

<h2>Service Lifecycle Management with systemd</h2>
<p>Server applications (such as databases, web servers, and monitoring agents) run as systemd background service units:</p>

<div class="tutorial-command">
# Inspect whether a service is active and view recent log lines
systemctl status postgresql

# Ensure the service starts automatically on system boot
systemctl enable postgresql

# Reload service configuration without terminating active client sessions
systemctl reload nginx
</div>

<h2>Centralized Telemetry & Log Auditing</h2>
<p>The systemd journal captures stdout, stderr, kernel messages, and syslog events centrally:</p>

<div class="tutorial-command">
# View real-time log output for a specific service
journalctl -u sshd -f

# View system boot logs from the previous failed boot session
journalctl -b -1 -p err
</div>

<p><em>Tip: Always configure out-of-band management (such as cloud serial consoles, Proxmox VNC consoles, or server IPMI) before making network or firewall changes. If an administrative error locks you out of SSH, console access provides an emergency rescue path.</em></p>

<h2>Summary</h2>
<p>Operating enterprise Linux servers requires a strict defense-in-depth posture: running headless installations to conserve resources, enforcing SSH key authentication, locking down network ports with host firewalls, and monitoring service health with systemd and journalctl.</p>"""
    },

    # =========================================================================
    # CYBERSECURITY BATCH (3 Tutorials)
    # =========================================================================
    {
        "id": "cybersecurity-fundamentals",
        "title": "Cybersecurity Fundamentals",
        "category": "Cybersecurity",
        "category_dir": "cybersecurity",
        "category_page": "cybersecurity.html",
        "level": "Beginner",
        "readTime": "6 min read",
        "description": "Understand fundamental enterprise cybersecurity principles: the CIA Triad, Defense-in-Depth, threat actors, and common attack vectors.",
        "keywords": "cybersecurity, cia triad, confidentiality, integrity, availability, defense in depth, threats, attack vectors, hardening",
        "html": """<p><strong>Cybersecurity</strong> is the practice of protecting systems, networks, programs, and data from digital attacks, unauthorized access, corruption, or destruction. In enterprise IT, security is not an isolated product or feature; it is an overarching operational discipline integrated into every architecture decision.</p>

<h2>The CIA Triad: Core Security Objectives</h2>
<p>The foundational framework of information security is the <strong>CIA Triad</strong>. Every policy, firewall rule, encryption algorithm, and backup schedule exists to support one or more of these three pillars:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Pillar</th>
                <th>Definition</th>
                <th>Enterprise Defensive Implementation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Confidentiality</strong></td>
                <td>Ensuring data is accessible only to authorized personnel and protected from eavesdropping or leaks.</td>
                <td>TLS 1.3 encryption in transit, AES-256 encryption at rest (BitLocker), Role-Based Access Control (RBAC), Multi-Factor Authentication.</td>
            </tr>
            <tr>
                <td><strong>Integrity</strong></td>
                <td>Guaranteeing that data and system configurations remain accurate, authentic, and untampered with.</td>
                <td>Cryptographic hashing (SHA-256), digital signatures, file integrity monitoring (FIM), database transaction logging.</td>
            </tr>
            <tr>
                <td><strong>Availability</strong></td>
                <td>Ensuring authorized users have timely, uninterrupted access to critical systems and information assets.</td>
                <td>Redundant server hardware, load balancers, DDoS mitigation, RAID storage arrays, verified 3-2-1 backup copies.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Defense-in-Depth (Layered Security)</h2>
<p>No single security control is 100% impenetrable. Enterprise security architectures implement <strong>Defense-in-Depth</strong>—stacking multiple defensive layers so that if an adversary bypasses one barrier, subsequent controls contain and neutralize the threat:</p>
<ul>
    <li><strong>Perimeter Layer:</strong> Next-Generation Firewalls (NGFW), Cloudflare/AWS DDoS protection, and external DNS filtering.</li>
    <li><strong>Network Layer:</strong> VLAN segmentation, Internal firewalls, Network Access Control (802.1X), and encrypted site-to-site VPN tunnels.</li>
    <li><strong>Endpoint Layer:</strong> Endpoint Detection and Response (EDR) agents, host firewalls, full disk encryption, and automated patch management.</li>
    <li><strong>Application Layer:</strong> Web Application Firewalls (WAF), secure software development lifecycles (DevSecOps), and API authentication tokens.</li>
    <li><strong>Data Layer:</strong> Principle of Least Privilege, database encryption, Data Loss Prevention (DLP) agents, and immutable off-site backups.</li>
</ul>

<h2>Understanding Threat Actors</h2>
<p>Security teams model defensive strategies based on adversary profiles and capabilities:</p>
<ul>
    <li><strong>Cybercriminal Syndicates:</strong> Motivated by financial gain. Primary weapons include Ransomware-as-a-Service (RaaS), phishing campaigns, and wire fraud schemes.</li>
    <li><strong>Nation-State Advanced Persistent Threats (APTs):</strong> Highly funded, patient adversaries targeting intellectual property, national infrastructure, and strategic intelligence.</li>
    <li><strong>Insider Threats:</strong> Disgruntled employees, contractors, or careless staff who leak credentials or accidentally delete critical production data.</li>
    <li><strong>Opportunistic Attackers:</strong> Automated scanning bots scouring public IP ranges for exposed RDP ports, default passwords, and unpatched CVE vulnerabilities.</li>
</ul>

<h2>The Security Controls Taxonomy</h2>
<p>Security safeguards fall into three operational categories:</p>
<ul>
    <li><strong>Preventive Controls:</strong> Stop an attack before it succeeds (e.g., MFA, firewall rules, user access revocation).</li>
    <li><strong>Detective Controls:</strong> Identify an ongoing or attempted security event (e.g., SIEM alerts, antivirus scans, honeypots).</li>
    <li><strong>Corrective Controls:</strong> Remediate damage and restore operations after an incident (e.g., restoring from clean backups, rebuilding infected hosts, revoking compromised API keys).</li>
</ul>

<p><em>Note: The human element remains a primary attack surface. Over 80% of enterprise security breaches involve stolen credentials, social engineering, or phishing emails. Technical controls must always be coupled with continuous employee security awareness training.</em></p>

<h2>Summary</h2>
<p>Cybersecurity balances business productivity against operational risk. By grounding administrative practices in the CIA Triad, implementing layered Defense-in-Depth controls, and modeling realistic threat actor capabilities, IT professionals protect critical organizational assets against modern cyber threats.</p>"""
    },
    {
        "id": "authentication-vs-authorization",
        "title": "Authentication vs Authorization",
        "category": "Cybersecurity",
        "category_dir": "cybersecurity",
        "category_page": "cybersecurity.html",
        "level": "Beginner",
        "readTime": "6 min read",
        "description": "Differentiate between proving identity (Authentication) and granting permissions (Authorization) in enterprise identity systems.",
        "keywords": "authentication, authorization, authn, authz, identity, rbac, iam, active directory, ldap, kerberos",
        "html": """<p>While often grouped together under Identity and Access Management (IAM), <strong>Authentication (AuthN)</strong> and <strong>Authorization (AuthZ)</strong> represent two completely distinct security operations. Conflating the two is a primary cause of broken access control vulnerabilities in enterprise environments.</p>

<h2>Core Definitions</h2>
<ul>
    <li><strong>Authentication (AuthN) — "Who are you?":</strong> The process of verifying the claimed identity of a user, service account, or device. Authentication proves that you are who you claim to be.</li>
    <li><strong>Authorization (AuthZ) — "What are you allowed to do?":</strong> The process of determining the specific access rights, permissions, and privileges granted to an already authenticated identity.</li>
</ul>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Comparison Factor</th>
                <th>Authentication (AuthN)</th>
                <th>Authorization (AuthZ)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Primary Question</strong></td>
                <td>"Who are you? Prove your identity."</td>
                <td>"What resources are you permitted to touch?"</td>
            </tr>
            <tr>
                <td><strong>Execution Order</strong></td>
                <td>Must occur <strong>first</strong></td>
                <td>Occurs <strong>second</strong> (after identity is proven)</td>
            </tr>
            <tr>
                <td><strong>Data Exchanged</strong></td>
                <td>Usernames, passwords, MFA tokens, biometrics</td>
                <td>Access control lists (ACLs), role assignments, scopes</td>
            </tr>
            <tr>
                <td><strong>Enterprise Protocols</strong></td>
                <td>Kerberos, NTLM, OpenID Connect (OIDC), SAML 2.0</td>
                <td>OAuth 2.0 (scopes), LDAP groups, NTFS ACLs, AWS IAM policies</td>
            </tr>
            <tr>
                <td><strong>Failure Result</strong></td>
                <td>401 Unauthorized (Identity verification failed)</td>
                <td>403 Forbidden (Identity verified, but access denied)</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>The Enterprise AAA Framework</h2>
<p>Enterprise identity management expands AuthN and AuthZ into the industry-standard <strong>AAA Framework</strong>:</p>
<ol>
    <li><strong>Authentication:</strong> Verifying credentials via Active Directory Kerberos, cloud identity providers, or RADIUS.</li>
    <li><strong>Authorization:</strong> Checking group memberships (e.g., verifying if the user belongs to the <code>Finance-Read-Only</code> security group).</li>
    <li><strong>Accounting (Auditing):</strong> Tracking what the user actually did, logging timestamps, source IP addresses, file access events, and privilege escalation attempts for compliance.</li>
</ol>

<h2>The Three Classic Authentication Factors</h2>
<p>Authentication mechanisms rely on one or more verifiable factors:</p>
<ul>
    <li><strong>Something You Know:</strong> Passwords, PINs, passphrases (vulnerable to phishing and credential stuffing).</li>
    <li><strong>Something You Have:</strong> Hardware security keys (YubiKey), smartphone authenticator apps (TOTP), smart cards.</li>
    <li><strong>Something You Are:</strong> Biometrics such as fingerprint scans, facial recognition (Windows Hello), or retina scans.</li>
</ul>

<h2>Common Authorization Models</h2>
<p>Once identity is established, systems evaluate authorization policies using structured models:</p>
<ul>
    <li><strong>Role-Based Access Control (RBAC):</strong> The enterprise standard. Permissions are assigned to business roles (e.g., "Network Engineer" or "Help Desk"), and users are added to groups reflecting those roles.</li>
    <li><strong>Attribute-Based Access Control (ABAC):</strong> Granular policies evaluated at runtime based on user attributes, resource classification, time of day, and device security compliance.</li>
    <li><strong>Discretionary Access Control (DAC):</strong> The file owner dictates access rights (e.g., standard Unix file permissions managed by individual users).</li>
</ul>

<h2>A Real-World Enterprise Scenario</h2>
<p>Consider an engineer logging onto their corporate laptop to access a payroll spreadsheet on an internal file share:</p>
<ol>
    <li><strong>Authentication:</strong> The engineer enters their username, password, and approves a push notification on their phone. Microsoft Entra ID verifies the credentials and issues an authentication ticket. <em>(AuthN Complete)</em></li>
    <li><strong>Authorization:</strong> The engineer attempts to open <code>\\\\fileserver\\payroll\\salaries.xlsx</code>. The file server inspects the engineer's security token and checks the NTFS access control list on the file. Because the engineer is in the "IT Support" group and not the "HR Leadership" group, access is blocked with a <em>Permission Denied</em> prompt. <em>(AuthZ Enforced)</em></li>
</ol>

<p><em>Important: Broken Access Control represents the #1 web application security vulnerability according to OWASP. An application that successfully verifies identity but fails to rigorously evaluate authorization boundaries on every API request allows authenticated users to view or tamper with unauthorized customer records.</em></p>

<h2>Summary</h2>
<p>Authentication verifies identity; authorization enforces permissions. Designing secure enterprise systems requires treating both as independent checkpoints, ensuring that robust multi-factor authentication is paired with strict role-based authorization adhering to the Principle of Least Privilege.</p>"""
    },
    {
        "id": "multi-factor-authentication-explained",
        "title": "Multi-Factor Authentication (MFA) Explained",
        "category": "Cybersecurity",
        "category_dir": "cybersecurity",
        "category_page": "cybersecurity.html",
        "level": "Intermediate",
        "readTime": "7 min read",
        "description": "Explore how Multi-Factor Authentication works, factor types, OTP vs push notifications, FIDO2/WebAuthn, and MFA bypass prevention.",
        "keywords": "mfa, 2fa, multi factor authentication, totp, fido2, webauthn, authenticator, push fatigue, security",
        "html": """<p><strong>Multi-Factor Authentication (MFA)</strong> is a security mechanism that requires a user to provide two or more independent authentication factors before being granted access to an application, account, or network resource. Enforcing MFA is single-handedly the most effective control for neutralizing credential theft and automated account takeover attacks.</p>

<h2>Why Passwords Alone Are Obsolete</h2>
<p>Traditional single-factor authentication (passwords) fails against modern adversary capabilities:</p>
<ul>
    <li><strong>Credential Stuffing:</strong> Automated bots test billions of leaked username/password pairs stolen from third-party breaches across corporate portals.</li>
    <li><strong>Phishing Campaigns:</strong> Sophisticated adversary-in-the-middle (AiTM) reverse proxies trick users into entering passwords on deceptive spoofed login pages.</li>
    <li><strong>Keylogging & Infostealers:</strong> Endpoint malware intercepts keystrokes and extracts browser-cached credentials silently.</li>
</ul>
<p>By requiring a second factor from a physically separate channel, stolen passwords become useless to an attacker without concurrent physical access to the secondary authenticator.</p>

<h2>MFA Methods Ranked by Security Strength</h2>
<p>Not all MFA implementations offer equal protection. Security architectures must understand the resistance of each method to phishing and interception:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>MFA Method</th>
                <th>Underlying Technology</th>
                <th>Phishing Resistance</th>
                <th>Enterprise Evaluation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>SMS / Voice OTP</strong></td>
                <td>Cellular SMS delivery of 6-digit numeric codes</td>
                <td><strong>Vulnerable</strong> (Low)</td>
                <td>Vulnerable to SIM swapping attacks, SS7 cellular interception, and plain text relaying. Minimum acceptable fallback only.</td>
            </tr>
            <tr>
                <td><strong>Time-Based OTP (TOTP)</strong></td>
                <td>RFC 6238 shared secret HMAC algorithm (Google / Microsoft Authenticator)</td>
                <td><strong>Moderate</strong></td>
                <td>Generates dynamic 6-digit codes refreshing every 30 seconds. Stronger than SMS, but still vulnerable to real-time AiTM phishing proxies.</td>
            </tr>
            <tr>
                <td><strong>Push Notification with Number Matching</strong></td>
                <td>Encrypted mobile push notification requiring matching a 2-digit number shown on screen</td>
                <td><strong>High</strong></td>
                <td>Neutralizes accidental approvals and MFA fatigue attacks by requiring the user to physically read and enter matching numbers.</td>
            </tr>
            <tr>
                <td><strong>FIDO2 / WebAuthn Hardware Keys</strong></td>
                <td>Public-key cryptography tied to origin domain (YubiKey, Windows Hello)</td>
                <td><strong>Phishing-Resistant</strong> (Maximum)</td>
                <td>Cryptographically signs challenge using private key stored inside tamper-resistant hardware. Immune to phishing because the browser verifies domain identity.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>How TOTP Algorithms Work (RFC 6238)</h2>
<p>Time-based One-Time Password (TOTP) applications do not require an active internet connection on your phone to generate codes. Here is the mathematical process:</p>
<ol>
    <li>During setup, the server generates a random cryptographic secret key (encoded in a QR code) and shares it with the authenticator app.</li>
    <li>Both the server and the app take the current Unix epoch time divided into 30-second windows (Time Step: <code>T = floor(Epoch / 30)</code>).</li>
    <li>Both calculate an HMAC-SHA1 hash combining the secret key and the time step.</li>
    <li>The resulting hash is truncated to generate an identical 6-digit code on both devices simultaneously.</li>
</ol>

<h2>Combating Modern MFA Attacks</h2>
<p>As organizations mandate MFA, attackers have evolved techniques to bypass secondary factors:</p>
<ul>
    <li><strong>MFA Prompt Bombing (Push Fatigue):</strong> Attackers send dozens of login push notifications at 2:00 AM until an exasperated employee taps "Approve" simply to silence their phone. <em>Defense: Enforce Number Matching and disable simple binary approve/deny prompts.</em></li>
    <li><strong>Adversary-in-the-Middle (AiTM) Phishing:</strong> Reverse-proxy phishing kits (e.g., Evilginx) intercept both the user's password and the valid TOTP code in real time, capturing the final authenticated session cookie. <em>Defense: Mandate FIDO2/WebAuthn phishing-resistant credentials.</em></li>
    <li><strong>Session Cookie Hijacking:</strong> Stealing valid session tokens directly from local browser storage via infostealer malware. <em>Defense: Enforce Conditional Access policies checking device compliance and continuous token binding.</em></li>
</ul>

<p><em>Warning: Avoid using SMS as your primary MFA method for administrative or financial accounts. Mobile carriers remain vulnerable to SIM-swap social engineering, allowing attackers to redirect text messages to adversary-controlled phones within minutes.</em></p>

<h2>Summary</h2>
<p>Multi-Factor Authentication is an essential defensive control that renders stolen passwords ineffective. By transitioning away from insecure SMS verification toward mobile push notifications with number matching and hardware-backed FIDO2 security keys, organizations build resilient, phishing-resistant identity architectures.</p>"""
    },

    # =========================================================================
    # CLOUD & AI BATCH (3 Tutorials)
    # =========================================================================
    {
        "id": "cloud-computing-fundamentals",
        "title": "Cloud Computing Fundamentals",
        "category": "Cloud & AI",
        "category_dir": "cloud",
        "category_page": "cloud.html",
        "level": "Beginner",
        "readTime": "6 min read",
        "description": "Learn the core definition, essential characteristics, and business advantages of modern cloud computing architectures.",
        "keywords": "cloud, cloud computing, on-demand, elasticity, pooling, shared responsibility, aws, azure, gcp, opex",
        "html": """<p><strong>Cloud Computing</strong> is the on-demand delivery of IT resources—including compute power, storage databases, and networking—over the Internet with pay-as-you-go pricing. Rather than purchasing, racking, and maintaining physical datacenters and on-premises servers, organizations rent technological infrastructure from cloud hyperscalers like AWS, Microsoft Azure, and Google Cloud Platform.</p>

<h2>The 5 Essential Characteristics (NIST SP 800-145)</h2>
<p>The National Institute of Standards and Technology (NIST) defines cloud computing through five mandatory criteria:</p>
<ul>
    <li><strong>On-Demand Self-Service:</strong> Consumers can provision computing capabilities (such as server time or cloud storage) automatically through web portals or APIs without human intervention from the service provider.</li>
    <li><strong>Broad Network Access:</strong> Capabilities are accessible over standard network protocols from diverse client platforms (laptops, mobile devices, branch offices).</li>
    <li><strong>Resource Pooling:</strong> The provider's physical computing resources are pooled to serve multiple customers (multi-tenancy), dynamically allocating virtual resources according to consumer demand.</li>
    <li><strong>Rapid Elasticity:</strong> Capabilities can be elastically provisioned and released—often automatically—to scale outward during peak traffic and scale inward during lulls to control costs.</li>
    <li><strong>Measured Service:</strong> Resource usage is monitored, controlled, and billed transparently based on actual consumption (e.g., gigabyte-hours of storage, CPU-hours, egress bandwidth).</li>
</ul>

<h2>Financial Economics: CapEx vs OpEx</h2>
<p>Cloud adoption fundamentally alters corporate IT financial modeling:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Financial Model</th>
                <th>Capital Expenditure (CapEx)</th>
                <th>Operational Expenditure (OpEx)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Billing Nature</strong></td>
                <td>Substantial upfront capital investment</td>
                <td>Recurring ongoing operational expenses</td>
            </tr>
            <tr>
                <td><strong>Asset Ownership</strong></td>
                <td>Company purchases physical servers, switches, and cooling units</td>
                <td>Company rents compute capacity as an operating utility</td>
            </tr>
            <tr>
                <td><strong>Depreciation</strong></td>
                <td>Assets depreciate on accounting balance sheets over 3–5 years</td>
                <td>Deducted as operational business expense in the current tax year</td>
            </tr>
            <tr>
                <td><strong>Capacity Risk</strong></td>
                <td>Risk of over-provisioning (idle hardware) or under-provisioning (outages)</td>
                <td>Scale capacity dynamically; pay only for active resources consumed</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Cloud Deployment Models</h2>
<p>Organizations deploy workloads across different architectural boundaries depending on regulatory and security requirements:</p>
<ul>
    <li><strong>Public Cloud:</strong> Services are owned and operated by a third-party cloud provider (AWS, Azure, GCP) and delivered over the public Internet. Maximum scalability and zero physical hardware maintenance.</li>
    <li><strong>Private Cloud:</strong> Cloud infrastructure provisioned for exclusive use by a single organization, hosted either in an on-premises enterprise datacenter or managed by a dedicated hosting provider.</li>
    <li><strong>Hybrid Cloud:</strong> A unified computing environment connecting private on-premises infrastructure with public cloud resources over encrypted ExpressRoute/DirectConnect or VPN tunnels, allowing workloads and data to shift seamlessly.</li>
    <li><strong>Multi-Cloud:</strong> The intentional utilization of services across multiple distinct public cloud vendors (e.g., running workloads in AWS while leveraging Microsoft 365 and Entra ID in Azure) to avoid vendor lock-in.</li>
</ul>

<h2>The Shared Responsibility Model</h2>
<p>Security in the cloud is a shared partnership between the cloud service provider (CSP) and the customer:</p>
<ul>
    <li><strong>Security OF the Cloud (Provider Responsibility):</strong> Physical datacenter security, power redundancy, hardware maintenance, host virtualization hypervisors, and global network backbone infrastructure.</li>
    <li><strong>Security IN the Cloud (Customer Responsibility):</strong> Guest operating system patching, customer data encryption, firewall security group configurations, IAM user access policies, and application code.</li>
</ul>

<p><em>Note: The boundary of the Shared Responsibility Model shifts depending on the service tier. In IaaS, you manage the OS, runtime, and data. In SaaS, the provider manages the entire infrastructure, leaving only data classification and user access under your control.</em></p>

<h2>Summary</h2>
<p>Cloud computing replaces rigid on-premises hardware procurement with elastic, on-demand infrastructure billed on an OpEx utility model. By internalizing the five essential NIST characteristics and the Shared Responsibility Model, IT engineers architect scalable, cost-efficient cloud solutions.</p>"""
    },
    {
        "id": "iaas-vs-paas-vs-saas",
        "title": "IaaS vs PaaS vs SaaS Explained",
        "category": "Cloud & AI",
        "category_dir": "cloud",
        "category_page": "cloud.html",
        "level": "Beginner",
        "readTime": "7 min read",
        "description": "Compare Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS) with real-world examples.",
        "keywords": "iaas, paas, saas, cloud service models, ec2, s3, app service, microsoft 365, salesforce, cloud architecture",
        "html": """<p>Cloud computing services are organized into three primary delivery tiers known as the <strong>Cloud Service Models</strong>: <strong>Infrastructure as a Service (IaaS)</strong>, <strong>Platform as a Service (PaaS)</strong>, and <strong>Software as a Service (SaaS)</strong>. Understanding these models defines where your administrative responsibility ends and where the cloud provider's automation begins.</p>

<h2>The Cloud Service Model Pyramid</h2>
<p>Each tier provides a different level of control, flexibility, and operational abstraction:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Attribute</th>
                <th>IaaS (Infrastructure)</th>
                <th>PaaS (Platform)</th>
                <th>SaaS (Software)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Primary Focus</strong></td>
                <td>Virtual hardware and networking primitives</td>
                <td>Application code deployment and data</td>
                <td>Consuming end-user business software</td>
            </tr>
            <tr>
                <td><strong>Customer Manages</strong></td>
                <td>OS, middleware, runtime, apps, data, networking rules</td>
                <td>Application source code, configurations, database data</td>
                <td>User access, data classification, tenant settings</td>
            </tr>
            <tr>
                <td><strong>Provider Manages</strong></td>
                <td>Physical servers, hypervisors, physical network, cooling</td>
                <td>OS patching, runtime libraries, scaling, physical servers</td>
                <td>The entire application stack, updates, security, and hardware</td>
            </tr>
            <tr>
                <td><strong>Flexibility & Control</strong></td>
                <td><strong>Maximum</strong> (Full root/administrator OS access)</td>
                <td><strong>Moderate</strong> (Constrained to supported runtimes)</td>
                <td><strong>Low</strong> (Configurable only within software options)</td>
            </tr>
            <tr>
                <td><strong>Enterprise Examples</strong></td>
                <td>AWS EC2, Azure Virtual Machines, Google Compute Engine</td>
                <td>AWS Elastic Beanstalk, Azure App Service, Google App Engine</td>
                <td>Microsoft 365, Google Workspace, Salesforce, Zoom, Slack</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>1. Infrastructure as a Service (IaaS)</h2>
<p>IaaS provides on-demand access to fundamental computing resources: virtual machines, raw block storage, and software-defined networks. It is the cloud equivalent of leasing a blank virtual server in a remote datacenter.</p>
<ul>
    <li><strong>Administrative Experience:</strong> You log in via SSH (Linux) or RDP (Windows). You are responsible for installing operating system security patches, antivirus agents, and software dependencies.</li>
    <li><strong>Ideal Use Cases:</strong> Migrating legacy enterprise applications ("lift-and-shift"), running custom kernels, or deploying software requiring specific operating system versions.</li>
</ul>

<h2>2. Platform as a Service (PaaS)</h2>
<p>PaaS removes the need for organizations to manage underlying virtual machines and operating systems. The cloud provider delivers a managed development and execution runtime (e.g., Node.js, Python, .NET, Java, or managed SQL databases):</p>
<ul>
    <li><strong>Administrative Experience:</strong> You upload your compiled application code or container image via Git or CI/CD pipelines. The cloud provider automatically provisions compute capacity, handles OS security updates, and scales container instances in response to traffic spikes.</li>
    <li><strong>Ideal Use Cases:</strong> Web applications, microservices, REST APIs, and modern cloud-native development where developers want to focus on code rather than server administration.</li>
</ul>

<h2>3. Software as a Service (SaaS)</h2>
<p>SaaS delivers complete, fully managed web applications directly to end users over a browser or mobile app. The underlying infrastructure, runtime, operating systems, and application code are entirely maintained by the vendor:</p>
<ul>
    <li><strong>Administrative Experience:</strong> Administrators manage user provisioning, single sign-on (SSO) integration, multi-factor authentication, and data retention policies through an administrative dashboard.</li>
    <li><strong>Ideal Use Cases:</strong> Corporate email (Exchange Online/Gmail), collaboration (Teams/Slack), CRM (Salesforce), and enterprise productivity suites.</li>
</ul>

<h2>Stack Responsibility Breakdown</h2>
<p>Compare the technological stack management across all models:</p>
<ul>
    <li><strong>Applications:</strong> Customer (IaaS, PaaS) | Provider (SaaS)</li>
    <li><strong>Data:</strong> Customer (IaaS, PaaS, SaaS)</li>
    <li><strong>Runtime & Middleware:</strong> Customer (IaaS) | Provider (PaaS, SaaS)</li>
    <li><strong>Operating System:</strong> Customer (IaaS) | Provider (PaaS, SaaS)</li>
    <li><strong>Virtualization & Hardware:</strong> Provider (IaaS, PaaS, SaaS)</li>
</ul>

<p><em>Tip: When evaluating cloud migrations, remember that customer data remains YOUR responsibility across all three models. In SaaS environments like Microsoft 365, vendors guarantee service availability, but you are still responsible for protecting corporate data against accidental deletion, ransomware, and insider threats using third-party backup solutions.</em></p>

<h2>Summary</h2>
<p>Choosing between IaaS, PaaS, and SaaS balances operational control against administrative management overhead. IaaS offers total infrastructure control at the cost of manual patching; PaaS streamlines application deployment by abstracting servers; SaaS delivers turnkey business productivity with zero infrastructure maintenance.</p>"""
    },
    {
        "id": "aws-vs-azure-cloud-fundamentals",
        "title": "AWS vs Azure Cloud Fundamentals",
        "category": "Cloud & AI",
        "category_dir": "cloud",
        "category_page": "cloud.html",
        "level": "Intermediate",
        "readTime": "8 min read",
        "description": "A comprehensive architectural comparison between Amazon Web Services (AWS) and Microsoft Azure for enterprise IT professionals.",
        "keywords": "aws, azure, cloud comparison, ec2, azure vm, s3, blob, vpc, vnet, iam, entra id, cloud architecture",
        "html": """<p><strong>Amazon Web Services (AWS)</strong> and <strong>Microsoft Azure</strong> are the two dominant public cloud hyperscalers powering global enterprise infrastructure. While both platforms offer comparable compute, storage, networking, and identity capabilities, understanding their naming conventions, architecture patterns, and enterprise strengths is essential for modern IT professionals.</p>

<h2>Market Positioning and Enterprise Focus</h2>
<ul>
    <li><strong>Amazon Web Services (AWS):</strong> The pioneer of modern public cloud infrastructure, launched in 2006. Known for high developer adoption, massive service breadth, modular Unix-friendly primitives, and extensive open-source community support.</li>
    <li><strong>Microsoft Azure:</strong> Launched in 2010. Deeply entrenched in corporate enterprise environments due to seamless native integration with Active Directory (Microsoft Entra ID), Windows Server licensing, Microsoft 365, and hybrid on-premises tooling (Azure Arc).</li>
</ul>

<h2>Global Infrastructure Architecture</h2>
<p>Both platforms deploy infrastructure across global geographic footprints using identical architectural concepts:</p>
<ul>
    <li><strong>Regions:</strong> Distinct physical geographic locations around the world (e.g., <code>us-east-1</code> in Virginia or <code>East US</code>) containing multiple physically isolated datacenters.</li>
    <li><strong>Availability Zones (AZs):</strong> Isolated datacenters within a Region with independent power, cooling, and low-latency fiber connectivity. Architecting across multiple AZs guarantees high availability against physical datacenter outages.</li>
    <li><strong>Edge Locations:</strong> Global Points of Presence (PoP) delivering low-latency cached content via Content Delivery Networks (AWS CloudFront / Azure Front Door).</li>
</ul>

<h2>Direct Core Service Mapping</h2>
<p>Engineers moving between AWS and Azure can cross-reference equivalent services across foundational IT disciplines:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Discipline</th>
                <th>AWS Service</th>
                <th>Microsoft Azure Service</th>
                <th>Functional Overview</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Virtual Compute</strong></td>
                <td>Amazon EC2 (Elastic Compute Cloud)</td>
                <td>Azure Virtual Machines (VMs)</td>
                <td>On-demand virtual server instances (Windows / Linux)</td>
            </tr>
            <tr>
                <td><strong>Object Storage</strong></td>
                <td>Amazon S3 (Simple Storage Service)</td>
                <td>Azure Blob Storage</td>
                <td>Highly durable, scalable unstructured object storage accessed via HTTP APIs</td>
            </tr>
            <tr>
                <td><strong>Virtual Networking</strong></td>
                <td>Amazon VPC (Virtual Private Cloud)</td>
                <td>Azure VNet (Virtual Network)</td>
                <td>Isolated private network topology with subnets, route tables, and gateways</td>
            </tr>
            <tr>
                <td><strong>Host Firewalling</strong></td>
                <td>AWS Security Groups</td>
                <td>Azure Network Security Groups (NSGs)</td>
                <td>Stateful virtual firewalls filtering inbound and outbound port traffic</td>
            </tr>
            <tr>
                <td><strong>Identity & Access</strong></td>
                <td>AWS IAM (Identity and Access Management)</td>
                <td>Microsoft Entra ID (formerly Azure AD)</td>
                <td>User identities, service principals, RBAC roles, and access policies</td>
            </tr>
            <tr>
                <td><strong>Relational Database</strong></td>
                <td>Amazon RDS</td>
                <td>Azure SQL Database / Azure Database for PostgreSQL</td>
                <td>Fully managed SQL database engines with automated backups and failover</td>
            </tr>
            <tr>
                <td><strong>Serverless Compute</strong></td>
                <td>AWS Lambda</td>
                <td>Azure Functions</td>
                <td>Event-driven serverless code execution billed per millisecond</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Key Architectural Differences</h2>
<p>Despite surface similarities, structural differences impact administrative operations:</p>
<ul>
    <li><strong>Identity Architecture:</strong> AWS IAM is tenant-local to individual AWS accounts, relying heavily on IAM Roles and cross-account assumption. Azure utilizes a centralized tenant-wide <strong>Microsoft Entra ID</strong> directory that can manage multiple Azure Subscriptions and integrate natively with on-premises Active Directory via Entra Connect.</li>
    <li><strong>Account and Governance Hierarchy:</strong> AWS uses AWS Organizations and Organizational Units (OUs) with Service Control Policies (SCPs). Azure organizes resources hierarchically into Management Groups -> Subscriptions -> Resource Groups -> Resources, applying Azure Policy at any level.</li>
    <li><strong>Network Address Space:</strong> In AWS VPC, subnets are strictly bound to a single Availability Zone. In Azure VNet, subnets can span across the entire region, allowing VMs in different AZs to share the same subnet IP range.</li>
</ul>

<p><em>Note: For organizations heavily invested in Microsoft enterprise licensing (Windows Server, SQL Server, Microsoft 365), Azure Hybrid Benefit offers substantial cost reductions by allowing on-premises software licenses with Software Assurance to be applied directly to Azure virtual machines.</em></p>

<h2>Summary</h2>
<p>AWS and Azure provide equivalent enterprise cloud capabilities using different terminology and identity models. Mastering the direct service mappings between EC2 and Azure VMs, S3 and Blob Storage, and VPC and VNet equips systems engineers to design and troubleshoot multi-cloud enterprise architectures effectively.</p>"""
    }
]

def generate_phase6_5_content():
    print("=" * 68)
    print("MJ Tech Hub - Phase 6.5 Content Expansion Generator")
    print("=" * 68)

    # 1. Load existing tutorials.json
    with open(TUTS_JSON_PATH, "r", encoding="utf-8") as f:
        tutorials_data = json.load(f)

    existing_ids = {t["id"] for t in tutorials_data}
    print(f"Existing tutorials in tutorials.json: {len(tutorials_data)}")

    # 2. Generate HTML files
    created_files = []
    new_metadata_records = []

    for tut in NEW_TUTORIALS:
        tid = tut["id"]
        cat_dir = tut["category_dir"]
        cat_page = tut["category_page"]

        target_dir = ROOT_DIR / "tutorials" / cat_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / f"{tid}.html"
        html_content = build_tutorial_html(tut, cat_dir, cat_page)

        target_file.write_text(html_content, encoding="utf-8")
        created_files.append(str(target_file.relative_to(ROOT_DIR)))

        if tid not in existing_ids:
            new_record = {
                "id": tid,
                "title": tut["title"],
                "description": tut["description"],
                "category": tut["category"],
                "level": tut["level"],
                "readTime": tut["readTime"],
                "keywords": tut["keywords"],
                "url": f"tutorials/{cat_dir}/{tid}.html",
                "publishedAt": PUBLISH_DATE,
                "updatedAt": PUBLISH_DATE
            }
            new_metadata_records.append(new_record)
            existing_ids.add(tid)

    # 3. Append to tutorials.json in canonical category order
    tutorials_data.extend(new_metadata_records)

    with open(TUTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(tutorials_data, f, indent=4)

    print(f"\nSuccessfully generated {len(created_files)} tutorial HTML files.")
    print(f"Added {len(new_metadata_records)} new tutorial records to tutorials.json.")
    print(f"Total tutorials in tutorials.json: {len(tutorials_data)}")

    return True

if __name__ == "__main__":
    generate_phase6_5_content()
