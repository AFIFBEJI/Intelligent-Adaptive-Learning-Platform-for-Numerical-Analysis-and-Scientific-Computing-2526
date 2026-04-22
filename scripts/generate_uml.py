"""
Generate 5 high-fidelity UML diagrams for Phase 1.

Uses Graphviz with HTML-like labels to produce professional-looking
UML diagrams. Content reflects the actual source code:
  - models/{etudiant,mastery,quiz,tutor}.py  -> class diagram
  - routers/{auth,quiz,graph,tutor,etudiants}.py -> use cases
  - docker/docker-compose.yml  -> deployment diagram
  - actual login + quiz submission flows -> sequence diagrams

Outputs PNG + SVG into docs/uml/.
"""
import shutil
import tempfile
from pathlib import Path
import graphviz as gv

ROOT = Path("/sessions/blissful-great-pascal/mnt/Intelligent_Adaptive_Learning_Platform_for_Numerical_Analysis_and_Scientific_Computing-2526")
UML_DIR = ROOT / "docs" / "uml"
UML_DIR.mkdir(parents=True, exist_ok=True)


def render(g, name):
    """Render to a temp dir (mount has no FIFO/fsync), then copy out."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_p = Path(tmp)
        g.render(str(tmp_p / name), format="png", cleanup=True)
        g.render(str(tmp_p / name), format="svg", cleanup=True)
        shutil.copy(tmp_p / f"{name}.png", UML_DIR / f"{name}.png")
        shutil.copy(tmp_p / f"{name}.svg", UML_DIR / f"{name}.svg")
    size = (UML_DIR / f"{name}.png").stat().st_size
    print(f"  [OK] {name}.png ({size:,} bytes) + .svg")


# =======================================================================
# 1. USE CASE DIAGRAM — based on the real routers
# =======================================================================
def gen_use_case():
    g = gv.Digraph("use_case", filename="use_case")
    g.attr(rankdir="LR", bgcolor="white", pad="0.4",
           label="<<B>Use Case Diagram — Intelligent Adaptive Learning Platform (Phase 1)</B>>",
           labelloc="t", fontname="Helvetica", fontsize="16")
    g.attr("node", fontname="Helvetica")

    # Actors (stick-figure style via shape=none + image-like labels)
    with g.subgraph(name="cluster_actors") as s:
        s.attr(style="invis")
        s.node("student", shape="none", width="1.2",
               label=(
                   "<<TABLE BORDER=\"0\" CELLBORDER=\"0\"><TR><TD>"
                   "<FONT POINT-SIZE=\"40\">&#128100;</FONT></TD></TR>"
                   "<TR><TD><B>Étudiant</B></TD></TR></TABLE>>"))
        s.node("admin", shape="none",
               label=(
                   "<<TABLE BORDER=\"0\" CELLBORDER=\"0\"><TR><TD>"
                   "<FONT POINT-SIZE=\"40\">&#128104;&#8205;&#127979;</FONT></TD></TR>"
                   "<TR><TD><B>Enseignant / Admin</B></TD></TR></TABLE>>"))

    # System boundary — all use cases inside
    with g.subgraph(name="cluster_system") as s:
        s.attr(label="Adaptive Learning Platform", style="rounded,dashed",
               color="#2c3e50", fontsize="13", fontname="Helvetica-Bold",
               bgcolor="#f8fafc")
        uc_style = dict(shape="ellipse", style="filled", fillcolor="#dbeafe",
                        color="#1e40af", fontsize="11")
        # Authentication
        s.node("uc_register", "S'inscrire\n(POST /auth/register)", **uc_style)
        s.node("uc_login",    "Se connecter\n(POST /auth/login)",   **uc_style)
        s.node("uc_profile",  "Consulter mon profil\n(GET /auth/me)", **uc_style)
        # Graph / learning path
        s.node("uc_modules",  "Parcourir les modules\n(GET /graph/modules)", **uc_style)
        s.node("uc_path",     "Obtenir mon parcours\nadaptatif\n(GET /graph/learning-path)", **uc_style)
        s.node("uc_content",  "Consulter un concept\n(GET /graph/concepts/{id}/adaptive-content)", **uc_style)
        # Quiz
        s.node("uc_takequiz", "Passer un quiz\n(GET /quiz/{id})",   **uc_style)
        s.node("uc_submit",   "Soumettre mes réponses\n(POST /quiz/{id}/submit)", **uc_style)
        s.node("uc_results",  "Voir mes résultats\n(GET /quiz/results)", **uc_style)
        s.node("uc_remediate","Recevoir une remédiation\n(GET /graph/remediation/{id})", **uc_style)
        s.node("uc_next",     "Obtenir le prochain quiz\n(GET /quiz/next/{id})", **uc_style)
        # Tutor IA
        s.node("uc_tutor",    "Interroger le tuteur IA\n(POST /tutor/ask)", **uc_style)
        # Admin-only
        s.node("uc_seed",     "Seeder le graphe Neo4j\n(scripts/seed_neo4j.py)",
               shape="ellipse", style="filled", fillcolor="#fde68a", color="#b45309", fontsize="11")
        s.node("uc_stats",    "Inspecter les stats du graphe\n(GET /graph/stats)",
               shape="ellipse", style="filled", fillcolor="#fde68a", color="#b45309", fontsize="11")

    # Associations
    for uc in ["uc_register", "uc_login", "uc_profile", "uc_modules",
               "uc_path", "uc_content", "uc_takequiz", "uc_submit",
               "uc_results", "uc_next", "uc_tutor"]:
        g.edge("student", uc, arrowhead="none", color="#1e3a8a")
    for uc in ["uc_seed", "uc_stats", "uc_modules"]:
        g.edge("admin", uc, arrowhead="none", color="#92400e")

    # <<include>> and <<extend>> relationships
    g.edge("uc_submit", "uc_remediate",
           label="«include»", style="dashed", fontsize="9",
           color="#6b7280", fontcolor="#6b7280")
    g.edge("uc_path", "uc_content",
           label="«include»", style="dashed", fontsize="9",
           color="#6b7280", fontcolor="#6b7280")
    g.edge("uc_next", "uc_submit",
           label="«extend»", style="dashed", fontsize="9",
           color="#6b7280", fontcolor="#6b7280")

    render(g, "use_case")


# =======================================================================
# 2. CLASS DIAGRAM — reflects real SQLAlchemy models + Neo4j graph
# =======================================================================
def gen_class_diagram():
    g = gv.Digraph("class_diagram", filename="class_diagram")
    g.attr(rankdir="LR", bgcolor="white", pad="0.4", nodesep="0.7", ranksep="1.0",
           label="<<B>Class Diagram — Domain Model (Phase 1)</B>>",
           labelloc="t", fontname="Helvetica", fontsize="16")
    g.attr("node", shape="none", fontname="Helvetica")

    def cls(name, stereotype, attrs, methods, color="#e0e7ff", border="#3730a3"):
        """Build an HTML-label class box."""
        rows = []
        rows.append(f'<TR><TD BGCOLOR="{border}"><FONT COLOR="white"><I>«{stereotype}»</I></FONT></TD></TR>')
        rows.append(f'<TR><TD BGCOLOR="{color}"><B>{name}</B></TD></TR>')
        if attrs:
            a = "<BR/>".join(f'<FONT POINT-SIZE="10">{a}</FONT>' for a in attrs)
            rows.append(f'<TR><TD ALIGN="LEFT" BALIGN="LEFT">{a}</TD></TR>')
        else:
            rows.append('<TR><TD></TD></TR>')
        if methods:
            m = "<BR/>".join(f'<FONT POINT-SIZE="10">{x}</FONT>' for x in methods)
            rows.append(f'<TR><TD ALIGN="LEFT" BALIGN="LEFT">{m}</TD></TR>')
        else:
            rows.append('<TR><TD></TD></TR>')
        return "<<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\" CELLPADDING=\"4\">" + "".join(rows) + "</TABLE>>"

    # --- PostgreSQL entities (SQLAlchemy) ---
    g.node("Etudiant", cls("Etudiant", "SQLAlchemy Entity", [
        "- id : int [PK]",
        "- nom_complet : str",
        "- email : str [unique]",
        "- mot_de_passe : str(255)  // bcrypt hash",
        "- niveau_actuel : str = 'Débutant'",
        "- is_active : bool = True",
    ], [
        "+ verify_password(pwd) : bool",
        "+ to_response() : EtudiantResponse",
    ]))

    g.node("ConceptMastery", cls("ConceptMastery", "SQLAlchemy Entity", [
        "- id : int [PK]",
        "- etudiant_id : int [FK → Etudiant]",
        "- concept_neo4j_id : str(255)  // link to Neo4j",
        "- niveau_maitrise : float (0-100)",
        "- derniere_mise_a_jour : datetime",
        "  UNIQUE(etudiant_id, concept_neo4j_id)",
    ], [
        "+ update(new_score) : void",
    ]))

    g.node("Quiz", cls("Quiz", "SQLAlchemy Entity", [
        "- id : int [PK]",
        "- titre : str(255)",
        "- module : str(255) [indexed]",
        "- difficulte : str(50)  // facile|moyen|difficile",
        "- questions : JSON",
        "- date_creation : datetime",
    ], [
        "+ grade(answers) : float",
    ]))

    g.node("QuizResult", cls("QuizResult", "SQLAlchemy Entity", [
        "- id : int [PK]",
        "- etudiant_id : int [FK → Etudiant]",
        "- quiz_id : int [FK → Quiz]",
        "- score : float (0-100)",
        "- temps_reponse : int  // seconds",
        "- reponses : JSON",
        "- date_tentative : datetime",
    ], []))

    g.node("TutorSession", cls("TutorSession", "SQLAlchemy Entity", [
        "- id : int [PK]",
        "- etudiant_id : int [FK → Etudiant]",
        "- concept_id : str?  // Neo4j ID",
        "- created_at : datetime",
        "- updated_at : datetime",
    ], [
        "+ add_message(msg) : void",
    ]))

    # --- Neo4j graph nodes ---
    g.node("Module", cls("Module", "Neo4j Node", [
        "- id : str [PK]",
        "- name : str",
        "- order : int",
    ], [], color="#ddd6fe", border="#6d28d9"))

    g.node("Concept", cls("Concept", "Neo4j Node", [
        "- id : str [PK]",
        "- name : str",
        "- difficulty : str",
        "- learning_objectives : [str]",
    ], [], color="#ddd6fe", border="#6d28d9"))

    g.node("Resource", cls("Resource", "Neo4j Node", [
        "- id : str [PK]",
        "- type : str  // pdf | video | notebook | exercise",
        "- url : str",
        "- difficulty : str",
    ], [], color="#ddd6fe", border="#6d28d9"))

    # --- Associations (PostgreSQL) ---
    g.edge("Etudiant", "ConceptMastery",
           label="1    *", arrowhead="odiamond", arrowtail="none", dir="both",
           fontsize="10", color="#1f2937")
    g.edge("Etudiant", "QuizResult",
           label="1    *", arrowhead="odiamond", arrowtail="none", dir="both",
           fontsize="10", color="#1f2937")
    g.edge("Quiz", "QuizResult",
           label="1    *", arrowhead="odiamond", arrowtail="none", dir="both",
           fontsize="10", color="#1f2937")
    g.edge("Etudiant", "TutorSession",
           label="1    *", arrowhead="odiamond", arrowtail="none", dir="both",
           fontsize="10", color="#1f2937")

    # --- Cross-store link (dashed: mastery references Neo4j concept) ---
    g.edge("ConceptMastery", "Concept",
           label="references\n(by string id)", style="dashed",
           arrowhead="vee", fontsize="9", color="#dc2626", fontcolor="#dc2626")
    g.edge("TutorSession", "Concept",
           label="references", style="dashed",
           arrowhead="vee", fontsize="9", color="#dc2626", fontcolor="#dc2626")

    # --- Neo4j relationships ---
    g.edge("Module", "Concept", label="COVERS (15)", fontsize="10",
           color="#6d28d9", fontcolor="#6d28d9")
    g.edge("Concept", "Concept", label="REQUIRES (14)", fontsize="10",
           color="#6d28d9", fontcolor="#6d28d9")
    g.edge("Resource", "Concept", label="REMEDIATES_TO (8)", fontsize="10",
           color="#6d28d9", fontcolor="#6d28d9")

    render(g, "class_diagram")


# =======================================================================
# 3. SEQUENCE DIAGRAM — Login flow (based on routers/auth.py)
# =======================================================================
def gen_sequence_login():
    g = gv.Digraph("sequence_login", filename="sequence_login")
    g.attr(bgcolor="white", pad="0.4", rankdir="LR",
           label="<<B>Sequence Diagram — Login Flow (POST /auth/login)</B>>",
           labelloc="t", fontname="Helvetica", fontsize="16")
    g.attr("node", fontname="Helvetica", shape="box", style="filled")

    # Lifelines (aligned top)
    actors = [
        ("user", "Étudiant\n(Browser)", "#fef3c7"),
        ("fe",   "React SPA\n(LoginPage.tsx)", "#dbeafe"),
        ("api",  "FastAPI\n/auth/login", "#d1fae5"),
        ("sec",  "core/security.py\n(bcrypt + JWT)", "#fce7f3"),
        ("db",   "PostgreSQL\netudiants", "#e0e7ff"),
    ]
    with g.subgraph() as s:
        s.attr(rank="same")
        for n, lbl, col in actors:
            s.node(n, lbl, fillcolor=col, color="#374151")

    # Messages (use invisible nodes as time markers, edges ordered vertically)
    steps = [
        ("user", "fe",  "1: fill (email, pwd) & click Login"),
        ("fe",   "api", "2: POST /auth/login\n(OAuth2PasswordRequestForm)"),
        ("api",  "db",  "3: SELECT * FROM etudiants\nWHERE email = :email"),
        ("db",   "api", "4: Etudiant row (mot_de_passe hash)"),
        ("api",  "sec", "5: verify_password(plain, hash)"),
        ("sec",  "api", "6: True / False"),
        ("api",  "sec", "7: create_access_token({sub: id})"),
        ("sec",  "api", "8: JWT (HS256, 30 min)"),
        ("api",  "fe",  "9: 200 {access_token, token_type: bearer}"),
        ("fe",   "user","10: save token (localStorage)\n→ redirect /dashboard"),
    ]
    for i, (a, b, lbl) in enumerate(steps, start=1):
        g.edge(a, b, label=lbl, fontsize="9", color="#374151",
               penwidth="1.2", constraint="true")

    # Alt path (invalid creds)
    g.edge("sec", "api", label="alt: False → raise HTTPException(401)",
           style="dashed", color="#dc2626", fontcolor="#dc2626", fontsize="9")

    render(g, "sequence_login")


# =======================================================================
# 4. SEQUENCE DIAGRAM — Quiz submission + remediation (routers/quiz.py)
# =======================================================================
def gen_sequence_quiz():
    g = gv.Digraph("sequence_quiz", filename="sequence_quiz")
    g.attr(bgcolor="white", pad="0.4", rankdir="LR",
           label="<<B>Sequence Diagram — Quiz Submission &amp; Adaptive Remediation</B>>",
           labelloc="t", fontname="Helvetica", fontsize="16")
    g.attr("node", fontname="Helvetica", shape="box", style="filled")

    actors = [
        ("user",  "Étudiant\n(Browser)", "#fef3c7"),
        ("fe",    "React SPA\n(QuizPage.tsx)", "#dbeafe"),
        ("qapi",  "FastAPI\n/quiz/{id}/submit", "#d1fae5"),
        ("pg",    "PostgreSQL\nquiz_resultats\nconcept_mastery", "#e0e7ff"),
        ("gsvc",  "graph_service.py", "#fce7f3"),
        ("neo",   "Neo4j\n(Concept, Resource)", "#ede9fe"),
    ]
    with g.subgraph() as s:
        s.attr(rank="same")
        for n, lbl, col in actors:
            s.node(n, lbl, fillcolor=col, color="#374151")

    steps = [
        ("user", "fe",   "1: submit answers"),
        ("fe",   "qapi", "2: POST /quiz/{id}/submit\n{answers: [...]}"),
        ("qapi", "qapi", "3: grade answers\n→ score (0-100)"),
        ("qapi", "pg",   "4: INSERT INTO quiz_resultats"),
        ("pg",   "qapi", "5: QuizResult{id, score}"),
        ("qapi", "qapi", "6: update_mastery(etudiant, concept, score)"),
        ("qapi", "pg",   "7: UPSERT concept_mastery\nniveau_maitrise = f(current, score)"),
        ("pg",   "qapi", "8: OK"),
        ("qapi", "qapi", "9: if mastery < 60: need remediation"),
        ("qapi", "gsvc", "10: get_remediation(concept_id)"),
        ("gsvc", "neo",  "11: MATCH (r:Resource)-[:REMEDIATES_TO]->(c:Concept)\nWHERE c.id = $id RETURN r"),
        ("neo",  "gsvc", "12: [Resource, ...]"),
        ("gsvc", "qapi", "13: ranked resources"),
        ("qapi", "fe",   "14: 200 {score, mastery, remediation: [...]}"),
        ("fe",   "user", "15: show score + suggest resources"),
    ]
    for a, b, lbl in steps:
        g.edge(a, b, label=lbl, fontsize="9", color="#374151", penwidth="1.2")

    render(g, "sequence_quiz")


# =======================================================================
# 5. DEPLOYMENT DIAGRAM — reflects docker-compose.yml + GitHub Actions
# =======================================================================
def gen_deployment():
    g = gv.Digraph("deployment", filename="deployment")
    g.attr(rankdir="TB", bgcolor="white", pad="0.4",
           label="<<B>Deployment Diagram — Phase 1 Topology</B>>",
           labelloc="t", fontname="Helvetica", fontsize="16")
    g.attr("node", fontname="Helvetica")

    # Developer node
    with g.subgraph(name="cluster_dev") as s:
        s.attr(label="«device» Developer Laptop (Windows 11)",
               style="rounded,filled", fillcolor="#f3f4f6", color="#374151",
               fontname="Helvetica-Bold")

        # Browser
        s.node("browser", "«execution env»\nBrowser\n(Chrome, :5173 or :8080)",
               shape="box3d", style="filled", fillcolor="#fef9c3", color="#854d0e")

        # Docker host
        with s.subgraph(name="cluster_docker") as d:
            d.attr(label="«execution env» Docker Engine\n(docker/docker-compose.yml)",
                   style="rounded,filled", fillcolor="#dbeafe", color="#1e40af")

            d.node("backend",
                   "«container»\nbackend (FastAPI)\nuvicorn 0.0.0.0:8000\nimage: adaptive-backend",
                   shape="component", style="filled", fillcolor="#bbf7d0", color="#166534")

            d.node("frontend",
                   "«container»\nfrontend\nnginx :8080 (prod)\nVite dev :5173 (dev)",
                   shape="component", style="filled", fillcolor="#a7f3d0", color="#065f46")

            d.node("postgres",
                   "«container»\npostgres:15\nport 5433→5432\nDB: adaptive_learning",
                   shape="cylinder", style="filled", fillcolor="#e0e7ff", color="#3730a3")

            d.node("neo4j",
                   "«container»\nneo4j:5\nports 7475→7474, 7687\nauth: neo4j/*****",
                   shape="cylinder", style="filled", fillcolor="#fce7f3", color="#9d174d")

    # CI node
    with g.subgraph(name="cluster_ci") as c:
        c.attr(label="«cloud» GitHub Actions CI",
               style="rounded,filled", fillcolor="#f5f5f4", color="#78716c",
               fontname="Helvetica-Bold")
        c.node("ci", "Runner ubuntu-latest\n5 jobs parallèles:\n• backend-lint (ruff)\n• backend-smoke (import)\n• frontend-build (tsc+vite)\n• graph-integrity (pytest)\n• docker-validate (compose)",
               shape="box", style="filled", fillcolor="#fde68a", color="#92400e")

    # Edges — artifacts / protocols
    g.edge("browser", "frontend", label="HTTP\n:8080 / :5173", fontsize="9")
    g.edge("frontend", "backend", label="REST JSON\n:8000/api/*", fontsize="9")
    g.edge("backend", "postgres", label="asyncpg / psycopg\n:5432 (SQLAlchemy)", fontsize="9")
    g.edge("backend", "neo4j", label="bolt://\n:7687 (neo4j driver)", fontsize="9")
    g.edge("ci", "backend", label="builds + tests\non every push",
           style="dashed", color="#6b7280", fontcolor="#6b7280", fontsize="9")

    render(g, "deployment")


# =======================================================================
# MERMAID SOURCES (for GitHub/VS Code preview)
# =======================================================================
MERMAID = {
    "use_case.mmd": """%% Use Case Diagram - Phase 1
