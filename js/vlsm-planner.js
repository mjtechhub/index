/**
 * MJ Tech Hub - VLSM / Variable Length Subnet Masking Planner
 * Deterministic largest-first subnet allocation engine with overlap prevention
 * and strict parent boundary containment checks.
 */

(function() {
    'use strict';

    function intToIp(int) {
        return [
            (int >>> 24) & 255,
            (int >>> 16) & 255,
            (int >>> 8) & 255,
            int & 255
        ].join('.');
    }

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

    // Core VLSM Allocation Engine
    function calculateVlsm(parentCidrStr, requirementsList) {
        if (!parentCidrStr || typeof parentCidrStr !== 'string') {
            return { error: 'Invalid parent network. Please provide a CIDR network (e.g. 192.168.10.0/24).' };
        }

        const cidrParts = parentCidrStr.trim().split('/');
        if (cidrParts.length !== 2) {
            return { error: 'Invalid parent network format. Expected format: 192.168.10.0/24' };
        }

        const parentIpInt = ipToInt(cidrParts[0]);
        const parentPrefix = parseInt(cidrParts[1], 10);

        if (parentIpInt === null || isNaN(parentPrefix) || parentPrefix < 0 || parentPrefix > 30 || String(parentPrefix) !== cidrParts[1].trim()) {
            return { error: 'Invalid parent network IP or prefix. Parent prefix must be an integer between /0 and /30.' };
        }

        const parentMaskInt = parentPrefix === 0 ? 0 : (~0 << (32 - parentPrefix)) >>> 0;
        const parentNetworkInt = (parentIpInt & parentMaskInt) >>> 0;
        const parentWildcardInt = (~parentMaskInt) >>> 0;
        const parentBroadcastInt = (parentNetworkInt | parentWildcardInt) >>> 0;
        const parentTotalAddresses = Math.pow(2, 32 - parentPrefix);

        const wasNormalized = (parentIpInt !== parentNetworkInt);
        const enteredParent = parentCidrStr.trim();
        const normalizedParent = `${intToIp(parentNetworkInt)}/${parentPrefix}`;

        if (!Array.isArray(requirementsList) || requirementsList.length === 0) {
            return { error: 'Please specify at least one subnet requirement.' };
        }

        if (requirementsList.length > 20) {
            return { error: 'Maximum 20 subnet requirement rows supported.' };
        }

        // Validate and filter requirements (strict integer and positive check)
        const cleanRequirements = [];
        const seenNames = new Set();
        let hasDuplicateNames = false;

        for (let i = 0; i < requirementsList.length; i++) {
            const req = requirementsList[i];
            const name = (req.name !== undefined && req.name !== null ? String(req.name) : '').trim();
            if (!name) {
                return { error: `Subnet requirement #${i + 1} has an empty name. Please provide a unique name for each subnet.` };
            }

            const rawHosts = String(req.hosts !== undefined && req.hosts !== null ? req.hosts : '').trim();

            if (!/^\d+$/.test(rawHosts)) {
                return { error: `Invalid host requirement for '${name}'. Host count must be a valid positive integer.` };
            }

            const hosts = parseInt(rawHosts, 10);
            if (hosts <= 0) {
                return { error: `Invalid host requirement for '${name}'. Must be a positive integer greater than 0.` };
            }
            if (hosts > 16777214) {
                return { error: `Host requirement for '${name}' exceeds maximum practical IPv4 subnet capacity.` };
            }

            const lowerName = name.toLowerCase();
            if (seenNames.has(lowerName)) {
                return { error: `Duplicate subnet name detected: '${name}'. Each subnet requirement must have a unique name.` };
            }
            seenNames.add(lowerName);

            cleanRequirements.push({ id: req.id || `req-${i}`, name: name, hosts: hosts, originalIndex: i });
        }

        // Strict VLSM Rule: Sort requirements largest-first
        const sorted = [...cleanRequirements].sort((a, b) => b.hosts - a.hosts);

        let currentAddressInt = parentNetworkInt;
        const allocations = [];
        let totalAllocatedAddresses = 0;
        let hasOverflow = false;

        for (const req of sorted) {
            // Determine required prefix for host count:
            // Standard LAN subnets require 2 reserved addresses (network + broadcast)
            // hostBits = ceil(log2(hosts + 2))
            const neededAddresses = req.hosts + 2;
            let hostBits = Math.ceil(Math.log2(neededAddresses));
            if (hostBits < 2) hostBits = 2; // Minimum /30 for LAN subnet (2 usable hosts)
            const prefix = 32 - hostBits;
            const blockSize = Math.pow(2, hostBits);
            const maskInt = (~0 << hostBits) >>> 0;

            // Boundary alignment: current address must be a multiple of block size
            const remainder = currentAddressInt % blockSize;
            if (remainder !== 0) {
                currentAddressInt += (blockSize - remainder);
            }

            const subnetNetworkInt = currentAddressInt >>> 0;
            const subnetBroadcastInt = (subnetNetworkInt + blockSize - 1) >>> 0;
            const firstUsableInt = (subnetNetworkInt + 1) >>> 0;
            const lastUsableInt = (subnetBroadcastInt - 1) >>> 0;
            const usableHostsCount = blockSize - 2;

            // Verify allocation does not exceed parent boundary
            const fitsInParent = subnetBroadcastInt <= parentBroadcastInt && !hasOverflow;

            if (!fitsInParent) {
                hasOverflow = true;
                allocations.push({
                    name: req.name,
                    requiredHosts: req.hosts,
                    allocatedPrefix: `/${prefix}`,
                    mask: intToIp(maskInt),
                    network: '—',
                    usableRange: 'Insufficient Parent Capacity',
                    broadcast: '—',
                    availableHosts: 0,
                    status: 'INSUFFICIENT_SPACE',
                    originalIndex: req.originalIndex
                });
            } else {
                totalAllocatedAddresses += blockSize;
                allocations.push({
                    name: req.name,
                    requiredHosts: req.hosts,
                    allocatedPrefix: `/${prefix}`,
                    mask: intToIp(maskInt),
                    network: intToIp(subnetNetworkInt),
                    usableRange: `${intToIp(firstUsableInt)} – ${intToIp(lastUsableInt)}`,
                    broadcast: intToIp(subnetBroadcastInt),
                    availableHosts: usableHostsCount,
                    status: 'SUCCESS',
                    originalIndex: req.originalIndex
                });
                currentAddressInt = (subnetBroadcastInt + 1) >>> 0;
            }
        }

        // Restore original order for display clarity
        allocations.sort((a, b) => a.originalIndex - b.originalIndex);

        const efficiencyPercent = ((totalAllocatedAddresses / parentTotalAddresses) * 100).toFixed(1);

        return {
            error: null,
            wasNormalized: wasNormalized,
            enteredParent: enteredParent,
            normalizedParent: normalizedParent,
            hasDuplicateNames: hasDuplicateNames,
            parentNetwork: intToIp(parentNetworkInt),
            parentPrefix: parentPrefix,
            parentBroadcast: intToIp(parentBroadcastInt),
            parentTotalAddresses: parentTotalAddresses.toLocaleString(),
            totalAllocatedAddresses: totalAllocatedAddresses.toLocaleString(),
            efficiencyPercent: efficiencyPercent,
            hasOverflow: hasOverflow,
            allocations: allocations
        };
    }

    // Export to global namespace for testing and UI
    window.MJVlsmPlanner = {
        calculateVlsm: calculateVlsm,
        ipToInt: ipToInt,
        intToIp: intToIp
    };

    // DOM UI Initialization
    document.addEventListener('DOMContentLoaded', function() {
        const parentInput = document.getElementById('vlsm-parent-input');
        const rowsContainer = document.getElementById('vlsm-rows-container');
        const addRowBtn = document.getElementById('vlsm-add-row-btn');
        const calculateBtn = document.getElementById('vlsm-calc-btn');
        const preloadBtn = document.getElementById('vlsm-preload-btn');
        const errorAlert = document.getElementById('vlsm-error-alert');
        const resultsCard = document.getElementById('vlsm-results-card');
        const resultsTbody = document.getElementById('vlsm-results-tbody');
        const statsEl = document.getElementById('vlsm-stats-summary');

        if (!parentInput || !rowsContainer) return;

        let rowCount = 0;

        function createRow(nameVal = '', hostsVal = '') {
            if (rowsContainer.children.length >= 20) {
                alert('Maximum 20 subnet rows permitted.');
                return;
            }
            rowCount++;
            const rowDiv = document.createElement('div');
            rowDiv.className = 'vlsm-input-row';
            rowDiv.dataset.rowId = `row-${rowCount}`;

            const nameInput = document.createElement('input');
            nameInput.type = 'text';
            nameInput.className = 'form-control vlsm-name-input';
            nameInput.placeholder = 'e.g. Users VLAN';
            nameInput.value = nameVal;
            nameInput.setAttribute('aria-label', `Subnet ${rowCount} Name`);

            const hostsInput = document.createElement('input');
            hostsInput.type = 'number';
            hostsInput.className = 'form-control vlsm-hosts-input';
            hostsInput.placeholder = 'Hosts needed';
            hostsInput.min = '1';
            hostsInput.value = hostsVal;
            hostsInput.setAttribute('aria-label', `Subnet ${rowCount} Required Hosts`);

            const removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.className = 'btn btn-secondary btn-sm vlsm-remove-btn';
            removeBtn.innerHTML = '<i class="fa-solid fa-trash-can" aria-hidden="true"></i>';
            removeBtn.setAttribute('aria-label', `Remove Subnet ${rowCount}`);
            removeBtn.addEventListener('click', function() {
                if (rowsContainer.children.length > 1) {
                    rowDiv.remove();
                } else {
                    alert('You must have at least one subnet requirement.');
                }
            });

            rowDiv.appendChild(nameInput);
            rowDiv.appendChild(hostsInput);
            rowDiv.appendChild(removeBtn);
            rowsContainer.appendChild(rowDiv);
        }

        function preloadSampleData() {
            rowsContainer.innerHTML = '';
            parentInput.value = '192.168.10.0/24';
            createRow('LAN-A (Sales)', '100');
            createRow('LAN-B (Engineering)', '50');
            createRow('LAN-C (Servers)', '20');
            createRow('LAN-D (Management)', '10');
            runCalculation();
        }

        function runCalculation() {
            const parentVal = parentInput.value.trim();
            const rowEls = rowsContainer.querySelectorAll('.vlsm-input-row');
            const reqs = [];

            rowEls.forEach((r, idx) => {
                const name = r.querySelector('.vlsm-name-input').value.trim();
                const rawHosts = r.querySelector('.vlsm-hosts-input').value.trim();
                reqs.push({ name: name, hosts: rawHosts, id: `req-${idx}` });
            });

            const result = calculateVlsm(parentVal, reqs);

            if (result.error) {
                errorAlert.textContent = result.error;
                errorAlert.style.display = 'block';
                resultsCard.style.display = 'none';
                return;
            }

            errorAlert.style.display = 'none';
            resultsCard.style.display = 'block';

            // Visible disclosure if parent network was normalized
            const noticeEl = document.getElementById('vlsm-normalization-notice');
            if (noticeEl) {
                if (result.wasNormalized) {
                    noticeEl.textContent = `Parent Network Normalization Disclosure: Entered network: '${result.enteredParent}' contained host bits. Normalized parent network: '${result.normalizedParent}'.`;
                    noticeEl.style.display = 'block';
                } else {
                    noticeEl.style.display = 'none';
                }
            }

            // Render stats summary
            statsEl.textContent = `Parent: ${result.parentNetwork}/${result.parentPrefix} (${result.parentTotalAddresses} Total IPs) | Allocated: ${result.totalAllocatedAddresses} IPs (${result.efficiencyPercent}% Utilization)`;

            // Render table rows safely
            resultsTbody.innerHTML = '';
            result.allocations.forEach(alloc => {
                const tr = document.createElement('tr');
                if (alloc.status === 'INSUFFICIENT_SPACE') {
                    tr.className = 'table-row-error';
                }

                const tdName = document.createElement('td');
                tdName.textContent = alloc.name;
                tdName.style.fontWeight = '600';

                const tdReq = document.createElement('td');
                tdReq.textContent = alloc.requiredHosts.toLocaleString();

                const tdPrefix = document.createElement('td');
                const badge = document.createElement('span');
                badge.className = alloc.status === 'SUCCESS' ? 'badge badge-primary' : 'badge badge-danger';
                badge.textContent = alloc.allocatedPrefix;
                tdPrefix.appendChild(badge);

                const tdMask = document.createElement('td');
                tdMask.textContent = alloc.mask;

                const tdNet = document.createElement('td');
                tdNet.textContent = alloc.network;
                tdNet.className = 'font-mono';

                const tdRange = document.createElement('td');
                tdRange.textContent = alloc.usableRange;
                tdRange.className = 'font-mono';

                const tdBroad = document.createElement('td');
                tdBroad.textContent = alloc.broadcast;
                tdBroad.className = 'font-mono';

                const tdAvail = document.createElement('td');
                tdAvail.textContent = alloc.availableHosts.toLocaleString();

                tr.appendChild(tdName);
                tr.appendChild(tdReq);
                tr.appendChild(tdPrefix);
                tr.appendChild(tdMask);
                tr.appendChild(tdNet);
                tr.appendChild(tdRange);
                tr.appendChild(tdBroad);
                tr.appendChild(tdAvail);
                resultsTbody.appendChild(tr);
            });

            // Announce to screen reader
            const liveAnnouncer = document.getElementById('vlsm-live-announcer');
            if (liveAnnouncer) {
                liveAnnouncer.textContent = `VLSM calculated successfully. ${result.allocations.length} subnets planned inside ${result.parentNetwork}/${result.parentPrefix}.`;
            }
        }

        addRowBtn.addEventListener('click', () => createRow());
        preloadBtn.addEventListener('click', preloadSampleData);
        calculateBtn.addEventListener('click', runCalculation);

        // Initialize with default sample
        preloadSampleData();
    });
})();
