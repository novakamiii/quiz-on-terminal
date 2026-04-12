#!/usr/bin/env python3
"""
Test script for Rich Live display functionality.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from live_display import LiveQuizDisplay
from rich.console import Console

def test_live_display():
    """Test the live display with sample questions."""
    print("Testing Rich Live Display...")

    # Sample questions
    sample_questions = [
        {
            'question_text': 'What is the capital of France?',
            'options': ['London', 'Berlin', 'Paris', 'Madrid'],
            'question_type': 'multiple_choice',
            'correct_answer': 'C',
            'points': 10
        },
        {
            'question_text': 'What is 2 + 2?',
            'options': ['3', '4', '5', '6'],
            'question_type': 'multiple_choice',
            'correct_answer': 'B',
            'points': 10
        },
        {
            'question_text': 'What is the largest planet in our solar system?',
            'options': ['Earth', 'Mars', 'Jupiter', 'Saturn'],
            'question_type': 'multiple_choice',
            'correct_answer': 'C',
            'points': 10
        }
    ]

    def on_finish(results):
        print(f"\n✓ Quiz completed! Viewed {results['current_index'] + 1}/{results['total_questions']} questions")

    def on_question_change(index):
        print(f"\n✓ Changed to question {index + 1}")

    console = Console()
    display = LiveQuizDisplay(console)

    print("\nStarting live display test...")
    print("Controls:")
    print("  ← → : Navigate questions")
    print("  F   : Finish quiz")
    print("  P   : Pause/Resume timer")
    print("  Q   : Quit")
    print("\nPress Enter to start...")
    input()

    try:
        results = display.display_quiz(
            sample_questions,
            time_per_question=30,
            on_finish=on_finish,
            on_question_change=on_question_change
        )
        print("\n✓ Test completed successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_live_display()
    sys.exit(0 if success else 1)
