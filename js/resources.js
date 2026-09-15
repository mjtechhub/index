/**
 * MJ Tech Hub - Curated Resources Module (js/resources.js)
 * Data-driven external reference library with safe DOM rendering, filtering, search, and accessible navigation.
 */

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('curated-resources-container');
    const filterTabsContainer = document.getElementById('resource-category-filters');
    const searchInput = document.getElementById('resources-search-input');
    const counter = document.getElementById('resources-counter');

    if (!container) return;

    // Base Path Resolution
    const scripts = document.getElementsByTagName('script');
    let basePath = '.';
    for (let script of scripts) {
        if (script.src && script.src.includes('js/resources.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/resources.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }

    let allResources = [];
    let externalResources = [];
    let activeFilter = 'All';
    let searchQuery = '';

    showLoadingState();

    fetch(`${basePath}/data/resources.json`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch resources');
            return response.json();
        })
        .then(data => {
            allResources = Array.isArray(data) ? data : [];
            // Focus curated section on external authoritative resources (http/https)
            externalResources = allResources.filter(r => r.url && r.url.startsWith('http'));
            setupCategoryFilters(externalResources);
            setupSearch();
            applyFilterAndSearch();
        })
        .catch(error => {
            console.error('Error loading resources:', error);
            showErrorState('Failed to load curated resource library. Please refresh or try again later.');
        });

    function showLoadingState() {
        container.innerHTML = '';
        const stateDiv = document.createElement('div');
        stateDiv.className = 'category-empty-state';
        stateDiv.style.gridColumn = '1 / -1';
        stateDiv.style.padding = '3rem';
        stateDiv.style.textAlign = 'center';

        const icon = document.createElement('div');
        icon.className = 'empty-state-icon';
        icon.setAttribute('aria-hidden', 'true');
        icon.style.fontSize = '2rem';
        icon.style.marginBottom = '1rem';
        icon.style.color = 'var(--text-muted)';
        const i = document.createElement('i');
        i.className = 'fa-solid fa-spinner fa-spin';
        icon.appendChild(i);

        const title = document.createElement('h3');
        title.className = 'empty-state-title';
        title.style.marginBottom = '0.5rem';
        title.textContent = 'Loading Curated Resources...';

        const desc = document.createElement('p');
        desc.className = 'empty-state-desc';
        desc.style.color = 'var(--text-secondary)';
        desc.textContent = 'Fetching verified documentation, standards, and references.';

        stateDiv.appendChild(icon);
        stateDiv.appendChild(title);
        stateDiv.appendChild(desc);
        container.appendChild(stateDiv);
    }

    function showErrorState(msg) {
        container.innerHTML = '';
        const stateDiv = document.createElement('div');
        stateDiv.className = 'category-empty-state';
        stateDiv.style.gridColumn = '1 / -1';
        stateDiv.style.padding = '2rem';
        stateDiv.style.textAlign = 'center';

        const p = document.createElement('p');
        p.className = 'text-danger';
        p.textContent = msg || 'Failed to load curated resource library. Please refresh or try again later.';
        stateDiv.appendChild(p);
        container.appendChild(stateDiv);
    }

    function showEmptyFilterState() {
        container.innerHTML = '';
        const stateDiv = document.createElement('div');
        stateDiv.className = 'category-empty-state';
        stateDiv.style.gridColumn = '1 / -1';
        stateDiv.style.padding = '3rem';
        stateDiv.style.textAlign = 'center';

        const icon = document.createElement('div');
        icon.className = 'empty-state-icon';
        icon.setAttribute('aria-hidden', 'true');
        icon.style.fontSize = '2rem';
        icon.style.marginBottom = '1rem';
        icon.style.color = 'var(--text-muted)';
        const i = document.createElement('i');
        i.className = 'fa-solid fa-book-bookmark';
        icon.appendChild(i);

        const title = document.createElement('h3');
        title.className = 'empty-state-title';
        title.style.marginBottom = '0.5rem';
        title.textContent = 'No resources match your search';

        const desc = document.createElement('p');
        desc.className = 'empty-state-desc';
        desc.style.color = 'var(--text-secondary)';
        desc.textContent = 'Try clearing your search query or choosing another category.';

        stateDiv.appendChild(icon);
        stateDiv.appendChild(title);
        stateDiv.appendChild(desc);
        container.appendChild(stateDiv);
    }

    function setupCategoryFilters(resources) {
        if (!filterTabsContainer) return;
        filterTabsContainer.innerHTML = '';

        const categories = ['All'];
        resources.forEach(r => {
            if (r.category && !categories.includes(r.category)) {
                categories.push(r.category);
            }
        });

        categories.forEach(cat => {
            const btn = document.createElement('button');
            btn.className = `cmd-filter-btn ${cat === 'All' ? 'active' : ''}`;
            btn.setAttribute('role', 'tab');
            btn.setAttribute('aria-selected', cat === 'All' ? 'true' : 'false');
            
            const count = cat === 'All' ? resources.length : resources.filter(r => r.category === cat).length;
            btn.textContent = `${cat} (${count})`;

            btn.addEventListener('click', () => {
                filterTabsContainer.querySelectorAll('.cmd-filter-btn').forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                btn.classList.add('active');
                btn.setAttribute('aria-selected', 'true');
                activeFilter = cat;
                applyFilterAndSearch();
            });
            filterTabsContainer.appendChild(btn);
        });
    }

    function setupSearch() {
        if (!searchInput) return;
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            applyFilterAndSearch();
        });
    }

    function applyFilterAndSearch() {
        let filtered = externalResources;

        if (activeFilter !== 'All') {
            filtered = filtered.filter(r => r.category === activeFilter);
        }

        if (searchQuery) {
            filtered = filtered.filter(r => {
                const title = (r.title || '').toLowerCase();
                const desc = (r.description || '').toLowerCase();
                const provider = (r.provider || '').toLowerCase();
                const tags = (r.tags || '').toLowerCase();
                const type = (r.type || '').toLowerCase();
                return title.includes(searchQuery) || desc.includes(searchQuery) || provider.includes(searchQuery) || tags.includes(searchQuery) || type.includes(searchQuery);
            });
        }

        if (counter) {
            counter.textContent = `Showing ${filtered.length} of ${externalResources.length} verified external resources`;
        }

        renderResourceList(filtered);
    }

    function renderResourceList(resources) {
        container.innerHTML = '';

        if (resources.length === 0) {
            showEmptyFilterState();
            return;
        }

        resources.forEach(res => {
            const card = document.createElement('div');
            card.className = 'about-card';
            card.style.display = 'flex';
            card.style.flexDirection = 'column';
            card.style.height = '100%';
            card.style.transition = 'transform 0.2s ease, box-shadow 0.2s ease';

            const provider = res.provider || 'Authoritative Source';
            const resType = res.type || 'Official Documentation';
            const cat = res.category || 'General';

            // Top Badges Row
            const topRow = document.createElement('div');
            topRow.style.display = 'flex';
            topRow.style.justifyContent = 'space-between';
            topRow.style.alignItems = 'flex-start';
            topRow.style.gap = '0.5rem';
            topRow.style.marginBottom = '1rem';
            topRow.style.flexWrap = 'wrap';

            const catPill = document.createElement('span');
            catPill.className = 'meta-pill meta-pill-brand';
            catPill.style.fontSize = '0.75rem';
            const catIcon = document.createElement('i');
            catIcon.className = 'fa-solid fa-layer-group';
            catIcon.setAttribute('aria-hidden', 'true');
            catIcon.style.marginRight = '0.35rem';
            catPill.appendChild(catIcon);
            catPill.appendChild(document.createTextNode(cat));

            const typePill = document.createElement('span');
            typePill.className = 'meta-pill';
            typePill.style.fontSize = '0.75rem';
            typePill.style.background = 'var(--bg-secondary)';
            typePill.textContent = resType;

            topRow.appendChild(catPill);
            topRow.appendChild(typePill);

            // Provider Row
            const providerRow = document.createElement('div');
            providerRow.style.display = 'flex';
            providerRow.style.alignItems = 'center';
            providerRow.style.gap = '0.5rem';
            providerRow.style.marginBottom = '0.5rem';

            const provIcon = document.createElement('i');
            provIcon.className = 'fa-solid fa-building-columns';
            provIcon.style.color = 'var(--brand-primary)';
            provIcon.style.fontSize = '0.9rem';
            provIcon.setAttribute('aria-hidden', 'true');

            const provSpan = document.createElement('span');
            provSpan.style.fontSize = '0.85rem';
            provSpan.style.fontWeight = '600';
            provSpan.style.color = 'var(--text-muted)';
            provSpan.style.textTransform = 'uppercase';
            provSpan.style.letterSpacing = '0.5px';
            provSpan.textContent = provider;

            providerRow.appendChild(provIcon);
            providerRow.appendChild(provSpan);

            // Title
            const titleEl = document.createElement('h3');
            titleEl.style.fontSize = '1.15rem';
            titleEl.style.marginBottom = '0.75rem';
            titleEl.style.lineHeight = '1.4';
            titleEl.style.color = 'var(--text-primary)';
            titleEl.textContent = res.title || '';

            // Description
            const descEl = document.createElement('p');
            descEl.style.flexGrow = '1';
            descEl.style.fontSize = '0.95rem';
            descEl.style.lineHeight = '1.6';
            descEl.style.color = 'var(--text-secondary)';
            descEl.style.marginBottom = '1.5rem';
            descEl.textContent = res.description || '';

            // External Link Button
            const linkEl = document.createElement('a');
            linkEl.setAttribute('href', res.url || '#');
            linkEl.setAttribute('target', '_blank');
            linkEl.setAttribute('rel', 'noopener noreferrer');
            linkEl.className = 'btn btn-secondary';
            linkEl.style.width = '100%';
            linkEl.style.textAlign = 'center';
            linkEl.style.display = 'inline-flex';
            linkEl.style.alignItems = 'center';
            linkEl.style.justifyContent = 'center';
            linkEl.style.gap = '0.5rem';
            linkEl.setAttribute('aria-label', `Visit ${res.title || 'Resource'} (opens in new tab)`);

            const linkText = document.createElement('span');
            linkText.textContent = 'Visit Resource';

            const linkIcon = document.createElement('i');
            linkIcon.className = 'fa-solid fa-arrow-up-right-from-square';
            linkIcon.setAttribute('aria-hidden', 'true');
            linkIcon.style.fontSize = '0.85rem';

            linkEl.appendChild(linkText);
            linkEl.appendChild(linkIcon);

            // Assemble Card
            card.appendChild(topRow);
            card.appendChild(providerRow);
            card.appendChild(titleEl);
            card.appendChild(descEl);
            card.appendChild(linkEl);

            container.appendChild(card);
        });
    }
});
