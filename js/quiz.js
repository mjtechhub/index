/**
 * MJ Tech Hub - Quiz Module (js/quiz.js)
 * Interactive learning engine with domain taxonomy, difficulty badges, accessible controls, and review analysis.
 */

document.addEventListener('DOMContentLoaded', () => {
    const selectorScreen = document.getElementById('quiz-selector');
    const quizApp = document.getElementById('quiz-app');
    const resultScreen = document.getElementById('result-screen');
    const backBtn = document.getElementById('back-to-quizzes');
    
    let allQuizzes = [];
    let currentQuiz = null;
    let currentQuestionIndex = 0;
    let userAnswers = [];
    
    // Load quizzes data
    fetch('./data/quizzes.json')
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch quizzes');
            return response.json();
        })
        .then(data => {
            allQuizzes = Array.isArray(data) ? data : [];
            renderQuizList();
            
            const params = new URLSearchParams(window.location.search);
            const quizParam = params.get('quiz');
            if (quizParam && allQuizzes.some(q => q.id === quizParam)) {
                startQuiz(quizParam);
            }
        })
        .catch(err => {
            console.error('Error loading quizzes:', err);
            if (selectorScreen) {
                selectorScreen.innerHTML = '<p class="text-center text-danger" style="color:var(--danger); grid-column: 1 / -1;">Failed to load practice quizzes. Please try again later.</p>';
            }
        });
        
    function renderQuizList() {
        if (!selectorScreen) return;
        selectorScreen.innerHTML = '';
        
        allQuizzes.forEach(quiz => {
            const card = document.createElement('div');
            card.className = 'card quiz-card';
            card.style.display = 'flex';
            card.style.flexDirection = 'column';
            card.style.height = '100%';
            
            const qCount = Array.isArray(quiz.questions) ? quiz.questions.length : 0;
            const category = quiz.category || 'General';
            
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                    <span class="meta-pill meta-pill-brand" style="font-size: 0.75rem;">${escapeHtml(category)}</span>
                    <span class="meta-pill" style="font-size: 0.75rem;">
                        <i class="fa-solid fa-circle-question" aria-hidden="true" style="margin-right: 0.35rem;"></i>${qCount} Questions
                    </span>
                </div>
                <h3 class="card-title" style="margin-bottom: 0.75rem; font-size: 1.25rem;">${escapeHtml(quiz.title)}</h3>
                <p class="card-text" style="color: var(--text-secondary); flex-grow: 1; margin-bottom: 1.5rem; line-height: 1.6; font-size: 0.95rem;">
                    ${escapeHtml(quiz.description)}
                </p>
                <button class="btn btn-primary start-quiz-btn" data-id="${escapeHtml(quiz.id)}" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 0.5rem;" aria-label="Start ${escapeHtml(quiz.title)} Quiz">
                    <i class="fa-solid fa-play" aria-hidden="true"></i> Start Quiz
                </button>
            `;
            selectorScreen.appendChild(card);
        });
        
        document.querySelectorAll('.start-quiz-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const target = e.currentTarget;
                const quizId = target.getAttribute('data-id');
                startQuiz(quizId);
            });
        });
    }
    
    function startQuiz(quizId) {
        currentQuiz = allQuizzes.find(q => q.id === quizId);
        if (!currentQuiz) return;
        currentQuestionIndex = 0;
        userAnswers = new Array(currentQuiz.questions.length).fill(null);
        
        selectorScreen.style.display = 'none';
        resultScreen.classList.remove('active');
        quizApp.classList.add('active');
        
        const titleEl = document.getElementById('quiz-title');
        if (titleEl) titleEl.textContent = currentQuiz.title;
        renderQuestion();
        
        // Scroll smoothly to top of quiz app
        quizApp.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    function renderQuestion() {
        const questionData = currentQuiz.questions[currentQuestionIndex];
        const container = document.getElementById('question-container');
        const tracker = document.getElementById('question-tracker');
        const fill = document.getElementById('progress-fill');
        
        tracker.textContent = `Question ${currentQuestionIndex + 1} of ${currentQuiz.questions.length}`;
        fill.style.width = `${((currentQuestionIndex + 1) / currentQuiz.questions.length) * 100}%`;
        fill.setAttribute('aria-valuenow', currentQuestionIndex + 1);
        fill.setAttribute('aria-valuemax', currentQuiz.questions.length);
        
        const diff = questionData.difficulty || 'Intermediate';
        const diffColor = diff === 'Beginner' ? 'var(--success)' : diff === 'Advanced' ? 'var(--danger)' : 'var(--warning)';
        
        let html = `
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem;">
                <span class="meta-pill" style="border-color: ${diffColor}; color: ${diffColor}; font-size: 0.75rem; font-weight: 600;">
                    ${escapeHtml(diff)}
                </span>
                <span style="font-size: 0.85rem; color: var(--text-muted);">${escapeHtml(questionData.category || currentQuiz.category || '')}</span>
            </div>
            <div class="question-text" style="font-size: 1.15rem; font-weight: 600; line-height: 1.5; margin-bottom: 1.5rem; color: var(--text-primary);">
                ${escapeHtml(questionData.question)}
            </div>
            <div class="options-list" role="radiogroup" aria-label="Question options">
        `;
        
        questionData.options.forEach((opt, index) => {
            const isSelected = userAnswers[currentQuestionIndex] === index;
            html += `
                <label class="option-label ${isSelected ? 'selected' : ''}" style="min-height: 48px; display: flex; align-items: center; gap: 0.85rem; padding: 0.85rem 1rem;">
                    <input type="radio" name="option" value="${index}" class="option-input" ${isSelected ? 'checked' : ''} aria-label="${escapeHtml(opt)}" style="width: 18px; height: 18px; accent-color: var(--brand-primary); cursor: pointer;">
                    <span style="font-size: 0.95rem; line-height: 1.4;">${escapeHtml(opt)}</span>
                </label>
            `;
        });
        html += `</div>`;
        container.innerHTML = html;
        
        // Hide feedback container on new question
        const feedbackContainer = document.getElementById('feedback-container');
        if (feedbackContainer) feedbackContainer.style.display = 'none';
        
        // Add option listeners
        document.querySelectorAll('input[name="option"]').forEach(input => {
            input.addEventListener('change', (e) => {
                document.querySelectorAll('.option-label').forEach(l => l.classList.remove('selected'));
                e.target.closest('.option-label').classList.add('selected');
                userAnswers[currentQuestionIndex] = parseInt(e.target.value, 10);
            });
        });
        
        updateControls();
    }
    
    function updateControls() {
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');
        const btnSubmit = document.getElementById('btn-submit');
        
        if (btnPrev) btnPrev.disabled = currentQuestionIndex === 0;
        
        if (currentQuestionIndex === currentQuiz.questions.length - 1) {
            if (btnNext) btnNext.style.display = 'none';
            if (btnSubmit) btnSubmit.style.display = 'inline-flex';
        } else {
            if (btnNext) btnNext.style.display = 'inline-flex';
            if (btnSubmit) btnSubmit.style.display = 'none';
        }
    }
    
    // Controls Event Listeners
    const btnNext = document.getElementById('btn-next');
    if (btnNext) {
        btnNext.addEventListener('click', () => {
            if (currentQuestionIndex < currentQuiz.questions.length - 1) {
                currentQuestionIndex++;
                renderQuestion();
            }
        });
    }
    
    const btnPrev = document.getElementById('btn-prev');
    if (btnPrev) {
        btnPrev.addEventListener('click', () => {
            if (currentQuestionIndex > 0) {
                currentQuestionIndex--;
                renderQuestion();
            }
        });
    }
    
    const btnSubmit = document.getElementById('btn-submit');
    if (btnSubmit) {
        btnSubmit.addEventListener('click', showResults);
    }
    
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            quizApp.classList.remove('active');
            selectorScreen.style.display = 'grid';
            selectorScreen.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }
    
    function showResults() {
        quizApp.classList.remove('active');
        resultScreen.classList.add('active');
        
        let score = 0;
        const reviewContainer = document.getElementById('answers-review');
        if (reviewContainer) {
            reviewContainer.innerHTML = '<h3 style="margin-bottom: 1.5rem; font-size: 1.3rem;">Detailed Answer Review</h3>';
        }
        
        currentQuiz.questions.forEach((q, i) => {
            const userAnswer = userAnswers[i];
            const isCorrect = userAnswer === q.correctIndex;
            if (isCorrect) score++;
            
            if (reviewContainer) {
                const reviewItem = document.createElement('div');
                reviewItem.className = `feedback ${isCorrect ? 'correct' : 'incorrect'}`;
                reviewItem.style.padding = '1.25rem';
                reviewItem.style.marginBottom = '1.25rem';
                reviewItem.setAttribute('tabindex', '0');
                reviewItem.setAttribute('aria-label', `Question ${i + 1}: ${isCorrect ? 'Correct' : 'Incorrect'}`);
                reviewItem.innerHTML = `
                    <p style="margin: 0 0 0.5rem 0; font-size: 1rem;">
                        <strong>Q${i + 1}: ${escapeHtml(q.question)}</strong>
                    </p>
                    <p style="margin: 0 0 0.25rem 0; font-size: 0.95rem; color: ${isCorrect ? 'var(--success)' : 'var(--danger)'};">
                        <strong>Your answer:</strong> ${userAnswer !== null && userAnswer !== undefined ? escapeHtml(q.options[userAnswer]) : '<em>Not answered</em>'}
                        <span style="margin-left: 0.5rem; font-weight: 600;">
                            ${isCorrect ? '<i class="fa-solid fa-check" aria-hidden="true"></i> [Correct]' : '<i class="fa-solid fa-xmark" aria-hidden="true"></i> [Incorrect]'}
                        </span>
                    </p>
                    ${!isCorrect ? `
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.95rem; color: var(--success);">
                            <strong>Correct answer:</strong> ${escapeHtml(q.options[q.correctIndex])}
                        </p>
                    ` : ''}
                    <p style="font-size: 0.9rem; margin-top: 0.5rem; margin-bottom: 0; line-height: 1.5; color: var(--text-secondary); background: var(--bg-primary); padding: 0.75rem; border-radius: 6px;">
                        <i class="fa-solid fa-lightbulb" aria-hidden="true" style="color: var(--warning); margin-right: 0.4rem;"></i>
                        ${escapeHtml(q.explanation)}
                    </p>
                `;
                reviewContainer.appendChild(reviewItem);
            }
        });
        
        const total = currentQuiz.questions.length;
        const scoreCircle = document.getElementById('score-circle');
        if (scoreCircle) scoreCircle.textContent = `${score} / ${total}`;
        
        const pct = Math.round((score / total) * 100);
        let msg = "";
        let perfClass = "";
        if (pct === 100) {
            msg = "Perfect Score! Strong Mastery (100%)";
            perfClass = "text-success";
        } else if (pct >= 80) {
            msg = "Great Job! Strong (80%+)";
            perfClass = "text-success";
        } else if (pct >= 60) {
            msg = "Good Performance! Solid Foundation (60%+)";
            perfClass = "text-primary";
        } else if (pct >= 40) {
            msg = "Developing Skills — Review Recommended";
            perfClass = "text-warning";
        } else {
            msg = "Needs Review — Revisit Learning Materials";
            perfClass = "text-danger";
        }
        
        const scoreMsg = document.getElementById('score-message');
        if (scoreMsg) {
            scoreMsg.textContent = `${msg} — ${pct}% Correct (${score} of ${total})`;
        }
        
        resultScreen.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    const btnRestart = document.getElementById('btn-restart');
    if (btnRestart) {
        btnRestart.addEventListener('click', () => {
            if (currentQuiz) startQuiz(currentQuiz.id);
        });
    }
    
    const btnAllQuizzes = document.getElementById('btn-all-quizzes');
    if (btnAllQuizzes) {
        btnAllQuizzes.addEventListener('click', () => {
            resultScreen.classList.remove('active');
            selectorScreen.style.display = 'grid';
            selectorScreen.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }
    
    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
