// ============================================================
// Register Page — Glassmorphism 3D
// ============================================================

import { api } from '../api'
import { createNavbar } from '../components/navbar'
import { createParticleBackground } from '../components/particles'
import { router } from '../router'

export function RegisterPage(): HTMLElement {
  const container = document.createElement('div')
  container.style.cssText = 'min-height:100vh;overflow:hidden;position:relative;'

  const stopParticles = createParticleBackground(container)
  container.appendChild(createNavbar())

  const main = document.createElement('div')
  main.innerHTML = `
    <style>
      @keyframes slideUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
      @keyframes glowPulse { 0%,100%{box-shadow:0 0 30px rgba(129,140,248,0.2)} 50%{box-shadow:0 0 60px rgba(129,140,248,0.4)} }

      .auth-wrapper {
        position:relative;z-index:1;
        min-height:calc(100vh - 64px);
        display:flex;align-items:center;justify-content:center;
        padding:2rem;
      }

      .glass-card {
        background:rgba(15,23,42,0.75);
        backdrop-filter:blur(40px) saturate(150%);
        border:1px solid rgba(129,140,248,0.2);
        border-radius:24px;padding:2.5rem;
        width:100%;max-width:440px;
        animation:slideUp 0.6s ease, glowPulse 4s infinite;
        box-shadow:0 25px 80px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
      }

      .card-header { text-align:center;margin-bottom:2rem; }
      .card-icon {
        width:64px;height:64px;border-radius:18px;
        background:linear-gradient(135deg,rgba(99,102,241,0.2),rgba(192,132,252,0.2));
        border:1px solid rgba(129,140,248,0.3);
        display:flex;align-items:center;justify-content:center;
        font-size:1.8rem;margin:0 auto 1rem;animation:glowPulse 3s infinite;
      }
      .card-title { font-size:1.6rem;font-weight:800;color:#f1f5f9;margin-bottom:0.3rem; }
      .card-sub { color:#64748b;font-size:0.85rem; }

      .form-row { display:grid;grid-template-columns:1fr 1fr;gap:1rem; }
      .form-group { margin-bottom:1.1rem;position:relative; }
      .form-label { display:block;color:#94a3b8;font-size:0.78rem;font-weight:600;letter-spacing:0.06em;margin-bottom:0.4rem; }
      .form-input, .form-select {
        width:100%;padding:0.8rem 1rem 0.8rem 2.8rem;
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:12px;color:#e2e8f0;font-size:0.9rem;
        outline:none;transition:all 0.3s;
      }
      .form-select { padding-left:1rem; }
      .form-input:focus, .form-select:focus {
        border-color:rgba(129,140,248,0.5);
        background:rgba(129,140,248,0.05);
        box-shadow:0 0 0 3px rgba(129,140,248,0.1);
      }
      .form-select option { background:#1e293b;color:#e2e8f0; }
      .input-icon { position:absolute;left:0.9rem;top:50%;transform:translateY(50%);color:#475569;font-size:0.9rem;pointer-events:none; }

      .niveau-options { display:grid;grid-template-columns:repeat(3,1fr);gap:0.5rem; }
      .niveau-btn {
        padding:0.6rem;border-radius:10px;border:1px solid rgba(255,255,255,0.08);
        background:transparent;color:#94a3b8;font-size:0.78rem;font-weight:600;
        cursor:pointer;transition:all 0.2s;text-align:center;
      }
      .niveau-btn:hover { border-color:rgba(129,140,248,0.4);color:#e2e8f0; }
      .niveau-btn.selected {
        background:rgba(99,102,241,0.2);border-color:rgba(129,140,248,0.6);
        color:#a5b4fc;box-shadow:0 0 15px rgba(99,102,241,0.2);
      }

      .btn-submit {
        width:100%;padding:0.95rem;
        background:linear-gradient(135deg,#6366f1,#c084fc);
        color:white;border:none;border-radius:12px;
        font-size:1rem;font-weight:700;cursor:pointer;
        transition:all 0.3s;overflow:hidden;position:relative;
        box-shadow:0 4px 20px rgba(99,102,241,0.3);margin-top:0.75rem;
      }
      .btn-submit:hover:not(:disabled) { transform:translateY(-2px);box-shadow:0 8px 30px rgba(99,102,241,0.5); }
      .btn-submit:disabled { opacity:0.6;cursor:not-allowed; }
      .btn-submit::before { content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,0.15),transparent); }

      .divider { display:flex;align-items:center;gap:1rem;margin:1.25rem 0;color:#334155;font-size:0.8rem; }
      .divider::before,.divider::after { content:'';flex:1;height:1px;background:rgba(255,255,255,0.06); }
      .auth-link { text-align:center;color:#64748b;font-size:0.85rem; }
      .auth-link a { color:#818cf8;text-decoration:none;font-weight:600; }

      .error-box {
        background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);
        color:#fca5a5;padding:0.75rem 1rem;border-radius:10px;
        font-size:0.82rem;margin-bottom:1rem;display:none;
      }
      .password-strength { height:3px;border-radius:2px;margin-top:0.4rem;transition:all 0.3s;background:#1e293b; }
    </style>

    <div class="auth-wrapper">
      <div class="glass-card">
        <div class="card-header">
          <div class="card-icon">🎓</div>
          <h1 class="card-title">Créer un compte</h1>
          <p class="card-sub">Rejoignez la plateforme adaptative</p>
        </div>

        <div class="error-box" id="error-box"></div>

        <form id="register-form">
          <div class="form-group">
            <label class="form-label">NOM COMPLET</label>
            <span class="input-icon">👤</span>
            <input class="form-input" type="text" id="nom" placeholder="Prénom Nom" required/>
          </div>

          <div class="form-group">
            <label class="form-label">EMAIL</label>
            <span class="input-icon">✉️</span>
            <input class="form-input" type="email" id="email" placeholder="votre@email.com" required/>
          </div>

          <div class="form-group">
            <label class="form-label">MOT DE PASSE</label>
            <span class="input-icon">🔑</span>
            <input class="form-input" type="password" id="password" placeholder="Minimum 8 caractères" required minlength="8"/>
            <div class="password-strength" id="pwd-strength"></div>
          </div>

          <div class="form-group">
            <label class="form-label">NIVEAU ACTUEL</label>
            <div class="niveau-options">
              <button type="button" class="niveau-btn" data-val="debutant">🌱 Débutant</button>
              <button type="button" class="niveau-btn selected" data-val="intermediaire">⚡ Intermédiaire</button>
              <button type="button" class="niveau-btn" data-val="avance">🔥 Avancé</button>
            </div>
            <input type="hidden" id="niveau" value="intermediaire"/>
          </div>

          <button type="submit" class="btn-submit" id="submit-btn">🚀 Créer mon compte</button>
        </form>

        <div class="divider">ou</div>
        <div class="auth-link">Déjà un compte ? <a href="/login" data-link>Se connecter</a></div>
      </div>
    </div>
  `

  // Niveau buttons
  main.querySelectorAll('.niveau-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      main.querySelectorAll('.niveau-btn').forEach(b => b.classList.remove('selected'))
      btn.classList.add('selected');
      (main.querySelector('#niveau') as HTMLInputElement).value = (btn as HTMLElement).dataset.val || ''
    })
  })

  // Password strength
  const pwdInput = main.querySelector('#password') as HTMLInputElement
  const pwdStrength = main.querySelector('#pwd-strength') as HTMLElement
  pwdInput.addEventListener('input', () => {
    const v = pwdInput.value
    const strength = [v.length >= 8, /[A-Z]/.test(v), /[0-9]/.test(v), /[^a-zA-Z0-9]/.test(v)].filter(Boolean).length
    const colors = ['transparent', '#ef4444', '#f97316', '#eab308', '#22c55e']
    const widths = ['0%', '25%', '50%', '75%', '100%']
    pwdStrength.style.width = widths[strength]
    pwdStrength.style.background = colors[strength]
  })

  // Submit
  const form = main.querySelector('#register-form') as HTMLFormElement
  const errorBox = main.querySelector('#error-box') as HTMLElement
  const submitBtn = main.querySelector('#submit-btn') as HTMLButtonElement

  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    submitBtn.disabled = true
    submitBtn.textContent = 'Création...'
    errorBox.style.display = 'none'

    try {
      const token = await api.register({
        nom_complet: (main.querySelector('#nom') as HTMLInputElement).value,
        email: (main.querySelector('#email') as HTMLInputElement).value,
        mot_de_passe: (main.querySelector('#password') as HTMLInputElement).value,
        niveau_actuel: (main.querySelector('#niveau') as HTMLInputElement).value,
      })
      api.setToken(token.access_token)
      localStorage.setItem('token', token.access_token)
      const user = await api.getMe()
      localStorage.setItem('user', JSON.stringify(user))
      stopParticles()
      router.navigate('/dashboard')
    } catch (err: unknown) {
      errorBox.textContent = '❌ ' + (err instanceof Error ? err.message : 'Erreur lors de l\'inscription')
      errorBox.style.display = 'block'
      submitBtn.disabled = false
      submitBtn.textContent = '🚀 Créer mon compte'
    }
  })

  container.appendChild(main)
  return container
}
