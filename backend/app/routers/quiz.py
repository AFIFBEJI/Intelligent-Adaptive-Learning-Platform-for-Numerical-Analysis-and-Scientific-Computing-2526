from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.quiz import Quiz, QuizResult
from app.schemas.quiz import (
    QuizCreate,
    QuizResponse,
    QuizResultCreate,
    QuizResultResponse,
)

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/", response_model=QuizResponse)
def create_quiz(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    Create a new quiz (admin functionality).

    Args:
        quiz_data: Quiz information
        db: Database session
        current_user_id: Current authenticated user ID

    Returns:
        Created quiz
    """
    nouveau_quiz = Quiz(
        titre=quiz_data.titre,
        module=quiz_data.module,
        difficulte=quiz_data.difficulte,
        questions=quiz_data.questions
    )

    db.add(nouveau_quiz)
    db.commit()
    db.refresh(nouveau_quiz)

    return nouveau_quiz


@router.get("/", response_model=List[QuizResponse])
def list_quiz(
    module: str = None,
    difficulte: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    List all quizzes with optional filtering.

    Args:
        module: Filter by module name
        difficulte: Filter by difficulty level
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user_id: Current authenticated user ID

    Returns:
        List of quizzes
    """
    query = db.query(Quiz)

    if module:
        query = query.filter(Quiz.module == module)

    if difficulte:
        query = query.filter(Quiz.difficulte == difficulte)

    quizzes = query.offset(skip).limit(limit).all()
    return quizzes


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    Get a specific quiz by ID.

    Args:
        quiz_id: Quiz ID
        db: Database session
        current_user_id: Current authenticated user ID

    Returns:
        Quiz information
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    return quiz


@router.post("/{quiz_id}/submit", response_model=QuizResultResponse)
def submit_quiz(
    quiz_id: int,
    result_data: QuizResultCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    Submit quiz answers and save the result.

    Args:
        quiz_id: Quiz ID
        result_data: Quiz result data
        db: Database session
        current_user_id: Current authenticated user ID

    Returns:
        Quiz result
    """
    # Verify quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    # Create quiz result
    quiz_result = QuizResult(
        etudiant_id=current_user_id,
        quiz_id=quiz_id,
        score=result_data.score,
        temps_reponse=result_data.temps_reponse,
        reponses=result_data.reponses
    )

    db.add(quiz_result)
    db.commit()
    db.refresh(quiz_result)

    return quiz_result


@router.get("/results/{etudiant_id}", response_model=List[QuizResultResponse])
def get_student_results(
    etudiant_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    Get all quiz results for a student.
    Students can only view their own results.

    Args:
        etudiant_id: Student ID
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user_id: Current authenticated user ID

    Returns:
        List of quiz results
    """
    # Check authorization
    if current_user_id != etudiant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own results"
        )

    results = db.query(QuizResult).filter(
        QuizResult.etudiant_id == etudiant_id
    ).offset(skip).limit(limit).all()

    return results
