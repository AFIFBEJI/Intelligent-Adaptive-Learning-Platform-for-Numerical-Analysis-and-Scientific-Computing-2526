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

export interface Quiz {
  id: number
  titre: string
  module: string
  difficulte: string
  questions: Array<{
    id: number
    question: string
    options: string[]
    correct_index: number
    points: number
  }>
  date_creation: string
}

export interface QuizResult {
  id: number
  etudiant_id: number
  quiz_id: number
  score: number
  temps_reponse: number
  reponses: any
  date_tentative: string
}

export interface QuizSubmit {
  etudiant_id: number
  score: number
  temps_reponse: number
  reponses: any
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

  async login(data: LoginRequest): Promise<TokenResponse> {
  // OAuth2PasswordRequestForm attend du form-data, pas du JSON
  const formData = new URLSearchParams()
  formData.append('username', data.email)
  formData.append('password', data.mot_de_passe)

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData.toString()
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Erreur serveur' }))
    throw new Error(error.detail || `Erreur ${response.status}`)
  }

  return response.json()
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

  // Quiz
  async getQuizList(module?: string, difficulte?: string): Promise<Quiz[]> {
    let endpoint = '/quiz/'
    const params = new URLSearchParams()
    if (module) params.append('module', module)
    if (difficulte) params.append('difficulte', difficulte)
    const query = params.toString()
    if (query) endpoint += `?${query}`
    return this.request<Quiz[]>('GET', endpoint)
  }

  async getQuiz(quizId: number): Promise<Quiz> {
    return this.request<Quiz>('GET', `/quiz/${quizId}`)
  }

  async submitQuiz(quizId: number, data: QuizSubmit): Promise<QuizResult> {
    return this.request<QuizResult>('POST', `/quiz/${quizId}/submit`, data)
  }

  async getMyResults(etudiantId: number): Promise<QuizResult[]> {
    return this.request<QuizResult[]>('GET', `/quiz/results/${etudiantId}`)
  }
}

export const api = new ApiService()
