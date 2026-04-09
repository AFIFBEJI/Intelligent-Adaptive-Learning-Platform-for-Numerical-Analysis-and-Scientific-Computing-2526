// ============================================================
// Quiz Page — Interactive 3D Quiz with Glassmorphism
// ============================================================

import { api, Quiz, QuizResult } from '../api'
import { createNavbar } from '../components/navbar'

export function QuizPage(): HTMLElement {
  const container = document.createElement('div')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null
  const token = localStorage.getItem('token')
  if (token) api.setToken(token)

  container.appendChild(createNavbar(user?.nom_complet))

  const main = document.createElement('div')
  main.innerHTML = `
    <style>
      @keyframes slideUp { from{opacity:0;transform:translateY(25px)} to{opacity:1;transform:translateY(0)} }
      @keyframes fadeIn { from{opacity:0} to{opacity:1} }
      @keyframes shimmer { 0%{background-position:-200% 0} 100%{background-position:200% 0} }
      @keyframes popIn { from{opacity:0;transform:scale(0.8)} to{opacity:1;transform:scale(1)} }
      @keyframes glowPulse { 0%,100%{box-shadow:0 0 20px rgba(56,189,248,0.2)} 50%{box-shadow:0 0 40px rgba(56,189,248,0.4)} }
      @keyframes correctAnim { 0%{transform:scale(1)} 50%{transform:scale(1.04)} 100%{transform:scale(1)} }
      @keyframes timerTick { from{stroke-dashoffset:0} to{stroke-dashoffset:283} }

      .quiz-page { max-width:900px;margin:0 auto;padding:2rem;position:relative;z-index:1; }

      /* Header */
      .page-header { margin-bottom:2rem;animation:slideUp 0.5s ease; }
      .page-title {
        font-size:2rem;font-weight:900;
        background:linear-gradient(135deg,#f1f5f9 0%,#38bdf8 50%,#818cf8 100%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
        margin-bottom:0.4rem;
      }
      .page-sub { color:#64748b;font-size:0.9rem; }

      /* Quiz list grid */
      .quiz-grid {
        display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
        gap:1.25rem;animation:slideUp 0.5s 0.1s ease both;
      }

      .quiz-card {
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.07);
        border-radius:20px;padding:1.5rem;
        backdrop-filter:blur(20px);cursor:pointer;
        transition:all 0.3s;position:relative;overflow:hidden;
      }
      .quiz-card::before {
        content:'';position:absolute;inset:0;border-radius:20px;
        background:linear-gradient(135deg,transparent,rgba(56,189,248,0.03));
        opacity:0;transition:opacity 0.3s;
      }
      .quiz-card:hover { border-color:rgba(56,189,248,0.3);transform:translateY(-4px);
        box-shadow:0 15px 40px rgba(0,0,0,0.3); }
      .quiz-card:hover::before { opacity:1; }

      .quiz-module-badge {
        display:inline-block;font-size:0.68rem;font-weight:700;
        padding:0.25rem 0.7rem;border-radius:20px;
        letter-spacing:0.06em;margin-bottom:0.75rem;
        background:rgba(56,189,248,0.1);color:#38bdf8;border:1px solid rgba(56,189,248,0.25);
      }
      .quiz-title { font-weight:700;color:#f1f5f9;font-size:1.05rem;margin-bottom:0.6rem;line-height:1.3; }
      .quiz-meta {
        display:flex;gap:0.75rem;flex-wrap:wrap;margin-top:0.75rem;
        padding-top:0.75rem;border-top:1px solid rgba(255,255,255,0.05);
      }
      .quiz-meta-item { font-size:0.75rem;color:#64748b;display:flex;align-items:center;gap:0.3rem; }

      .diff-badge {
        display:inline-block;font-size:0.7rem;font-weight:700;
        padding:0.2rem 0.6rem;border-radius:8px;
      }
      .diff-facile { background:rgba(52,211,153,0.15);color:#34d399;border:1px solid rgba(52,211,153,0.3); }
      .diff-moyen { background:rgba(251,146,60,0.15);color:#fb923c;border:1px solid rgba(251,146,60,0.3); }
      .diff-difficile { background:rgba(239,68,68,0.15);color:#f87171;border:1px solid rgba(239,68,68,0.3); }

      /* Active quiz */
      .quiz-active { display:none;animation:fadeIn 0.4s ease; }
      .quiz-active.visible { display:block; }

      .quiz-header-bar {
        display:flex;align-items:center;justify-content:space-between;
        margin-bottom:2rem;flex-wrap:wrap;gap:1rem;
      }
      .quiz-title-active { font-size:1.25rem;font-weight:800;color:#f1f5f9; }
      .progress-info { display:flex;align-items:center;gap:1rem; }
      .q-counter { font-size:0.85rem;color:#64748b;font-weight:600; }
      .progress-bar-wrap { width:120px;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;overflow:hidden; }
      .progress-bar-fill { height:100%;border-radius:2px;background:linear-gradient(90deg,#38bdf8,#818cf8);transition:width 0.5s ease; }

      /* Question card */
      .question-card {
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:24px;padding:2rem;
        backdrop-filter:blur(20px);
        margin-bottom:1.5rem;
        animation:popIn 0.4s cubic-bezier(0.4,0,0.2,1);
      }
      .question-number { font-size:0.75rem;font-weight:700;color:#64748b;letter-spacing:0.08em;margin-bottom:0.75rem; }
      .question-text { font-size:1.05rem;color:#e2e8f0;font-weight:600;line-height:1.6;margin-bottom:1.5rem; }

      /* Options */
      .options-grid { display:flex;flex-direction:column;gap:0.7rem; }
      .option-btn {
        width:100%;text-align:left;padding:1rem 1.25rem;
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:14px;color:#94a3b8;
        font-size:0.9rem;font-weight:500;cursor:pointer;
        transition:all 0.25s;position:relative;overflow:hidden;
      }
      .option-btn::before {
        content:'';position:absolute;left:0;top:0;bottom:0;width:3px;
        background:linear-gradient(135deg,#38bdf8,#818cf8);
        opacity:0;transition:opacity 0.25s;border-radius:3px 0 0 3px;
      }
      .option-btn:hover:not(:disabled) {
        border-color:rgba(56,189,248,0.35);
        background:rgba(56,189,248,0.06);color:#e2e8f0;
      }
      .option-btn:hover:not(:disabled)::before { opacity:1; }
      .option-btn.selected { border-color:rgba(56,189,248,0.5);background:rgba(56,189,248,0.1);color:#38bdf8; }
      .option-btn.selected::before { opacity:1; }
      .option-btn.correct { border-color:rgba(52,211,153,0.6);background:rgba(52,211,153,0.1);color:#34d399;animation:correctAnim 0.3s ease; }
      .option-btn.wrong { border-color:rgba(239,68,68,0.5);background:rgba(239,68,68,0.08);color:#f87171; }
      .option-btn:disabled { cursor:default; }

      /* Nav buttons */
      .quiz-nav { display:flex;justify-content:space-between;align-items:center;gap:1rem; }
      .btn-next {
        padding:0.8rem 2rem;
        background:linear-gradient(135deg,#0ea5e9,#6366f1);
        color:white;border:none;border-radius:12px;
        font-size:0.9rem;font-weight:700;cursor:pointer;
        transition:all 0.3s;
        box-shadow:0 4px 20px rgba(14,165,233,0.3);
      }
      .btn-next:hover:not(:disabled) { transform:translateY(-2px);box-shadow:0 8px 30px rgba(14,165,233,0.5); }
      .btn-next:disabled { opacity:0.4;cursor:not-allowed; }
      .btn-quit {
        padding:0.8rem 1.5rem;background:transparent;
        border:1px solid rgba(255,255,255,0.1);
        color:#64748b;border-radius:12px;font-size:0.85rem;cursor:pointer;transition:all 0.25s;
      }
      .btn-quit:hover { border-color:rgba(239,68,68,0.3);color:#f87171; }

      /* Result screen */
      .result-screen {
        display:none;text-align:center;padding:3rem 2rem;
        background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
        border-radius:24px;backdrop-filter:blur(20px);
        animation:popIn 0.5s cubic-bezier(0.4,0,0.2,1);
      }
      .result-screen.visible { display:block; }
      .result-emoji { font-size:4rem;margin-bottom:1rem;display:block; }
      .result-score {
        font-size:4rem;font-weight:900;
        background:linear-gradient(135deg,#38bdf8,#818cf8);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
        margin-bottom:0.5rem;
      }
      .result-label { color:#64748b;font-size:0.9rem;margin-bottom:2rem; }
      .result-actions { display:flex;gap:1rem;justify-content:center;flex-wrap:wrap; }
      .btn-retry {
        padding:0.85rem 2rem;
        background:linear-gradient(135deg,#0ea5e9,#6366f1);
        color:white;border:none;border-radius:12px;font-size:0.9rem;font-weight:700;cursor:pointer;
        transition:all 0.3s;box-shadow:0 4px 20px rgba(14,165,233,0.3);
      }
      .btn-retry:hover { transform:translateY(-2px);box-shadow:0 8px 30px rgba(14,165,233,0.5); }
      .btn-back {
        padding:0.85rem 2rem;background:transparent;
        border:1px solid rgba(255,255,255,0.12);color:#94a3b8;
        border-radius:12px;font-size:0.9rem;cursor:pointer;transition:all 0.25s;
      }
      .btn-back:hover { border-color:rgba(56,189,248,0.3);color:#38bdf8; }

      /* Skeleton */
      .sk-card { height:160px;border-radius:20px;
        background:linear-gradient(90deg,rgba(255,255,255,0.04) 25%,rgba(255,255,255,0.08) 50%,rgba(255,255,255,0.04) 75%);
        background-size:200% 100%;animation:shimmer 1.5s infinite; }
      .no-results { text-align:center;padding:3rem;color:#475569; }
    </style>

    <div class="quiz-page">
      <div class="page-header" id="quiz-list-header">
        <h1 class="page-title">📝 Quiz Adaptatifs</h1>
        <p class="page-sub">Testez vos connaissances et améliorez votre maîtrise</p>
      </div>

      <!-- Quiz list -->
      <div class="quiz-grid" id="quiz-grid">
        ${[1,2,3,4,5,6].map(_=>`<div class="sk-card"></div>`).join('')}
      </div>

      <!-- Active quiz -->
      <div class="quiz-active" id="quiz-active">
        <div class="quiz-header-bar">
          <div class="quiz-title-active" id="active-quiz-title">Quiz</div>
          <div class="progress-info">
            <span class="q-counter" id="q-counter">Question 1/5</span>
            <div class="progress-bar-wrap">
              <div class="progress-bar-fill" id="progress-fill" style="width:0%"></div>
            </div>
          </div>
        </div>
        <div class="question-card" id="question-card">
          <div class="question-number" id="q-number">QUESTION 1</div>
          <div class="question-text" id="q-text"></div>
          <div class="options-grid" id="options-grid"></div>
        </div>
        <div class="quiz-nav">
          <button class="btn-quit" id="btn-quit">✕ Quitter</button>
          <button class="btn-next" id="btn-next" disabled>Suivant →</button>
        </div>
      </div>

      <!-- Result -->
      <div class="result-screen" id="result-screen">
        <span class="result-emoji" id="result-emoji">🎉</span>
        <div class="result-score" id="result-score">0%</div>
        <div class="result-label" id="result-label">Score final</div>
        <div class="result-actions">
          <button class="btn-retry" id="btn-retry">🔄 Recommencer</button>
          <button class="btn-back" id="btn-back-result">← Retour aux quiz</button>
        </div>
      </div>
    </div>
  `

  container.appendChild(main)

  // State
  let currentQuiz: Quiz | null = null
  let currentQ = 0
  let answers: number[] = []
  let selectedAnswer: number | null = null

  const quizGrid = main.querySelector('#quiz-grid')!
  const quizActive = main.querySelector('#quiz-active')!
  const quizListHeader = main.querySelector('#quiz-list-header')!
  const resultScreen = main.querySelector('#result-screen')!
  const btnNext = main.querySelector('#btn-next') as HTMLButtonElement
  const btnQuit = main.querySelector('#btn-quit')!

  const showList = () => {
    quizGrid.style.display = 'grid'
    quizListHeader.style.display = 'block'
    quizActive.classList.remove('visible')
    resultScreen.classList.remove('visible')
    currentQuiz = null
    currentQ = 0
    answers = []
  }

  const renderQuestion = () => {
    if (!currentQuiz) return
    const q = currentQuiz.questions[currentQ]
    const total = currentQuiz.questions.length

    ;(main.querySelector('#q-counter') as HTMLElement).textContent = `Question ${currentQ + 1}/${total}`
    ;(main.querySelector('#progress-fill') as HTMLElement).style.width = `${((currentQ) / total) * 100}%`
    ;(main.querySelector('#q-number') as HTMLElement).textContent = `QUESTION ${currentQ + 1}`
    ;(main.querySelector('#q-text') as HTMLElement).textContent = q.question

    const optionsGrid = main.querySelector('#options-grid')!
    optionsGrid.innerHTML = q.options.map((opt: string, i: number) => `
      <button class="option-btn" data-idx="${i}">${String.fromCharCode(65 + i)}. ${opt}</button>
    `).join('')

    optionsGrid.querySelectorAll('.option-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        optionsGrid.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'))
        btn.classList.add('selected')
        selectedAnswer = parseInt((btn as HTMLElement).dataset.idx || '0')
        btnNext.disabled = false
      })
    })

    btnNext.disabled = true
    selectedAnswer = null
  }

  const startQuiz = (quiz: Quiz) => {
    currentQuiz = quiz
    currentQ = 0
    answers = []
    selectedAnswer = null
    quizGrid.style.display = 'none'
    quizListHeader.style.display = 'none'
    quizActive.classList.add('visible')
    resultScreen.classList.remove('visible')
    ;(main.querySelector('#active-quiz-title') as HTMLElement).textContent = quiz.titre
    renderQuestion()
  }

  btnNext.addEventListener('click', () => {
    if (!currentQuiz || selectedAnswer === null) return
    const q = currentQuiz.questions[currentQ]
    answers.push(selectedAnswer)

    // Show correct/wrong
    const optionsGrid = main.querySelector('#options-grid')!
    optionsGrid.querySelectorAll('.option-btn').forEach(btn => {
      const idx = parseInt((btn as HTMLElement).dataset.idx || '0')
      ;(btn as HTMLButtonElement).disabled = true
      if (idx === q.correct_index) btn.classList.add('correct')
      else if (idx === selectedAnswer) btn.classList.add('wrong')
    })
    btnNext.disabled = true

    setTimeout(() => {
      currentQ++
      if (currentQ < currentQuiz!.questions.length) {
        renderQuestion()
      } else {
        // Show result
        const correct = answers.filter((a, i) => a === currentQuiz!.questions[i].correct_index).length
        const score = Math.round((correct / currentQuiz!.questions.length) * 100)

        quizActive.classList.remove('visible')
        resultScreen.classList.add('visible')
        ;(main.querySelector('#result-score') as HTMLElement).textContent = `${score}%`
        ;(main.querySelector('#result-emoji') as HTMLElement).textContent = score >= 80 ? '🏆' : score >= 60 ? '🎯' : score >= 40 ? '📚' : '💪'
        ;(main.querySelector('#result-label') as HTMLElement).textContent =
          `${correct}/${currentQuiz!.questions.length} correctes — ${score >= 70 ? 'Concept maîtrisé !' : 'Continuez à pratiquer'}`

        // Submit to backend
        if (user) {
          api.submitQuiz(currentQuiz!.id, {
            etudiant_id: user.id,
            score,
            reponses: answers,
            temps_reponse: 0,
          }).catch(() => {})
        }
      }
    }, 800)
  })

  btnQuit.addEventListener('click', showList)
  main.querySelector('#btn-back-result')?.addEventListener('click', showList)
  main.querySelector('#btn-retry')?.addEventListener('click', () => {
    if (currentQuiz) startQuiz(currentQuiz)
  })

  // Load quiz list
  api.getQuizList().then((quizzes: Quiz[]) => {
    if (quizzes.length === 0) {
      quizGrid.innerHTML = '<div class="no-results" style="grid-column:1/-1;"><div style="font-size:2.5rem;margin-bottom:1rem">📭</div><p>Aucun quiz disponible pour le moment.</p></div>'
      return
    }
    quizGrid.innerHTML = quizzes.map(q => {
      const diffClass = q.difficulte === 'facile' ? 'diff-facile' : q.difficulte === 'difficile' ? 'diff-difficile' : 'diff-moyen'
      return `
        <div class="quiz-card" data-id="${q.id}">
          <div class="quiz-module-badge">${q.module || 'Module'}</div>
          <div class="quiz-title">${q.titre}</div>
          <div class="quiz-meta">
            <span class="quiz-meta-item">❓ ${q.questions?.length || 0} questions</span>
            <span class="diff-badge ${diffClass}">${q.difficulte || 'moyen'}</span>
          </div>
        </div>
      `
    }).join('')

    quizGrid.querySelectorAll('.quiz-card').forEach(card => {
      card.addEventListener('click', () => {
        const id = parseInt((card as HTMLElement).dataset.id || '0')
        const quiz = quizzes.find(q => q.id === id)
        if (quiz) startQuiz(quiz)
      })
    })
  }).catch(() => {
    quizGrid.innerHTML = `
      <div class="no-results" style="grid-column:1/-1;">
        <div style="font-size:2.5rem;margin-bottom:1rem">🔌</div>
        <p>Backend non connecté. Démarrez uvicorn et rechargez.</p>
      </div>
    `
  })

  return container
}
