/**
 * MJ Tech Hub - Theme Management
 * Handles light/dark mode toggling and persistence
 */

document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const root = document.documentElement;
    const themeIcon = themeToggleBtn?.querySelector('i');
    
    // Check for saved theme preference in localStorage
    const savedTheme = localStorage.getItem('mj-theme');
    
    // Set initial theme
    if (savedTheme === 'dark') {
        root.setAttribute('data-theme', 'dark');
        updateIcon('dark');
    } else {
        root.setAttribute('data-theme', 'light');
        updateIcon('light');
    }
    
    // Toggle theme on button click
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = root.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            root.setAttribute('data-theme', newTheme);
            localStorage.setItem('mj-theme', newTheme);
            updateIcon(newTheme);
        });
    }
    
    // Helper function to update the icon
    function updateIcon(theme) {
        if (!themeIcon) return;
        
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-sun'; // Show sun when in dark mode
        } else {
            themeIcon.className = 'fas fa-moon'; // Show moon when in light mode
        }
    }
});
