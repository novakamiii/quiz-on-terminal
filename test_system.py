#!/usr/bin/env python3
"""
Test script to verify all components of the Neural Quiz System.
Run this to ensure everything is working correctly.
"""

import sys
import os


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from database import QuizDatabase
        from ui import QuizUI
        from quiz_manager import QuizManager
        from game import QuizGame
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_database():
    """Test database operations."""
    print("\nTesting database...")
    try:
        from database import QuizDatabase

        # Create a test database
        db = QuizDatabase("test_quiz.db")

        # Create a test quiz
        quiz_id = db.create_quiz(
            name="Test Quiz",
            description="A test quiz",
            time_per_question=10,
            quiz_type="multiple_choice"
        )
        print(f"✓ Created quiz with ID: {quiz_id}")

        # Add a test question
        question_id = db.add_question(
            quiz_id,
            "Test question?",
            "multiple_choice",
            ["A", "B", "C", "D"],
            "A",
            10
        )
        print(f"✓ Added question with ID: {question_id}")

        # Retrieve quiz
        quiz = db.get_quiz(quiz_id)
        assert quiz is not None, "Failed to retrieve quiz"
        assert quiz['name'] == "Test Quiz", "Quiz name mismatch"
        print("✓ Retrieved quiz successfully")

        # Retrieve questions
        questions = db.get_questions(quiz_id)
        assert len(questions) == 1, "Question count mismatch"
        print("✓ Retrieved questions successfully")

        # Save a result
        db.save_result(quiz_id, "TestPlayer", 10, 10)
        print("✓ Saved result successfully")

        # Get results
        results = db.get_results(quiz_id)
        assert len(results) == 1, "Result count mismatch"
        print("✓ Retrieved results successfully")

        # Cleanup
        db.delete_quiz(quiz_id)
        print("✓ Deleted quiz successfully")

        db.close()

        # Remove test database
        os.remove("test_quiz.db")
        print("✓ Database test passed")

        return True

    except Exception as e:
        print(f"✗ Database test failed: {e}")
        # Cleanup on failure
        if os.path.exists("test_quiz.db"):
            os.remove("test_quiz.db")
        return False


def test_ui():
    """Test UI components."""
    print("\nTesting UI...")
    try:
        from ui import QuizUI

        ui = QuizUI()
        print("✓ UI initialized successfully")

        # Test that UI methods exist
        assert hasattr(ui, 'show_title'), "Missing show_title method"
        assert hasattr(ui, 'show_menu'), "Missing show_menu method"
        assert hasattr(ui, 'show_question'), "Missing show_question method"
        assert hasattr(ui, 'show_results'), "Missing show_results method"
        print("✓ UI methods verified")

        return True

    except Exception as e:
        print(f"✗ UI test failed: {e}")
        return False


def test_quiz_manager():
    """Test quiz manager."""
    print("\nTesting quiz manager...")
    try:
        from database import QuizDatabase
        from quiz_manager import QuizManager

        db = QuizDatabase("test_quiz.db")
        manager = QuizManager(db)
        print("✓ Quiz manager initialized successfully")

        # Test that manager methods exist
        assert hasattr(manager, 'create_interactive_quiz'), "Missing create_interactive_quiz method"
        assert hasattr(manager, 'add_questions_interactive'), "Missing add_questions_interactive method"
        assert hasattr(manager, 'edit_quiz_time'), "Missing edit_quiz_time method"
        assert hasattr(manager, 'delete_quiz'), "Missing delete_quiz method"
        assert hasattr(manager, 'view_quiz_details'), "Missing view_quiz_details method"
        print("✓ Quiz manager methods verified")

        db.close()
        os.remove("test_quiz.db")

        return True

    except Exception as e:
        print(f"✗ Quiz manager test failed: {e}")
        if os.path.exists("test_quiz.db"):
            os.remove("test_quiz.db")
        return False


def test_game():
    """Test game components."""
    print("\nTesting game components...")
    try:
        from database import QuizDatabase
        from ui import QuizUI
        from game import QuizGame

        db = QuizDatabase("test_quiz.db")
        ui = QuizUI()
        game = QuizGame(db, ui)
        print("✓ Game initialized successfully")

        # Test that game methods exist
        assert hasattr(game, 'start_quiz'), "Missing start_quiz method"
        assert hasattr(game, 'play'), "Missing play method"
        assert hasattr(game, 'calculate_score'), "Missing calculate_score method"
        print("✓ Game methods verified")

        db.close()
        os.remove("test_quiz.db")

        return True

    except Exception as e:
        print(f"✗ Game test failed: {e}")
        if os.path.exists("test_quiz.db"):
            os.remove("test_quiz.db")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 50)
    print("NEURAL QUIZ SYSTEM - TEST SUITE")
    print("=" * 50)

    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("UI", test_ui),
        ("Quiz Manager", test_quiz_manager),
        ("Game", test_game),
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
        print("\n🎉 All tests passed! The system is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
