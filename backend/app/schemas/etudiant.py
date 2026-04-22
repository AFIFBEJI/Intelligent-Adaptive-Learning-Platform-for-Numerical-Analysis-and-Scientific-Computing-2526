
from pydantic import BaseModel


class EtudiantCreate(BaseModel):
    nom_complet: str
    email: str
    mot_de_passe: str
    niveau_actuel: str = "Débutant"


class EtudiantResponse(BaseModel):
    id: int
    nom_complet: str
    email: str
    niveau_actuel: str
    # ⚠️ mot_de_passe absent intentionnellement - jamais envoyé au client!

    class Config:
        from_attributes = True


class EtudiantUpdate(BaseModel):
    nom_complet: str | None = None
    email: str | None = None
    mot_de_passe: str | None = None
    niveau_actuel: str | None = None


class LoginRequest(BaseModel):
    email: str
    mot_de_passe: str


class Token(BaseModel):
    access_token: str
    token_type: str
