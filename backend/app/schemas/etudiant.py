from typing import Literal

from pydantic import BaseModel, Field

Langue = Literal["en", "fr"]


class EtudiantCreate(BaseModel):
    nom_complet: str
    email: str
    mot_de_passe: str
    niveau_actuel: str = "beginner"
    # Langue obligatoire : aucun défaut, doit être explicitement fournie ('en' ou 'fr').
    langue_preferee: Langue = Field(..., description="Langue d'apprentissage choisie au moment de l'inscription. Obligatoire.")


class EtudiantResponse(BaseModel):
    id: int
    nom_complet: str
    email: str
    niveau_actuel: str
    langue_preferee: Langue = "en"
    # Phase 3 : etat de verification de l'email. Le frontend peut
    # afficher un bandeau "verifie ton email" dans le dashboard tant
    # que c'est False.
    is_verified: bool = False

    class Config:
        from_attributes = True


class EtudiantUpdate(BaseModel):
    nom_complet: str | None = None
    email: str | None = None
    mot_de_passe: str | None = None
    niveau_actuel: str | None = None
    langue_preferee: Langue | None = None


class EtudiantLanguageUpdate(BaseModel):
    langue_preferee: Langue = Field("en", description="Preferred UI and learning language.")


class LoginRequest(BaseModel):
    email: str
    mot_de_passe: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ============================================================
# Phase 3 : verification email + reset password
# ============================================================
class EmailRequest(BaseModel):
    """Body pour /auth/request-verification et /auth/forgot-password.

    On accepte juste un email. Volontairement on ne demande PAS le mot de
    passe : si l'utilisateur a oublie son mot de passe il ne peut pas le
    fournir, et meme pour la verification c'est inutile (on identifie par
    email).
    """
    email: str


class ResetPasswordRequest(BaseModel):
    """Body pour /auth/reset-password : token + nouveau mot de passe."""
    token: str
    new_password: str = Field(..., min_length=8, description="Nouveau mot de passe (min 8 caracteres)")


class MessageResponse(BaseModel):
    """Reponse generique 'message' pour les endpoints qui ne retournent
    pas de donnees structurees."""
    message: str
    detail: str | None = None
