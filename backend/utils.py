from passlib.context import CryptContext

# On dit à Passlib d'utiliser l'algorithme très puissant "bcrypt"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hacher_mot_de_passe(mot_de_passe: str):
    """Prend un mot de passe en clair et retourne une version indéchiffrable."""
    return pwd_context.hash(mot_de_passe)




