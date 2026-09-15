/**
 * MJ Tech Hub - Guided Troubleshooting Labs Simulator
 * Data-driven educational incident diagnosis engine.
 * Supports realistic multi-step branching, evidence analysis, and systematic RCA.
 */

(function() {
    'use strict';

    let labsData = [];
    let currentLab = null;
    let currentStepIndex = 0;
    let userDecisionHistory = [];

    // Determine Base Path
    let basePath = '.';
    const scripts = document.getElementsByTagName('script');
    for (let script of scripts) {
        if (script.src && script.src.includes('js/labs.js')) {
            const srcAttr = script.getAttribute('src');
            basePath = srcAttr.substring(0, srcAttr.lastIndexOf('/js/labs.js'));
            if (basePath === '') basePath = '.';
            break;
        }
    }

    async function loadLabsData() {
        try {
            const res = await fetch(`${basePath}/data/troubleshooting-labs.json`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            labsData = await res.json();

            // Check if URL has a specific lab parameter
            const urlParams = new URLSearchParams(window.location.search);
            const labParam = urlParams.get('lab') || window.location.hash.replace('#', '');
            if (labParam) {
                const target = labsData.find(l => l.id === labParam);
                if (target) {
                    startLab(target);
                    return;
                }
            }
            renderLabSelector();
        } catch (err) {
            console.error('Failed to load troubleshooting-labs.json:', err);
            const container = document.getElementById('labs-content-container');
            if (container) {
                container.innerHTML = '<div class="alert alert-danger">Failed to load troubleshooting labs. Please refresh the page.</div>';
            }
        }
    }

    function renderLabSelector() {
        currentLab = null;
        userDecisionHistory = [];
        window.history.replaceState(null, '', window.location.pathname);

        const container = document.getElementById('labs-content-container');
        if (!container) return;

        container.innerHTML = `
            <div class="labs-selector-header">
                <span class="about-eyebrow">HANDS-ON SIMULATION</span>
                <h1 class="page-title">Guided Troubleshooting Labs</h1>
                <p class="page-subtitle">Practice systematic incident diagnosis across 6 core enterprise IT domains without introducing live system risk.</p>
            </div>
            <div class="labs-grid" id="labs-selector-grid"></div>
        `;

        const grid = document.getElementById('labs-selector-grid');

        labsData.forEach(lab => {
            const card = document.createElement('article');
            card.className = 'lab-card';
            card.id = lab.id;

            const header = document.createElement('div');
            header.className = 'lab-card-header';

            const catBadge = document.createElement('span');
            catBadge.className = `badge badge-${lab.category.toLowerCase().replace(/[^a-z]/g, '')}`;
            catBadge.textContent = lab.category;

            const metaSpan = document.createElement('span');
            metaSpan.className = 'lab-card-meta';
            metaSpan.innerHTML = `<i class="fa-solid fa-clock" aria-hidden="true"></i> ${lab.estimatedTime} &bull; ${lab.level}`;

            header.appendChild(catBadge);
            header.appendChild(metaSpan);

            const title = document.createElement('h3');
            title.className = 'lab-card-title';
            title.textContent = lab.title;

            const symptoms = document.createElement('p');
            symptoms.className = 'lab-card-symptoms';
            symptoms.innerHTML = `<strong>Symptoms:</strong> ${lab.symptoms}`;

            const footer = document.createElement('div');
            footer.className = 'lab-card-footer';

            const launchBtn = document.createElement('button');
            launchBtn.type = 'button';
            launchBtn.className = 'btn btn-primary lab-launch-btn';
            launchBtn.innerHTML = `<i class="fa-solid fa-play" aria-hidden="true"></i> Start Investigation`;
            launchBtn.setAttribute('aria-label', `Start investigation for ${lab.title}`);
            launchBtn.addEventListener('click', () => startLab(lab));

            footer.appendChild(launchBtn);

            card.appendChild(header);
            card.appendChild(title);
            card.appendChild(symptoms);
            card.appendChild(footer);

            grid.appendChild(card);
        });

        const liveAnnouncer = document.getElementById('labs-live-announcer');
        if (liveAnnouncer) liveAnnouncer.textContent = 'Showing 6 guided troubleshooting labs.';
    }

    function startLab(lab) {
        currentLab = lab;
        currentStepIndex = 0;
        userDecisionHistory = [];

        // Update URL parameter without reload
        const newUrl = `${window.location.pathname}?lab=${encodeURIComponent(lab.id)}`;
        window.history.pushState({ labId: lab.id }, '', newUrl);

        renderLabStep();
    }

    function renderLabStep() {
        const container = document.getElementById('labs-content-container');
        if (!container || !currentLab) return;

        const currentStep = currentLab.decisionPoints[currentStepIndex];
        const totalSteps = currentLab.decisionPoints.length;

        container.innerHTML = `
            <div class="lab-workspace">
                <nav class="lab-workspace-nav" aria-label="Lab Navigation">
                    <button type="button" id="lab-back-selector-btn" class="btn btn-secondary btn-sm">
                        <i class="fa-solid fa-arrow-left" aria-hidden="true"></i> Back to All Labs
                    </button>
                    <span class="badge badge-primary">${currentLab.category}</span>
                    <span class="lab-step-indicator">Investigation Step ${currentStep.stepNumber} of ${totalSteps}</span>
                </nav>

                <header class="lab-incident-banner">
                    <h1 class="lab-active-title">${currentLab.title}</h1>
                    <div class="lab-incident-brief">
                        <p><strong>Environment:</strong> ${currentLab.environment}</p>
                        <p><strong>Incident Scenario:</strong> ${currentLab.scenarioDescription}</p>
                    </div>
                </header>

                <div class="lab-step-card" id="lab-step-card">
                    <h2 class="lab-step-title">Step ${currentStep.stepNumber}: ${currentStep.title}</h2>
                    <p class="lab-step-desc">${currentStep.description}</p>

                    <div class="lab-evidence-box" aria-label="Lab Evidence Terminal">
                        <div class="lab-evidence-header">
                            <i class="fa-solid fa-terminal" aria-hidden="true"></i>
                            <span>Lab Evidence / Diagnostic Output</span>
                        </div>
                        <pre class="lab-evidence-content"><code>${escapeHtml(currentStep.evidence)}</code></pre>
                    </div>

                    <fieldset class="lab-options-fieldset">
                        <legend class="lab-options-legend">Choose Your Next Diagnostic or Remediation Action:</legend>
                        <div class="lab-options-list" id="lab-options-list"></div>
                    </fieldset>

                    <div id="lab-feedback-container" class="lab-feedback-container" style="display:none;" aria-live="polite"></div>

                    <div class="lab-step-actions" id="lab-step-actions" style="display:none;">
                        <button type="button" id="lab-next-step-btn" class="btn btn-primary">
                            Proceed <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('lab-back-selector-btn').addEventListener('click', renderLabSelector);

        const optionsList = document.getElementById('lab-options-list');
        const feedbackBox = document.getElementById('lab-feedback-container');
        const actionsBox = document.getElementById('lab-step-actions');
        const nextBtn = document.getElementById('lab-next-step-btn');

        currentStep.options.forEach((opt, idx) => {
            const label = document.createElement('label');
            label.className = 'lab-option-label';
            label.id = `opt-label-${idx}`;

            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = 'lab-choice';
            radio.value = opt.id;
            radio.className = 'lab-option-radio';

            const span = document.createElement('span');
            span.className = 'lab-option-text';
            span.textContent = opt.text;

            label.appendChild(radio);
            label.appendChild(span);

            radio.addEventListener('change', function() {
                // Disable other options
                const radios = document.querySelectorAll('input[name="lab-choice"]');
                radios.forEach(r => r.disabled = true);

                // Highlight selected
                label.classList.add('selected');

                // Determine feedback badge style
                let badgeClass = 'badge-primary';
                let iconClass = 'fa-check';
                let typeLabel = 'Optimal Next Step';

                if (opt.type === 'suboptimal') {
                    badgeClass = 'badge-secondary';
                    iconClass = 'fa-info-circle';
                    typeLabel = 'Valid but Less Efficient';
                } else if (opt.type === 'inefficient') {
                    badgeClass = 'badge-warning';
                    iconClass = 'fa-triangle-exclamation';
                    typeLabel = 'Inefficient / Unwarranted Action';
                } else if (opt.type === 'unsafe') {
                    badgeClass = 'badge-danger';
                    iconClass = 'fa-circle-xmark';
                    typeLabel = 'Unsafe / Dangerous Practice';
                }

                feedbackBox.className = `lab-feedback-container feedback-${opt.type}`;
                feedbackBox.innerHTML = `
                    <div class="feedback-badge-row">
                        <span class="badge ${badgeClass}"><i class="fa-solid ${iconClass}" aria-hidden="true"></i> ${typeLabel}</span>
                    </div>
                    <p class="feedback-text">${opt.feedback}</p>
                `;
                feedbackBox.style.display = 'block';

                userDecisionHistory.push({
                    stepNumber: currentStep.stepNumber,
                    stepTitle: currentStep.title,
                    chosenText: opt.text,
                    type: opt.type,
                    nextStepId: opt.nextStepId
                });

                actionsBox.style.display = 'flex';
                if (currentStepIndex === totalSteps - 1 || opt.nextStepId === 'diagnosis') {
                    nextBtn.innerHTML = `View Root Cause Analysis & Remediation <i class="fa-solid fa-flag-checkered" aria-hidden="true"></i>`;
                } else {
                    nextBtn.innerHTML = `Proceed to Next Step <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>`;
                }

                nextBtn.onclick = function() {
                    if (currentStepIndex === totalSteps - 1 || opt.nextStepId === 'diagnosis') {
                        renderFinalDiagnosis();
                    } else {
                        currentStepIndex++;
                        renderLabStep();
                    }
                };
            });

            optionsList.appendChild(label);
        });

        // Scroll smoothly to top of workspace
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function renderFinalDiagnosis() {
        const container = document.getElementById('labs-content-container');
        if (!container || !currentLab) return;

        const diag = currentLab.finalDiagnosis;

        let commandsHtml = '';
        if (Array.isArray(diag.relatedCommands) && diag.relatedCommands.length > 0) {
            commandsHtml = `
                <div class="diag-section">
                    <h3><i class="fa-solid fa-terminal" aria-hidden="true"></i> Recommended Diagnostic Commands</h3>
                    <div class="diag-links-grid">
                        ${diag.relatedCommands.map(cmdId => `<a href="commands.html#${cmdId}" class="diag-link-pill"><i class="fa-solid fa-code"></i> ${cmdId.replace('cmd-', '')}</a>`).join('')}
                    </div>
                </div>
            `;
        }

        let tutorialsHtml = '';
        if (Array.isArray(diag.relatedTutorials) && diag.relatedTutorials.length > 0) {
            tutorialsHtml = `
                <div class="diag-section">
                    <h3><i class="fa-solid fa-book-open" aria-hidden="true"></i> In-Depth Learning Tutorials</h3>
                    <div class="diag-links-grid">
                        ${diag.relatedTutorials.map(tutUrl => {
                            const slug = tutUrl.split('/').pop().replace('.html', '').replace(/-/g, ' ');
                            return `<a href="${tutUrl}" class="diag-link-pill"><i class="fa-solid fa-graduation-cap"></i> ${slug}</a>`;
                        }).join('')}
                    </div>
                </div>
            `;
        }

        container.innerHTML = `
            <div class="lab-workspace lab-results-view">
                <nav class="lab-workspace-nav" aria-label="Lab Navigation">
                    <button type="button" id="lab-restart-btn" class="btn btn-secondary btn-sm">
                        <i class="fa-solid fa-rotate-left" aria-hidden="true"></i> Investigate Another Incident
                    </button>
                    <span class="badge badge-success"><i class="fa-solid fa-check" aria-hidden="true"></i> Incident Resolved</span>
                </nav>

                <header class="lab-results-header">
                    <span class="about-eyebrow">ROOT CAUSE ANALYSIS (RCA)</span>
                    <h1 class="lab-results-title">${diag.title}</h1>
                </header>

                <div class="lab-rca-card">
                    <div class="rca-block">
                        <h2><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i> Root Cause Summary</h2>
                        <p class="rca-text">${diag.rootCause}</p>
                    </div>

                    <div class="rca-block">
                        <h2><i class="fa-solid fa-list-check" aria-hidden="true"></i> Evidence Collected</h2>
                        <pre class="rca-evidence-summary"><code>${escapeHtml(diag.evidenceSummary)}</code></pre>
                    </div>

                    <div class="rca-block">
                        <h2><i class="fa-solid fa-wrench" aria-hidden="true"></i> Recommended Remediation</h2>
                        <p class="rca-text">${diag.recommendedRemediation}</p>
                    </div>

                    <div class="rca-block">
                        <h2><i class="fa-solid fa-circle-check" aria-hidden="true"></i> Verification Steps</h2>
                        <p class="rca-text">${diag.verificationSteps}</p>
                    </div>

                    <div class="rca-block">
                        <h2><i class="fa-solid fa-shield-halved" aria-hidden="true"></i> Prevention & Hardening Measures</h2>
                        <p class="rca-text">${diag.preventionMeasures}</p>
                    </div>

                    ${commandsHtml}
                    ${tutorialsHtml}
                </div>

                <div class="lab-results-actions">
                    <button type="button" id="lab-return-selector-btn" class="btn btn-primary">
                        Return to All Troubleshooting Labs <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
                    </button>
                </div>
            </div>
        `;

        document.getElementById('lab-restart-btn').addEventListener('click', renderLabSelector);
        document.getElementById('lab-return-selector-btn').addEventListener('click', renderLabSelector);

        window.scrollTo({ top: 0, behavior: 'smooth' });

        const liveAnnouncer = document.getElementById('labs-live-announcer');
        if (liveAnnouncer) liveAnnouncer.textContent = `Lab completed: ${diag.title}. Root cause analysis and remediation instructions displayed.`;
    }

    function escapeHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Export to global namespace
    window.MJLabsEngine = {
        loadLabsData: loadLabsData,
        startLabById: (id) => {
            const target = labsData.find(l => l.id === id);
            if (target) startLab(target);
        }
    };

    document.addEventListener('DOMContentLoaded', loadLabsData);
})();
