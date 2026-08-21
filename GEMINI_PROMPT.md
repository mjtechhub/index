# MJ TECH HUB — FINAL FULL-SITE ASSET INTEGRATION + UI MATCH PROMPT

You are acting as CTO, Senior Frontend Architect, Senior UI/UX Designer, Senior Web Developer, Product Manager, Accessibility Specialist, Security Engineer, and Director of QA.

I have copied an asset pack into the ROOT of my existing MJ Tech Hub project. **Do not rename or regenerate these assets. Use the exact file names below.**

## Visual source of truth
- `reference/approved-homepage-light.png` = APPROVED TARGET DESIGN.
- `reference/current-homepage-before-fix.png` = older/current implementation reference.

The approved screenshot is the visual source of truth for the entire website design language. Do NOT create a new design direction.

## Required supplied assets
### Brand
- `assets/brand/mj-tech-hub-header.png` — use in the global header/navigation.
- `assets/brand/mj-tech-hub-icon.png` — use where a compact MJ mark is needed.
- `assets/brand/favicon-32.png`
- `assets/brand/favicon-64.png`
- `assets/brand/favicon-192.png`
- `assets/brand/favicon-512.png`

### Hero
- `assets/hero/mj-tech-hero.png` — **use this exact image directly as the homepage hero right-side visual.** Do not replace it with a white logo rectangle and do not regenerate a laptop illustration.

### Topic icons
- `assets/icons/networking.png`
- `assets/icons/windows.png`
- `assets/icons/linux.png`
- `assets/icons/servers.png`
- `assets/icons/cybersecurity.png`
- `assets/icons/cloud-ai.png`

### Social
- `assets/social/instagram.png`

# 1. FIRST AUDIT THE ENTIRE PROJECT
Before modifying code, inspect every HTML, CSS, JS and JSON file. Identify shared components, duplicate styles, conflicting responsive rules, incorrect relative paths, and page-to-page header inconsistencies. Preserve all working functionality.

# 2. GLOBAL HEADER — SAME ON EVERY PAGE
Every page must use the same desktop order:

`[MJ TECH HUB LOGO] Home Topics Commands Quiz Resources About [Search] [Theme]`

Use `assets/brand/mj-tech-hub-header.png` for the logo.

Requirements:
- light mode default
- header height approximately 72–80px
- logo visual height approximately 46–52px desktop, 36–42px mobile
- do not stretch/crop the logo
- active navigation style identical across all pages
- search must not disappear on secondary pages
- theme toggle must stay on far right
- responsive mobile layout: `[Logo] [Theme] [Menu]`

# 3. HOMEPAGE HERO — DO NOT RECREATE THE IMAGE
The homepage hero must be a two-column layout:

LEFT:
- `Learn IT. Solve Problems.`
- `Grow Your Skills.`
- `Practical tutorials, command guides and real-world solutions for Networking, Windows, Linux, Servers, Security, Cloud & more.`
- `Start Learning`
- `Explore Topics →`
- `⭐ New content added regularly`

RIGHT:
- `<img src="assets/hero/mj-tech-hero.png" ...>`

Use the supplied hero image directly. Do NOT display a separate large white MJ logo panel. The supplied hero already contains the approved laptop, branding and floating IT icons.

Suggested desktop CSS behavior:
```css
.hero-inner {
  display: grid;
  grid-template-columns: minmax(0, .92fr) minmax(520px, 1.08fr);
  gap: 40px;
  align-items: center;
}
.hero-visual img {
  width: 100%;
  max-width: 760px;
  height: auto;
  display: block;
  margin-inline: auto;
}
```

Target hero height: approximately 430–500px desktop. Remove excessive empty space.

# 4. HOMEPAGE TOPICS — SIX CARDS ON ONE DESKTOP ROW
Use the exact supplied topic icon files.

Cards:
1. Networking — `assets/icons/networking.png`
2. Windows — `assets/icons/windows.png`
3. Linux — `assets/icons/linux.png`
4. Servers — `assets/icons/servers.png`
5. Cybersecurity — `assets/icons/cybersecurity.png`
6. Cloud & AI — `assets/icons/cloud-ai.png`

At >= 1280px use a compact six-column grid:
```css
.topic-grid { grid-template-columns: repeat(6, minmax(0, 1fr)); }
```

Cards must have compact padding, consistent height, subtle border/shadow, category accent and `Explore →`. At 1440x900 the full header, hero, all six cards and beginning of next section should be visible.

# 5. LOWER HOMEPAGE LAYOUT
Immediately below the topic row, use the approved three-column structure:

LEFT — Latest Tutorials
- 5 CMD Commands Every IT Engineer Should Know
- Linux File Permissions Explained Simply
- What is VLAN? How Does It Work?

MIDDLE — Popular Commands
- `ipconfig /all`
- `ping`
- `tracert`
- `nslookup`
- `netstat -ano`
- `systeminfo`
- `tasklist`
- `chkdsk`
- `sfc /scannow`
- `gpupdate /force`
- `driverquery`