graph LR
  student(["Étudiant"])
  admin(["Enseignant/Admin"])
  subgraph Platform[Adaptive Learning Platform]
    UC1(["S'inscrire"])
    UC2(["Se connecter"])
    UC3(["Consulter profil"])
    UC4(["Parcourir modules"])
    UC5(["Obtenir parcours adaptatif"])
    UC6(["Consulter concept"])
    UC7(["Passer quiz"])
    UC8(["Soumettre quiz"])
    UC9(["Voir résultats"])
    UC10(["Recevoir remédiation"])
    UC11(["Prochain quiz"])
    UC12(["Tuteur IA"])
    UC13(["Seeder graphe"])
    UC14(["Stats graphe"])
  end
  student --- UC1 & UC2 & UC3 & UC4 & UC5 & UC6 & UC7 & UC8 & UC9 & UC11 & UC12
  admin --- UC13 & UC14 & UC4
  UC8 -.->|<<include>>| UC10
  UC5 -.->|<<include>>| UC6
  UC11 -.->|<<extend>>| UC8
""",

    "class_diagram.mmd": """%% Class Diagram - Domain Model
classDiagram
  class Etudiant {
    +int id
    +string nom_complet
    +string email
    +string mot_de_passe
    +string niveau_actuel
    +bool is_active
    +verify_password(pwd) bool
  }
  class ConceptMastery {
    +int id
    +int etudiant_id
    +string concept_neo4j_id
    +float niveau_maitrise (0-100)
    +datetime derniere_mise_a_jour
  }
  class Quiz {
    +int id
    +string titre
    +string module
    +string difficulte
    +JSON questions
    +datetime date_creation
    +grade(answers) float
  }
  class QuizResult {
    +int id
    +int etudiant_id
    +int quiz_id
    +float score
    +int temps_reponse
    +JSON reponses
    +datetime date_tentative
  }
  class TutorSession {
    +int id
    +int etudiant_id
    +string concept_id
    +datetime created_at
    +datetime updated_at
  }
  class Module {
    <<Neo4j>>
    +string id
    +string name
    +int order
  }
  class Concept {
    <<Neo4j>>
    +string id
    +string name
    +string difficulty
  }
  class Resource {
    <<Neo4j>>
    +string id
    +string type
    +string url
  }
  Etudiant "1" o-- "*" ConceptMastery
  Etudiant "1" o-- "*" QuizResult
  Etudiant "1" o-- "*" TutorSession
  Quiz "1" o-- "*" QuizResult
  ConceptMastery ..> Concept : references
  TutorSession ..> Concept : references
  Module "1" --> "*" Concept : COVERS
  Concept --> Concept : REQUIRES
  Resource "1" --> "*" Concept : REMEDIATES_TO
