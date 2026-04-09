from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_tables
from app.routers import auth, etudiants, graph, quiz 

app = FastAPI(
    title="PFE - Adaptive Learning Platform",
    description="API Backend pour la plateforme d'apprentissage adaptatif",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(etudiants.router)
app.include_router(graph.router)
app.include_router(quiz.router)

@app.on_event("startup")
def startup():
    create_tables()
    print("✅ Tables créées dans PostgreSQL!")
    print("✅ Router Quiz chargé!")

@app.get("/")
def root():
    return {"message": "PFE API fonctionne!", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}