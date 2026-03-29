# recommender.py
# This module handles the SEARCH and HEURISTIC RANKING.
#
# AI Concept 1 - Search Strategy:
#   We filter (search) the dataset by subject, difficulty, and type.
#   This is like a constraint-based search in AI.
#
# AI Concept 2 - Heuristic Ranking:
#   After filtering, we RANK materials using a heuristic score.
#   A heuristic is a smart estimation — here, our score estimates
#   how useful a material will be to this student.

import pandas as pd
from feedback import update_scores_in_materials
from utils import load_csv

MATERIALS_FILE = "data/materials.csv"

# ─────────────────────────────────────────────
# HEURISTIC RANKING FORMULA (Key AI Concept)
# ─────────────────────────────────────────────
# score = adaptive_score × difficulty_weight × type_weight
#
# difficulty_weight:
#   Easy   → 1.0 (standard weight)
#   Medium → 1.1 (slightly boost medium content)
#   Hard   → 1.2 (reward challenging material)
#
# type_weight:
#   Video    → 1.0
#   Notes    → 1.05 (slight boost — concise reference)
#   Practice → 1.1  (bigger boost — active learning)
#
# The final score is used to rank materials.
# Higher score = ranked higher in recommendations.
# ─────────────────────────────────────────────

DIFFICULTY_WEIGHTS = {
    "Easy": 1.0,
    "Medium": 1.1,
    "Hard": 1.2
}

TYPE_WEIGHTS = {
    "Video": 1.0,
    "Notes": 1.05,
    "Practice": 1.1
}

def calculate_heuristic_score(adaptive_score, difficulty, mat_type):
    """
    Applies the heuristic ranking formula.

    Parameters:
        adaptive_score : float — score after applying user feedback
        difficulty     : str   — Easy / Medium / Hard
        mat_type       : str   — Video / Notes / Practice

    Returns:
        float — final heuristic score for ranking
    """
    d_weight = DIFFICULTY_WEIGHTS.get(difficulty, 1.0)
    t_weight = TYPE_WEIGHTS.get(mat_type, 1.0)
    heuristic_score = adaptive_score * d_weight * t_weight
    return round(heuristic_score, 3)

def search_materials(subject, difficulty, mat_type):
    """
    SEARCH STRATEGY — Constraint-Based Filtering

    This function searches the dataset using constraints:
    - subject    : must match exactly
    - difficulty : must match exactly
    - mat_type   : must match exactly

    Think of it like a SQL WHERE clause:
        SELECT * FROM materials
        WHERE subject = ? AND difficulty = ? AND type = ?

    After filtering, we apply heuristic ranking to sort results.
    """
    materials_df = load_csv(MATERIALS_FILE)

    if materials_df is None:
        print("❌ Could not load materials database.")
        return None

    # Step 1: Apply adaptive scores from feedback
    materials_df = update_scores_in_materials(materials_df)

    # Step 2: Filter by constraints (Search Strategy)
    filtered = materials_df[
        (materials_df["subject"].str.lower() == subject.lower()) &
        (materials_df["difficulty"].str.lower() == difficulty.lower()) &
        (materials_df["type"].str.lower() == mat_type.lower())
    ].copy()

    if filtered.empty:
        return filtered  # Return empty if no matches

    # Step 3: Apply heuristic ranking formula to each result
    filtered["score"] = filtered.apply(
        lambda row: calculate_heuristic_score(row["score"], row["difficulty"], row["type"]),
        axis=1
    )

    # Step 4: Sort by score (highest first) — this is our ranked output
    filtered = filtered.sort_values("score", ascending=False).reset_index(drop=True)

    return filtered

def get_available_options():
    """
    Returns lists of unique valid subjects, difficulties, and types
    from the materials dataset. Used to show the user valid choices.
    """
    materials_df = load_csv(MATERIALS_FILE)
    if materials_df is None:
        return [], [], []

    subjects = sorted(materials_df["subject"].unique().tolist())
    difficulties = ["Easy", "Medium", "Hard"]
    types = ["Video", "Notes", "Practice"]

    return subjects, difficulties, types
