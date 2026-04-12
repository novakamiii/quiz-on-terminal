"""
Quiz manager module for creating and managing quizzes.
Handles quiz creation, editing, and validation.
"""

from typing import List, Dict, Optional
from database import QuizDatabase


class QuizManager:
    """Manager for quiz creation and manipulation."""

    def __init__(self, db: QuizDatabase):
        self.db = db

    def create_interactive_quiz(self, ui) -> int:
        """Create a new quiz through interactive prompts."""
        ui.show_title("CREATE NEW QUIZ")

        # Get quiz name
        while True:
            name = ui.show_input_prompt("Enter quiz name: ")
            if not name:
                ui.show_error("Quiz name cannot be empty.")
                continue

            # Check if quiz already exists
            if self.db.get_quiz_by_name(name):
                ui.show_error("Quiz with this name already exists.")
                continue

            break

        # Get description
        description = ui.show_input_prompt("Enter quiz description (optional): ")

        # Get quiz type (now allows mixed types)
        ui.show_message("\nQuiz Types:")
        ui.show_message("1. Multiple Choice Only (A, B, C, D)")
        ui.show_message("2. Enumeration Only (text input)")
        ui.show_message("3. Mixed (both types in same quiz)")

        while True:
            choice = ui.show_input_prompt("Select quiz type [1-3]: ")
            if choice == "1":
                quiz_type = "multiple_choice"
                break
            elif choice == "2":
                quiz_type = "enumeration"
                break
            elif choice == "3":
                quiz_type = "mixed"
                break
            else:
                ui.show_error("Invalid choice.")

        # Get time per question
        while True:
            time_input = ui.show_input_prompt("Time per question in seconds (default 30): ")
            if not time_input:
                time_per_question = 30
                break

            try:
                time_per_question = int(time_input)
                if time_per_question > 0:
                    break
                ui.show_error("Time must be positive.")
            except ValueError:
                ui.show_error("Please enter a valid number.")

        # Create quiz
        quiz_id = self.db.create_quiz(name, description, time_per_question, quiz_type)
        ui.show_success(f"Quiz '{name}' created with ID: {quiz_id}")
        ui.wait_for_key()

        # Add questions
        self.add_questions_interactive(quiz_id, quiz_type, ui)

        return quiz_id

    def add_questions_interactive(self, quiz_id: int, quiz_type: str, ui):
        """Add questions to a quiz interactively."""
        ui.show_title("ADD QUESTIONS")

        question_count = 0

        while True:
            ui.clear_screen()
            ui.show_title(f"ADD QUESTION {question_count + 1}")

            # For mixed quizzes, ask for question type each time
            current_question_type = quiz_type
            if quiz_type == "mixed":
                ui.show_message("\nQuestion Type:")
                ui.show_message("1. Multiple Choice (A, B, C, D)")
                ui.show_message("2. Enumeration (text input)")

                while True:
                    type_choice = ui.show_input_prompt("Select question type [1-2]: ")
                    if type_choice == "1":
                        current_question_type = "multiple_choice"
                        break
                    elif type_choice == "2":
                        current_question_type = "enumeration"
                        break
                    else:
                        ui.show_error("Invalid choice.")

            # Get question text
            question_text = ui.show_input_prompt("Enter question text: ")
            if not question_text:
                ui.show_error("Question text cannot be empty.")
                continue

            # Get options for multiple choice
            options = None
            if current_question_type == "multiple_choice":
                ui.show_message("\nEnter 4 options (A, B, C, D):")
                options = []
                for i in range(4):
                    option = ui.show_input_prompt(f"  Option {chr(65 + i)}: ")
                    options.append(option)

                # Get correct answer
                while True:
                    correct = ui.show_input_prompt("Enter correct answer (A, B, C, D): ").upper()
                    if correct in ['A', 'B', 'C', 'D']:
                        correct_answer = correct
                        break
                    ui.show_error("Invalid option. Enter A, B, C, or D.")

            else:  # enumeration
                correct_answer = ui.show_input_prompt("Enter correct answer: ")

            # Get points
            while True:
                points_input = ui.show_input_prompt("Points for this question (default 10): ")
                if not points_input:
                    points = 10
                    break

                try:
                    points = int(points_input)
                    if points > 0:
                        break
                    ui.show_error("Points must be positive.")
                except ValueError:
                    ui.show_error("Please enter a valid number.")

            # Add question to database
            self.db.add_question(
                quiz_id,
                question_text,
                current_question_type,
                options,
                correct_answer,
                points
            )

            question_count += 1
            ui.show_success(f"Question {question_count} added!")

            # Ask if user wants to add more questions
            continue_adding = ui.show_input_prompt("\nAdd another question? (y/n): ").lower()
            if continue_adding != 'y':
                break

        ui.show_success(f"Total questions added: {question_count}")

    def edit_quiz_time(self, quiz_id: int, ui):
        """Edit the time per question for a quiz."""
        ui.clear_screen()
        quiz = self.db.get_quiz(quiz_id)
        if not quiz:
            ui.show_error("Quiz not found.")
            return

        ui.show_title(f"EDIT TIME - {quiz['name']}")
        ui.show_message(f"Current time per question: {quiz['time_per_question']}s")

        while True:
            time_input = ui.show_input_prompt("Enter new time per question in seconds: ")
            try:
                new_time = int(time_input)
                if new_time > 0:
                    self.db.update_quiz_time(quiz_id, new_time)
                    ui.show_success(f"Time updated to {new_time}s")
                    return
                ui.show_error("Time must be positive.")
            except ValueError:
                ui.show_error("Please enter a valid number.")

    def delete_quiz(self, quiz_id: int, ui):
        """Delete a quiz."""
        ui.clear_screen()
        quiz = self.db.get_quiz(quiz_id)
        if not quiz:
            ui.show_error("Quiz not found.")
            return

        ui.show_title(f"DELETE QUIZ - {quiz['name']}")
        ui.show_warning(f"Are you sure you want to delete '{quiz['name']}'?")
        ui.show_warning("This action cannot be undone!")

        confirm = ui.show_input_prompt("Type 'yes' to confirm: ").lower()
        if confirm == 'yes':
            self.db.delete_quiz(quiz_id)
            ui.show_success("Quiz deleted successfully.")
        else:
            ui.show_message("Deletion cancelled.")

    def view_quiz_details(self, quiz_id: int, ui):
        """View detailed information about a quiz."""
        ui.clear_screen()
        quiz = self.db.get_quiz(quiz_id)
        if not quiz:
            ui.show_error("Quiz not found.")
            return

        questions = self.db.get_questions(quiz_id)

        ui.show_title(f"QUIZ DETAILS - {quiz['name']}")

        ui.show_message(f"Description: {quiz['description'] or 'None'}")
        ui.show_message(f"Type: {quiz['quiz_type']}")
        ui.show_message(f"Time per question: {quiz['time_per_question']}s")
        ui.show_message(f"Total questions: {len(questions)}")
        ui.show_message(f"Created: {quiz['created_at']}")

        ui.show_message("\n--- Questions ---")
        for i, q in enumerate(questions, 1):
            ui.show_message(f"\n{i}. {q['question_text']}")
            if q['options']:
                for j, opt in enumerate(q['options'], 1):
                    ui.show_message(f"   {chr(64 + j)}. {opt}")
            ui.show_message(f"   Points: {q['points']}")

        total_points = sum(q['points'] for q in questions)
        ui.show_message(f"\nTotal possible points: {total_points}")

    def get_quiz_statistics(self, quiz_id: int) -> Dict:
        """Get statistics for a quiz."""
        quiz = self.db.get_quiz(quiz_id)
        questions = self.db.get_questions(quiz_id)
        results = self.db.get_results(quiz_id)

        return {
            'quiz_name': quiz['name'] if quiz else 'Unknown',
            'total_questions': len(questions),
            'total_points': sum(q['points'] for q in questions),
            'total_attempts': len(results),
            'average_score': sum(r['score'] for r in results) / len(results) if results else 0,
            'best_score': max(r['score'] for r in results) if results else 0
        }
