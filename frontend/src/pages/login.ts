// ============================================================
// Login Page — Glassmorphism 3D
// ============================================================

import { api } from '../api'
import { createNavbar } from '../components/navbar'
import { createParticleBackground } from '../components/particles'
import { router } from '../router'

export function LoginPage(): HTMLElement {
  const container = document.createElement('div')
  container.style.cssText = 'min-height:100vh;overflow:hidden;position:relative;'

  const stopParticles = createParticleBackground(container)
  container.appendChild(createNavbar())

  const main = document.createElement('div')
  main.innerHTML = `
    <style>
      @keyframes slideUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
      @keyframes glowPulse { 0%,100%{box-shadow:0 0 30px rgba(56,189,248,0.2)} 50%{box-shadow:0 0 60px rgba(56,189,248,0.4)} }
      @keyframes borderGlow {
        0%{border-color:rgba(56,189,248,0.3)}
        50%{border-color:rgba(129,140,248,0.6)}
        100%{border-color:rgba(56,189,248,0.3)}
      }

      .auth-wrapper {
        position:relative;z-index:1;
        min-height:calc(100vh - 64px);
        display:flex;align-items:center;justify-content:center;padding:2rem;
      }

      .glass-card {
        background:rgba(15,23,42,0.7);
        backdrop-filter:blur(40px) saturate(150%);
        border:1px solid rgba(56,189,248,0.2);
        border-radius:24px;padding:2.5rem;
        width:100%;max-width:420px;
        animation:slideUp 0.6s ease, glowPulse 4s infinite;
        box-shadow:0 25px 80px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
      }

      .card-header { text-align:center;margin-bottom:2rem; }
      .card-icon {
        width:64px;height:64px;border-radius:18px;
        background:linear-gradient(135deg,rgba(14,165,233,0.2),rgba(99,102,241,0.2));
        border:1px solid rgba(56,189,248,0.3);
        display:flex;align-items:center;justify-content:center;
        font-size:1.8rem;margin:0 auto 1rem;
        animation:glowPulse 3s infinite;
      }
      .card-title { font-size:1.6rem;font-weight:800;color:#f1f5f9;margin-bottom:0.3rem; }
      .card-sub { color:#64748b;font-size:0.85rem; }

      .form-group { margin-bottom:1.25rem;position:relative; }
      .form-label {
        display:block;color:#94a3b8;font-size:0.78rem;
        font-weight:600;letter-spacing:0.06em;margin-bottom:0.5rem;
      }
      .form-input {
        width:100%;padding:0.85rem 1rem 0.85rem 3rem;
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:12px;color:#e2e8f0;font-size:0.95rem;
        outline:none;transition:all 0.3s;
        backdrop-filter:blur(10px);
      }
      .form-input:focus {
        border-color:rgba(56,189,248,0.5);
        background:rgba(56,189,248,0.05);
        box-shadow:0 0 0 3px rgba(56,189,248,0.1), 0 0 20px rgba(56,189,248,0.1);
      }
      .input-icon {
        position:absolute;left:1rem;top:50%;transform:translateY(50%);
        color:#475569;font-size:1rem;pointer-events:none;
      }

      .btn-submit {
        width:100%;padding:0.95rem;
        background:linear-gradient(135deg,#0ea5e9,#6366f1);
        color:white;border:none;border-radius:12px;
        font-size:1rem;font-weight:700;cursor:pointer;
        transition:all 0.3s;position:relative;overflow:hidden;
        box-shadow:0 4px 20px rgba(14,165,233,0.3);
        margin-top:0.5rem;
      }
      .btn-submit::before {
        content:'';position:absolute;inset:0;
        background:linear-gradient(135deg,rgba(255,255,255,0.15),transparent);
        border-radius:inherit;
      }
      .btn-submit:hover:not(:disabled) {
        transform:translateY(-2px);
        box-shadow:0 8px 30px rgba(14,165,233,0.5);
      }
      .btn-submit:disabled { opacity:0.6;cursor:not-allowed; }

      .divider {
        display:flex;align-items:center;gap:1rem;margin:1.5rem 0;
        color:#334155;font-size:0.8rem;
      }
      .divider::before,.divider::after {
        content:'';flex:1;height:1px;background:rgba(255,255,255,0.06);
      }

      .auth-link { text-align:center;color:#64748b;font-size:0.85rem; }
      .auth-link a { color:#38bdf8;text-decoration:none;font-weight:600; }
      .auth-link a:hover { text-decoration:underline; }

      .error-box {
        background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);
        color:#fca5a5;padding:0.75rem 1rem;border-radius:10px;
        font-size:0.82rem;margin-bottom:1rem;display:none;
        animation:slideUp 0.3s ease;
      }

      .loading-dots::after {
        content:'';animation:dots 1.5s infinite;
      }
      @keyframes dots {
        0%{content:'.'} 33%{content:'..'} 66%{content:'...'} 100%{content:''}
      }
    </style>

    <div class="auth-wrapper">
      <div class="glass-card">
        <div class="card-header">
          <div class="card-icon">🔐</div>
          <h1 class="card-title">Connexion</h1>
          <p class="card-sub">Accédez à votre parcours personnalisé</p>
        </div>

        <div class="error-box" id="error-box"></div>

        <form id="login-form">
          <div class="form-group">
            <label class="form-label">ADRESSE EMAIL</label>
            <span class="input-icon">✉️</span>
            <input class="form-input" type="email" id="email" placeholder="votre@email.com" required autocomplete="email"/>
          </div>
          <div class="form-group">
            <label class="form-label">MOT DE PASSE</label>
            <span class="input-icon">🔑</span>
            <input class="form-input" type="password" id="password" placeholder="••••••••" required autocomplete="current-password"/>
          </div>

          <button type="submit" class="btn-submit" id="submit-btn">
            Se connecter
          </button>
        </form>

        <div class="divider">ou</div>
        <div class="auth-link">
          Pas encore de compte ? <a href="/register" data-link>Créer un compte</a>
        </div>
      </div>
    </div>
  `

  const form = main.querySelector('#login-form') as HTMLFormElement
  const errorBox = main.querySelector('#error-box') as HTMLElement
  const submitBtn = main.querySelector('#submit-btn') as HTMLButtonElement

  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    submitBtn.disabled = true
    submitBtn.innerHTML = '<span class="loading-dots">Connexion</span>'
    errorBox.style.display = 'none'

    try {
      const token = await api.login({
        email: (main.querySelector('#email') as HTMLInputElement).value,
        mot_de_passe: (main.querySelector('#password') as HTMLInputElement).value,
      })
      api.setToken(token.access_token)
      localStorage.setItem('token', token.access_token)
      const user = await api.getMe()
      localStorage.setItem('user', JSON.stringify(user))
      stopParticles()
      router.navigate('/dashboard')
    } catch (err: unknown) {
      errorBox.textContent = '❌ ' + (err instanceof Error ? err.message : 'Email ou mot de passe incorrect')
      errorBox.style.display = 'block'
      submitBtn.disabled = false
      submitBtn.textContent = 'Se connecter'
    }
  })

  container.appendChild(main)
  return container
}
