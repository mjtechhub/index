# scripts/content/batch5_windows.py
"""
MJ Tech Hub - Phase 6.5E Batch 5 Windows Content Module
Contains authoritative content for 3 Windows tutorials:
1. windows-registry-architecture-and-root-hives
2. windows-robocopy-advanced-file-replication-guide
3. windows-active-directory-domain-join-prerequisites-workflow
"""

WINDOWS_TUTORIALS = [
    {
        "id": "windows-registry-architecture-and-root-hives",
        "title": "Windows Registry Architecture: Root Hives & System Keys",
        "category": "Windows",
        "category_dir": "windows",
        "category_page": "windows.html",
        "level": "Intermediate",
        "description": "Master Windows Registry internals: HKEY root hives, disk-backed hive files, transaction logging, value data types, and enterprise management via PowerShell.",
        "keywords": "windows registry, regedit, hklm, hkcu, registry hives, ntuser.dat, dword, reg_sz, powershell psdrive, sysadmin",
        "html": r"""<p>The <strong>Windows Registry</strong> is a hierarchical, database-driven configuration store introduced in early Windows NT to replace legacy text-based <code>.ini</code> and configuration files. Operating at the core of Windows 11 and Windows Server 2022/2025, the Registry centralizes hardware drivers, kernel parameters, service configurations, user profile preferences, and installed software settings.</p>
<p>For systems administrators, mastering the Registry is vital: group policies, system hardening baselines, security configurations, and forensic analysis all interface directly with its root hives and underlying disk files.</p>

<h2>Logical Structure: The Five Root Hives</h2>
<p>When administrators launch the Registry Editor (<code>regedit.exe</code>), Windows presents five logical root keys (often abbreviated as hives). While they appear as top-level containers, two are primary hardware/system stores, and three are dynamic symbolic links:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Logical Root Hive</th>
                <th>Abbreviation</th>
                <th>Physical Storage Type</th>
                <th>Operational Scope & Content</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>HKEY_LOCAL_MACHINE</strong></td>
                <td><code>HKLM</code></td>
                <td>Physical on disk</td>
                <td>System-wide settings applicable to all users and hardware: kernel parameters, security policy, system services, and installed software.</td>
            </tr>
            <tr>
                <td><strong>HKEY_USERS</strong></td>
                <td><code>HKU</code></td>
                <td>Physical on disk</td>
                <td>Contains individual subkeys for every loaded user profile on the machine, indexed by their Active Directory / local Security Identifier (SID).</td>
            </tr>
            <tr>
                <td><strong>HKEY_CURRENT_USER</strong></td>
                <td><code>HKCU</code></td>
                <td>Symbolic Link</td>
                <td>Points dynamically to the currently logged-on user's branch inside <code>HKEY_USERS\&lt;User-SID&gt;</code> (e.g., desktop background, app settings).</td>
            </tr>
            <tr>
                <td><strong>HKEY_CLASSES_ROOT</strong></td>
                <td><code>HKCR</code></td>
                <td>Symbolic Link / Merged</td>
                <td>Merges <code>HKLM\Software\Classes</code> with <code>HKCU\Software\Classes</code>. Stores file associations, ProgIDs, and COM/OLE object registrations.</td>
            </tr>
            <tr>
                <td><strong>HKEY_CURRENT_CONFIG</strong></td>
                <td><code>HKCC</code></td>
                <td>Symbolic Link</td>
                <td>Points to <code>HKLM\SYSTEM\CurrentControlSet\Hardware Profiles\Current</code>, storing volatile hardware profile information used at boot.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Physical Hive Files & Transactional Integrity</h2>
<p>The registry is not stored as a single monolithic file. Instead, the kernel's Configuration Manager parses distinct binary files called <strong>hives</strong> located on the physical disk:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Registry Hive Branch</th>
                <th>Physical File Path on Disk</th>
                <th>Access & Security Level</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>HKLM\SYSTEM</code></td>
                <td><code>C:\Windows\System32\config\SYSTEM</code></td>
                <td>System / Kernel startup parameters and driver boot control sets.</td>
            </tr>
            <tr>
                <td><code>HKLM\SOFTWARE</code></td>
                <td><code>C:\Windows\System32\config\SOFTWARE</code></td>
                <td>Machine-wide third-party software and Windows operating system components.</td>
            </tr>
            <tr>
                <td><code>HKLM\SAM</code></td>
                <td><code>C:\Windows\System32\config\SAM</code></td>
                <td>Local Security Accounts Manager; stores local user hashes (heavily restricted to SYSTEM).</td>
            </tr>
            <tr>
                <td><code>HKLM\SECURITY</code></td>
                <td><code>C:\Windows\System32\config\SECURITY</code></td>
                <td>Local security policies, audit rules, and LSA secrets.</td>
            </tr>
            <tr>
                <td><code>HKCU</code></td>
                <td><code>C:\Users\&lt;Username&gt;\NTUSER.DAT</code></td>
                <td>User-specific profile hive mounted into memory during user login.</td>
            </tr>
        </tbody>
    </table>
</div>

<h3>Registry Transaction Logs (.LOG1, .LOG2)</h3>
<p>To prevent catastrophic database corruption during sudden power losses or system crashes, Windows utilizes <strong>Common Log File System (CLFS)</strong> transactional logging. Alongside each hive file are transaction journals (e.g., <code>SYSTEM.LOG1</code> and <code>SYSTEM.LOG2</code>). All registry write operations are recorded in the transaction log first before being committed to the main hive file. If the system loses power mid-write, the kernel replays or rolls back incomplete transactions during the subsequent boot phase.</p>

<h2>Registry Value Data Types</h2>
<p>Each registry key contains one or more named values storing specific binary or string data structures:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Data Type Constant</th>
                <th>Common Usage</th>
                <th>Example Value Representation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>REG_SZ</strong></td>
                <td>Fixed-length Unicode text string.</td>
                <td><code>"C:\Program Files\MyApp"</code></td>
            </tr>
            <tr>
                <td><strong>REG_EXPAND_SZ</strong></td>
                <td>Expandable string containing unexpanded environment variables.</td>
                <td><code>"%SystemRoot%\System32"</code></td>
            </tr>
            <tr>
                <td><strong>REG_DWORD</strong></td>
                <td>32-bit unsigned integer (boolean flags, port numbers, time limits).</td>
                <td><code>0x00000001 (1)</code> or <code>3389</code></td>
            </tr>
            <tr>
                <td><strong>REG_QWORD</strong></td>
                <td>64-bit integer used for 64-bit memory sizes and 64-bit timestamps.</td>
                <td><code>0x00000001A4C00000</code></td>
            </tr>
            <tr>
                <td><strong>REG_BINARY</strong></td>
                <td>Raw binary byte array (hardware configuration, cryptographic hashes).</td>
                <td><code>01 00 00 00 D0 8C 9DDF</code></td>
            </tr>
            <tr>
                <td><strong>REG_MULTI_SZ</strong></td>
                <td>Array of null-terminated strings delimited by an empty string.</td>
                <td><code>"DNS1\0DNS2\0DNS3\0\0"</code></td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Managing the Registry via PowerShell (PSDrives)</h2>
<p>Modern Windows systems administration avoids manual <code>regedit.exe</code> editing. Instead, administrators automate registry changes using PowerShell's built-in <code>Registry</code> provider, which exposes <code>HKLM:</code> and <code>HKCU:</code> as virtual filesystems:</p>

<div class="tutorial-command">
    <pre><code># 1. Inspect registry keys using standard filesystem cmdlets
Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion' | Select-Object ProgramFilesDir, CommonFilesDir

# 2. Create a new registry key for an application policy
New-Item -Path 'HKLM:\SOFTWARE\Policies\MyEnterprise' -Force

# 3. Create or update a REG_DWORD value (e.g., enable telemetry restriction)
Set-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\MyEnterprise' -Name "DisableTelemetry" -Value 1 -Type DWord

# 4. Read the configured value back to verify
Get-ItemPropertyValue -Path 'HKLM:\SOFTWARE\Policies\MyEnterprise' -Name "DisableTelemetry"

# 5. Remove the value cleanly
Remove-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\MyEnterprise' -Name "DisableTelemetry"</code></pre>
</div>

<div class="tutorial-callout callout-warning">
    <p><strong>Destructive Registry Operations:</strong> Erroneous modifications or deletions in <code>HKLM\SYSTEM</code> or <code>HKLM\SOFTWARE</code> can render the Windows operating system unbootable. Always export a backup of the target branch (<code>reg export HKLM\SYSTEM C:\Backup\system.reg</code>) or create a System Restore Point prior to making registry changes.</p>
</div>

<h2>Registry Hardening & Security Best Practices</h2>
<ul>
    <li><strong>Principle of Least Privilege:</strong> Non-administrative users should have strictly read-only permissions across <code>HKLM</code>. Only elevated administrators and <code>NT AUTHORITY\SYSTEM</code> should possess write rights.</li>
    <li><strong>Auditing Registry Persistence:</strong> Adversaries frequently achieve persistence via Run keys: <code>HKLM\Software\Microsoft\Windows\CurrentVersion\Run</code> and <code>HKCU\Software\Microsoft\Windows\CurrentVersion\Run</code>. Monitor these keys with Sysinternals Autoruns or EDR tools.</li>
    <li><strong>Remote Registry Service:</strong> Ensure the <code>RemoteRegistry</code> Windows service is disabled in enterprise environments unless strictly required by centralized vulnerability scanners.</li>
</ul>"""
    },
    {
        "id": "windows-robocopy-advanced-file-replication-guide",
        "title": "Robocopy Advanced File Replication, Mirroring & Multithreading",
        "category": "Windows",
        "category_dir": "windows",
        "category_page": "windows.html",
        "level": "Intermediate",
        "description": "Master Windows Robust File Copy (Robocopy): enterprise data migration, /MIR mirroring mechanics, multithreaded performance (/MT), ACL security preservation, and exit code handling.",
        "keywords": "robocopy, windows file copy, file migration, /mir, multithreading /mt, copyall, ntfs acls, exit codes, powershell, sysadmin",
        "html": r"""<p>File migrations and large-scale directory synchronization are routine administrative responsibilities. However, relying on the standard Windows File Explorer GUI or legacy command-line tools like <code>copy</code> and <code>xcopy</code> frequently results in failed operations: long file path limits exceed 260 characters, network drops abort multi-gigabyte transfers, file timestamps reset, and NTFS Access Control Lists (ACLs) are stripped.</p>
<p>Microsoft's standard for enterprise data replication is <strong>Robocopy (Robust File Copy)</strong>. Built natively into Windows 11 and Windows Server, Robocopy provides multithreaded transfer engines, comprehensive metadata and security preservation, intelligent retry mechanisms, and bitmask exit codes designed for automated scripts.</p>

<h2>Core Syntax and Operational Flags</h2>
<p>Robocopy follows a standardized syntax: <code>robocopy &lt;source&gt; &lt;destination&gt; [file...] [options]</code>.</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Category</th>
                <th>Switch</th>
                <th>Functional Behavior</th>
                <th>Operational Guidance</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Copy Scope</strong></td>
                <td><code>/E</code></td>
                <td>Copies all subdirectories, including empty ones.</td>
                <td>Standard recursive directory tree duplication.</td>
            </tr>
            <tr>
                <td><strong>Mirroring</strong></td>
                <td><code>/MIR</code></td>
                <td>Mirrors source tree to destination (equivalent to <code>/E /PURGE</code>).</td>
                <td><strong>Caution:</strong> Deletes any destination file that does not exist in the source!</td>
            </tr>
            <tr>
                <td><strong>Performance</strong></td>
                <td><code>/MT:n</code></td>
                <td>Enables multithreaded copying using <code>n</code> threads (1 to 128; default is 8).</td>
                <td>Dramatically accelerates transfers of millions of small files over fast networks (e.g., <code>/MT:32</code>).</td>
            </tr>
            <tr>
                <td><strong>Restartability</strong></td>
                <td><code>/Z</code></td>
                <td>Enables restartable mode for network file transfers.</td>
                <td>If connection drops mid-file, Robocopy resumes transfer where it left off instead of restarting from byte 0.</td>
            </tr>
            <tr>
                <td><strong>Metadata</strong></td>
                <td><code>/COPYALL</code></td>
                <td>Copies all file info (<code>/COPY:DATSOU</code>).</td>
                <td>Preserves Data, Attributes, Timestamps, Security (ACLs), Owner info, and Auditing info.</td>
            </tr>
            <tr>
                <td><strong>Logging</strong></td>
                <td><code>/NP /NDL /TEE</code></td>
                <td>Suppresses progress percentage (<code>/NP</code>) and directory lists (<code>/NDL</code>); outputs to console and log (<code>/TEE</code>).</td>
                <td>Keeps automation log files clean and performant.</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="tutorial-callout callout-warning">
    <p><strong>The Danger of /MIR (Mirror Mode):</strong> The <code>/MIR</code> switch enforces parity. If the target destination directory already contains existing corporate data that is absent from the source path, Robocopy will permanently purge those files from the destination without sending them to the Recycle Bin. Always run a trial simulation with <code>/L</code> (List Only mode) before executing a mirror command in production.</p>
</div>

<h2>Preserving Security & Permissions: /COPY Flags</h2>
<p>When migrating shared folders between Windows file servers, preserving NTFS permissions is critical. Robocopy provides granular control via the <code>/COPY</code> flag:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Flag Code</th>
                <th>Preserved Metadata Element</th>
                <th>Administrative Requirement</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>D</strong></td>
                <td>Data (file payload contents)</td>
                <td>Standard read permissions.</td>
            </tr>
            <tr>
                <td><strong>A</strong></td>
                <td>Attributes (Read-Only, Hidden, System, Archive)</td>
                <td>Standard write permissions.</td>
            </tr>
            <tr>
                <td><strong>T</strong></td>
                <td>Timestamps (Created, Modified, Last Accessed)</td>
                <td>Ensures file modification times match original source.</td>
            </tr>
            <tr>
                <td><strong>S</strong></td>
                <td>NTFS Security (Discretionary ACLs)</td>
                <td>Preserves explicit and inherited access rights.</td>
            </tr>
            <tr>
                <td><strong>O</strong></td>
                <td>Owner information</td>
                <td>Requires <em>Restore Files and Directories</em> administrative user right.</td>
            </tr>
            <tr>
                <td><strong>U</strong></td>
                <td>Auditing information (System ACLs)</td>
                <td>Requires <em>Manage Auditing and Security Log</em> administrative right.</td>
            </tr>
        </tbody>
    </table>
</div>

<p>For standard enterprise file server migrations, administrators typically use <code>/COPY:DATS</code> or <code>/COPYALL</code> to guarantee full permission fidelity.</p>

<h2>Configuring Network Resilience: Avoiding Default Hangs</h2>
<p>By default, if Robocopy encounters a locked file or temporary network disconnect, its default retry settings are catastrophic for automation:</p>
<ul>
    <li>Default Retries (<code>/R</code>): <strong>1,000,000 retries</strong></li>
    <li>Default Wait Time (<code>/W</code>): <strong>30 seconds</strong></li>
</ul>
<p>Under default settings, a single locked file causes Robocopy to stall for up to 347 days! In production scripts, always explicitly override these parameters:</p>

<div class="tutorial-command">
    <pre><code># Restrict retries to 3 attempts with a 5-second wait between attempts
robocopy C:\Source D:\Dest /R:3 /W:5</code></pre>
</div>

<h2>Production Migration Command Example</h2>
<p>A battle-tested production command for migrating enterprise file shares over an internal LAN:</p>

<div class="tutorial-command">
    <pre><code>robocopy "\\Server01\FinanceShare" "\\Server02\FinanceShare" *.* /E /COPYALL /ZB /MT:32 /R:3 /W:5 /FFT /V /TS /FP /NP /LOG:"C:\MigrationLogs\FinanceShare_Migration.log" /TEE</code></pre>
</div>

<p>Command breakdown:</p>
<ul>
    <li><code>/ZB</code>: Uses restartable mode; if access is denied, automatically falls back to administrative Backup Mode to bypass file locking.</li>
    <li><code>/MT:32</code>: Spawns 32 parallel worker threads for high-speed file transfers.</li>
    <li><code>/FFT</code>: Uses FAT file timing (2-second precision tolerance), preventing false-positive re-copies across heterogeneous network storage (e.g., Linux SMB/NAS).</li>
    <li><code>/LOG:... /TEE</code>: Writes detailed timestamps and full paths to a log file while simultaneously displaying summary output in the terminal.</li>
</ul>

<h2>Interpreting Robocopy Return Codes in Automation</h2>
<p>Unlike standard Windows utilities where an exit code of <code>0</code> is the only success indicator, Robocopy uses a <strong>bitmask return code</strong> architecture:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Exit Code</th>
                <th>Hex Bit</th>
                <th>Operational Meaning</th>
                <th>Script Evaluation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>0</strong></td>
                <td><code>0x00</code></td>
                <td>No errors occurred, but no files were copied (source and destination are already in sync).</td>
                <td>Success (Clean No-Op)</td>
            </tr>
            <tr>
                <td><strong>1</strong></td>
                <td><code>0x01</code></td>
                <td>One or more files were copied successfully.</td>
                <td><strong>Success</strong></td>
            </tr>
            <tr>
                <td><strong>2</strong></td>
                <td><code>0x02</code></td>
                <td>Extra files exist in destination that are not in source. No files failed.</td>
                <td>Success (Extras Present)</td>
            </tr>
            <tr>
                <td><strong>4</strong></td>
                <td><code>0x04</code></td>
                <td>Some mismatched files or directories were detected.</td>
                <td>Success (Mismatches Resolved)</td>
            </tr>
            <tr>
                <td><strong>8</strong></td>
                <td><code>0x08</code></td>
                <td>Several files failed to copy (access denied, file locked, network dropped).</td>
                <td><strong>Failure / Warning</strong></td>
            </tr>
            <tr>
                <td><strong>16</strong></td>
                <td><code>0x10</code></td>
                <td>Fatal error: Robocopy did not copy any files (invalid syntax, unreachable share).</td>
                <td><strong>Fatal Failure</strong></td>
            </tr>
        </tbody>
    </table>
</div>

<p>In PowerShell scripts, any exit code <strong>less than 8</strong> represents a successful execution:</p>

<div class="tutorial-command">
    <pre><code># Correct PowerShell error evaluation for Robocopy
robocopy "\\Source\Data" "D:\Data" /E /R:2 /W:2
$rc = $LASTEXITCODE

if ($rc -ge 8) {
    Write-Error "Robocopy failed with exit code $rc. Inspect migration log!"
} else {
    Write-Host "Robocopy completed successfully with status $rc." -ForegroundColor Green
}</code></pre>
</div>"""
    },
    {
        "id": "windows-active-directory-domain-join-prerequisites-workflow",
        "title": "Active Directory Domain Join: Prerequisites, DNS & Troubleshooting",
        "category": "Windows",
        "category_dir": "windows",
        "category_page": "windows.html",
        "level": "Intermediate",
        "description": "Master Windows Active Directory domain join architecture: DNS SRV record locator discovery, Kerberos time sync, Netlogon secure channel, and offline domain join with djoin.",
        "keywords": "active directory, domain join, dc locator, srv records, netlogon, secure channel, djoin, offline domain join, powershell, sysadmin",
        "html": r"""<p>In standalone enterprise environments, Windows workstations and servers operate within isolated Workgroups, relying strictly on their local Security Accounts Manager (SAM) database for user authentication. To transition an endpoint into an enterprise management fabric, the system must undergo an <strong>Active Directory Domain Join</strong>.</p>
<p>Joining an Active Directory domain establishes a mutual trust boundary between the endpoint and the domain: Kerberos single sign-on (SSO) is enabled, centralized Group Policy Objects (GPOs) are applied, and a machine account with a cryptographically rotated secure channel password is created in the directory.</p>

<h2>Architecture: The Domain Join Lifecycle</h2>
<p>When an administrator initiates a domain join, the operating system executes a strict multi-step cryptographic handshake across the network:</p>

<ol>
    <li><strong>DNS DC Locator Discovery:</strong> The client queries its configured DNS server for Active Directory Service Location (SRV) records: <code>_ldap._tcp.dc._msdcs.&lt;DomainName&gt;</code>.</li>
    <li><strong>LDAP Ping & Site Identification:</strong> The client sends an unauthenticated UDP LDAP ping to candidate Domain Controllers (DCs). The DCs respond with Netlogon details, informing the client of its Active Directory Site assignment.</li>
    <li><strong>Kerberos / NTLM Authentication:</strong> The client contacts the DC using the administrative credentials supplied by the user to authenticate admission rights.</li>
    <li><strong>Computer Object Provisioning:</strong> The DC creates or takes ownership of a <strong>Computer Object</strong> in the directory (by default inside the <code>CN=Computers</code> container, unless pre-staged in a designated Organizational Unit).</li>
    <li><strong>Secure Channel Password Generation:</strong> The client and DC negotiate a shared 120-character random password. This establishes the <strong>Netlogon Secure Channel</strong> used to encrypt machine-to-DC communication.</li>
    <li><strong>Local SAM Group Adjustment:</strong> The domain's <code>Domain Admins</code> group is automatically injected into the client's local <code>Administrators</code> group, and <code>Domain Users</code> is added to local <code>Users</code>.</li>
</ol>

<h2>Foundational Technical Prerequisites</h2>
<p>Domain join failures almost universally stem from deficiencies in foundational networking prerequisites:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Prerequisite Domain</th>
                <th>Technical Requirement</th>
                <th>Failure Consequence</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>DNS Configuration</strong></td>
                <td>Primary network adapter must point exclusively to AD Domain Controllers as primary DNS resolvers.</td>
                <td>Error <code>0x54B</code> (Domain does not exist or cannot be contacted) if client queries public DNS (8.8.8.8) that cannot resolve internal <code>_msdcs</code> zones.</td>
            </tr>
            <tr>
                <td><strong>Time Synchronization</strong></td>
                <td>Client system clock must match the Domain Controller within <strong>5 minutes (300 seconds)</strong>.</td>
                <td>Kerberos authentication fails with <code>KRB_AP_ERR_SKEW</code>; domain join is rejected due to replay attack prevention.</td>
            </tr>
            <tr>
                <td><strong>Network Port Egress</strong></td>
                <td>TCP/UDP 53 (DNS), TCP/UDP 88 (Kerberos), TCP/UDP 389 (LDAP), TCP 445 (SMB), TCP 135 (RPC Endpoint Mapper).</td>
                <td>RPC server unavailable or transport timeouts during machine account creation.</td>
            </tr>
            <tr>
                <td><strong>Account Permissions</strong></td>
                <td>Joining account must have <em>Create Computer Objects</em> permission in target container/OU.</td>
                <td>Access Denied (Error <code>0x5</code>) if the standard user has already reached their 10-machine join quota (<code>ms-DS-MachineAccountQuota</code>).</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Joining a Domain via PowerShell</h2>
<p>Modern administration automates domain onboarding using native PowerShell cmdlets:</p>

<div class="tutorial-command">
    <pre><code># 1. Verify DNS resolution of the Domain Controller's SRV records
Resolve-DnsName -Name "_ldap._tcp.dc._msdcs.corp.contoso.com" -Type SRV

# 2. Verify clock synchronization with the Domain Controller
w32tm /stripchart /computer:dc01.corp.contoso.com /samples:3 /dataonly

# 3. Join the domain and specify destination Organizational Unit (OU)
$credential = Get-Credential
Add-Computer -DomainName "corp.contoso.com" `
             -OUPath "OU=Workstations,OU=NYC,DC=corp,DC=contoso,DC=com" `
             -Credential $credential `
             -Restart</code></pre>
</div>

<h2>Offline Domain Join (ODJ) via djoin.exe</h2>
<p>In secure enterprise environments, systems administrators frequently deploy servers into isolated perimeter networks (DMZs), branch offices without network connectivity, or automated virtual machine templates. Active Directory supports <strong>Offline Domain Join (ODJ)</strong> using <code>djoin.exe</code>:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Phase</th>
                <th>Executed On</th>
                <th>Command & Action</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. Provisioning</strong></td>
                <td>Online Domain Controller</td>
                <td><code>djoin.exe /provision /domain corp.contoso.com /machine WEB-SRV-01 /savefile C:\ODJ\blob.txt</code><br>Creates computer account in AD and exports cryptographic metadata into a provisioning blob file.</td>
            </tr>
            <tr>
                <td><strong>2. Insertion</strong></td>
                <td>Offline Target Machine</td>
                <td><code>djoin.exe /requestODJ /loadfile C:\ODJ\blob.txt /windowspath %SystemRoot% /localos</code><br>Injects domain membership metadata and machine password into offline Windows image. Upon reboot and network connection, the system is fully domain-joined.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Diagnosing Common Domain Join Failures</h2>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Reported Error Message</th>
                <th>Root Cause Analysis</th>
                <th>Remediation Workflow</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>The specified domain either does not exist or could not be contacted (0x54B)</strong></td>
                <td>Client's network adapter is using external public DNS (e.g., home router or 1.1.1.1) or local firewall is blocking UDP port 53.</td>
                <td>Update IPv4/IPv6 DNS settings on adapter to point directly to the corporate domain controller. Validate with <code>nltest /dsgetdc:corp.contoso.com</code>.</td>
            </tr>
            <tr>
                <td><strong>Access is denied (0x5)</strong></td>
                <td>User account lacks administrative rights on local machine or exceeded the <code>ms-DS-MachineAccountQuota</code> in Active Directory.</td>
                <td>Pre-stage computer account in target OU with delegated permissions, or use a domain administrator account.</td>
            </tr>
            <tr>
                <td><strong>The trust relationship between this workstation and the primary domain failed</strong></td>
                <td>Machine account password desynchronized (e.g., computer restored from VM snapshot or inactive for 60+ days).</td>
                <td>Reset the secure channel from PowerShell: <code>Test-ComputerSecureChannel -Repair -Credential (Get-Credential)</code>.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Post-Join Validation Checklist</h2>
<ul>
    <li>Log in using domain credentials: <code>CORP\AdminUser</code>.</li>
    <li>Validate secure channel health: <code>Test-ComputerSecureChannel -Verbose</code>.</li>
    <li>Verify Group Policy processing: execute <code>gpresult /r</code> to confirm applied Computer and User policy GPOs.</li>
</ul>"""
    }
]
