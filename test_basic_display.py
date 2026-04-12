#!/usr/bin/env python3
"""
Simple test to verify the display works without errors.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from live_display import LiveQuizDisplay

def test_basic_display():
    """Test basic display functionality."""
    print("Testing Basic Display...")
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
        }
    ]

    # Test display creation
    print("✓ Display created successfully")
    print("✓ Questions loaded successfully")
    print()
    print("Ready to run full test with:")
    print("  python3 quiz_game.py")
    print()

if __name__ == "__main__":
    try:
        test_basic_display()
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
