#!/usr/bin/env python3
"""
Simple test to verify Rich Live display UI is working correctly.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from live_display import LiveQuizDisplay
from rich.console import Console

def test_ui_layout():
    """Test the UI layout with various question types."""
    print("Testing Rich Live Display UI Layout...")

    # Test questions with different lengths
    test_questions = [
        {
            'question_text': 'Short question?',
            'options': ['A', 'B', 'C', 'D'],
            'question_type': 'multiple_choice',
            'correct_answer': 'A',
            'points': 10
        },
        {
            'question_text': 'This is a much longer question that should test how the UI handles text wrapping and display. It should not get cut off or distorted.',
            'options': [
                'This is a very long option that tests text wrapping',
                'Another long option to see how it displays',
                'Third option with more text',
                'Fourth option to complete the test'
            ],
            'question_type': 'multiple_choice',
            'correct_answer': 'B',
            'points': 10
        },
        {
            'question_text': 'Medium length question text here?',
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'question_type': 'multiple_choice',
            'correct_answer': 'C',
            'points': 10
        }
    ]

    console = Console()
    display = LiveQuizDisplay(console)

    print(f"\nTerminal size: {display.terminal_width}x{display.terminal_height}")

    # Test creating layouts for each question
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*50}")
        print(f"Testing Question {i}")
        print(f"{'='*50}")
        print(f"Question length: {len(question['question_text'])} chars")
        print(f"Options count: {len(question['options'])}")
        print(f"Option lengths: {[len(opt) for opt in question['options']]}")

        # Create layout
        layout = display.create_layout(
            question['question_text'],
            question['options'],
            30,  # time_remaining
            30,  # total_time
            i,
            len(test_questions),
            show_pause=True
        )

        # Render the layout
        console.print(layout)
        print(f"\n✓ Question {i} layout created successfully")

    print(f"\n{'='*50}")
    print("✓ All UI layout tests passed!")
    print(f"{'='*50}")

    return True

if __name__ == "__main__":
    try:
        success = test_ui_layout()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
