from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class Quiz(Base):
    """
    Quiz model storing quiz information and questions.
    """
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False)
    module = Column(String(255), nullable=False, index=True)
    difficulte = Column(String(50), nullable=False)  # facile, moyen, difficile
    questions = Column(JSON, nullable=False)  # Array of question objects
    date_creation = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    resultats = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz(id={self.id}, titre={self.titre}, module={self.module})>"


class QuizResult(Base):
    """
    Quiz result model storing student quiz attempts.
    """
    __tablename__ = "quiz_resultats"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id", ondelete="CASCADE"), nullable=False, index=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)  # 0-100
    temps_reponse = Column(Integer, nullable=False)  # in seconds
    reponses = Column(JSON, nullable=True)  # Detailed student answers
    date_tentative = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    # Relationships
    quiz = relationship("Quiz", back_populates="resultats")

    def __repr__(self):
        return f"<QuizResult(id={self.id}, etudiant_id={self.etudiant_id}, quiz_id={self.quiz_id}, score={self.score})>"
