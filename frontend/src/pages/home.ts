// ============================================================
// Home Page — Hero + Animations (English)
// ============================================================

import { createNavbar } from '../components/navbar'
import { createParticleBackground } from '../components/particles'
import { applyTilt } from '../components/tilt'

export function HomePage(): HTMLElement {
  const container = document.createElement('div')
  container.style.cssText = 'min-height:100vh;overflow:hidden;position:relative;'

  const stopParticles = createParticleBackground(container)
  container.appendChild(createNavbar())

  const main = document.createElement('div')
  main.innerHTML = `
    <style>
      @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-18px)} }
      @keyframes gradientShift {
        0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}
      }
      @keyframes glowPulse { 0%,100%{opacity:0.4;transform:scale(1)} 50%{opacity:0.8;transform:scale(1.05)} }
      @keyframes slideUp { from{opacity:0;transform:translateY(40px)} to{opacity:1;transform:translateY(0)} }
      @keyframes rotateSlow { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
      @keyframes counterGlow { 0%,100%{text-shadow:0 0 20px #38bdf8} 50%{text-shadow:0 0 40px #818cf8,0 0 60px #38bdf8} }

      .hero-section {
        position:relative;z-index:1;
        min-height:calc(100vh - 64px);
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        text-align:center;padding:2rem;
      }

      .hero-badge {
        display:inline-flex;align-items:center;gap:0.5rem;
        background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.3);
        color:#38bdf8;padding:0.5rem 1.2rem;border-radius:50px;
        font-size:0.8rem;font-weight:600;letter-spacing:0.05em;
        margin-bottom:2rem;animation:slideUp 0.6s ease forwards;
        backdrop-filter:blur(10px);
      }
      .badge-dot {
        width:8px;height:8px;border-radius:50%;background:#38bdf8;
        animation:glowPulse 2s infinite;
      }

      .hero-title {
        font-size:clamp(2.5rem, 6vw, 5rem);font-weight:900;line-height:1.1;
        max-width:900px;margin:0 auto 1.5rem;
        background:linear-gradient(135deg, #f1f5f9 0%, #38bdf8 40%, #818cf8 70%, #c084fc 100%);
        background-size:300% 300%;
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;
        animation:gradientShift 4s ease infinite, slideUp 0.8s 0.2s ease both;
      }

      .hero-sub {
        color:#94a3b8;font-size:1.15rem;max-width:600px;margin:0 auto 2.5rem;
        line-height:1.7;animation:slideUp 0.8s 0.4s ease both;
      }

      .hero-btns {
        display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;
        animation:slideUp 0.8s 0.6s ease both;margin-bottom:4rem;
      }

      .btn-3d-primary {
        position:relative;padding:0.9rem 2.5rem;
        background:linear-gradient(135deg, #0ea5e9, #6366f1);
        color:white;border:none;border-radius:12px;
        font-size:1rem;font-weight:700;cursor:pointer;
        text-decoration:none;display:inline-block;
        box-shadow:0 0 30px rgba(14,165,233,0.4), 0 8px 25px rgba(0,0,0,0.3);
        transition:all 0.3s;overflow:hidden;
      }
      .btn-3d-primary::before {
        content:'';position:absolute;inset:0;
        background:linear-gradient(135deg, rgba(255,255,255,0.2), transparent);
        border-radius:inherit;
      }
      .btn-3d-primary:hover {
        transform:translateY(-3px) scale(1.02);
        box-shadow:0 0 50px rgba(14,165,233,0.6), 0 15px 35px rgba(0,0,0,0.4);
      }

      .btn-3d-secondary {
        padding:0.9rem 2.5rem;
        background:rgba(255,255,255,0.05);
        color:#e2e8f0;border:1px solid rgba(255,255,255,0.15);
        border-radius:12px;font-size:1rem;font-weight:700;
        cursor:pointer;text-decoration:none;display:inline-block;
        backdrop-filter:blur(10px);transition:all 0.3s;
      }
      .btn-3d-secondary:hover {
        background:rgba(255,255,255,0.1);border-color:rgba(56,189,248,0.5);
        transform:translateY(-3px);box-shadow:0 10px 30px rgba(0,0,0,0.3);
      }

      .stats-row {
        display:flex;gap:2rem;flex-wrap:wrap;justify-content:center;
        margin-bottom:5rem;animation:slideUp 0.8s 0.8s ease both;
      }
      .stat-item { text-align:center; }
      .stat-num {
        font-size:2.5rem;font-weight:900;
        background:linear-gradient(135deg,#38bdf8,#818cf8);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;animation:counterGlow 3s infinite;
      }
      .stat-lbl { color:#64748b;font-size:0.8rem;margin-top:0.2rem;letter-spacing:0.05em; }
      .stat-divider { width:1px;background:rgba(255,255,255,0.08);align-self:stretch; }

      .features-grid {
        display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
        gap:1.5rem;max-width:1000px;width:100%;
        animation:slideUp 1s 1s ease both;
      }
      .feature-card {
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:20px;padding:1.75rem;
        backdrop-filter:blur(20px);
        cursor:default;transition:border-color 0.3s;
        transform-style:preserve-3d;
      }
      .feature-card:hover { border-color:rgba(56,189,248,0.3); }

      .feature-icon-wrap {
        width:52px;height:52px;border-radius:14px;
        display:flex;align-items:center;justify-content:center;
        font-size:1.5rem;margin-bottom:1rem;
      }
      .fi-blue { background:linear-gradient(135deg,rgba(14,165,233,0.2),rgba(99,102,241,0.2)); border:1px solid rgba(14,165,233,0.3); }
      .fi-purple { background:linear-gradient(135deg,rgba(139,92,246,0.2),rgba(192,132,252,0.2)); border:1px solid rgba(139,92,246,0.3); }
      .fi-green { background:linear-gradient(135deg,rgba(52,211,153,0.2),rgba(16,185,129,0.2)); border:1px solid rgba(52,211,153,0.3); }
      .fi-pink { background:linear-gradient(135deg,rgba(244,114,182,0.2),rgba(251,113,133,0.2)); border:1px solid rgba(244,114,182,0.3); }

      .feature-title { font-weight:700;color:#f1f5f9;margin-bottom:0.5rem;font-size:1rem; }
      .feature-desc { color:#64748b;font-size:0.82rem;line-height:1.6; }

      .orbit-container {
        position:absolute;right:5%;top:50%;transform:translateY(-50%);
        width:350px;height:350px;opacity:0.15;
        animation:rotateSlow 30s linear infinite;display:none;
      }
      @media(min-width:1200px){ .orbit-container{display:block;} }
      .orbit-ring { position:absolute;inset:0;border-radius:50%;border:1px solid rgba(56,189,248,0.6); }
      .orbit-ring:nth-child(2){inset:30px;border-color:rgba(129,140,248,0.5);}
      .orbit-ring:nth-child(3){inset:60px;border-color:rgba(192,132,252,0.4);}
      .orbit-dot { position:absolute;width:10px;height:10px;border-radius:50%;top:-5px;left:50%;transform:translateX(-50%); }
      .d1{background:#38bdf8;box-shadow:0 0 15px #38bdf8;}
      .d2{background:#818cf8;box-shadow:0 0 15px #818cf8;top:auto;bottom:-5px;}
      .d3{background:#c084fc;box-shadow:0 0 15px #c084fc;top:50%;left:-5px;}
    </style>

    <div class="orbit-container">
      <div class="orbit-ring"><div class="orbit-dot d1"></div><div class="orbit-dot d2"></div></div>
      <div class="orbit-ring"></div>
      <div class="orbit-ring"><div class="orbit-dot d3"></div></div>
    </div>

    <section class="hero-section">
      <div class="hero-badge"><div class="badge-dot"></div>PFE 2025-2026 · AI + Knowledge Graphs</div>

      <h1 class="hero-title">Adaptive Learning Platform for Numerical Analysis</h1>

      <p class="hero-sub">Personalized learning paths powered by a Neo4j knowledge graph, intelligent diagnostics, and targeted remediation to master scientific computing.</p>

      <div class="hero-btns">
        <a href="/register" data-link class="btn-3d-primary">🚀 Get Started Free</a>
        <a href="/login" data-link class="btn-3d-secondary">Sign In →</a>
      </div>

      <div class="stats-row">
        <div class="stat-item"><div class="stat-num">15</div><div class="stat-lbl">CONCEPTS</div></div>
        <div class="stat-divider"></div>
        <div class="stat-item"><div class="stat-num">3</div><div class="stat-lbl">MODULES</div></div>
        <div class="stat-divider"></div>
        <div class="stat-item"><div class="stat-num">100%</div><div class="stat-lbl">ADAPTIVE</div></div>
        <div class="stat-divider"></div>
        <div class="stat-item"><div class="stat-num">AI</div><div class="stat-lbl">POWERED</div></div>
      </div>

      <div class="features-grid" id="features-grid">
        ${[
          { icon:'🧠', cls:'fi-blue', t:'Neo4j Graph', d:'15 concepts organized with pedagogical dependencies: Interpolation, Integration, ODEs.' },
          { icon:'🎯', cls:'fi-purple', t:'Adaptive Path', d:'Intelligent algorithm recommends the next concept based on your mastery level.' },
          { icon:'📊', cls:'fi-green', t:'Real-Time Tracking', d:'Dashboard with 0-100% mastery per concept, updated after each quiz.' },
          { icon:'🔧', cls:'fi-pink', t:'Targeted Remediation', d:'Resources automatically suggested via REMEDIATES_TO relations in Neo4j.' },
        ].map(f => `
          <div class="feature-card" data-tilt>
            <div class="feature-icon-wrap ${f.cls}">${f.icon}</div>
            <div class="feature-title">${f.t}</div>
            <div class="feature-desc">${f.d}</div>
          </div>
        `).join('')}
      </div>
    </section>
  `

  container.appendChild(main)

  setTimeout(() => {
    main.querySelectorAll('[data-tilt]').forEach(el => applyTilt(el as HTMLElement, 10))
  }, 100)

  const counters = main.querySelectorAll('.stat-num')
  counters.forEach(el => {
    const text = el.textContent || ''
    if (!/^\d+/.test(text)) return
    const target = parseInt(text)
    let current = 0
    const step = target / 40
    const interval = setInterval(() => {
      current = Math.min(current + step, target)
      el.textContent = Math.round(current) + (text.includes('%') ? '%' : '')
      if (current >= target) clearInterval(interval)
    }, 30)
  })

  container.addEventListener('remove', stopParticles)
  const origRemove = container.remove.bind(container)
  container.remove = () => { stopParticles(); origRemove() }

  return container
}
