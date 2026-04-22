# ============================================================
# Configuration de l'application
# ============================================================
# Ce fichier lit TOUTES les variables depuis le fichier .env
# Pourquoi ? Pour ne JAMAIS mettre de mots de passe dans le code.
#
# Comment ça marche ?
# 1. Vous écrivez GOOGLE_API_KEY=abc123 dans .env
# 2. Pydantic Settings lit automatiquement ce fichier
# 3. Vous accédez à la valeur avec : settings.GOOGLE_API_KEY
# ============================================================

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Lit automatiquement toutes les variables depuis le fichier .env

    Chaque attribut ci-dessous correspond à une ligne dans .env.
    Si une variable a une valeur par défaut (ex: ALGORITHM = "HS256"),
    elle est optionnelle dans .env. Sinon, elle est OBLIGATOIRE.
    """

    # --- PostgreSQL ---
    # L'URL de connexion à PostgreSQL
    # Format : postgresql://utilisateur:motdepasse@adresse:port/nom_base
    DATABASE_URL: str

    # --- Neo4j (Graphe de connaissances) ---
    # URI : l'adresse de Neo4j (bolt:// est le protocole de communication)
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str

    # --- JWT (Authentification) ---
    # SECRET_KEY : une clé secrète pour signer les tokens JWT
    # C'est comme un tampon officiel : si quelqu'un modifie le token, la signature ne match plus
    SECRET_KEY: str
    # ALGORITHM : l'algorithme de signature (HS256 = HMAC-SHA256, très courant)
    ALGORITHM: str = "HS256"
    # Durée de validité du token en minutes (60 min = 1 heure)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 jours (7 * 24 * 60)

    # ============================================================
    # NOUVEAU - Tuteur IA GraphRAG (Gemini gratuit)
    # ============================================================

    # --- Google Gemini ---
    # Votre clé API Gemini (gratuite, à créer sur aistudio.google.com)
    # Cette clé permet à notre application d'envoyer des requêtes à Gemini
    GOOGLE_API_KEY: str = ""

    # Le modèle Gemini à utiliser
    # "gemini-2.0-flash" : rapide et gratuit, très bon pour les maths
    # Alternatives : "gemini-1.5-pro" (plus puissant mais quota plus limité)
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # --- Paramètres du LLM ---
    # Temperature : contrôle la "créativité" de l'IA (0.0 à 1.0)
    # 0.0 = très déterministe (même question → même réponse)
    # 1.0 = très créatif (réponses variées mais parfois incohérentes)
    # 0.3 = bon équilibre pour les maths (précision > créativité)
    LLM_TEMPERATURE: float = 0.3

    # Nombre maximum de tokens dans la réponse
    # 1 token ≈ 0.75 mot en français
    # 2048 tokens ≈ 1500 mots (suffisant pour une explication détaillée)
    LLM_MAX_TOKENS: int = 2048

    # --- Paramètres du RAG (Retrieval-Augmented Generation) ---
    # Profondeur de recherche des prérequis dans Neo4j
    # Ex: Si depth=3 et l'étudiant pose une question sur RK4 :
    #   RK4 → REQUIRES → Improved Euler → REQUIRES → Euler → REQUIRES → Taylor Series
    # On remonte 3 niveaux dans l'arbre des prérequis
    RAG_PREREQUISITE_DEPTH: int = 3

    # Seuil de maîtrise (0-100) au-dessus duquel un concept est "maîtrisé"
    # Si maîtrise >= 70%, l'étudiant a compris le concept
    MASTERY_THRESHOLD: float = 70.0

    # Active/désactive la vérification SymPy des formules dans les réponses
    # True = on vérifie chaque formule LaTeX (plus sûr mais plus lent)
    ENABLE_SYMPY_VERIFICATION: bool = True

    # ============================================================
    # Ollama (Modèle local — fallback si Gemini est indisponible)
    # ============================================================
    # Ollama fait tourner des modèles d'IA directement sur ton PC.
    # Avantages : pas de quota, pas d'internet, données privées.
    # Inconvénient : un peu moins bon en maths que Gemini.

    # Le modèle Ollama à utiliser (doit être téléchargé avec "ollama pull")
    # "llama3.1:8b" : bon équilibre qualité/vitesse, ~5 Go de RAM
    # Alternatives : "mistral:7b" (rapide), "llama3.1:70b" (meilleur mais lourd)
    OLLAMA_MODEL: str = "llama3.1:8b"

    # L'adresse du serveur Ollama sur ton PC
    # Par défaut, Ollama écoute sur le port 11434 de ta machine
    # Tu n'as RIEN à changer ici sauf si tu as modifié la config d'Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    class Config:
        # Où chercher le fichier .env (2 niveaux au-dessus de app/core/)
        env_file = "../.env"


@lru_cache
def get_settings():
    """
    Retourne les settings en cache.

    @lru_cache() = la première fois qu'on appelle get_settings(),
    Python lit le .env et crée l'objet Settings.
    Les appels suivants retournent le même objet sans relire le .env.
    C'est une optimisation de performance.
    """
    return Settings()
