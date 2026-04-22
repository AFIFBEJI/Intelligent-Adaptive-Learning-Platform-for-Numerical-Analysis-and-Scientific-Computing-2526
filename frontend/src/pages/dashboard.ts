// ============================================================
// Dashboard — Cards + Animated Progress (English)
// ============================================================

import { api, Etudiant, LearningPath } from '../api'
import { createNavbar } from '../components/navbar'
import { applyTilt } from '../components/tilt'

export function DashboardPage(): HTMLElement {
  const container = document.createElement('div')
  const userStr = localStorage.getItem('user')
  const user: Etudiant | null = userStr ? JSON.parse(userStr) : null
  const token = localStorage.getItem('token')
  if (token) api.setToken(token)

  container.appendChild(createNavbar(user?.nom_complet))

  const main = document.createElement('div')
  main.innerHTML = `
    <style>
      @keyframes slideUp { from{opacity:0;transform:translateY(25px)} to{opacity:1;transform:translateY(0)} }
      @keyframes glowPulse { 0%,100%{opacity:0.6} 50%{opacity:1} }
      @keyframes pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.05)} }
      @keyframes shimmer { 0%{background-position:-200% 0} 100%{background-position:200% 0} }

      .dashboard { max-width:1200px;margin:0 auto;padding:2rem;position:relative;z-index:1; }

      .welcome-bar {
        display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;
        gap:1rem;margin-bottom:2rem;animation:slideUp 0.5s ease;
      }
      .welcome-title { font-size:1.7rem;font-weight:800;color:#f1f5f9; }
      .welcome-title span {
        background:linear-gradient(135deg,#38bdf8,#818cf8);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
      }
      .welcome-sub { color:#64748b;margin-top:0.2rem;font-size:0.9rem; }
      .niveau-pill {
        padding:0.4rem 1.2rem;border-radius:50px;font-size:0.8rem;font-weight:700;
        background:linear-gradient(135deg,rgba(14,165,233,0.15),rgba(99,102,241,0.15));
        border:1px solid rgba(56,189,248,0.3);color:#38bdf8;animation:glowPulse 3s infinite;
      }

      .stats-grid {
        display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
        gap:1rem;margin-bottom:2rem;animation:slideUp 0.6s 0.1s ease both;
      }
      .stat-card {
        background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
        border-radius:18px;padding:1.5rem;display:flex;align-items:center;gap:1rem;
        backdrop-filter:blur(20px);transition:all 0.3s;cursor:default;
        position:relative;overflow:hidden;
      }
      .stat-card::before { content:'';position:absolute;inset:0;background:linear-gradient(135deg,transparent,rgba(255,255,255,0.02));border-radius:inherit; }
      .stat-icon { width:52px;height:52px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0; }
      .si-blue { background:rgba(14,165,233,0.15);border:1px solid rgba(14,165,233,0.3); }
      .si-green { background:rgba(52,211,153,0.15);border:1px solid rgba(52,211,153,0.3); }
      .si-orange { background:rgba(251,146,60,0.15);border:1px solid rgba(251,146,60,0.3); }
      .si-purple { background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.3); }

      .stat-info { flex:1;min-width:0; }
      .stat-number {
        font-size:2rem;font-weight:900;line-height:1;
        background:linear-gradient(135deg,#f1f5f9,#94a3b8);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
      }
      .stat-label { color:#64748b;font-size:0.78rem;margin-top:0.3rem;font-weight:600;letter-spacing:0.04em; }

      .ring-container { position:relative;width:80px;height:80px;flex-shrink:0; }
      .ring-svg { transform:rotate(-90deg); }
      .ring-bg { fill:none;stroke:rgba(255,255,255,0.05);stroke-width:6; }
      .ring-fill { fill:none;stroke-width:6;stroke-linecap:round;transition:stroke-dashoffset 1.5s ease; }
      .ring-text { position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:0.9rem;font-weight:800;color:#f1f5f9; }

      .main-grid { display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;animation:slideUp 0.7s 0.2s ease both; }
      @media(max-width:768px){ .main-grid{grid-template-columns:1fr;} }

      .panel {
        background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
        border-radius:20px;padding:1.5rem;backdrop-filter:blur(20px);
      }
      .panel-title {
        font-size:0.85rem;font-weight:700;color:#94a3b8;
        letter-spacing:0.08em;margin-bottom:1.25rem;display:flex;align-items:center;gap:0.5rem;
      }
      .panel-title::before { content:'';flex:1;max-width:30px;height:2px;background:currentColor;opacity:0.4; }

      .concept-row {
        display:flex;align-items:center;gap:0.75rem;
        padding:0.75rem 0;border-bottom:1px solid rgba(255,255,255,0.04);transition:all 0.2s;
      }
      .concept-row:last-child { border-bottom:none; }
      .concept-row:hover { transform:translateX(4px); }
      .concept-name { color:#e2e8f0;font-size:0.88rem;font-weight:500;flex:1;min-width:0; }
      .concept-bar-wrap { width:90px;height:5px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;flex-shrink:0; }
      .concept-bar { height:100%;border-radius:3px;transition:width 1.2s ease; }
      .bar-orange { background:linear-gradient(90deg,#f97316,#ef4444); }
      .concept-pct { font-size:0.75rem;font-weight:700;min-width:32px;text-align:right; }

      .rec-card {
        display:flex;align-items:center;gap:0.75rem;
        padding:0.85rem;border-radius:12px;
        background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
        margin-bottom:0.6rem;transition:all 0.2s;cursor:default;
      }
      .rec-card:hover { border-color:rgba(56,189,248,0.3);background:rgba(56,189,248,0.05);transform:translateX(4px); }
      .rec-dot { width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,#38bdf8,#818cf8);flex-shrink:0;animation:pulse 2s infinite; }
      .rec-name { color:#e2e8f0;font-size:0.87rem;font-weight:500;flex:1; }
      .rec-badge { font-size:0.7rem;padding:0.2rem 0.6rem;border-radius:20px;font-weight:700;background:rgba(52,211,153,0.15);color:#34d399;border:1px solid rgba(52,211,153,0.2); }

      .skeleton {
        background:linear-gradient(90deg,rgba(255,255,255,0.05) 25%,rgba(255,255,255,0.1) 50%,rgba(255,255,255,0.05) 75%);
        background-size:200% 100%;animation:shimmer 1.5s infinite;border-radius:8px;
      }
      .sk-row { height:40px;margin-bottom:0.6rem; }
      .sk-title { height:16px;width:40%;margin-bottom:1rem; }
      .empty-state { text-align:center;padding:2rem;color:#475569; }
      .empty-icon { font-size:2.5rem;margin-bottom:0.5rem; }
    </style>

    <div class="dashboard">
      <div class="welcome-bar">
        <div>
          <div class="welcome-title">Hello, <span>${user?.nom_complet?.split(' ')[0] || 'Student'}</span> 👋</div>
          <div class="welcome-sub">Your adaptive path through numerical analysis</div>
        </div>
        <div class="niveau-pill">⚡ ${user?.niveau_actuel || 'Intermediate'}</div>
      </div>

      <div class="stats-grid" id="stats-grid">
        ${['📚','✅','🔥','⭐'].map((ic,i) => `
          <div class="stat-card">
            <div class="stat-icon si-${['blue','green','orange','purple'][i]}">${ic}</div>
            <div class="stat-info">
              <div class="stat-number skeleton" style="height:2rem;width:60px;border-radius:6px"></div>
              <div class="stat-label skeleton" style="height:10px;width:80px;margin-top:6px;border-radius:4px"></div>
            </div>
          </div>
        `).join('')}
      </div>

      <div class="main-grid">
        <div class="panel">
          <div class="panel-title">🔁 Needs Improvement</div>
          <div id="improve-list">
            <div class="skeleton sk-title"></div>
            ${[1,2,3].map(_=>`<div class="skeleton sk-row"></div>`).join('')}
          </div>
        </div>
        <div class="panel">
          <div class="panel-title">⭐ Recommended Next</div>
          <div id="recommend-list">
            <div class="skeleton sk-title"></div>
            ${[1,2,3].map(_=>`<div class="skeleton sk-row"></div>`).join('')}
          </div>
        </div>
      </div>
    </div>
  `

  container.appendChild(main)

  if (user) {
    api.getLearningPath(user.id).then((path: LearningPath) => {
      const { total_concepts, mastered, in_progress } = path.overall_progress
      const toDiscover = total_concepts - mastered - in_progress
      const masteryPct = Math.round((mastered / total_concepts) * 100) || 0

      const statsGrid = main.querySelector('#stats-grid')!
      const statsData = [
        { icon:'📚', cls:'si-blue', num: total_concepts, label:'TOTAL CONCEPTS' },
        { icon:'✅', cls:'si-green', num: mastered, label:'MASTERED (≥70%)' },
        { icon:'🔥', cls:'si-orange', num: in_progress, label:'IN PROGRESS' },
        { icon:'⭐', cls:'si-purple', num: toDiscover, label:'TO DISCOVER' },
      ]
      statsGrid.innerHTML = statsData.map(s => `
        <div class="stat-card" data-tilt>
          <div class="stat-icon ${s.cls}">${s.icon}</div>
          <div class="stat-info">
            <div class="stat-number" data-target="${s.num}">0</div>
            <div class="stat-label">${s.label}</div>
          </div>
          <div class="ring-container">
            <svg class="ring-svg" width="80" height="80" viewBox="0 0 80 80">
              <circle class="ring-bg" cx="40" cy="40" r="32"/>
              <circle class="ring-fill" cx="40" cy="40" r="32"
                stroke="${['#38bdf8','#34d399','#f97316','#a78bfa'][statsData.indexOf(s)]}"
                stroke-dasharray="201"
                stroke-dashoffset="${201 - (201 * Math.min(s.num / Math.max(total_concepts,1), 1))}"/>
            </svg>
            <div class="ring-text">${masteryPct}%</div>
          </div>
        </div>
      `).join('')

      statsGrid.querySelectorAll('[data-target]').forEach(el => {
        const target = parseInt((el as HTMLElement).dataset.target || '0')
        let current = 0
        const step = Math.max(1, target / 30)
        const iv = setInterval(() => {
          current = Math.min(current + step, target)
          el.textContent = Math.round(current).toString()
          if (current >= target) clearInterval(iv)
        }, 40)
      })

      setTimeout(() => {
        statsGrid.querySelectorAll('[data-tilt]').forEach(el => applyTilt(el as HTMLElement, 8))
      }, 100)

      const improveList = main.querySelector('#improve-list')!
      if (path.concepts_to_improve.length === 0) {
        improveList.innerHTML = `<div class="empty-state"><div class="empty-icon">🎉</div><p>No concepts lagging behind!</p></div>`
      } else {
        improveList.innerHTML = path.concepts_to_improve.map(c => `
          <div class="concept-row">
            <div class="concept-name">${c.name}</div>
            <div class="concept-bar-wrap"><div class="concept-bar bar-orange" style="width:${c.mastery}%"></div></div>
            <div class="concept-pct" style="color:#f97316">${c.mastery.toFixed(0)}%</div>
          </div>
        `).join('')
      }

      const recommendList = main.querySelector('#recommend-list')!
      if (path.next_recommended.length === 0) {
        recommendList.innerHTML = `<div class="empty-state"><div class="empty-icon">📖</div><p>Complete current concepts first</p></div>`
      } else {
        recommendList.innerHTML = path.next_recommended.map(c => `
          <div class="rec-card">
            <div class="rec-dot"></div>
            <div class="rec-name">${c.name}</div>
            <span class="rec-badge">Ready</span>
          </div>
        `).join('')
      }
    }).catch(() => {
      main.querySelector('#improve-list')!.innerHTML = `<div class="empty-state"><div class="empty-icon">🎯</div><p>Take your first quiz to see your progress</p></div>`
      main.querySelector('#recommend-list')!.innerHTML = `<div class="empty-state"><div class="empty-icon">🧠</div><p>Data not available</p></div>`
    })
  }

  return container
}
