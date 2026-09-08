/**
 * MJ Tech Hub - Main JavaScript
 * Handles global functionality like mobile menu
 */

if (window.mjMainInitialized) {
    // Prevent duplicate initialization
} else {
    window.mjMainInitialized = true;

    function initMain() {
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
    


    // Dynamic Statistics (Homepage)
    const statTutorials = document.getElementById('stat-tutorials');
    const statCommands = document.getElementById('stat-commands');
    const statTopics = document.getElementById('stat-topics');
    const statQuizzes = document.getElementById('stat-quizzes');

    if (statTutorials || statCommands || statTopics || statQuizzes) {
        fetch('./data/tutorials.json')
            .then(res => res.ok ? res.json() : [])
            .then(data => {
                if (statTutorials && Array.isArray(data)) {
                    statTutorials.textContent = data.length + '+';
                }
            })
            .catch(() => {});

        fetch('./data/commands.json')
            .then(res => res.ok ? res.json() : [])
            .then(data => {
                if (statCommands && Array.isArray(data)) {
                    statCommands.textContent = data.length;
                }
            })
            .catch(() => {});

        fetch('./data/topics.json')
            .then(res => res.ok ? res.json() : {})
            .then(data => {
                if (statTopics && data.categories) {
                    const coreCount = data.categories.filter(c => c.type === 'core').length;
                    statTopics.textContent = coreCount || 6;
                }
            })
            .catch(() => {});

        fetch('./data/quizzes.json')
            .then(res => res.ok ? res.json() : [])
            .then(data => {
                if (statQuizzes && Array.isArray(data)) {
                    statQuizzes.textContent = data.length;
                }
            })
            .catch(() => {});
    }

    // Dynamic Latest Tutorials (Homepage)
    const latestTutorialsList = document.getElementById('latest-tutorials-list');
    if (latestTutorialsList) {
        fetch('./data/tutorials.json')
            .then(res => {
                if (!res.ok) throw new Error('Network response was not ok');
                return res.json();
            })
            .then(data => {
                if (!data || !Array.isArray(data) || data.length === 0) {
                    latestTutorialsList.textContent = 'No tutorials published yet.';
                    return;
                }

                function parseDate(val) {
                    if (!val || val === 'UNKNOWN') return 0;
                    const d = new Date(val).getTime();
                    return isNaN(d) ? 0 : d;
                }

                // Sort by date descending
                const sorted = [...data].sort((a, b) => {
                    const dateA = parseDate(a.updatedAt || a.publishedAt || a.createdAt);
                    const dateB = parseDate(b.updatedAt || b.publishedAt || b.createdAt);
                    return dateB - dateA;
                });

                const topTutorials = sorted.slice(0, 3);
                latestTutorialsList.innerHTML = ''; // Clear container

                topTutorials.forEach(tut => {
                    const link = document.createElement('a');
                    link.href = tut.url || '#';
                    link.className = 'dash-tut-card';

                    // Determine icon and colors based on category
                    let iconPath = './assets/icons/networking.png';
                    let badgeBg = 'rgba(37, 99, 235, 0.1)';
                    let badgeColor = 'var(--cat-networking, #2563EB)';

                    const cat = (tut.category || '').toLowerCase();
                    if (cat.includes('windows')) {
                        iconPath = './assets/icons/windows.png';
                        badgeBg = 'rgba(2, 132, 199, 0.1)';
                        badgeColor = 'var(--cat-windows, #0284C7)';
                    } else if (cat.includes('linux')) {
                        iconPath = './assets/icons/linux.png';
                        badgeBg = 'rgba(16, 185, 129, 0.1)';
                        badgeColor = 'var(--cat-linux, #10B981)';
                    } else if (cat.includes('server')) {
                        iconPath = './assets/icons/servers.png';
                        badgeBg = 'rgba(124, 58, 237, 0.1)';
                        badgeColor = 'var(--cat-servers, #7C3AED)';
                    } else if (cat.includes('cyber') || cat.includes('security')) {
                        iconPath = './assets/icons/cybersecurity.png';
                        badgeBg = 'rgba(249, 115, 22, 0.1)';
                        badgeColor = 'var(--cat-cybersecurity, #F97316)';
                    } else if (cat.includes('cloud') || cat.includes('ai')) {
                        iconPath = './assets/icons/cloud-ai.png';
                        badgeBg = 'rgba(6, 182, 212, 0.1)';
                        badgeColor = 'var(--cat-cloud, #06B6D4)';
                    }

                    // Thumbnail
                    const thumb = document.createElement('div');
                    thumb.className = 'dash-tut-thumb';
                    const thumbImg = document.createElement('img');
                    thumbImg.src = iconPath;
                    thumbImg.alt = '';
                    thumbImg.width = 26;
                    thumbImg.height = 26;
                    thumb.appendChild(thumbImg);
                    link.appendChild(thumb);

                    // Body
                    const body = document.createElement('div');
                    body.className = 'dash-tut-body';

                    // Title Row
                    const titleRow = document.createElement('div');
                    titleRow.className = 'dash-tut-title-row';

                    const titleEl = document.createElement('h4');
                    titleEl.className = 'dash-tut-title';
                    titleEl.textContent = tut.title || 'Untitled';

                    const badgeEl = document.createElement('span');
                    badgeEl.className = 'dash-tut-badge';
                    badgeEl.style.backgroundColor = badgeBg;
                    badgeEl.style.color = badgeColor;
                    badgeEl.textContent = tut.category || 'General';

                    titleRow.appendChild(titleEl);
                    titleRow.appendChild(badgeEl);
                    body.appendChild(titleRow);

                    // Description
                    const descEl = document.createElement('p');
                    descEl.className = 'dash-tut-desc';
                    descEl.textContent = tut.description || '';
                    body.appendChild(descEl);

                    // Meta Row
                    const metaRow = document.createElement('div');
                    metaRow.className = 'dash-tut-meta';

                    const metaLeft = document.createElement('span');
                    metaLeft.innerHTML = `<i class="fa-regular fa-clock" aria-hidden="true"></i> ${tut.readTime || '5 min read'} &nbsp;&bull;&nbsp; <i class="fa-solid fa-signal" aria-hidden="true"></i> ${tut.level || 'Beginner'}`;

                    metaRow.appendChild(metaLeft);

                    const timeVal = parseDate(tut.updatedAt || tut.publishedAt || tut.createdAt);
                    if (timeVal > 0) {
                        const dateSpan = document.createElement('span');
                        dateSpan.className = 'dash-tut-date';
                        dateSpan.textContent = new Date(timeVal).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                        metaRow.appendChild(dateSpan);
                    }

                    body.appendChild(metaRow);
                    link.appendChild(body);
                    latestTutorialsList.appendChild(link);
                });
            })
            .catch(err => {
                console.error('Failed to load tutorials:', err);
                latestTutorialsList.textContent = 'Unable to load tutorials.';
            });
    }

    // Dynamic Popular Commands (Homepage)
    const popularCommandsList = document.getElementById('popular-commands-list');
    if (popularCommandsList) {
        fetch('./data/commands.json')
            .then(res => res.ok ? res.json() : [])
            .then(commands => {
                popularCommandsList.innerHTML = '';
                if (!Array.isArray(commands) || commands.length === 0) {
                    popularCommandsList.textContent = 'No commands available.';
                    return;
                }

                commands.slice(0, 12).forEach(cmd => {
                    const pill = document.createElement('a');
                    pill.href = 'commands.html';
                    pill.className = 'command-pill';
                    if (cmd.purpose) {
                        pill.title = cmd.purpose;
                    }
                    const code = document.createElement('code');
                    code.textContent = cmd.command;
                    pill.appendChild(code);
                    popularCommandsList.appendChild(pill);
                });
            })
            .catch(err => {
                console.error('Failed to load popular commands:', err);
            });
    }
}

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMain);
    } else {
        initMain();
    }
}
