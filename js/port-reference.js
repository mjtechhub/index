/**
 * MJ Tech Hub - Port & Protocol Reference Engine
 * Searchable, filterable enterprise port reference with security context.
 */

(function() {
    'use strict';

    let portsData = [];
    let activeCategory = 'all';
    let activeTransport = 'all';
    let searchQuery = '';

    // Determine Base Path
    let basePath = '.';
    const scripts = document.getElementsByTagName('script');
    for (let script of scripts) {
        if (script.src && script.src.includes('js/port-reference.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/port-reference.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }

    async function loadPortsData() {
        try {
            const res = await fetch(`${basePath}/data/ports.json`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            portsData = await res.json();
            renderPorts();
        } catch (err) {
            console.error('Failed to load ports.json:', err);
            const container = document.getElementById('ports-grid');
            if (container) {
                container.innerHTML = '<div class="alert alert-danger">Failed to load port reference data. Please refresh the page.</div>';
            }
        }
    }

    function filterPorts() {
        return portsData.filter(item => {
            // Category filter
            if (activeCategory !== 'all' && item.category !== activeCategory) {
                return false;
            }

            // Transport filter
            if (activeTransport !== 'all') {
                if (activeTransport === 'TCP' && item.transport !== 'TCP' && item.transport !== 'TCP/UDP') return false;
                if (activeTransport === 'UDP' && item.transport !== 'UDP' && item.transport !== 'TCP/UDP') return false;
                if (activeTransport === 'IP Protocol' && item.transport !== 'IP Protocol') return false;
            }

            // Search query filter
            if (searchQuery) {
                const q = searchQuery.toLowerCase();
                const matchService = item.service.toLowerCase().includes(q);
                const matchPort = item.port ? item.port.toLowerCase().includes(q) : false;
                const matchProtoNum = item.protocolNumber ? String(item.protocolNumber).includes(q) : false;
                const matchDesc = item.description.toLowerCase().includes(q);
                const matchNotes = item.securityNotes.toLowerCase().includes(q);
                const matchKeywords = Array.isArray(item.keywords) && item.keywords.some(k => k.toLowerCase().includes(q));
                if (!matchService && !matchPort && !matchProtoNum && !matchDesc && !matchNotes && !matchKeywords) {
                    return false;
                }
            }

            return true;
        });
    }

    function renderPorts() {
        const grid = document.getElementById('ports-grid');
        const counter = document.getElementById('ports-count-badge');
        const emptyState = document.getElementById('ports-empty-state');
        const liveAnnouncer = document.getElementById('ports-live-announcer');

        if (!grid) return;

        const filtered = filterPorts();

        if (counter) {
            counter.textContent = `${filtered.length} of ${portsData.length} Protocols`;
        }

        if (filtered.length === 0) {
            grid.innerHTML = '';
            if (emptyState) emptyState.style.display = 'block';
            if (liveAnnouncer) liveAnnouncer.textContent = 'No matching ports or protocols found.';
            return;
        }

        if (emptyState) emptyState.style.display = 'none';
        grid.innerHTML = '';

        filtered.forEach(item => {
            const card = document.createElement('article');
            card.className = 'port-card';
            card.id = item.id;

            // Header row with port number badge and service title
            const header = document.createElement('div');
            header.className = 'port-card-header';

            const titleWrap = document.createElement('div');
            titleWrap.className = 'port-title-wrap';

            const portBadge = document.createElement('span');
            portBadge.className = 'port-number-badge';
            portBadge.textContent = item.port !== null ? item.port : `IP Proto ${item.protocolNumber}`;

            const serviceTitle = document.createElement('h3');
            serviceTitle.className = 'port-service-title';
            serviceTitle.textContent = item.service;

            titleWrap.appendChild(portBadge);
            titleWrap.appendChild(serviceTitle);

            const badgesWrap = document.createElement('div');
            badgesWrap.className = 'port-badges-wrap';

            const transportBadge = document.createElement('span');
            transportBadge.className = 'badge badge-primary';
            transportBadge.textContent = item.transport;

            const catBadge = document.createElement('span');
            catBadge.className = 'badge badge-secondary';
            catBadge.textContent = item.category;

            badgesWrap.appendChild(transportBadge);
            badgesWrap.appendChild(catBadge);

            header.appendChild(titleWrap);
            header.appendChild(badgesWrap);

            // Description
            const desc = document.createElement('p');
            desc.className = 'port-card-desc';
            desc.textContent = item.description;

            // Security Notes Callout
            const secNotes = document.createElement('div');
            secNotes.className = 'port-sec-notes';
            
            const secIcon = document.createElement('i');
            secIcon.className = 'fa-solid fa-shield-halved port-sec-icon';
            secIcon.setAttribute('aria-hidden', 'true');

            const secText = document.createElement('div');
            secText.className = 'port-sec-text';
            secText.innerHTML = `<strong>Security & Hardening:</strong> `;
            secText.appendChild(document.createTextNode(item.securityNotes));

            secNotes.appendChild(secIcon);
            secNotes.appendChild(secText);

            // Footer actions (1-click copy)
            const footer = document.createElement('div');
            footer.className = 'port-card-footer';

            const copyBtn = document.createElement('button');
            copyBtn.type = 'button';
            copyBtn.className = 'btn btn-secondary btn-sm port-copy-btn';
            const copyText = item.port !== null ? item.port : `IP Protocol ${item.protocolNumber}`;
            const copyLabel = item.port !== null ? `Copy ${item.service} port ${item.port}` : `Copy ${item.service} IP protocol ${item.protocolNumber}`;
            copyBtn.innerHTML = `<i class="fa-solid fa-copy" aria-hidden="true"></i> ${item.port !== null ? 'Copy Port' : 'Copy Proto #'}`;
            copyBtn.setAttribute('aria-label', copyLabel);
            copyBtn.addEventListener('click', function() {
                navigator.clipboard.writeText(copyText).then(() => {
                    copyBtn.innerHTML = `<i class="fa-solid fa-check" aria-hidden="true"></i> Copied!`;
                    setTimeout(() => {
                        copyBtn.innerHTML = `<i class="fa-solid fa-copy" aria-hidden="true"></i> ${item.port !== null ? 'Copy Port' : 'Copy Proto #'}`;
                    }, 1800);
                });
            });

            footer.appendChild(copyBtn);

            card.appendChild(header);
            card.appendChild(desc);
            card.appendChild(secNotes);
            card.appendChild(footer);

            grid.appendChild(card);
        });

        if (liveAnnouncer) {
            liveAnnouncer.textContent = `Showing ${filtered.length} matching enterprise protocols.`;
        }
    }

    // Export to global for automated testing
    window.MJPortReference = {
        loadPortsData: loadPortsData,
        filterPorts: filterPorts,
        setSearch: (q) => { searchQuery = q; renderPorts(); },
        setCategory: (c) => { activeCategory = c; renderPorts(); },
        setTransport: (t) => { activeTransport = t; renderPorts(); }
    };

    // DOM UI Initialization
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('ports-search-input');
        const catPills = document.querySelectorAll('.ports-cat-pill');
        const transportPills = document.querySelectorAll('.ports-transport-pill');

        if (searchInput) {
            searchInput.addEventListener('input', function(e) {
                searchQuery = e.target.value.trim();
                renderPorts();
            });
        }

        catPills.forEach(pill => {
            pill.addEventListener('click', function() {
                catPills.forEach(p => {
                    p.classList.remove('active');
                    p.removeAttribute('aria-current');
                });
                pill.classList.add('active');
                pill.setAttribute('aria-current', 'true');
                activeCategory = pill.dataset.category || 'all';
                renderPorts();
            });
        });

        transportPills.forEach(pill => {
            pill.addEventListener('click', function() {
                transportPills.forEach(p => {
                    p.classList.remove('active');
                    p.removeAttribute('aria-current');
                });
                pill.classList.add('active');
                pill.setAttribute('aria-current', 'true');
                activeTransport = pill.dataset.transport || 'all';
                renderPorts();
            });
        });

        loadPortsData();
    });
})();
