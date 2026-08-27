const fs = require('fs');
const path = require('path');

function processDir(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            if (!fullPath.includes('node_modules') && !fullPath.includes('.git') && !fullPath.includes('tools')) {
                processDir(fullPath);
            }
        } else if (fullPath.endsWith('.html')) {
            injectScript(fullPath);
        }
    }
}

function injectScript(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Check if already injected
    if (content.includes('js/theme-init.js')) return;
    
    // Find the relative path from the themes.css link
    const cssMatch = content.match(/href="([^"]*)css\/themes\.css"/);
    if (!cssMatch) return;
    
    const relativePrefix = cssMatch[1]; // e.g., "../" or ""
    const scriptTag = `<script src="${relativePrefix}js/theme-init.js"></script>`;
    
    // Inject right before </head> or right after <head>
    if (content.includes('<head>')) {
        content = content.replace('<head>', `<head>\n    ${scriptTag}`);
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Injected into ${filePath}`);
    }
}

processDir(path.join(__dirname));
