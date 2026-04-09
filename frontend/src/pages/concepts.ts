// ============================================================
// Concepts Page — 3D Flip Cards + Filters
// ============================================================

import { api, Concept } from '../api'
import { createNavbar } from '../components/navbar'

export function ConceptsPage(): HTMLElement {
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

      .concepts-page { max-width:1200px;margin:0 auto;padding:2rem;position:relative;z-index:1; }

      .page-header { margin-bottom:2rem;animation:slideUp 0.5s ease; }
      .page-title {
        font-size:2rem;font-weight:900;
        background:linear-gradient(135deg,#f1f5f9 0%,#38bdf8 50%,#818cf8 100%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
        margin-bottom:0.4rem;
      }
      .page-sub { color:#64748b;font-size:0.9rem; }

      /* Filters */
      .filter-bar {
        display:flex;gap:0.6rem;flex-wrap:wrap;margin-bottom:2rem;
        animation:slideUp 0.5s 0.1s ease both;
      }
      .filter-chip {
        padding:0.45rem 1.1rem;border-radius:50px;
        border:1px solid rgba(255,255,255,0.08);
        background:transparent;color:#64748b;
        font-size:0.8rem;font-weight:600;cursor:pointer;
        transition:all 0.25s;letter-spacing:0.03em;
      }
      .filter-chip:hover { border-color:rgba(56,189,248,0.4);color:#94a3b8; }
      .filter-chip.active {
        background:linear-gradient(135deg,rgba(14,165,233,0.2),rgba(99,102,241,0.2));
        border-color:rgba(56,189,248,0.5);color:#38bdf8;
        box-shadow:0 0 15px rgba(56,189,248,0.15);
      }

      /* Cards grid */
      .cards-grid {
        display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
        gap:1.25rem;animation:slideUp 0.5s 0.2s ease both;
      }

      /* 3D Flip card */
      .flip-card { height:200px;perspective:1000px;cursor:pointer; }
      .flip-inner {
        position:relative;width:100%;height:100%;
        transform-style:preserve-3d;transition:transform 0.6s cubic-bezier(0.4,0,0.2,1);
      }
      .flip-card:hover .flip-inner { transform:rotateY(180deg); }

      .flip-front, .flip-back {
        position:absolute;inset:0;border-radius:18px;
        backface-visibility:hidden;-webkit-backface-visibility:hidden;
        padding:1.5rem;overflow:hidden;
      }

      .flip-front {
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.07);
        backdrop-filter:blur(20px);
        display:flex;flex-direction:column;justify-content:space-between;
        transition:border-color 0.3s;
      }
      .flip-card:hover .flip-front { border-color:rgba(56,189,248,0.2); }

      .flip-back {
        background:linear-gradient(135deg,rgba(14,165,233,0.1),rgba(99,102,241,0.15));
        border:1px solid rgba(56,189,248,0.25);
        transform:rotateY(180deg);
        display:flex;flex-direction:column;justify-content:center;
        backdrop-filter:blur(20px);
      }

      .card-category-badge {
        display:inline-block;font-size:0.68rem;font-weight:700;
        padding:0.25rem 0.7rem;border-radius:20px;
        letter-spacing:0.06em;margin-bottom:0.75rem;
      }
      .cat-interpolation { background:rgba(14,165,233,0.15);color:#38bdf8;border:1px solid rgba(14,165,233,0.3); }
      .cat-integration { background:rgba(52,211,153,0.15);color:#34d399;border:1px solid rgba(52,211,153,0.3); }
      .cat-ode { background:rgba(192,132,252,0.15);color:#c084fc;border:1px solid rgba(192,132,252,0.3); }
      .cat-default { background:rgba(148,163,184,0.15);color:#94a3b8;border:1px solid rgba(148,163,184,0.3); }

      .card-name { font-weight:700;color:#f1f5f9;font-size:1rem;line-height:1.3; }
      .card-level-bar { display:flex;gap:3px;margin-top:auto;padding-top:0.75rem; }
      .level-dot {
        height:4px;flex:1;border-radius:2px;
        background:rgba(255,255,255,0.08);
      }
      .level-dot.active { background:linear-gradient(90deg,#38bdf8,#818cf8); }

      .back-label { font-size:0.7rem;color:#64748b;font-weight:600;letter-spacing:0.06em;margin-bottom:0.5rem; }
      .back-desc { color:#94a3b8;font-size:0.82rem;line-height:1.6;margin-bottom:0.75rem; }
      .back-action {
        font-size:0.75rem;color:#38bdf8;font-weight:600;
        display:flex;align-items:center;gap:0.4rem;
      }

      /* Skeleton */
      .sk-card {
        height:200px;border-radius:18px;
        background:linear-gradient(90deg,rgba(255,255,255,0.04) 25%,rgba(255,255,255,0.08) 50%,rgba(255,255,255,0.04) 75%);
        background-size:200% 100%;animation:shimmer 1.5s infinite;
      }

      .no-results { grid-column:1/-1;text-align:center;padding:3rem;color:#475569; }
    </style>

    <div class="concepts-page">
      <div class="page-header">
        <h1 class="page-title">🧠 Graphe de Connaissances</h1>
        <p class="page-sub">Survolez une carte pour voir les détails — 15 concepts en 3 modules</p>
      </div>

      <div class="filter-bar" id="filter-bar">
        <button class="filter-chip active" data-cat="all">Tous les concepts</button>
      </div>

      <div class="cards-grid" id="cards-grid">
        ${[1,2,3,4,5,6].map(_=>`<div class="sk-card"></div>`).join('')}
      </div>
    </div>
  `

  container.appendChild(main)

  const getCatClass = (cat: string) => {
    if (cat?.toLowerCase().includes('interpolat')) return 'cat-interpolation'
    if (cat?.toLowerCase().includes('integrat') || cat?.toLowerCase().includes('intégrat')) return 'cat-integration'
    if (cat?.toLowerCase().includes('ode') || cat?.toLowerCase().includes('différentiel')) return 'cat-ode'
    return 'cat-default'
  }

  const getLevelDots = (level: string | number) => {
    const lvl = typeof level === 'number' ? level : parseInt(level) || 2
    return [1,2,3,4,5].map(i => `<div class="level-dot${i <= lvl ? ' active' : ''}"></div>`).join('')
  }

  api.getConcepts().then((concepts: Concept[]) => {
    const categories = ['all', ...new Set(concepts.map(c => c.category).filter(Boolean))]

    const filterBar = main.querySelector('#filter-bar')!
    filterBar.innerHTML = categories.map(cat => `
      <button class="filter-chip${cat === 'all' ? ' active' : ''}" data-cat="${cat}">
        ${cat === 'all' ? '✦ Tous les concepts' : cat}
      </button>
    `).join('')

    const renderCards = (filter: string) => {
      const filtered = filter === 'all' ? concepts : concepts.filter(c => c.category === filter)
      const grid = main.querySelector('#cards-grid')!

      if (filtered.length === 0) {
        grid.innerHTML = '<div class="no-results">Aucun concept trouvé</div>'
        return
      }

      grid.innerHTML = filtered.map(c => `
        <div class="flip-card">
          <div class="flip-inner">
            <div class="flip-front">
              <div>
                <span class="card-category-badge ${getCatClass(c.category)}">${c.category || 'Concept'}</span>
                <div class="card-name">${c.name}</div>
              </div>
              <div class="card-level-bar">${getLevelDots(c.level)}</div>
            </div>
            <div class="flip-back">
              <div class="back-label">DESCRIPTION</div>
              <div class="back-desc">${c.description || 'Concept fondamental d\'analyse numérique et calcul scientifique.'}</div>
              <div class="back-action">📖 Niveau ${c.level || '—'} <span>→</span></div>
            </div>
          </div>
        </div>
      `).join('')
    }

    renderCards('all')

    filterBar.addEventListener('click', (e) => {
      const chip = (e.target as HTMLElement).closest('.filter-chip') as HTMLElement | null
      if (!chip) return
      filterBar.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'))
      chip.classList.add('active')
      renderCards(chip.dataset.cat || 'all')
    })

  }).catch(() => {
    main.querySelector('#cards-grid')!.innerHTML = `
      <div class="no-results">
        <div style="font-size:2.5rem;margin-bottom:1rem">🔌</div>
        <p>Backend non connecté. Démarrez uvicorn et rechargez.</p>
      </div>
    `
  })

  return container
}
