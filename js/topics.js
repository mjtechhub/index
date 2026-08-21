/**
 * MJ Tech Hub - Topics Architecture
 * Dynamically renders core and more IT topics from JSON.
 */

document.addEventListener('DOMContentLoaded', () => {
    const coreGrid = document.getElementById('core-topics-grid');
    const moreGrid = document.getElementById('more-topics-grid');
    
    if (!coreGrid && !moreGrid) return;
    
    fetch('./data/topics.json')
        .then(res => {
            if (!res.ok) throw new Error('Failed to load topics data');
            return res.json();
        })
        .then(data => {
            const categories = data.categories || [];
            const coreTopics = categories.filter(c => c.type === 'core');
            const moreTopics = categories.filter(c => c.type === 'more');
            
            if (coreGrid) renderCoreTopics(coreTopics, coreGrid);
            if (moreGrid) renderMoreTopics(moreTopics, moreGrid);
        })
        .catch(err => {
            console.error('Error rendering topics:', err);
            if (coreGrid) coreGrid.innerHTML = '<p class="error-msg">Unable to load topics at this time. Please try again later.</p>';
        });
        
    function renderCoreTopics(topics, container) {
        container.innerHTML = '';
        topics.forEach(topic => {
            const card = document.createElement('div');
            card.className = `card topic-card topic-accent-${topic.accent}`;
            card.style.flexDirection = 'column';
            card.style.alignItems = 'center';
            card.style.textAlign = 'center';
            card.style.gap = '0.5rem';
            card.style.padding = '2rem 1.5rem';
            
            card.innerHTML = `
                <img src="${topic.icon}" alt="${topic.name}" style="width: 64px; height: 64px; margin-bottom: 1rem;">
                <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem; color: var(--text-primary);">${topic.name}</h3>
                <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.5; margin-bottom: 1.5rem; flex-grow: 1;">
                    ${topic.description}
                </p>
                <a href="${topic.url}" class="btn btn-primary" style="width: 100%; text-align: center;">Explore ${topic.name}</a>
            `;
            container.appendChild(card);
        });
    }
    
    function renderMoreTopics(topics, container) {
        container.innerHTML = '';
        topics.forEach(topic => {
            const card = document.createElement('a');
            card.href = topic.url;
            card.className = `card topic-card topic-accent-${topic.accent}`;
            card.style.textDecoration = 'none';
            card.style.display = 'block';
            card.style.padding = '1.5rem';
            
            card.innerHTML = `
                <h3 style="font-size: 1.1rem; margin-bottom: 0.5rem;">${topic.name}</h3>
                <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0; line-height: 1.4;">${topic.description}</p>
            `;
            container.appendChild(card);
        });
    }
});
