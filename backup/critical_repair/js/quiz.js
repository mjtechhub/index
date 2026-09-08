/**
 * MJ Tech Hub - Quiz Logic
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
            allQuizzes = data;
            renderQuizList();
        })
        .catch(err => {
            console.error(err);
            if(selectorScreen) selectorScreen.innerHTML = '<p class="text-center" style="color:red;">Error loading quizzes.</p>';
        });
        
    function renderQuizList() {
        if (!selectorScreen) return;
        selectorScreen.innerHTML = '';
        
        allQuizzes.forEach(quiz => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h3 class="card-title">${quiz.title}</h3>
                <p class="card-text">${quiz.description}</p>
                <button class="btn btn-primary start-quiz-btn" data-id="${quiz.id}" style="width: 100%;">Start Quiz</button>
            `;
            selectorScreen.appendChild(card);
        });
        
        document.querySelectorAll('.start-quiz-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const quizId = e.target.getAttribute('data-id');
                startQuiz(quizId);
            });
        });
    }
    
    function startQuiz(quizId) {
        currentQuiz = allQuizzes.find(q => q.id === quizId);
        currentQuestionIndex = 0;
        userAnswers = new Array(currentQuiz.questions.length).fill(null);
        
        selectorScreen.style.display = 'none';
        resultScreen.classList.remove('active');
        quizApp.classList.add('active');
        
        document.getElementById('quiz-title').textContent = currentQuiz.title;
        renderQuestion();
    }
    
    function renderQuestion() {
        const questionData = currentQuiz.questions[currentQuestionIndex];
        const container = document.getElementById('question-container');
        const tracker = document.getElementById('question-tracker');
        const fill = document.getElementById('progress-fill');
        
        tracker.textContent = `Question ${currentQuestionIndex + 1} of ${currentQuiz.questions.length}`;
        fill.style.width = `${((currentQuestionIndex + 1) / currentQuiz.questions.length) * 100}%`;
        
        let html = `<div class="question-text">${questionData.question}</div><div class="options-list">`;
        
        questionData.options.forEach((opt, index) => {
            const isSelected = userAnswers[currentQuestionIndex] === index;
            html += `
                <label class="option-label ${isSelected ? 'selected' : ''}">
                    <input type="radio" name="option" value="${index}" class="option-input" ${isSelected ? 'checked' : ''}>
                    ${opt}
                </label>
            `;
        });
        html += `</div>`;
        container.innerHTML = html;
        
        // Hide feedback container on new question until selected
        document.getElementById('feedback-container').style.display = 'none';
        
        // Add listeners
        document.querySelectorAll('input[name="option"]').forEach(input => {
            input.addEventListener('change', (e) => {
                document.querySelectorAll('.option-label').forEach(l => l.classList.remove('selected'));
                e.target.closest('.option-label').classList.add('selected');
                userAnswers[currentQuestionIndex] = parseInt(e.target.value);
            });
        });
        
        updateControls();
    }
    
    function updateControls() {
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');
        const btnSubmit = document.getElementById('btn-submit');
        
        btnPrev.disabled = currentQuestionIndex === 0;
        
        if (currentQuestionIndex === currentQuiz.questions.length - 1) {
            btnNext.style.display = 'none';
            btnSubmit.style.display = 'block';
        } else {
            btnNext.style.display = 'block';
            btnSubmit.style.display = 'none';
        }
    }
    
    // Controls Event Listeners
    if(document.getElementById('btn-next')) {
        document.getElementById('btn-next').addEventListener('click', () => {
            if(currentQuestionIndex < currentQuiz.questions.length - 1) {
                currentQuestionIndex++;
                renderQuestion();
            }
        });
    }
    
    if(document.getElementById('btn-prev')) {
        document.getElementById('btn-prev').addEventListener('click', () => {
            if(currentQuestionIndex > 0) {
                currentQuestionIndex--;
                renderQuestion();
            }
        });
    }
    
    if(document.getElementById('btn-submit')) {
        document.getElementById('btn-submit').addEventListener('click', showResults);
    }
    
    if(backBtn) {
        backBtn.addEventListener('click', () => {
            quizApp.classList.remove('active');
            selectorScreen.style.display = 'grid';
        });
    }
    
    function showResults() {
        quizApp.classList.remove('active');
        resultScreen.classList.add('active');
        
        let score = 0;
        const reviewContainer = document.getElementById('answers-review');
        reviewContainer.innerHTML = '<h3>Review</h3>';
        
        currentQuiz.questions.forEach((q, i) => {
            const userAnswer = userAnswers[i];
            const isCorrect = userAnswer === q.correctIndex;
            if (isCorrect) score++;
            
            const reviewItem = document.createElement('div');
            reviewItem.className = `feedback ${isCorrect ? 'correct' : 'incorrect'}`;
            reviewItem.innerHTML = `
                <p><strong>Q: ${q.question}</strong></p>
                <p>Your answer: ${userAnswer !== null ? q.options[userAnswer] : 'Not answered'}</p>
                ${!isCorrect ? `<p>Correct answer: ${q.options[q.correctIndex]}</p>` : ''}
                <p style="font-size:0.875rem; margin-top:0.5rem;">${q.explanation}</p>
            `;
            reviewContainer.appendChild(reviewItem);
        });
        
        document.getElementById('score-circle').textContent = `${score} / ${currentQuiz.questions.length}`;
        const pct = (score / currentQuiz.questions.length) * 100;
        let msg = "";
        if (pct === 100) msg = "Perfect Score!";
        else if (pct >= 70) msg = "Great Job!";
        else msg = "Keep Learning!";
        
        document.getElementById('score-message').textContent = msg;
    }
    
    if(document.getElementById('btn-restart')) {
        document.getElementById('btn-restart').addEventListener('click', () => {
            startQuiz(currentQuiz.id);
        });
    }
    
    if(document.getElementById('btn-all-quizzes')) {
        document.getElementById('btn-all-quizzes').addEventListener('click', () => {
            resultScreen.classList.remove('active');
            selectorScreen.style.display = 'grid';
        });
    }
});
