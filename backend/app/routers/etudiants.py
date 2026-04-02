from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hacher_mot_de_passe
from app.models.etudiant import Etudiant
from app.schemas.etudiant import EtudiantCreate, EtudiantResponse, EtudiantUpdate

router = APIRouter(prefix="/etudiants", tags=["etudiants"])


@router.post("/", response_model=EtudiantResponse)
def creer_etudiant(etudiant: EtudiantCreate, db: Session = Depends(get_db)):
    etudiant_existant = db.query(Etudiant).filter(
        Etudiant.email == etudiant.email
    ).first()
    if etudiant_existant:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")

    nouvel_etudiant = Etudiant(
        nom_complet=etudiant.nom_complet,
        email=etudiant.email,
        mot_de_passe=hacher_mot_de_passe(etudiant.mot_de_passe),
        niveau_actuel=etudiant.niveau_actuel
    )
    db.add(nouvel_etudiant)
    db.commit()
    db.refresh(nouvel_etudiant)
    return nouvel_etudiant


@router.get("/", response_model=list[EtudiantResponse])
def lire_tous_les_etudiants(db: Session = Depends(get_db)):
    return db.query(Etudiant).all()


@router.get("/{etudiant_id}", response_model=EtudiantResponse)
def lire_un_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    if etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant introuvable.")
    return etudiant


@router.put("/{etudiant_id}", response_model=EtudiantResponse)
def modifier_etudiant(etudiant_id: int, modifications: EtudiantUpdate, db: Session = Depends(get_db)):
    etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    if etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant introuvable.")

    if modifications.nom_complet is not None:
        etudiant.nom_complet = modifications.nom_complet
    if modifications.email is not None:
        etudiant.email = modifications.email
    if modifications.mot_de_passe is not None:
        etudiant.mot_de_passe = hacher_mot_de_passe(modifications.mot_de_passe)
    if modifications.niveau_actuel is not None:
        etudiant.niveau_actuel = modifications.niveau_actuel

    db.commit()
    db.refresh(etudiant)
    return etudiant


@router.delete("/{etudiant_id}")
def supprimer_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    if etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant introuvable.")
    db.delete(etudiant)
    db.commit()
    return {"message": f"Étudiant {etudiant_id} supprimé avec succès."}