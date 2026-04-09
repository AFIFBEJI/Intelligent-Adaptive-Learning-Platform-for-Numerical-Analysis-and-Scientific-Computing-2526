from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class QuestionSchema(BaseModel):
    """Schema for a quiz question."""
    id: int
    question: str
    type: str  # multiple_choice, short_answer, true_false
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    points: int = 1


class QuizCreate(BaseModel):
    """Schema for creating a new quiz."""
    titre: str
    module: str
    difficulte: str  # facile, moyen, difficile
    questions: List[Dict[str, Any]]


class QuizResponse(BaseModel):
    """Schema for returning quiz information."""
    id: int
    titre: str
    module: str
    difficulte: str
    questions: List[Dict[str, Any]]
    date_creation: datetime

    class Config:
        from_attributes = True


class QuizResultCreate(BaseModel):
    """Schema for submitting quiz results."""
    score: float
    temps_reponse: int
    reponses: Optional[Any] = None


class QuizResultResponse(BaseModel):
    """Schema for returning quiz result information."""
    id: int
    etudiant_id: int
    quiz_id: int
    score: float
    temps_reponse: int
    reponses: Optional[Dict[str, Any]] = None
    date_tentative: datetime

    class Config:
        from_attributes = True
