// ============================================================
// API Service - Communication avec le backend FastAPI
// ============================================================
// C'est quoi ce fichier ?
//
// C'est le "FACTEUR" de l'application. Il envoie des requêtes
// HTTP au backend (FastAPI) et rapporte les réponses.
//
// Chaque méthode = un appel à un endpoint du backend.
// Exemple : api.login() → POST /api/auth/login
//
// C'est quoi une requête HTTP ?
// C'est un message envoyé par le navigateur au serveur.
// Il y a 4 types principaux :
//   GET    → "donne-moi des données"       (lire)
//   POST   → "voici des données, traite-les" (créer)
//   PUT    → "modifie ces données"          (mettre à jour)
//   DELETE → "supprime ces données"         (supprimer)
//
// C'est quoi une interface TypeScript ?
// C'est un "contrat" qui décrit la FORME d'un objet.
// Par exemple, l'interface Etudiant dit :
//   "un objet Etudiant DOIT avoir un id (number), un nom (string)..."
// Si on essaie de créer un Etudiant sans id → TypeScript refuse.
// Ça évite les bugs AVANT même d'exécuter le code !
// ============================================================

const BASE_URL = '/api'

// ============================================================
// INTERFACES — Les "contrats" des données
// ============================================================

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

// ============================================================
// NOUVELLES INTERFACES — Pour le Tuteur IA
// ============================================================
// Ces interfaces décrivent les données échangées entre
// le frontend et les endpoints /tutor/*

/**
 * Une session de tutorat (une conversation).
 * C'est comme un "fil de discussion" WhatsApp.
 */
export interface TutorSession {
  id: number
  etudiant_id: number
  concept_id: string | null      // Le concept discuté (peut être null)
  created_at: string             // Date ISO (ex: "2026-04-15T10:30:00")
  updated_at: string
  message_count: number          // Nombre de messages dans la session
}

/**
 * Un message dans une session de tutorat.
 * Peut être de l'étudiant ("student") ou du tuteur ("tutor").
 */
export interface TutorMessage {
  id: number
  role: 'student' | 'tutor'     // Qui a envoyé le message
  content: string                // Le texte (peut contenir du LaTeX)
  verified: boolean | null       // Maths vérifiées par SymPy ?
  concept_id: string | null      // Le concept identifié
  created_at: string
}

/**
 * Ce que le frontend ENVOIE pour poser une question.
 */
export interface TutorAskRequest {
  question: string               // La question de l'étudiant
  concept_id?: string            // Concept ciblé (optionnel)
}

/**
 * Ce que le backend RETOURNE après la réponse de Gemini.
 */
export interface TutorAskResponse {
  message_id: number             // ID du message sauvegardé
  content: string                // La réponse de Gemini (avec LaTeX)
  verified: boolean              // Badge "Vérifié par SymPy"
  concept_name: string           // Nom du concept identifié
  student_mastery: number        // Maîtrise de l'étudiant (0-100)
  complexity_level: string       // "simplified" | "standard" | "rigorous"
  verification_details: any      // Détails de la vérification SymPy
}

/**
 * L'historique complet d'une session.
 */
export interface TutorSessionHistory {
  session_id: number
  concept_id: string | null
  messages: TutorMessage[]
}


// ============================================================
// LA CLASSE ApiService — Le facteur
// ============================================================

class ApiService {
  // Le token JWT (null si pas connecté)
  // C'est comme un "badge d'accès" qu'on montre à chaque requête
  private token: string | null = null

  setToken(token: string) {
    this.token = token
  }

  clearToken() {
    this.token = null
  }

