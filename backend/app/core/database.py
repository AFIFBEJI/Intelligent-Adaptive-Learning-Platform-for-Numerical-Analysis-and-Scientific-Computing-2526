from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings

# URL lue depuis .env - le mot de passe n'est plus visible dans le code!
settings = get_settings()

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Ouvre une connexion et la ferme automatiquement après chaque requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crée les tables dans PostgreSQL au démarrage si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)

    