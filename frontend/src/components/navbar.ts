// ============================================================
// Navbar Component — Glassmorphism 3D
// ============================================================

export function createNavbar(userName?: string): HTMLElement {
  const nav = document.createElement('nav')
  nav.innerHTML = `
    <style>
      @keyframes navSlideDown { from{opacity:0;transform:translateY(-100%)} to{opacity:1;transform:translateY(0)} }
      @keyframes glowPulse { 0%,100%{opacity:0.5} 50%{opacity:1} }
      @keyframes shimmerBrand {
        0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}
      }

      .navbar {
        display:flex;align-items:center;justify-content:space-between;
        padding:0 2rem;height:64px;
        background:rgba(10,15,30,0.7);
        backdrop-filter:blur(20px) saturate(180%);
        -webkit-backdrop-filter:blur(20px) saturate(180%);
        border-bottom:1px solid rgba(56,189,248,0.12);
        position:sticky;top:0;z-index:1000;
        animation:navSlideDown 0.5s ease;
        box-shadow:0 4px 30px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
        transition:background 0.3s, box-shadow 0.3s;
      }
      .navbar.scrolled {
        background:rgba(7,10,20,0.9);
        box-shadow:0 4px 40px rgba(0,0,0,0.6), 0 0 0 1px rgba(56,189,248,0.08), inset 0 1px 0 rgba(255,255,255,0.04);
      }

      .navbar-brand {
        font-size:1.15rem;font-weight:900;text-decoration:none;
        display:flex;align-items:center;gap:0.6rem;
        position:relative;letter-spacing:-0.01em;
      }
      .brand-icon {
        width:34px;height:34px;border-radius:10px;
        background:linear-gradient(135deg,rgba(14,165,233,0.25),rgba(99,102,241,0.25));
        border:1px solid rgba(56,189,248,0.35);
        display:flex;align-items:center;justify-content:center;
        font-size:1rem;flex-shrink:0;
        box-shadow:0 0 15px rgba(56,189,248,0.15);
        transition:all 0.3s;
      }
      .navbar-brand:hover .brand-icon {
        background:linear-gradient(135deg,rgba(14,165,233,0.4),rgba(99,102,241,0.4));
        box-shadow:0 0 25px rgba(56,189,248,0.35);
        transform:rotate(-5deg) scale(1.05);
      }
      .brand-text {
        background:linear-gradient(135deg,#f1f5f9 0%,#38bdf8 50%,#818cf8 100%);
        background-size:200% 200%;
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
        animation:shimmerBrand 4s ease infinite;
      }
      .brand-text span { -webkit-text-fill-color:#64748b;font-weight:400; }

      .navbar-links { display:flex;gap:0.25rem;align-items:center; }

      .nav-link {
        position:relative;color:#64748b;text-decoration:none;
        font-size:0.85rem;font-weight:600;letter-spacing:0.02em;
        padding:0.45rem 0.9rem;border-radius:10px;
        transition:all 0.25s;
        overflow:hidden;
      }
      .nav-link::before {
        content:'';position:absolute;inset:0;border-radius:10px;
        background:linear-gradient(135deg,rgba(56,189,248,0.08),rgba(99,102,241,0.08));
        opacity:0;transition:opacity 0.25s;
      }
      .nav-link::after {
        content:'';position:absolute;bottom:4px;left:50%;transform:translateX(-50%);
        width:0;height:2px;border-radius:1px;
        background:linear-gradient(90deg,#38bdf8,#818cf8);
        transition:width 0.3s cubic-bezier(0.4,0,0.2,1);
      }
      .nav-link:hover { color:#e2e8f0; }
      .nav-link:hover::before { opacity:1; }
      .nav-link:hover::after { width:60%; }
      .nav-link.active { color:#38bdf8; }
      .nav-link.active::after { width:60%; }

      .nav-divider { width:1px;height:20px;background:rgba(255,255,255,0.08);margin:0 0.5rem; }

      .user-badge {
        display:flex;align-items:center;gap:0.5rem;
        padding:0.35rem 0.9rem 0.35rem 0.5rem;
        border-radius:50px;
        background:rgba(56,189,248,0.06);
        border:1px solid rgba(56,189,248,0.15);
        color:#94a3b8;font-size:0.8rem;font-weight:600;
        letter-spacing:0.02em;
      }
      .user-avatar {
        width:24px;height:24px;border-radius:50%;
        background:linear-gradient(135deg,#0ea5e9,#6366f1);
        display:flex;align-items:center;justify-content:center;
        font-size:0.65rem;font-weight:800;color:white;flex-shrink:0;
      }

      .btn-logout {
        display:flex;align-items:center;gap:0.4rem;
        padding:0.42rem 0.9rem;
        background:rgba(239,68,68,0.08);
        border:1px solid rgba(239,68,68,0.2);
        color:#f87171;border-radius:10px;
        font-size:0.8rem;font-weight:600;cursor:pointer;
        transition:all 0.25s;letter-spacing:0.02em;
        margin-left:0.25rem;
      }
      .btn-logout:hover {
        background:rgba(239,68,68,0.18);
        border-color:rgba(239,68,68,0.4);
        color:#fca5a5;
        transform:translateY(-1px);
        box-shadow:0 4px 15px rgba(239,68,68,0.2);
      }

      .nav-toggle {
        display:none;
        flex-direction:column;gap:5px;
        background:none;border:none;cursor:pointer;padding:0.5rem;
      }
      .nav-toggle span {
        display:block;width:22px;height:2px;border-radius:1px;
        background:#64748b;transition:all 0.3s;
      }

      @media(max-width:640px) {
        .nav-toggle { display:flex; }
        .navbar-links {
          display:none;position:absolute;top:64px;left:0;right:0;
          flex-direction:column;align-items:stretch;gap:0.25rem;
          background:rgba(7,10,20,0.95);backdrop-filter:blur(20px);
          padding:1rem;border-bottom:1px solid rgba(56,189,248,0.12);
        }
        .navbar-links.open { display:flex; }
        .nav-link { padding:0.65rem 1rem; }
        .nav-divider { width:100%;height:1px;margin:0.25rem 0; }
      }

      .navbar-glow {
        position:absolute;bottom:-1px;left:10%;right:10%;height:1px;
        background:linear-gradient(90deg,transparent,rgba(56,189,248,0.4),rgba(129,140,248,0.4),transparent);
        animation:glowPulse 3s infinite;
      }
    </style>

    <nav class="navbar" id="main-navbar">
      <a class="navbar-brand" href="/dashboard" data-link>
        <div class="brand-icon">&#129504;</div>
        <span class="brand-text">Adaptive<span>Learn</span></span>
      </a>

      <button class="nav-toggle" id="nav-toggle" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>

      <div class="navbar-links" id="navbar-links">
        ${userName ? `
          <a href="/dashboard" data-link class="nav-link" data-route="/dashboard">&#128202; Dashboard</a>
          <a href="/concepts" data-link class="nav-link" data-route="/concepts">&#129513; Concepts</a>
          <a href="/content" data-link class="nav-link" data-route="/content">&#128218; Content</a>
          <a href="/path" data-link class="nav-link" data-route="/path">&#128506; Path</a>
          <a href="/quiz" data-link class="nav-link" data-route="/quiz">&#128221; Quiz</a>
          <a href="/tutor" data-link class="nav-link" data-route="/tutor">&#129302; Tuteur IA</a>
          <div class="nav-divider"></div>
          <div class="user-badge">
            <div class="user-avatar">${userName.charAt(0).toUpperCase()}</div>
            ${userName.split(' ')[0]}
          </div>
          <button class="btn-logout" id="logout-btn">&#9211; D&#233;connexion</button>
        ` : `
          <a href="/login" data-link class="nav-link" data-route="/login">Connexion</a>
          <a href="/register" data-link class="nav-link" data-route="/register">
            <span style="background:linear-gradient(135deg,#38bdf8,#818cf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:700;">
              Commencer &#8594;
            </span>
          </a>
        `}
      </div>
      <div class="navbar-glow"></div>
    </nav>
  `

  const currentPath = window.location.pathname
  nav.querySelectorAll('.nav-link[data-route]').forEach(link => {
    if ((link as HTMLElement).dataset.route === currentPath) {
      link.classList.add('active')
    }
  })

  const navbar = nav.querySelector('#main-navbar') as HTMLElement
  const onScroll = () => {
    if (window.scrollY > 20) navbar?.classList.add('scrolled')
    else navbar?.classList.remove('scrolled')
  }
  window.addEventListener('scroll', onScroll, { passive: true })

  const toggle = nav.querySelector('#nav-toggle')
  const links = nav.querySelector('#navbar-links')
  toggle?.addEventListener('click', () => {
    links?.classList.toggle('open')
  })

  const logoutBtn = nav.querySelector('#logout-btn')
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    })
  }

  const observer = new MutationObserver(() => {
    if (!document.contains(nav)) {
      window.removeEventListener('scroll', onScroll)
      observer.disconnect()
    }
  })
  observer.observe(document.body, { childList: true, subtree: true })

  return nav
}
