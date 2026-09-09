/**
 * MJ Tech Hub - Unified Category Engine (js/category.js)
 * Single reusable renderer powering all category pages:
 * networking.html, windows.html, linux.html, servers.html, cybersecurity.html, cloud.html.
 */

document.addEventListener('DOMContentLoaded', () => {
    const mainContainer = document.querySelector('main[data-category]') || document.getElementById('main-content');
    if (!mainContainer) return;

    // 1. Determine Category Slug
    let catSlug = mainContainer.getAttribute('data-category');
    if (!catSlug) {
        const path = window.location.pathname.toLowerCase();
        if (path.includes('networking')) catSlug = 'networking';
        else if (path.includes('windows')) catSlug = 'windows';
        else if (path.includes('linux')) catSlug = 'linux';
        else if (path.includes('servers')) catSlug = 'servers';
        else if (path.includes('cybersecurity')) catSlug = 'cybersecurity';
        else if (path.includes('cloud')) catSlug = 'cloud';
        else catSlug = 'networking';
    }
    catSlug = catSlug.toLowerCase().trim();
    // Normalize cloud-ai to cloud canonical ID
    if (catSlug === 'cloud-ai') catSlug = 'cloud';

    // 2. Base Path Resolution
    const scripts = document.getElementsByTagName('script');
    let basePath = '.';
    for (let script of scripts) {
        if (script.src && script.src.includes('js/category.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/category.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }

    // 3. Fetch Data Concurrently
    Promise.all([
        fetch(`${basePath}/data/topics.json`).then(r => r.ok ? r.json() : { categories: [] }).catch(() => ({ categories: [] })),
        fetch(`${basePath}/data/tutorials.json`).then(r => r.ok ? r.json() : []).catch(() => [])
    ]).then(([topicsData, tutsData]) => {
        const categories = topicsData.categories || [];
        const tutorials = Array.isArray(tutsData) ? tutsData : [];

        // Match Category in topics.json
        const currentCat = categories.find(c => {
            const cid = (c.id || '').toLowerCase();
            return cid === catSlug || (catSlug === 'cloud' && (cid === 'cloud' || cid === 'cloud-ai'));
        }) || {
            id: catSlug,
            name: catSlug.charAt(0).toUpperCase() + catSlug.slice(1),
            description: 'Tutorials and guides for ' + catSlug,
            icon: `./assets/icons/${catSlug}.png`,
            accent: catSlug,
            sections: []
        };

        // Filter Tutorials for this Category
        const categoryTutorials = tutorials.filter(t => {
            const tCat = (t.category || '').toLowerCase().trim();
            if (catSlug === 'cloud') {
                return tCat.includes('cloud') || tCat.includes('ai');
            }
            return tCat === catSlug || tCat === currentCat.name.toLowerCase();
        });

        renderCategoryPage(currentCat, categoryTutorials, categories, basePath);
    }).catch(err => {
        console.error('Error loading category data:', err);
        const contentMount = document.getElementById('category-content');
        if (contentMount) {
            contentMount.innerHTML = `<div class="category-empty-state"><p class="text-danger">Failed to load category data. Please refresh or try again later.</p></div>`;
        }
    });

    // 4. Master Page Renderer
    function renderCategoryPage(cat, tuts, allCategories, basePath) {
        // A. Render Breadcrumb
        const breadcrumbMount = document.getElementById('category-breadcrumb');
        if (breadcrumbMount) {
            breadcrumbMount.innerHTML = `
                <a href="${basePath}/index.html">Home</a>
                <span class="breadcrumb-separator" aria-hidden="true">/</span>
                <a href="${basePath}/topics.html">Topics</a>
                <span class="breadcrumb-separator" aria-hidden="true">/</span>
                <span aria-current="page">${cat.name}</span>
            `;
        }

        // B. Render Category Hero
        const heroMount = document.getElementById('category-hero');
        if (heroMount) {
            const hasTutorials = tuts.length > 0;
            const sectionsCount = Array.isArray(cat.sections) ? cat.sections.length : 0;
            const totalCurriculumTopics = Array.isArray(cat.sections) ? cat.sections.reduce((acc, s) => acc + (Array.isArray(s.subtopics) ? s.subtopics.length : 0), 0) : 0;
            const accentVar = `var(--cat-${cat.accent || cat.id}, var(--brand-primary))`;

            heroMount.innerHTML = `
                <div class="page-hero-header">
                    <div class="page-hero-icon" aria-hidden="true" style="border-top: 3px solid ${accentVar};">
                        <img src="${basePath}/${cat.icon.replace('./', '')}" alt="" width="38" height="38" style="object-fit: contain;">
                    </div>
                    <div class="page-hero-body">
                        <h1 class="page-hero-title">${cat.name}</h1>
                        <p class="page-hero-desc">${cat.description}</p>
                        <div class="page-hero-meta">
                            <span class="meta-pill ${hasTutorials ? 'meta-pill-brand' : ''}">
                                <i class="fa-solid fa-book-open" aria-hidden="true"></i> ${tuts.length} Published ${tuts.length === 1 ? 'Tutorial' : 'Tutorials'}
                            </span>
                            ${totalCurriculumTopics > 0 ? `
                                <span class="meta-pill">
                                    <i class="fa-solid fa-graduation-cap" aria-hidden="true"></i> ${totalCurriculumTopics} Curriculum Topics
                                </span>
                            ` : ''}
                            ${sectionsCount > 0 ? `
                                <span class="meta-pill">
                                    <i class="fa-solid fa-list-check" aria-hidden="true"></i> ${sectionsCount} Curriculum Sections
                                </span>
                            ` : ''}
                            ${hasTutorials ? `
                                <span class="meta-pill">
                                    <i class="fa-solid fa-signal" aria-hidden="true"></i> Beginner to Advanced
                                </span>
                            ` : `
                                <span class="meta-pill" style="color: var(--warning); border-color: rgba(245, 158, 11, 0.3);">
                                    <i class="fa-solid fa-clock-rotate-left" aria-hidden="true"></i> Content in Preparation
                                </span>
                            `}
                        </div>
                    </div>
                </div>
            `;
        }

        // C. Render Main Content (Active Tutorials or Professional Empty State)
        const contentMount = document.getElementById('category-content');
        if (contentMount) {
            contentMount.innerHTML = '';
            if (tuts.length > 0) {
                renderActiveTutorials(cat, tuts, contentMount, basePath);
            } else {
                renderEmptyCategoryState(cat, contentMount, basePath);
            }
        }

        // D. Render Related Categories
        const relatedMount = document.getElementById('related-categories');
        if (relatedMount) {
            const coreCats = allCategories.filter(c => c.type === 'core' && c.id !== cat.id);
            relatedMount.innerHTML = '';
            coreCats.forEach(rc => {
                const a = document.createElement('a');
                a.href = `${basePath}/${rc.url}`;
                a.className = 'related-cat-card';

                const img = document.createElement('img');
                img.src = `${basePath}/${rc.icon.replace('./', '')}`;
                img.alt = '';
                img.width = 22;
                img.height = 22;

                const span = document.createElement('span');
                span.textContent = rc.name;

                a.appendChild(img);
                a.appendChild(span);
                relatedMount.appendChild(a);
            });
        }
    }

    // 5. Active Tutorials Renderer (With Audited Level Filters and Live Search)
    function renderActiveTutorials(cat, allTuts, container, basePath) {
        // Derive unique difficulty levels from actual data
        const levels = ['All'];
        const validLevels = ['Beginner', 'Intermediate', 'Advanced'];
        validLevels.forEach(lvl => {
            if (allTuts.some(t => t.level === lvl)) {
                levels.push(lvl);
            }
        });

        // Toolbar Container
        const toolbar = document.createElement('div');
        toolbar.className = 'category-toolbar';

        // Filter Group
        const filterGroup = document.createElement('div');
        filterGroup.className = 'category-filter-group';
        filterGroup.setAttribute('role', 'tablist');
        filterGroup.setAttribute('aria-label', 'Filter by difficulty');

        let activeFilter = 'All';
        let searchQuery = '';
        const PAGE_SIZE = 18;
        let visibleCount = PAGE_SIZE;

        levels.forEach(lvl => {
            const btn = document.createElement('button');
            btn.className = `filter-btn ${lvl === 'All' ? 'active' : ''}`;
            btn.setAttribute('role', 'tab');
            btn.setAttribute('aria-selected', lvl === 'All' ? 'true' : 'false');

            const count = lvl === 'All' ? allTuts.length : allTuts.filter(t => t.level === lvl).length;
            btn.textContent = `${lvl} (${count})`;

            btn.addEventListener('click', () => {
                filterGroup.querySelectorAll('.filter-btn').forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                btn.classList.add('active');
                btn.setAttribute('aria-selected', 'true');
                activeFilter = lvl;
                applyFilters(true);
            });
            filterGroup.appendChild(btn);
        });
        toolbar.appendChild(filterGroup);

        // Search Input
        const searchBox = document.createElement('div');
        searchBox.className = 'category-search-box';

        const searchIcon = document.createElement('i');
        searchIcon.className = 'fa-solid fa-search category-search-icon';
        searchIcon.setAttribute('aria-hidden', 'true');

        const searchInput = document.createElement('input');
        searchInput.type = 'search';
        searchInput.className = 'category-search-input';
        searchInput.placeholder = `Search ${cat.name} tutorials...`;
        searchInput.setAttribute('aria-label', `Search ${cat.name} tutorials`);

        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            applyFilters(true);
        });

        searchBox.appendChild(searchIcon);
        searchBox.appendChild(searchInput);
        toolbar.appendChild(searchBox);

        container.appendChild(toolbar);

        // Results counter with aria-live
        const counter = document.createElement('div');
        counter.className = 'text-xs text-muted mb-2';
        counter.setAttribute('aria-live', 'polite');
        container.appendChild(counter);

        // Tutorials Grid Mount
        const grid = document.createElement('div');
        grid.className = 'category-tut-grid';
        container.appendChild(grid);

        // Load More Tutorials Wrapper & Control
        const loadMoreWrap = document.createElement('div');
        loadMoreWrap.className = 'category-load-more-wrap';

        const loadMoreBtn = document.createElement('button');
        loadMoreBtn.type = 'button';
        loadMoreBtn.id = 'load-more-btn';
        loadMoreBtn.className = 'load-more-btn';
        loadMoreBtn.setAttribute('aria-label', 'Load more tutorials');
        loadMoreBtn.innerHTML = '<i class="fa-solid fa-angles-down" aria-hidden="true"></i> Load More Tutorials';

        loadMoreBtn.addEventListener('click', () => {
            const previousCount = visibleCount;
            visibleCount += PAGE_SIZE;
            applyFilters(false);

            // Keyboard accessibility: move focus to the first newly loaded card if button gets hidden
            setTimeout(() => {
                const cards = grid.querySelectorAll('.cat-tut-card');
                if (cards && cards.length > previousCount && loadMoreWrap.style.display === 'none') {
                    cards[previousCount].focus();
                }
            }, 50);
        });

        loadMoreWrap.appendChild(loadMoreBtn);
        container.appendChild(loadMoreWrap);

        function applyFilters(resetCount = true) {
            if (resetCount) {
                visibleCount = PAGE_SIZE;
            }

            let filtered = allTuts;

            // 1. Difficulty filter across entire dataset
            if (activeFilter !== 'All') {
                filtered = filtered.filter(t => t.level === activeFilter);
            }

            // 2. Search query across entire dataset
            if (searchQuery) {
                filtered = filtered.filter(t => {
                    const title = (t.title || '').toLowerCase();
                    const desc = (t.description || '').toLowerCase();
                    const kw = (t.keywords || '').toLowerCase();
                    return title.includes(searchQuery) || desc.includes(searchQuery) || kw.includes(searchQuery);
                });
            }

            const totalMatches = filtered.length;
            const currentVisible = Math.min(visibleCount, totalMatches);

            // 3. Counter message
            if (totalMatches === 0) {
                counter.textContent = 'Showing 0 of 0 tutorials';
            } else if (activeFilter !== 'All') {
                if (searchQuery) {
                    counter.textContent = `Showing ${currentVisible} of ${totalMatches} matching ${activeFilter} tutorials`;
                } else {
                    counter.textContent = `Showing ${currentVisible} of ${totalMatches} ${activeFilter} tutorials`;
                }
            } else {
                if (searchQuery) {
                    counter.textContent = `Showing ${currentVisible} of ${totalMatches} matching tutorials`;
                } else {
                    counter.textContent = `Showing ${currentVisible} of ${totalMatches} tutorials`;
                }
            }

            // 4. Load More Visibility
            if (totalMatches > currentVisible) {
                loadMoreWrap.style.display = 'flex';
                loadMoreBtn.disabled = false;
            } else {
                loadMoreWrap.style.display = 'none';
            }

            // 5. Render visible slice
            const toRender = filtered.slice(0, currentVisible);
            renderCards(toRender);
        }

        function renderCards(tutsToRender) {
            grid.innerHTML = '';
            if (tutsToRender.length === 0) {
                grid.innerHTML = `
                    <div style="grid-column: 1 / -1; padding: 3rem 1.5rem; text-align: center; background: var(--surface); border: 1px dashed var(--border-color); border-radius: var(--radius-lg);">
                        <i class="fa-solid fa-magnifying-glass" style="font-size: 2rem; color: var(--text-muted); margin-bottom: 0.75rem; display: block;"></i>
                        <p style="color: var(--text-secondary); margin: 0; font-size: var(--text-sm);">No tutorials found matching your search.</p>
                    </div>
                `;
                return;
            }

            tutsToRender.forEach(tut => {
                const card = document.createElement('a');
                card.href = `${basePath}/${tut.url.replace('./', '')}`;
                card.className = 'cat-tut-card';

                const levelClass = (tut.level || 'Beginner').toLowerCase();

                card.innerHTML = `
                    <div class="cat-tut-meta-row">
                        <span class="cat-tut-badge ${levelClass}">${tut.level || 'Tutorial'}</span>
                        <span class="cat-tut-time"><i class="fa-regular fa-clock" aria-hidden="true"></i> ${tut.readTime || '5 min'}</span>
                    </div>
                    <h3 class="cat-tut-title">${tut.title}</h3>
                    <p class="cat-tut-desc">${tut.description}</p>
                    <div class="cat-tut-footer">
                        <span>Read Tutorial</span>
                        <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        // Initial render
        applyFilters(true);

        // Render Master Curriculum Roadmap below published tutorials
        renderCurriculumRoadmap(cat, container, basePath);
    }

    // 6. Curriculum Roadmap Component (Native <details> Accordion)
    function renderCurriculumRoadmap(cat, container, basePath) {
        const sections = Array.isArray(cat.sections) ? cat.sections : [];
        if (sections.length === 0) return;

        const totalTopics = sections.reduce((acc, s) => acc + (Array.isArray(s.subtopics) ? s.subtopics.length : 0), 0);
        const totalPublished = sections.reduce((acc, s) => {
            const subs = Array.isArray(s.subtopics) ? s.subtopics : [];
            return acc + subs.filter(sub => sub.status === 'published').length;
        }, 0);

        const accentVar = `var(--cat-${cat.accent || cat.id}, var(--brand-primary))`;

        const roadmapWrap = document.createElement('div');
        roadmapWrap.className = 'curriculum-roadmap-wrap';
        roadmapWrap.id = 'curriculum-roadmap';

        roadmapWrap.innerHTML = `
            <div class="section-header-bar mb-2">
                <div class="section-title-wrap">
                    <span class="section-accent-bar" aria-hidden="true" style="background: ${accentVar};"></span>
                    <h2 class="section-heading-title">Curriculum Roadmap</h2>
                </div>
                <span class="text-xs text-muted" style="font-weight: 600;">${totalTopics} Topics • ${totalPublished} Published</span>
            </div>
            <p class="curriculum-roadmap-intro">
                Explore the structured curriculum for ${cat.name}. Published tutorials are accessible immediately, while planned topics outline upcoming additions to our technical roadmap.
            </p>
        `;

        const accordionContainer = document.createElement('div');
        accordionContainer.className = 'curriculum-accordion-container';

        sections.forEach((sec) => {
            const subtopics = Array.isArray(sec.subtopics) ? sec.subtopics : [];
            const secPubCount = subtopics.filter(sub => sub.status === 'published').length;
            const secTotal = subtopics.length;

            const details = document.createElement('details');
            details.className = 'curriculum-section-details';
            // Default to collapsed (no 'open' attribute)

            const summary = document.createElement('summary');
            summary.className = 'curriculum-section-summary';

            summary.innerHTML = `
                <span class="curriculum-summary-title">
                    <i class="fa-solid fa-folder" aria-hidden="true"></i>
                    <strong>${sec.name || sec.title}</strong>
                </span>
                <span class="curriculum-summary-meta">
                    <span class="meta-pill text-xs">${secTotal} ${secTotal === 1 ? 'topic' : 'topics'} • ${secPubCount} published</span>
                    <i class="fa-solid fa-chevron-down curriculum-chevron" aria-hidden="true"></i>
                </span>
            `;
            details.appendChild(summary);

            const body = document.createElement('div');
            body.className = 'curriculum-section-body';

            const list = document.createElement('ul');
            list.className = 'curriculum-subtopic-list';

            subtopics.forEach(sub => {
                const li = document.createElement('li');
                li.className = `curriculum-subtopic-item ${sub.status || 'planned'}`;
                const levelClass = (sub.level || 'beginner').toLowerCase();

                if (sub.status === 'published' && sub.url) {
                    const a = document.createElement('a');
                    a.href = `${basePath}/${sub.url.replace('./', '')}`;
                    a.className = 'curriculum-subtopic-link';
                    a.innerHTML = `
                        <span class="curriculum-subtopic-name">
                            <i class="fa-solid fa-circle-check text-success" aria-hidden="true"></i>
                            <span>${sub.name}</span>
                        </span>
                        <span class="curriculum-item-badges">
                            <span class="cat-tut-badge ${levelClass}">${sub.level || 'Tutorial'}</span>
                            <span class="curriculum-status-pill published">Published</span>
                        </span>
                    `;
                    li.appendChild(a);
                } else {
                    const div = document.createElement('div');
                    div.className = 'curriculum-subtopic-static';
                    div.innerHTML = `
                        <span class="curriculum-subtopic-name">
                            <i class="fa-regular fa-circle text-muted" aria-hidden="true"></i>
                            <span>${sub.name}</span>
                        </span>
                        <span class="curriculum-item-badges">
                            <span class="cat-tut-badge ${levelClass}">${sub.level || 'Planned'}</span>
                            <span class="curriculum-status-pill planned">Planned</span>
                        </span>
                    `;
                    li.appendChild(div);
                }

                list.appendChild(li);
            });

            body.appendChild(list);
            details.appendChild(body);
            accordionContainer.appendChild(details);
        });

        roadmapWrap.appendChild(accordionContainer);
        container.appendChild(roadmapWrap);
    }

    // 7. Professional Empty State (Strictly separates Published vs Planned)
    function renderEmptyCategoryState(cat, container, basePath) {
        const sections = Array.isArray(cat.sections) ? cat.sections : [];

        const emptyCard = document.createElement('div');
        emptyCard.className = 'category-empty-state';

        let plannedHtml = '';
        if (sections.length > 0) {
            plannedHtml = `
                <div class="planned-curriculum-box">
                    <div class="planned-curriculum-header">
                        <h4>PLANNED CURRICULUM</h4>
                        <span class="meta-pill" style="font-size: 0.65rem;">Planned • Not Yet Published</span>
                    </div>
                    <ul class="planned-curriculum-list">
                        ${sections.map(s => `
                            <li class="planned-curriculum-item">
                                <i class="fa-regular fa-circle-dot" aria-hidden="true"></i>
                                <span><strong>${s.name || s.title}</strong> — ${s.subtopics ? s.subtopics.length + ' upcoming topics' : 'Curriculum planned'}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            `;
        } else {
            plannedHtml = `
                <div class="planned-curriculum-box" style="text-align: center;">
                    <p style="font-size: var(--text-xs); color: var(--text-muted); margin: 0;">
                        Curriculum topics for ${cat.name} are currently being structured by our engineering team.
                    </p>
                </div>
            `;
        }

        emptyCard.innerHTML = `
            <div class="empty-state-icon" aria-hidden="true">
                <i class="fa-solid fa-compass-drafting"></i>
            </div>
            <span class="empty-state-status-badge">
                <i class="fa-solid fa-clock" aria-hidden="true"></i> 0 Published Tutorials • Curriculum In Preparation
            </span>
            <h2 class="empty-state-title">Tutorials for this category are being prepared</h2>
            <p class="empty-state-desc">
                Our team is currently authoring comprehensive, peer-reviewed tutorials and practical labs for ${cat.name}. We do not publish placeholder articles. In the meantime, you can explore our published curriculum or test your skills.
            </p>
            ${plannedHtml}
            <div style="margin-top: 2rem; display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem;">
                <a href="${basePath}/networking.html" class="btn btn-primary" style="font-size: var(--text-xs); padding: 0.5rem 1rem;">
                    <i class="fa-solid fa-network-wired" aria-hidden="true"></i> Explore Networking (61 Tutorials)
                </a>
                <a href="${basePath}/commands.html" class="btn btn-secondary" style="font-size: var(--text-xs); padding: 0.5rem 1rem;">
                    <i class="fa-solid fa-terminal" aria-hidden="true"></i> Essential Commands (12 Guides)
                </a>
                <a href="${basePath}/quiz.html" class="btn btn-secondary" style="font-size: var(--text-xs); padding: 0.5rem 1rem;">
                    <i class="fa-solid fa-brain" aria-hidden="true"></i> IT Practice Quizzes
                </a>
            </div>
        `;

        container.appendChild(emptyCard);
    }
});
