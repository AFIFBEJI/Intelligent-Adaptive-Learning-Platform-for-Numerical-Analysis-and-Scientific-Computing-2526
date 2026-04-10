from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.quiz import Quiz, QuizResult
from app.models.mastery import ConceptMastery
from app.schemas.quiz import (
    QuizCreate,
    QuizResponse,
    QuizResultCreate,
    QuizResultResponse,
)

router = APIRouter(prefix="/quiz", tags=["quiz"])

# ============================================================
# Mapping concept Neo4j → module quiz
# ============================================================
MODULE_CONCEPT_MAP = {
    "Interpolation": [
        "concept_polynomial_basics", "concept_lagrange",
        "concept_divided_differences", "concept_newton_interpolation",
        "concept_spline_interpolation"
    ],
    "Intégration Numérique": [
        "concept_riemann_sums", "concept_definite_integrals",
        "concept_trapezoidal", "concept_simpson",
        "concept_gaussian_quadrature"
    ],
    "EDOs": [
        "concept_initial_value", "concept_taylor_series",
        "concept_euler", "concept_improved_euler",
        "concept_rk4"
    ],
}

DIFFICULTY_CONCEPT_MAP = {
    "Interpolation": {
        "facile": "concept_polynomial_basics",
        "moyen": "concept_lagrange",
        "difficile": "concept_spline_interpolation",
    },
    "Intégration Numérique": {
        "facile": "concept_riemann_sums",
        "moyen": "concept_trapezoidal",
        "difficile": "concept_gaussian_quadrature",
    },
    "EDOs": {
        "facile": "concept_initial_value",
        "moyen": "concept_euler",
        "difficile": "concept_rk4",
    },
}


def update_mastery(db: Session, etudiant_id: int, concept_id: str, score: float):
    """Met à jour le niveau de maîtrise d'un concept pour un étudiant."""
    mastery = db.query(ConceptMastery).filter(
        ConceptMastery.etudiant_id == etudiant_id,
        ConceptMastery.concept_neo4j_id == concept_id
    ).first()

    if mastery:
        # Moyenne pondérée : 60% ancien + 40% nouveau score
        mastery.niveau_maitrise = round(mastery.niveau_maitrise * 0.6 + score * 0.4, 1)
        mastery.derniere_mise_a_jour = datetime.now(timezone.utc)
    else:
        mastery = ConceptMastery(
            etudiant_id=etudiant_id,
            concept_neo4j_id=concept_id,
            niveau_maitrise=round(score, 1),
            derniere_mise_a_jour=datetime.now(timezone.utc)
        )
        db.add(mastery)


@router.post("/", response_model=QuizResponse)
def create_quiz(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Créer un nouveau quiz."""
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
    """Liste les quiz avec filtrage optionnel."""
    query = db.query(Quiz)
    if module:
        query = query.filter(Quiz.module == module)
    if difficulte:
        query = query.filter(Quiz.difficulte == difficulte)
    return query.offset(skip).limit(limit).all()


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Récupérer un quiz par son ID."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.post("/{quiz_id}/submit", response_model=QuizResultResponse)
def submit_quiz(
    quiz_id: int,
    result_data: QuizResultCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Soumettre un quiz et mettre à jour la maîtrise automatiquement."""
    # 1. Vérifier que le quiz existe
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # 2. Sauvegarder le résultat
    quiz_result = QuizResult(
        etudiant_id=current_user_id,
        quiz_id=quiz_id,
        score=result_data.score,
        temps_reponse=result_data.temps_reponse,
        reponses=result_data.reponses
    )
    db.add(quiz_result)

    # 3. ALGORITHME ADAPTATIF : mettre à jour la maîtrise
    module = quiz.module
    difficulte = quiz.difficulte
    score = result_data.score

    # Trouver le concept principal lié à ce quiz
    concept_id = DIFFICULTY_CONCEPT_MAP.get(module, {}).get(difficulte)
    if concept_id:
        update_mastery(db, current_user_id, concept_id, score)

    # Si quiz mixte (difficile), mettre à jour tous les concepts du module
    if difficulte == "difficile" and module in MODULE_CONCEPT_MAP:
        for cid in MODULE_CONCEPT_MAP[module]:
            if cid != concept_id:
                # Impact réduit (20%) pour les concepts non-ciblés
                update_mastery(db, current_user_id, cid, score * 0.5)

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
    """Résultats d'un étudiant (seulement les siens)."""
    if current_user_id != etudiant_id:
        raise HTTPException(status_code=403, detail="You can only view your own results")
    return db.query(QuizResult).filter(
        QuizResult.etudiant_id == etudiant_id
    ).offset(skip).limit(limit).all()


@router.get("/next/{etudiant_id}", response_model=QuizResponse)
def get_next_quiz(
    etudiant_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Recommande le prochain quiz adapté au niveau de l'étudiant."""
    if current_user_id != etudiant_id:
        raise HTTPException(status_code=403, detail="Accès interdit")

    # Récupérer la maîtrise
    mastery_records = db.query(ConceptMastery).filter(
        ConceptMastery.etudiant_id == etudiant_id
    ).all()
    mastery_dict = {m.concept_neo4j_id: m.niveau_maitrise for m in mastery_records}

    # Chercher le meilleur quiz à proposer
    all_quizzes = db.query(Quiz).filter(Quiz.module != "Prérequis").all()

    # Priorité 1 : quiz facile d'un module pas encore commencé
    for quiz in all_quizzes:
        if quiz.difficulte == "facile":
            concepts = MODULE_CONCEPT_MAP.get(quiz.module, [])
            if concepts and all(mastery_dict.get(c, 0) == 0 for c in concepts):
                return quiz

    # Priorité 2 : quiz moyen d'un module avec maîtrise entre 30-69%
    for quiz in all_quizzes:
        if quiz.difficulte == "moyen":
            concept_id = DIFFICULTY_CONCEPT_MAP.get(quiz.module, {}).get("facile")
            if concept_id and 30 <= mastery_dict.get(concept_id, 0) < 70:
                return quiz

    # Priorité 3 : quiz difficile d'un module avec maîtrise >= 70%
    for quiz in all_quizzes:
        if quiz.difficulte == "difficile" and "Mixte" not in quiz.titre:
            concept_id = DIFFICULTY_CONCEPT_MAP.get(quiz.module, {}).get("moyen")
            if concept_id and mastery_dict.get(concept_id, 0) >= 70:
                return quiz

    # Fallback : quiz diagnostique
    diag = db.query(Quiz).filter(Quiz.module == "Prérequis").first()
    if diag:
        return diag

    raise HTTPException(status_code=404, detail="Aucun quiz disponible")