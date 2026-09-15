/**
 * MJ Tech Hub - IPv4 Subnet & CIDR Calculator
 * High-precision, zero-dependency, client-side IP math engine.
 * Fully RFC 3021 (/31) and RFC 1918 compliant.
 */

(function() {
    'use strict';

    // Utility: Convert 32-bit unsigned integer to dotted-decimal IPv4 string
    function intToIp(int) {
        return [
            (int >>> 24) & 255,
            (int >>> 16) & 255,
            (int >>> 8) & 255,
            int & 255
        ].join('.');
    }

    // Utility: Convert dotted-decimal IPv4 string to 32-bit unsigned integer
    function ipToInt(ipStr) {
        const parts = ipStr.trim().split('.');
        if (parts.length !== 4) return null;
        let num = 0;
        for (let i = 0; i < 4; i++) {
            const p = parts[i];
            if (!/^\d+$/.test(p)) return null;
            const val = parseInt(p, 10);
            if (val < 0 || val > 255) return null;
            num = (num << 8) | val;
        }
        return num >>> 0;
    }

    // Utility: Convert 32-bit int to 8-bit dotted binary string
    function intToBinary(int, prefix) {
        const binStr = (int >>> 0).toString(2).padStart(32, '0');
        const octets = [
            binStr.slice(0, 8),
            binStr.slice(8, 16),
            binStr.slice(16, 24),
            binStr.slice(24, 32)
        ];
        return octets.join('.');
    }

    // Utility: Classify RFC 1918 and Special-Use IPv4 space
    function classifyIp(int) {
        const o1 = (int >>> 24) & 255;
        const o2 = (int >>> 16) & 255;

        // 10.0.0.0/8
        if (o1 === 10) {
            return { scope: 'Private', rfc: 'RFC 1918 (10.0.0.0/8 Private Enterprise Network)', isPrivate: true };
        }
        // 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
        if (o1 === 172 && o2 >= 16 && o2 <= 31) {
            return { scope: 'Private', rfc: 'RFC 1918 (172.16.0.0/12 Private Enterprise Network)', isPrivate: true };
        }
        // 192.168.0.0/16
        if (o1 === 192 && o2 === 168) {
            return { scope: 'Private', rfc: 'RFC 1918 (192.168.0.0/16 Private Enterprise Network)', isPrivate: true };
        }
        // 127.0.0.0/8 (Loopback)
        if (o1 === 127) {
            return { scope: 'Loopback', rfc: 'RFC 1122 (Host Loopback)', isPrivate: false };
        }
        // 169.254.0.0/16 (Link-Local / APIPA)
        if (o1 === 169 && o2 === 254) {
            return { scope: 'Link-Local', rfc: 'RFC 3927 (Dynamic Configuration of IPv4 Link-Local)', isPrivate: false };
        }
        // 224.0.0.0/4 (Multicast)
        if (o1 >= 224 && o1 <= 239) {
            return { scope: 'Multicast', rfc: 'RFC 5771 (Multicast Address Space - Class D)', isPrivate: false };
        }
        // 240.0.0.0/4 (Reserved)
        if (o1 >= 240) {
            return { scope: 'Reserved', rfc: 'RFC 1112 (Reserved for Future Use - Class E)', isPrivate: false };
        }
        // 0.0.0.0/8 (Current network)
        if (o1 === 0) {
            return { scope: 'Current Network', rfc: 'RFC 1122 ("This host on this network")', isPrivate: false };
        }

        return { scope: 'Public', rfc: 'Public Globally Routable IPv4 Address', isPrivate: false };
    }

    // Core Calculation Function
    function calculateSubnet(ipStr, prefixInt) {
        const ipInt = ipToInt(ipStr);
        if (ipInt === null) {
            return { error: 'Invalid IPv4 address format. Please enter four numeric octets (0-255) separated by dots.' };
        }

        if (isNaN(prefixInt) || prefixInt < 0 || prefixInt > 32) {
            return { error: 'Invalid CIDR prefix. Prefix length must be an integer between /0 and /32.' };
        }

        // Calculate 32-bit Subnet Mask
        const maskInt = prefixInt === 0 ? 0 : (~0 << (32 - prefixInt)) >>> 0;
        const wildcardInt = (~maskInt) >>> 0;

        // Calculate Network & Broadcast Addresses
        const networkInt = (ipInt & maskInt) >>> 0;
        const broadcastInt = (networkInt | wildcardInt) >>> 0;

        // Calculate Total & Usable Hosts
        const hostBits = 32 - prefixInt;
        let totalHosts = 0;
        let usableHosts = 0;
        let firstUsableInt = 0;
        let lastUsableInt = 0;
        let specialNote = '';

        if (prefixInt === 32) {
            // /32 Host route
            totalHosts = 1;
            usableHosts = 1;
            firstUsableInt = networkInt;
            lastUsableInt = networkInt;
            specialNote = 'RFC 4632 / Single host route. Network and broadcast semantics do not apply; address represents an individual interface or loopback.';
        } else if (prefixInt === 31) {
            // RFC 3021 Point-to-point links
            totalHosts = 2;
            usableHosts = 2;
            firstUsableInt = networkInt;
            lastUsableInt = broadcastInt;
            specialNote = 'RFC 3021 Point-to-Point link. Both addresses are fully usable for endpoint interfaces without dedicated network or broadcast addresses.';
        } else if (prefixInt === 0) {
            // /0 Default route
            totalHosts = 4294967296;
            usableHosts = 4294967294;
            firstUsableInt = 1;
            lastUsableInt = 4294967294;
            specialNote = 'Default route (0.0.0.0/0). Represents all IPv4 Internet routes.';
        } else {
            // Standard /1 through /30
            totalHosts = Math.pow(2, hostBits);
            usableHosts = Math.max(0, totalHosts - 2);
            firstUsableInt = (networkInt + 1) >>> 0;
            lastUsableInt = (broadcastInt - 1) >>> 0;
        }

        const classification = classifyIp(ipInt);

        return {
            error: null,
            ip: intToIp(ipInt),
            prefix: prefixInt,
            mask: intToIp(maskInt),
            wildcard: intToIp(wildcardInt),
            network: intToIp(networkInt),
            broadcast: intToIp(broadcastInt),
            firstUsable: intToIp(firstUsableInt),
            lastUsable: intToIp(lastUsableInt),
            usableRange: prefixInt === 32 
                ? intToIp(networkInt) 
                : `${intToIp(firstUsableInt)} – ${intToIp(lastUsableInt)}`,
            totalHosts: totalHosts.toLocaleString(),
            usableHosts: usableHosts.toLocaleString(),
            scope: classification.scope,
            rfcNotice: classification.rfc,
            isPrivate: classification.isPrivate,
            specialNote: specialNote,
            binaryIp: intToBinary(ipInt, prefixInt),
            binaryMask: intToBinary(maskInt, prefixInt),
            binaryNetwork: intToBinary(networkInt, prefixInt),
            binaryBroadcast: intToBinary(broadcastInt, prefixInt)
        };
    }

    // Export to global namespace for interactive UI & automated testing
    window.MJSubnetCalculator = {
        calculateSubnet: calculateSubnet,
        ipToInt: ipToInt,
        intToIp: intToIp,
        classifyIp: classifyIp
    };

    // Initialize UI when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        const ipInput = document.getElementById('subnet-ip-input');
        const prefixSelect = document.getElementById('subnet-prefix-select');
        const calcBtn = document.getElementById('subnet-calc-btn');
        const errorAlert = document.getElementById('subnet-error-alert');
        const resultsCard = document.getElementById('subnet-results-card');

        if (!ipInput || !prefixSelect) return;

        function runCalculation() {
            const rawIp = ipInput.value.trim();
            const prefix = parseInt(prefixSelect.value, 10);

            // Handle empty input gracefully
            if (!rawIp) {
                errorAlert.textContent = 'Please enter an IPv4 address (e.g. 192.168.1.10).';
                errorAlert.style.display = 'block';
                resultsCard.style.display = 'none';
                return;
            }

            const res = calculateSubnet(rawIp, prefix);

            if (res.error) {
                errorAlert.textContent = res.error;
                errorAlert.style.display = 'block';
                resultsCard.style.display = 'none';
                return;
            }

            errorAlert.style.display = 'none';
            resultsCard.style.display = 'block';

            // Populate DOM fields securely using textContent
            document.getElementById('res-ip').textContent = `${res.ip} /${res.prefix}`;
            document.getElementById('res-mask').textContent = res.mask;
            document.getElementById('res-wildcard').textContent = res.wildcard;
            document.getElementById('res-network').textContent = res.network;
            document.getElementById('res-broadcast').textContent = res.broadcast;
            document.getElementById('res-range').textContent = res.usableRange;
            document.getElementById('res-usable-hosts').textContent = res.usableHosts;
            document.getElementById('res-total-hosts').textContent = res.totalHosts;

            // Scope & RFC badge
            const scopeEl = document.getElementById('res-scope');
            scopeEl.textContent = res.scope;
            scopeEl.className = 'badge ' + (res.isPrivate ? 'badge-success' : (res.scope === 'Public' ? 'badge-primary' : 'badge-warning'));
            document.getElementById('res-rfc').textContent = res.rfcNotice;

            // Special notes box for /31 or /32
            const noteBox = document.getElementById('res-note-box');
            if (res.specialNote) {
                noteBox.textContent = res.specialNote;
                noteBox.style.display = 'block';
            } else {
                noteBox.style.display = 'none';
            }

            // Binary representations
            document.getElementById('bin-ip').textContent = res.binaryIp;
            document.getElementById('bin-mask').textContent = res.binaryMask;
            document.getElementById('bin-network').textContent = res.binaryNetwork;
            document.getElementById('bin-broadcast').textContent = res.binaryBroadcast;

            // Announce calculation to screen readers via aria-live
            const liveRegion = document.getElementById('subnet-live-announcer');
            if (liveRegion) {
                liveRegion.textContent = `Calculated ${res.ip}/${res.prefix}: Network ${res.network}, ${res.usableHosts} usable hosts.`;
            }
        }

        calcBtn.addEventListener('click', runCalculation);

        ipInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') runCalculation();
        });

        prefixSelect.addEventListener('change', runCalculation);

        // Pre-run initial calculation on page load
        runCalculation();
    });
})();
