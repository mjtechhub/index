/**
 * MJ Tech Hub - IP / DNS / Port Network Diagnostic Workbench
 * Educational troubleshooting decision engine for systematic TCP/IP layer isolation.
 * Runs 100% client-side in the browser based on user-entered diagnostic observations.
 */

(function() {
    'use strict';

    function formatEvidenceSummary(obs) {
        const parts = [];
        const formatVal = (v) => v === 'yes' ? 'Success / Responding' : v === 'no' ? 'Failed / Unresponsive' : 'Not Tested';
        parts.push(`Gateway Ping: ${formatVal(obs.gatewayPing)}`);
        parts.push(`Public IP Ping: ${formatVal(obs.publicPing)}`);
        parts.push(`DNS Lookup: ${formatVal(obs.dnsResolve)}`);
        parts.push(`Port Reachability: ${formatVal(obs.portReachable)}`);
        parts.push(`Medium: ${obs.connectionType === 'wifi' ? 'Wi-Fi' : obs.connectionType === 'vpn' ? 'VPN' : obs.connectionType === 'wired' ? 'Wired Ethernet' : 'Unknown'}`);
        parts.push(`Scope: ${obs.scope === 'entire_site' ? 'Entire Site' : obs.scope === 'multiple' ? 'Multiple Devices' : 'Single Device'}`);
        if (obs.targetHost) {
            parts.push(`Target: ${obs.targetHost}`);
        }
        return parts.join(' | ');
    }

    function analyzeObservations(obs) {
        const {
            gatewayPing,     // 'yes', 'no', 'not_tested'
            publicPing,      // 'yes', 'no', 'not_tested'
            dnsResolve,      // 'yes', 'no', 'not_tested'
            portReachable,   // 'yes', 'no', 'not_tested'
            scope,           // 'single', 'multiple', 'entire_site', 'unknown'
            connectionType,  // 'wired', 'wifi', 'vpn', 'unknown'
            targetHost       // string
        } = obs;

        let faultDomain = 'Inconclusive / More Data Needed';
        let confidence = 'Preliminary (Insufficient Observations)';
        let explanation = '';
        let confirmingObs = '';
        let refutingObs = '';
        let nextSteps = [];
        let recommendedCommands = [];
        let relatedTutorials = [];

        const evidenceSummary = formatEvidenceSummary(obs);

        // Scenario 1: Default Gateway Ping Fails
        if (gatewayPing === 'no') {
            if (connectionType === 'wifi') {
                faultDomain = 'Local Wi-Fi Association or Layer 1/2 Wireless Gateway Link';
                confidence = 'Likely (High Evidence Strength)';
                explanation = 'Working hypothesis: The workstation cannot reach its local default gateway over the wireless medium. Packets do not traverse the local subnet, indicating an RF disconnect, incorrect WPA key, AP isolation, or stale DHCP assignment.';
                confirmingObs = 'NIC shows disconnected or APIPA address (169.254.x.x); RSSI weaker than -75 dBm; ping to gateway yields "Destination host unreachable".';
                refutingObs = 'Workstation successfully pings another wireless client on the same AP, or wired devices also cannot reach the gateway.';
                nextSteps = [
                    'Verify Wi-Fi connection status, SSID association, and signal strength (RSSI).',
                    'Check IP configuration with "ipconfig /all" to verify you do not have an APIPA (169.254.x.x) address.',
                    'Test reconnecting to the wireless access point or testing with an Ethernet cable.'
                ];
                recommendedCommands = [
                    { cmd: 'ipconfig /all', desc: 'Inspect local IP, subnet mask, gateway, and DHCP status' },
                    { cmd: 'ping -t <Gateway_IP>', desc: 'Continuous ICMP probe to monitor wireless link stability' },
                    { cmd: 'netsh wlan show interfaces', desc: 'Audit Windows Wi-Fi signal, channel, and BSSID state' }
                ];
                relatedTutorials = [
                    { title: 'Wi-Fi Security: WPA2 vs WPA3 Enterprise', url: 'tutorials/networking/wi-fi-security-wpa2-enterprise-vs-wpa3.html' },
                    { title: 'DHCP DORA Process & IP Assignment', url: 'tutorials/networking/dhcp-dora-process-and-ip-assignment.html' }
                ];
            } else if (connectionType === 'vpn') {
                faultDomain = 'Virtual Private Network (VPN) Tunnel or Routing Metric Conflict';
                confidence = 'Likely (High Evidence Strength)';
                explanation = 'Working hypothesis: The VPN tunnel virtual adapter cannot reach the configured tunnel gateway. This commonly indicates tunnel negotiation failure, expired credentials, or an interface metric routing conflict.';
                confirmingObs = 'Virtual adapter shows 0.0.0.0 or disconnected; routing table lacks tunnel 0.0.0.0/0 route; ping fails with "General failure".';
                refutingObs = 'Direct ping to physical default gateway fails before starting VPN; or VPN concentrator logs confirm active authenticated session.';
                nextSteps = [
                    'Verify physical Internet reachability before initiating the VPN client.',
                    'Inspect the routing table to verify default route metric preference.',
                    'Check VPN concentrator logs or client authentication status.'
                ];
                recommendedCommands = [
                    { cmd: 'route print', desc: 'Inspect IPv4 routing table and gateway interface metrics' },
                    { cmd: 'ip route show', desc: 'Inspect Linux routing table entries' }
                ];
                relatedTutorials = [
                    { title: 'Subnetting Basics: Network IDs & Masks', url: 'tutorials/networking/subnetting-basics.html' }
                ];
            } else {
                faultDomain = 'Local Subnet Configuration or Physical Layer (Layer 1/2)';
                confidence = 'Likely (High Evidence Strength)';
                explanation = 'Working hypothesis: Failing to ping the local default gateway indicates a breakdown at the Data Link or Physical layer (Layer 1/2), or an invalid static IP/subnet mask configuration on the local host.';
                confirmingObs = 'NIC link light is unlit; "Media disconnected"; ARP cache ("arp -a") shows no entry or MAC 00-00-00-00-00-00 for the gateway IP.';
                refutingObs = 'ARP cache successfully displays the router hardware MAC address, but ICMP is explicitly administratively blocked by gateway ACL.';
                nextSteps = [
                    'Inspect physical link status (NIC link LED or Ethernet carrier state).',
                    'Confirm the workstation is on the correct VLAN and has received valid DHCP parameters.',
                    'Query the ARP table ("arp -a" or "ip neigh") to confirm if the gateway MAC address is resolved.'
                ];
                recommendedCommands = [
                    { cmd: 'ipconfig /all', desc: 'Verify local IP, subnet mask, and default gateway' },
                    { cmd: 'arp -a', desc: 'Verify ARP table resolution for the default gateway IP' },
                    { cmd: 'ip neigh', desc: 'Inspect Linux neighbor cache and ARP state' }
                ];
                relatedTutorials = [
                    { title: 'OSI Model Explained: The 7 Layers', url: 'tutorials/networking/osi-model-explained.html' },
                    { title: 'Address Resolution Protocol (ARP) Deep Dive', url: 'tutorials/networking/arp-protocol-explained.html' }
                ];
            }
        }
        // Scenario 2: Gateway OK, but Public IP Ping Fails
        else if (gatewayPing === 'yes' && publicPing === 'no') {
            faultDomain = 'Upstream WAN / ISP Routing or Gateway NAT Configuration';
            confidence = 'Likely (High Evidence Strength)';
            explanation = 'Working hypothesis: The local LAN segment and default gateway are responding normally, but outbound packets cannot reach public Internet IP addresses. The failure resides at the edge router, NAT gateway, WAN firewall, or ISP circuit.';
            confirmingObs = 'Traceroute ("tracert -d 8.8.8.8") succeeds to the default gateway but times out on the WAN edge hop or ISP gateway.';
            refutingObs = 'Secondary public IP (e.g. 1.1.1.1 or 9.9.9.9) responds immediately, indicating 8.8.8.8 is specifically filtered or unreachable.';
            nextSteps = [
                'Execute a traceroute ("tracert 8.8.8.8" or "traceroute 8.8.8.8") to identify the exact hop where packets are dropped.',
                'Log into the perimeter router/firewall to check WAN interface status and NAT overload (PAT) table.',
                'Check with your Internet Service Provider for regional circuit outages.'
            ];
            recommendedCommands = [
                { cmd: 'tracert -d 8.8.8.8', desc: 'Trace route to public destination without performing reverse DNS' },
                { cmd: 'traceroute 8.8.8.8', desc: 'Trace network hops on Linux systems' },
                { cmd: 'ping 1.1.1.1', desc: 'Verify against a secondary public resolver to rule out single-IP filtering' }
            ];
            relatedTutorials = [
                { title: 'OSI Model Explained: The 7 Layers', url: 'tutorials/networking/osi-model-explained.html' },
                { title: 'Subnetting Basics: Network IDs & Masks', url: 'tutorials/networking/subnetting-basics.html' }
            ];
        }
        // Scenario 3: Gateway & Public IP OK, but DNS Resolution Fails
        else if (gatewayPing === 'yes' && publicPing === 'yes' && dnsResolve === 'no') {
            faultDomain = 'Domain Name System (DNS) Resolution / Forwarder Failure';
            confidence = 'Likely (High Evidence Strength)';
            explanation = 'Working hypothesis: Layer 1 through Layer 3 IP connectivity is fully functional across the Internet, but application hostnames cannot be resolved. The fault is isolated to DNS client configuration, unresponsive recursive DNS resolvers, or firewall filtering on UDP port 53.';
            confirmingObs = 'Querying configured resolver fails with "DNS request timed out" or "server can\'t find domain", but querying "nslookup google.com 8.8.8.8" succeeds immediately.';
            refutingObs = 'DNS queries to both internal and external public resolvers fail, and port 53 is verified closed by upstream firewall.';
            nextSteps = [
                'Query the configured DNS server directly using "nslookup" or "dig".',
                'Test querying an authoritative public DNS server explicitly (e.g. "nslookup google.com 8.8.8.8").',
                'Verify DNS server IP assignments in DHCP scope or local network adapter settings.',
                'Flush the local DNS resolver cache.'
            ];
            recommendedCommands = [
                { cmd: 'nslookup <hostname>', desc: 'Test default DNS resolver for hostname lookup' },
                { cmd: 'nslookup <hostname> 8.8.8.8', desc: 'Bypass internal DNS and query public resolver' },
                { cmd: 'dig <hostname> +trace', desc: 'Trace recursive DNS resolution across root and TLD servers' },
                { cmd: 'ipconfig /flushdns', desc: 'Clear stale entries from local Windows DNS resolver cache' }
            ];
            relatedTutorials = [
                { title: 'DNS Resolution: Iterative vs Recursive Queries', url: 'tutorials/networking/dns-resolution-iterative-vs-recursive-queries.html' }
            ];
        }
        // Scenario 4: Gateway, Public IP & DNS OK, but Port Unreachable
        else if (gatewayPing === 'yes' && (publicPing === 'yes' || publicPing === 'not_tested') && dnsResolve === 'yes' && portReachable === 'no') {
            faultDomain = 'Transport Layer Firewall / Service Daemon Listener or Security Group';
            confidence = 'Likely (High Evidence Strength)';
            explanation = 'Working hypothesis: Network routing and DNS resolution succeed, but the destination TCP port refused the connection or timed out. This isolates the fault to Layer 4/7: perimeter or host firewalls, cloud Security Groups, or the backend service daemon is stopped/bound to loopback.';
            confirmingObs = 'Test-NetConnection reports "TcpTestSucceeded : False"; service daemon status shows "inactive (dead)" or binding to 127.0.0.1 instead of 0.0.0.0.';
            refutingObs = 'TCP handshake completes successfully when tested directly on the local host where the daemon runs, confirming intermediate network firewall block.';
            nextSteps = [
                'Test TCP port reachability using "Test-NetConnection" (PowerShell), "nc -zv", or "curl -v".',
                'If you administer the target server, check if the service process is active ("systemctl status <svc>").',
                'Verify socket listener binding with "ss -tulpn" to ensure the daemon is listening on 0.0.0.0, not 127.0.0.1.',
                'Inspect perimeter and host firewall rules for inbound permit on the target port.'
            ];
            recommendedCommands = [
                { cmd: 'Test-NetConnection -ComputerName <host> -Port <port>', desc: 'Test end-to-end TCP three-way handshake across firewalls' },
                { cmd: 'ss -tulpn', desc: 'Inspect listening TCP/UDP sockets and process bindings on Linux' },
                { cmd: 'netsh advfirewall firewall show rule name=all', desc: 'Audit Windows Defender Firewall rule allowance' }
            ];
            relatedTutorials = [
                { title: 'TCP Three-Way Handshake & Connection Teardown', url: 'tutorials/networking/tcp-three-way-handshake-and-teardown.html' },
                { title: 'Cloud Security Groups vs Network ACLs', url: 'tutorials/cloud/cloud-security-groups-vs-network-access-control-lists.html' }
            ];
        }
        // Scenario 5: All Tests Succeeded
        else if (gatewayPing === 'yes' && publicPing === 'yes' && dnsResolve === 'yes' && portReachable === 'yes') {
            faultDomain = 'Application / HTTP / Content / Authentication Layer';
            confidence = 'Likely (High Evidence Strength)';
            explanation = 'Working hypothesis: All underlying network layers (Physical, Data Link, Network, Transport, and DNS) are healthy and passing packets. If users still experience errors, the issue is at the application layer (HTTP 500 error, TLS certificate expired, CORS policy, or authentication/SSO failure).';
            confirmingObs = 'Browser dev tools show HTTP status code 500/502/403 or TLS certificate alert; TCP connection opens cleanly.';
            refutingObs = 'Intermittent packet drops or RST packets observed in Wireshark packet capture during bulk payload transfer.';
            nextSteps = [
                'Inspect HTTP response status codes using browser Developer Tools (F12 Network tab) or "curl -I".',
                'Check web server error logs (e.g. /var/log/nginx/error.log) and application server telemetry.',
                'Inspect TLS certificate validity dates and trust chains.'
            ];
            recommendedCommands = [
                { cmd: 'curl -Iv https://<hostname>', desc: 'Audit TLS handshake, cipher negotiation, and HTTP response headers' },
                { cmd: 'openssl s_client -connect <host>:443 -servername <host>', desc: 'Inspect remote TLS certificate chain and expiry' }
            ];
            relatedTutorials = [
                { title: 'TCP Three-Way Handshake & Teardown Flow', url: 'tutorials/networking/tcp-three-way-handshake-and-teardown.html' }
            ];
        }
        // General Inconclusive State
        else {
            faultDomain = 'Preliminary Evidence Collected — Further Isolation Required';
            confidence = 'Low / Preliminary (More Data Needed)';
            explanation = 'Working hypothesis: The supplied observations do not conclusively isolate a single layer. Complete the untested checks (especially default gateway reachability and DNS resolution) to narrow down the fault domain.';
            confirmingObs = 'Providing test results for gateway reachability and DNS lookup will resolve this hypothesis to a specific Layer.';
            refutingObs = 'N/A — Incomplete baseline dataset.';
            nextSteps = [
                'Execute a baseline ping to the local default gateway to isolate Layer 2/3.',
                'Test DNS resolution for both internal and public hostnames.',
                'Test transport connectivity to the specific TCP port in question.'
            ];
            recommendedCommands = [
                { cmd: 'ipconfig /all', desc: 'Retrieve local IP, subnet, gateway, and DNS servers' },
                { cmd: 'ping <Gateway_IP>', desc: 'Verify local gateway reachability' }
            ];
            relatedTutorials = [
                { title: 'OSI Model Explained: The 7 Layers', url: 'tutorials/networking/osi-model-explained.html' }
            ];
        }

        // Scope Considerations
        if (scope === 'entire_site') {
            explanation += ' [Impact Alert]: Because the entire site is affected, prioritize core centralized infrastructure: edge routers, core switches, primary ISP links, or central DHCP/DNS servers rather than individual workstation settings.';
        } else if (scope === 'single') {
            explanation += ' [Scope Note]: Because only a single device is affected, focus initial troubleshooting on endpoint configuration, local patch cables, wireless association, or host-level firewalls before investigating shared infrastructure.';
        }

        return {
            faultDomain: faultDomain,
            confidence: confidence,
            evidenceSummary: evidenceSummary,
            explanation: explanation,
            confirmingObs: confirmingObs,
            refutingObs: refutingObs,
            nextSteps: nextSteps,
            recommendedCommands: recommendedCommands,
            relatedTutorials: relatedTutorials
        };
    }

    // Export to global namespace
    window.MJNetworkDiagnostic = {
        analyzeObservations: analyzeObservations
    };

    // DOM UI Initialization
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('diag-form');
        const resultsCard = document.getElementById('diag-results-card');
        const faultDomainEl = document.getElementById('diag-fault-domain');
        const confidenceEl = document.getElementById('diag-confidence');
        const evidenceSummaryEl = document.getElementById('diag-evidence-summary');
        const explanationEl = document.getElementById('diag-explanation');
        const confirmingObsEl = document.getElementById('diag-confirming-obs');
        const refutingObsEl = document.getElementById('diag-refuting-obs');
        const nextStepsList = document.getElementById('diag-next-steps');
        const commandsList = document.getElementById('diag-commands-list');
        const tutorialsList = document.getElementById('diag-tutorials-list');
        const liveAnnouncer = document.getElementById('diag-live-announcer');

        if (!form) return;

        function runAnalysis() {
            const gatewayPing = document.querySelector('input[name="gateway-ping"]:checked')?.value || 'not_tested';
            const publicPing = document.querySelector('input[name="public-ping"]:checked')?.value || 'not_tested';
            const dnsResolve = document.querySelector('input[name="dns-resolve"]:checked')?.value || 'not_tested';
            const portReachable = document.querySelector('input[name="port-reachable"]:checked')?.value || 'not_tested';
            const scope = document.querySelector('input[name="scope"]:checked')?.value || 'unknown';
            const connectionType = document.querySelector('input[name="conn-type"]:checked')?.value || 'unknown';
            const targetHost = document.getElementById('diag-target-host')?.value.trim() || '';

            const result = analyzeObservations({
                gatewayPing: gatewayPing,
                publicPing: publicPing,
                dnsResolve: dnsResolve,
                portReachable: portReachable,
                scope: scope,
                connectionType: connectionType,
                targetHost: targetHost
            });

            resultsCard.style.display = 'block';

            faultDomainEl.textContent = result.faultDomain;
            confidenceEl.textContent = result.confidence;
            confidenceEl.className = 'badge ' + (result.confidence.startsWith('Likely') ? 'badge-primary' : 'badge-warning');
            
            if (evidenceSummaryEl) {
                evidenceSummaryEl.textContent = result.evidenceSummary;
            }
            explanationEl.textContent = result.explanation;

            if (confirmingObsEl) {
                confirmingObsEl.textContent = result.confirmingObs;
            }
            if (refutingObsEl) {
                refutingObsEl.textContent = result.refutingObs;
            }

            // Render Next Steps
            nextStepsList.innerHTML = '';
            result.nextSteps.forEach(step => {
                const li = document.createElement('li');
                li.textContent = step;
                nextStepsList.appendChild(li);
            });

            // Render Commands
            commandsList.innerHTML = '';
            result.recommendedCommands.forEach(cmd => {
                const div = document.createElement('div');
                div.className = 'diag-cmd-item';
                
                const code = document.createElement('code');
                code.className = 'diag-code';
                code.textContent = cmd.cmd;

                const desc = document.createElement('span');
                desc.className = 'diag-desc';
                desc.textContent = ` — ${cmd.desc}`;

                div.appendChild(code);
                div.appendChild(desc);
                commandsList.appendChild(div);
            });

            // Render Tutorials
            tutorialsList.innerHTML = '';
            result.relatedTutorials.forEach(tut => {
                const a = document.createElement('a');
                a.href = tut.url;
                a.className = 'diag-tutorial-link';
                a.innerHTML = `<i class="fa-solid fa-book-open" aria-hidden="true"></i> ${tut.title}`;
                tutorialsList.appendChild(a);
            });

            if (liveAnnouncer) {
                liveAnnouncer.textContent = `Diagnostic analysis updated: Likely fault domain is ${result.faultDomain}.`;
            }
        }

        form.addEventListener('change', runAnalysis);
        document.getElementById('diag-analyze-btn')?.addEventListener('click', runAnalysis);

        // Pre-run analysis on load
        runAnalysis();
    });
})();

