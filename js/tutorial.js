/**
 * MJ Tech Hub - Shared Tutorial Engine (js/tutorial.js)
 * Modern technical reading engine providing:
 * - Table of Contents (TOC) with scroll-spy active state and mobile accordion
 * - Enhanced code blocks & CLI commands with accessible 1-click clipboard copy
 * - Standardized responsive tables and semantic callouts
 * - Canonical Previous/Next navigation and deterministic Related Tutorials
 * - Strict idempotency and reduced-motion compliance
 */

(function () {
    'use strict';

    function initTutorialEngine() {
        const main = document.querySelector('main');
        if (!main) return;

        // Base Path Resolution
        const scripts = document.getElementsByTagName('script');
        let basePath = '../..';
        for (let script of scripts) {
            if (script.src && script.src.includes('js/tutorial.js')) {
                const srcAttr = script.getAttribute('src');
                basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/tutorial.js'));
                if (basePath === '') basePath = '.';
                break;
            }
        }

        const currentPath = window.location.pathname.toLowerCase();
        const filename = currentPath.substring(currentPath.lastIndexOf('/') + 1) || 'index.html';

        // 1. Fetch metadata from tutorials.json
        fetch(`${basePath}/data/tutorials.json`)
            .then(res => {
                if (!res.ok) throw new Error('Failed to load tutorials data');
                return res.json();
            })
            .then(data => {
                const tutorials = Array.isArray(data) ? data : [];
                const currentTut = tutorials.find(t => {
                    const tUrl = (t.url || '').toLowerCase();
                    return tUrl.endsWith(filename) || (t.id && filename.startsWith(t.id));
                });

                if (currentTut) {
                    enhanceTutorialHero(currentTut, basePath);
                    renderTutorialNavigation(currentTut, tutorials, basePath);
                }
            })
            .catch(err => {
                console.warn('Tutorial metadata error or offline mode:', err);
            });

        // 2. Immediate DOM Enhancements (Idempotent)
        const article = document.querySelector('.tutorial-article, .lesson-content');
        if (article) {
            setupTableOfContents(article);
            enhanceCodeBlocks(article);
            standardizeCallouts(article);
            enhanceTables(article);
        }
    }

    /**
     * 1. Enhance Tutorial Hero (Preserving Single H1 & Adding Metadata)
     */
    function enhanceTutorialHero(tut, basePath) {
        const hero = document.getElementById('tutorial-header');
        if (!hero || hero.getAttribute('data-enhanced') === 'true') return;
        hero.setAttribute('data-enhanced', 'true');

        // Check if hero already has static elements
        let metaRow = hero.querySelector('.tutorial-meta-row');
        if (!metaRow) {
            metaRow = document.createElement('div');
            metaRow.className = 'tutorial-meta-row';

            const levelClass = (tut.level || 'Beginner').toLowerCase();
            const levelBadge = document.createElement('span');
            levelBadge.className = `cat-tut-badge ${levelClass}`;
            levelBadge.textContent = tut.level || 'Tutorial';
            metaRow.appendChild(levelBadge);

            if (tut.readTime) {
                const timeItem = document.createElement('span');
                timeItem.className = 'tutorial-meta-item';
                timeItem.innerHTML = `<i class="fa-regular fa-clock" aria-hidden="true"></i> ${escapeHtml(tut.readTime)}`;
                metaRow.appendChild(timeItem);
            }

            const rawDate = tut.updatedAt || tut.publishedAt;
            if (rawDate && rawDate !== 'UNKNOWN') {
                const dateItem = document.createElement('span');
                dateItem.className = 'tutorial-meta-item';
                dateItem.innerHTML = `<i class="fa-regular fa-calendar" aria-hidden="true"></i> Updated: ${formatDate(rawDate)}`;
                metaRow.appendChild(dateItem);
            }

            const titleEl = hero.querySelector('h1');
            if (titleEl) {
                hero.insertBefore(metaRow, titleEl);
            } else {
                hero.appendChild(metaRow);
            }
        }
    }

    /**
     * 2. Table of Contents (TOC) with Slugified IDs, Active Scroll-Spy & Reduced Motion
     */
    function setupTableOfContents(article) {
        const tocNav = document.getElementById('tutorial-toc');
        if (!tocNav || tocNav.getAttribute('data-enhanced') === 'true') return;

        const headings = article.querySelectorAll('h2, h3');
        if (headings.length === 0) {
            const sidebar = document.querySelector('.tutorial-sidebar');
            if (sidebar) sidebar.style.display = 'none';
            return;
        }

        tocNav.setAttribute('data-enhanced', 'true');

        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const scrollBehavior = prefersReducedMotion ? 'auto' : 'smooth';

        const usedIds = new Set();
        const tocList = document.createElement('ul');
        tocList.className = 'tutorial-toc-list';

        // Prepare mobile collapsible TOC wrapper above article if not already present
        let mobileToc = document.querySelector('.tutorial-mobile-toc');
        let mobileTocList = null;
        if (!mobileToc && article.parentElement) {
            mobileToc = document.createElement('details');
            mobileToc.className = 'tutorial-mobile-toc';
            mobileToc.innerHTML = `
                <summary><i class="fa-solid fa-list-ul" aria-hidden="true"></i> Table of Contents</summary>
                <div class="tutorial-mobile-toc-body"></div>
            `;
            article.parentElement.insertBefore(mobileToc, article);
            mobileTocList = document.createElement('ul');
            mobileTocList.className = 'tutorial-toc-list';
            mobileToc.querySelector('.tutorial-mobile-toc-body').appendChild(mobileTocList);
        }

        headings.forEach((heading, idx) => {
            // A. Ensure unique, valid ID
            let id = heading.id;
            if (!id || id.trim() === '') {
                id = slugify(heading.textContent || `section-${idx + 1}`);
                let candidateId = id;
                let counter = 2;
                while (usedIds.has(candidateId) || document.getElementById(candidateId)) {
                    candidateId = `${id}-${counter}`;
                    counter++;
                }
                id = candidateId;
                heading.id = id;
            }
            usedIds.add(id);

            const isH3 = heading.tagName.toLowerCase() === 'h3';

            // Desktop Item
            const li = document.createElement('li');
            const link = document.createElement('a');
            link.href = `#${id}`;
            link.className = `toc-link ${isH3 ? 'toc-sublink' : ''}`;
            link.textContent = heading.textContent.trim();
            link.addEventListener('click', (e) => {
                e.preventDefault();
                heading.scrollIntoView({ behavior: scrollBehavior });
                history.pushState(null, '', `#${id}`);
                setActiveTocLink(id);
            });
            li.appendChild(link);
            tocList.appendChild(li);

            // Mobile Item
            if (mobileTocList) {
                const mLi = document.createElement('li');
                const mLink = document.createElement('a');
                mLink.href = `#${id}`;
                mLink.className = `toc-link ${isH3 ? 'toc-sublink' : ''}`;
                mLink.textContent = heading.textContent.trim();
                mLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    heading.scrollIntoView({ behavior: scrollBehavior });
                    history.pushState(null, '', `#${id}`);
                    mobileToc.removeAttribute('open');
                });
                mLi.appendChild(mLink);
                mobileTocList.appendChild(mLi);
            }
        });

        tocNav.innerHTML = `<h2 class="tutorial-toc-title">On This Page</h2>`;
        tocNav.appendChild(tocList);

        // Active Heading Highlighting using IntersectionObserver
        function setActiveTocLink(activeId) {
            const allLinks = tocNav.querySelectorAll('.toc-link');
            allLinks.forEach(a => {
                if (a.getAttribute('href') === `#${activeId}`) {
                    a.classList.add('active');
                } else {
                    a.classList.remove('active');
                }
            });
        }

        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                const visible = entries.filter(e => e.isIntersecting);
                if (visible.length > 0) {
                    setActiveTocLink(visible[0].target.id);
                }
            }, { rootMargin: '0px 0px -65% 0px', threshold: 0 });

            headings.forEach(h => observer.observe(h));
        }
    }

    /**
     * 3. Enhanced Code Blocks & Controlled CLI Commands
     * Controlled selectors: pre > code, .tutorial-command
     */
    function enhanceCodeBlocks(article) {
        const blocks = article.querySelectorAll('pre > code, .tutorial-command');

        blocks.forEach((block) => {
            if (block.getAttribute('data-enhanced') === 'true' || block.closest('.tutorial-code-block')) {
                return;
            }
            block.setAttribute('data-enhanced', 'true');

            const isCommand = block.classList.contains('tutorial-command');
            const targetContainer = isCommand ? block : block.parentElement; // <pre> if pre > code

            const wrapper = document.createElement('div');
            wrapper.className = 'tutorial-code-block';

            const header = document.createElement('div');
            header.className = 'tutorial-code-header';

            const langLabel = document.createElement('span');
            langLabel.className = 'tutorial-code-lang';
            langLabel.innerHTML = isCommand
                ? '<i class="fa-solid fa-terminal" aria-hidden="true"></i> Command / Terminal'
                : '<i class="fa-solid fa-code" aria-hidden="true"></i> Code / Syntax';

            const copyBtn = document.createElement('button');
            copyBtn.type = 'button';
            copyBtn.className = 'tutorial-code-copy-btn';
            copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
            copyBtn.innerHTML = '<i class="fa-regular fa-copy" aria-hidden="true"></i> Copy';

            copyBtn.addEventListener('click', () => {
                const codeText = block.innerText || block.textContent || '';
                copyToClipboard(codeText, copyBtn);
            });

            header.appendChild(langLabel);
            header.appendChild(copyBtn);
            wrapper.appendChild(header);

            targetContainer.parentNode.insertBefore(wrapper, targetContainer);

            if (isCommand) {
                targetContainer.classList.add('tutorial-code-content');
                wrapper.appendChild(targetContainer);
            } else {
                targetContainer.classList.add('tutorial-code-content');
                wrapper.appendChild(targetContainer);
            }
        });
    }

    /**
     * 4. Accessible Clipboard Copy Functionality
     */
    let copyToastTimeout = null;
    function copyToClipboard(text, button) {
        const cleanText = text.replace(/^\s+|\s+$/g, '');

        function onSuccess() {
            button.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i> Copied!';
            button.classList.add('copied');

            const toast = document.getElementById('copy-toast');
            const toastMsg = document.getElementById('copy-toast-msg');
            if (toast && toastMsg) {
                toastMsg.textContent = 'Code snippet copied to clipboard!';
                toast.classList.add('active');

                clearTimeout(copyToastTimeout);
                copyToastTimeout = setTimeout(() => {
                    toast.classList.remove('active');
                }, 2200);
            }

            setTimeout(() => {
                button.innerHTML = '<i class="fa-regular fa-copy" aria-hidden="true"></i> Copy';
                button.classList.remove('copied');
            }, 2000);
        }

        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(cleanText).then(onSuccess).catch(() => fallbackCopy(cleanText, onSuccess));
        } else {
            fallbackCopy(cleanText, onSuccess);
        }
    }

    function fallbackCopy(text, cb) {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.left = '-9999px';
        document.body.appendChild(ta);
        ta.focus();
        ta.select();
        try {
            document.execCommand('copy');
            cb();
        } catch (e) {
            console.error('Fallback copy failed', e);
        }
        document.body.removeChild(ta);
    }

    /**
     * 5. Standardize Audited Callouts (Note, Warning, Tip, Important)
     */
    function standardizeCallouts(article) {
        const paragraphs = article.querySelectorAll('p');
        const calloutRegex = /^\s*(Note|Tip|Warning|Important)\s*:\s*(.*)/i;

        paragraphs.forEach(p => {
            if (p.getAttribute('data-callout-enhanced') === 'true' || p.closest('.tutorial-callout')) return;

            // Check if paragraph starts with <em>Label:, <strong>Label:, or text node "Label:"
            let match = null;
            const em = p.querySelector('em:first-child, strong:first-child');
            if (em) {
                match = calloutRegex.exec(em.textContent.trim());
            } else if (p.childNodes.length > 0 && p.childNodes[0].nodeType === Node.TEXT_NODE) {
                match = calloutRegex.exec(p.childNodes[0].textContent.trim());
            }

            if (match) {
                p.setAttribute('data-callout-enhanced', 'true');
                const labelType = match[1].toLowerCase();
                const labelCapitalized = match[1].charAt(0).toUpperCase() + match[1].slice(1).toLowerCase();

                let iconClass = 'fa-solid fa-circle-info';
                if (labelType === 'warning') iconClass = 'fa-solid fa-triangle-exclamation';
                else if (labelType === 'tip') iconClass = 'fa-solid fa-lightbulb';
                else if (labelType === 'important') iconClass = 'fa-solid fa-circle-exclamation';

                const callout = document.createElement('div');
                callout.className = `tutorial-callout callout-${labelType}`;
                callout.setAttribute('role', 'note');

                const iconDiv = document.createElement('div');
                iconDiv.className = 'callout-icon';
                iconDiv.innerHTML = `<i class="${iconClass}" aria-hidden="true"></i>`;

                const bodyDiv = document.createElement('div');
                bodyDiv.className = 'callout-body';

                // Clone contents preserving all inner text and links
                const clonedP = p.cloneNode(true);
                bodyDiv.appendChild(clonedP);

                callout.appendChild(iconDiv);
                callout.appendChild(bodyDiv);

                p.parentNode.insertBefore(callout, p);
                p.remove();
            }
        });
    }

    /**
     * 6. Auto-Wrap Tables in Responsive Container
     */
    function enhanceTables(article) {
        const tables = article.querySelectorAll('table');
        tables.forEach(table => {
            if (!table.parentElement.classList.contains('table-responsive')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
        });
    }

    /**
     * 7. Previous / Next Navigation & Deterministic Related Tutorials
     * Order Contract: tutorials.json canonical array sequence
     */
    function renderTutorialNavigation(tut, tutorials, basePath) {
        const mount = document.getElementById('tutorial-footer-mount');
        if (!mount || mount.getAttribute('data-enhanced') === 'true') return;
        mount.setAttribute('data-enhanced', 'true');

        const currentIndex = tutorials.findIndex(t => t.id === tut.id);
        const prev = currentIndex > 0 ? tutorials[currentIndex - 1] : null;
        const next = currentIndex < tutorials.length - 1 ? tutorials[currentIndex + 1] : null;

        const footerSection = document.createElement('section');
        footerSection.className = 'tutorial-footer-section';
        footerSection.setAttribute('aria-label', 'Tutorial Navigation');

        // A. Previous / Next Cards Grid
        const navGrid = document.createElement('div');
        navGrid.className = 'tutorial-nav-grid';

        if (prev) {
            const prevCard = document.createElement('a');
            prevCard.href = `${basePath}/${prev.url.replace('./', '')}`;
            prevCard.className = 'tutorial-nav-card prev';
            prevCard.setAttribute('rel', 'prev');
            prevCard.innerHTML = `
                <span class="tutorial-nav-sub"><i class="fa-solid fa-arrow-left" aria-hidden="true"></i> Previous Tutorial</span>
                <span class="tutorial-nav-title">${escapeHtml(prev.title)}</span>
            `;
            navGrid.appendChild(prevCard);
        } else {
            navGrid.appendChild(document.createElement('div')); // Empty column spacer
        }

        if (next) {
            const nextCard = document.createElement('a');
            nextCard.href = `${basePath}/${next.url.replace('./', '')}`;
            nextCard.className = 'tutorial-nav-card next';
            nextCard.setAttribute('rel', 'next');
            nextCard.innerHTML = `
                <span class="tutorial-nav-sub">Next Tutorial <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>
                <span class="tutorial-nav-title">${escapeHtml(next.title)}</span>
            `;
            navGrid.appendChild(nextCard);
        } else {
            navGrid.appendChild(document.createElement('div')); // Empty column spacer
        }

        footerSection.appendChild(navGrid);

        // B. Canonical "Back to Category" Action
        const catSlug = (tut.category || 'networking').toLowerCase().trim();
        const catUrl = catSlug.includes('cloud') ? 'cloud.html' : `${catSlug}.html`;

        const backWrap = document.createElement('div');
        backWrap.className = 'tutorial-back-category';
        backWrap.innerHTML = `
            <a href="${basePath}/${catUrl}" class="btn btn-secondary" style="font-size: var(--text-xs); padding: 0.5rem 1.25rem;">
                <i class="fa-solid fa-layer-group" aria-hidden="true"></i> Back to ${escapeHtml(tut.category || 'Category')}
            </a>
        `;
        footerSection.appendChild(backWrap);

        // C. Deterministic Related Tutorials (Condition 8: Same Category, Same Difficulty, Neighboring, max 3)
        const relatedTutorials = getRelatedTutorials(tut, tutorials);
        if (relatedTutorials.length > 0) {
            const relatedSection = document.createElement('section');
            relatedSection.className = 'tutorial-related-section';
            relatedSection.setAttribute('aria-labelledby', 'related-tutorials-heading');

            const relatedTitle = document.createElement('h2');
            relatedTitle.id = 'related-tutorials-heading';
            relatedTitle.className = 'tutorial-related-title';
            relatedTitle.textContent = 'Related Tutorials';
            relatedSection.appendChild(relatedTitle);

            const relatedGrid = document.createElement('div');
            relatedGrid.className = 'tutorial-related-grid';

            relatedTutorials.forEach(r => {
                const card = document.createElement('a');
                card.href = `${basePath}/${r.url.replace('./', '')}`;
                card.className = 'tutorial-related-card';

                const lvlClass = (r.level || 'Beginner').toLowerCase();

                card.innerHTML = `
                    <div class="tutorial-related-meta">
                        <span class="cat-tut-badge ${lvlClass}">${r.level || 'Tutorial'}</span>
                        <span style="font-size: var(--text-xs); color: var(--text-muted);"><i class="fa-regular fa-clock" aria-hidden="true"></i> ${r.readTime || '5 min'}</span>
                    </div>
                    <h3 class="tutorial-related-name">${escapeHtml(r.title)}</h3>
                    <p class="tutorial-related-desc">${escapeHtml(r.description || '')}</p>
                `;
                relatedGrid.appendChild(card);
            });

            relatedSection.appendChild(relatedGrid);
            footerSection.appendChild(relatedSection);
        }

        mount.appendChild(footerSection);
    }

    /**
     * Deterministic Related Tutorials Selection Logic
     */
    function getRelatedTutorials(currentTut, allTutorials) {
        const categoryTutorials = allTutorials.filter(t => t.id !== currentTut.id && t.category === currentTut.category);
        const currentIndex = allTutorials.findIndex(t => t.id === currentTut.id);

        const scored = categoryTutorials.map(t => {
            let score = 0;
            if (t.level === currentTut.level) score += 10;

            const tIndex = allTutorials.findIndex(item => item.id === t.id);
            const distance = Math.abs(tIndex - currentIndex);
            score += Math.max(0, 10 - distance);

            return { tut: t, score, index: tIndex };
        });

        // Deterministic sort: highest score first, then canonical array index
        scored.sort((a, b) => b.score - a.score || a.index - b.index);
        return scored.slice(0, 3).map(s => s.tut);
    }

    /**
     * Utility Functions
     */
    function slugify(text) {
        return text
            .toString()
            .toLowerCase()
            .trim()
            .replace(/&/g, '-and-')
            .replace(/[\s\W-]+/g, '-')
            .replace(/^-+|-+$/g, '');
    }

    function formatDate(dateStr) {
        if (!dateStr || dateStr === 'UNKNOWN') return '';
        const d = new Date(dateStr);
        if (isNaN(d.getTime())) return dateStr;
        return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Expose for testing & manual initialization
    window.initTutorialEngine = initTutorialEngine;

    // Auto-init on DOMContentLoaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTutorialEngine);
    } else {
        initTutorialEngine();
    }
})();
