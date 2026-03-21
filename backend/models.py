from sqlalchemy import Column, Integer, String
from database import Base

class Etudiant(Base):
    __tablename__ = "etudiants"

    id = Column(Integer, primary_key=True, index=True)
    nom_complet = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    mot_de_passe = Column(String)
    niveau_actuel = Column(String, default="Débutant")