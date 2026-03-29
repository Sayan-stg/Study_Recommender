# agent.py
# This module implements the INTELLIGENT AGENT.
#
# AI Concept — Intelligent Agent:
# An agent has 4 parts:
#   1. PERCEPT   → It senses the environment (reads user input)
#   2. BRAIN     → It processes using search + heuristic ranking
#   3. ACTION    → It recommends materials
#   4. LEARN     → It updates knowledge from feedback
#
# Our StudyAgent class models all 4 behaviors!

from recommender import search_materials, get_available_options
from feedback import save_feedback, get_feedback_summary
from utils import (
    print_separator, display_materials_table,
    validate_rating
)

class StudyAgent:
    """
    The Intelligent Agent of our system.

    This agent:
    - Perceives student preferences (subject, difficulty, type)
    - Searches and ranks study materials
    - Recommends top materials
    - Learns from student ratings
    """

    def __init__(self):
        self.name = "StudyBot"
        self.last_recommendations = None  # Stores last shown recommendations

    def perceive(self):
        """
        PERCEPT: The agent reads student preferences from input.
        Validates each input before accepting it.
        Returns a tuple of (subject, difficulty, type).
        """
        subjects, difficulties, types = get_available_options()

        print(f"\n🤖 {self.name}: Hello! I will recommend study materials for you.")
        print_separator()

        # --- Subject Input ---
        print(f"\n📚 Available Subjects: {', '.join(subjects)}")
        while True:
            subject = input("👉 Enter subject: ").strip()
            if subject in subjects:
                break
            print(f"❌ Invalid subject. Choose from: {', '.join(subjects)}")

        # --- Difficulty Input ---
        print(f"\n🎯 Difficulty Levels: {', '.join(difficulties)}")
        while True:
            difficulty = input("👉 Enter difficulty: ").strip().capitalize()
            if difficulty in difficulties:
                break
            print(f"❌ Invalid difficulty. Choose from: {', '.join(difficulties)}")

        # --- Type Input ---
        print(f"\n📂 Material Types: {', '.join(types)}")
        while True:
            mat_type = input("👉 Enter type: ").strip().capitalize()
            if mat_type in types:
                break
            print(f"❌ Invalid type. Choose from: {', '.join(types)}")

        return subject, difficulty, mat_type

    def recommend(self, subject, difficulty, mat_type):
        """
        ACTION: The agent searches for and displays recommendations.
        Stores results for later feedback collection.
        """
        print(f"\n🔍 Searching for: {subject} | {difficulty} | {mat_type}")
        print_separator()

        results = search_materials(subject, difficulty, mat_type)

        if results is None or results.empty:
            print(f"😔 Sorry, no materials found for your criteria.")
            print("💡 Try a different subject, difficulty, or type.")
            self.last_recommendations = None
            return

        print(f"\n✅ Top {len(results)} Recommendations (ranked by AI score):\n")
        display_materials_table(results)
        self.last_recommendations = results

    def collect_feedback(self):
        """
        LEARN: The agent asks for ratings and saves them.
        This feedback updates future recommendation scores.
        """
        if self.last_recommendations is None or self.last_recommendations.empty:
            print("⚠️  No recommendations to rate yet.")
            return

        print("\n💬 Would you like to rate a material? (Feedback improves future recommendations!)")
        choice = input("👉 Enter 'yes' or 'no': ").strip().lower()

        if choice != 'yes':
            print("🤖 Okay! Come back anytime for more recommendations.")
            return

        print("\nEnter the number of the material you want to rate:")
        try:
            num = int(input("👉 Material number: ").strip())
            if num < 1 or num > len(self.last_recommendations):
                print("❌ Invalid number.")
                return
        except ValueError:
            print("❌ Please enter a valid number.")
            return

        # Get the selected material's details
        selected = self.last_recommendations.iloc[num - 1]

        print(f"\n📖 You selected: {selected['title']}")
        print("⭐ Rate this material from 1 (Poor) to 5 (Excellent):")
        rating_input = input("👉 Your rating: ").strip()

        rating = validate_rating(rating_input)
        if rating is None:
            return

        # Save feedback — this triggers adaptive learning
        save_feedback(
            material_id=selected["id"],
            title=selected["title"],
            subject=selected["subject"],
            difficulty=selected["difficulty"],
            mat_type=selected["type"],
            rating=rating
        )

        stars = "⭐" * rating
        print(f"{stars} You rated '{selected['title']}' as {rating}/5")
        print("🧠 System has learned from your feedback!")

    def show_learning_progress(self):
        """
        Shows how the system has learned from all past feedback.
        """
        print("\n")
        get_feedback_summary()
