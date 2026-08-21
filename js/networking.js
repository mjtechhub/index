/**
 * MJ Tech Hub - Networking Learning Path
 * Dynamically renders the learning path from topics.json.
 */

document.addEventListener('DOMContentLoaded', () => {
    const learningPath = document.getElementById('networking-learning-path');
    
    if (!learningPath) return;
    
    fetch('./data/topics.json')
        .then(res => {
            if (!res.ok) throw new Error('Failed to load topics data');
            return res.json();
        })
        .then(data => {
            const categories = data.categories || [];
            const networking = categories.find(c => c.id === 'networking');
            
            if (networking && networking.sections) {
                renderLearningPath(networking.sections, learningPath);
            } else {
                throw new Error('Networking data not found');
            }
        })
        .catch(err => {
            console.error('Error rendering networking path:', err);
            learningPath.innerHTML = '<p class="error-msg">Unable to load curriculum at this time. Please try again later.</p>';
        });
        
    function renderLearningPath(sections, container) {
        container.innerHTML = '';
        
        sections.forEach(section => {
            const sectionDiv = document.createElement('div');
            sectionDiv.style.marginBottom = '2rem';
            
            const title = document.createElement('h3');
            title.style.color = 'var(--brand-primary)';
            title.style.marginBottom = '1rem';
            title.style.borderBottom = '2px solid var(--border-color)';
            title.style.paddingBottom = '0.5rem';
            title.innerHTML = `<i class="fas fa-book-open"></i> ${section.name}`;
            sectionDiv.appendChild(title);
            
            const grid = document.createElement('div');
            grid.className = 'topic-grid';
            grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
            
            if (section.subtopics) {
                section.subtopics.forEach(topic => {
                    const card = document.createElement('a');
                    card.href = topic.url;
                    card.className = 'card topic-card';
                    card.style.textDecoration = 'none';
                    card.style.display = 'flex';
                    card.style.flexDirection = 'column';
                    card.style.padding = '1.25rem';
                    card.style.borderLeft = '4px solid var(--brand-secondary)';
                    
                    let levelBadge = '';
                    if (topic.level) {
                        const bg = topic.level === 'Beginner' ? 'rgba(16,185,129,0.1)' : 'rgba(59,130,246,0.1)';
                        const color = topic.level === 'Beginner' ? 'var(--success)' : 'var(--brand-primary)';
                        levelBadge = `<span style="font-size: 0.7rem; background: ${bg}; color: ${color}; padding: 2px 8px; border-radius: 12px; margin-top: 0.5rem; display: inline-block;">${topic.level}</span>`;
                    }
                    
                    card.innerHTML = `
                        <h4 style="font-size: 1.05rem; margin-bottom: 0.25rem; color: var(--text-primary); transition: color 0.2s;">${topic.name}</h4>
                        <p style="font-size: 0.85rem; color: var(--text-secondary); margin: 0; display: flex; justify-content: space-between; align-items: center;">
                            Read Lesson &rarr;
                            ${levelBadge}
                        </p>
                    `;
                    grid.appendChild(card);
                });
            }
            
            sectionDiv.appendChild(grid);
            container.appendChild(sectionDiv);
        });
    }
});
