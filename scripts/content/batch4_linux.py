"""
MJ Tech Hub - Batch 4 Linux Tutorials Content
Topics:
1. linux-lvm-architecture-physical-volumes-volume-groups
2. linux-process-signaling-and-termination-kill-pkill
3. linux-systemd-journalctl-log-analysis-and-filtering
"""

LINUX_TUTORIALS = [
    {
        "id": "linux-lvm-architecture-physical-volumes-volume-groups",
        "title": "Logical Volume Manager (LVM) Architecture: PV, VG and LV Provisioning",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Intermediate",
        "description": "Master Linux storage virtualization: Physical Volumes (PV), Volume Groups (VG), Logical Volumes (LV), Physical Extents (PE), dynamic expansion, and filesystem resizing constraints.",
        "keywords": "lvm, physical volume, volume group, logical volume, pvcreate, vgcreate, lvcreate, lvextend, resize2fs, xfs_growfs, linux storage, sysadmin",
        "html": r"""<p>In traditional Linux storage administration, filesystems were formatted directly onto raw block partitions (e.g., <code>/dev/sdb1</code>). While simple, this static partitioning model presents severe operational limitations: expanding a filesystem requires unmounting the volume, modifying the partition table, rebooting the system, and risking data corruption if sector boundaries are miscalculated. Furthermore, a single filesystem cannot span across multiple physical disks.</p>
<p>The <strong>Logical Volume Manager (LVM)</strong> abstracts physical storage into a flexible, virtualized pooling architecture. With LVM, systems administrators can concatenate multiple physical drives into dynamic pools, allocate virtual block devices on demand, extend volumes online without service downtime, and take instant point-in-time snapshots.</p>

<h2>The LVM Three-Tier Abstraction Hierarchy</h2>
<p>LVM organizes storage across three distinct architectural layers:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>LVM Layer</th>
                <th>Abbreviation</th>
                <th>Architectural Role</th>
                <th>Underlying Unit of Allocation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Physical Volume</strong></td>
                <td><strong>PV</strong></td>
                <td>The physical foundation: a raw block storage device, NVMe drive, SSD, SAN LUN, or partition tagged with LVM metadata headers.</td>
                <td>Raw sectors initialized with an LVM UUID and label.</td>
            </tr>
            <tr>
                <td><strong>Volume Group</strong></td>
                <td><strong>VG</strong></td>
                <td>The centralized storage pool: aggregates one or more PVs into a unified capacity pool.</td>
                <td>Sliced into uniform allocation chunks called <strong>Physical Extents (PE)</strong>, typically <strong>4 MiB</strong> by default.</td>
            </tr>
            <tr>
                <td><strong>Logical Volume</strong></td>
                <td><strong>LV</strong></td>
                <td>The virtual partition: carved out of the VG, presenting as a standard block device (e.g., <code>/dev/vg_data/lv_app</code>) ready to format with ext4 or XFS.</td>
                <td>Composed of <strong>Logical Extents (LE)</strong>, each mapping directly 1-to-1 to a Physical Extent (PE) in the underlying Volume Group.</td>
            </tr>
        </tbody>
    </table>
</div>

<p>When an administrator writes data to a Logical Volume, LVM's device mapper kernel driver translates requests from Logical Extents (LE) to the corresponding Physical Extents (PE) distributed across one or more physical drives seamlessly.</p>

<h2>Step-by-Step LVM Provisioning Workflow</h2>
<p>Deploying a production-ready LVM storage volume follows a disciplined sequential pipeline:</p>

<h3>1. Initialize Physical Volumes (PV)</h3>
<p>Convert raw block devices (such as new SSDs <code>/dev/sdb</code> and <code>/dev/sdc</code>) into LVM physical volumes:</p>
<div class="tutorial-command">
    <pre><code># Tag block devices as LVM Physical Volumes
sudo pvcreate /dev/sdb /dev/sdc

# Verify PV initialization, size, and assigned UUIDs
sudo pvs
sudo pvdisplay /dev/sdb</code></pre>
</div>

<h3>2. Create the Volume Group (VG)</h3>
<p>Pool the initialized Physical Volumes into a named Volume Group:</p>
<div class="tutorial-command">
    <pre><code># Create Volume Group 'vg_enterprise' using both physical volumes
sudo vgcreate vg_enterprise /dev/sdb /dev/sdc

# Verify total pool capacity, free extents, and PE size (default 4 MiB)
sudo vgs
sudo vgdisplay vg_enterprise</code></pre>
</div>

<h3>3. Allocate the Logical Volume (LV)</h3>
<p>Carve a Logical Volume from the pool by specifying an absolute size (e.g., <code>-L 50G</code>) or a percentage of remaining free pool extents (e.g., <code>-l 100%FREE</code>):</p>
<div class="tutorial-command">
    <pre><code># Allocate a 50 GB Logical Volume named 'lv_database' from 'vg_enterprise'
sudo lvcreate -n lv_database -L 50G vg_enterprise

# Verify LV creation and device-mapper path (/dev/vg_enterprise/lv_database)
sudo lvs</code></pre>
</div>

<h3>4. Format and Mount the Filesystem</h3>
<p>Format the virtual block device with an enterprise filesystem (e.g., ext4) and mount it to the directory tree:</p>
<div class="tutorial-command">
    <pre><code># Format the LV with ext4
sudo mkfs.ext4 /dev/vg_enterprise/lv_database

# Create mount point and mount the volume
sudo mkdir -p /srv/database
sudo mount /dev/vg_enterprise/lv_database /srv/database

# Retrieve the filesystem UUID for permanent fstab mounting
sudo blkid /dev/vg_enterprise/lv_database</code></pre>
</div>

<h2>Dynamic Volume Expansion (Online Storage Growth)</h2>
<p>When an application volume nears full capacity, LVM enables seamless online capacity expansion without unmounting the filesystem or restarting services:</p>

<div class="tutorial-command">
    <pre><code># 1. (Optional) Add a new physical drive (/dev/sdd) to the Volume Group if pool capacity is depleted
sudo pvcreate /dev/sdd
sudo vgextend vg_enterprise /dev/sdd

# 2. Extend the Logical Volume by adding 20 GB of extents
sudo lvextend -L +20G /dev/vg_enterprise/lv_database

# 3. Expand the filesystem to occupy the newly available volume space:
# For ext4 filesystems (online expansion):
sudo resize2fs /dev/vg_enterprise/lv_database

# For XFS filesystems (must specify mount point, not device path):
sudo xfs_growfs /srv/database</code></pre>
</div>

<div class="tutorial-callout callout-warning">
    <p><strong>DANGER: Critical Warnings on Volume Reduction & Filesystem Constraints:</strong></p>
    <ul>
        <li><strong>Volume Reduction Risks:</strong> Shrinking a Logical Volume (<code>lvreduce</code>) is a high-risk destructive operation. If the block device is reduced before the filesystem is safely shrunk, file headers are truncated, resulting in irreversible data loss. Always perform a complete backup prior to volume reduction.</li>
        <li><strong>ext4 Requires Offline Shrinking:</strong> While ext4 supports <em>online expansion</em>, it strictly requires taking the volume offline (<code>umount</code>) to shrink. The administrator must execute <code>e2fsck -f</code>, shrink the filesystem first with <code>resize2fs</code>, and only then shrink the LV.</li>
        <li><strong>XFS CANNOT BE SHRUNK:</strong> <strong>XFS filesystems do NOT support shrinking under any circumstance.</strong> By architectural design, the XFS metadata structure cannot be reduced. If an XFS volume must be made smaller, administrators must back up all data, delete the Logical Volume, recreate a smaller LV, format it with XFS, and restore the data.</li>
    </ul>
</div>

<h2>Inspection and Health Telemetry</h2>
<p>Systems administrators monitor LVM health and extent allocation using standardized reporting commands:</p>

<div class="tutorial-command">
    <pre><code># Terse tabular overview across all three layers
sudo pvs
sudo vgs
sudo lvs

# Query free extents in a specific Volume Group
sudo vgdisplay vg_enterprise | grep -E "(Total PE|Alloc PE|Free PE)"

# Inspect block device mapper relationships and mount hierarchies
lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,UUID</code></pre>
</div>
<p>Ensure that Volume Groups maintain a safety margin of unallocated Free PEs to facilitate online LVM snapshot creation for consistent database backups.</p>"""
    },
    {
        "id": "linux-process-signaling-and-termination-kill-pkill",
        "title": "Process Termination & POSIX Signals: SIGTERM, SIGKILL, SIGHUP (kill/pkill)",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Beginner",
        "description": "Master Linux process lifecycle: PID/PPID hierarchy, process execution states, foreground/background job control, and POSIX signal handling with kill, pkill, and killall.",
        "keywords": "linux process, posix signals, sigterm, sigkill, sighup, kill, pkill, pgrep, ps, process management, sysadmin",
        "html": r"""<p>Every running program, service daemon, and shell command in Linux executes as an isolated <strong>process</strong> inside the kernel's virtual memory space. As applications perform computation, spawn child worker processes, consume system memory, or occasionally enter hung unresponsive loops, systems administrators must understand how the Linux kernel manages process lifecycles and communicates state changes through standardized <strong>POSIX signals</strong>.</p>
<p>Terminating misbehaving processes is not simply a matter of executing destructive kill commands; responsible system administration requires understanding process states, graceful teardown semantics, and the severe architectural risks of relying on uncatchable termination signals.</p>

<h2>Process Lifecycle, PID Hierarchy, and Execution States</h2>
<p>When the Linux kernel boots, it initializes <strong>systemd</strong> as Process ID 1 (<code>PID 1</code>). All subsequent system daemons, user shells, and application threads are spawned as child processes forming a strict hierarchical tree:</p>

<ul>
    <li><strong>PID (Process ID):</strong> Unique numerical identifier assigned to each active process.</li>
    <li><strong>PPID (Parent Process ID):</strong> The identifier of the process that spawned this child using the <code>fork()</code> or <code>clone()</code> system call. When a parent process terminates before its child, the orphaned child is automatically adopted by PID 1 (systemd).</li>
</ul>

<p>Processes cycle through standardized operational states visible in utilities like <code>ps</code>, <code>top</code>, and <code>htop</code>:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>State Code</th>
                <th>State Name</th>
                <th>Kernel Description</th>
                <th>Signal Responsiveness</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>R</strong></td>
                <td>Running / Runnable</td>
                <td>The process is actively executing on a CPU core or sitting in the kernel run queue waiting for a scheduler time-slice.</td>
                <td>Instantly processes received signals.</td>
            </tr>
            <tr>
                <td><strong>S</strong></td>
                <td>Interruptible Sleep</td>
                <td>The process is sleeping, waiting for an external event, user input, or network socket data.</td>
                <td>Wakes up immediately upon receiving a signal.</td>
            </tr>
            <tr>
                <td><strong>D</strong></td>
                <td>Uninterruptible Sleep</td>
                <td>The process is waiting for synchronous hardware I/O (typically disk write or NFS lock).</td>
                <td><strong>Cannot handle signals:</strong> Even <code>kill -9</code> will not terminate a process in state 'D' until the hardware I/O completes or times out.</td>
            </tr>
            <tr>
                <td><strong>T</strong></td>
                <td>Stopped</td>
                <td>The process was suspended by a job control signal (e.g., <code>Ctrl+Z</code> or <code>SIGSTOP</code>).</td>
                <td>Resumes execution upon receiving <code>SIGCONT</code>.</td>
            </tr>
            <tr>
                <td><strong>Z</strong></td>
                <td>Zombie (Defunct)</td>
                <td>The process has completed execution (<code>exit()</code>), but its parent has not yet read its exit status via <code>waitpid()</code>.</td>
                <td>Already dead; consumes no CPU or RAM, but occupies a slot in the kernel PID table.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Foreground vs Background Job Control</h2>
<p>Interactive terminal sessions allow administrators to manipulate process execution states directly using shell job control:</p>

<div class="tutorial-command">
    <pre><code># 1. Run a long-running backup script in the background using the ampersand (&) operator
./database_backup.sh &

# 2. Suspend an actively running foreground process: press [Ctrl + Z]
# The kernel transmits signal SIGTSTP (20), suspending the process into state 'T'

# 3. List active background jobs belonging to the current shell session
jobs -l

# 4. Resume the suspended job in the background
bg %1

# 5. Bring background job %1 back into the active interactive foreground
fg %1</code></pre>
</div>

<h2>Essential POSIX Signals for Administrators</h2>
<p>Linux processes communicate asynchronously via standardized <strong>POSIX signals</strong>. Administrators transmit signals using the <code>kill</code> utility by numerical ID or symbolic name:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Signal Number</th>
                <th>Signal Name</th>
                <th>Catchable by Process?</th>
                <th>Standard Operational Function</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1</strong></td>
                <td><strong>SIGHUP</strong></td>
                <td>Yes</td>
                <td><strong>Hangup:</strong> Originally signaled a dropped modem line. In modern servers, daemons (e.g., Nginx, Apache, sshd) catch SIGHUP to <strong>reload configuration files</strong> without restarting or dropping active client connections.</td>
            </tr>
            <tr>
                <td><strong>2</strong></td>
                <td><strong>SIGINT</strong></td>
                <td>Yes</td>
                <td><strong>Interrupt:</strong> Sent by the terminal driver when the user presses <code>Ctrl + C</code>, requesting graceful interruption of foreground commands.</td>
            </tr>
            <tr>
                <td><strong>15</strong></td>
                <td><strong>SIGTERM</strong></td>
                <td>Yes</td>
                <td><strong>Termination (Default):</strong> The standard polite termination request. Allows the process to flush write buffers to disk, release file locks, close database connections, and delete temporary files before exiting cleanly.</td>
            </tr>
            <tr>
                <td><strong>9</strong></td>
                <td><strong>SIGKILL</strong></td>
                <td><strong>NO (Uncatchable)</strong></td>
                <td><strong>Forced Kill:</strong> Handled directly by the kernel scheduler. Instantly strips memory, unmaps file pages, and destroys the process. The process is given zero CPU cycles to clean up state.</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="tutorial-callout callout-warning">
    <p><strong>Why kill -9 Must NEVER Be Your First Choice:</strong> Novice administrators frequently run <code>kill -9 &lt;PID&gt;</code> immediately when a service appears unresponsive. While the Linux kernel cleanly frees process memory and closes open file descriptors, <code>SIGKILL</code> <strong>cannot be caught, blocked, or handled by the process</strong>. This completely prevents application-level cleanup routines from executing, which can leave:</p>
    <ul>
        <li><strong>Incomplete Transactions:</strong> Uncommitted database or financial transactions are abruptly abandoned mid-flight.</li>
        <li><strong>Stale Lock and State Files:</strong> Unremoved lock files (e.g., <code>/var/run/daemon.pid</code> or <code>.lock</code> files) remain on the filesystem, frequently blocking subsequent service restarts.</li>
        <li><strong>Lost Buffered Application Data:</strong> In-memory application caches and pending write buffers that have not yet been synchronized to disk are permanently lost.</li>
        <li><strong>Application and Database Consistency Issues:</strong> Multi-file stores or relational tables can be left in an inconsistent, split state requiring slow recovery or manual repair.</li>
    </ul>
    <p><strong>Best Practice:</strong> Always send <code>SIGTERM (15)</code> first to request graceful shutdown and allow the process to flush state. Wait 5–10 seconds for cleanup routines to complete, and use <code>SIGKILL (9)</code> strictly as an emergency last resort for completely unresponsive processes.</p>
</div>

<h2>Practical Process Termination Commands</h2>
<p>Systems administrators leverage specialized CLI utilities to locate and signal processes efficiently:</p>

<div class="tutorial-command">
    <pre><code># 1. List processes matching a pattern and display their PIDs
pgrep -l -u www-data nginx

# 2. Terminate a process politely using default SIGTERM (Signal 15)
kill 14205

# 3. Explicitly send SIGHUP (Signal 1) to reload a daemon configuration
kill -HUP 14205
# Or using signal number:
kill -1 14205

# 4. Signal processes matching a pattern using pkill (targets all worker threads)
pkill -TERM -f "celery worker"

# 5. Emergency escalation: Force-kill an unresponsive process using SIGKILL (Signal 9)
kill -KILL 14205
# Or using numerical ID:
kill -9 14205

# 6. Verify that the process has completely vacated the process table
pgrep 14205 || echo "Process successfully terminated"</code></pre>
</div>

<div class="tutorial-callout callout-note">
    <p><strong>Dealing with Unkillable Zombie Processes:</strong> A zombie process (state <code>Z</code>) is already dead; transmitting <code>kill -9</code> to a zombie has zero effect because it has no memory or execution thread to terminate. To eliminate zombies, you must signal their <strong>parent process</strong> (PPID) to invoke <code>wait()</code>, or gracefully restart the parent process so systemd inherits and reaps the dead child.</p>
</div>"""
    },
    {
        "id": "linux-systemd-journalctl-log-analysis-and-filtering",
        "title": "Systemd Journal Architecture & Advanced journalctl Filtering Queries",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Intermediate",
        "description": "Master systemd centralized logging: binary journal storage, journald.conf configuration, and high-performance filtering queries by boot, unit, priority, and time.",
        "keywords": "journalctl, systemd-journald, logging, linux logs, log filtering, systemd, journald.conf, vacuum, sysadmin, telemetry",
        "html": r"""<p>Traditional Linux system logging relied on the classic Unix syslog daemon (such as <code>rsyslogd</code> or <code>syslog-ng</code>), which collected plain-text log streams and appended them into unindexed files under <code>/var/log/messages</code> or <code>/var/log/syslog</code>. While plain text is easily read with <code>cat</code> and <code>grep</code>, it suffers from severe enterprise limitations: timestamps are unstandardized, multiline logs are fragmented, unprivileged users cannot view their own service logs, and parsing gigabytes of unstructured text causes massive disk I/O bottlenecks.</p>
<p>Modern Linux distributions powered by systemd resolve these telemetry challenges through <strong>systemd-journald</strong>. Journald aggregates logs from the Linux kernel ring buffer, system services, standard output/error (stdout/stderr), and the syslog API into a high-performance, structured <strong>binary indexed format</strong> queried using the <strong>journalctl</strong> utility.</p>

<h2>Journald Architecture & Storage Modes</h2>
<p>The <code>systemd-journald</code> daemon acts as the centralized ingestion point for all system events. Unlike flat text files, every log entry in the journal is stored as a rich, structured object containing key-value metadata fields (such as <code>_SYSTEMD_UNIT</code>, <code>_PID</code>, <code>_UID</code>, <code>PRIORITY</code>, and <code>_BOOT_ID</code>):</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Journal Storage Mode</th>
                <th>Filesystem Path</th>
                <th>Persistence Characteristics</th>
                <th>Typical Deployment Scenario</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Volatile</strong></td>
                <td><code>/run/log/journal/</code></td>
                <td>Stored exclusively in RAM (tmpfs). All logs are purged upon reboot or kernel panic.</td>
                <td>Stateless live rescue media, container base images, systems with write-sensitive embedded flash memory.</td>
            </tr>
            <tr>
                <td><strong>Persistent</strong></td>
                <td><code>/var/log/journal/</code></td>
                <td>Stored on persistent disk. Logs survive reboots, enabling historical multi-boot post-mortem diagnostics.</td>
                <td>Standard enterprise servers, production database hosts, cloud virtual machines.</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="tutorial-callout callout-note">
    <p><strong>Init System Awareness:</strong> Not all Linux distributions utilize systemd or journald. Lightweight and container-focused distributions such as Alpine Linux use OpenRC and syslog-ng, Void Linux utilizes runit, and legacy enterprise installations may rely entirely on rsyslog without systemd journal integration.</p>
</div>

<h2>Configuring Persistent Logging via journald.conf</h2>
<p>To guarantee that system logs persist across reboots and enforce disk consumption limits, configure <code>/etc/systemd/journald.conf</code>:</p>

<div class="tutorial-command">
    <pre><code># Edit the primary journald configuration file
sudo nano /etc/systemd/journald.conf

# Enforce the following baseline parameters under the [Journal] block:
[Journal]
Storage=persistent
Compress=yes
SystemMaxUse=2G
SystemKeepFree=5G
MaxRetentionSec=1month

# Restart the journald service to apply storage policies
sudo systemctl restart systemd-journald</code></pre>
</div>

<h2>Advanced journalctl Filtering Queries</h2>
<p>The primary power of <code>journalctl</code> lies in executing instant, indexed queries across gigabytes of telemetry without invoking slow shell pipelines like <code>grep</code> and <code>awk</code>:</p>

<h3>1. Filtering by Systemd Service Unit</h3>
<p>Isolate logs belonging exclusively to a specific service unit, including its stdout and stderr streams:</p>
<div class="tutorial-command">
    <pre><code># Query logs for the Nginx web server service
journalctl -u nginx.service

# Combine multiple units to analyze correlated service interactions
journalctl -u nginx.service -u php-fpm.service --since "1 hour ago"</code></pre>
</div>

<h3>2. Filtering by System Boot</h3>
<p>Perform crash forensics on previous operational sessions without sifting through current runtime logs:</p>
<div class="tutorial-command">
    <pre><code># List all recorded historical boot sessions with their timestamps and UUIDs
journalctl --list-boots

# Inspect logs from the current active boot session
journalctl -b 0

# Inspect logs from the immediately preceding boot session (e.g., prior to a crash/reboot)
journalctl -b -1</code></pre>
</div>

<h3>3. Filtering by RFC 5424 Log Severity / Priority</h3>
<p>Filter logs based on standard syslog severity levels (0 Emerg, 1 Alert, 2 Crit, 3 Err, 4 Warning, 5 Notice, 6 Info, 7 Debug):</p>
<div class="tutorial-command">
    <pre><code># Display only Error, Critical, Alert, and Emergency events
journalctl -p err..alert

# Query kernel hardware errors from the current boot
journalctl -k -p err</code></pre>
</div>

<h3>4. Time-Window Boundaries</h3>
<p>Isolate exact incident timelines using flexible natural language or ISO-8601 timestamps:</p>
<div class="tutorial-command">
    <pre><code># Query logs generated in the last 30 minutes
journalctl --since "30 min ago"

# Query logs within an exact maintenance window
journalctl --since "2026-09-10 14:00:00" --until "2026-09-10 15:30:00"</code></pre>
</div>

<h3>5. Real-Time Streaming & Output Formats</h3>
<p>Stream logs continuously during active troubleshooting or export structured JSON for external SIEM log forwarding:</p>
<div class="tutorial-command">
    <pre><code># Follow active logs in real-time (equivalent to tail -f)
journalctl -f -u sshd

# Export structured JSON objects with complete metadata fields
journalctl -u sshd -n 1 -o json-pretty</code></pre>
</div>

<h2>Safe Journal Maintenance & Vacuuming</h2>
<p>Because the journal uses indexed binary files, <strong>never use manual <code>rm -rf /var/log/journal/*</code> commands</strong> to delete logs. Deleting active journal files while the daemon is running corrupts memory-mapped file handles and breaks index pointers.</p>
<p>Use journald's built-in <strong>vacuuming commands</strong> to safely prune old logs while preserving index integrity:</p>

<div class="tutorial-command">
    <pre><code># Check current disk space consumed by journal files
journalctl --disk-usage

# Prune old logs until total journal disk usage drops below 1 GB
sudo journalctl --vacuum-size=1G

# Prune logs older than 14 days
sudo journalctl --vacuum-time=14d

# Verify journal file integrity
sudo journalctl --verify</code></pre>
</div>
<p>Automating journal vacuuming ensures historical auditability without risking root volume disk exhaustion.</p>"""
    }
]
