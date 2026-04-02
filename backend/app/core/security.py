from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hacher_mot_de_passe(mot_de_passe: str) -> str:
    """Transforme le mot de passe en code indéchiffrable."""
    return pwd_context.hash(mot_de_passe)


def verifier_mot_de_passe(mot_de_passe: str, mot_de_passe_hache: str) -> bool:
    """Vérifie si le mot de passe correspond au hash stocké."""
    return pwd_context.verify(mot_de_passe, mot_de_passe_hache)



def creer_token(data: dict) -> str:
    """Crée un token JWT pour garder l'étudiant connecté."""
    to_encode = data.copy()
    to_encode["sub"] = str(to_encode["sub"])  # ← AJOUTER CETTE LIGNE
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    """Vérifie le token JWT et retourne l'ID de l'étudiant connecté."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        return int(user_id)  # ← CHANGER ICI: int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")