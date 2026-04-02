from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_tables
from app.routers import auth, etudiants

# Créer l'application FastAPI
app = FastAPI(
    title="PFE - Adaptive Learning Platform",
    description="API Backend pour la plateforme d'apprentissage adaptatif",
    version="1.0.0"
)

# Permettre au frontend Vanilla TypeScript + Vite (port 5173) de parler au backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrer les routers
app.include_router(auth.router)
app.include_router(etudiants.router)


@app.on_event("startup")
def startup():
    """Au démarrage: créer les tables dans PostgreSQL."""
    create_tables()
    print("✅ Tables créées dans PostgreSQL!")


@app.get("/")
def root():
    return {"message": "PFE API fonctionne!", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}