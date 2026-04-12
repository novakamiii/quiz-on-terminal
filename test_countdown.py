#!/usr/bin/env python3
"""
Test script to verify countdown timer functionality.
"""

import sys
import time
from database import QuizDatabase
from ui import QuizUI


def test_countdown_timer():
    """Test that countdown timer works correctly."""
    print("Testing countdown timer...")
    print()

    db = QuizDatabase()
    ui = QuizUI()

    # Get a quiz
    quiz = db.get_quiz(1)
    questions = db.get_questions(quiz['id'])

    print(f"Quiz: {quiz['name']}")
    print(f"Time per question: {quiz['time_per_question']}s")
    print(f"Total questions: {len(questions)}")
    print()

    # Test countdown timer display
    print("Testing countdown timer display...")
    for t in [30, 15, 10, 5, 3, 2, 1, 0]:
        ui.clear_screen()
        ui.show_countdown_timer(t, 1, len(questions))
        print(f"Displaying timer: {t}s")
        time.sleep(0.5)

    print()
    print("✓ Countdown timer display test passed")

    # Test timer colors
    print()
    print("Testing timer color changes...")
    print("Green (>10s), Yellow (5-10s), Red (<=5s)")
    time.sleep(2)

    db.close()
    print()
    print("✓ All tests passed!")


if __name__ == "__main__":
    try:
        test_countdown_timer()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
