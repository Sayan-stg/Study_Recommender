# utils.py
# Helper functions used across the project

import os
import pandas as pd
from datetime import datetime

def clear_screen():
    """Clears the terminal screen for clean output"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Prints project title banner"""
    print("=" * 60)
    print("   🎓 AI ADAPTIVE STUDY MATERIAL RECOMMENDER SYSTEM")
    print("=" * 60)
    print()

def print_separator():
    """Prints a visual separator line"""
    print("-" * 60)

def get_timestamp():
    """Returns current date and time as a string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate_rating(rating_input):
    """
    Validates that user rating is between 1 and 5.
    Returns integer rating or None if invalid.
    """
    try:
        rating = int(rating_input)
        if 1 <= rating <= 5:
            return rating
        else:
            print("❌ Rating must be between 1 and 5.")
            return None
    except ValueError:
        print("❌ Please enter a valid number.")
        return None

def load_csv(filepath):
    """
    Safely loads a CSV file into a pandas DataFrame.
    Returns None if file is missing or empty.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except pd.errors.EmptyDataError:
        print(f"⚠️  File is empty: {filepath}")
        return None

def display_materials_table(materials_df):
    """
    Displays recommended materials in a numbered, readable table.
    """
    if materials_df is None or materials_df.empty:
        print("⚠️  No materials found for your criteria.")
        return

    print(f"\n{'No.':<5} {'Title':<40} {'Difficulty':<12} {'Type':<10} {'Score':<6}")
    print_separator()

    for i, row in enumerate(materials_df.itertuples(), start=1):
        title = str(row.title)[:37] + "..." if len(str(row.title)) > 37 else str(row.title)
        print(f"{i:<5} {title:<40} {row.difficulty:<12} {row.type:<10} {row.score:.2f}")

    print_separator()
