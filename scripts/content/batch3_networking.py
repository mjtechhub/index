"""
MJ Tech Hub - Batch 3 Networking Tutorials Content
Topics:
1. wireless-access-points-and-controllers-wlc
2. ipv6-addressing-and-slaac
3. snmp-v2c-vs-v3-security-and-usm
"""

NETWORKING_TUTORIALS = [
    {
        "id": "wireless-access-points-and-controllers-wlc",
        "title": "Wireless Access Points, CAPWAP & WLC Architecture",
        "category": "Networking",
        "category_dir": "networking",
        "category_page": "networking.html",
        "level": "Intermediate",
        "description": "Understand enterprise Wi-Fi: Autonomous vs Lightweight APs (LAP), CAPWAP control and data tunneling, and centralized Wireless LAN Controller (WLC) deployments.",
        "keywords": "wireless, wlc, capwap, access point, lap, autonomous ap, split-mac, 802.11, enterprise wifi, networking",
        "html": r"""<p>In consumer home environments, Wi-Fi is provided by an all-in-one integrated router, switch, and wireless access point. However, attempting to scale enterprise campus connectivity by deploying dozens of standalone, uncoordinated access points creates severe operational friction: channel interference, dropped roaming handoffs, inconsistent security policies, and unmanageable configuration overhead.</p>
<p>Modern enterprise wireless networks solve these scaling challenges by decoupling wireless radio management from centralized policy control through the <strong>Split-MAC Architecture</strong>, using <strong>Lightweight Access Points (LAPs)</strong> and <strong>Wireless LAN Controllers (WLCs)</strong> interconnected by the <strong>CAPWAP protocol</strong>.</p>

<h2>Autonomous vs Lightweight Access Points (Split-MAC)</h2>
<p>The transition from legacy standalone APs to modern controller-based architectures hinges on how IEEE 802.11 MAC-layer functions are divided between physical access points and central controllers:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>MAC Layer Function</th>
                <th>Autonomous AP Architecture</th>
                <th>Split-MAC (LAP + WLC) Architecture</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Real-Time MAC (RF Frame Handling)</strong></td>
                <td>Handled locally by the AP hardware.</td>
                <td><strong>Handled locally by the LAP:</strong> Beacon generation, probe responses, frame acknowledgment (ACK), frame buffering, and 802.11 physical encryption.</td>
            </tr>
            <tr>
                <td><strong>Management & Control MAC</strong></td>
                <td>Handled locally on each AP (requires manual per-device configuration).</td>
                <td><strong>Handled centrally by the WLC:</strong> 802.1X EAP authentication, association processing, dynamic radio resource management (RRM), roaming coordination, and QoS policy enforcement.</td>
            </tr>
            <tr>
                <td><strong>Configuration Management</strong></td>
                <td>Decentralized; each AP has its own IP, CLI, web interface, and configuration file.</td>
                <td>Centralized; APs download firmware and configuration dynamically from the WLC upon boot.</td>
            </tr>
            <tr>
                <td><strong>VLAN Trunking</strong></td>
                <td>Requires trunking all client VLANs directly to the physical switch port of every AP.</td>
                <td>Switch ports connecting LAPs only require access to an AP-management VLAN. Client traffic is encapsulated in CAPWAP back to the WLC.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>The CAPWAP Protocol: Control and Data Tunnels</h2>
<p>Lightweight APs communicate with the Wireless LAN Controller using <strong>Control and Provisioning of Wireless Access Points (CAPWAP, RFC 5415/5416)</strong>. CAPWAP operates over UDP and establishes two separate encrypted or encapsulated tunnels:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>CAPWAP Tunnel Type</th>
                <th>UDP Port</th>
                <th>Security / Encryption</th>
                <th>Operational Traffic Carried</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>CAPWAP Control</strong></td>
                <td><strong>UDP 5246</strong></td>
                <td>Encrypted with <strong>DTLS</strong> (Datagram Transport Layer Security) using X.509 digital certificates installed in hardware.</td>
                <td>AP configuration commands, firmware updates, Radio Resource Management (RRM) telemetry, channel assignment, and AP keepalive heartbeats.</td>
            </tr>
            <tr>
                <td><strong>CAPWAP Data</strong></td>
                <td><strong>UDP 5247</strong></td>
                <td>Optional DTLS encryption (unencrypted by default for wire-speed performance).</td>
                <td>Encapsulated 802.11 wireless client data frames transmitted between the AP and the WLC.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>WLC Traffic Modes: Centralized vs FlexConnect</h2>
<p>Enterprises deploy WLC architectures in two primary topologies based on branch office WAN constraints:</p>

<h3>1. Centralized (Local Mode)</h3>
<p>The default enterprise campus mode. All client wireless traffic received by the LAP is encapsulated into CAPWAP Data frames and tunneled across the internal network back to the centralized WLC. The WLC terminates the tunnel, extracts the 802.3 Ethernet frames, and switches them onto the local core network VLANs. This ensures centralized firewalling, deep packet inspection, and uniform security policy enforcement.</p>

<h3>2. FlexConnect (formerly H-REAP)</h3>
<p>Engineered for remote branch offices separated from the corporate data center by WAN or internet links. In FlexConnect mode, the LAP locally switches wireless client traffic directly onto the branch office's physical switch ports without hair-pinning traffic back across the WAN. Furthermore, if the WAN link drops and connectivity to the central WLC is lost, branch clients can continue communicating locally with local file servers and printers without interruption.</p>

<div class="callout callout-important">
    <div class="callout-title"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i> The AP Boot & Discovery Sequence</div>
    <div class="callout-body">When a Lightweight AP powers on via Power-over-Ethernet (PoE), it executes a strict sequence to join its WLC:
    <ol>
        <li>Obtains an IP address, subnet mask, and default gateway via DHCP.</li>
        <li>Discovers the WLC IP via <strong>DHCP Option 43</strong>, DNS query for <code>CISCO-CAPWAP-CONTROLLER.localdomain</code>, or local subnet broadcast.</li>
        <li>Establishes a DTLS handshake with the WLC to validate mutual certificates.</li>
        <li>Downloads matching firmware image from the WLC if versions differ.</li>
        <li>Registers and downloads runtime radio configurations (SSIDs, transmit power, channels).</li>
    </ol>
    </div>
</div>

<h2>Radio Resource Management (RRM)</h2>
<p>One of the greatest operational advantages of a centralized WLC is <strong>Dynamic Radio Resource Management</strong>:</p>
<ul>
    <li><strong>Dynamic Channel Assignment (DCA):</strong> The WLC monitors RF interference and automatically redistributes channels across APs to prevent co-channel interference.</li>
    <li><strong>Transmit Power Control (TPC):</strong> Automatically adjusts AP radio wattage to eliminate Wi-Fi dead zones while preventing signal bleed into adjacent office areas.</li>
    <li><strong>Coverage Hole Detection and Mitigation (CHDM):</strong> If an AP detects that several client devices are communicating at low signal-to-noise ratios (SNR), the WLC instructs surrounding APs to increase radio power to cover the gap.</li>
</ul>

<h2>Summary</h2>
<p>The enterprise shift from autonomous APs to centralized WLC and CAPWAP architectures enables scalable wireless operations. By delegating real-time RF processing to lightweight access points and centralizing security, policy, and radio management on controllers, enterprise networks achieve seamless client roaming, robust policy enforcement, and autonomous RF optimization.</p>"""
    },
    {
        "id": "ipv6-addressing-and-slaac",
        "title": "IPv6 Addressing, SLAAC & Global Unicast Architecture",
        "category": "Networking",
        "category_dir": "networking",
        "category_page": "networking.html",
        "level": "Intermediate",
        "description": "Master enterprise IPv6 fundamentals: 128-bit address representation, address scopes, Stateless Address Autoconfiguration (SLAAC), and ICMPv6 Neighbor Discovery.",
        "keywords": "ipv6, slaac, icmpv6, global unicast, link local, ndp, dual stack, networking, subnetting, eui-64",
        "html": r"""<p>The exhaustion of the 32-bit IPv4 address space—which provides only approximately 4.3 billion unique public addresses—has made modern enterprise networking increasingly complex. While Network Address Translation (NAT) extended the lifespan of IPv4 by allowing thousands of internal hosts to hide behind a single public IP, NAT breaks end-to-end network transparency, complicates peer-to-peer applications, and introduces stateful tracking overhead on firewalls.</p>
<p><strong>Internet Protocol version 6 (IPv6)</strong> resolves the address exhaustion crisis with a <strong>128-bit address space</strong>, providing 340 undecillion ($3.4 \times 10^{38}$) unique addresses. Beyond address abundance, IPv6 introduces cleaner packet headers, eliminates broadcast traffic, and features automated, stateless address configuration.</p>

<h2>IPv6 Address Representation and Compression Rules</h2>
<p>An IPv6 address is written as eight groups of four hexadecimal digits (16 bits per group, known as a <strong>hextet</strong>), separated by colons:</p>
<div class="command-header"><span class="command-label">Uncompressed 128-Bit IPv6 Address</span></div>
<pre><code>2001:0db8:0000:0000:0000:0000:0042:0001</code></pre>

<p>To make addresses manageable for network administrators, RFC 5952 establishes two mandatory compression rules:</p>
<ol>
    <li><strong>Omit Leading Zeros:</strong> Within any 16-bit hextet, leading zeros can be omitted. (e.g. <code>:0db8:</code> becomes <code>:db8:</code>, and <code>:0042:</code> becomes <code>:42:</code>).</li>
    <li><strong>Compress Consecutive Hextets of Zeros (Double Colon <code>::</code>):</strong> A single contiguous sequence of one or more all-zero hextets can be replaced with a double colon (<code>::</code>). <strong>This rule can only be applied once per address</strong> to preserve mathematical reversibility.</li>
</ol>

<div class="command-header"><span class="command-label">Properly Compressed Representation</span></div>
<pre><code>2001:db8::42:1</code></pre>

<h2>Core IPv6 Address Scopes</h2>
<p>Unlike IPv4 where an interface typically possesses only a single IP address, an IPv6-enabled interface simultaneously maintains multiple addresses across distinct <strong>Address Scopes</strong>:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Address Scope Type</th>
                <th>Prefix / Range</th>
                <th>Scope & Operational Purpose</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Global Unicast Address (GUA)</strong></td>
                <td><code>2000::/3</code> (typically <code>2001::</code> or <code>2002::</code>)</td>
                <td>Publicly routable across the global internet (analogous to public IPv4). Every host with a GUA has direct, end-to-end connectivity without NAT.</td>
            </tr>
            <tr>
                <td><strong>Link-Local Address (LLA)</strong></td>
                <td><code>fe80::/10</code> (commonly <code>fe80::/64</code>)</td>
                <td>Mandatory on every IPv6 interface. Used strictly for local communications on the physical link (same broadcast domain/VLAN). <strong>Never routed by routers.</strong> Used for neighbor discovery, routing protocol peering (OSPFv3, BGP), and default gateway next-hops.</td>
            </tr>
            <tr>
                <td><strong>Unique Local Address (ULA)</strong></td>
                <td><code>fc00::/7</code> (commonly <code>fd00::/8</code>)</td>
                <td>Routable only within an enterprise organization or private VPN fabric. Analogous to RFC 1918 private IPv4 space (10.0.0.0/8). Not routable on the public internet.</td>
            </tr>
            <tr>
                <td><strong>Multicast</strong></td>
                <td><code>ff00::/8</code></td>
                <td>Used to deliver packets to multiple destinations simultaneously. Replaces IPv4 broadcast. (e.g. <code>ff02::1</code> = All Nodes on link, <code>ff02::2</code> = All Routers on link).</td>
            </tr>
            <tr>
                <td><strong>Loopback</strong></td>
                <td><code>::1/128</code></td>
                <td>Local host software loopback (analogous to 127.0.0.1).</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Global Unicast Address (GUA) Structure</h2>
<p>A standard enterprise Global Unicast address conforms to a clean, hierarchical structure:</p>
<ul>
    <li><strong>Global Routing Prefix (typically <code>/48</code>):</strong> Assigned by the upstream ISP or Regional Internet Registry (RIR) to identify the specific enterprise organization.</li>
    <li><strong>Subnet ID (16 bits, extending prefix to <code>/64</code>):</strong> Managed by internal network engineers to allocate up to 65,536 distinct subnets within the enterprise.</li>
    <li><strong>Interface ID (64 bits):</strong> Identifies the specific host interface on that subnet (generated via SLAAC, random generation, or manual assignment).</li>
</ul>

<div class="callout callout-important">
    <div class="callout-title"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i> The Golden Rule: Always Use /64 Subnets</div>
    <div class="callout-body">In IPv6, end-user subnets must always be sized as <strong><code>/64</code></strong>. While variable-length subnetting is mathematically possible, breaking the <code>/64</code> boundary breaks core automated features including Stateless Address Autoconfiguration (SLAAC) and Mobile IPv6.</div>
</div>

<h2>Stateless Address Autoconfiguration (SLAAC) & NDP</h2>
<p>IPv6 eliminates dependency on a dedicated DHCP server through <strong>Stateless Address Autoconfiguration (SLAAC)</strong>, governed by the <strong>Neighbor Discovery Protocol (NDP)</strong> running over ICMPv6:</p>

<ol>
    <li><strong>Router Solicitation (RS - ICMPv6 Type 133):</strong> Upon link initialization, the host generates its Link-Local address (<code>fe80::...</code>) and multicasts an RS packet to <code>ff02::2</code> (All-Routers) asking local routers for subnet parameters.</li>
    <li><strong>Router Advertisement (RA - ICMPv6 Type 134):</strong> The local router replies with an RA packet (sent to <code>ff02::1</code> All-Nodes) containing:
        <ul>
            <li>The 64-bit network prefix (e.g. <code>2001:db8:acad:1::/64</code>).</li>
            <li>Default gateway link-local address.</li>
            <li>Address lifecycle timers (Preferred and Valid lifetimes).</li>
            <li>Configuration flags (e.g. <strong>M-flag</strong> for Managed DHCPv6 or <strong>O-flag</strong> for Other DNS options via Stateless DHCPv6).</li>
        </ul>
    </li>
    <li><strong>Interface ID Generation:</strong> The host combines the advertised <code>/64</code> prefix with its own 64-bit Interface ID. This can be derived from the hardware MAC address using the legacy <strong>Modified EUI-64</strong> process (inverting the 7th bit and inserting <code>FF:FE</code> into the center), or modern privacy extensions (RFC 4941 / RFC 7217) which generate stable, cryptographically randomized Interface IDs to prevent physical device tracking.</li>
    <li><strong>Duplicate Address Detection (DAD):</strong> Before activating the new address, the host sends a Neighbor Solicitation (NS) for its own candidate address. If no Neighbor Advertisement (NA) is received within the timeout, the host confirms the address is unique and begins transmission.</li>
</ol>

<h2>Inspecting IPv6 Configuration on Hosts</h2>
<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Linux / macOS (Bash)</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code>ip -6 addr show dev eth0</code></pre>
</div>

<div class="command-header"><span class="command-label">Example Output</span></div>
<pre><code>2: eth0: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 state UP qlen 1000
    inet6 2001:db8:acad:1:5054:ff:fe12:3456/64 scope global dynamic mngtmpaddr 
       valid_lft 86395sec preferred_lft 14395sec
    inet6 fe80::5054:ff:fe12:3456/64 scope link 
       valid_lft forever preferred_lft forever</code></pre>

<h2>Summary</h2>
<p>IPv6 is far more than an expanded address space. By structuring networks around clean <code>/64</code> subnets, leveraging distinct Link-Local scopes for local router interactions, and employing ICMPv6 Neighbor Discovery for automatic SLAAC provisioning, IPv6 establishes an efficient, scalable, and NAT-free networking architecture.</p>"""
    },
    {
        "id": "snmp-v2c-vs-v3-security-and-usm",
        "title": "SNMPv2c vs SNMPv3: Cryptographic Authentication & Privacy (USM)",
        "category": "Networking",
        "category_dir": "networking",
        "category_page": "networking.html",
        "level": "Intermediate",
        "description": "Examine the evolution of Simple Network Management Protocol (SNMP): MIBs, OIDs, plaintext community string vulnerabilities in SNMPv2c, and SNMPv3 USM encryption.",
        "keywords": "snmp, snmpv2c, snmpv3, usm, vacm, mib, oid, network monitoring, authentication, sha, aes encryption, sysadmin",
        "html": r"""<p>For over three decades, the <strong>Simple Network Management Protocol (SNMP)</strong> has functioned as the foundational protocol for monitoring network equipment health, interface throughput, CPU utilization, and system uptime across routers, switches, servers, and storage appliances. However, older implementations—specifically <strong>SNMPv1 and SNMPv2c</strong>—possess critical security vulnerabilities that expose network topologies and allow unauthorized configuration modification over plain text.</p>
<p>To protect enterprise management traffic, the Internet Engineering Task Force (IETF) standardized <strong>SNMPv3 (RFC 3411–3418)</strong>, introducing cryptographic authentication, tamper prevention, and symmetric encryption via the <strong>User-Based Security Model (USM)</strong>.</p>

<h2>SNMP Core Architecture: MIBs and OIDs</h2>
<p>Regardless of protocol version, SNMP operates around an asynchronous client-server management model:</p>
<ul>
    <li><strong>SNMP Manager (Network Management Station / NMS):</strong> The centralized monitoring server (e.g. Zabbix, PRTG, SolarWinds, Prometheus SNMP Exporter) that polls devices or receives asynchronous alerts.</li>
    <li><strong>SNMP Agent:</strong> Software running on the managed device (router, switch, Linux host) that collects internal hardware and software metrics into local memory structures.</li>
    <li><strong>Management Information Base (MIB):</strong> A structured hierarchical database defining all manageable variables on the system.</li>
    <li><strong>Object Identifier (OID):</strong> A dot-delimited numerical address representing a specific variable in the MIB tree. For example, the standardized system description string resides at <code>1.3.6.1.2.1.1.1.0</code> (iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0).</li>
</ul>

<h2>SNMP Operations</h2>
<p>SNMP communication utilizes UDP transport (Port 161 for polling queries, Port 162 for asynchronous Trap/Inform messages):</p>
<ol>
    <li><strong>GET / GETNEXT:</strong> The NMS requests the value of a specific OID or iterates through the next variable in the MIB tree.</li>
    <li><strong>GETBULK:</strong> Introduced in SNMPv2c to retrieve large blocks of tabular data (such as an entire switch interface table) in a single packet round-trip.</li>
    <li><strong>SET:</strong> The NMS writes a value to an OID, modifying the device configuration (such as shutting down a switch port).</li>
    <li><strong>TRAP:</strong> An unacknowledged alert sent proactively by the agent to the NMS when an event occurs (e.g. link state transition down).</li>
    <li><strong>INFORM:</strong> A reliable trap introduced in SNMPv2c that requires an explicit acknowledgment from the NMS, retransmitting if dropped.</li>
</ol>

<h2>The Critical Vulnerability of SNMPv2c: Plaintext Communities</h2>
<p>SNMPv2c relies exclusively on <strong>Community Strings</strong> for access control. A community string is essentially a cleartext shared password transmitted in every single packet header:</p>
<ul>
    <li><strong>Read-Only (RO) Community:</strong> Allows polling telemetry (defaults historically to <code>public</code>).</li>
    <li><strong>Read-Write (RW) Community:</strong> Permits remote configuration changes via SET requests (defaults historically to <code>private</code>).</li>
</ul>

<div class="callout callout-warning">
    <div class="callout-title"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i> The Danger of SNMPv2c on Production Networks</div>
    <div class="callout-body">Because SNMPv2c transmits community strings in unencrypted cleartext, any adversary with access to the local switch fabric or a tapped span port can capture community strings using a packet analyzer like Wireshark. A compromised Read-Write community string allows attackers to overwrite boot configurations, redirect traffic via routing changes, or trigger reboot loops.</div>
</div>

<h2>SNMPv3 Security Architecture: USM and VACM</h2>
<p>SNMPv3 completely replaces community strings with user identity credentials and provides two complementary security frameworks:</p>
<ol>
    <li><strong>User-Based Security Model (USM):</strong> Handles cryptographic authentication, replay protection, and payload encryption.</li>
    <li><strong>View-Based Access Control Model (VACM):</strong> Controls authorization by restricting which OID subtrees specific users or groups are allowed to view or modify.</li>
</ol>

<h3>SNMPv3 Security Levels</h3>
<p>SNMPv3 defines three distinct security operating tiers:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Security Level</th>
                <th>Authentication</th>
                <th>Privacy (Encryption)</th>
                <th>Security Impact</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>noAuthNoPriv</strong></td>
                <td>None (Username match only)</td>
                <td>None (Plaintext)</td>
                <td>Insecure; only provides username verification with no cryptographic protection.</td>
            </tr>
            <tr>
                <td><strong>authNoPriv</strong></td>
                <td>HMAC-SHA-256 / SHA-512</td>
                <td>None (Plaintext)</td>
                <td>Authenticates the message origin and prevents tampering, but payload remains readable by eavesdroppers.</td>
            </tr>
            <tr>
                <td><strong>authPriv</strong></td>
                <td>HMAC-SHA-256 / SHA-512</td>
                <td>AES-128 / AES-192 / AES-256</td>
                <td><strong>Recommended Enterprise Standard:</strong> Mutual cryptographic authentication and full payload encryption.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Replay Attack Mitigation in SNMPv3</h2>
<p>To defend against replay attacks where an adversary captures an authentic encrypted SNMP packet and re-transmits it later to duplicate commands, SNMPv3 USM embeds authoritative engine state:</p>
<ul>
    <li><strong>snmpEngineID:</strong> A unique hexadecimal identifier assigned to every SNMP entity.</li>
    <li><strong>snmpEngineBoots:</strong> A persistent integer that increments every time the SNMP agent reboots.</li>
    <li><strong>snmpEngineTime:</strong> The current uptime counter of the agent in seconds.</li>
</ul>
<p>The SNMP agent rejects any packet whose timestamp deviates by more than 150 seconds from its authoritative internal clock.</p>

<h2>Enterprise Configuration: Cisco IOS-XE SNMPv3 Example</h2>
<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Cisco IOS-XE Global Configuration</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code>! 1. Define a restricted MIB view exposing only system and interface statistics
snmp-server view MONITOR-VIEW iso.org.dod.internet.mgmt.mib-2.system included
snmp-server view MONITOR-VIEW iso.org.dod.internet.mgmt.mib-2.interfaces included

! 2. Create an SNMPv3 group enforcing authPriv security level
snmp-server group SECURE-NMS-GRP v3 priv read MONITOR-VIEW

! 3. Provision a dedicated SNMPv3 monitoring user with SHA-256 auth and AES-256 encryption
snmp-server user nms-admin SECURE-NMS-GRP v3 auth sha256 StrongAuthPass2026! priv aes 256 StrongPrivKey2026!</code></pre>
</div>

<h2>Querying SNMPv3 from Linux with <code>snmpget</code></h2>
<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-terminal" aria-hidden="true"></i> Bash (Net-SNMP CLI)</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code># Query system uptime using SNMPv3 authPriv credentials
snmpget -v3 -l authPriv \
    -u nms-admin \
    -a SHA-256 -A "StrongAuthPass2026!" \
    -x AES-256 -X "StrongPrivKey2026!" \
    192.168.10.1 \
    1.3.6.1.2.1.1.3.0</code></pre>
</div>

<h2>Summary</h2>
<p>While SNMPv2c remains common in legacy environments, its plaintext community string model poses severe operational risks on modern networks. Upgrading to SNMPv3 with the <code>authPriv</code> security tier enforces strong HMAC-SHA authentication, AES symmetric encryption, and replay protection, ensuring network monitoring traffic remains confidential, authentic, and secure across enterprise infrastructure.</p>"""
    }
]
