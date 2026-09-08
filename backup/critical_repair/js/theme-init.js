/**
 * MJ Tech Hub - Theme Initialization Bootstrap
 * This script MUST run synchronously in the <head> before page rendering
 * to prevent the Flash of Unstyled Content (FOUC).
 */
(function() {
    try {
        var savedTheme = localStorage.getItem('mj-theme');
        if (savedTheme === 'light' || savedTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', savedTheme);
        } else {
            // No saved preference. Fallback to system preference, otherwise light.
            var isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
        }
    } catch (e) {
        // Fallback if localStorage is restricted
        document.documentElement.setAttribute('data-theme', 'dark');
    }
})();
