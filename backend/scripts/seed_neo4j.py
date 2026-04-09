#!/usr/bin/env python3
"""
Neo4j Seed Script for Adaptive Learning Platform PFE
Populates the knowledge graph with numerical analysis concepts
"""

from neo4j import GraphDatabase
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Neo4jSeeder:
    """Handles Neo4j database seeding and graph population"""

    def __init__(self, uri, user, password):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = None

    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()

    def clear_database(self):
        """Clear all existing nodes and relationships"""
        logger.info("Clearing existing data...")
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("Database cleared successfully")

    def create_constraints(self):
        """Create database constraints"""
        logger.info("Creating constraints...")
        with self.driver.session() as session:
            # Unique constraints for IDs
            session.run("CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE")
            session.run("CREATE CONSTRAINT module_id IF NOT EXISTS FOR (m:Module) REQUIRE m.id IS UNIQUE")
            session.run("CREATE CONSTRAINT resource_id IF NOT EXISTS FOR (r:Resource) REQUIRE r.id IS UNIQUE")
        logger.info("Constraints created")

    def create_modules(self):
        """Create Module nodes"""
        logger.info("Creating Module nodes...")
        modules = [
            {
                "id": "module_interpolation",
                "name": "Interpolation",
                "description": "Techniques for estimating values between known data points using polynomial methods"
            },
            {
                "id": "module_integration",
                "name": "Numerical Integration",
                "description": "Methods for computing definite integrals numerically"
            },
            {
                "id": "module_odes",
                "name": "Ordinary Differential Equations (ODEs)",
                "description": "Numerical methods for solving differential equations with initial conditions"
            }
        ]

        with self.driver.session() as session:
            for module in modules:
                session.run(
                    """
                    CREATE (m:Module {
                        id: $id,
                        name: $name,
                        description: $description
                    })
                    """,
                    id=module["id"],
                    name=module["name"],
                    description=module["description"]
                )
        logger.info(f"Created {len(modules)} modules")
        return modules

    def create_concepts(self):
        """Create Concept nodes for all three modules"""
        logger.info("Creating Concept nodes...")

        concepts = [
            # Module 1: Interpolation
            {
                "id": "concept_polynomial_basics",
                "name": "Polynomial Basics",
                "description": "Fundamental concepts of polynomial functions and their properties",
                "difficulty": "beginner",
                "module_id": "module_interpolation"
            },
            {
                "id": "concept_lagrange",
                "name": "Lagrange Interpolation",
                "description": "Method of constructing polynomial from known values using Lagrange basis polynomials",
                "difficulty": "intermediate",
                "module_id": "module_interpolation"
            },
            {
                "id": "concept_divided_differences",
                "name": "Divided Differences",
                "description": "Technique for computing coefficients in Newton form of interpolating polynomial",
                "difficulty": "intermediate",
                "module_id": "module_interpolation"
            },
            {
                "id": "concept_newton_interpolation",
                "name": "Newton Interpolation",
                "description": "Constructing interpolating polynomials using divided differences",
                "difficulty": "intermediate",
                "module_id": "module_interpolation"
            },
            {
                "id": "concept_spline_interpolation",
                "name": "Spline Interpolation",
                "description": "Using piecewise polynomial functions for smooth interpolation",
                "difficulty": "advanced",
                "module_id": "module_interpolation"
            },

            # Module 2: Numerical Integration
            {
                "id": "concept_riemann_sums",
                "name": "Riemann Sums",
                "description": "Approximating integrals using sums of rectangle areas",
                "difficulty": "beginner",
                "module_id": "module_integration"
            },
            {
                "id": "concept_definite_integrals",
                "name": "Definite Integrals",
                "description": "Theoretical foundations of definite integrals and their properties",
                "difficulty": "beginner",
                "module_id": "module_integration"
            },
            {
                "id": "concept_trapezoidal",
                "name": "Trapezoidal Rule",
                "description": "Numerical integration method using trapezoid approximations",
                "difficulty": "intermediate",
                "module_id": "module_integration"
            },
            {
                "id": "concept_simpson",
                "name": "Simpson's Rule",
                "description": "More accurate integration method using parabolic approximations",
                "difficulty": "intermediate",
                "module_id": "module_integration"
            },
            {
                "id": "concept_gaussian_quadrature",
                "name": "Gaussian Quadrature",
                "description": "Advanced integration method using optimal node placement and weights",
                "difficulty": "advanced",
                "module_id": "module_integration"
            },

            # Module 3: ODEs
            {
                "id": "concept_initial_value",
                "name": "Initial Value Problems",
                "description": "Differential equations with specified initial conditions",
                "difficulty": "beginner",
                "module_id": "module_odes"
            },
            {
                "id": "concept_taylor_series",
                "name": "Taylor Series",
                "description": "Series expansion of functions and its application to numerical methods",
                "difficulty": "intermediate",
                "module_id": "module_odes"
            },
            {
                "id": "concept_euler",
                "name": "Euler's Method",
                "description": "Simple first-order method for solving differential equations numerically",
                "difficulty": "intermediate",
                "module_id": "module_odes"
            },
            {
                "id": "concept_improved_euler",
                "name": "Improved Euler (Heun's Method)",
                "description": "Second-order method improving upon Euler's method accuracy",
                "difficulty": "intermediate",
                "module_id": "module_odes"
            },
            {
                "id": "concept_rk4",
                "name": "Runge-Kutta Method (RK4)",
                "description": "Fourth-order method providing excellent accuracy for ODE solving",
                "difficulty": "advanced",
                "module_id": "module_odes"
            }
        ]

        with self.driver.session() as session:
            for concept in concepts:
                module_id = concept.pop("module_id")
                session.run(
                    """
                    CREATE (c:Concept {
                        id: $id,
                        name: $name,
                        description: $description,
                        difficulty: $difficulty
                    })
                    """,
                    **concept
                )
        logger.info(f"Created {len(concepts)} concepts")
        return concepts

    def create_resources(self):
        """Create Resource nodes"""
        logger.info("Creating Resource nodes...")

        resources = [
            {
                "id": "resource_lagrange_video",
                "name": "Lagrange Interpolation Video Tutorial",
                "type": "video",
                "url": "https://www.example.com/lagrange-interpolation"
            },
            {
                "id": "resource_newton_exercise",
                "name": "Newton Interpolation Practice Problems",
                "type": "exercise",
                "url": "https://www.example.com/newton-exercises"
            },
            {
                "id": "resource_spline_tutorial",
                "name": "Spline Interpolation Tutorial",
                "type": "tutorial",
                "url": "https://www.example.com/spline-tutorial"
            },
            {
                "id": "resource_trapezoidal_video",
                "name": "Trapezoidal Rule Video",
                "type": "video",
                "url": "https://www.example.com/trapezoidal-rule"
            },
            {
                "id": "resource_simpson_exercise",
                "name": "Simpson's Rule Exercises",
                "type": "exercise",
                "url": "https://www.example.com/simpson-exercises"
            },
            {
                "id": "resource_gaussian_tutorial",
                "name": "Gaussian Quadrature Deep Dive",
                "type": "tutorial",
                "url": "https://www.example.com/gaussian-quadrature"
            },
            {
                "id": "resource_euler_video",
                "name": "Euler's Method Explained",
                "type": "video",
                "url": "https://www.example.com/euler-method"
            },
            {
                "id": "resource_rk4_exercise",
                "name": "RK4 Implementation Exercises",
                "type": "exercise",
                "url": "https://www.example.com/rk4-exercises"
            }
        ]

        with self.driver.session() as session:
            for resource in resources:
                session.run(
                    """
                    CREATE (r:Resource {
                        id: $id,
                        name: $name,
                        type: $type,
                        url: $url
                    })
                    """,
                    **resource
                )
        logger.info(f"Created {len(resources)} resources")
        return resources

    def create_module_covers_relationships(self):
        """Create Module-COVERS-Concept relationships"""
        logger.info("Creating Module COVERS Concept relationships...")

        relationships = [
            # Module 1: Interpolation
            ("module_interpolation", "concept_polynomial_basics"),
            ("module_interpolation", "concept_lagrange"),
            ("module_interpolation", "concept_divided_differences"),
            ("module_interpolation", "concept_newton_interpolation"),
            ("module_interpolation", "concept_spline_interpolation"),

            # Module 2: Integration
            ("module_integration", "concept_riemann_sums"),
            ("module_integration", "concept_definite_integrals"),
            ("module_integration", "concept_trapezoidal"),
            ("module_integration", "concept_simpson"),
            ("module_integration", "concept_gaussian_quadrature"),

            # Module 3: ODEs
            ("module_odes", "concept_initial_value"),
            ("module_odes", "concept_taylor_series"),
            ("module_odes", "concept_euler"),
            ("module_odes", "concept_improved_euler"),
            ("module_odes", "concept_rk4")
        ]

        with self.driver.session() as session:
            for module_id, concept_id in relationships:
                session.run(
                    """
                    MATCH (m:Module {id: $module_id})
                    MATCH (c:Concept {id: $concept_id})
                    CREATE (m)-[:COVERS]->(c)
                    """,
                    module_id=module_id,
                    concept_id=concept_id
                )
        logger.info(f"Created {len(relationships)} Module-COVERS-Concept relationships")

    def create_concept_requires_relationships(self):
        """Create Concept-REQUIRES-Concept prerequisite relationships"""
        logger.info("Creating Concept REQUIRES relationships...")

        prerequisites = [
            # Module 1: Interpolation
            ("concept_polynomial_basics", "concept_lagrange"),
            ("concept_polynomial_basics", "concept_newton_interpolation"),
            ("concept_divided_differences", "concept_newton_interpolation"),
            ("concept_lagrange", "concept_spline_interpolation"),

            # Module 2: Integration
            ("concept_riemann_sums", "concept_trapezoidal"),
            ("concept_definite_integrals", "concept_trapezoidal"),
            ("concept_trapezoidal", "concept_simpson"),
            ("concept_simpson", "concept_gaussian_quadrature"),

            # Module 3: ODEs
            ("concept_initial_value", "concept_euler"),
            ("concept_taylor_series", "concept_euler"),
            ("concept_euler", "concept_improved_euler"),
            ("concept_improved_euler", "concept_rk4")
        ]

        with self.driver.session() as session:
            for prerequisite_id, dependent_id in prerequisites:
                session.run(
                    """
                    MATCH (c1:Concept {id: $prerequisite_id})
                    MATCH (c2:Concept {id: $dependent_id})
                    CREATE (c2)-[:REQUIRES]->(c1)
                    """,
                    prerequisite_id=prerequisite_id,
                    dependent_id=dependent_id
                )
        logger.info(f"Created {len(prerequisites)} Concept REQUIRES relationships")

    def create_remediation_relationships(self):
        """Create Concept-REMEDIATES_TO-Resource relationships"""
        logger.info("Creating Concept REMEDIATES_TO Resource relationships...")

        remediations = [
            ("concept_lagrange", "resource_lagrange_video"),
            ("concept_newton_interpolation", "resource_newton_exercise"),
            ("concept_spline_interpolation", "resource_spline_tutorial"),
            ("concept_trapezoidal", "resource_trapezoidal_video"),
            ("concept_simpson", "resource_simpson_exercise"),
            ("concept_gaussian_quadrature", "resource_gaussian_tutorial"),
            ("concept_euler", "resource_euler_video"),
            ("concept_rk4", "resource_rk4_exercise")
        ]

        with self.driver.session() as session:
            for concept_id, resource_id in remediations:
                session.run(
                    """
                    MATCH (c:Concept {id: $concept_id})
                    MATCH (r:Resource {id: $resource_id})
                    CREATE (c)-[:REMEDIATES_TO]->(r)
                    """,
                    concept_id=concept_id,
                    resource_id=resource_id
                )
        logger.info(f"Created {len(remediations)} Concept REMEDIATES_TO Resource relationships")

    def verify_graph(self):
        """Verify the created graph and print statistics"""
        logger.info("\n" + "="*60)
        logger.info("GRAPH VERIFICATION")
        logger.info("="*60)

        with self.driver.session() as session:
            # Count nodes by type (separate queries - compatible with Neo4j 5 Community)
            total_nodes = 0
            logger.info("\nNode Counts:")
            for label in ["Module", "Concept", "Resource"]:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) AS count")
                count = result.single()["count"]
                total_nodes += count
                logger.info(f"  - {label}: {count}")

            # Count relationships by type (without APOC)
            logger.info("\nRelationship Counts:")
            total_rels = 0
            for rel_type in ["COVERS", "REQUIRES", "REMEDIATES_TO"]:
                result = session.run(f"MATCH ()-[r:{rel_type}]->() RETURN count(r) AS count")
                count = result.single()["count"]
                total_rels += count
                logger.info(f"  - {rel_type}: {count}")
            logger.info(f"\nTotal Relationships: {total_rels}")

            # Module Coverage
            logger.info("\nModule Coverage:")
            module_coverage = session.run(
                """
                MATCH (m:Module)-[:COVERS]->(c:Concept)
                RETURN m.name AS module_name, count(c) AS concept_count
                ORDER BY module_name
                """
            )

            for record in module_coverage:
                logger.info(f"  - {record['module_name']}: {record['concept_count']} concepts")

            logger.info("\n" + "="*60)
            logger.info(f"Total Nodes Created: {total_nodes}")
            logger.info("="*60 + "\n")

    def seed(self):
        """Execute the complete seeding process"""
        try:
            logger.info("Starting Neo4j database seeding...")
            self.clear_database()
            self.create_constraints()
            self.create_modules()
            self.create_concepts()
            self.create_resources()
            self.create_module_covers_relationships()
            self.create_concept_requires_relationships()
            self.create_remediation_relationships()
            self.verify_graph()
            logger.info("Seeding completed successfully!")
        except Exception as e:
            logger.error(f"Error during seeding: {e}")
            raise
        finally:
            self.close()


def main():
    """
    Point d'entrée principal.
    Les paramètres de connexion sont lus depuis le fichier .env
    """
    import os
    import sys
    from dotenv import load_dotenv

    # Charger les variables depuis .env (2 niveaux au-dessus : backend/scripts/ → racine)
    dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
    load_dotenv(dotenv_path)

    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

    # Vérifier que toutes les variables sont présentes
    if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
        logger.error("❌ Variables manquantes dans .env : NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD")
        logger.error(f"   Fichier .env cherché : {os.path.abspath(dotenv_path)}")
        sys.exit(1)

    logger.info(f"Connexion à Neo4j : {NEO4J_URI} avec l'utilisateur {NEO4J_USER}")

    seeder = Neo4jSeeder(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    seeder.seed()


if __name__ == "__main__":
    main()
