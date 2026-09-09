/**
 * MJ Tech Hub - Topics Architecture
 * Dynamically renders core and specialized IT topics from JSON with dynamic tutorial counts.
 */

document.addEventListener('DOMContentLoaded', () => {
    const coreGrid = document.getElementById('core-topics-grid');
    const moreGrid = document.getElementById('more-topics-grid');
    const homeGrid = document.getElementById('home-topics-grid');
    const totalTutBadge = document.getElementById('topics-total-tut-badge');
    
    if (!coreGrid && !moreGrid && !homeGrid) return;
    
    // Base path logic for data
    const scripts = document.getElementsByTagName('script');
    let basePath = '.';
    for (let script of scripts) {
        if (script.src && script.src.includes('js/topics.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/topics.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }
    
    Promise.all([
        fetch(`${basePath}/data/topics.json`).then(r => r.ok ? r.json() : { categories: [] }).catch(() => ({ categories: [] })),
        fetch(`${basePath}/data/tutorials.json`).then(r => r.ok ? r.json() : []).catch(() => [])
    ]).then(([topicsData, tutsData]) => {
        const categories = topicsData.categories || [];
        const tutorials = Array.isArray(tutsData) ? tutsData : [];
        
        // Count tutorials per category
        const tutCounts = {};
        tutorials.forEach(tut => {
            const cat = (tut.category || '').toLowerCase().trim();
            tutCounts[cat] = (tutCounts[cat] || 0) + 1;
        });

        // Update total badge if on topics.html
        if (totalTutBadge) {
            totalTutBadge.innerHTML = `<i class="fa-solid fa-book-open" aria-hidden="true"></i> ${tutorials.length} Published Tutorials`;
        }

        const coreTopics = categories.filter(c => c.type === 'core');
        const moreTopics = categories.filter(c => c.type === 'more');
        
        if (coreGrid) renderCoreTopics(coreTopics, tutCounts, coreGrid, basePath);
        if (moreGrid) renderMoreTopics(moreTopics, moreGrid, basePath);
        if (homeGrid) renderHomeTopics(coreTopics, homeGrid, basePath);
    }).catch(err => {
        console.error('Error rendering topics:', err);
    });
        
    function renderCoreTopics(topics, tutCounts, container, basePath) {
        container.innerHTML = '';
        topics.forEach(topic => {
            const card = document.createElement('a');
            card.href = `${basePath}/${topic.url}`;
            card.className = 'topic-domain-card';
            
            const accentVar = `var(--cat-${topic.accent}, var(--brand-primary))`;
            card.style.borderTop = `3px solid ${accentVar}`;
            
            const count = tutCounts[topic.id.toLowerCase()] || tutCounts[topic.name.toLowerCase()] || 0;
            const hasContent = count > 0;
            
            // Top Row (Icon & Count Badge)
            const topRow = document.createElement('div');
            topRow.className = 'topic-domain-top';
            
            const iconWrap = document.createElement('div');
            iconWrap.className = 'topic-domain-icon';
            const iconImg = document.createElement('img');
            iconImg.src = `${basePath}/${topic.icon.replace('./', '')}`;
            iconImg.alt = '';
            iconImg.width = 28;
            iconImg.height = 28;
            iconWrap.appendChild(iconImg);
            
            const countBadge = document.createElement('span');
            countBadge.className = `topic-tut-count-badge ${hasContent ? 'has-content' : ''}`;
            countBadge.textContent = hasContent ? `${count} Tutorials` : 'In preparation';
            
            topRow.appendChild(iconWrap);
            topRow.appendChild(countBadge);
            card.appendChild(topRow);
            
            // Title
            const title = document.createElement('h3');
            title.className = 'topic-domain-title';
            title.textContent = topic.name;
            card.appendChild(title);
            
            // Description
            const desc = document.createElement('p');
            desc.className = 'topic-domain-desc';
            desc.textContent = topic.description;
            card.appendChild(desc);
            
            // Footer CTA
            const footer = document.createElement('div');
            footer.className = 'topic-domain-footer';
            footer.style.color = accentVar;
            footer.innerHTML = `<span>Explore ${topic.name}</span> <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>`;
            card.appendChild(footer);
            
            container.appendChild(card);
        });
    }

    function renderMoreTopics(topics, container, basePath) {
        container.innerHTML = '';
        topics.forEach(topic => {
            const isComingSoon = topic.url === '#' || topic.url === '';
            const card = document.createElement(isComingSoon ? 'div' : 'a');
            
            if (!isComingSoon) {
                card.href = `${basePath}/${topic.url}`;
                card.style.cursor = 'pointer';
            }
            
            card.className = 'specialized-topic-card';
            
            const accentVar = `var(--cat-${topic.accent}, var(--brand-primary))`;
            card.style.borderLeftColor = accentVar;
            
            const statusBadge = document.createElement('span');
            statusBadge.className = 'specialized-status';
            statusBadge.textContent = 'Coming Soon';
            card.appendChild(statusBadge);
            
            const title = document.createElement('h4');
            title.textContent = topic.name;
            card.appendChild(title);
            
            const desc = document.createElement('p');
            desc.textContent = topic.description;
            card.appendChild(desc);
            
            container.appendChild(card);
        });
    }

    // Unmodified Homepage Topic Renderer - Preserves Phase 4 Homepage Stability
    function renderHomeTopics(topics, container, basePath) {
        container.innerHTML = '';
        topics.forEach(topic => {
            const card = document.createElement('div');
            card.className = 'home-topic-card card';
            
            const accentVar = `var(--cat-${topic.accent}, var(--brand-primary))`;
            
            // Header row with icon and title
            const headerRow = document.createElement('div');
            headerRow.className = 'topic-header-row';
            
            const iconWrap = document.createElement('div');
            iconWrap.className = 'topic-icon-wrap';
            
            const iconImg = document.createElement('img');
            iconImg.src = `${basePath}/${topic.icon.replace('./', '')}`;
            iconImg.alt = '';
            iconImg.width = 28;
            iconImg.height = 28;
            iconImg.style.objectFit = 'contain';
            iconWrap.appendChild(iconImg);
            
            const title = document.createElement('h3');
            title.className = 'topic-title';
            title.style.color = accentVar;
            title.textContent = topic.name;
            
            headerRow.appendChild(iconWrap);
            headerRow.appendChild(title);
            card.appendChild(headerRow);
            
            // Description
            const desc = document.createElement('p');
            desc.className = 'topic-desc';
            desc.textContent = topic.description;
            card.appendChild(desc);
            
            // CTA Link
            const cta = document.createElement('a');
            cta.href = `${basePath}/${topic.url}`;
            cta.className = 'topic-cta';
            cta.style.color = accentVar;
            cta.innerHTML = `Explore <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>`;
            card.appendChild(cta);
            
            container.appendChild(card);
        });
    }
});
