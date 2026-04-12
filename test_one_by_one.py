#!/usr/bin/env python3
"""
Test script to verify one-by-one display mode.
"""

import sys
import time
from database import QuizDatabase
from ui import QuizUI


def test_one_by_one_display():
    """Test that one-by-one mode shows one question at a time."""
    print("Testing one-by-one display mode...")
    print()

    db = QuizDatabase()
    ui = QuizUI()

    # Get a quiz
    quiz = db.get_quiz(1)
    questions = db.get_questions(quiz['id'])

    print(f"Quiz: {quiz['name']}")
    print(f"Total questions: {len(questions)}")
    print()

    # Simulate one-by-one display
    current_index = 0

    print("Simulating one-by-one display...")
    print("Press Enter to see next question, or 'q' to quit")
    print()

    while True:
        question = questions[current_index]

        # Clear screen
        ui.clear_screen()

        # Display header
        ui.show_title(f"QUIZ: {quiz['name']}")
        ui.show_timer_display(quiz['time_per_question'], current_index + 1, len(questions))

        # Display question
        ui.show_large_question(question['question_text'], current_index + 1, len(questions))

        # Display options
        if question['question_type'] == "multiple_choice" and question['options']:
            ui.show_large_options(question['options'])
        else:
            ui.show_message("(Write your answer on paper)")

        ui.show_message("Controls:")
        ui.show_message("  ← Previous question")
        ui.show_message("  → Next question")
        ui.show_message("  F  Finish quiz")
        ui.show_message()
        ui.show_message("TEST MODE: Press Enter to continue, 'q' to quit")

        # Get input
        user_input = input()

        if user_input.lower() == 'q':
            break

        # Navigate to next question
        if current_index < len(questions) - 1:
            current_index += 1
        else:
            print("End of quiz!")
            break

    db.close()
    print()
    print("✓ Test completed")


if __name__ == "__main__":
    try:
        test_one_by_one_display()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
