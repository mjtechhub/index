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
                    <i class="fas fa-search" aria-hidden="true"></i>
                    <input type="text" id="search-modal-input" class="search-modal-input" placeholder="Search tutorials, topics, commands..." aria-label="Search">
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
    let isFetching = false;
    let activeIndex = -1;
    let currentResults = [];

    // 3. Fetch Data Once
    async function getSearchData() {
        if (searchDataCache) return searchDataCache;
        if (isFetching) return null; // wait
        isFetching = true;
        
        let data = [];
        try {
            const [topicsRes, tutsRes] = await Promise.all([
                fetch(`${basePath}/data/topics.json`).catch(()=>null),
                fetch(`${basePath}/data/tutorials.json`).catch(()=>null)
            ]);
            
            if (topicsRes && topicsRes.ok) {
                const topics = await topicsRes.json();
                const allTopics = Array.isArray(topics) ? topics : ((topics.coreTopics || []).concat(topics.moreTopics || []));
                allTopics.forEach(t => {
                    data.push({
                        type: 'Topic',
                        title: t.name || t.id || 'Topic',
                        desc: t.description || '',
                        tags: t.id ? t.id.toLowerCase() : '',
                        url: t.url || `topics.html#${t.id}`
                    });
                });
            }
            
            if (tutsRes && tutsRes.ok) {
                const tuts = await tutsRes.json();
                const allTuts = Array.isArray(tuts) ? tuts : [];
                allTuts.forEach(t => {
                    const tutUrl = t.url ? t.url.replace('./', '') : '';
                    data.push({
                        type: 'Tutorial',
                        title: t.title || 'Tutorial',
                        desc: t.description || '',
                        tags: (t.keywords || '') + ' ' + (t.category || '').toLowerCase(),
                        url: tutUrl
                    });
                });
            }
            
            const cmdsRes = await fetch(`${basePath}/data/commands.json`).catch(()=>null);
            if (cmdsRes && cmdsRes.ok) {
                const cmds = await cmdsRes.json();
                cmds.forEach(c => {
                    data.push({
                        type: 'Command',
                        title: c.command,
                        desc: c.purpose,
                        tags: (c.platform || '').toLowerCase(),
                        url: 'commands.html'
                    });
                });
            }
            
            searchDataCache = data;
        } catch (e) {
            console.error("Search data load failed", e);
        }
        isFetching = false;
        return searchDataCache;
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
        
        return scored.sort((a, b) => b.score - a.score).slice(0, 12).map(r => r.item);
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
            if (!finalUrl.startsWith('http')) finalUrl = `${basePath}/${finalUrl}`;
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
                             res.type === 'Topic' ? 'fas fa-layer-group' : 'fas fa-book-open';
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
