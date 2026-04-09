from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime, timezone
from app.core.database import Base


class ConceptMastery(Base):
    """
    Concept mastery model tracking student progress on individual concepts.
    Links to Neo4j concept nodes.
    """
    __tablename__ = "concept_mastery"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_neo4j_id = Column(String(255), nullable=False, index=True)  # ID of concept in Neo4j
    niveau_maitrise = Column(Float, default=0.0, nullable=False)  # 0-100
    derniere_mise_a_jour = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Ensure one mastery record per student-concept pair
    __table_args__ = (
        UniqueConstraint("etudiant_id", "concept_neo4j_id", name="unique_student_concept"),
    )

    def __repr__(self):
        return f"<ConceptMastery(id={self.id}, etudiant_id={self.etudiant_id}, concept={self.concept_neo4j_id}, niveau={self.niveau_maitrise})>"
