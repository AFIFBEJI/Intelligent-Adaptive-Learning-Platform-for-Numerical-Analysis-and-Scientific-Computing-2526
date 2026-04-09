// ============================================================
// Point d'entrée principal - Adaptive Learning Platform SPA
// ============================================================

import { router } from './router'
import { HomePage } from './pages/home'
import { LoginPage } from './pages/login'
import { RegisterPage } from './pages/register'
import { DashboardPage } from './pages/dashboard'
import { ConceptsPage } from './pages/concepts'

// Restaurer le token au démarrage
const token = localStorage.getItem('token')
if (token) {
  const { api } = await import('./api')
  api.setToken(token)
}

// Définir les routes
router
  .addRoute('/', HomePage, false)
  .addRoute('/login', LoginPage, false)
  .addRoute('/register', RegisterPage, false)
  .addRoute('/dashboard', DashboardPage, true)
  .addRoute('/concepts', ConceptsPage, true)

// Démarrer le router
router.start()
