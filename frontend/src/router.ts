// ============================================================
// Router - Custom SPA Router (Vanilla TypeScript)
// ============================================================

type RouteHandler = () => HTMLElement

interface Route {
  path: string
  handler: RouteHandler
  requiresAuth: boolean
}

class Router {
  private routes: Route[] = []
  private appContainer: HTMLElement

  constructor(containerId: string) {
    const container = document.getElementById(containerId)
    if (!container) throw new Error(`Container #${containerId} not found`)
    this.appContainer = container

    window.addEventListener('popstate', () => this.resolve())
    document.addEventListener('click', (e) => {
      const target = e.target as HTMLElement
      const link = target.closest('[data-link]') as HTMLAnchorElement | null
      if (link) {
        e.preventDefault()
        this.navigate(link.getAttribute('href') || '/')
      }
    })
  }

  addRoute(path: string, handler: RouteHandler, requiresAuth = false): Router {
    this.routes.push({ path, handler, requiresAuth })
    return this
  }

  navigate(path: string): void {
    window.history.pushState(null, '', path)
    this.resolve()
  }

  resolve(): void {
    const path = window.location.pathname
    const route = this.routes.find(r => r.path === path) || this.routes.find(r => r.path === '/404')

    if (!route) return

    const token = localStorage.getItem('token')
    if (route.requiresAuth && !token) {
      this.navigate('/login')
      return
    }

    if ((path === '/login' || path === '/register') && token) {
      this.navigate('/dashboard')
      return
    }

    this.appContainer.innerHTML = ''
    this.appContainer.appendChild(route.handler())
  }

  start(): void {
    this.resolve()
  }
}

export const router = new Router('app')
