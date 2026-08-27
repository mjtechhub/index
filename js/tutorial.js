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
                renderTutorialFooter(currentTut, tutorials, basePath);
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
            <nav aria-label="Breadcrumb" class="breadcrumb" style="margin-bottom: 2rem;">
                <a href="${basePath}/index.html" style="color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; font-weight: 500;">
                    Home
                </a> 
                <span style="color: var(--text-muted); margin: 0 0.5rem;">/</span>
                <a href="${basePath}/${tut.category.toLowerCase()}.html" style="color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; font-weight: 500;">
                    ${tut.category}
                </a>
                <span style="color: var(--text-muted); margin: 0 0.5rem;">/</span>
                <span aria-current="page" style="color: var(--text-primary); font-size: 0.9rem; font-weight: 600;">
                    ${tut.title}
                </span>
            </nav>
            
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

    function renderTutorialFooter(tut, tutorials, basePath) {
        const main = document.querySelector('main');
        if (!main) return;
        
        const existingNav = main.querySelector('div[style*="justify-content: space-between"]');
        if (existingNav) existingNav.remove();

        const footerDiv = document.createElement('div');
        footerDiv.id = "dynamic-tutorial-footer";
        footerDiv.style.marginTop = "4rem";

        const currentIndex = tutorials.findIndex(t => t.id === tut.id);
        const prev = currentIndex > 0 ? tutorials[currentIndex - 1] : null;
        const next = currentIndex < tutorials.length - 1 ? tutorials[currentIndex + 1] : null;
        
        let navHtml = `
            <nav aria-label="Tutorial navigation" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 4rem; border-top: 1px solid var(--border-color); padding-top: 2rem;">
        `;
        
        if (prev) {
            navHtml += `
                <a href="${basePath}/${prev.url}" style="text-decoration: none; display: flex; flex-direction: column; padding: 1.5rem; border: 1px solid var(--border-color); border-radius: 12px; background: var(--bg-secondary); transition: all 0.2s ease;" onmouseenter="this.style.borderColor='var(--brand-primary)'; this.style.transform='translateY(-2px)';" onmouseleave="this.style.borderColor='var(--border-color)'; this.style.transform='translateY(0)';">
                    <span style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;">&larr; Previous Tutorial</span>
                    <span style="font-size: 1.1rem; font-weight: 700; color: var(--text-primary); line-height: 1.3;">${prev.title}</span>
                </a>
            `;
        } else {
            navHtml += `<div></div>`;
        }
        
        if (next) {
            navHtml += `
                <a href="${basePath}/${next.url}" style="text-decoration: none; display: flex; flex-direction: column; align-items: flex-end; text-align: right; padding: 1.5rem; border: 1px solid var(--border-color); border-radius: 12px; background: var(--bg-secondary); transition: all 0.2s ease;" onmouseenter="this.style.borderColor='var(--brand-primary)'; this.style.transform='translateY(-2px)';" onmouseleave="this.style.borderColor='var(--border-color)'; this.style.transform='translateY(0)';">
                    <span style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;">Next Tutorial &rarr;</span>
                    <span style="font-size: 1.1rem; font-weight: 700; color: var(--text-primary); line-height: 1.3;">${next.title}</span>
                </a>
            `;
        } else {
            navHtml += `<div></div>`;
        }
        
        navHtml += `</nav>`;

        let relatedHtml = `
            <section aria-labelledby="related-heading" style="border-top: 1px solid var(--border-color); padding-top: 2rem; margin-bottom: 2rem;">
                <h2 id="related-heading" style="font-size: 1.5rem; font-weight: 800; margin-bottom: 1.5rem; color: var(--text-primary);">Related Tutorials</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        `;
        
        const tutKeywords = (tut.keywords || "").toLowerCase().split(',').map(k => k.trim()).filter(k => k);
        const scored = tutorials.map(t => {
            if (t.id === tut.id) return { t, score: -1 };
            let score = 0;
            if (t.category === tut.category) score += 5;
            
            const tKeywords = (t.keywords || "").toLowerCase().split(',').map(k => k.trim()).filter(k => k);
            const shared = tutKeywords.filter(k => tKeywords.includes(k)).length;
            score += shared * 10;
            
            if (t.level === tut.level) score += 2;
            
            return { t, score };
        }).filter(item => item.score >= 0);
        
        scored.sort((a, b) => b.score - a.score);
        const topRelated = scored.slice(0, 3).map(i => i.t);
        
        topRelated.forEach(r => {
            relatedHtml += `
                <a href="${basePath}/${r.url}" style="text-decoration: none; padding: 1.25rem; border: 1px solid var(--border-color); border-radius: 12px; background: var(--bg-secondary); display: flex; flex-direction: column; transition: all 0.2s ease;" onmouseenter="this.style.borderColor='var(--brand-primary)'; this.style.transform='translateY(-2px)';" onmouseleave="this.style.borderColor='var(--border-color)'; this.style.transform='translateY(0)';">
                    <span style="font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem; line-height: 1.3;">${r.title}</span>
                    <span style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${r.description}</span>
                </a>
            `;
        });
        
        relatedHtml += `</div></section>`;
        
        footerDiv.innerHTML = navHtml + relatedHtml;
        main.appendChild(footerDiv);
    }
});
