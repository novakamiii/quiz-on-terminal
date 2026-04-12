#!/usr/bin/env python3
"""
Simple test to verify the display doesn't scroll.
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from live_display import LiveQuizDisplay

def test_no_scrolling():
    """Test that display doesn't scroll."""
    print("Testing Display Scrolling Fix...")
    print("This test will run for 10 seconds.")
    print("Watch the display - it should NOT scroll down.")
    print()

    # Create display
    display = LiveQuizDisplay()

    # Sample questions
    questions = [
        {
            'question_text': 'What is the capital of France?',
            'options': ['London', 'Berlin', 'Paris', 'Madrid']
        },
        {
            'question_text': 'What is 2 + 2?',
            'options': ['3', '4', '5', '6']
        },
        {
            'question_text': 'What is the largest planet?',
            'options': ['Earth', 'Mars', 'Jupiter', 'Saturn']
        }
    ]

    # Display quiz
    print("Starting display test...")
    print("Press Ctrl+C to exit early.")
    print()

    try:
        display.display_quiz(
            questions=questions,
            time_per_question=30,
            on_finish=lambda results: print(f"Finished! {results}"),
            on_question_change=lambda idx: None
        )
    except KeyboardInterrupt:
        print("\n✓ Test interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n✓ Test finished")

if __name__ == "__main__":
    test_no_scrolling()
