from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models
import schemas
import utils

# 1. On vérifie que les tables existent au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PFE Adaptive Learning API")

# 2. Fonction qui gère la connexion à la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- CREATE : CRÉER UN ÉTUDIANT ---
@app.post("/etudiants/", response_model=schemas.EtudiantResponse)
def creer_etudiant(etudiant: schemas.EtudiantCreate, db: Session = Depends(get_db)):
    
    # Vérifier si l'email existe déjà
    etudiant_existant = db.query(models.Etudiant).filter(
        models.Etudiant.email == etudiant.email
    ).first()
    if etudiant_existant:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")
    
    nouvel_etudiant = models.Etudiant(
        nom_complet=etudiant.nom_complet,
        email=etudiant.email,
        mot_de_passe=utils.hacher_mot_de_passe(etudiant.mot_de_passe),  # ✅ Haché
        niveau_actuel=etudiant.niveau_actuel
    )
    
    db.add(nouvel_etudiant)
    db.commit()
    db.refresh(nouvel_etudiant)
    return nouvel_etudiant


# --- READ : VOIR TOUS LES ÉTUDIANTS ---
@app.get("/etudiants/", response_model=list[schemas.EtudiantResponse])
def lire_tous_les_etudiants(db: Session = Depends(get_db)):
    etudiants = db.query(models.Etudiant).all()
    return etudiants


# --- READ : VOIR UN SEUL ÉTUDIANT PAR SON ID ---
@app.get("/etudiants/{etudiant_id}", response_model=schemas.EtudiantResponse)
def lire_un_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    etudiant = db.query(models.Etudiant).filter(
        models.Etudiant.id == etudiant_id
    ).first()
    
    # ✅ Retourner une erreur 404 si l'étudiant n'existe pas
    if etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant introuvable.")
    
    return etudiant


# --- UPDATE : MODIFIER UN ÉTUDIANT ---
@app.put("/etudiants/{etudiant_id}", response_model=schemas.EtudiantResponse)
def modifier_etudiant(etudiant_id: int, modifications: schemas.EtudiantUpdate, db: Session = Depends(get_db)):
    etudiant = db.query(models.Etudiant).filter(
        models.Etudiant.id == etudiant_id
    ).first()
    
    # ✅ Retourner une erreur 404 si l'étudiant n'existe pas
    if etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant introuvable.")
    
    if modifications.nom_complet is not None:
        etudiant.nom_complet = modifications.nom_complet
    if modifications.email is not None:
        etudiant.email = modifications.email
    if modifications.mot_de_passe is not None:
        etudiant.mot_de_passe = utils.hacher_mot_de_passe(modifications.mot_de_passe)  # ✅ Haché
    if modifications.niveau_actuel is not None:
        etudiant.niveau_actuel = modifications.niveau_actuel
        
    db.commit()
    db.refresh(etudiant)
    return etudiant


# --- DELETE : SUPPRIMER UN ÉTUDIANT ---
@app.delete("/etudiants/{etudiant_id}")
def supprimer_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    etudiant = db.query(models.Etudiant).filter(
        models.Etudiant.id == etudiant_id
    ).first()
    
    # ✅ Retourner une erreur 404 si l'étudiant n'existe pas
    if etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant introuvable.")
    
    db.delete(etudiant)
    db.commit()
    return {"message": f"L'étudiant numéro {etudiant_id} a été supprimé avec succès."}