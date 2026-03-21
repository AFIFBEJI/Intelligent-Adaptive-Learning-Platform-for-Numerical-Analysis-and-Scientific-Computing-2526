from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# On ajoute explicitement +psycopg2 dans l'URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:monmotdepasse123@localhost:5433/adaptive_learning"

# Création du moteur
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La nouvelle bonne pratique pour SQLAlchemy 2.0
Base = declarative_base()

# --- TEST DE CONNEXION SÉCURISÉ ---
if __name__ == "__main__":
    try:
        print("Tentative de connexion à la base de données...")
        connexion = engine.connect()
        print("🎉 SUCCÈS TOTAL : Python est bien connecté à PostgreSQL dans Docker !")
        connexion.close()
    except Exception as e:
        print("❌ ERREUR : La base de données est injoignable.")
        print("Détail de l'erreur (sans plantage) :", repr(e))