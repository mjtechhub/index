# scripts/content/batch5_servers.py
"""
MJ Tech Hub - Phase 6.5E Batch 5 Servers Content Module
Contains authoritative content for 3 Servers tutorials:
1. server-hardware-health-monitoring-ipmi-snmp-traps
2. windows-server-security-baselines-and-cis-benchmark-hardening
3. systematic-root-cause-analysis-rca-methodology-for-server-outages
"""

SERVERS_TUTORIALS = [
    {
        "id": "server-hardware-health-monitoring-ipmi-snmp-traps",
        "title": "Server Hardware Health Telemetry via IPMI Sensors & SNMP Traps",
        "category": "Servers",
        "category_dir": "servers",
        "category_page": "servers.html",
        "level": "Intermediate",
        "description": "Master out-of-band enterprise server hardware monitoring: Baseboard Management Controllers (BMC), IPMI 2.0 sensor telemetry, Redfish APIs, and real-time SNMP trap alerting.",
        "keywords": "ipmi, bmc, server hardware monitoring, snmp traps, idrac, ilo, ipmitool, redfish, hardware sensors, sysadmin",
        "html": r"""<p>Operating enterprise compute infrastructure requires visibility beneath the operating system layer. When a server suffers a failing cooling fan, correctable memory errors on a DIMM, or redundant power supply degradation, standard OS-level performance monitoring tools often register no anomaly until the server halts abruptly from thermal shutdown or unrecoverable hardware fault.</p>
<p>Enterprise server monitoring relies on <strong>Out-of-Band (OOB) telemetry</strong> delivered by the <strong>Baseboard Management Controller (BMC)</strong> via the <strong>Intelligent Platform Management Interface (IPMI)</strong>, modern <strong>Redfish APIs</strong>, and <strong>SNMP Traps</strong>.</p>

<h2>The Baseboard Management Controller (BMC) Architecture</h2>
<p>Every enterprise rack and blade server (e.g., Dell PowerEdge with iDRAC, HPE ProLiant with iLO, Lenovo ThinkSystem with XCC) incorporates an independent, specialized microcontroller mounted directly onto the motherboard: the <strong>Baseboard Management Controller (BMC)</strong>.</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Architectural Attribute</th>
                <th>Host Operating System</th>
                <th>Baseboard Management Controller (BMC)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Processor Architecture</strong></td>
                <td>Main multi-core x86_64 / ARM server CPUs</td>
                <td>Dedicated embedded SoC (ARM/ASPEED) with independent flash and RAM.</td>
            </tr>
            <tr>
                <td><strong>Power Plane</strong></td>
                <td>Operates on Main Power Plane (active when server is powered ON).</td>
                <td>Operates on Auxiliary Standby Power (active as long as server is plugged into wall/PDU).</td>
            </tr>
            <tr>
                <td><strong>Network Interface</strong></td>
                <td>Production server 10G/25G NICs</td>
                <td>Dedicated 1GbE Out-of-Band management Ethernet port (or shared LOM port).</td>
            </tr>
            <tr>
                <td><strong>Telemetry Scope</strong></td>
                <td>Process states, memory allocation, filesystems</td>
                <td>Low-level hardware sensors: voltages, temperatures, fan tachometers, chassis intrusion, power draw.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>IPMI Architecture & Sensor Data Records (SDR)</h2>
<p>The <strong>Intelligent Platform Management Interface (IPMI 2.0)</strong> standardizes communication with the BMC across vendors. The BMC interfaces with dozens of physical sensors through the I2C/SMBus backplane, exposing telemetry through <strong>Sensor Data Records (SDR)</strong>:</p>

<ul>
    <li><strong>Thermal Probes:</strong> Monitors ambient chassis intake, CPU die temperature, memory DIMM banks, and power supply exhaust in degrees Celsius.</li>
    <li><strong>Cooling Fans:</strong> Tracks rotational speed in RPM; alerts if a fan drops below defined lower non-critical (LNC) or lower critical (LC) thresholds.</li>
    <li><strong>Voltage Regulators:</strong> Monitors motherboard DC voltage rails (+12V, +5V, +3.3V, Vcore) to identify electrical degradation.</li>
    <li><strong>Power Supply Units (PSU):</strong> Monitors AC input wattage, DC output load, and redundancy state (1+1 or 2+2).</li>
</ul>

<h3>Inspecting Hardware Telemetry via ipmitool</h3>
<p>Systems administrators query the BMC locally through kernel drivers (<code>/dev/ipmi0</code>) or remotely over the network using the Remote Management Control Protocol (RMCP+):</p>

<div class="tutorial-command">
    <pre><code># 1. Query real-time readings from all physical hardware sensors
ipmitool sdr list

# 2. Query power supply redundancy and status specifically
ipmitool sdr type "Power Supply"

# 3. Read the hardware System Event Log (SEL)
ipmitool sel elist

# 4. Clear resolved events from the hardware SEL
ipmitool sel clear</code></pre>
</div>

<p>Example terminal output from <code>ipmitool sdr list</code> on an enterprise rack server:</p>

<div class="tutorial-command">
    <pre><code>CPU1 Temp        | 42 degrees C      | ok
CPU2 Temp        | 45 degrees C      | ok
Inlet Temp       | 21 degrees C      | ok
Exhaust Temp     | 34 degrees C      | ok
Fan1A RPM        | 7800 RPM          | ok
Fan1B RPM        | 7600 RPM          | ok
PS1 Status       | 0x01              | ok
PS2 Status       | 0x01              | ok
Volts 12V        | 12.08 Volts       | ok</code></pre>
</div>

<h2>Real-Time Alerting: SNMP Traps vs Informs</h2>
<p>While monitoring servers can periodically poll the BMC over IPMI or Redfish (pull model), critical hardware failures require instant push notifications. The BMC achieves this by transmitting <strong>SNMP Traps</strong> immediately upon threshold violations:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Telemetry Model</th>
                <th>Protocol Mechanism</th>
                <th>Delivery Guarantee</th>
                <th>Operational Use Case</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>SNMP Polling (Pull)</strong></td>
                <td>SNMP GET / GETBULK (UDP 161)</td>
                <td>Request / Response</td>
                <td>Periodic metrics collection for historical trending and Grafana dashboards.</td>
            </tr>
            <tr>
                <td><strong>SNMP Trap (Push)</strong></td>
                <td>Unacknowledged Trap (UDP 162)</td>
                <td>Best-Effort (Fire-and-Forget)</td>
                <td>Immediate alerting on component failure (e.g., Fan Fail, PSU Unplugged).</td>
            </tr>
            <tr>
                <td><strong>SNMP Inform (Push)</strong></td>
                <td>Acknowledged Inform (UDP 162)</td>
                <td>Guaranteed (Receiver ACKs)</td>
                <td>High-reliability alerting; BMC retransmits trap until monitoring server acknowledges receipt.</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="tutorial-callout callout-warning">
    <p><strong>Security Warning: IPMI 2.0 Cipher Suite 0 & RAKP Flaws:</strong> Legacy IPMI 2.0 deployments frequently suffer from known cryptographic vulnerabilities (such as Cipher Suite 0 allowing authentication bypass, or RAKP authentication exposing salted password hashes over UDP port 623). Always isolate BMC management interfaces onto a strictly segmented management VLAN with access restricted to authorized jump boxes and monitoring collectors.</p>
</div>

<h2>The Modern Standard: DMTF Redfish REST API</h2>
<p>Modern datacenter infrastructure is transitioning from IPMI to <strong>DMTF Redfish</strong>. Redfish exposes hardware telemetry over secure HTTPS using standard JSON schemas (RFC 8259):</p>

<div class="tutorial-command">
    <pre><code># Query server thermal metrics via Redfish REST API using curl
curl -k -u "admin:SecretPassword" \
     https://10.10.50.25/redfish/v1/Chassis/System.Embedded.1/Thermal \
     | jq '.Temperatures[] | {Sensor: .Name, Reading: .ReadingCelsius, Status: .Status.Health}'</code></pre>
</div>

<h2>Enterprise Monitoring Architecture Checklist</h2>
<ol>
    <li>Assign all server BMCs (iDRAC, iLO) dedicated static IP addresses on an isolated management VLAN.</li>
    <li>Configure SNMPv3 with authentication (SHA-256) and privacy encryption (AES-256) to secure trap delivery.</li>
    <li>Deploy Prometheus IPMI Exporter or Redfish Exporter to ingest hardware metrics into centralized Grafana dashboards.</li>
    <li>Set automated threshold alerts for predictive hardware failure indicators: correctable ECC memory errors, degraded RAID arrays, and PSU redundancy loss.</li>
</ol>"""
    },
    {
        "id": "windows-server-security-baselines-and-cis-benchmark-hardening",
        "title": "Windows Server Hardening via CIS Benchmarks & Microsoft Security Baselines",
        "category": "Servers",
        "category_dir": "servers",
        "category_page": "servers.html",
        "level": "Intermediate",
        "description": "Harden Windows Server 2022/2025: Microsoft Security Compliance Toolkit (MSCT), CIS Level 1 & Level 2 benchmarks, LSA Protection, Credential Guard, and disabling legacy protocols.",
        "keywords": "windows server hardening, cis benchmarks, security baselines, lgpo, lsa protection, credential guard, smbv1, ntlm, sysadmin",
        "html": r"""<p>Fresh installations of Windows Server are engineered by default to maximize backward compatibility with legacy applications and enterprise networks. Out of the box, legacy protocols, permissive local rights, broad administrative shares, and unhardened cryptographic ciphers remain enabled.</p>
<p>In production enterprise environments, systems administrators must harden operating system configurations against lateral movement, credential dumping (Mimikatz), and privilege escalation. Hardening Windows Server requires adopting verified industry baselines: the <strong>Microsoft Security Compliance Toolkit (MSCT)</strong> and <strong>Center for Internet Security (CIS) Benchmarks</strong>.</p>

<h2>CIS Benchmark Levels: Level 1 vs Level 2</h2>
<p>The Center for Internet Security (CIS) publishes globally recognized consensus benchmarks for Windows Server 2022 and 2025, partitioned into two distinct security operational tiers:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Hardening Tier</th>
                <th>Target Environment</th>
                <th>Operational Impact</th>
                <th>Key Included Baselines</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>CIS Level 1 (Benchmark)</strong></td>
                <td>Standard enterprise production servers</td>
                <td>Minimal to no service disruption; balance of defense and utility.</td>
                <td>Disabling SMBv1/LLMNR, enforcing password complexity, restricting anonymous enumeration, enabling Windows Defender Antivirus.</td>
            </tr>
            <tr>
                <td><strong>CIS Level 2 (Defense-in-Depth)</strong></td>
                <td>High-security, defense, financial, and critical infrastructure</td>
                <td>May inhibit legacy software; requires extensive pre-production testing.</td>
                <td>Mandatory Credential Guard, strict LSA protection, blocking debug privileges, disabling NTLM completely in favor of Kerberos.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Core Hardening Vectors</h2>

<h3>1. Eliminating Insecure Legacy Protocols</h3>
<p>Adversaries rely heavily on unhardened network broadcast and legacy transport protocols for network poisoning and relay attacks:</p>
<ul>
    <li><strong>Disable SMBv1:</strong> SMBv1 is cryptographically obsolete and vulnerable to remote code execution (e.g., EternalBlue / WannaCry). Modern servers must enforce SMBv2/v3 with mandatory encryption and pre-authentication integrity.</li>
    <li><strong>Disable LLMNR & NetBIOS:</strong> Link-Local Multicast Name Resolution (LLMNR) and NetBIOS over TCP/IP transmit broadcast requests when DNS lookups fail. Attackers use tools like Responder to capture and relay password hashes across the subnet.</li>
    <li><strong>Mandate NTLMv2 & Restrict LM:</strong> Enforce <code>LmCompatibilityLevel = 5</code> (Send NTLMv2 response only, refuse LM & NTLM).</li>
</ul>

<h3>2. Memory Defense: LSA Protection & Credential Guard</h3>
<p>The <strong>Local Security Authority Subsystem Service (LSASS)</strong> process (<code>lsass.exe</code>) manages user authentications and tokens. Unhardened servers allow administrative processes to read LSASS memory and dump plaintext credentials and Kerberos tickets:</p>
<ul>
    <li><strong>LSA Protection (RunAsPPL):</strong> Configures LSASS as a Protected Process Light (PPL). Once enabled, even processes running as <code>NT AUTHORITY\SYSTEM</code> cannot read or inject code into LSASS without a cryptographically signed Microsoft kernel certificate.</li>
    <li><strong>Windows Defender Credential Guard:</strong> Leverages <strong>Virtualization-Based Security (VBS)</strong> to isolate NTLM and Kerberos secret keys into a hardware-isolated micro-hypervisor (Virtual Secure Mode), completely inaccessible to the host kernel.</li>
</ul>

<h3>3. Restricting User Rights Assignments (URA)</h3>
<p>Hardened servers enforce strict least-privilege user rights under Local Security Policy:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>User Rights Policy</th>
                <th>Recommended Baseline</th>
                <th>Threat Vector Mitigated</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Access this computer from the network</strong></td>
                <td>Restrict to <code>Administrators</code> and authorized service accounts. Exclude local accounts.</td>
                <td>Pass-the-Hash and lateral movement across servers using local administrative credentials.</td>
            </tr>
            <tr>
                <td><strong>Debug programs (SeDebugPrivilege)</strong></td>
                <td>Assign strictly to <code>Administrators</code> (or empty in high-security Tier 0 DCs).</td>
                <td>Attacker processes attaching to running system services to extract memory or inject code.</td>
            </tr>
            <tr>
                <td><strong>Shut down the system</strong></td>
                <td>Restrict to <code>Administrators</code>.</td>
                <td>Accidental or malicious server shutdowns by standard users.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Applying Baselines via Microsoft LGPO Utility</h2>
<p>To automate baseline application without waiting for Active Directory Group Policy synchronization, administrators deploy Microsoft's <strong>Local Group Policy Object (LGPO.exe)</strong> utility:</p>

<div class="tutorial-command">
    <pre><code># 1. Export current baseline as a backup before making changes
lgpo.exe /b "C:\Backup\PreHardening_GPO"

# 2. Apply Microsoft Security Compliance Toolkit security templates
lgpo.exe /g "C:\SecBaselines\WindowsServer2022_MemberServer"

# 3. Force instant local policy recompilation
gpupdate /force</code></pre>
</div>

<h2>Enforcing Security Baselines via PowerShell</h2>
<p>Administrators can automate key CIS compliance baselines directly via PowerShell:</p>

<div class="tutorial-command">
    <pre><code># 1. Enable LSA Protection (Protected Process Light)
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name "RunAsPPL" -Value 1 -Type DWord

# 2. Disable NetBIOS over TCP/IP on all network adapters
Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled } | ForEach-Object {
    $_.SetTcpipNetbios(2) # 2 = Disable NetBIOS
}

# 3. Disable LLMNR across all network profiles
Set-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient' -Name "EnableMulticast" -Value 0 -Type DWord

# 4. Enforce strict NTLMv2 only (LmCompatibilityLevel = 5)
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name "LmCompatibilityLevel" -Value 5 -Type DWord</code></pre>
</div>

<div class="tutorial-callout callout-warning">
    <p><strong>LSA Protection UEFI Lock Considerations:</strong> Setting <code>RunAsPPL = 1</code> enables software-level protection. To achieve maximum tamper-proofing, administrators configure the UEFI variable lock (<code>RunAsPPL = 2</code> on Windows Server 2022/2025). Note that once locked via UEFI, this policy cannot be disabled via registry edits without physical access to the server BIOS.</p>
</div>

<h2>Auditing & Compliance Verification Checklist</h2>
<ul>
    <li>Run Microsoft <strong>Policy Analyzer</strong> to compare active GPOs against the official Microsoft Security Baseline.</li>
    <li>Verify LSA Protection state in the System Event Log: look for Event ID <code>12</code> (LSASS was started as a protected process).</li>
    <li>Conduct regular vulnerability scans using SCAP/CIS-CAT benchmark compliance engines to detect configuration drift.</li>
</ul>"""
    },
    {
        "id": "systematic-root-cause-analysis-rca-methodology-for-server-outages",
        "title": "Systematic Root Cause Analysis (RCA) Methodology & 5-Whys for System Outages",
        "category": "Servers",
        "category_dir": "servers",
        "category_page": "servers.html",
        "level": "Intermediate",
        "description": "Master enterprise infrastructure Root Cause Analysis (RCA): blameless post-mortem culture, timeline reconstruction, the 5-Whys framework, Fishbone diagrams, and preventative action tracking.",
        "keywords": "root cause analysis, rca, 5 whys, blameless post-mortem, server outage, site reliability engineering, sre, capa, incident post-mortem",
        "html": r"""<p>When an enterprise service suffers an unscheduled outage—whether a hypervisor cluster failure, active database crash, or network routing breakdown—the immediate operational objective is service restoration. However, restoring service is only half the engineering obligation.</p>
<p>Without a rigorous, disciplined <strong>Root Cause Analysis (RCA)</strong>, the latent technical or procedural defect that caused the failure remains embedded in the environment, virtually guaranteeing recurrence. Professional systems engineering approaches post-mortems through systematic causal analysis frameworks and blameless reliability culture.</p>

<h2>The Principle of Blameless Post-Mortems</h2>
<p>Modern Site Reliability Engineering (SRE) establishes a foundational cultural baseline: <strong>blameless post-mortems</strong>. Pioneered by organizations like Etsy and Google SRE, this philosophy recognizes that human operators do not wake up intending to break production systems.</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Cultural Dimension</th>
                <th>Blame-Oriented Culture (Toxic)</th>
                <th>Blameless SRE Culture (Resilient)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Primary Focus</strong></td>
                <td><em>Who</em> made the mistake? Assign personal fault.</td>
                <td><em>Why</em> did the system permit this failure to occur?</td>
            </tr>
            <tr>
                <td><strong>Engineer Behavior</strong></td>
                <td>Engineers hide mistakes, conceal data, and delay escalation.</td>
                <td>Engineers speak candidly, share timelines, and proactively flag risks.</td>
            </tr>
            <tr>
                <td><strong>Remediation Outcome</strong></td>
                <td>Retrain or discipline employee; root architectural flaw unaddressed.</td>
                <td>Harden guardrails, add automated validation, and eliminate single points of failure.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Phase 1: Chronological Incident Timeline Reconstruction</h2>
<p>A rigorous RCA begins with assembling an objective, second-by-second timeline of the incident. All timestamps must be normalized to a standard time zone (preferably <strong>UTC</strong>) to correlate distributed event logs across disparate systems:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Timestamp (UTC)</th>
                <th>Phase</th>
                <th>Observed System State & Event Telemetry</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>14:02:15</code></td>
                <td>Trigger</td>
                <td>Scheduled backup job triggers high I/O storm on SAN storage volume <code>LUN_04</code>.</td>
            </tr>
            <tr>
                <td><code>14:05:30</code></td>
                <td>Degradation</td>
                <td>Disk latency spikes from 2 ms to 2,400 ms. Database write queue overflows.</td>
            </tr>
            <tr>
                <td><code>14:07:00</code></td>
                <td>Outage</td>
                <td>Database service fails health check; web frontend drops all user requests (HTTP 500).</td>
            </tr>
            <tr>
                <td><code>14:08:45</code></td>
                <td>Detection</td>
                <td>Prometheus automated alert fires to PagerDuty; on-call engineer paged.</td>
            </tr>
            <tr>
                <td><code>14:14:20</code></td>
                <td>Triage & Action</td>
                <td>Engineer terminates runaway backup task; storage I/O throttles drop to baseline.</td>
            </tr>
            <tr>
                <td><code>14:18:00</code></td>
                <td>Recovery</td>
                <td>Database finishes crash recovery replay; all API endpoints return HTTP 200.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Phase 2: Proximate Cause vs True Root Cause</h2>
<p>A common failure in RCA execution is stopping investigation at the <strong>proximate cause</strong> (the immediate trigger) rather than drilling down to the <strong>root cause</strong>:</p>

<ul>
    <li><strong>Proximate Cause (The Trigger):</strong> <em>"The database crashed because storage volume LUN_04 latency exceeded 2 seconds."</em> While factually true, addressing only the trigger (e.g., rescheduling the backup) leaves the core architectural vulnerability exposed.</li>
    <li><strong>Root Cause (The Systemic Flaw):</strong> <em>"The database virtual disk lacked Quality of Service (QoS) IOPS limits, and the storage SAN allowed unthrottled backup snapshots to consume 100% of controller cache."</em></li>
</ul>

<h2>The 5-Whys Framework in Action</h2>
<p>Developed within Toyota Production System and widely adopted across technology infrastructure, the <strong>5-Whys</strong> methodology drills through superficial symptoms to isolate core systemic failures:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Iteration</th>
                <th>Analytical Question</th>
                <th>Factual Finding</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Why 1?</strong></td>
                <td>Why did the production ordering API become unavailable?</td>
                <td>Because the backend primary SQL database service halted abruptly.</td>
            </tr>
            <tr>
                <td><strong>Why 2?</strong></td>
                <td>Why did the SQL database halt?</td>
                <td>Because the underlying database transaction log volume ran out of free disk space (0 bytes free).</td>
            </tr>
            <tr>
                <td><strong>Why 3?</strong></td>
                <td>Why did the transaction log volume exhaust disk space?</td>
                <td>Because a nightly transaction log backup job failed, preventing log truncation.</td>
            </tr>
            <tr>
                <td><strong>Why 4?</strong></td>
                <td>Why did the log backup job fail?</td>
                <td>Because the service account password expired unexpectedly without automatic renewal.</td>
            </tr>
            <tr>
                <td><strong>Why 5? (Root Cause)</strong></td>
                <td>Why was a standard interactive user account with an expiring password used for critical infrastructure services instead of a Group Managed Service Account (gMSA)?</td>
                <td>Because deployment procedures lacked an automated infrastructure-as-code baseline mandating non-expiring gMSAs and disk capacity predictive alerting.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Phase 3: The Ishikawa (Fishbone) Diagram</h2>
<p>When outages involve complex multi-system failures, engineers map causal factors across five categorical domains:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Causal Domain</th>
                <th>Investigative Area</th>
                <th>Example Outage Contributing Factors</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Technology</strong></td>
                <td>Hardware, operating system, network, firmware</td>
                <td>Storage controller firmware bug, NIC driver crash, unapplied patch.</td>
            </tr>
            <tr>
                <td><strong>Process</strong></td>
                <td>Change management, release procedures, approvals</td>
                <td>Unscheduled mid-day change, lack of peer review, absence of rollback plan.</td>
            </tr>
            <tr>
                <td><strong>Tooling & Monitoring</strong></td>
                <td>Observability, threshold alerting, test environments</td>
                <td>Alert fatigue, missing synthetic checks, staging environment not matching prod.</td>
            </tr>
            <tr>
                <td><strong>People & Training</strong></td>
                <td>Documentation, runbooks, escalation clarity</td>
                <td>Outdated disaster recovery runbook, delayed escalation to database admin.</td>
            </tr>
            <tr>
                <td><strong>Environment</strong></td>
                <td>Physical facilities, cloud quotas, vendors</td>
                <td>Datacenter HVAC cooling failure, cloud region quota exhaustion, ISP fiber cut.</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Phase 4: Corrective and Preventive Actions (CAPA)</h2>
<p>An RCA without trackable, assigned action items is useless. Every published post-mortem must conclude with <strong>SMART</strong> (Specific, Measurable, Achievable, Relevant, Time-bound) action items assigned to designated owners:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Action ID</th>
                <th>Action Item Description</th>
                <th>Category</th>
                <th>Assigned Owner</th>
                <th>Target SLA</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>ACT-01</code></td>
                <td>Migrate SQL backup service accounts to Group Managed Service Accounts (gMSA) with automated Kerberos key rotation.</td>
                <td>Preventative</td>
                <td>Enterprise Identity Team</td>
                <td>14 Days</td>
            </tr>
            <tr>
                <td><code>ACT-02</code></td>
                <td>Deploy Prometheus alert rule warning when database transaction log volume exceeds 80% capacity.</td>
                <td>Detective</td>
                <td>Observability Team</td>
                <td>3 Days</td>
            </tr>
            <tr>
                <td><code>ACT-03</code></td>
                <td>Update file server provisioning templates in Terraform to mandate volume auto-expansion policies.</td>
                <td>Remediation</td>
                <td>Cloud Ops Team</td>
                <td>30 Days</td>
            </tr>
        </tbody>
    </table>
</div>"""
    }
]
