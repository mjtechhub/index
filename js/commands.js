/**
 * MJ Tech Hub - Essential Commands Module (js/commands.js)
 * Modern, compact, operational CLI command library with accessible copy and structured filtering.
 */

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('commands-container');
    const filterTabsContainer = document.getElementById('command-category-filters');
    const searchInput = document.getElementById('commands-search-input');
    const counter = document.getElementById('commands-counter');
    const toast = document.getElementById('copy-toast');
    const toastMsg = document.getElementById('copy-toast-msg');

    if (!container) return;

    // Base Path Resolution
    const scripts = document.getElementsByTagName('script');
    let basePath = '.';
    for (let script of scripts) {
        if (script.src && script.src.includes('js/commands.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/commands.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }

    let allCommands = [];
    let activeFilter = 'All';
    let searchQuery = '';
    let toastTimeout = null;

    // Fetch Commands Data
    fetch(`${basePath}/data/commands.json`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch commands');
            return response.json();
        })
        .then(data => {
            allCommands = Array.isArray(data) ? data : [];
            setupCategoryFilters(allCommands);
            setupSearch();
            renderCommandList(allCommands);
        })
        .catch(error => {
            console.error('Error loading commands:', error);
            container.innerHTML = `
                <div class="category-empty-state">
                    <p class="text-danger">Failed to load command library. Please refresh or try again later.</p>
                </div>
            `;
        });

    // Setup Category & Platform Filter Tabs Derived Strictly from Data
    function setupCategoryFilters(commands) {
        if (!filterTabsContainer) return;
        filterTabsContainer.innerHTML = '';

        // Extract unique categories from structured data
        const categories = ['All'];
        commands.forEach(c => {
            if (c.category && !categories.includes(c.category)) {
                categories.push(c.category);
            }
        });

        // Add Linux cross-platform option (audited from data: ping, nslookup)
        const linuxCount = commands.filter(c => (c.platform || '').toLowerCase().includes('linux')).length;

        // Render standard category tabs
        categories.forEach(cat => {
            const btn = document.createElement('button');
            btn.className = `cmd-filter-btn ${cat === 'All' ? 'active' : ''}`;
            btn.setAttribute('role', 'tab');
            btn.setAttribute('aria-selected', cat === 'All' ? 'true' : 'false');
            
            const count = cat === 'All' ? commands.length : commands.filter(c => c.category === cat).length;
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

        // Add platform specific filter tab if data supports it
        if (linuxCount > 0) {
            const linuxBtn = document.createElement('button');
            linuxBtn.className = 'cmd-filter-btn';
            linuxBtn.setAttribute('role', 'tab');
            linuxBtn.setAttribute('aria-selected', 'false');
            linuxBtn.textContent = `Linux (${linuxCount})`;

            linuxBtn.addEventListener('click', () => {
                filterTabsContainer.querySelectorAll('.cmd-filter-btn').forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                linuxBtn.classList.add('active');
                linuxBtn.setAttribute('aria-selected', 'true');
                activeFilter = 'PLATFORM_LINUX';
                applyFilterAndSearch();
            });
            filterTabsContainer.appendChild(linuxBtn);
        }
    }

    // Setup Live Search Input
    function setupSearch() {
        if (!searchInput) return;
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            applyFilterAndSearch();
        });
    }

    // Apply Filter & Search Simultaneously
    function applyFilterAndSearch() {
        let filtered = allCommands;

        // 1. Category / Platform Filter
        if (activeFilter === 'PLATFORM_LINUX') {
            filtered = filtered.filter(c => (c.platform || '').toLowerCase().includes('linux'));
        } else if (activeFilter !== 'All') {
            filtered = filtered.filter(c => c.category === activeFilter);
        }

        // 2. Search Query
        if (searchQuery) {
            filtered = filtered.filter(c => {
                const cmd = (c.command || '').toLowerCase();
                const purpose = (c.purpose || '').toLowerCase();
                const syntax = (c.syntax || '').toLowerCase();
                const ex = (c.example || '').toLowerCase();
                const useCase = (c.useCase || '').toLowerCase();
                return cmd.includes(searchQuery) || purpose.includes(searchQuery) || syntax.includes(searchQuery) || ex.includes(searchQuery) || useCase.includes(searchQuery);
            });
        }

        // Update Counter
        if (counter) {
            counter.textContent = `Showing ${filtered.length} of ${allCommands.length} commands`;
        }

        renderCommandList(filtered);
    }

    // Render Compact Command Cards
    function renderCommandList(commands) {
        container.innerHTML = '';

        if (commands.length === 0) {
            container.innerHTML = `
                <div class="category-empty-state">
                    <div class="empty-state-icon" aria-hidden="true">
                        <i class="fa-solid fa-terminal"></i>
                    </div>
                    <h3 class="empty-state-title">No commands match your filter</h3>
                    <p class="empty-state-desc">Try searching for different keywords or select "All" categories to view all essential commands.</p>
                </div>
            `;
            return;
        }

        commands.forEach(cmd => {
            const card = document.createElement('div');
            card.className = 'command-item-card';

            // Top Row
            const topRow = document.createElement('div');
            topRow.className = 'cmd-card-top';

            const titleWrap = document.createElement('div');
            titleWrap.className = 'cmd-title-wrap';

            const codeName = document.createElement('span');
            codeName.className = 'cmd-code-name';
            codeName.textContent = cmd.command;
            titleWrap.appendChild(codeName);

            const platBadge = document.createElement('span');
            platBadge.className = 'cmd-badge cmd-badge-plat';
            platBadge.textContent = cmd.platform;
            titleWrap.appendChild(platBadge);

            const catBadge = document.createElement('span');
            catBadge.className = 'cmd-badge cmd-badge-cat';
            catBadge.textContent = cmd.category;
            titleWrap.appendChild(catBadge);

            topRow.appendChild(titleWrap);

            // Copy Action Button
            const copyBtn = document.createElement('button');
            copyBtn.className = 'cmd-copy-btn';
            copyBtn.setAttribute('aria-label', `Copy ${cmd.command} to clipboard`);
            copyBtn.innerHTML = '<i class="fa-regular fa-copy" aria-hidden="true"></i> Copy';

            copyBtn.addEventListener('click', () => {
                copyTextToClipboard(cmd.example, cmd.command, copyBtn);
            });

            topRow.appendChild(copyBtn);
            card.appendChild(topRow);

            // Purpose
            const purposeP = document.createElement('p');
            purposeP.className = 'cmd-purpose';
            purposeP.textContent = cmd.purpose;
            card.appendChild(purposeP);

            // Example Row
            const exampleRow = document.createElement('div');
            exampleRow.className = 'cmd-example-row';

            const exampleCode = document.createElement('code');
            exampleCode.className = 'cmd-example-code';
            exampleCode.textContent = cmd.example;
            exampleRow.appendChild(exampleCode);

            card.appendChild(exampleRow);

            // Progressive Disclosure (<details>) for Deep Details
            const details = document.createElement('details');
            details.className = 'cmd-details-disclosure';

            const summary = document.createElement('summary');
            summary.className = 'cmd-details-summary';
            summary.innerHTML = '<i class="fa-solid fa-chevron-right" aria-hidden="true"></i> View syntax, example output & use case';
            
            // Toggle icon animation on open/close
            details.addEventListener('toggle', () => {
                const icon = summary.querySelector('i');
                if (details.open) {
                    icon.className = 'fa-solid fa-chevron-down';
                } else {
                    icon.className = 'fa-solid fa-chevron-right';
                }
            });

            details.appendChild(summary);

            const expandedContent = document.createElement('div');
            expandedContent.className = 'cmd-expanded-content';

            // Syntax Field
            const syntaxField = document.createElement('div');
            syntaxField.className = 'cmd-detail-field';
            syntaxField.innerHTML = `
                <span class="cmd-detail-label">Syntax</span>
                <span class="cmd-detail-val" style="font-family: var(--font-mono);">${escapeHtml(cmd.syntax)}</span>
            `;
            expandedContent.appendChild(syntaxField);

            // Example Output Field
            const resultField = document.createElement('div');
            resultField.className = 'cmd-detail-field';
            resultField.innerHTML = `
                <span class="cmd-detail-label">Example Output</span>
                <span class="cmd-detail-val">${escapeHtml(cmd.expectedResult)}</span>
            `;
            expandedContent.appendChild(resultField);

            // Practical Use Case Field
            const useCaseField = document.createElement('div');
            useCaseField.className = 'cmd-detail-field' + (cmd.warnings ? '' : ' style="grid-column: 1 / -1;"');
            useCaseField.innerHTML = `
                <span class="cmd-detail-label">Practical Scenario</span>
                <span class="cmd-detail-val">${escapeHtml(cmd.useCase)}</span>
            `;
            expandedContent.appendChild(useCaseField);

            // Warning Box if exists
            if (cmd.warnings) {
                const warningBox = document.createElement('div');
                warningBox.className = 'cmd-warning-box';
                warningBox.innerHTML = `
                    <i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i>
                    <div><strong>Caution:</strong> ${escapeHtml(cmd.warnings)}</div>
                `;
                expandedContent.appendChild(warningBox);
            }

            details.appendChild(expandedContent);
            card.appendChild(details);

            container.appendChild(card);
        });
    }

    // Accessible Copy Functionality with Toast & ARIA
    function copyTextToClipboard(text, cmdName, button) {
        if (!navigator.clipboard) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {
                document.execCommand('copy');
                showCopiedState(button, cmdName);
            } catch (err) {
                console.error('Fallback copy failed', err);
            }
            document.body.removeChild(textArea);
            return;
        }

        navigator.clipboard.writeText(text).then(() => {
            showCopiedState(button, cmdName);
        }).catch(err => {
            console.error('Clipboard write failed:', err);
        });
    }

    function showCopiedState(button, cmdName) {
        // 1. Button Visual State (Text + Checkmark, not color alone)
        button.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i> Copied!';
        button.classList.add('copied');

        // 2. Floating Toast Notification
        if (toast && toastMsg) {
            toastMsg.textContent = `Copied "${cmdName}" to clipboard!`;
            toast.classList.add('active');

            clearTimeout(toastTimeout);
            toastTimeout = setTimeout(() => {
                toast.classList.remove('active');
            }, 2500);
        }

        // Reset Button State after 2 seconds
        setTimeout(() => {
            button.innerHTML = '<i class="fa-regular fa-copy" aria-hidden="true"></i> Copy';
            button.classList.remove('copied');
        }, 2000);
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
});
