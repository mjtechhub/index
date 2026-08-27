/**
 * MJ Tech Hub - Main JavaScript
 * Handles global functionality like mobile menu
 */

document.addEventListener('DOMContentLoaded', () => {
    // Dynamic component initialization is handled via event delegation
    // to support dynamically injected header/footer HTML.
    
    document.addEventListener('click', (e) => {
        const mobileMenuBtn = e.target.closest('.mobile-menu-toggle');
        const navLinks = document.querySelector('.nav-links');
        
        // 1. Toggle via hamburger button
        if (mobileMenuBtn && navLinks) {
            e.stopPropagation();
            const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
            
            if (isExpanded) {
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
                navLinks.classList.remove('active');
            } else {
                mobileMenuBtn.setAttribute('aria-expanded', 'true');
                navLinks.classList.add('active');
            }
            return;
        }
        
        // 2. Close when clicking a nav link
        if (e.target.closest('.nav-links a') && navLinks && navLinks.classList.contains('active')) {
            const btn = document.querySelector('.mobile-menu-toggle');
            navLinks.classList.remove('active');
            if (btn) btn.setAttribute('aria-expanded', 'false');
            return;
        }
        
        // 3. Close when clicking outside
        if (navLinks && navLinks.classList.contains('active')) {
            if (!navLinks.contains(e.target)) {
                const btn = document.querySelector('.mobile-menu-toggle');
                navLinks.classList.remove('active');
                if (btn) btn.setAttribute('aria-expanded', 'false');
            }
        }
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const navLinks = document.querySelector('.nav-links');
            if (navLinks && navLinks.classList.contains('active')) {
                const btn = document.querySelector('.mobile-menu-toggle');
                navLinks.classList.remove('active');
                if (btn) {
                    btn.setAttribute('aria-expanded', 'false');
                    btn.focus();
                }
            }
        }
    });
    


    // Dynamic Latest Tutorials (Homepage)
    const latestTutorialsList = document.getElementById('latest-tutorials-list');
    if (latestTutorialsList) {
        fetch('./data/tutorials.json')
            .then(res => {
                if (!res.ok) throw new Error('Network response was not ok');
                return res.json();
            })
            .then(data => {
                if (!data || data.length === 0) {
                    latestTutorialsList.textContent = 'No tutorials published yet.';
                    return;
                }

                // Sort by date descending
                data.sort((a, b) => {
                    const dateA = new Date(a.updatedAt || a.publishedAt || a.createdAt || 0);
                    const dateB = new Date(b.updatedAt || b.publishedAt || b.createdAt || 0);
                    return dateB - dateA;
                });

                const topTutorials = data.slice(0, 3);
                latestTutorialsList.innerHTML = ''; // Clear container

                topTutorials.forEach(tut => {
                    // Wrapper Link
                    const link = document.createElement('a');
                    link.href = tut.url ? tut.url : '#';
                    link.className = 'list-card-link';

                    // Main Card
                    const card = document.createElement('div');
                    card.className = 'list-card';

                    // Determine Icon and Colors based on category
                    let iconClass = 'fas fa-terminal';
                    let iconBg = '#000';
                    let iconColor = 'white';
                    let badgeBg = 'var(--bg-tertiary)';
                    let badgeColor = 'var(--brand-primary)';

                    const cat = (tut.category || '').toLowerCase();
                    if (cat.includes('windows')) {
                        iconClass = 'fab fa-windows';
                        iconBg = '#0078D7';
                    } else if (cat.includes('linux')) {
                        iconClass = 'fab fa-linux';
                        iconBg = '#f1f5f9';
                        iconColor = 'black';
                        badgeBg = 'rgba(16,185,129,0.1)';
                        badgeColor = 'var(--success)';
                    } else if (cat.includes('network') || cat.includes('active directory')) {
                        iconClass = 'fas fa-network-wired';
                        iconBg = '#e0f2fe';
                        iconColor = 'var(--brand-secondary)';
                    } else if (cat.includes('server')) {
                        iconClass = 'fas fa-server';
                        iconBg = '#4b5563';
                    } else if (cat.includes('cyber') || cat.includes('security')) {
                        iconClass = 'fas fa-shield-alt';
                        iconBg = '#fef08a';
                        iconColor = '#854d0e';
                    } else if (cat.includes('cloud')) {
                        iconClass = 'fas fa-cloud';
                        iconBg = '#0ea5e9';
                    }

                    // Icon Div
                    const iconDiv = document.createElement('div');
                    iconDiv.style.width = '80px';
                    iconDiv.style.height = '60px';
                    iconDiv.style.background = iconBg;
                    iconDiv.style.borderRadius = '8px';
                    iconDiv.style.display = 'flex';
                    iconDiv.style.alignItems = 'center';
                    iconDiv.style.justifyContent = 'center';
                    iconDiv.style.color = iconColor;
                    iconDiv.style.fontSize = '1.5rem';
                    const iconEl = document.createElement('i');
                    iconEl.className = iconClass;
                    iconDiv.appendChild(iconEl);
                    card.appendChild(iconDiv);

                    // Content Div
                    const contentDiv = document.createElement('div');
                    contentDiv.style.flexGrow = '1';

                    // Header Row (Title and Badge)
                    const headerRow = document.createElement('div');
                    headerRow.style.display = 'flex';
                    headerRow.style.justifyContent = 'space-between';
                    
                    const titleEl = document.createElement('h4');
                    titleEl.style.margin = '0';
                    titleEl.style.fontSize = '0.95rem';
                    titleEl.textContent = tut.title || 'Untitled';
                    
                    const badgeEl = document.createElement('span');
                    badgeEl.style.fontSize = '0.7rem';
                    badgeEl.style.background = badgeBg;
                    badgeEl.style.color = badgeColor;
                    badgeEl.style.padding = '2px 6px';
                    badgeEl.style.borderRadius = '4px';
                    badgeEl.textContent = tut.category || 'Uncategorized';
                    
                    headerRow.appendChild(titleEl);
                    headerRow.appendChild(badgeEl);
                    contentDiv.appendChild(headerRow);

                    // Description
                    const descEl = document.createElement('p');
                    descEl.style.fontSize = '0.8rem';
                    descEl.style.color = 'var(--text-secondary)';
                    descEl.style.margin = '0.25rem 0';
                    descEl.textContent = tut.description || '';
                    contentDiv.appendChild(descEl);

                    // Meta Row (Read Time, Level, Date)
                    const metaRow = document.createElement('div');
                    metaRow.style.display = 'flex';
                    metaRow.style.justifyContent = 'space-between';
                    metaRow.style.fontSize = '0.75rem';
                    metaRow.style.color = 'var(--text-muted)';
                    
                    const leftMeta = document.createElement('span');
                    leftMeta.innerHTML = `<i class="fas fa-clock"></i> ${tut.readTime || '5 min'} &nbsp;&nbsp; <i class="fas fa-signal"></i> ${tut.level || 'Beginner'}`;
                    
                    const rightMeta = document.createElement('span');
                    const dateObj = new Date(tut.updatedAt || tut.publishedAt || tut.createdAt || 0);
                    rightMeta.textContent = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                    
                    metaRow.appendChild(leftMeta);
                    metaRow.appendChild(rightMeta);
                    contentDiv.appendChild(metaRow);

                    card.appendChild(contentDiv);
                    link.appendChild(card);
                    latestTutorialsList.appendChild(link);
                });
            })
            .catch(err => {
                console.error('Failed to load tutorials:', err);
                latestTutorialsList.textContent = 'Unable to load tutorials.';
            });
    }
});
