/**
 * MJ Tech Hub - Tutorial Architecture
 * Dynamically loads breadcrumbs and metadata from tutorials.json
 */

document.addEventListener('DOMContentLoaded', () => {
    const tutorialHeader = document.getElementById('tutorial-header');
    
    if (!tutorialHeader) return;
    
    const scripts = document.getElementsByTagName('script');
    let basePath = '.';
    for (let script of scripts) {
        if (script.src && script.src.includes('js/tutorial.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/tutorial.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }

    const currentPath = window.location.pathname;
    let urlSlug = currentPath.substring(currentPath.lastIndexOf('tutorials/'));
    if (urlSlug.startsWith('/')) urlSlug = urlSlug.substring(1);
    
    const parts = currentPath.split('/');
    const filename = parts[parts.length - 1];
    
    fetch(`${basePath}/data/tutorials.json`)
        .then(res => {
            if (!res.ok) throw new Error('Failed to load tutorials data');
            return res.json();
        })
        .then(data => {
            let tutorials = Array.isArray(data) ? data : (data.tutorials || []);
            let currentTut = tutorials.find(t => t.url.includes(filename) || t.url === urlSlug);
            
            if (currentTut) {
                renderTutorialHeader(currentTut, basePath);
            } else {
                console.warn('Tutorial metadata not found for this page.');
            }
        })
        .catch(err => {
            console.error('Error rendering tutorial header:', err);
        });

    function renderTutorialHeader(tut, basePath) {
        let levelColor = 'var(--success)';
        if (tut.level === 'Intermediate') levelColor = 'var(--warning)';
        if (tut.level === 'Advanced') levelColor = 'var(--danger)';

        const html = `
            <!-- Breadcrumb -->
            <div class="breadcrumb" style="margin-bottom: 2rem;">
                <a href="${basePath}/index.html" style="color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; font-weight: 500;">
                    Home
                </a> 
                <span style="color: var(--text-muted); margin: 0 0.5rem;">/</span>
                <a href="${basePath}/${tut.category.toLowerCase()}.html" style="color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; font-weight: 500;">
                    ${tut.category}
                </a>
            </div>
            
            <div style="display: flex; gap: 0.75rem; align-items: center; margin-bottom: 1.5rem;">
                <span style="font-size: 0.75rem; font-weight: 700; color: ${levelColor}; background: rgba(255,255,255,0.05); padding: 0.35rem 0.85rem; border-radius: 20px; text-transform: uppercase; border: 1px solid ${levelColor}33;">
                    ${tut.level}
                </span>
                <span style="font-size: 0.85rem; color: var(--text-muted); display: flex; align-items: center; gap: 0.35rem;">
                    <i class="fa-regular fa-clock"></i> ${tut.readTime || '5 min read'}
                </span>
            </div>
            
            <h1 style="font-size: clamp(2.5rem, 5vw, 3.5rem); line-height: 1.1; margin-bottom: 1rem; color: var(--text-primary); font-weight: 800;">
                ${tut.title}
            </h1>
            
            <p style="font-size: 1.2rem; color: var(--text-secondary); margin-bottom: 3rem; max-width: 700px; line-height: 1.6;">
                ${tut.description}
            </p>
            
            <div style="border-bottom: 1px solid var(--border-color); margin-bottom: 3rem; width: 100%;"></div>
        `;
        
        tutorialHeader.innerHTML = html;
    }
});
