from neo4j import GraphDatabase
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """Singleton pour la connexion Neo4j"""
    _instance = None
    _driver = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        if self._driver is None:
            settings = get_settings()
            self._driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            logger.info(f"✅ Connecté à Neo4j : {settings.NEO4J_URI}")
        return self._driver

    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None

    def get_session(self):
        return self.connect().session()


# Instance globale (Singleton)
neo4j_conn = Neo4jConnection()
