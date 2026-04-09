#!/usr/bin/env python3
"""
Phase 2 — Sprint 1 : Banque de Questions
Peuple la table quiz avec des QCM couvrant les 15 concepts d'analyse numérique.

Usage :
    cd backend
    venv\Scripts\activate
    python scripts/seed_quizzes.py

Prérequis :
    - PostgreSQL lancé (docker-compose up -d)
    - Backend démarré au moins une fois (tables créées)
    - .env configuré
"""

import os
import sys
import logging
from datetime import datetime, timezone

# Setup path pour importer les modules app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================
# BANQUE DE QUESTIONS — 15 Quiz (1 par concept) + 6 Quiz Mixtes
# ============================================================

QUIZZES = [
    # ============================================================
    # MODULE 1 : INTERPOLATION
    # ============================================================
    {
        "titre": "Les Bases des Polynômes",
        "module": "Interpolation",
        "difficulte": "facile",
        "questions": [
            {
                "id": 1,
                "question": "Quel est le degré du polynôme P(x) = 3x⁴ + 2x² - 5 ?",
                "options": ["2", "3", "4", "5"],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 2,
                "question": "Combien de racines (réelles ou complexes) un polynôme de degré n possède-t-il au maximum ?",
                "options": ["n - 1", "n", "n + 1", "2n"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 3,
                "question": "Si P(x) est un polynôme de degré 3, combien de coefficients faut-il pour le définir complètement ?",
                "options": ["3", "4", "5", "6"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "Quelle est la forme générale d'un polynôme de degré 2 ?",
                "options": ["ax + b", "ax² + bx + c", "ax³ + bx² + cx + d", "a/x + b"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "Un polynôme d'interpolation de degré n passe par combien de points ?",
                "options": ["n - 1", "n", "n + 1", "2n"],
                "correct_index": 2,
                "points": 1
            }
        ]
    },
    {
        "titre": "Interpolation de Lagrange",
        "module": "Interpolation",
        "difficulte": "moyen",
        "questions": [
            {
                "id": 1,
                "question": "Dans la formule de Lagrange, que vaut le polynôme de base Lᵢ(xᵢ) ?",
                "options": ["0", "1", "xᵢ", "n"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "Pour n+1 points distincts, quel est le degré maximal du polynôme de Lagrange ?",
                "options": ["n - 1", "n", "n + 1", "2n"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 3,
                "question": "Que vaut Lᵢ(xⱼ) quand i ≠ j ?",
                "options": ["0", "1", "-1", "xⱼ"],
                "correct_index": 0,
                "points": 1
            },
            {
                "id": 4,
                "question": "Quel est le principal inconvénient de l'interpolation de Lagrange quand on ajoute un nouveau point ?",
                "options": [
                    "Le polynôme devient instable",
                    "Il faut recalculer tous les polynômes de base",
                    "Le degré ne change pas",
                    "Les coefficients restent identiques"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "L'interpolation de Lagrange garantit que le polynôme passe par :",
                "options": [
                    "Certains points seulement",
                    "Tous les points donnés exactement",
                    "Aucun point exactement",
                    "Uniquement les points aux extrémités"
                ],
                "correct_index": 1,
                "points": 1
            }
        ]
    },
    {
        "titre": "Différences Divisées",
        "module": "Interpolation",
        "difficulte": "moyen",
        "questions": [
            {
                "id": 1,
                "question": "La différence divisée de premier ordre f[xᵢ, xᵢ₊₁] est définie comme :",
                "options": [
                    "f(xᵢ₊₁) - f(xᵢ)",
                    "(f(xᵢ₊₁) - f(xᵢ)) / (xᵢ₊₁ - xᵢ)",
                    "f(xᵢ) × f(xᵢ₊₁)",
                    "(xᵢ₊₁ - xᵢ) / (f(xᵢ₊₁) - f(xᵢ))"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "Les différences divisées sont utilisées principalement pour construire :",
                "options": [
                    "Le polynôme de Lagrange",
                    "Le polynôme de Newton",
                    "Les splines cubiques",
                    "La quadrature de Gauss"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 3,
                "question": "Comment sont organisées les différences divisées pour le calcul ?",
                "options": [
                    "En matrice carrée",
                    "En tableau triangulaire",
                    "En vecteur linéaire",
                    "En arbre binaire"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "La différence divisée d'ordre k utilise combien de points ?",
                "options": ["k", "k + 1", "k - 1", "2k"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "Si tous les points sont équidistants (h constant), les différences divisées se simplifient en :",
                "options": [
                    "Différences finies divisées par des puissances de h",
                    "Dérivées exactes",
                    "Intégrales numériques",
                    "Valeurs constantes"
                ],
                "correct_index": 0,
                "points": 1
            }
        ]
    },
    {
        "titre": "Interpolation de Newton",
        "module": "Interpolation",
        "difficulte": "moyen",
        "questions": [
            {
                "id": 1,
                "question": "Quel avantage a la forme de Newton par rapport à la forme de Lagrange ?",
                "options": [
                    "Elle est plus précise",
                    "On peut ajouter un point sans tout recalculer",
                    "Elle utilise moins de mémoire",
                    "Elle converge toujours"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "Dans la forme de Newton, P(x) = f[x₀] + f[x₀,x₁](x-x₀) + ... Le terme f[x₀,x₁,...,xₙ] est :",
                "options": [
                    "Une dérivée",
                    "Une différence divisée d'ordre n",
                    "Un coefficient de Lagrange",
                    "Une intégrale"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 3,
                "question": "Le polynôme de Newton de degré n nécessite le calcul de combien de différences divisées au total ?",
                "options": [
                    "n",
                    "n + 1",
                    "n(n+1)/2",
                    "n²"
                ],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 4,
                "question": "Pour 4 points de données, le polynôme de Newton sera de degré :",
                "options": ["2", "3", "4", "5"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "La forme progressive de Newton utilise les différences divisées à partir de :",
                "options": [
                    "La fin du tableau",
                    "Le milieu du tableau",
                    "Le début du tableau (x₀)",
                    "N'importe quel point"
                ],
                "correct_index": 2,
                "points": 1
            }
        ]
    },
    {
        "titre": "Interpolation par Splines",
        "module": "Interpolation",
        "difficulte": "difficile",
        "questions": [
            {
                "id": 1,
                "question": "Pourquoi utilise-t-on des splines plutôt qu'un polynôme de haut degré ?",
                "options": [
                    "Les splines sont plus rapides à calculer",
                    "Les polynômes de haut degré oscillent (phénomène de Runge)",
                    "Les splines utilisent moins de mémoire",
                    "Les polynômes ne passent pas par les points"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "Une spline cubique est un polynôme de degré __ sur chaque intervalle.",
                "options": ["1", "2", "3", "4"],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 3,
                "question": "Quelle condition de continuité une spline cubique satisfait-elle aux nœuds intérieurs ?",
                "options": [
                    "Continuité de la fonction uniquement",
                    "Continuité de la fonction et de la dérivée première",
                    "Continuité de la fonction, dérivée première et dérivée seconde",
                    "Continuité jusqu'à la dérivée troisième"
                ],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 4,
                "question": "Les splines « naturelles » imposent quelle condition aux extrémités ?",
                "options": [
                    "Dérivée première = 0",
                    "Dérivée seconde = 0",
                    "La fonction = 0",
                    "Dérivée troisième = 0"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "Pour n+1 points, combien de polynômes cubiques une spline cubique contient-elle ?",
                "options": ["n - 1", "n", "n + 1", "2n"],
                "correct_index": 1,
                "points": 1
            }
        ]
    },

    # ============================================================
    # MODULE 2 : INTÉGRATION NUMÉRIQUE
    # ============================================================
    {
        "titre": "Sommes de Riemann",
        "module": "Intégration Numérique",
        "difficulte": "facile",
        "questions": [
            {
                "id": 1,
                "question": "Le principe des sommes de Riemann est d'approcher l'intégrale par :",
                "options": [
                    "Des triangles",
                    "Des rectangles",
                    "Des paraboles",
                    "Des cercles"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "Quand le nombre de sous-intervalles n → ∞, la somme de Riemann converge vers :",
                "options": [
                    "Zéro",
                    "L'infini",
                    "L'intégrale définie exacte",
                    "La dérivée de la fonction"
                ],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 3,
                "question": "Dans la somme de Riemann à gauche, on évalue la fonction en :",
                "options": [
                    "Le point milieu de chaque intervalle",
                    "L'extrémité gauche de chaque intervalle",
                    "L'extrémité droite de chaque intervalle",
                    "Les deux extrémités"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "Si h est la largeur de chaque sous-intervalle et n le nombre de sous-intervalles, alors h = :",
                "options": ["(b-a)/n", "(b+a)/n", "n/(b-a)", "(b-a)×n"],
                "correct_index": 0,
                "points": 1
            },
            {
                "id": 5,
                "question": "L'erreur des sommes de Riemann est de l'ordre de :",
                "options": ["O(h)", "O(h²)", "O(h³)", "O(h⁴)"],
                "correct_index": 0,
                "points": 1
            }
        ]
    },
    {
        "titre": "Intégrales Définies — Fondements",
        "module": "Intégration Numérique",
        "difficulte": "facile",
        "questions": [
            {
                "id": 1,
                "question": "L'intégrale définie ∫ₐᵇ f(x)dx représente géométriquement :",
                "options": [
                    "La pente de f",
                    "L'aire sous la courbe de f entre a et b",
                    "La valeur maximale de f",
                    "La longueur de la courbe"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "Si f(x) < 0 sur [a,b], l'intégrale définie est :",
                "options": ["Positive", "Négative", "Nulle", "Indéfinie"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 3,
                "question": "∫ₐᵃ f(x)dx = ?",
                "options": ["f(a)", "1", "0", "∞"],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 4,
                "question": "La propriété ∫ₐᵇ f(x)dx = -∫ᵇₐ f(x)dx s'appelle :",
                "options": [
                    "Linéarité",
                    "Antisymétrie des bornes",
                    "Additivité",
                    "Positivité"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "Pourquoi a-t-on besoin de méthodes numériques pour calculer des intégrales ?",
                "options": [
                    "Les ordinateurs ne comprennent pas les intégrales",
                    "Beaucoup de fonctions n'ont pas de primitive analytique connue",
                    "Les intégrales sont toujours approximatives",
                    "C'est plus rapide qu'un calcul exact"
                ],
                "correct_index": 1,
                "points": 1
            }
        ]
    },
    {
        "titre": "Méthode des Trapèzes",
        "module": "Intégration Numérique",
        "difficulte": "moyen",
        "questions": [
            {
                "id": 1,
                "question": "La méthode des trapèzes approche la fonction sur chaque intervalle par :",
                "options": ["Une constante", "Une droite (segment)", "Une parabole", "Un polynôme de degré 3"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "L'erreur de la méthode des trapèzes composée est de l'ordre de :",
                "options": ["O(h)", "O(h²)", "O(h³)", "O(h⁴)"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 3,
                "question": "La formule du trapèze simple entre a et b est :",
                "options": [
                    "(b-a) × f(a)",
                    "(b-a) × (f(a) + f(b)) / 2",
                    "(b-a) × f((a+b)/2)",
                    "(b-a)² × f'(a)"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "Pour une fonction linéaire f(x) = mx + p, la méthode des trapèzes donne :",
                "options": [
                    "Une approximation avec erreur",
                    "Le résultat exact",
                    "Toujours zéro",
                    "Une valeur négative"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "Si on double le nombre de sous-intervalles n, l'erreur de la méthode des trapèzes :",
                "options": [
                    "Est divisée par 2",
                    "Est divisée par 4",
                    "Est divisée par 8",
                    "Reste la même"
                ],
                "correct_index": 1,
                "points": 1
            }
        ]
    },
    {
        "titre": "Méthode de Simpson",
        "module": "Intégration Numérique",
        "difficulte": "moyen",
        "questions": [
            {
                "id": 1,
                "question": "La méthode de Simpson approche la fonction sur chaque intervalle par :",
                "options": ["Un segment", "Une parabole", "Un polynôme de degré 3", "Une exponentielle"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "L'ordre de convergence de la méthode de Simpson est :",
                "options": ["O(h²)", "O(h³)", "O(h⁴)", "O(h⁵)"],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 3,
                "question": "La méthode de Simpson nécessite un nombre de sous-intervalles :",
                "options": ["Quelconque", "Pair", "Impair", "Multiple de 3"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "La formule de Simpson 1/3 simple utilise combien de points ?",
                "options": ["2", "3", "4", "5"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "Simpson est exacte pour les polynômes de degré ≤ :",
                "options": ["1", "2", "3", "4"],
                "correct_index": 2,
                "points": 1
            }
        ]
    },
    {
        "titre": "Quadrature de Gauss",
        "module": "Intégration Numérique",
        "difficulte": "difficile",
        "questions": [
            {
                "id": 1,
                "question": "Quel est l'avantage principal de la quadrature de Gauss par rapport aux trapèzes/Simpson ?",
                "options": [
                    "Elle est plus simple à programmer",
                    "Elle atteint une précision maximale avec un minimum de points",
                    "Elle fonctionne sur des intervalles infinis uniquement",
                    "Elle ne nécessite aucun calcul"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "Les nœuds de la quadrature de Gauss-Legendre sont les racines de :",
                "options": [
                    "Polynômes de Taylor",
                    "Polynômes de Lagrange",
                    "Polynômes de Legendre",
                    "Polynômes de Chebyshev"
                ],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 3,
                "question": "Avec n points, la quadrature de Gauss est exacte pour les polynômes de degré ≤ :",
                "options": ["n", "n + 1", "2n - 1", "2n"],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 4,
                "question": "L'intervalle standard pour la quadrature de Gauss-Legendre est :",
                "options": ["[0, 1]", "[-1, 1]", "[0, ∞]", "[-∞, ∞]"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "Pour appliquer Gauss-Legendre sur [a, b] quelconque, on utilise :",
                "options": [
                    "Un changement de variable linéaire",
                    "Une transformation logarithmique",
                    "La formule de Taylor",
                    "Aucune transformation"
                ],
                "correct_index": 0,
                "points": 1
            }
        ]
    },

    # ============================================================
    # MODULE 3 : ÉQUATIONS DIFFÉRENTIELLES ORDINAIRES (EDOs)
    # ============================================================
    {
        "titre": "Problèmes à Valeur Initiale",
        "module": "EDOs",
        "difficulte": "facile",
        "questions": [
            {
                "id": 1,
                "question": "Un problème à valeur initiale (IVP) est défini par :",
                "options": [
                    "Une équation différentielle + une condition aux limites",
                    "Une équation différentielle + une condition initiale y(t₀) = y₀",
                    "Deux équations différentielles",
                    "Une intégrale + une dérivée"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "Dans y' = f(t, y), y(0) = 1, que représente y' ?",
                "options": [
                    "La valeur de y",
                    "La dérivée de y par rapport à t",
                    "L'intégrale de y",
                    "Le carré de y"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 3,
                "question": "Pourquoi résout-on les EDOs numériquement plutôt qu'analytiquement ?",
                "options": [
                    "C'est toujours plus précis",
                    "Beaucoup d'EDOs n'ont pas de solution analytique connue",
                    "Les solutions analytiques sont toujours fausses",
                    "Les ordinateurs préfèrent les nombres"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "Le pas de temps h dans les méthodes numériques d'EDO représente :",
                "options": [
                    "La hauteur de la courbe",
                    "L'intervalle entre deux points de la solution discrète",
                    "L'erreur maximale",
                    "Le nombre d'itérations"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "Si on réduit le pas h, la solution numérique devient généralement :",
                "options": [
                    "Moins précise",
                    "Plus précise mais plus coûteuse en calcul",
                    "Identique",
                    "Instable"
                ],
                "correct_index": 1,
                "points": 1
            }
        ]
    },
    {
        "titre": "Séries de Taylor",
        "module": "EDOs",
        "difficulte": "moyen",
        "questions": [
            {
                "id": 1,
                "question": "Le développement de Taylor de f(x) autour de x₀ utilise :",
                "options": [
                    "Les intégrales de f",
                    "Les dérivées successives de f en x₀",
                    "Les racines de f",
                    "Les valeurs de f aux points entiers"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "Le terme de Taylor d'ordre n est proportionnel à :",
                "options": ["(x - x₀)ⁿ", "xⁿ", "1/n", "eⁿ"],
                "correct_index": 0,
                "points": 1
            },
            {
                "id": 3,
                "question": "L'approximation de Taylor d'ordre 1 de f(x₀ + h) est :",
                "options": [
                    "f(x₀)",
                    "f(x₀) + h × f'(x₀)",
                    "f(x₀) + h² × f''(x₀)/2",
                    "h × f(x₀)"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "Le reste (erreur de troncature) de Taylor d'ordre n est de l'ordre de :",
                "options": ["O(hⁿ)", "O(hⁿ⁺¹)", "O(h)", "O(1/n)"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "La méthode de Taylor pour les EDOs est peu utilisée en pratique car :",
                "options": [
                    "Elle diverge toujours",
                    "Elle nécessite le calcul des dérivées d'ordre supérieur de f",
                    "Elle est moins précise que Euler",
                    "Elle ne fonctionne pas avec des ordinateurs"
                ],
                "correct_index": 1,
                "points": 1
            }
        ]
    },
    {
        "titre": "Méthode d'Euler",
        "module": "EDOs",
        "difficulte": "moyen",
        "questions": [
            {
                "id": 1,
                "question": "La formule d'Euler explicite est :",
                "options": [
                    "yₙ₊₁ = yₙ + h × f(tₙ, yₙ)",
                    "yₙ₊₁ = yₙ × h + f(tₙ, yₙ)",
                    "yₙ₊₁ = yₙ - h × f(tₙ, yₙ)",
                    "yₙ₊₁ = h × f(tₙ₊₁, yₙ₊₁)"
                ],
                "correct_index": 0,
                "points": 1
            },
            {
                "id": 2,
                "question": "L'erreur locale de troncature de la méthode d'Euler est de l'ordre de :",
                "options": ["O(h)", "O(h²)", "O(h³)", "O(h⁴)"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 3,
                "question": "L'erreur globale de la méthode d'Euler est de l'ordre de :",
                "options": ["O(h)", "O(h²)", "O(h³)", "O(h⁴)"],
                "correct_index": 0,
                "points": 1
            },
            {
                "id": 4,
                "question": "La méthode d'Euler est dérivée du développement de Taylor en gardant :",
                "options": [
                    "Uniquement le terme d'ordre 0",
                    "Les termes d'ordre 0 et 1",
                    "Les termes jusqu'à l'ordre 2",
                    "Tous les termes"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "Géométriquement, la méthode d'Euler suit :",
                "options": [
                    "La tangente à la courbe solution en chaque point",
                    "La normale à la courbe",
                    "Un arc de cercle",
                    "Une parabole"
                ],
                "correct_index": 0,
                "points": 1
            }
        ]
    },
    {
        "titre": "Méthode d'Euler Améliorée (Heun)",
        "module": "EDOs",
        "difficulte": "moyen",
        "questions": [
            {
                "id": 1,
                "question": "La méthode de Heun utilise combien d'évaluations de f par pas ?",
                "options": ["1", "2", "3", "4"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "L'ordre de convergence de la méthode de Heun est :",
                "options": ["1", "2", "3", "4"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 3,
                "question": "La méthode de Heun est aussi appelée :",
                "options": [
                    "Euler implicite",
                    "Méthode du trapèze pour EDOs",
                    "Méthode de Simpson pour EDOs",
                    "Euler rétrograde"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "Dans Heun, la pente finale est calculée comme :",
                "options": [
                    "La pente au début",
                    "La pente à la fin (prédiction)",
                    "La moyenne des pentes au début et à la fin",
                    "Le produit des pentes"
                ],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 5,
                "question": "Par rapport à Euler simple, Heun est :",
                "options": [
                    "Moins précis mais plus rapide",
                    "Plus précis grâce à la correction de pente",
                    "Identique en précision",
                    "Plus rapide mais moins stable"
                ],
                "correct_index": 1,
                "points": 1
            }
        ]
    },
    {
        "titre": "Méthode de Runge-Kutta (RK4)",
        "module": "EDOs",
        "difficulte": "difficile",
        "questions": [
            {
                "id": 1,
                "question": "Combien d'évaluations de f la méthode RK4 classique effectue-t-elle par pas ?",
                "options": ["2", "3", "4", "5"],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 2,
                "question": "L'erreur locale de RK4 est de l'ordre de :",
                "options": ["O(h²)", "O(h³)", "O(h⁴)", "O(h⁵)"],
                "correct_index": 3,
                "points": 1
            },
            {
                "id": 3,
                "question": "Dans la formule RK4, yₙ₊₁ = yₙ + (h/6)(k₁ + 2k₂ + 2k₃ + k₄), les poids (1,2,2,1) signifient :",
                "options": [
                    "Toutes les pentes ont le même poids",
                    "Les pentes au milieu de l'intervalle comptent double",
                    "La première pente est la plus importante",
                    "La dernière pente est la plus importante"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "RK4 est préféré à la méthode de Taylor d'ordre 4 car :",
                "options": [
                    "RK4 est plus précis",
                    "RK4 ne nécessite pas le calcul de dérivées partielles de f",
                    "RK4 utilise moins d'évaluations",
                    "Taylor d'ordre 4 n'existe pas"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 5,
                "question": "L'erreur globale de RK4 est de l'ordre de :",
                "options": ["O(h²)", "O(h³)", "O(h⁴)", "O(h⁵)"],
                "correct_index": 2,
                "points": 1
            }
        ]
    },

    # ============================================================
    # QUIZ MIXTES — Évaluation transversale
    # ============================================================
    {
        "titre": "Quiz Mixte — Interpolation Complet",
        "module": "Interpolation",
        "difficulte": "difficile",
        "questions": [
            {
                "id": 1,
                "question": "Le phénomène de Runge apparaît quand on utilise :",
                "options": [
                    "Des splines cubiques",
                    "Un polynôme de haut degré avec des points équidistants",
                    "La méthode de Simpson",
                    "La quadrature de Gauss"
                ],
                "correct_index": 1,
                "points": 2
            },
            {
                "id": 2,
                "question": "Le théorème d'unicité de l'interpolation polynomiale dit que pour n+1 points distincts, il existe :",
                "options": [
                    "Aucun polynôme",
                    "Exactement un polynôme de degré ≤ n",
                    "Plusieurs polynômes de degré ≤ n",
                    "Un polynôme de degré exactement n"
                ],
                "correct_index": 1,
                "points": 2
            },
            {
                "id": 3,
                "question": "Lagrange, Newton, et les différences divisées produisent :",
                "options": [
                    "Des polynômes différents",
                    "Le même polynôme écrit différemment",
                    "Des approximations de précision différente",
                    "Des résultats incompatibles"
                ],
                "correct_index": 1,
                "points": 2
            }
        ]
    },
    {
        "titre": "Quiz Mixte — Intégration Complet",
        "module": "Intégration Numérique",
        "difficulte": "difficile",
        "questions": [
            {
                "id": 1,
                "question": "Classez ces méthodes par ordre de précision croissante :",
                "options": [
                    "Simpson < Trapèzes < Riemann",
                    "Riemann < Trapèzes < Simpson",
                    "Trapèzes < Riemann < Simpson",
                    "Riemann < Simpson < Trapèzes"
                ],
                "correct_index": 1,
                "points": 2
            },
            {
                "id": 2,
                "question": "Si h est divisé par 2, l'erreur de Simpson est divisée par :",
                "options": ["2", "4", "8", "16"],
                "correct_index": 3,
                "points": 2
            },
            {
                "id": 3,
                "question": "La quadrature de Gauss à 2 points est exacte pour les polynômes de degré ≤ :",
                "options": ["1", "2", "3", "4"],
                "correct_index": 2,
                "points": 2
            }
        ]
    },
    {
        "titre": "Quiz Mixte — EDOs Complet",
        "module": "EDOs",
        "difficulte": "difficile",
        "questions": [
            {
                "id": 1,
                "question": "Classez ces méthodes par ordre de précision croissante :",
                "options": [
                    "RK4 < Heun < Euler",
                    "Euler < Heun < RK4",
                    "Heun < Euler < RK4",
                    "Euler < RK4 < Heun"
                ],
                "correct_index": 1,
                "points": 2
            },
            {
                "id": 2,
                "question": "Si on divise h par 2, l'erreur globale d'Euler est divisée par :",
                "options": ["2", "4", "8", "16"],
                "correct_index": 0,
                "points": 2
            },
            {
                "id": 3,
                "question": "Si on divise h par 2, l'erreur globale de RK4 est divisée par :",
                "options": ["2", "4", "8", "16"],
                "correct_index": 3,
                "points": 2
            }
        ]
    },
    {
        "titre": "Évaluation Diagnostique — Prérequis Généraux",
        "module": "Prérequis",
        "difficulte": "facile",
        "questions": [
            {
                "id": 1,
                "question": "La dérivée de f(x) = x³ est :",
                "options": ["x²", "3x²", "3x³", "x⁴/4"],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 2,
                "question": "∫ 2x dx = ?",
                "options": ["2x²", "x²", "x² + C", "2x² + C"],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 3,
                "question": "En Python, comment crée-t-on un tableau NumPy de 10 zéros ?",
                "options": [
                    "np.array(10)",
                    "np.zeros(10)",
                    "np.empty(10)",
                    "np.zero(10)"
                ],
                "correct_index": 1,
                "points": 1
            },
            {
                "id": 4,
                "question": "La valeur absolue de -7 est :",
                "options": ["-7", "0", "7", "49"],
                "correct_index": 2,
                "points": 1
            },
            {
                "id": 5,
                "question": "Une matrice 3×3 a combien d'éléments ?",
                "options": ["3", "6", "9", "27"],
                "correct_index": 2,
                "points": 1
            }
        ]
    }
]


def seed_quizzes():
    """Insère tous les quiz dans PostgreSQL."""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        logger.error("❌ DATABASE_URL manquante dans .env")
        sys.exit(1)

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Import du modèle
        from app.models.quiz import Quiz

        # Vérifier si des quiz existent déjà
        existing = session.query(Quiz).count()
        if existing > 0:
            logger.warning(f"⚠️  {existing} quiz déjà en base. Suppression et recréation...")
            session.query(Quiz).delete()
            session.commit()

        # Insérer les quiz
        for i, quiz_data in enumerate(QUIZZES):
            quiz = Quiz(
                titre=quiz_data["titre"],
                module=quiz_data["module"],
                difficulte=quiz_data["difficulte"],
                questions=quiz_data["questions"]
            )
            session.add(quiz)
            logger.info(f"  ✅ Quiz {i+1}/{len(QUIZZES)}: {quiz_data['titre']} ({quiz_data['module']}, {quiz_data['difficulte']}, {len(quiz_data['questions'])} questions)")

        session.commit()

        # Statistiques
        total_quizzes = len(QUIZZES)
        total_questions = sum(len(q["questions"]) for q in QUIZZES)
        modules = set(q["module"] for q in QUIZZES)

        logger.info(f"\n{'='*60}")
        logger.info(f"BANQUE DE QUESTIONS PEUPLÉE AVEC SUCCÈS")
        logger.info(f"{'='*60}")
        logger.info(f"  Quiz créés      : {total_quizzes}")
        logger.info(f"  Questions total  : {total_questions}")
        logger.info(f"  Modules couverts : {', '.join(sorted(modules))}")
        logger.info(f"  Difficultés      : facile, moyen, difficile")
        logger.info(f"{'='*60}\n")

    except Exception as e:
        session.rollback()
        logger.error(f"❌ Erreur : {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_quizzes()
