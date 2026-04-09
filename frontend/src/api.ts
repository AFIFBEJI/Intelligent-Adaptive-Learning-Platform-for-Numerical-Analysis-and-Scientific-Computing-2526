// ============================================================
// API Service - Communication avec le backend FastAPI
// ============================================================

const BASE_URL = '/api'

export interface LoginRequest {
  email: string
  mot_de_passe: string
}

export interface RegisterRequest {
  nom_complet: string
  email: string
  mot_de_passe: string
  niveau_actuel: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface Etudiant {
  id: number
  nom_complet: string
  email: string
  niveau_actuel: string
  date_inscription: string
  is_active: boolean
}

export interface Concept {
  id: string
  name: string
  description: string
  level: string
  category: string
}

export interface LearningPath {
  etudiant_id: number
  concepts_to_improve: Array<{ id: string; name: string; mastery: number; status: string }>
  next_recommended: Array<{ id: string; name: string; level: string; category: string }>
  overall_progress: { total_concepts: number; mastered: number; in_progress: number }
}

class ApiService {
  private token: string | null = null

  setToken(token: string) {
    this.token = token
  }

  clearToken() {
    this.token = null
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = { 'Content-Type': 'application/json' }
    if (this.token) headers['Authorization'] = `Bearer ${this.token}`
    return headers
  }

  private async request<T>(method: string, endpoint: string, body?: unknown): Promise<T> {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method,
      headers: this.getHeaders(),
      body: body ? JSON.stringify(body) : undefined
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Erreur serveur' }))
      throw new Error(error.detail || `Erreur ${response.status}`)
    }

    return response.json()
  }

  // Auth
  async login(data: LoginRequest): Promise<TokenResponse> {
    return this.request<TokenResponse>('POST', '/auth/login', data)
  }

  async register(data: RegisterRequest): Promise<TokenResponse> {
    return this.request<TokenResponse>('POST', '/auth/register', data)
  }

  async getMe(): Promise<Etudiant> {
    return this.request<Etudiant>('GET', '/auth/me')
  }

  // Graph
  async getConcepts(): Promise<Concept[]> {
    return this.request<Concept[]>('GET', '/graph/concepts')
  }

  async getLearningPath(etudiantId: number): Promise<LearningPath> {
    return this.request<LearningPath>('GET', `/graph/learning-path/${etudiantId}`)
  }

  async getRemediation(conceptId: string) {
    return this.request('GET', `/graph/remediation/${conceptId}`)
  }
}

export const api = new ApiService()
