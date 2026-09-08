// js/components.js

document.addEventListener('DOMContentLoaded', () => {
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

    // Load header and footer
    
    // Dynamically load global search module
    function injectSearch(basePath) {
        if (document.querySelector('script[src*="search.js"]')) return;
        const script = document.createElement('script');
        script.src = `${basePath}/js/search.js`;
        script.defer = true;
        document.head.appendChild(script);
    }
    
    injectSearch(basePath);

    loadComponent(headerContainer, '/components/header.html', 'header');
    loadComponent(footerContainer, '/components/footer.html', 'footer');
});
