# main.py
# This is the MAIN program that runs the entire system.
# It ties together the Agent, Recommender, and Feedback modules.
#
# Program Flow:
#   1. Show banner
#   2. Agent perceives student preferences
#   3. Agent recommends materials
#   4. Agent collects feedback
#   5. Ask to continue or exit

from agent import StudyAgent
from utils import clear_screen, print_banner, print_separator

def main():
    """
    Main function — entry point of the program.
    Runs an interactive loop until the student exits.
    """
    clear_screen()
    print_banner()

    print("Welcome to the AI Adaptive Study Material Recommender!")
    print("This system uses AI to recommend study materials AND")
    print("learns from your ratings to improve over time.\n")
    print_separator()

    # Create the Intelligent Agent
    agent = StudyAgent()

    while True:
        print("\n📋 MAIN MENU")
        print("  1. Get Study Material Recommendations")
        print("  2. View Feedback & Learning Progress")
        print("  3. Exit")
        print_separator()

        choice = input("👉 Enter your choice (1/2/3): ").strip()

        if choice == "1":
            # Step 1: Agent perceives user preferences
            subject, difficulty, mat_type = agent.perceive()

            # Step 2: Agent recommends materials
            agent.recommend(subject, difficulty, mat_type)

            # Step 3: Agent collects feedback for adaptive learning
            agent.collect_feedback()

        elif choice == "2":
            agent.show_learning_progress()

        elif choice == "3":
            print("\n👋 Thank you for using the Study Recommender!")
            print("🧠 The system has saved your feedback for future sessions.")
            print("Goodbye! Keep learning! 🚀\n")
            break

        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
