/**
 * MJ Tech Hub - Topics Architecture
 * Dynamically renders core and more IT topics from JSON.
 */

document.addEventListener('DOMContentLoaded', () => {
    const coreGrid = document.getElementById('core-topics-grid');
    const moreGrid = document.getElementById('more-topics-grid');
    const homeGrid = document.getElementById('home-topics-grid');
    
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
    
    fetch(`${basePath}/data/topics.json`)
        .then(res => {
            if (!res.ok) throw new Error('Failed to load topics data');
            return res.json();
        })
        .then(data => {
            const categories = data.categories || [];
            const coreTopics = categories.filter(c => c.type === 'core');
            const moreTopics = categories.filter(c => c.type === 'more');
            
            if (coreGrid) renderCoreTopics(coreTopics, coreGrid, basePath);
            if (moreGrid) renderMoreTopics(moreTopics, moreGrid, basePath);
            if (homeGrid) renderHomeTopics(coreTopics, homeGrid, basePath);
        })
        .catch(err => {
            console.error('Error rendering topics:', err);
        });
        
    function renderCoreTopics(topics, container, basePath) {
        container.innerHTML = '';
        topics.forEach(topic => {
            const card = document.createElement('div');
            card.className = `topic-card`;
            
            // Map accent from css variables
            let accentVar = `var(--cat-${topic.accent}, var(--brand-primary))`;
            
            card.style.borderTop = `4px solid ${accentVar}`;
            
            card.innerHTML = `
                <div class="topic-icon-wrap" style="border-radius: 50%; width: 72px; height: 72px; border: 1px solid rgba(255,255,255,0.05);">
                    <img src="${basePath}/${topic.icon.replace('./', '')}" alt="${topic.name}" style="width: 40px; height: 40px; object-fit: contain;">
                </div>
                <h3 class="topic-title">${topic.name}</h3>
                <p class="topic-desc">${topic.description}</p>
                <a href="${basePath}/${topic.url}" class="btn btn-primary topic-cta">Explore ${topic.name}</a>
            `;
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
            } else {
                card.style.cursor = 'default';
            }
            
            card.className = `card`;
            card.style.textDecoration = 'none';
            card.style.display = 'block';
            card.style.padding = '1.5rem';
            card.style.position = 'relative';
            
            let accentVar = `var(--cat-${topic.accent}, var(--brand-primary))`;
            card.style.borderLeft = `3px solid ${accentVar}`;
            
            let comingSoonBadge = isComingSoon ? `<span style="position: absolute; top: 1rem; right: 1rem; font-size: 0.7rem; background: var(--bg-secondary); padding: 0.2rem 0.5rem; border-radius: 4px; color: var(--text-secondary); border: 1px solid var(--border-color);">Coming Soon</span>` : '';

            card.innerHTML = `
                ${comingSoonBadge}
                <h3 style="font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--text-primary); transition: color 0.2s;">${topic.name}</h3>
                <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0; line-height: 1.4;">${topic.description}</p>
            `;
            
            if (!isComingSoon) {
                card.addEventListener('mouseenter', () => {
                    card.querySelector('h3').style.color = accentVar;
                });
                card.addEventListener('mouseleave', () => {
                    card.querySelector('h3').style.color = 'var(--text-primary)';
                });
            } else {
                card.querySelector('h3').style.color = 'var(--text-secondary)';
            }
            
            container.appendChild(card);
        });
    }

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