""",

    "sequence_login.mmd": """%% Sequence Diagram - Login Flow
sequenceDiagram
  actor U as Étudiant
  participant FE as React SPA (LoginPage)
  participant API as FastAPI /auth/login
  participant SEC as core/security
  participant DB as PostgreSQL
  U->>FE: fill (email, pwd) + click Login
  FE->>API: POST /auth/login (OAuth2 form)
  API->>DB: SELECT * FROM etudiants WHERE email=?
  DB-->>API: Etudiant row (bcrypt hash)
  API->>SEC: verify_password(plain, hash)
  SEC-->>API: True
  API->>SEC: create_access_token({sub: id})
  SEC-->>API: JWT (HS256, 30m)
  API-->>FE: 200 {access_token, token_type}
  FE-->>U: save token + redirect /dashboard
  alt invalid credentials
    SEC-->>API: False
    API-->>FE: 401 Unauthorized
  end
""",

    "sequence_quiz.mmd": """%% Sequence Diagram - Quiz Submission + Remediation
sequenceDiagram
  actor U as Étudiant
  participant FE as React SPA (QuizPage)
  participant API as FastAPI /quiz/{id}/submit
  participant PG as PostgreSQL
  participant GSV as graph_service
  participant NEO as Neo4j
  U->>FE: submit answers
  FE->>API: POST /quiz/{id}/submit {answers}
  API->>API: grade answers → score
  API->>PG: INSERT quiz_resultats
  PG-->>API: QuizResult{id, score}
  API->>PG: UPSERT concept_mastery
  PG-->>API: OK
  opt mastery < 60
    API->>GSV: get_remediation(concept_id)
    GSV->>NEO: MATCH (r:Resource)-[:REMEDIATES_TO]->(c) WHERE c.id=? RETURN r
    NEO-->>GSV: [Resource, ...]
    GSV-->>API: ranked resources
  end
  API-->>FE: 200 {score, mastery, remediation}
  FE-->>U: show score + remediation list
