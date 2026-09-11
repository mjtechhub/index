"""
MJ Tech Hub - Batch 4 Servers Tutorials Content
Topics:
1. windows-server-core-headless-deployment-and-remote-management
2. enterprise-dhcp-failover-load-balancing-and-hot-standby
3. windows-server-failover-clustering-wsfc-architecture
"""

SERVERS_TUTORIALS = [
    {
        "id": "windows-server-core-headless-deployment-and-remote-management",
        "title": "Windows Server Core: Headless Installation & Remote Administration",
        "category": "Servers",
        "category_dir": "servers",
        "category_page": "servers.html",
        "level": "Intermediate",
        "description": "Master headless Windows Server 2022/2025 administration: reduced attack surface, initial configuration with sconfig, Windows Admin Center (WAC), PowerShell Remoting, and RSAT.",
        "keywords": "windows server core, headless server, sconfig, windows admin center, winrm, powershell remoting, rsat, server administration, sysadmin",
        "html": r"""<p>When deploying Windows Server in production enterprise environments, the default installation choice historically included the graphical <strong>Desktop Experience</strong>. While a local GUI provides familiarity, running a full desktop shell on a production server introduces severe operational liabilities: it consumes 4+ GB of additional disk space, increases memory utilization, broadens the attack surface with hundreds of unnecessary binaries, and mandates frequent server reboots to patch non-critical desktop and graphics rendering libraries.</p>
<p>In modern enterprise infrastructure on <strong>Windows Server 2022 and Windows Server 2025</strong>, Microsoft's recommended production baseline is <strong>Server Core</strong>. Server Core provides a lean, headless operating system that eliminates the graphical desktop entirely, relying on modern remote administration tooling: <strong>Windows Admin Center (WAC)</strong>, <strong>PowerShell Remoting</strong>, and <strong>Remote Server Administration Tools (RSAT)</strong>.</p>

<h2>Architectural Benefits of Headless Server Core</h2>
<p>Deploying Server Core delivers measurable security and operational advantages over Desktop Experience:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Operational Metric</th>
                <th>Server with Desktop Experience</th>
                <th>Headless Server Core</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Disk Footprint</strong></td>
                <td>Requires ~15 GB – 25 GB base disk capacity.</td>
                <td>Requires ~6 GB – 10 GB (reduces baseline storage consumption by over 40%).</td>
            </tr>
            <tr>
                <td><strong>Memory Overhead</strong></td>
                <td>Desktop shell (Explorer), MMC, and GUI services consume 1.5 GB – 2 GB RAM at idle.</td>
                <td>Headless baseline consumes less than 512 MB – 800 MB RAM at idle.</td>
            </tr>
            <tr>
                <td><strong>Attack Surface</strong></td>
                <td>Includes Internet Explorer/Edge engines, multimedia codecs, font parsers, and Shell DLLs.</td>
                <td><strong>Stripped Minimal Surface:</strong> Only essential server subsystem binaries are present on disk.</td>
            </tr>
            <tr>
                <td><strong>Servicing Reboots</strong></td>
                <td>Frequent required reboots; majority of Windows monthly quality fixes target desktop shell libraries.</td>
                <td><strong>Significantly Fewer Reboots:</strong> Kernel and infrastructure updates only; higher uptime SLAs.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Initial Out-of-the-Box Configuration: sconfig</h2>
<p>Upon booting Server Core for the first time, administrators are greeted by a command prompt window running the <strong>Server Configuration tool (sconfig)</strong>:</p>

<div class="tutorial-command">
    <pre><code># Launch sconfig if closed accidentally
sconfig</code></pre>
</div>

<p>The text-based menu guides the administrator through mandatory foundational configuration tasks without requiring a GUI:</p>
<ul>
    <li><strong>Option 1: Domain/Workgroup:</strong> Joins the server to an Active Directory domain or assigns an isolated workgroup.</li>
    <li><strong>Option 2: Computer Name:</strong> Renames the default randomly generated machine name to corporate naming standards (e.g., <code>NYC-DC-01</code>).</li>
    <li><strong>Option 4: Configure Remote Management:</strong> Ensures Windows Remote Management (WinRM) is enabled to permit remote PowerShell and Server Manager connections.</li>
    <li><strong>Option 8: Network Settings:</strong> Configures static IPv4 addressing, subnet mask, default gateway, and DNS resolvers on primary network adapters.</li>
    <li><strong>Option 10: Telemetry Settings:</strong> Configures Windows Update servicing channels and download schedules.</li>
</ul>

<h2>Configuring Networking via PowerShell</h2>
<p>Administrators can automate post-installation configuration directly from the command line using native PowerShell cmdlets:</p>

<div class="tutorial-command">
    <pre><code># 1. Identify network adapter interface index (ifIndex)
Get-NetAdapter | Select-Object Name, InterfaceIndex, Status, LinkSpeed

# 2. Assign static IPv4 address and default gateway to interface index 2
New-NetIPAddress -InterfaceIndex 2 -IPAddress 10.10.10.15 -PrefixLength 24 -DefaultGateway 10.10.10.1

# 3. Configure primary and secondary Active Directory DNS servers
Set-DnsClientServerAddress -InterfaceIndex 2 -ServerAddresses ("10.10.10.10", "10.10.10.11")

# 4. Join the server to the corporate Active Directory domain and reboot
Add-Computer -DomainName "corp.contoso.com" -Restart</code></pre>
</div>

<h2>The Modern Remote Administration Stack</h2>
<p>Operating Server Core does not mean living in a local console window. Production environments manage Server Core nodes through four remote administration vectors:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Administration Tool</th>
                <th>Management Protocol</th>
                <th>Primary Administrative Use Case</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Windows Admin Center (WAC)</strong></td>
                <td>HTTPS (Port 443) / PowerShell / WMI</td>
                <td>Modern browser-based single-pane gateway: manages certificates, events, storage, performance graphs, firewall rules, and virtual machines without installing GUI agents on the server.</td>
            </tr>
            <tr>
                <td><strong>PowerShell Remoting</strong></td>
                <td>WinRM (HTTP 5985 / HTTPS 5986)</td>
                <td>Automated command execution and interactive CLI sessions (<code>Enter-PSSession</code>, <code>Invoke-Command</code>).</td>
            </tr>
            <tr>
                <td><strong>Server Manager Console</strong></td>
                <td>WMI / DCOM / WinRM</td>
                <td>Centralized multi-server console on admin workstations to install roles, inspect service states, and monitor events.</td>
            </tr>
            <tr>
                <td><strong>RSAT (Remote MMC Tools)</strong></td>
                <td>RPC / LDAP / Kerberos</td>
                <td>Native MMC snap-ins (Active Directory Users and Computers, DNS Manager, DHCP Console) running on admin workstations targeting the headless server.</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="tutorial-callout callout-note">
    <p><strong>WinRM Protocol Dynamics: HTTP 5985 vs HTTPS 5986:</strong></p>
    <p>PowerShell Remoting operates over the Windows Remote Management (WinRM) service, listening on <strong>TCP port 5985 (HTTP)</strong> and <strong>TCP port 5986 (HTTPS)</strong>. It is an architectural misconception that remoting over HTTP/5985 transmits plaintext commands:</p>
    <ul>
        <li><strong>Message-Level Encryption on HTTP (Port 5985):</strong> WinRM encrypts PowerShell Remoting communication after authentication has completed. HTTP/5985 does not mean unencrypted traffic; rather, it uses message-level encryption negotiated by the authentication protocol. Kerberos is normally used for domain computer-name connections, and modern Kerberos environments commonly use AES-based encryption to cryptographically protect the remoting payload. When NTLM is negotiated instead (such as IP-address connections or non-domain scenarios), NTLM provides its own distinct message protection characteristics. Therefore, HTTP/5985 is not inherently plaintext PowerShell Remoting traffic after authentication.</li>
        <li><strong>TLS Transport Protection on HTTPS (Port 5986):</strong> Establishing an HTTPS listener provides full TLS transport-layer protection, requiring a valid X.509 certificate (issued by an enterprise PKI or trusted CA) bound to the WinRM service. HTTPS is appropriate and recommended for untrusted workgroup connections, cross-forest administration, or public/DMZ scenarios where Kerberos mutual authentication is unavailable and TLS is needed to validate host identity.</li>
    </ul>
    <p><strong>Architectural Decision:</strong> Administrators should choose between HTTP/5985 and HTTPS/5986 based on trust boundaries, authentication mechanisms, and deployment architecture: trusted Active Directory domain workloads commonly leverage default HTTP/5985 with Kerberos message encryption, while untrusted or perimeter boundaries deploy HTTPS/5986 with TLS.</p>
</div>

<h2>Installing Server Roles via PowerShell</h2>
<p>Roles and features are provisioned on Server Core using the <code>ServerManager</code> PowerShell module:</p>

<div class="tutorial-command">
    <pre><code># 1. Query available roles on the Server Core host
Get-WindowsFeature -Name *DHCP*, *DNS*, *AD* | Select-Object Name, DisplayName, InstallState

# 2. Install Active Directory Domain Services with management tools
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools

# 3. Install DNS Server role and failover clustering
Install-WindowsFeature -Name DNS, Failover-Clustering -IncludeManagementTools</code></pre>
</div>

<div class="tutorial-callout callout-important">
    <p><strong>Supported Roles on Server Core:</strong> Server Core supports all foundational infrastructure roles, including AD DS, DNS, DHCP, Hyper-V, File & Storage Services, IIS Web Server, and Failover Clustering. However, legacy software that strictly relies on desktop APIs or SQL Server Reporting Services may require Desktop Experience or containerized deployment.</p>
</div>"""
    },
    {
        "id": "enterprise-dhcp-failover-load-balancing-and-hot-standby",
        "title": "Windows Server DHCP Failover: Load Balance vs Hot Standby Modes",
        "category": "Servers",
        "category_dir": "servers",
        "category_page": "servers.html",
        "level": "Intermediate",
        "description": "Master Windows Server DHCP high availability: Load Balance vs Hot Standby modes, Maximum Client Lead Time (MCLT), partner communication states, and DHCPv4 scope replication.",
        "keywords": "dhcp failover, windows server dhcp, load balance, hot standby, mclt, scope replication, high availability, server administration, sysadmin",
        "html": r"""<p>In enterprise local area networks, Dynamic Host Configuration Protocol (DHCP) is a mission-critical infrastructure dependency: if DHCP servers become unreachable, endpoints cannot renew IP addresses, lose default gateway routing, fail to resolve DNS names, and drop off corporate networks entirely. Historically, administrators achieved redundancy through "split-scope" designs (e.g., Server A handles 80% of the pool, Server B handles 20%) or complex clustered storage instances.</p>
<p>Modern enterprise IP resiliency on Windows platforms relies on native <strong>Windows Server DHCP Failover</strong> (RFC 3074). Built directly into the DHCP Server role on Windows Server, DHCP Failover enables two standalone DHCP servers to share a common subnet scope, synchronize lease states in real-time, and provide seamless, zero-downtime failover without requiring shared SAN storage or failover clustering.</p>

<h2>Failover Modes: Load Balance vs Hot Standby</h2>
<p>When configuring a failover relationship between two Windows Server DHCP partners, administrators must select between two distinct architectural modes:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Operational Dimension</th>
                <th>Load Balance Mode (Active-Active)</th>
                <th>Hot Standby Mode (Active-Passive)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Primary Deployment Topology</strong></td>
                <td>Single physical site where both DHCP servers reside on high-speed low-latency corporate subnets.</td>
                <td>Hub-and-spoke or multi-site topology where the Active server is local and the Standby partner is located in a central data center.</td>
            </tr>
            <tr>
                <td><strong>Traffic Handling</strong></td>
                <td><strong>Active-Active:</strong> Both partner servers actively respond to client DHCPDISCOVER and DHCPREQUEST messages simultaneously.</td>
                <td><strong>Active-Passive:</strong> The Primary server serves 100% of client leases under normal conditions. The Secondary server remains passive.</td>
            </tr>
            <tr>
                <td><strong>Load Distribution</strong></td>
                <td>Determined by a deterministic hash of the client's MAC address (RFC 3074). Default split is <strong>50% / 50%</strong> (configurable, e.g., 70/30).</td>
                <td>Primary serves all traffic; Standby maintains a configurable <strong>Reserve Pool</strong> (default 5% of scope) for temporary leases during an outage.</td>
            </tr>
            <tr>
                <td><strong>WAN Sensitivity</strong></td>
                <td>Requires low latency (&lt; 10 ms) between partners for synchronized hashing.</td>
                <td>Resilient across higher-latency WAN connections between branch offices and data centers.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>The Failover State Machine & Maximum Client Lead Time (MCLT)</h2>
<p>DHCP Failover partners communicate continuously over <strong>TCP port 647</strong> to synchronize lease database modifications. The resiliency of the relationship is governed by the <strong>Maximum Client Lead Time (MCLT)</strong> parameter (default: 1 hour):</p>

<ol>
    <li><strong>Normal State:</strong> Both partners communicate over TCP 647. Whenever Server A grants or renews an IP lease, it sends a binding update (BNDUPD) to Server B, which acknowledges the update (BNDACK). Both lease tables remain synchronized.</li>
    <li><strong>Communication-Interrupted State:</strong> If Server A loses network connectivity to Server B, Server B transitions to <code>COMMUNICATION-INTERRUPTED</code>. Server B does not know if Server A has crashed or if a temporary network partition occurred. To prevent granting duplicate IP addresses, Server B issues new leases and renewals strictly for the duration of the <strong>MCLT</strong> (e.g., 1 hour), rather than the full scope lease time (e.g., 8 days).</li>
    <li><strong>Partner-Down State:</strong> If an administrator or automated script confirms that Server A has physically crashed and will not return, Server B is transitioned into <code>PARTNER-DOWN</code>. Server B waits for the MCLT timer to expire (ensuring all existing client leases expire or renew), and then takes over <strong>100% of the entire scope pool</strong>, serving full-duration leases.</li>
</ol>

<div class="tutorial-callout callout-important">
    <p><strong>Critical Scope Limitation: IPv4 Only:</strong> Windows Server DHCP Failover is supported <strong>exclusively for DHCPv4 scopes</strong>. Microsoft DHCP Server does <em>not</em> support failover relationships for DHCPv6 scopes. For IPv6 environments, high availability is achieved natively via router advertisements (SLAAC) or deploying independent stateless DHCPv6 servers.</p>
</div>

<h2>Configuring Windows Server DHCP Failover via PowerShell</h2>
<p>Systems administrators configure, replicate, and manage DHCP failover relationships using the native <code>DhcpServer</code> module:</p>

<div class="tutorial-command">
    <pre><code># 1. Create a Load Balance failover relationship between DC1 and DC2 for subnet 10.10.10.0
Add-DhcpServerv4Failover -ComputerName "DC1.corp.contoso.com" `
    -Name "DC1-DC2-Failover" `
    -PartnerServer "DC2.corp.contoso.com" `
    -ScopeId 10.10.10.0 `
    -Mode LoadBalance `
    -LoadPercent 50 `
    -MaxClientLeadTime 01:00:00 `
    -SharedSecret "ComplexClusterSecretP@ss2026" `
    -AutoStateTransition $True `
    -StateSwitchInterval 00:30:00

# 2. Alternatively, create a Hot Standby relationship for branch site 10.20.10.0
# DC1 is Active Primary; DC2 is Standby holding 10% reserve capacity
Add-DhcpServerv4Failover -ComputerName "DC1.corp.contoso.com" `
    -Name "DC1-DC2-BranchStandby" `
    -PartnerServer "DC2.corp.contoso.com" `
    -ScopeId 10.20.10.0 `
    -Mode HotStandby `
    -ServerRole Active `
    -ReservePercent 10 `
    -MaxClientLeadTime 01:00:00 `
    -SharedSecret "ComplexClusterSecretP@ss2026"

# 3. Manually replicate scope configuration updates from Primary to Partner
Invoke-DhcpServerv4FailoverReplication -ComputerName "DC1.corp.contoso.com"</code></pre>
</div>

<h2>Auditing and Monitoring Failover Health</h2>
<p>To inspect active partnership health and verify that lease synchronization is operational:</p>

<div class="tutorial-command">
    <pre><code># Query active failover relationship operational states
Get-DhcpServerv4Failover -ComputerName "DC1.corp.contoso.com" | Format-List Name, Mode, ServerRole, State, PartnerState

# Inspect active lease counts and scope allocation across both failover partners
Get-DhcpServerv4ScopeStatistics -ComputerName "DC1.corp.contoso.com" -ScopeId 10.10.10.0</code></pre>
</div>
<p>Verify that both <code>State</code> and <code>PartnerState</code> report <code>Normal</code>, and ensure that TCP port 647 is permitted through local host firewalls on both Domain Controllers.</p>"""
    },
    {
        "id": "windows-server-failover-clustering-wsfc-architecture",
        "title": "Windows Server Failover Clustering (WSFC) Architecture & Validation Tests",
        "category": "Servers",
        "category_dir": "servers",
        "category_page": "servers.html",
        "level": "Intermediate",
        "description": "Master enterprise high availability clustering: WSFC nodes, quorum models, witness types (Cloud/File Share/Disk), Cluster Validation Wizard, and stateful workload failover.",
        "keywords": "wsfc, failover clustering, windows server cluster, quorum, cloud witness, file share witness, cluster validation, high availability, sysadmin",
        "html": r"""<p>In enterprise IT operations, mission-critical workloads such as database management systems (Microsoft SQL Server), hypervisors (Hyper-V), and file repositories cannot tolerate single points of physical failure. When a physical server motherboard fails, a power supply blows, or kernel hardware errors trigger an unplanned restart, underlying infrastructure must detect the node failure and orchestrate automated workload migration in seconds.</p>
<p>On the Microsoft platform, this capability is delivered by <strong>Windows Server Failover Clustering (WSFC)</strong>. WSFC connects independent physical or virtual servers (called <strong>nodes</strong>) into a resilient multi-node cluster, providing automated failure detection, state synchronization, distributed lock management, and planned maintenance orchestration.</p>

<h2>WSFC Core Architecture & Communication Dynamics</h2>
<p>A Windows Server Failover Cluster relies on coordinated interaction across several foundational subsystems:</p>

<ul>
    <li><strong>Cluster Nodes:</strong> Up to 64 physical or virtual Windows Server nodes joined to an Active Directory domain, sharing identical OS patch levels and CPU architectures.</li>
    <li><strong>Cluster Heartbeats:</strong> Nodes transmit continuous UDP heartbeats over <strong>UDP port 3343</strong> across all cluster networks. If a node fails to respond to heartbeats within a configurable threshold (default: 5 consecutive missed heartbeats across 5 seconds on same-subnet clusters), the cluster declares the node dead and initiates workload failover.</li>
    <li><strong>Cluster IP & Name (Cluster Name Object - CNO):</strong> The cluster presents a unified virtual hostname and IP address in Active Directory and DNS, providing a single point of administrative contact regardless of which physical node holds active roles.</li>
    <li><strong>Cluster Shared Volumes (CSV):</strong> In Hyper-V and Scale-Out File Server deployments, CSV allows all cluster nodes simultaneous read and write access to the same shared SAN LUN or storage pool, eliminating disk ownership unmount/remount delays during VM migration.</li>
</ul>

<h2>Quorum Architecture: Preventing Cluster Split-Brain</h2>
<p>The most critical mathematical construct in clustering is <strong>Quorum</strong>. If a network partition severs communication between nodes (e.g., East Data Center loses WAN connection to West Data Center), both isolated groups of nodes might independently assume the other side has died. If both sides attempt to bring the same SQL databases or storage volumes online, catastrophic data corruption (known as <strong>Split-Brain</strong>) occurs.</p>
<p>WSFC prevents split-brain using a <strong>Majority Voting Model (50% + 1 votes)</strong>. A cluster can only remain online and service workloads if a strict majority of voting members are active and communicating:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Witness Typology</th>
                <th>Storage / Network Dependency</th>
                <th>Operational Mechanism</th>
                <th>Recommended Deployment Scenario</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Cloud Witness</strong></td>
                <td>Direct HTTPS (Port 443) outbound to Microsoft Azure Blob Storage.</td>
                <td>Writes a lightweight timestamp token to an Azure Blob container. Acts as an external tie-breaker vote with zero on-premises storage footprint.</td>
                <td><strong>Recommended Modern Default:</strong> Multi-site clusters, branch offices, clusters with Internet connectivity.</td>
            </tr>
            <tr>
                <td><strong>File Share Witness (FSW)</strong></td>
                <td>Standard SMB file share located on an independent server outside the cluster.</td>
                <td>Maintains a <code>witness.log</code> lock file on the file share to claim a tie-breaking vote.</td>
                <td>Air-gapped, isolated enterprise enclaves without public cloud access.</td>
            </tr>
            <tr>
                <td><strong>Disk Witness</strong></td>
                <td>Dedicated shared LUN on enterprise SAN storage (minimum 512 MB).</td>
                <td>Uses SCSI-3 Persistent Reservations (PR) to lock the shared disk and claim a vote.</td>
                <td>Traditional single-site SAN data center deployments.</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="tutorial-callout callout-note">
    <p><strong>Dynamic Quorum & Dynamic Witness:</strong> Modern Windows Server clustering automatically calculates dynamic votes. If an administrator gracefully shuts down Node 3 for hardware maintenance, the cluster automatically decrements the total voting weight from 5 down to 4, recalculating the quorum majority threshold dynamically so future unplanned failures can still achieve quorum.</p>
</div>

<h2>The Mandatory Cluster Validation Wizard</h2>
<p>Before creating a cluster or opening a support ticket with Microsoft, administrators must execute the <strong>Cluster Validation Wizard</strong> (<code>Test-Cluster</code>). The validation suite executes hundreds of rigorous diagnostic probes across four categories:</p>

<ol>
    <li><strong>System Configuration:</strong> Validates OS build numbers, hotfixes, Active Directory domain architecture, and system software compatibility.</li>
    <li><strong>Networking:</strong> Verifies that nodes possess redundant network paths, tests UDP 3343 heartbeat latency, checks IPv4/IPv6 binding orders, and ensures network adapters are on independent subnets.</li>
    <li><strong>Storage:</strong> Executes non-destructive SCSI-3 Persistent Reservation tests, verifies multi-path I/O (MPIO) configurations, and measures disk latency across all nodes.</li>
    <li><strong>Hardware:</strong> Ensures CPU stepping, virtualization extensions, and memory sizing are consistent across nodes.</li>
</ol>

<div class="tutorial-callout callout-important">
    <p><strong>Application Cluster-Awareness Requirement:</strong> WSFC provides high-availability infrastructure, but WSFC itself does <em>not</em> automatically make arbitrary third-party software highly available. Applications must be explicitly written to be <strong>cluster-aware</strong> (such as SQL Server FCI, Exchange DAG, Hyper-V, or File Services) to support automated state synchronization and transactional failover.</p>
</div>

<h2>Automating Cluster Deployment via PowerShell</h2>
<p>Systems administrators can validate, create, and inspect failover clusters using PowerShell:</p>

<div class="tutorial-command">
    <pre><code># 1. Execute the comprehensive Cluster Validation suite across two prospective nodes
Test-Cluster -Node "NODE1.corp.contoso.com", "NODE2.corp.contoso.com" -Include "Storage", "Network", "System Configuration"

# 2. Inspect the generated HTML validation report to confirm zero errors:
# Output saved to: C:\Windows\Cluster\Reports\Validation Report &lt;timestamp&gt;.html

# 3. Create the Failover Cluster with static IP and dedicated Cluster Name Object (CNO)
New-Cluster -Name "NYC-HA-CL01" `
    -Node "NODE1.corp.contoso.com", "NODE2.corp.contoso.com" `
    -StaticAddress "10.10.10.100"

# 4. Configure an Azure Cloud Witness as the tie-breaking quorum vote
Set-ClusterQuorum -CloudWitness `
    -AccountName "contosoclusterstorage" `
    -AccessKey "SecureStorageAccountKeyGeneratedFromAzurePortal==" `
    -Endpoint "core.windows.net"</code></pre>
</div>

<h2>Monitoring Cluster Quorum and Node Health</h2>
<p>To inspect active cluster node states, quorum votes, and network health:</p>

<div class="tutorial-command">
    <pre><code># Query node operational states and assigned dynamic quorum votes
Get-ClusterNode | Select-Object Name, State, DynamicWeight, NodeWeight

# Inspect active quorum model and witness health
Get-ClusterQuorum | Select-Object QuorumType, QuorumResource

# List all cluster networks and their assigned roles (ClusterOnly, ClusterAndClient)
Get-ClusterNetwork | Select-Object Name, Subnet, Metric, Role</code></pre>
</div>
<p>Confirm that all nodes report state <code>Up</code> and that <code>QuorumType</code> displays <code>Majority</code> with an active Cloud or File Share Witness.</p>"""
    }
]