RIGHT — Test Your Knowledge
- `Practice with our quizzes`
- `Test your IT knowledge and track your progress.`
- `Start Quiz →`
- compact `Improve Every Day` card below

# 6. INSTAGRAM CTA
Use `assets/social/instagram.png` and one full-width banner near the bottom:

`Stay Updated!`
`Follow @themjtechhub on Instagram for daily IT tips, tutorials & updates.`
`Follow on Instagram →`

Do not duplicate large Instagram banners.

# 7. APPLY THE DESIGN TO EVERY SECTION/PAGE — NOT ONLY TOPICS
Audit and visually normalize ALL of these:
- Home
- Topics
- Networking
- Windows
- Linux
- Servers
- Cybersecurity
- Cloud & AI
- Commands
- Quiz
- Resources
- About
- Search
- Tutorial detail pages
- Privacy
- Terms
- Disclaimer
- Contact (if present)
- 404
- Header
- Footer
- Mobile navigation
- Light mode
- Dark mode

Every page must feel like the SAME application.

# 8. TOPICS PAGE
Dedicated Topics page can use a 3x2 desktop grid, but use the supplied six icon assets and the same card system, colors, radius, shadow, typography and header used on the homepage.

# 9. DESIGN TOKENS
Default light mode:
```css
--background: #FFFFFF;
--surface: #F8FAFC;
--surface-secondary: #F1F5F9;
--text-primary: #0F172A;
--text-secondary: #475569;
--primary: #2563EB;
--cyan: #06B6D4;
--orange: #F59E0B;
--border: #E2E8F0;
```

Use a consistent max-width around 1440px, centered. Suggested horizontal padding: 48px desktop, 24–32px tablet, 16–20px mobile.

# 10. TYPOGRAPHY
Use one modern sans-serif system globally (Inter/Manrope/system fallback). Keep heading, body, navigation and buttons consistent. Hero main heading should remain visually strong around 54–64px on desktop using responsive `clamp()`.

# 11. SEARCH / THEME / FUNCTIONALITY
Do not break:
- site-wide search
- light/dark theme
- mobile menu
- topic navigation
- commands/search/copy
- quiz JSON loading/scoring/restart
- resources/about/tutorial links
- Instagram link
- footer/legal links

Search must render user input safely; avoid unsafe `innerHTML` for user-controlled text.

# 12. QUIZ FETCH
The site is tested via HTTP at `http://localhost/mjtechhub/`, not `file://`.
Use repository-safe relative paths and validate `response.ok`. Ensure GitHub Pages compatibility.

# 13. RESPONSIVE TEST MATRIX
Test all major pages at:
320, 360, 375, 390, 414, 768, 1024, 1366, 1440, 1920px.

Desktop homepage: six topic cards in one row where width allows.
Tablet: 2–3 per row.
Mobile: one per row.
No horizontal scrolling.

# 14. GITHUB PAGES PATHS
Must work locally and at `https://username.github.io/repository-name/`.
No Windows drive paths, no `file://`, no localhost hardcoding in production code. Inspect relative asset depth carefully for subpages.

# 15. VISUAL REGRESSION
After implementation open `reference/approved-homepage-light.png` side-by-side with the live homepage. Compare:
- header/logo scale
- navigation spacing
- search/theme placement
- hero two-column proportions
- exact supplied hero image usage
- hero height/white space
- six-card topic row
- Latest Tutorials / Popular Commands / Quiz layout
- Instagram banner
- overall density and polish

Continue correcting obvious differences. Do not report PASS after only a single CSS edit.

# 16. QA — FULL SITE
Run functional, regression, negative, accessibility, responsive and security tests.
Require:
- 0 critical console errors
- no required asset 404s
- no JSON 404s
- no broken nav links
- no broken primary actions
- no severe mobile overflow
- no fake/unfinished visible features

Do not show Login, Bookmarks, fake learner counts, fake tutorial totals, certificates or progress tracking unless they genuinely work.

# 17. FINAL REPORT
Return:

`MJ TECH HUB — FINAL ASSET INTEGRATION & PRODUCTION QA REPORT`

Include:
- root causes found
- files modified
- assets integrated with exact paths
- Homepage PASS/FAIL
- every main page PASS/FAIL
- Header PASS/FAIL
- Footer PASS/FAIL
- Light Mode PASS/FAIL
- Dark Mode PASS/FAIL
- Search PASS/FAIL
- Commands PASS/FAIL
- Quiz PASS/FAIL
- Responsive PASS/FAIL
- Accessibility PASS/FAIL
- Security PASS/FAIL
- GitHub Pages PASS/FAIL
- Console PASS/FAIL
- Broken Assets PASS/FAIL
- Regression PASS/FAIL
- total tests / passed / failed / blocked (only tests actually executed)

Finish with exactly one:

`🟢 GO — PRODUCTION READY`

or

`🔴 NO-GO — FIXES REQUIRED`

# FINAL EXECUTION RULE
Do not answer with suggestions only. Inspect and modify the existing project directly. Use the supplied images instead of inventing replacements, especially `assets/hero/mj-tech-hero.png`. Preserve all working functionality while making the complete site visually consistent with `reference/approved-homepage-light.png`.
