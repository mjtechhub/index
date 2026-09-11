# scripts/content/batch5_linux.py
"""
MJ Tech Hub - Phase 6.5E Batch 5 Linux Content Module
Contains authoritative content for 3 Linux tutorials:
1. linux-troubleshooting-boot-failures-grub-emergency-mode
2. linux-standard-streams-redirection-and-pipes
3. linux-sudo-configuration-and-visudo-administration
"""

LINUX_TUTORIALS = [
    {
        "id": "linux-troubleshooting-boot-failures-grub-emergency-mode",
        "title": "Troubleshooting Boot Failures: Navigating GRUB Rescue & Emergency Mode",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Intermediate",
        "description": "Diagnose and resolve critical Linux boot failures: navigating GRUB rescue prompts, dracut initramfs emergency shells, fstab mount errors, and systemd emergency mode.",
        "keywords": "linux boot failure, grub rescue, emergency mode, dracut, initramfs, fstab errors, chroot recovery, sysadmin, kernel panic",
        "html": r"""<p>Few operational emergencies cause as much panic as an enterprise Linux server failing to boot after a kernel update, storage reconfiguration, or unscheduled power outage. Instead of a normal login prompt, the administrator is confronted with a blank screen, a cryptic <code>grub rescue&gt;</code> prompt, or a systemd emergency maintenance shell.</p>
<p>Systematic boot recovery requires understanding the sequential stages of the Linux boot architecture: UEFI/BIOS firmware, the GRUB2 bootloader, the initial RAM filesystem (initramfs), the kernel initialization, and systemd target activation.</p>

<h2>The Multi-Stage Linux Boot Architecture</h2>
<p>Boot failures manifest differently depending on which subsystem encounters an unrecoverable fault:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Boot Stage</th>
                <th>Subsystem Responsible</th>
                <th>Failure Manifestation</th>
                <th>Primary Root Cause</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Stage 1: Bootloader</strong></td>
                <td>GRUB2 (<code>/boot/efi</code>, <code>/boot/grub2</code>)</td>
                <td><code>grub rescue&gt;</code> or <code>grub&gt;</code> prompt</td>
                <td>Missing/corrupted <code>grub.cfg</code>, altered disk partition UUID, or missing EFI bootloader binary.</td>
            </tr>
            <tr>
                <td><strong>Stage 2: Early Userspace</strong></td>
                <td>Kernel & Initramfs (dracut / initrd)</td>
                <td><code>dracut:/#</code> or <code>(initramfs)</code> shell</td>
                <td>Root filesystem UUID not found, missing storage/RAID drivers, inactive LVM volume group.</td>
            </tr>
            <tr>
                <td><strong>Stage 3: Service Init</strong></td>
                <td>systemd (<code>sysinit.target</code>)</td>
                <td><code>Welcome to emergency mode!</code></td>
                <td>Non-root filesystem mount failure in <code>/etc/fstab</code>, filesystem corruption requiring manual <code>fsck</code>.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Stage 1: Recovering from the GRUB Rescue Shell</h2>
<p>If GRUB cannot locate its modules or configuration directory, it drops to the minimal <code>grub rescue&gt;</code> interface. In this mode, only internal built-in commands are available.</p>

<h3>Step-by-Step Manual GRUB Boot Workflow</h3>
<div class="tutorial-command">
    <pre><code># 1. Identify accessible disks and partitions
grub rescue> ls
# Example output: (hd0) (hd0,gpt1) (hd0,gpt2) (hd0,gpt3)

# 2. Inspect each partition to find the /boot filesystem
grub rescue> ls (hd0,gpt2)/
# Look for: vmlinuz-*, initramfs-*, or grub/grub2 directory

# 3. Set the root partition and prefix path
grub rescue> set root=(hd0,gpt2)
grub rescue> set prefix=(hd0,gpt2)/boot/grub2

# 4. Load the standard normal module and enter full GRUB menu
grub rescue> insmod normal
grub rescue> normal</code></pre>
</div>
<p>Once the full GRUB menu loads, boot into the kernel. After logging in as root, permanently regenerate the GRUB configuration to prevent recurrence:</p>
<div class="tutorial-command">
    <pre><code># RHEL / Rocky / Fedora:
grub2-mkconfig -o /boot/grub2/grub.cfg

# Ubuntu / Debian:
update-grub</code></pre>
</div>

<h2>Stage 2: Resolving Dracut / Initramfs Shell Failures</h2>
<p>If the kernel decompresses successfully but cannot mount the root filesystem (e.g., <code>/dev/mapper/vg00-root</code>), execution halts inside the initramfs shell (<code>dracut:/#</code>):</p>

<div class="tutorial-command">
    <pre><code># 1. Inspect block devices and storage UUIDs
dracut:/# blkid

# 2. If using LVM, scan and activate all volume groups
dracut:/# lvm pvscan
dracut:/# lvm vgscan
dracut:/# lvm vgchange -ay

# 3. Check and repair root filesystem integrity
dracut:/# e2fsck -y /dev/mapper/vg00-root
# (Or 'xfs_repair -v /dev/mapper/vg00-root' for XFS filesystems)

# 4. Resume normal boot sequence
dracut:/# exit</code></pre>
</div>

<h2>Stage 3: Navigating Systemd Emergency Mode</h2>
<p>When systemd reaches <code>sysinit.target</code>, it attempts to mount all filesystems declared in <code>/etc/fstab</code>. By default, if any local filesystem fails to mount (e.g., an external backup disk is unplugged or a secondary partition is dirty), systemd halts the entire boot process and drops to emergency mode:</p>

<div class="tutorial-command">
    <pre><code>Give root password for maintenance
(or press Control-D to continue):</code></pre>
</div>

<p>To diagnose and remediate from emergency mode:</p>
<ol>
    <li>Enter the root password to access the maintenance shell.</li>
    <li>Remount the root filesystem read-write:
        <div class="tutorial-command">
            <pre><code>mount -o remount,rw /</code></pre>
        </div>
    </li>
    <li>Examine systemd journal logs to pinpoint the offending mount:
        <div class="tutorial-command">
            <pre><code>journalctl -xb | grep -i "failed"</code></pre>
        </div>
    </li>
    <li>Edit <code>/etc/fstab</code> to comment out the missing mount or add the <code>nofail</code> mount option:
        <div class="tutorial-command">
            <pre><code># Safe entry with nofail: prevents boot halting if disk is missing
UUID=1234-ABCD   /mnt/data   ext4   defaults,nofail   0   2</code></pre>
        </div>
    </li>
    <li>Test all mounts and reboot:
        <div class="tutorial-command">
            <pre><code>mount -a
systemctl reboot</code></pre>
        </div>
    </li>
</ol>

<div class="tutorial-callout callout-warning">
    <p><strong>The Role of the nofail Mount Option:</strong> Secondary and non-critical data partitions (such as secondary database storage, NFS shares, or external drives) should always include the <code>nofail</code> option in <code>/etc/fstab</code>. Without <code>nofail</code>, a single detached auxiliary volume prevents the entire production server from booting.</p>
</div>

<h2>Chroot Recovery from Live Rescue Media</h2>
<p>When an operating system is completely unbootable from disk, boot the server using live rescue media (such as an installation ISO in rescue mode), mount the storage, and enter a <code>chroot</code> jail to repair the broken system:</p>

<div class="tutorial-command">
    <pre><code># 1. Mount root filesystem and virtual kernel filesystems
mount /dev/mapper/vg00-root /mnt
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys

# 2. Enter the chroot jail
chroot /mnt

# 3. You now operate directly inside the broken installation:
# Reinstall kernel packages or rebuild initramfs
dracut -f --kver $(uname -r)
# Reinstall GRUB to the Master Boot Record / EFI partition
grub2-install /dev/sda
exit

# 4. Unmount cleanly and reboot
umount -R /mnt
reboot</code></pre>
</div>"""
    },
    {
        "id": "linux-standard-streams-redirection-and-pipes",
        "title": "Standard Streams (stdin, stdout, stderr), Pipes & Redirection Operators",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Beginner",
        "description": "Master POSIX standard I/O streams: File descriptors 0, 1, and 2, redirection operators (>, >>, 2>&1), pipelines (|), tee, and robust exit code handling in Bash.",
        "keywords": "linux streams, stdin, stdout, stderr, redirection, bash pipes, file descriptors, 2>&1, /dev/null, tee, pipestatus",
        "html": r"""<p>The Unix philosophy is built around a core architectural tenet: <em>"Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface."</em></p>
<p>At the foundation of this philosophy lies the concept of <strong>Standard I/O Streams</strong>. Understanding how the Linux kernel abstracts inputs and outputs through numeric file descriptors, and how the Bash shell redirects and chains these streams using operators and pipes, is essential for every systems administrator and automation engineer.</p>

<h2>POSIX Standard File Descriptors: 0, 1, and 2</h2>
<p>Whenever the Linux kernel launches a process, it automatically binds three fundamental I/O channels represented by numeric <strong>File Descriptors (FD)</strong>:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>File Descriptor</th>
                <th>Stream Name</th>
                <th>Default Source / Destination</th>
                <th>Functional Purpose</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>0</code></td>
                <td><strong>stdin</strong> (Standard Input)</td>
                <td>Keyboard / Terminal</td>
                <td>Feeds input data into the process for execution.</td>
            </tr>
            <tr>
                <td><code>1</code></td>
                <td><strong>stdout</strong> (Standard Output)</td>
                <td>Display Terminal / Screen</td>
                <td>Transmits successful execution results and primary data stream.</td>
            </tr>
            <tr>
                <td><code>2</code></td>
                <td><strong>stderr</strong> (Standard Error)</td>
                <td>Display Terminal / Screen</td>
                <td>Transmits error messages, diagnostics, and operational warnings.</td>
            </tr>
        </tbody>
    </table>
</div>

<p>Because both <code>stdout</code> and <code>stderr</code> render to the terminal screen simultaneously by default, users often fail to realize they are entirely separate streams. Separating them via shell redirection allows administrators to log errors independently from standard output.</p>

<h2>Redirection Operators Deep Dive</h2>
<p>The shell intercepts redirection operators before launching the command, modifying the process's file descriptor table:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Operator</th>
                <th>Description</th>
                <th>Practical Example</th>
                <th>Behavioral Effect</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>&gt;</code></td>
                <td>Redirect stdout (overwrite)</td>
                <td><code>uname -r &gt; kernel.txt</code></td>
                <td>Overwrites destination file with process stdout.</td>
            </tr>
            <tr>
                <td><code>&gt;&gt;</code></td>
                <td>Redirect stdout (append)</td>
                <td><code>date &gt;&gt; uptime.log</code></td>
                <td>Appends process stdout to the end of the file.</td>
            </tr>
            <tr>
                <td><code>2&gt;</code></td>
                <td>Redirect stderr (overwrite)</td>
                <td><code>find / -name "*.conf" 2&gt; errors.txt</code></td>
                <td>Captures permission denied errors into <code>errors.txt</code> while displaying clean output on screen.</td>
            </tr>
            <tr>
                <td><code>2&gt;&gt;</code></td>
                <td>Redirect stderr (append)</td>
                <td><code>backup.sh 2&gt;&gt; backup_errors.log</code></td>
                <td>Appends error messages to an ongoing error log file.</td>
            </tr>
            <tr>
                <td><code>&lt;</code></td>
                <td>Redirect stdin from file</td>
                <td><code>mysql -u root db_prod &lt; dump.sql</code></td>
                <td>Supplies the contents of a file as input to stdin.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Combining Streams: The 2>&1 Idiom</h2>
<p>To capture both standard output and error diagnostics into a single unified log file, administrators use stream duplication:</p>

<div class="tutorial-command">
    <pre><code># POSIX Standard Method: Redirect stdout to file, then duplicate stderr to stdout
command > output.log 2>&1

# Modern Bash Shortcut (equivalent behavior)
command &> output.log</code></pre>
</div>

<div class="tutorial-callout callout-warning">
    <p><strong>Order of Operations Trap:</strong> The sequence of redirection matters! Executing <code>command 2>&1 > output.log</code> does <em>not</em> combine streams into the file. The shell evaluates left-to-right: it first redirects <code>stderr</code> to the current location of <code>stdout</code> (the terminal screen), and then redirects <code>stdout</code> to the file. As a result, errors still spill onto the terminal!</p>
</div>

<h3>Discarding Unwanted Output: /dev/null</h3>
<p>The special character device <code>/dev/null</code> (the Unix bit-bucket) discards all data written to it. To run a command silently in cron jobs or background scripts:</p>

<div class="tutorial-command">
    <pre><code># Discard all output and all error messages completely
command > /dev/null 2>&1</code></pre>
</div>

<h2>Pipelines: Inter-Process Communication in Memory</h2>
<p>The pipe operator (<code>|</code>) connects the <strong>stdout (FD 1)</strong> of the preceding process directly to the <strong>stdin (FD 0)</strong> of the succeeding process:</p>

<div class="tutorial-command">
    <pre><code># Count how many users have /bin/bash as their default login shell
grep '/bin/bash' /etc/passwd | wc -l

# Identify the top 5 memory-consuming processes
ps aux --sort=-%mem | head -n 6</code></pre>
</div>

<p>Pipes execute concurrently in separate subshells. Data flows through a kernel memory buffer without touching physical storage, making pipelines exceptionally fast and scalable.</p>

<div class="tutorial-callout callout-note">
    <p><strong>Pipes Only Capture stdout:</strong> By default, the pipe operator (<code>|</code>) redirects only standard output (FD 1). Errors generated on <code>stderr</code> (FD 2) will still bypass the pipe and print directly to the terminal screen. In modern Bash, use <code>|&</code> to pipe both stdout and stderr together into the next command.</p>
</div>

<h2>Splitting Streams with tee</h2>
<p>When running long automation scripts, administrators often want to observe command progress live on screen while simultaneously logging output to disk. The <code>tee</code> utility acts as a T-junction splitter:</p>

<div class="tutorial-command">
    <pre><code># Print output to terminal and simultaneously write to build.log
./build_kernel.sh | tee build.log

# Append to log file instead of overwriting (-a)
./deploy.sh | tee -a deployment.log</code></pre>
</div>

<h2>Pipeline Exit Codes & PIPESTATUS</h2>
<p>In standard Bash execution, the return code (<code>$?</code>) of a pipeline reflects only the exit code of the <em>final</em> command in the chain:</p>

<div class="tutorial-command">
    <pre><code># Even if 'cat' fails because file does not exist, 'grep' returns 1 (no match)
cat non_existent_file.txt | grep "test"
echo $?
# Output: 1 (grep's exit code, hiding cat's failure!)</code></pre>
</div>

<p>In production enterprise scripts, use <strong>pipefail</strong> to ensure that failures anywhere in a pipeline trigger error handling:</p>

<div class="tutorial-command">
    <pre><code># Enable pipefail: returns the exit code of the rightmost command that failed
set -o pipefail

# In Bash, inspect exit codes of every segment in the pipeline:
cat non_existent_file.txt | grep "test"
echo "${PIPESTATUS[@]}"
# Example Output: 1 1 (both commands failed)</code></pre>
</div>"""
    },
    {
        "id": "linux-sudo-configuration-and-visudo-administration",
        "title": "Sudoers Administration: Configuring Least Privilege Rules with visudo",
        "category": "Linux",
        "category_dir": "linux",
        "category_page": "linux.html",
        "level": "Intermediate",
        "description": "Master enterprise Linux privilege delegation: /etc/sudoers syntax, visudo safety locking, granular command aliases, NOPASSWD controls, and NOEXEC escape prevention.",
        "keywords": "linux sudo, visudo, /etc/sudoers, least privilege, sudoers.d, cmnd_alias, nopasswd, noexec, privilege escalation, sysadmin",
        "html": r"""<p>Sharing the root superuser password among team members is a catastrophic operational vulnerability: it destroys individual accountability, creates unmanageable security blast radiuses, and violates compliance standards (such as PCI-DSS, SOC 2, and CIS Benchmarks).</p>
<p>The standard mechanism for enforcing the <strong>Principle of Least Privilege (PoLP)</strong> on Linux is <strong>sudo (Superuser Do)</strong>. Through the <code>sudoers</code> policy engine, administrators grant granular, auditable administrative rights to specific users and groups without disclosing the root account credentials.</p>

<h2>The Sudoers Policy Architecture</h2>
<p>Sudo evaluates administrative permissions using rules defined in <code>/etc/sudoers</code> and modular files inside <code>/etc/sudoers.d/</code>. The configuration file follows a strict, declarative syntax:</p>

<div class="tutorial-command">
    <pre><code># Sudoers Grammar Format
who_user/group    where_host = (runas_user : runas_group)    [tag:] commands</code></pre>
</div>

<h3>Grammar Field Breakdown</h3>
<ul>
    <li><strong>Who:</strong> The user or group granted permissions. Groups are prefixed with a percent sign (e.g., <code>%wheel</code> in RHEL or <code>%sudo</code> in Ubuntu).</li>
    <li><strong>Where:</strong> The hostnames on which the rule applies (almost universally <code>ALL</code> in modern centralized configurations).</li>
    <li><strong>Run As:</strong> The target identity the user is permitted to assume (default is <code>(ALL:ALL)</code>, meaning any user and group).</li>
    <li><strong>Commands:</strong> Comma-delimited list of absolute binary paths the user is permitted to execute.</li>
</ul>

<h2>Why visudo is Mandatory</h2>
<p>Administrators must <strong>never</strong> edit <code>/etc/sudoers</code> directly using standard text editors like <code>nano</code> or <code>vim</code>. Doing so risks leaving syntax errors that lock all administrators out of elevated privileges.</p>

<p>Always use the <strong>visudo</strong> utility:</p>

<div class="tutorial-command">
    <pre><code># Launch visudo safely (uses default system editor)
sudo visudo

# Launch visudo using vim explicitly
sudo EDITOR=vim visudo

# Validate syntax of an auxiliary drop-in file without opening an editor
sudo visudo -c -f /etc/sudoers.d/99-webadmin</code></pre>
</div>

<p><code>visudo</code> provides three mandatory safeguards:</p>
<ol>
    <li><strong>Locking:</strong> Places an exclusive lock on the file to prevent concurrent conflicting edits.</li>
    <li><strong>Temporary Staging:</strong> Writes changes to a temporary file (e.g., <code>/etc/sudoers.tmp</code>).</li>
    <li><strong>Strict Syntax Validation:</strong> Parses the file with its internal compiler upon saving. If a syntax error is detected, <code>visudo</code> refuses to apply changes and prompts: <code>What now? [e]dit, [x]it, [Q]uit without saving</code>.</li>
</ol>

<h2>Granular Delegation via Aliases</h2>
<p>To prevent repetitive rule proliferation and simplify access reviews, <code>sudoers</code> supports four types of aliases:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Alias Identifier</th>
                <th>Grouped Elements</th>
                <th>Enterprise Configuration Example</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>User_Alias</code></td>
                <td>List of usernames, group names, or other User_Aliases</td>
                <td><code>User_Alias SEC_OPS = alice, bob, %secgroup</code></td>
            </tr>
            <tr>
                <td><code>Host_Alias</code></td>
                <td>Hostnames, IP addresses, or subnets</td>
                <td><code>Host_Alias WEB_FARM = 10.0.1.10, 10.0.1.11, web03</code></td>
            </tr>
            <tr>
                <td><code>Runas_Alias</code></td>
                <td>Target execution identities</td>
                <td><code>Runas_Alias DB_ADMIN = oracle, postgres, mysql</code></td>
            </tr>
            <tr>
                <td><code>Cmnd_Alias</code></td>
                <td>List of specific allowed executable binaries</td>
                <td><code>Cmnd_Alias NGINX_MGT = /usr/bin/systemctl restart nginx, /usr/bin/systemctl reload nginx</code></td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Modular Sudoers: /etc/sudoers.d/ Best Practices</h2>
<p>Modifying the core <code>/etc/sudoers</code> file directly complicates automated package upgrades. Enterprise configuration managers (Ansible, Puppet) place individual drop-in files inside <code>/etc/sudoers.d/</code>:</p>

<div class="tutorial-command">
    <pre><code># Create a dedicated configuration file for junior administrators
sudo visudo -f /etc/sudoers.d/20-junior-admins</code></pre>
</div>

<p>Add least-privilege service management rules:</p>
<div class="tutorial-command">
    <pre><code># Define allowed commands for web service management
Cmnd_Alias WEB_SERVICES = /usr/bin/systemctl restart httpd, /usr/bin/systemctl reload httpd, /usr/bin/journalctl -u httpd

# Permit junior admin team to execute web services commands without password
%junioradmins ALL=(root) NOPASSWD: WEB_SERVICES</code></pre>
</div>

<div class="tutorial-callout callout-warning">
    <p><strong>File Naming and Permission Rules in /etc/sudoers.d/:</strong> Drop-in files must be owned by <code>root:root</code> and have file permissions strictly set to <code>0440</code> (<code>chmod 0440 /etc/sudoers.d/*</code>). Furthermore, filenames must <em>not</em> contain periods (<code>.</code>) or tildes (<code>~</code>); otherwise, sudo ignores them completely.</p>
</div>

<h2>Critical Security Hazards: Shell Escapes & NOEXEC</h2>
<p>A common vulnerability in sudo configuration is granting access to binaries that possess built-in shell escape capabilities:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Vulnerable Binary</th>
                <th>Escape Vector</th>
                <th>Exploitation Mechanics</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>/usr/bin/vim</code> or <code>nano</code></td>
                <td>Internal shell execution</td>
                <td>From within vim, typing <code>:!/bin/sh</code> spawns an interactive root shell.</td>
            </tr>
            <tr>
                <td><code>/usr/bin/less</code> or <code>more</code></td>
                <td>Pager command execution</td>
                <td>Typing <code>!/bin/sh</code> while viewing a file instantly escapes to root.</td>
            </tr>
            <tr>
                <td><code>/usr/bin/find</code></td>
                <td><code>-exec</code> parameter</td>
                <td>Executing <code>sudo find . -exec /bin/sh \;</code> spawns root shell.</td>
            </tr>
        </tbody>
    </table>
</div>

<p>To prevent users from breaking out of text editors or pagers into root shells, utilize the <code>NOEXEC:</code> tag (which leverages <code>LD_PRELOAD</code> to intercept <code>execve</code> system calls) or deploy <code>sudoedit</code> instead of granting sudo directly on editor binaries:</p>

<div class="tutorial-command">
    <pre><code># Correct: Use sudoedit to allow file editing without shell escape risk
alice ALL=(root) sudoedit /etc/nginx/nginx.conf

# Alternatively, apply the NOEXEC tag to restrict execution
bob ALL=(root) NOEXEC: /usr/bin/less /var/log/*</code></pre>
</div>

<h2>Auditing and Verifying Sudo Privileges</h2>
<p>To verify the effective privileges of a user without executing commands:</p>

<div class="tutorial-command">
    <pre><code># Check active sudo privileges for the current session
sudo -l

# Check sudo privileges assigned to a specific target user
sudo -l -U alice</code></pre>
</div>"""
    }
]
