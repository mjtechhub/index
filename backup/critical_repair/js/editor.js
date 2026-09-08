/**
 * MJ Tech Hub - Lesson Editor Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const titleInput = document.getElementById('lesson-title');
    const idInput = document.getElementById('lesson-id');
    const categoryInput = document.getElementById('lesson-category');
    const levelInput = document.getElementById('lesson-level');
    const timeInput = document.getElementById('lesson-time');
    const markdownInput = document.getElementById('lesson-markdown');
    
    const previewContainer = document.getElementById('live-preview');
    const saveStatus = document.getElementById('save-status');
    const btnClear = document.getElementById('btn-clear');
    
    const btnExportHtml = document.getElementById('btn-export-html');
    const btnExportJson = document.getElementById('btn-export-json');
    const btnExportZip = document.getElementById('btn-export-zip');

    // Auto-generate ID from Title if ID is empty
    titleInput.addEventListener('input', () => {
        if (!idInput.value || idInput.dataset.auto === "true") {
            idInput.value = titleInput.value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, '');
            idInput.dataset.auto = "true";
        }
        updatePreview();
        saveDraft();
    });

    idInput.addEventListener('input', () => {
        idInput.dataset.auto = "false";
        saveDraft();
    });

    // Add listeners to all inputs
    [categoryInput, levelInput, timeInput, markdownInput].forEach(el => {
        el.addEventListener('input', () => {
            updatePreview();
            saveDraft();
        });
    });

    btnClear.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear the editor? This cannot be undone.')) {
            titleInput.value = '';
            idInput.value = '';
            idInput.dataset.auto = "true";
            categoryInput.value = '';
            levelInput.value = 'Beginner';
            timeInput.value = '';
            markdownInput.value = '';
            updatePreview();
            saveDraft();
        }
    });

    function updatePreview() {
        const title = titleInput.value || 'Lesson Title';
        const category = categoryInput.value || 'Category';
        const level = levelInput.value || 'Beginner';
        const time = timeInput.value || '5 min read';
        const markdown = markdownInput.value || '*Start typing to see preview...*';

        const parsedContent = marked.parse(markdown);

        previewContainer.innerHTML = `
            <div class="breadcrumb">
                <a href="#">Home</a> &gt; 
                <a href="#">Topics</a> &gt; 
                <a href="#">${category}</a> &gt; 
                <span style="color: var(--brand-primary);">${title}</span>
            </div>
            
            <span class="topic-badge">${category}</span>
            <h1>${title}</h1>
            
            <div class="meta-info">
                <span><i class="fas fa-signal" style="color: var(--success);"></i> ${level}</span>
                <span><i class="fas fa-clock"></i> ${time}</span>
            </div>
            
            <div class="content">
                ${parsedContent}
            </div>
        `;
    }

    // Auto-save logic
    let saveTimeout;
    function saveDraft() {
        saveStatus.textContent = 'Saving...';
        clearTimeout(saveTimeout);
        
        saveTimeout = setTimeout(() => {
            const draft = {
                title: titleInput.value,
                id: idInput.value,
                category: categoryInput.value,
                level: levelInput.value,
                time: timeInput.value,
                markdown: markdownInput.value,
                timestamp: new Date().toISOString(),
                publishedAt: window.mjTechHub_publishedAt || null,
                updatedAt: new Date().toISOString().split('T')[0]
            };
            localStorage.setItem('mjTechHub_lessonDraft', JSON.stringify(draft));
            
            const timeStr = new Date().toLocaleTimeString();
            saveStatus.textContent = `Draft saved at ${timeStr}`;
        }, 1000);
    }

    function loadDraft() {
        const draftStr = localStorage.getItem('mjTechHub_lessonDraft');
        if (draftStr) {
            try {
                const draft = JSON.parse(draftStr);
                titleInput.value = draft.title || '';
                idInput.value = draft.id || '';
                if (draft.id) idInput.dataset.auto = "false";
                categoryInput.value = draft.category || '';
                levelInput.value = draft.level || 'Beginner';
                timeInput.value = draft.time || '';
                markdownInput.value = draft.markdown || '';
                
                if (draft.publishedAt) {
                    window.mjTechHub_publishedAt = draft.publishedAt;
                }
                
                const timeStr = new Date(draft.timestamp).toLocaleTimeString();
                saveStatus.textContent = `Draft restored from ${timeStr}`;
            } catch (e) {
                console.error("Error loading draft", e);
            }
        }
        updatePreview();
    }

    // Generate Final HTML String
    function generateFinalHTML() {
        const title = titleInput.value || 'Lesson Title';
        const category = categoryInput.value || 'Category';
        const level = levelInput.value || 'Beginner';
        const time = timeInput.value || '5 min read';
        let markdown = markdownInput.value || '';
        
        // Remove duplicate H1 if it exactly matches the title
        const escapedTitle = title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const h1Regex = new RegExp(`^#\\s*${escapedTitle}\\s*\\n`, 'i');
        markdown = markdown.replace(h1Regex, '');

        const contentHtml = marked.parse(markdown);
        
        // This expects to be placed in tutorials/category/ folder, so relative paths use ../../
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title} | ${category} | MJ Tech Hub</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../../css/themes.css">
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/responsive.css">
    <script src="../../js/theme.js"></script>
    <script src="../../js/main.js" defer></script>
</head>
<body>
    <!-- Header -->
    <header>
        <div class="container nav-container">
            <!-- Logo -->
            <a href="../../index.html" class="brand-logo" aria-label="MJ Tech Hub Home">
                <img src="../../assets/brand/mj-tech-hub-header.png" alt="MJ Tech Hub" class="site-logo">
            </a>
            
            <!-- Navigation -->
            <nav style="flex-grow: 1; display: flex; align-items: center; justify-content: center;">
                <ul class="nav-links" id="nav-links">
                    <li><a href="../../index.html" class="nav-link" data-page="index.html">Home</a></li>
                    <li><a href="../../topics.html" class="nav-link" data-page="topics.html">Topics</a></li>
                    <li><a href="../../commands.html" class="nav-link" data-page="commands.html">Commands</a></li>
                    <li><a href="../../quiz.html" class="nav-link" data-page="quiz.html">Quiz</a></li>
                    <li><a href="../../resources.html" class="nav-link" data-page="resources.html">Resources</a></li>
                    <li><a href="../../about.html" class="nav-link" data-page="about.html">About</a></li>
                </ul>
            </nav>
            
            <!-- Search & Actions -->
            <div class="nav-actions" style="display: flex; align-items: center; gap: 1rem;">
                <div class="header-search">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Search tutorials, topics, commands..." aria-label="Search">
                </div>
                <button id="mobile-menu-btn" class="mobile-menu-btn" aria-label="Toggle navigation menu" aria-expanded="false">
                    <i class="fas fa-bars"></i>
                </button>
            </div>
        </div>
    </header>

    <main class="lesson-container py-4">
        <!-- Breadcrumb -->
        <div style="margin-bottom: 1rem; font-size: 0.85rem; color: var(--text-muted);">
            <a href="../../index.html" style="color: var(--text-secondary);">Home</a> &gt; 
            <a href="../../topics.html" style="color: var(--text-secondary);">Topics</a> &gt; 
            <a href="../../${category.toLowerCase()}.html" style="color: var(--text-secondary);">${category}</a> &gt; 
            <span style="color: var(--brand-primary);">${title}</span>
        </div>
        
        <span style="font-size: 0.8rem; background: var(--bg-tertiary); color: var(--brand-primary); padding: 4px 10px; border-radius: 4px; font-weight: 600; text-transform: uppercase;">${category}</span>
        <h1 style="font-size: 2.5rem; margin: 1rem 0; color: var(--text-primary);">${title}</h1>
        
        <div style="display: flex; gap: 1rem; margin-bottom: 2rem; font-size: 0.85rem; color: var(--text-muted);">
            <span><i class="fas fa-signal" style="color: var(--success);"></i> ${level}</span>
            <span><i class="fas fa-clock"></i> ${time}</span>
        </div>
        
        <div class="content lesson-content" style="font-size: 1.05rem; line-height: 1.7; color: var(--text-secondary);">
${contentHtml}
        </div>
        
        <!-- Navigation -->
        <div style="display: flex; justify-content: space-between; border-top: 1px solid var(--border-color); padding-top: 1.5rem; margin-top: 3rem;">
            <!-- Add PREV/NEXT links manually after export -->
            <span></span>
            <span></span>
        </div>
    </main>

    <!-- Footer -->
    <footer>
        <div class="container footer-content">
            <div>
                &copy; 2026 MJ Tech Hub. All rights reserved.
            </div>
            
            <ul class="footer-links">
                <li><a href="../../legal/privacy.html">Privacy Policy</a></li>
                <li><a href="../../legal/terms.html">Terms of Use</a></li>
                <li><a href="../../legal/disclaimer.html">Disclaimer</a></li>
                <li><a href="../../about.html">Contact</a></li>
            </ul>
            
            <div>
                Made with <i class="fas fa-heart" style="color: var(--danger);"></i> by The MJ Tech Hub
            </div>
        </div>
    </footer>
</body>
</html>`;
    }

    // Export Functions
    function downloadFile(filename, content, type) {
        const blob = new Blob([content], { type: type });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    btnExportHtml.addEventListener('click', () => {
        const html = generateFinalHTML();
        const filename = (idInput.value || 'untitled') + '.html';
        downloadFile(filename, html, 'text/html');
    });

    btnExportJson.addEventListener('click', () => {
        let draftObj = {};
        try {
            draftObj = JSON.parse(localStorage.getItem('mjTechHub_lessonDraft') || '{}');
        } catch (e) {}
        
        // Ensure dates are set for export
        const today = new Date().toISOString().split('T')[0];
        if (!draftObj.publishedAt) draftObj.publishedAt = today;
        draftObj.updatedAt = today;
        
        // Also update the global state so subsequent saves preserve it
        window.mjTechHub_publishedAt = draftObj.publishedAt;
        saveDraft();

        const draftStr = JSON.stringify(draftObj, null, 4);
        const filename = (idInput.value || 'untitled') + '.json';
        downloadFile(filename, draftStr, 'application/json');
    });

    btnExportZip.addEventListener('click', async () => {
        if (typeof JSZip === 'undefined') {
            alert("JSZip library not loaded yet. Please try again.");
            return;
        }
        
        const zip = new JSZip();
        const baseName = idInput.value || 'untitled';
        
        let draftObj = {};
        try {
            draftObj = JSON.parse(localStorage.getItem('mjTechHub_lessonDraft') || '{}');
        } catch (e) {}
        
        const today = new Date().toISOString().split('T')[0];
        if (!draftObj.publishedAt) draftObj.publishedAt = today;
        draftObj.updatedAt = today;
        
        window.mjTechHub_publishedAt = draftObj.publishedAt;
        saveDraft();

        const draftStr = JSON.stringify(draftObj, null, 4);

        zip.file(baseName + '.html', generateFinalHTML());
        zip.file(baseName + '.json', draftStr);
        
        try {
            const content = await zip.generateAsync({ type: "blob" });
            const url = URL.createObjectURL(content);
            const a = document.createElement('a');
            a.href = url;
            a.download = baseName + '_bundle.zip';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (e) {
            console.error("Failed to generate ZIP", e);
            alert("Failed to generate ZIP file.");
        }
    });

    // Initialize
    loadDraft();
});
