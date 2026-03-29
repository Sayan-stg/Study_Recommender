# feedback.py
# This module handles the ADAPTIVE LEARNING part of our system.
#
# AI/ML Concept: The system adjusts (adapts) the score of each
# material based on user ratings. High ratings increase the score;
# low ratings decrease it. This mimics reinforcement learning.

import pandas as pd
import os
from utils import get_timestamp, load_csv

FEEDBACK_FILE = "data/feedback.csv"
MATERIALS_FILE = "data/materials.csv"

def save_feedback(material_id, title, subject, difficulty, mat_type, rating):
    """
    Saves user feedback (rating) to feedback.csv.
    Each rating is stored with a timestamp for tracking history.
    """
    new_feedback = {
        "material_id": material_id,
        "title": title,
        "subject": subject,
        "difficulty": difficulty,
        "type": mat_type,
        "rating": rating,
        "timestamp": get_timestamp()
    }

    # If feedback file exists, append to it; otherwise create it
    if os.path.exists(FEEDBACK_FILE) and os.path.getsize(FEEDBACK_FILE) > 0:
        try:
            df = pd.read_csv(FEEDBACK_FILE)
            new_row = pd.DataFrame([new_feedback])
            df = pd.concat([df, new_row], ignore_index=True)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame([new_feedback])
    else:
        df = pd.DataFrame([new_feedback])

    df.to_csv(FEEDBACK_FILE, index=False)
    print(f"✅ Feedback saved! Thank you for rating this material.")

def calculate_adaptive_score(material_id, base_score):
    """
    ADAPTIVE LEARNING FORMULA:

    This is the core ML concept of the project.

    The system looks at all past ratings for a material and
    calculates a weighted score that blends the original base score
    with actual user ratings.

    Formula:
        adaptive_score = (base_score + sum_of_ratings) / (1 + count_of_ratings)

    Example:
        base_score = 3.5
        ratings = [5, 4, 5]  → sum = 14, count = 3
        adaptive_score = (3.5 + 14) / (1 + 3) = 17.5 / 4 = 4.375

    This means: the more positive ratings a material gets,
    the higher it ranks in future recommendations!
    """
    if not os.path.exists(FEEDBACK_FILE) or os.path.getsize(FEEDBACK_FILE) == 0:
        return base_score  # No feedback yet → return original score

    feedback_df = load_csv(FEEDBACK_FILE)
    if feedback_df is None or feedback_df.empty:
        return base_score

    # Filter feedback only for this specific material
    material_feedback = feedback_df[feedback_df["material_id"] == material_id]

    if material_feedback.empty:
        return base_score  # No feedback for this material yet

    # Apply the adaptive formula
    sum_ratings = material_feedback["rating"].sum()
    count_ratings = len(material_feedback)
    adaptive_score = (base_score + sum_ratings) / (1 + count_ratings)

    return round(adaptive_score, 2)

def update_scores_in_materials(materials_df):
    """
    Takes a DataFrame of materials and updates each material's
    score using the adaptive learning formula.

    This is called every time recommendations are generated,
    so the system always reflects the latest user feedback.
    """
    updated_scores = []

    for _, row in materials_df.iterrows():
        new_score = calculate_adaptive_score(row["id"], row["base_score"])
        updated_scores.append(new_score)

    materials_df = materials_df.copy()
    materials_df["score"] = updated_scores
    return materials_df

def get_feedback_summary():
    """
    Shows a summary of all feedback received so far.
    Useful for understanding how the system is learning.
    """
    if not os.path.exists(FEEDBACK_FILE) or os.path.getsize(FEEDBACK_FILE) == 0:
        print("📭 No feedback collected yet.")
        return

    feedback_df = load_csv(FEEDBACK_FILE)
    if feedback_df is None or feedback_df.empty:
        print("📭 No feedback collected yet.")
        return

    print("\n📊 FEEDBACK SUMMARY")
    print("-" * 60)

    # Group by material title and calculate average rating
    summary = feedback_df.groupby("title")["rating"].agg(["mean", "count"])
    summary.columns = ["Average Rating", "Total Ratings"]
    summary["Average Rating"] = summary["Average Rating"].round(2)
    summary = summary.sort_values("Average Rating", ascending=False)

    print(summary.to_string())
    print("-" * 60)