""",

    "deployment.mmd": """%% Deployment Diagram - Phase 1
graph TB
  subgraph Dev[Developer Laptop - Windows 11]
    Browser[Browser Chrome :5173 / :8080]
    subgraph Docker[Docker Engine docker-compose.yml]
      BE[container: backend FastAPI uvicorn :8000]
      FE[container: frontend nginx :8080 / Vite :5173]
      PG[(container: postgres:15 :5433→5432)]
      NEO[(container: neo4j:5 :7475→7474 bolt :7687)]
    end
  end
  subgraph Cloud[GitHub Actions]
    CI[Runner ubuntu-latest 5 jobs parallèles]
  end
  Browser -->|HTTP| FE
  FE -->|REST JSON :8000| BE
  BE -->|SQLAlchemy :5432| PG
  BE -->|bolt :7687| NEO
  CI -.->|validates on push| BE
""",
}


def write_mermaid():
    for fname, content in MERMAID.items():
        (UML_DIR / fname).write_text(content, encoding="utf-8")
        print(f"  [OK] {fname} ({len(content)} chars)")


# =======================================================================
def main():
    print("=== 1. Use Case ===")
    gen_use_case()
    print("=== 2. Class Diagram ===")
    gen_class_diagram()
    print("=== 3. Sequence — Login ===")
    gen_sequence_login()
    print("=== 4. Sequence — Quiz + Remediation ===")
    gen_sequence_quiz()
    print("=== 5. Deployment ===")
    gen_deployment()
    print("=== Mermaid sources ===")
    write_mermaid()
    print()
    print(f"All diagrams written to {UML_DIR}")


if __name__ == "__main__":
    main()
