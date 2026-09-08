// js/components.js

function initComponents() {
    const headerContainer = document.getElementById('site-header');
    const footerContainer = document.getElementById('site-footer');

    // Determine the base path dynamically from this script's src attribute
    const scripts = document.getElementsByTagName('script');
    let basePath = '.';
    for (let script of scripts) {
        if (script.src && script.src.includes('js/components.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/components.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }

    function highlightActiveNav(headerEl) {
        if (!headerEl) return;
        const currentPath = window.location.pathname.toLowerCase();
        const navLinks = headerEl.querySelectorAll('.nav-links a');
        
        // Category paths that map to Topics navigation item
        const categoryKeywords = ['topics', 'tutorial', 'networking', 'windows', 'linux', 'servers', 'cybersecurity', 'cloud'];
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;
            const target = href.split('/').pop().toLowerCase();
            const targetSlug = target.replace('.html', '');
            
            let isActive = false;
            if (target === 'index.html') {
                const isHome = currentPath.endsWith('/') || currentPath.endsWith('/index.html') || currentPath.endsWith('/index') || currentPath === '';
                isActive = isHome;
            } else if (targetSlug === 'topics') {
                isActive = categoryKeywords.some(cat => currentPath.includes(cat));
            } else if (targetSlug) {
                isActive = currentPath.includes(targetSlug);
            }
            
            if (isActive) {
                link.classList.add('active');
                link.setAttribute('aria-current', 'page');
            } else {
                link.classList.remove('active');
                link.removeAttribute('aria-current');
            }
        });
    }

    async function loadComponent(container, path, componentName) {
        if (!container) return;
        try {
            // Fetch the component using the calculated base path
            const response = await fetch(`${basePath}${path}`);
            if (!response.ok) throw new Error(`Failed to load ${path}`);
            let html = await response.text();
            
            // Replace {{BASE}} placeholder with the actual base path to fix relative links
            html = html.replace(/\{\{BASE\}\}/g, basePath);
            
            container.innerHTML = html;

            if (componentName === 'header') {
                highlightActiveNav(container);
                
                // Ensure main container has id="main-content" for accessibility skip link
                const mainEl = document.querySelector('main');
                if (mainEl && !mainEl.id) {
                    mainEl.id = 'main-content';
                    if (!mainEl.hasAttribute('tabindex')) {
                        mainEl.setAttribute('tabindex', '-1');
                    }
                }
            }
        } catch (error) {
            console.error(`Failed to load ${componentName} component:`, error);
        }
    }

    function injectFavicons(basePath) {
        // Prevent duplicate injection
        if (document.querySelector('link[rel="icon"]')) return;

        const favicons = [
            { rel: 'icon', type: 'image/x-icon', href: '/assets/favicon/favicon.ico' },
            { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/assets/favicon/favicon-32x32.png' },
            { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/assets/favicon/favicon-16x16.png' },
            { rel: 'apple-touch-icon', sizes: '180x180', href: '/assets/favicon/apple-touch-icon.png' },
            { rel: 'icon', type: 'image/png', sizes: '512x512', href: '/assets/favicon/favicon-512x512.png' }
        ];

        const fragment = document.createDocumentFragment();
        favicons.forEach(favicon => {
            const link = document.createElement('link');
            link.rel = favicon.rel;
            if (favicon.type) link.type = favicon.type;
            if (favicon.sizes) link.sizes = favicon.sizes;
            link.href = `${basePath}${favicon.href}`;
            fragment.appendChild(link);
        });

        document.head.appendChild(fragment);
    }

    injectFavicons(basePath);

    // Dynamically load global search and main module safely
    function injectScript(basePath, scriptName) {
        if (scriptName === 'search.js' && window.mjSearchInitialized) return;
        if (scriptName === 'main.js' && window.mjMainInitialized) return;
        if (document.querySelector(`script[src*="${scriptName}"]`)) return;
        const script = document.createElement('script');
        script.src = `${basePath}/js/${scriptName}`;
        script.defer = true;
        document.head.appendChild(script);
    }
    
    injectScript(basePath, 'search.js');
    injectScript(basePath, 'main.js');

    loadComponent(headerContainer, '/components/header.html', 'header');
    loadComponent(footerContainer, '/components/footer.html', 'footer');
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initComponents);
} else {
    initComponents();
}

