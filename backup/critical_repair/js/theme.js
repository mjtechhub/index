/**
 * MJ Tech Hub - Theme Management
 * Handles light/dark mode toggling and persistence centrally.
 * Uses event delegation to support dynamically injected headers.
 */

(function() {
    // 1. Initialize theme immediately to prevent FOUC (Flash of Unstyled Content)
    const root = document.documentElement;
    const storageKey = 'mj-theme';
    
    function applyTheme(theme) {
        root.setAttribute('data-theme', theme);
        
        // Update all theme toggle icons currently in the DOM
        const icons = document.querySelectorAll('.theme-toggle i');
        icons.forEach(icon => {
            icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
        });
    }

    // 2. Setup Event Delegation for toggling (works with dynamically injected header)
    document.addEventListener('click', (e) => {
        const toggleBtn = e.target.closest('.theme-toggle');
        if (toggleBtn) {
            const currentTheme = root.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            // Enable CSS transitions before changing the theme
            document.body.classList.add('theme-transition');
            
            localStorage.setItem(storageKey, newTheme);
            applyTheme(newTheme);
        }
    });

    // 3. Ensure the icon is correct once the DOM (and dynamic header) loads
    const observer = new MutationObserver((mutations) => {
        for (const m of mutations) {
            if (m.addedNodes.length > 0) {
                const currentTheme = root.getAttribute('data-theme') || 'light';
                const icons = document.querySelectorAll('.theme-toggle i');
                icons.forEach(icon => {
                    const expectedClass = currentTheme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
                    if (icon.className !== expectedClass) {
                        icon.className = expectedClass;
                    }
                });
            }
        }
    });
    
    document.addEventListener('DOMContentLoaded', () => {
        observer.observe(document.body, { childList: true, subtree: true });
    });
})();
