#!/usr/bin/env python3
"""
Test script to verify bug fixes.
"""

import sys
from database import QuizDatabase
from ui import QuizUI
from quiz_game import NeuralQuizSystem


def test_show_message_fix():
    """Test that show_message() is called with proper arguments."""
    print("Testing show_message() fix...")

    ui = QuizUI()

    # Test that show_message requires a message argument
    try:
        ui.show_message("Test message")
        print("✓ show_message() works with message argument")
    except TypeError as e:
        print(f"✗ show_message() failed: {e}")
        return False

    # Test that show_message() without arguments fails
    try:
        ui.show_message()
        print("✗ show_message() should require message argument")
        return False
    except TypeError:
        print("✓ show_message() correctly requires message argument")

    return True


def test_manage_quizzes_list():
    """Test that manage quizzes shows the quiz list."""
    print("\nTesting manage quizzes list display...")

    db = QuizDatabase()
    ui = QuizUI()

    quizzes = db.get_all_quizzes()

    if not quizzes:
        print("✗ No quizzes available for testing")
        return False

    print(f"✓ Found {len(quizzes)} quizzes")

    # Test that show_quiz_list works
    try:
        ui.show_quiz_list(quizzes)
        print("✓ show_quiz_list() works correctly")
    except Exception as e:
        print(f"✗ show_quiz_list() failed: {e}")
        return False

    db.close()
    return True


def test_display_quiz():
    """Test that display_quiz works without errors."""
    print("\nTesting display_quiz()...")

    db = QuizDatabase()
    ui = QuizUI()

    quizzes = db.get_all_quizzes()

    if not quizzes:
        print("✗ No quizzes available for testing")
        return False

    # Get first quiz
    quiz = quizzes[0]
    questions = db.get_questions(quiz['id'])

    if not questions:
        print("✗ Quiz has no questions")
        return False

    print(f"✓ Testing with quiz: {quiz['name']} ({len(questions)} questions)")

    # Test display_all_questions
    try:
        from quiz_game import NeuralQuizSystem
        app = NeuralQuizSystem()
        app.display_all_questions(quiz, questions)
        print("✓ display_all_questions() works")
    except Exception as e:
        print(f"✗ display_all_questions() failed: {e}")
        return False

    # Test show_all_answers
    try:
        app.show_all_answers(questions)
        print("✓ show_all_answers() works")
    except Exception as e:
        print(f"✗ show_all_answers() failed: {e}")
        return False

    db.close()
    return True


def main():
    """Run all tests."""
    print("=" * 50)
    print("BUG FIX VERIFICATION TESTS")
    print("=" * 50)

    tests = [
        ("show_message() Fix", test_show_message_fix),
        ("Manage Quizzes List", test_manage_quizzes_list),
        ("Display Quiz", test_display_quiz),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} test crashed: {e}")
            results.append((name, False))

    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All bug fixes verified!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
