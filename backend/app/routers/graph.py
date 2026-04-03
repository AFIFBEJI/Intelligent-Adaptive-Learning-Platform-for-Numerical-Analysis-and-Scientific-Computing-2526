from fastapi import APIRouter, HTTPException
from app.graph.neo4j_connection import neo4j_conn

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/health")
def graph_health():
    """Vérifie la connexion à Neo4j"""
    try:
        with neo4j_conn.get_session() as session:
            session.run("RETURN 1 AS ok").single()
        return {"status": "connected", "database": "neo4j"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Neo4j inaccessible: {str(e)}")


@router.get("/modules")
def get_modules():
    """Retourne tous les modules du knowledge graph"""
    with neo4j_conn.get_session() as session:
        result = session.run(
            "MATCH (m:Module) RETURN m.id AS id, m.name AS name, m.description AS description ORDER BY m.name"
        )
        return [dict(record) for record in result]


@router.get("/modules/{module_id}/concepts")
def get_module_concepts(module_id: str):
    """Retourne les concepts d'un module"""
    with neo4j_conn.get_session() as session:
        result = session.run(
            """
            MATCH (m:Module {id: $module_id})-[:COVERS]->(c:Concept)
            RETURN c.id AS id, c.name AS name, c.description AS description, c.difficulty AS difficulty
            ORDER BY c.difficulty, c.name
            """,
            module_id=module_id
        )
        concepts = [dict(record) for record in result]
        if not concepts:
            raise HTTPException(status_code=404, detail=f"Module '{module_id}' introuvable ou sans concepts")
        return concepts


@router.get("/concepts/{concept_id}/prerequisites")
def get_prerequisites(concept_id: str):
    """Retourne les prérequis d'un concept"""
    with neo4j_conn.get_session() as session:
        result = session.run(
            """
            MATCH (c:Concept {id: $concept_id})-[:REQUIRES]->(prereq:Concept)
            RETURN prereq.id AS id, prereq.name AS name, prereq.difficulty AS difficulty
            ORDER BY prereq.difficulty
            """,
            concept_id=concept_id
        )
        return [dict(record) for record in result]


@router.get("/concepts/{concept_id}/resources")
def get_concept_resources(concept_id: str):
    """Retourne les ressources pédagogiques d'un concept"""
    with neo4j_conn.get_session() as session:
        result = session.run(
            """
            MATCH (c:Concept {id: $concept_id})-[:REMEDIATES_TO]->(r:Resource)
            RETURN r.id AS id, r.title AS title, r.type AS type, r.url AS url, r.duration AS duration
            """,
            concept_id=concept_id
        )
        resources = [dict(record) for record in result]
        if not resources:
            raise HTTPException(status_code=404, detail=f"Concept '{concept_id}' introuvable ou sans ressources")
        return resources


@router.get("/stats")
def get_graph_stats():
    """Statistiques globales du knowledge graph"""
    with neo4j_conn.get_session() as session:
        stats = {}
        for label in ["Module", "Concept", "Resource"]:
            result = session.run(f"MATCH (n:{label}) RETURN count(n) AS count")
            stats[label.lower() + "s"] = result.single()["count"]
        for rel in ["COVERS", "REQUIRES", "REMEDIATES_TO"]:
            result = session.run(f"MATCH ()-[r:{rel}]->() RETURN count(r) AS count")
            stats[rel.lower()] = result.single()["count"]
        return stats
