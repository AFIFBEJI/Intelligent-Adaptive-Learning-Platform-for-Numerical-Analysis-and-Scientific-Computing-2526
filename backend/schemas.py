from pydantic import BaseModel
from typing import Optional
class EtudiantCreate(BaseModel):
    nom_complet: str
    email: str
    mot_de_passe: str
    niveau_actuel: str = "Débutant"

# --- NOUVEAU CODE À AJOUTER EN DESSOUS ---

class EtudiantResponse(BaseModel):
    id: int
    nom_complet: str
    email: str
    niveau_actuel: str
    # 🚨 Remarquez bien : on ne met PAS le mot_de_passe ici pour le protéger !

    class Config:
        from_attributes = True # Permet à Pydantic de lire les données de SQLAlchemy

# --- NOUVEAU SCHÉMA POUR LA MODIFICATION ---
class EtudiantUpdate(BaseModel):
    nom_complet: Optional[str] = None
    email: Optional[str] = None
    mot_de_passe: Optional[str] = None
    niveau_actuel: Optional[str] = None