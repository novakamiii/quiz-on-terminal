#!/usr/bin/env python3
"""
Setup script to create a sample quiz for testing.
Run this to populate the database with example content.
"""

from database import QuizDatabase


def create_sample_quiz():
    """Create a sample quiz with various question types."""
    db = QuizDatabase()

    print("Creating sample quizzes...")

    # Create a general knowledge quiz (multiple choice)
    quiz_id = db.create_quiz(
        name="General Knowledge",
        description="Test your general knowledge with these questions!",
        time_per_question=20,
        quiz_type="multiple_choice"
    )

    print(f"Created quiz with ID: {quiz_id}")

    # Add multiple choice questions
    questions = [
        {
            "text": "What is the capital of France?",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "answer": "C",
            "points": 10
        },
        {
            "text": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "answer": "B",
            "points": 10
        },
        {
            "text": "What is the largest ocean on Earth?",
            "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
            "answer": "D",
            "points": 10
        },
        {
            "text": "Who wrote 'Romeo and Juliet'?",
            "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
            "answer": "B",
            "points": 10
        },
        {
            "text": "What is the chemical symbol for gold?",
            "options": ["Go", "Gd", "Au", "Ag"],
            "answer": "C",
            "points": 10
        }
    ]

    for q in questions:
        db.add_question(
            quiz_id,
            q["text"],
            "multiple_choice",
            q["options"],
            q["answer"],
            q["points"]
        )
        print(f"Added question: {q['text'][:30]}...")

    # Create an enumeration quiz
    enum_quiz_id = db.create_quiz(
        name="Programming Basics",
        description="Test your programming knowledge!",
        time_per_question=30,
        quiz_type="enumeration"
    )

    print(f"\nCreated enumeration quiz with ID: {enum_quiz_id}")

    enum_questions = [
        {
            "text": "What does HTML stand for?",
            "answer": "HyperText Markup Language",
            "points": 15
        },
        {
            "text": "What is the output of: print(2 ** 3)?",
            "answer": "8",
            "points": 10
        },
        {
            "text": "What keyword is used to define a function in Python?",
            "answer": "def",
            "points": 10
        }
    ]

    for q in enum_questions:
        db.add_question(
            enum_quiz_id,
            q["text"],
            "enumeration",
            None,
            q["answer"],
            q["points"]
        )
        print(f"Added question: {q['text'][:30]}...")

    # Create a mixed quiz (both types)
    mixed_quiz_id = db.create_quiz(
        name="Mixed Challenge",
        description="A quiz with both multiple choice and enumeration questions!",
        time_per_question=25,
        quiz_type="mixed"
    )

    print(f"\nCreated mixed quiz with ID: {mixed_quiz_id}")

    # Add mixed questions
    mixed_questions = [
        {
            "text": "What is 2 + 2?",
            "type": "multiple_choice",
            "options": ["3", "4", "5", "6"],
            "answer": "B",
            "points": 10
        },
        {
            "text": "What is the capital of Japan?",
            "type": "enumeration",
            "answer": "Tokyo",
            "points": 15
        },
        {
            "text": "Which programming language is known for its simplicity?",
            "type": "multiple_choice",
            "options": ["C++", "Java", "Python", "Assembly"],
            "answer": "C",
            "points": 10
        },
        {
            "text": "What does CPU stand for?",
            "type": "enumeration",
            "answer": "Central Processing Unit",
            "points": 20
        }
    ]

    for q in mixed_questions:
        db.add_question(
            mixed_quiz_id,
            q["text"],
            q["type"],
            q.get("options"),
            q["answer"],
            q["points"]
        )
        print(f"Added question: {q['text'][:30]}...")

    print("\n✓ Sample quizzes created successfully!")
    print("You can now run 'python quiz_game.py' to play.")
    print("\nAvailable quizzes:")
    print(f"  1. General Knowledge (ID: {quiz_id}) - Multiple Choice")
    print(f"  2. Programming Basics (ID: {enum_quiz_id}) - Enumeration")
    print(f"  3. Mixed Challenge (ID: {mixed_quiz_id}) - Mixed Types")

    db.close()


if __name__ == "__main__":
    try:
        create_sample_quiz()
    except Exception as e:
        print(f"Error creating sample quiz: {e}")
