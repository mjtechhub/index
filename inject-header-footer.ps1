$headerHtml = @'
    <!-- Header -->
    <header>
        <div class="container nav-container">
            <!-- Logo -->
            <a href="ROOT_PATHindex.html" class="brand-logo" aria-label="MJ Tech Hub Home">
                <img src="ROOT_PATHassets/brand/mj-tech-hub-header.png" alt="MJ Tech Hub" class="site-logo">
            </a>
            
            <!-- Navigation -->
            <nav style="flex-grow: 1; display: flex; align-items: center; justify-content: center;">
                <ul class="nav-links" id="nav-links">
                    <li><a href="ROOT_PATHindex.html" class="nav-link" data-page="index.html">Home</a></li>
                    <li><a href="ROOT_PATHtopics.html" class="nav-link" data-page="topics.html">Topics</a></li>
                    <li><a href="ROOT_PATHcommands.html" class="nav-link" data-page="commands.html">Commands</a></li>
                    <li><a href="ROOT_PATHquiz.html" class="nav-link" data-page="quiz.html">Quiz</a></li>
                    <li><a href="ROOT_PATHresources.html" class="nav-link" data-page="resources.html">Resources</a></li>
                    <li><a href="ROOT_PATHabout.html" class="nav-link" data-page="about.html">About</a></li>
                </ul>
            </nav>
            
            <!-- Search & Actions -->
            <div class="nav-actions" style="display: flex; align-items: center; gap: 1rem;">
                <div class="header-search">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Search tutorials, topics, commands..." aria-label="Search">
                </div>
                
                <button id="theme-toggle" class="theme-toggle" aria-label="Toggle dark mode">
                    <i class="fas fa-sun"></i>
                </button>
                <button id="mobile-menu-btn" class="mobile-menu-btn" aria-label="Toggle navigation menu" aria-expanded="false">
                    <i class="fas fa-bars"></i>
                </button>
            </div>
        </div>
    </header>
'@

$footerHtml = @'
    <!-- Footer -->
    <footer>
        <div class="container footer-content">
            <div>
                &copy; 2026 MJ Tech Hub. All rights reserved.
            </div>
            
            <ul class="footer-links">
                <li><a href="ROOT_PATHlegal/privacy.html">Privacy Policy</a></li>
                <li><a href="ROOT_PATHlegal/terms.html">Terms of Use</a></li>
                <li><a href="ROOT_PATHlegal/disclaimer.html">Disclaimer</a></li>
                <li><a href="ROOT_PATHabout.html">Contact</a></li>
            </ul>
            
            <div>
                Made with <i class="fas fa-heart" style="color: var(--danger);"></i> by The MJ Tech Hub
            </div>
        </div>
    </footer>
'@

function Inject-Layout {
    param([string]$Path, [string]$RootPrefix)
    
    $files = Get-ChildItem -Path $Path -Filter *.html -File
    foreach ($f in $files) {
        $content = Get-Content $f.FullName -Raw
        
        $localHeader = $headerHtml -replace 'ROOT_PATH', $RootPrefix
        $localFooter = $footerHtml -replace 'ROOT_PATH', $RootPrefix
        
        if ($content -notmatch '<main') {
            # Wrap content in main if missing
            $content = $content -replace '(?s)(<body[^>]*>)(.*?)(</body>)', "`$1`n    <main class=`"container`">`n`$2`n    </main>`n`$3"
        }
        
        if ($content -match '(?s)(<body[^>]*>).*?(<main[^>]*>)') {
            $content = $content -replace '(?s)(<body[^>]*>).*?(<main[^>]*>)', "`$1`n$localHeader`n    `$2"
        }
        
        if ($content -match '(?s)(</main>).*?(</body>)') {
            $content = $content -replace '(?s)(</main>).*?(</body>)', "`$1`n$localFooter`n`$2"
        }
        
        Set-Content -Path $f.FullName -Value $content -NoNewline
    }
}

Inject-Layout -Path . -RootPrefix './'
Inject-Layout -Path ./legal -RootPrefix '../'

Write-Host "Injected header and footer globally."
