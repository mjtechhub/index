/**
 * MJ Tech Hub - Global Search Module
 * Secure, fast, Ctrl+K accessible global search.
 */

(function() {
    if (window.mjSearchInitialized) return;
    window.mjSearchInitialized = true;

    // 1. Determine Base Path
    let basePath = '.';
    const scripts = document.getElementsByTagName('script');
    for (let script of scripts) {
        if (script.src && script.src.includes('js/search.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/search.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }

    // 2. Inject Modal HTML safely
    const modalHtml = `
        <div class="search-modal-backdrop" id="search-modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="search-modal-title">
            <div class="search-modal">
                <div class="search-modal-header">
                    <h2 id="search-modal-title" class="sr-only" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0;">Search MJ Tech Hub</h2>
                    <i class="fas fa-search" aria-hidden="true"></i>
                    <input type="text" id="search-modal-input" class="search-modal-input" placeholder="Search tutorials, topics, commands, resources..." aria-label="Search">
                    <button class="search-modal-close" id="search-modal-close" aria-label="Close search">ESC</button>
                </div>
                <div class="search-results-container" id="search-results-container">
                    <div class="search-empty-state" id="search-empty-state">
                        Type to start searching...
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    const backdrop = document.getElementById('search-modal-backdrop');
    const input = document.getElementById('search-modal-input');
    const resultsContainer = document.getElementById('search-results-container');
    const emptyState = document.getElementById('search-empty-state');
    
    let searchDataCache = null;
    let fetchPromise = null;
    let activeIndex = -1;
    let currentResults = [];

    // 3. Fetch Data Once
    function getSearchData() {
        if (searchDataCache) return Promise.resolve(searchDataCache);
        if (fetchPromise) return fetchPromise;
        
        fetchPromise = (async () => {
            let data = [];
            try {
            const [topicsRes, tutsRes, cmdsRes, resRes, labsRes, quizRes] = await Promise.all([
                fetch(`${basePath}/data/topics.json`).catch(()=>null),
                fetch(`${basePath}/data/tutorials.json`).catch(()=>null),
                fetch(`${basePath}/data/commands.json`).catch(()=>null),
                fetch(`${basePath}/data/resources.json`).catch(()=>null),
                fetch(`${basePath}/data/troubleshooting-labs.json`).catch(()=>null),
                fetch(`${basePath}/data/quizzes.json`).catch(()=>null)
            ]);
            
            if (topicsRes && topicsRes.ok) {
                const topics = await topicsRes.json();
                const categories = Array.isArray(topics) ? topics : (topics.categories || (topics.coreTopics || []).concat(topics.moreTopics || []));
                categories.forEach(t => {
                    data.push({
                        type: 'Topic',
                        title: t.name || t.id || 'Topic',
                        desc: t.description || '',
                        tags: `${t.keywords || ''} ${t.id ? t.id.toLowerCase() : ''}`,
                        url: t.url || `topics.html#${t.id}`
                    });

                    // Index published subtopics only (prevent planned curriculum entries from flooding search)
                    if (Array.isArray(t.sections)) {
                        t.sections.forEach(sec => {
                            const secName = sec.name || sec.title || '';
                            const catName = t.name || t.id || 'Topic';
                            if (Array.isArray(sec.subtopics)) {
                                sec.subtopics.forEach(sub => {
                                    if (sub.status === 'published' && sub.url) {
                                        const subName = sub.name || sub.title || sub.id || 'Lesson';
                                        const subId = sub.id ? String(sub.id).toLowerCase() : '';
                                        data.push({
                                            type: 'Topic',
                                            title: subName,
                                            desc: `${secName ? secName + ' in ' : ''}${catName} (${sub.level || 'Tutorial'})`,
                                            tags: `${catName.toLowerCase()} ${secName.toLowerCase()} ${subId}`,
                                            url: sub.url
                                        });
                                    }
                                });
                            }
                        });
                    }
                });
            }
            
            if (tutsRes && tutsRes.ok) {
                const tuts = await tutsRes.json();
                const allTuts = Array.isArray(tuts) ? tuts : (tuts.tutorials || []);
                allTuts.forEach(t => {
                    const tutUrl = t.url ? t.url.replace('./', '') : '';
                    data.push({
                        type: 'Tutorial',
                        title: t.title || 'Tutorial',
                        desc: t.description || '',
                        tags: `${t.keywords || ''} ${(t.category || '').toLowerCase()}`,
                        url: tutUrl
                    });
                });
            }
            
            if (cmdsRes && cmdsRes.ok) {
                const cmds = await cmdsRes.json();
                if (Array.isArray(cmds)) {
                    cmds.forEach(c => {
                        data.push({
                            type: 'Command',
                            title: c.command,
                            desc: c.purpose,
                            tags: `${(c.platform || '').toLowerCase()} ${(c.category || '').toLowerCase()} ${c.useCase || ''} ${Array.isArray(c.keywords) ? c.keywords.join(' ') : ''}`,
                            url: 'commands.html'
                        });
                    });
                }
            }

            if (resRes && resRes.ok) {
                const resources = await resRes.json();
                if (Array.isArray(resources)) {
                    resources.forEach(r => {
                        data.push({
                            type: 'Resource',
                            title: r.title,
                            desc: r.description,
                            tags: `${r.tags || ''} ${(r.category || '').toLowerCase()} ${(r.type || '').toLowerCase()}`,
                            url: r.url
                        });
                    });
                }
            }

            // Index 4 Interactive IT Tools
            const interactiveTools = [
                {
                    type: 'Tool',
                    title: 'Subnet & CIDR Calculator',
                    desc: 'IPv4 Subnet & CIDR Calculator: calculate network IDs, broadcast, wildcard masks, usable host ranges, and binary layout (/0 to /32).',
                    tags: 'subnet calculator cidr calculator ip addressing mask network rfc 1918 rfc 3021 ipv4',
                    url: 'tools/subnet-calculator.html'
                },
                {
                    type: 'Tool',
                    title: 'VLSM / Subnet Planner',
                    desc: 'Variable Length Subnet Masking (VLSM) planner: largest-first non-overlapping subnet allocations with parent boundary capacity validation.',
                    tags: 'vlsm subnet planner variable length subnet masking vlan host allocation ip planning',
                    url: 'tools/vlsm-planner.html'
                },
                {
                    type: 'Tool',
                    title: 'Network Diagnostic Workbench',
                    desc: 'Interactive troubleshooting decision workbench: isolate TCP/IP issues across Gateway, WAN, DNS, and Port layers with recommended commands.',
                    tags: 'network diagnostic workbench troubleshooting ping dns port gateway fault domain isolate',
                    url: 'tools/network-diagnostic-workbench.html'
                },
                {
                    type: 'Tool',
                    title: 'Port & Protocol Reference',
                    desc: 'Searchable directory of enterprise network ports, transport protocols (TCP/UDP/IP Protocol), and objective security hardening notes.',
                    tags: 'port protocol reference dns http https rdp ssh kerberos bgp ldap syslog snmp enterprise directory',
                    url: 'tools/port-reference.html'
                }
            ];
            interactiveTools.forEach(tool => data.push(tool));

            // Index 6 Guided Troubleshooting Labs (Top-level landing entries)
            if (labsRes && labsRes.ok) {
                const labs = await labsRes.json();
                if (Array.isArray(labs)) {
                    labs.forEach(lab => {
                        data.push({
                            type: 'Lab',
                            title: `Lab: ${lab.title}`,
                            desc: `[${lab.category} Lab] ${lab.symptoms} (${lab.level}, ${lab.estimatedTime})`,
                            tags: `lab troubleshooting simulation incident rca ${lab.category.toLowerCase()} ${lab.level.toLowerCase()}`,
                            url: `labs.html?lab=${lab.id}`
                        });
                    });
                }
            }

            // Index 8 Practice Quiz Modules (Individual quiz assessment targets)
            if (quizRes && quizRes.ok) {
                const quizzes = await quizRes.json();
                if (Array.isArray(quizzes)) {
                    quizzes.forEach(q => {
                        const qCount = Array.isArray(q.questions) ? q.questions.length : 8;
                        data.push({
                            type: 'Quiz',
                            title: `Quiz: ${q.title}`,
                            desc: `${q.description || ''} (${qCount} Questions, ${q.category || 'General'})`,
                            tags: `quiz practice test assessment exam questions ${(q.category || '').toLowerCase()} ${(q.id || '').toLowerCase()}`,
                            url: `quiz.html?quiz=${encodeURIComponent(q.id)}`
                        });
                    });
                }
            }
            
            searchDataCache = data;
            return searchDataCache;
        } catch (e) {
            console.error("Search data load failed", e);
            return [];
        } finally {
            fetchPromise = null;
        }
        })();
        return fetchPromise;
    }

    // 4. Ranking Algorithm
    function rankResults(query, data) {
        const q = query.toLowerCase().trim();
        if (!q) return [];
        
        const scored = data.map(item => {
            let score = 0;
            const t = (item.title || '').toLowerCase();
            const d = (item.desc || '').toLowerCase();
            const tags = (item.tags || '').toLowerCase();
            
            if (t === q) score += 100;
            else if (t.startsWith(q)) score += 80;
            else if (t.includes(q)) score += 60;
            
            if (tags.includes(q)) score += 45;
            
            if (d.includes(q)) score += 20;

            // Multi-word query support (e.g. "Subnet Calculator" matching "Subnet & CIDR Calculator")
            const words = q.split(/\s+/).filter(w => w.length > 1);
            if (words.length > 1) {
                if (words.every(w => t.includes(w))) score += 55;
                else if (words.every(w => tags.includes(w) || t.includes(w))) score += 40;
            }
            
            return { item, score };
        }).filter(r => r.score > 0);
        
        if (scored.length === 0 && q.length > 3) {
            data.forEach(item => {
                const t = (item.title || '').toLowerCase();
                let matches = 0;
                for (let i=0; i<q.length; i++) {
                    if (t.includes(q[i])) matches++;
                }
                if (matches / q.length > 0.8) {
                    scored.push({ item, score: 10 });
                }
            });
        }
        
        const seenKeys = new Set();
        const uniqueResults = [];
        for (let r of scored.sort((a, b) => b.score - a.score)) {
            const normUrl = (r.item.url || '').replace(/^\.?\//, '');
            const dedupKey = normUrl.includes('tutorials/') ? normUrl : `${r.item.type}:${r.item.title}:${normUrl}`;
            if (seenKeys.has(dedupKey)) continue;
            seenKeys.add(dedupKey);
            uniqueResults.push(r.item);
            if (uniqueResults.length >= 12) break;
        }
        return uniqueResults;
    }

    // 5. Safe Rendering
    function renderResults(results, query) {
        resultsContainer.innerHTML = '';
        currentResults = results;
        activeIndex = -1;
        
        if (results.length === 0) {
            emptyState.textContent = `No results found for "${query}"`;
            resultsContainer.appendChild(emptyState);
            return;
        }
        
        results.forEach((res, index) => {
            const a = document.createElement('a');
            a.className = 'search-result-item';
            
            let finalUrl = res.url;
            if (finalUrl.startsWith('/')) finalUrl = finalUrl.substring(1);
            if (!finalUrl.startsWith('http')) {
                finalUrl = `${basePath}/${finalUrl}`;
            } else {
                a.target = '_blank';
                a.rel = 'noopener noreferrer';
            }
            a.href = finalUrl;
            
            const titleEl = document.createElement('div');
            titleEl.className = 'search-result-title';
            titleEl.textContent = res.title;
            
            const descEl = document.createElement('div');
            descEl.className = 'search-result-desc';
            descEl.textContent = res.desc;
            
            const metaEl = document.createElement('div');
            metaEl.className = 'search-result-meta';
            const icon = document.createElement('i');
            icon.className = res.type === 'Command' ? 'fas fa-terminal' : 
                             res.type === 'Topic' ? 'fas fa-layer-group' : 
                             res.type === 'Resource' ? 'fas fa-folder-open' :
                             res.type === 'Tool' ? 'fas fa-calculator' :
                             res.type === 'Lab' ? 'fas fa-flask-vial' :
                             res.type === 'Quiz' ? 'fas fa-brain' : 'fas fa-book-open';
            icon.setAttribute('aria-hidden', 'true');
            metaEl.appendChild(icon);
            metaEl.appendChild(document.createTextNode(' ' + res.type));
            
            a.appendChild(titleEl);
            a.appendChild(descEl);
            a.appendChild(metaEl);
            
            a.addEventListener('mouseenter', () => setActiveIndex(index));
            resultsContainer.appendChild(a);
        });
    }

    function setActiveIndex(index) {
        const items = resultsContainer.querySelectorAll('.search-result-item');
        items.forEach((item, i) => {
            if (i === index) item.classList.add('active');
            else item.classList.remove('active');
        });
        activeIndex = index;
        if (index >= 0 && index < items.length) {
            items[index].scrollIntoView({ block: 'nearest' });
        }
    }

    // 6. Event Listeners
    function openSearch() {
        backdrop.classList.add('active');
        input.value = '';
        resultsContainer.innerHTML = '';
        emptyState.textContent = 'Type to start searching...';
        resultsContainer.appendChild(emptyState);
        getSearchData();
        setTimeout(() => input.focus(), 50);
    }

    function closeSearch() {
        backdrop.classList.remove('active');
    }

    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            openSearch();
        }
        
        if (e.key === 'Escape' && backdrop.classList.contains('active')) {
            closeSearch();
        }
    });

    document.addEventListener('click', (e) => {
        if (e.target.closest('.search-box')) {
            openSearch();
        }
        if (e.target === backdrop) {
            closeSearch();
        }
    });
    
    document.getElementById('search-modal-close').addEventListener('click', closeSearch);

    input.addEventListener('input', async (e) => {
        const query = e.target.value;
        if (!query.trim()) {
            resultsContainer.innerHTML = '';
            emptyState.textContent = 'Type to start searching...';
            resultsContainer.appendChild(emptyState);
            return;
        }
        
        const data = await getSearchData();
        if (data) {
            const results = rankResults(query, data);
            renderResults(results, query.trim());
        } else {
            resultsContainer.innerHTML = '';
            emptyState.textContent = 'Loading search index...';
            resultsContainer.appendChild(emptyState);
        }
    });

    input.addEventListener('keydown', (e) => {
        if (!currentResults.length) return;
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            let n = activeIndex + 1;
            if (n >= currentResults.length) n = 0;
            setActiveIndex(n);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            let n = activeIndex - 1;
            if (n < 0) n = currentResults.length - 1;
            setActiveIndex(n);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (activeIndex >= 0 && activeIndex < currentResults.length) {
                const items = resultsContainer.querySelectorAll('.search-result-item');
                if (items[activeIndex]) items[activeIndex].click();
            }
        }
    });

})();
