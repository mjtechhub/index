/**
 * MJ Tech Hub - Search Logic
 * Client-side search across multiple JSON datasets.
 * Ensures DOM-safe injection without unsafe innerHTML.
 */

document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('search-results');
    const resultsInfo = document.getElementById('results-info');
    
    let searchData = [];
    
    // Fetch all data
    Promise.all([
        fetch('./data/topics.json').then(res => res.json()),
        fetch('./data/tutorials.json').then(res => res.json()),
        fetch('./data/commands.json').then(res => res.json())
    ]).then(([topics, tutorials, commands]) => {
        
        // Normalize data for search
        topics.forEach(t => searchData.push({
            type: 'Topic',
            title: t.title,
            description: t.description,
            keywords: t.keywords,
            url: `topics.html`
        }));
        
        tutorials.forEach(t => searchData.push({
            type: 'Tutorial',
            title: t.title,
            description: t.description,
            keywords: t.keywords,
            url: `topics.html` // Simplified routing
        }));
        
        commands.forEach(c => searchData.push({
            type: 'Command',
            title: c.command,
            description: c.purpose,
            keywords: c.platform,
            url: 'commands.html'
        }));
        
    }).catch(err => {
        console.error("Failed to load search data", err);
    });
    
    // Focus input on load
    if(searchInput) searchInput.focus();
    
    if (searchForm) {
        searchForm.addEventListener('submit', performSearch);
    }
    
    function performSearch() {
        const query = searchInput.value.trim().toLowerCase();
        
        // Clear previous results safely
        while (resultsContainer.firstChild) {
            resultsContainer.removeChild(resultsContainer.firstChild);
        }
        
        if (!query) {
            resultsInfo.style.display = 'none';
            return;
        }
        
        const results = searchData.filter(item => {
            return (item.title && item.title.toLowerCase().includes(query)) ||
                   (item.description && item.description.toLowerCase().includes(query)) ||
                   (item.keywords && item.keywords.toLowerCase().includes(query));
        });
        
        renderResults(results, query);
    }
    
    function renderResults(results, query) {
        resultsInfo.style.display = 'block';
        resultsInfo.textContent = `Showing ${results.length} result(s) for "${query}"`;
        
        if (results.length === 0) {
            const noRes = document.createElement('div');
            noRes.className = 'no-results';
            
            const icon = document.createElement('i');
            icon.className = 'fas fa-search';
            noRes.appendChild(icon);
            
            const msg = document.createElement('h3');
            msg.textContent = 'No results found. Try another keyword.';
            noRes.appendChild(msg);
            
            resultsContainer.appendChild(noRes);
            return;
        }
        
        results.forEach(res => {
            const card = document.createElement('a');
            card.className = 'result-card';
            card.href = res.url;
            card.style.display = 'block';
            card.style.textDecoration = 'none';
            
            const typeLabel = document.createElement('span');
            typeLabel.className = 'result-type';
            typeLabel.textContent = res.type;
            
            const title = document.createElement('h3');
            title.className = 'result-title';
            title.textContent = res.title;
            
            const desc = document.createElement('p');
            desc.className = 'result-desc';
            desc.textContent = res.description;
            
            card.appendChild(typeLabel);
            card.appendChild(title);
            card.appendChild(desc);
            
            resultsContainer.appendChild(card);
        });
    }
});