  // --- En-têtes HTTP ---
  // Chaque requête envoie des "en-têtes" (headers) :
  //   Content-Type: application/json → "je t'envoie du JSON"
  //   Authorization: Bearer <token> → "voici mon badge d'accès"
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = { 'Content-Type': 'application/json' }
    if (this.token) headers['Authorization'] = `Bearer ${this.token}`
    return headers
  }

  // --- Méthode générique pour toutes les requêtes ---
  // Au lieu de répéter le code fetch() partout, on a UNE méthode
  // qui fait le travail pour toutes les requêtes.
  //
  // <T> est un "Generic TypeScript" : ça veut dire "le type de retour
  // sera défini par celui qui appelle cette méthode".
  // Ex: request<Quiz>('GET', '/quiz/1') → retourne un Quiz
  private async request<T>(method: string, endpoint: string, body?: unknown): Promise<T> {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method,
      headers: this.getHeaders(),
      body: body ? JSON.stringify(body) : undefined
    })

    if (!response.ok) {
      // Si le token est expiré (erreur 401), on redirige AUTOMATIQUEMENT
      // vers la page de connexion. Comme ça l'étudiant n'a plus à le
      // faire manuellement — il se reconnecte et c'est reparti.
      if (response.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login'
        throw new Error('Session expirée, reconnexion...')
      }
      const error = await response.json().catch(() => ({ detail: 'Erreur serveur' }))
      throw new Error(error.detail || `Erreur ${response.status}`)
    }

    return response.json()
  }

  // ============================================================
  // AUTHENTIFICATION
  // ============================================================

  async login(data: LoginRequest): Promise<TokenResponse> {
    // OAuth2PasswordRequestForm attend du form-data, pas du JSON
    // C'est une particularité de FastAPI pour /auth/login
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

  // ============================================================
  // GRAPHE DE CONNAISSANCES
  // ============================================================

  async getConcepts(): Promise<Concept[]> {
    return this.request<Concept[]>('GET', '/graph/concepts')
  }

  async getLearningPath(etudiantId: number): Promise<LearningPath> {
    return this.request<LearningPath>('GET', `/graph/learning-path/${etudiantId}`)
  }

  async getRemediation(conceptId: string) {
    return this.request('GET', `/graph/remediation/${conceptId}`)
  }

  // ============================================================
  // QUIZ
  // ============================================================

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

  // ============================================================
  // TUTEUR IA (NOUVEAU !)
  // ============================================================
  // Ces méthodes appellent les endpoints /tutor/* qu'on a créés
  // dans backend/app/routers/tutor.py

  /**
   * Crée une nouvelle session de tutorat.
   *
   * C'est comme ouvrir une nouvelle conversation WhatsApp.
   * Le concept_id est optionnel — si fourni, la session sera
   * "ciblée" sur ce concept.
   *
   * Appelle : POST /tutor/sessions
   */
  async createTutorSession(conceptId?: string): Promise<TutorSession> {
    return this.request<TutorSession>(
      'POST',
      '/tutor/sessions',
      { concept_id: conceptId || null }
    )
  }

  /**
   * Liste toutes les sessions de tutorat de l'étudiant connecté.
   *
   * C'est la liste des conversations passées, triées de la
   * plus récente à la plus ancienne.
   *
   * Appelle : GET /tutor/sessions
   */
  async getTutorSessions(): Promise<TutorSession[]> {
    return this.request<TutorSession[]>('GET', '/tutor/sessions')
  }

  /**
   * Pose une question au tuteur IA dans une session donnée.
   *
   * C'est L'APPEL le plus important ! Il déclenche tout le
   * pipeline GraphRAG :
   *   Question → RAG → Gemini → SymPy → Réponse vérifiée
   *
   * Appelle : POST /tutor/sessions/{sessionId}/ask
   *
   * @param sessionId - l'ID de la session
   * @param data - { question: "...", concept_id?: "..." }
   * @returns La réponse de Gemini avec le badge de vérification
   */
  async askTutor(sessionId: number, data: TutorAskRequest): Promise<TutorAskResponse> {
    return this.request<TutorAskResponse>(
      'POST',
      `/tutor/sessions/${sessionId}/ask`,
      data
    )
  }

  /**
   * Récupère l'historique complet d'une session.
   *
   * Appelé quand l'étudiant ouvre une conversation existante.
   * Retourne TOUS les messages triés par date.
   *
   * Appelle : GET /tutor/sessions/{sessionId}/history
   */
  async getTutorHistory(sessionId: number): Promise<TutorSessionHistory> {
    return this.request<TutorSessionHistory>(
      'GET',
      `/tutor/sessions/${sessionId}/history`
    )
  }
}

export const api = new ApiService()
