from datetime import datetime

from pydantic import BaseModel


class MasteryResponse(BaseModel):
    """Schema for returning concept mastery information."""
    id: int
    etudiant_id: int
    concept_neo4j_id: str
    niveau_maitrise: float
    derniere_mise_a_jour: datetime

    class Config:
        from_attributes = True


class MasteryUpdate(BaseModel):
    """Schema for updating concept mastery."""
    niveau_maitrise: float


class MasteryCreateOrUpdate(BaseModel):
    """Schema for creating or updating mastery records."""
    concept_neo4j_id: str
    niveau_maitrise: float
