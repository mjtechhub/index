/**
 * MJ Tech Hub - Tutorials Architecture
 * Dynamically renders tutorials from JSON.
 */

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('tutorials-grid');
    if (!grid) return;
    
    const categoryFilter = grid.getAttribute('data-category');
    
    // Base path logic for data
    const scripts = document.getElementsByTagName('script');
    let basePath = '.';
    for (let script of scripts) {
        if (script.src && script.src.includes('js/tutorials.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/tutorials.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }
    
    fetch(`${basePath}/data/tutorials.json`)
        .then(res => {
            if (!res.ok) throw new Error('Failed to load tutorials data');
            return res.json();
        })
        .then(data => {
            let tutorials = data;
            if (!Array.isArray(data)) {
                // If the json is an object { tutorials: [...] }
                tutorials = data.tutorials || [];
            }

            if (categoryFilter) {
                tutorials = tutorials.filter(t => t.category === categoryFilter);
            }
            
            renderTutorials(tutorials, grid, basePath);
        })
        .catch(err => {
            console.error('Error rendering tutorials:', err);
            grid.innerHTML = `<div style="grid-column: 1 / -1; padding: 2rem; color: var(--danger); text-align: center;">Failed to load tutorials.</div>`;
        });
        
    function renderTutorials(tutorials, container, basePath) {
        container.innerHTML = '';
        
        if (tutorials.length === 0) {
            container.innerHTML = `<div style="grid-column: 1 / -1; padding: 2rem; color: var(--text-muted); text-align: center;">No tutorials found.</div>`;
            return;
        }

        tutorials.forEach(tut => {
            const card = document.createElement('a');
            card.href = `${basePath}/${tut.url}`;
            card.className = `card`;
            card.style.textDecoration = 'none';
            card.style.display = 'flex';
            card.style.flexDirection = 'column';
            card.style.padding = '1.5rem';
            card.style.gap = '1rem';
            
            let levelColor = 'var(--success)';
            if (tut.level === 'Intermediate') levelColor = 'var(--warning)';
            if (tut.level === 'Advanced') levelColor = 'var(--danger)';
            
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <span style="font-size: 0.75rem; font-weight: 700; color: ${levelColor}; background: rgba(255,255,255,0.05); padding: 0.25rem 0.75rem; border-radius: 12px; text-transform: uppercase;">${tut.level}</span>
                    <span style="font-size: 0.8rem; color: var(--text-muted);"><i class="fa-regular fa-clock"></i> ${tut.readTime || '5 min'}</span>
                </div>
                <div>
                    <h3 style="font-size: 1.15rem; margin-bottom: 0.5rem; color: var(--text-primary); transition: color 0.2s;">${tut.title}</h3>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">${tut.description}</p>
                </div>
                <div style="margin-top: auto; display: flex; align-items: center; justify-content: space-between; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                    <span style="font-size: 0.85rem; color: var(--brand-secondary); font-weight: 600;">Read Tutorial</span>
                    <i class="fa-solid fa-arrow-right" style="color: var(--brand-secondary); font-size: 0.85rem;"></i>
                </div>
            `;
            
            // Hover effect
            card.addEventListener('mouseenter', () => {
                card.querySelector('h3').style.color = 'var(--brand-primary)';
            });
            card.addEventListener('mouseleave', () => {
                card.querySelector('h3').style.color = 'var(--text-primary)';
            });
            
            container.appendChild(card);
        });
    }
});
