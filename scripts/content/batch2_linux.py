"""
MJ Tech Hub - Batch 2 Linux Tutorials Content
Tutorials:
1. linux-standard-file-permissions-chmod-chown
2. linux-systemd-service-units-creation-and-control
3. linux-memory-management-buffers-caches-oom-killer
"""

LINUX_TUTORIALS = [
    {
        "id": "linux-standard-file-permissions-chmod-chown",
        "title": "Standard Linux File Permissions: Read, Write, Execute (chmod & chown)",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Beginner",
        "readTime": "8 min read",
        "description": "Understand the POSIX file permission model (rwx), symbolic vs octal notation, directory execution semantics, and ownership management with chmod and chown.",
        "keywords": "linux, permissions, chmod, chown, chgrp, posix, rwx, octal permissions, umask, sysadmin, file security",
        "html": r"""<p>At the core of Linux multi-user security is the <strong>POSIX file permission model</strong>. Every file, directory, socket, and block device on a Linux filesystem is bound to an owner user, an owner group, and an access mode that dictates who can read, modify, or execute the resource. For systems administrators, mastering permission manipulation via <code>chmod</code> and <code>chown</code> is critical for securing web servers, containers, databases, and user home directories.</p>

<h2>The POSIX Triple Security Model</h2>
<p>When you inspect files using <code>ls -l</code> or <code>stat</code>, permissions are displayed as a 10-character string (e.g. <code>-rwxr-xr--</code>):</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Component</th>
                <th>Position</th>
                <th>Symbol Example</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>File Type</strong></td>
                <td>Character 1</td>
                <td><code>-</code>, <code>d</code>, <code>l</code>, <code>s</code></td>
                <td>Regular file (<code>-</code>), Directory (<code>d</code>), Symlink (<code>l</code>), Socket (<code>s</code>)</td>
            </tr>
            <tr>
                <td><strong>User (Owner)</strong></td>
                <td>Characters 2–4</td>
                <td><code>rwx</code></td>
                <td>Permissions assigned to the specific user account that owns the file</td>
            </tr>
            <tr>
                <td><strong>Group</strong></td>
                <td>Characters 5–7</td>
                <td><code>r-x</code></td>
                <td>Permissions assigned to members of the file's owning group</td>
            </tr>
            <tr>
                <td><strong>Other (World)</strong></td>
                <td>Characters 8–10</td>
                <td><code>r--</code></td>
                <td>Permissions applied to all other local user accounts on the system</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Files vs Directories: The Critical Distinction for Execute (<code>x</code>)</h2>
<p>The meaning of Read, Write, and Execute shifts fundamentally between files and directories:</p>
<ul>
    <li><strong>Regular Files:</strong>
        <ul>
            <li><code>Read (r)</code>: Open and view file contents (e.g. via <code>cat</code>, <code>less</code>).</li>
            <li><code>Write (w)</code>: Modify, append to, or truncate file contents.</li>
            <li><code>Execute (x)</code>: Execute the file as a compiled binary or interpreted script.</li>
        </ul>
    </li>
    <li><strong>Directories:</strong>
        <ul>
            <li><code>Read (r)</code>: Read the list of filenames inside the directory (e.g. <code>ls</code>).</li>
            <li><code>Write (w)</code>: Create, delete, or rename files inside the directory (requires <code>x</code> as well).</li>
            <li><code>Execute (x)</code>: <strong>Traverse or "enter" the directory</strong> (e.g. <code>cd</code>, access files inside).</li>
        </ul>
    </li>
</ul>

<div class="callout callout-warning">
    <div class="callout-title"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i> The Directory Traversal Trap</div>
    <div class="callout-body">If a directory has Read (<code>r</code>) permission but lacks Execute (<code>x</code>), a user can list the filenames inside using <code>ls</code>, but cannot read the contents of those files, check their file sizes, or <code>cd</code> into the folder. A directory must have execute permissions to be usable.</div>
</div>

<h2>Numeric (Octal) vs Symbolic Notation</h2>
<p>Linux administrators modify permissions using the <code>chmod</code> utility via two distinct syntax modes:</p>

<h3>1. Octal (Numeric) Representation</h3>
<p>Each permission is assigned a base-2 binary weight: <strong>Read = 4</strong>, <strong>Write = 2</strong>, <strong>Execute = 1</strong>. Adding these values produces an octal digit (0 through 7) for each entity:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Octal Value</th>
                <th>Binary</th>
                <th>Permission Symbols</th>
                <th>Security Meaning</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>7</strong></td>
                <td>111</td>
                <td><code>rwx</code></td>
                <td>Full read, write, and execute</td>
            </tr>
            <tr>
                <td><strong>6</strong></td>
                <td>110</td>
                <td><code>rw-</code></td>
                <td>Read and write (standard for non-executable files)</td>
            </tr>
            <tr>
                <td><strong>5</strong></td>
                <td>101</td>
                <td><code>r-x</code></td>
                <td>Read and execute (standard for scripts & directories)</td>
            </tr>
            <tr>
                <td><strong>4</strong></td>
                <td>100</td>
                <td><code>r--</code></td>
                <td>Read-only</td>
            </tr>
            <tr>
                <td><strong>0</strong></td>
                <td>000</td>
                <td><code>---</code></td>
                <td>No permissions granted</td>
            </tr>
        </tbody>
    </table>
</div>

<p>Common enterprise octal configurations:</p>
<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code># 644: Owner rw, Group r, Other r (standard web documents, configs)
chmod 644 /var/www/html/index.html

# 755: Owner rwx, Group rx, Other rx (standard directories and binaries)
chmod 755 /usr/local/bin/deploy.sh

# 600: Owner rw, Group none, Other none (SSH private keys, DB secrets)
chmod 600 ~/.ssh/id_ed25519</code></pre>
</div>

<h3>2. Symbolic Representation</h3>
<p>Symbolic notation modifies specific bits without overwriting the entire permission mask:</p>
<ul>
    <li><strong>Targets:</strong> <code>u</code> (user/owner), <code>g</code> (group), <code>o</code> (others), <code>a</code> (all).</li>
    <li><strong>Operators:</strong> <code>+</code> (add), <code>-</code> (remove), <code>=</code> (set explicitly).</li>
</ul>

<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code># Add execute permission to the owner only
chmod u+x backup.sh

# Revoke write and execute permissions from other/world
chmod o-wx database.sqlite

# Grant group read and write
chmod g+rw /opt/app/shared.log</code></pre>
</div>

<h2>Managing Ownership with <code>chown</code> and <code>chgrp</code></h2>
<p>Only the superuser (root or a user with <code>sudo</code> privileges) can reassign file ownership in Linux:</p>

<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash (Root / Sudo Required)</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code># Change owner to www-data and group to www-data (Debian/Ubuntu web server)
sudo chown www-data:www-data /var/www/html -R

# On RHEL/Rocky/Fedora web servers (Apache runs as apache user)
sudo chown -R apache:apache /var/www/html

# Change owner only, preserving existing group
sudo chown deployuser /opt/myapp/bin

# Change group only
sudo chgrp developers /opt/myapp/code</code></pre>
</div>

<div class="callout callout-info">
    <div class="callout-title"><i class="fa-solid fa-circle-info" aria-hidden="true"></i> Distro Differences in Default Service Accounts</div>
    <div class="callout-body">Be attentive to distribution conventions: Debian/Ubuntu distributions use <code>www-data</code> as the default web server user and group, while RHEL, AlmaLinux, and Fedora use <code>apache</code> or <code>nginx</code>. Applying Ubuntu ownership paths blindly on Red Hat environments breaks service authorization.</div>
</div>

<h2>Summary</h2>
<p>The Linux file permission architecture enforces multi-tenant boundary integrity. By understanding the distinction between file and directory execution, selecting between octal and symbolic <code>chmod</code>, and assigning appropriate user and group ownership via <code>chown</code>, administrators build robust, defense-in-depth Linux systems.</p>"""
    },
    {
        "id": "linux-systemd-service-units-creation-and-control",
        "title": "Authoring Systemd Service Units: Unit Files, Dependencies & systemctl",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Intermediate",
        "readTime": "9 min read",
        "description": "Learn to build production systemd service units, manage unit dependencies, configure process restart policies, and troubleshoot services with systemctl and journalctl.",
        "keywords": "linux, systemd, systemctl, unit files, service management, journalctl, rhel, ubuntu, sysadmin, init system",
        "html": r"""<p>Modern Linux distributions—including Ubuntu, Debian, Red Hat Enterprise Linux (RHEL), AlmaLinux, Fedora, and openSUSE—utilize <strong>systemd</strong> as their default system and service manager. Replacing legacy SysVinit scripts, systemd provides parallelized service booting, aggressive dependency resolution, process tracking via Linux Control Groups (cgroups), and centralized logging. For systems engineers, authoring custom systemd service units is mandatory for production workload deployment.</p>

<h2>Systemd Unit File Architecture</h2>
<p>A systemd unit is a declarative configuration file ending in <code>.service</code> (or <code>.target</code>, <code>.timer</code>, <code>.socket</code>). Unit files reside in three primary locations on the filesystem, prioritized in order of precedence:</p>
<ol>
    <li><strong><code>/etc/systemd/system/</code> (Highest Precedence):</strong> Custom administrator-authored unit files and overrides. Always place your production service files here.</li>
    <li><strong><code>/run/systemd/system/</code>:</strong> Transient runtime units generated dynamically by systemd generators.</li>
    <li><strong><code>/usr/lib/systemd/system/</code> (Lowest Precedence):</strong> Default vendor-supplied unit files installed by package managers (<code>apt</code>, <code>dnf</code>, <code>yum</code>). Never edit these directly, as OS updates will overwrite changes.</li>
</ol>

<h2>The Anatomy of a Production <code>.service</code> Unit</h2>
<p>A standard service unit is divided into three core sections: <code>[Unit]</code>, <code>[Service]</code>, and <code>[Install]</code>. Below is an enterprise-grade service definition for an internal Go/Node/Python API service:</p>

<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-file-code" aria-hidden="true"></i> /etc/systemd/system/api-worker.service</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code>[Unit]
Description=Enterprise API Background Worker Daemon
Documentation=https://themjtechhub.site/docs
After=network-online.target remote-fs.target
Wants=network-online.target

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/api-worker
ExecStart=/opt/api-worker/bin/worker --config=/etc/api-worker/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s

# Security Hardening & Sandboxing
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target</code></pre>
</div>

<h2>Section Deep Dive & Key Directives</h2>

<h3>1. The <code>[Unit]</code> Section: Dependencies & Ordering</h3>
<ul>
    <li><strong><code>After=</code> vs <code>Requires=</code>:</strong>
        <ul>
            <li><code>After=network-online.target</code> dictates <em>ordering only</em>. It guarantees that if both units are queued to start, systemd starts <code>network-online</code> before starting this service. It does <em>not</em> force the network to start if it wasn't requested.</li>
            <li><code>Requires=</code> creates a strict operational dependency: if the required unit fails or terminates, this service immediately terminates as well.</li>
            <li><code>Wants=</code> establishes a soft dependency: systemd attempts to activate the wanted unit, but failure of that unit will not abort this service.</li>
        </ul>
    </li>
</ul>

<h3>2. The <code>[Service]</code> Section: Process Lifecycle</h3>
<ul>
    <li><strong><code>Type=</code>:</strong>
        <ul>
            <li><code>simple</code> (Default): systemd assumes the service starts immediately upon spawning the process specified in <code>ExecStart</code>. Standard for modern web servers and background workers that do not daemonize.</li>
            <li><code>forking</code>: Used for traditional UNIX daemons that call <code>fork()</code> and exit the parent process. Requires <code>PIDFile=</code> so systemd tracks the child daemon.</li>
            <li><code>oneshot</code>: Used for scripts that execute tasks and exit immediately. Useful in combination with systemd timers.</li>
            <li><code>notify</code>: The daemon sends a notification signal via <code>sd_notify()</code> to systemd when initialization is complete.</li>
        </ul>
    </li>
    <li><strong><code>User=</code> & <code>Group=</code>:</strong> Drops root privileges, running the executable under a dedicated non-privileged service account.</li>
    <li><strong><code>Restart=on-failure</code>:</strong> Automatically relaunches the daemon if the process exits with a non-zero exit code, unhandled exception, or fatal signal.</li>
</ul>

<h3>3. The <code>[Install]</code> Section: Boot Activation</h3>
<ul>
    <li><strong><code>WantedBy=multi-user.target</code>:</strong> Specifies that enabling this service links it to runlevel equivalent <code>multi-user.target</code> (standard non-graphical multi-user mode). When the server boots into multi-user target, this service launches automatically.</li>
</ul>

<h2>Controlling Services with <code>systemctl</code></h2>
<p>After creating or editing any unit file, you must instruct the systemd manager daemon to reload its configuration cache:</p>

<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash (Root / Sudo Required)</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code># 1. Reload systemd daemon to pick up new unit files
sudo systemctl daemon-reload

# 2. Enable service to start at system boot
sudo systemctl enable api-worker.service

# 3. Start the service immediately
sudo systemctl start api-worker.service

# 4. Inspect real-time status, PID, memory consumption, and recent logs
sudo systemctl status api-worker.service</code></pre>
</div>

<div class="command-header"><span class="command-label">Example Status Output</span></div>
<pre><code>● api-worker.service - Enterprise API Background Worker Daemon
     Loaded: loaded (/etc/systemd/system/api-worker.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2026-09-09 10:15:30 UTC; 15min ago
   Main PID: 48210 (worker)
      Tasks: 8 (limit: 4915)
     Memory: 42.4M
        CPU: 1.250s
     CGroup: /system.slice/api-worker.service
             └─48210 /opt/api-worker/bin/worker --config=/etc/api-worker/config.yaml</code></pre>

<h2>Troubleshooting with <code>journalctl</code></h2>
<p>Because systemd intercepts standard output (<code>stdout</code>) and standard error (<code>stderr</code>) streams from managed processes, application logs are aggregated directly into the systemd journal:</p>

<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code># Follow live logs in real time (-f) for a specific service unit (-u)
sudo journalctl -u api-worker.service -f

# View errors only (-p err) recorded since the last system boot (-b)
sudo journalctl -u api-worker.service -b -p err --no-pager</code></pre>
</div>

<h2>Summary</h2>
<p>Authoring native systemd unit files enables administrators to deploy resilient, self-healing services with granular security isolation and unified journal logging. By understanding unit file sections, choosing appropriate service types, and applying <code>daemon-reload</code> workflows, systems engineers master modern Linux application orchestration.</p>"""
    },
    {
        "id": "linux-memory-management-buffers-caches-oom-killer",
        "title": "Linux Memory Management: Buffers, Page Cache & Out-Of-Memory (OOM) Killer",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Intermediate",
        "readTime": "9 min read",
        "description": "Deconstruct Linux kernel memory allocation: virtual memory, Buffers vs Page Cache, swap space mechanics, and how the Out-Of-Memory (OOM) Killer scores processes.",
        "keywords": "linux, memory management, ram, page cache, buffers, oom killer, oom_score, swap, vmstat, sysadmin, performance",
        "html": r"""<p>One of the most persistent misunderstandings among entry-level systems administrators and support engineers is interpreting Linux memory utilization. An administrator logging into a newly provisioned database or web server frequently panics upon discovering that 95% of physical RAM is consumed, even with minimal application load.</p>
<p>In Linux, <strong>free memory is wasted memory</strong>. The Linux kernel proactively repurposes idle RAM for filesystem disk caching, releasing it dynamically the microsecond applications demand memory. Understanding the architecture of <strong>Buffers</strong>, the <strong>Page Cache</strong>, and the kernel's emergency <strong>Out-Of-Memory (OOM) Killer</strong> is foundational for diagnosing performance degradation and application crashes.</p>

<h2>Virtual Memory Architecture & Pages</h2>
<p>Linux utilizes a <strong>Virtual Memory</strong> subsystem that isolates user applications into virtual address spaces. The kernel maps virtual addresses to physical RAM using the CPU's Memory Management Unit (MMU) in atomic blocks called <strong>Pages</strong> (typically 4 KB on x86_64 architecture):</p>
<ul>
    <li><strong>Resident Set Size (RSS):</strong> The actual portion of physical RAM currently allocated and occupied by a process.</li>
    <li><strong>Virtual Size (VSZ):</strong> The total virtual memory address space allocated to a process, including shared libraries, mapped disk files, and uncommitted allocations.</li>
    <li><strong>Anonymous Memory:</strong> Memory allocated for process stacks, heaps, and variable data that is not backed by a physical file on disk.</li>
</ul>

<h2>Buffers vs Page Cache: The Disk Caching Engine</h2>
<p>When you query system memory using the <code>free -m</code> or <code>free -h</code> command, the kernel breaks down physical memory into distinct categories:</p>

<div class="tutorial-command">
    <div class="command-header"><span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash</span></div>
    <pre><code>free -h</code></pre>
</div>

<div class="command-header"><span class="command-label">Example Output</span></div>
<pre><code>               total        used        free      shared  buff/cache   available
Mem:            31Gi       8.2Gi       1.1Gi       450Mi        22Gi        22Gi
Swap:          8.0Gi       120Mi       7.9Gi</code></pre>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Column / Metric</th>
                <th>Kernel Definition & Operational Purpose</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>total</strong></td>
                <td>Total physical RAM installed and recognized by the BIOS/UEFI.</td>
            </tr>
            <tr>
                <td><strong>used</strong></td>
                <td>Memory actively allocated to user-space processes, kernel data structures, and shared memory.</td>
            </tr>
            <tr>
                <td><strong>free</strong></td>
                <td>Memory with zero current assignment. In a healthy server, this should naturally be low.</td>
            </tr>
            <tr>
                <td><strong>buff/cache</strong></td>
                <td>Combined disk caching subsystem: <em>Buffers</em> (raw disk block I/O metadata) + <em>Page Cache</em> (cached file contents).</td>
            </tr>
            <tr>
                <td><strong>available</strong></td>
                <td><strong>The True Metric:</strong> Estimated memory available for starting new applications <em>without swapping</em>. Includes free RAM plus reclaimable page cache.</td>
            </tr>
        </tbody>
    </table>
</div>

<h3>The Critical Difference: Buffers vs Cache</h3>
<ul>
    <li><strong>Buffers:</strong> Temporary in-memory storage for raw disk blocks waiting to be written to or read from physical storage. Buffers track filesystem metadata (inodes, directory listings, block bitmaps) and raw block device access.</li>
    <li><strong>Page Cache:</strong> Caches the actual data contents of files read from disk. When an application reads a file, Linux retains the read pages in RAM. Subsequent reads are fulfilled directly from memory at nanosecond speeds rather than requiring mechanical disk or NVMe lookups. If an application needs memory, the kernel immediately evicts clean page cache pages with zero penalty.</li>
</ul>

<h2>The Role of Swap & <code>swappiness</code></h2>
<p><strong>Swap space</strong> is a designated disk partition or file utilized when physical memory demands exceed RAM capacity. Furthermore, Linux uses swap to page out stagnant, inactive memory pages (such as initialization code that ran once at boot), freeing fast physical RAM for active caching.</p>
<p>The kernel parameter <code>vm.swappiness</code> (ranging from 0 to 100, default typically 60) controls the kernel's aggressiveness in swapping anonymous memory versus reclaiming page cache:</p>

<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code># Check current swappiness value
sysctl vm.swappiness

# In latency-critical database servers (e.g. MySQL, Redis), reduce swappiness to 10
sudo sysctl -w vm.swappiness=10</code></pre>
</div>

<h2>The Out-Of-Memory (OOM) Killer Mechanics</h2>
<p>Because Linux permits memory overcommitting (promising applications more virtual memory than physically exists, assuming not all will use their full allocation simultaneously), a server can exhaust both physical RAM and swap space. When the kernel cannot allocate a single additional page to service an interrupt, it invokes the <strong>Out-Of-Memory (OOM) Killer</strong> to save the operating system from a total kernel panic.</p>

<h3>How the OOM Killer Scores Processes (<code>oom_score</code>)</h3>
<p>The kernel calculates an integer score (from 0 to 1000) for every running process, visible in <code>/proc/[PID]/oom_score</code>:</p>
<ol>
    <li>The primary factor is the percentage of physical RAM consumed by the process.</li>
    <li>The kernel applies penalties for processes that consume large amounts of memory with short runtimes.</li>
    <li>Processes running as root or critical system daemons receive minor negative adjustments.</li>
    <li>The process with the highest overall <code>oom_score</code> is terminated with an uncatchable <code>SIGKILL</code> (signal 9).</li>
</ol>

<h3>Forensic Detection in <code>dmesg</code></h3>
<p>When an application crashes unexpectedly due to memory exhaustion, inspect kernel logs immediately:</p>
<div class="tutorial-command">
    <div class="command-header"><span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash</span></div>
    <pre><code>sudo dmesg -T | grep -i -E "oom|out of memory|killed process"</code></pre>
</div>

<div class="command-header"><span class="command-label">Example Output</span></div>
<pre><code>[Wed Sep  9 11:22:15 2026] Out of memory: Killed process 14205 (mysqld) total-vm:18450124kB, anon-rss:14250100kB, file-rss:0kB, shmem-rss:0kB, UID:27 pgtables:32400kB oom_score_adj:0</code></pre>

<h3>Protecting Critical Daemons with <code>oom_score_adj</code></h3>
<p>To prevent the kernel from ever terminating a critical management daemon (such as <code>sshd</code>), an administrator can configure <code>oom_score_adj</code> to <code>-1000</code>:</p>

<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash (Root / Sudo Required)</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code># Find PID of sshd daemon and grant complete immunity from OOM Killer
sudo pkill -0 sshd && echo -1000 | sudo tee /proc/$(pgrep -o sshd)/oom_score_adj</code></pre>
</div>

<h2>Summary</h2>
<p>Evaluating Linux memory health requires focusing on <strong>available memory</strong> rather than raw free memory. By recognizing the performance benefits of the Page Cache, tuning <code>swappiness</code> appropriately for database and virtualization workloads, and auditing <code>dmesg</code> for OOM Killer invocations, Linux systems engineers ensure peak server performance and workload stability.</p>"""
    }
]
