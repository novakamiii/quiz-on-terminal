#!/usr/bin/env python3
"""
Neural Quiz System - A terminal-based quiz game with techno/AI styling.
Supports multiple choice and enumeration quizzes with SQLite storage.
Paper mode: Students view questions on terminal and answer on paper.
"""

import sys
import os
from database import QuizDatabase
from ui import QuizUI
from quiz_manager import QuizManager
from live_display import SimpleQuizDisplay
from rich.text import Text
from rich.panel import Panel
from rich.layout import Layout
from rich import box


class NeuralQuizSystem:
    """Main application controller."""

    def __init__(self):
        self.db = QuizDatabase()
        self.ui = QuizUI()
        self.quiz_manager = QuizManager(self.db)
        self.running = True

    def run(self):
        """Main application loop."""
        self.ui.show_title("NEURAL QUIZ SYSTEM v1.0")
        self.ui.show_message("Initializing neural interface...")
        self.ui.wait_for_key()

        while self.running:
            self.show_main_menu()

        self.cleanup()

    def show_main_menu(self):
        """Display and handle main menu."""
        options = [
            f"{chr(0xF05F)} Display Quiz (Paper Mode)",  # fa-regular fa-book (U+F05F)
            f"{chr(0xF07E)} Create New Quiz",  # fa-regular fa-box-archive (U+F07E)
            f"{chr(0xF0C6)} Manage Quizzes",  # fa-regular fa-file-lines (U+F0C6)
            f"{chr(0xF05E)} Exit System",  # fa-regular fa-circle-xmark (U+F05E)
        ]

        choice = self.ui.show_menu(options, "MAIN MENU")

        if choice == 0:
            self.display_quiz_menu()
        elif choice == 1:
            self.create_quiz_menu()
        elif choice == 2:
            self.manage_quizzes_menu()
        elif choice == 3:
            self.exit_system()

    def display_quiz_menu(self):
        """Menu for displaying a quiz in paper mode."""
        self.ui.clear_screen()
        quizzes = self.db.get_all_quizzes()

        if not quizzes:
            self.ui.show_warning("No quizzes available!")
            self.ui.show_message("Create a quiz first from the main menu.")
            self.ui.wait_for_key()
            return

        self.ui.show_quiz_list(quizzes)

        while True:
            quiz_id_input = self.ui.show_input_prompt(
                "Enter quiz ID to display (or 0 to go back): "
            )

            if quiz_id_input == "0":
                return

            try:
                quiz_id = int(quiz_id_input)
                quiz = self.db.get_quiz(quiz_id)

                if quiz:
                    self.display_quiz(quiz_id)
                    return
                else:
                    self.ui.show_error("Quiz not found.")
            except ValueError:
                self.ui.show_error("Please enter a valid number.")

    def display_quiz(self, quiz_id: int):
        """Display a quiz in paper mode (students answer on paper)."""
        quiz = self.db.get_quiz(quiz_id)
        questions = self.db.get_questions(quiz_id)

        if not questions:
            self.ui.show_error("Quiz has no questions.")
            return

        self.ui.clear_screen()
        self.ui.show_title(f"QUIZ: {quiz['name']}")
        self.ui.show_message(f"Description: {quiz['description'] or 'None'}")
        self.ui.show_message(f"Total Questions: {len(questions)}")
        self.ui.show_message(f"Time per Question: {quiz['time_per_question']}s")

        # Ask display mode
        self.ui.show_message("\nDisplay Mode:")
        self.ui.show_message("1. Show all questions at once")
        self.ui.show_message("2. Show questions one by one")

        while True:
            mode_choice = self.ui.show_input_prompt("Select display mode [1-2]: ")
            if mode_choice == "1":
                self.display_all_questions(quiz, questions)
                break
            elif mode_choice == "2":
                self.display_questions_one_by_one(quiz, questions)
                break
            else:
                self.ui.show_error("Invalid choice.")

        # After quiz display, show answer key
        self.ui.show_message("\n" + "=" * 50)
        self.ui.show_message("QUIZ COMPLETE")
        self.ui.show_message("=" * 50)
        self.ui.wait_for_key()

        # Ask how to show answers
        self.ui.clear_screen()
        self.ui.show_title("ANSWER KEY")
        self.ui.show_message("How would you like to view the answers?")
        self.ui.show_message("1. Show answers one by one")
        self.ui.show_message("2. Show all answers at once")

        while True:
            answer_mode = self.ui.show_input_prompt(
                "Select answer display mode [1-2]: "
            )
            if answer_mode == "1":
                self.show_answers_one_by_one(questions)
                break
            elif answer_mode == "2":
                self.show_all_answers(questions)
                break
            else:
                self.ui.show_error("Invalid choice.")

    def display_all_questions(self, quiz: dict, questions: list):
        """Display all questions at once."""
        self.ui.clear_screen()
        self.ui.show_title(f"QUIZ: {quiz['name']}")
        self.ui.show_message(f"Description: {quiz['description'] or 'None'}")
        self.ui.show_message(f"Total Questions: {len(questions)}")
        self.ui.show_timer_display(quiz["time_per_question"])
        self.ui.show_message()
        self.ui.show_message(
            "Note: Use 'One by One' mode for countdown timer and auto-advance"
        )
        self.ui.show_message()

        for i, question in enumerate(questions, 1):
            self.ui.show_message(f"\n{'=' * 50}")
            self.ui.show_message(f"Question {i}/{len(questions)}")
            self.ui.show_message(f"{'=' * 50}")

            # Display question in large format
            self.ui.show_large_question(question["question_text"], i, len(questions))

            # Display options in large format
            if question["question_type"] == "multiple_choice" and question["options"]:
                self.ui.show_large_options(question["options"])
            else:
                self.ui.show_message("(Write your answer on paper)")

        self.ui.show_message(f"\n{'=' * 50}")
        self.ui.show_message(f"END OF QUIZ - {len(questions)} questions total")
        self.ui.show_message(f"{'=' * 50}")
        self.ui.wait_for_key()

    def display_questions_one_by_one(self, quiz: dict, questions: list):
        """Display questions one by one with navigation and countdown timer using Rich Live display."""
        from rich.console import Console

        console = Console()
        display = SimpleQuizDisplay()

        def on_finish(results):
            """Callback when quiz is finished."""
            self.ui.show_message(
                f"\nQuiz completed! Viewed {results['current_index'] + 1}/{results['total_questions']} questions"
            )

        def on_question_change(index):
            """Callback when question changes."""
            pass  # Can add logging or other actions here

        # Display the quiz with live updates
        display.display_quiz(
            questions=questions,
            time_per_question=quiz["time_per_question"],
            on_finish=on_finish,
            on_question_change=on_question_change,
        )

    def show_answers_one_by_one(self, questions: list):
        """Show answers one by one with navigation."""
        current_index = 0

        while True:
            self.ui.clear_screen()
            question = questions[current_index]

            # Header
            self.ui.show_title("ANSWER KEY")
            self.ui.show_message(f"Question {current_index + 1}/{len(questions)}")

            # Display question in large format
            self.ui.show_large_question(
                question["question_text"], current_index + 1, len(questions)
            )

            # Display answer in large format
            if question["question_type"] == "multiple_choice":
                answer_letter = question["correct_answer"]
                answer_index = ord(answer_letter) - ord("A")
                if question["options"] and answer_index < len(question["options"]):
                    answer_text = (
                        f"{answer_letter}. {question['options'][answer_index]}"
                    )
                else:
                    answer_text = answer_letter
            else:
                answer_text = question["correct_answer"]

            self.ui.show_large_answer(answer_text, "Correct Answer")

            self.ui.show_message(f"Points: {question['points']}")
            self.ui.show_message("Controls:")
            self.ui.show_message("  ← Previous answer")
            self.ui.show_message("  → Next answer")
            self.ui.show_message("  Q  Quit")

            # Get navigation input
            import sys
            import tty
            import termios

            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                char = sys.stdin.read(1)

                if char == "\x1b":
                    # Arrow key
                    next_char = sys.stdin.read(1)
                    if next_char == "[":
                        arrow_char = sys.stdin.read(1)
                        if arrow_char == "D":  # Left
                            if current_index > 0:
                                current_index -= 1
                        elif arrow_char == "C":  # Right
                            if current_index < len(questions) - 1:
                                current_index += 1
                elif char in ["q", "Q"]:
                    break
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    def show_all_answers(self, questions: list):
        """Show all answers at once."""
        self.ui.clear_screen()
        self.ui.show_title("ANSWER KEY - ALL QUESTIONS")

        for i, question in enumerate(questions, 1):
            self.ui.show_message(f"\n{'=' * 50}")
            self.ui.show_message(f"Question {i}: {question['question_text'][:50]}...")
            self.ui.show_message(f"{'=' * 50}")

            # Display answer in large format
            if question["question_type"] == "multiple_choice":
                answer_letter = question["correct_answer"]
                answer_index = ord(answer_letter) - ord("A")
                if question["options"] and answer_index < len(question["options"]):
                    answer_text = (
                        f"{answer_letter}. {question['options'][answer_index]}"
                    )
                else:
                    answer_text = answer_letter
            else:
                answer_text = question["correct_answer"]

            self.ui.show_large_answer(answer_text, "Answer")
            self.ui.show_message(f"Points: {question['points']}")

        self.ui.show_message(f"\n{'=' * 50}")
        self.ui.show_message(f"Total Questions: {len(questions)}")
        self.ui.show_message(f"Total Points: {sum(q['points'] for q in questions)}")
        self.ui.show_message(f"{'=' * 50}")
        self.ui.wait_for_key()

    def create_quiz_menu(self):
        """Menu for creating a new quiz."""
        self.ui.clear_screen()
        try:
            quiz_id = self.quiz_manager.create_interactive_quiz(self.ui)
            self.ui.show_success(f"Quiz created successfully! ID: {quiz_id}")
        except Exception as e:
            self.ui.show_error(f"Failed to create quiz: {e}")

        self.ui.wait_for_key()

    def manage_quizzes_menu(self):
        """Menu for managing existing quizzes."""
        self.ui.clear_screen()
        quizzes = self.db.get_all_quizzes()

        if not quizzes:
            self.ui.show_warning("No quizzes available!")
            self.ui.wait_for_key()
            return

        while True:
            self.ui.show_quiz_list(quizzes)

            options = [
                "View Quiz Details",
                "Edit Quiz Time",
                "Delete Quiz",
                "Back to Main Menu",
            ]

            choice = self.ui.show_menu(options, "MANAGE QUIZZES")

            if choice == 0:
                self.view_quiz_details_menu(quizzes)
            elif choice == 1:
                self.edit_quiz_time_menu(quizzes)
            elif choice == 2:
                self.delete_quiz_menu(quizzes)
            elif choice == 3:
                return

    def view_quiz_details_menu(self, quizzes: list):
        """Menu for viewing quiz details."""
        self.ui.clear_screen()
        self.ui.show_quiz_list(quizzes)
        quiz_id = self.select_quiz(quizzes, "view")
        if quiz_id:
            self.quiz_manager.view_quiz_details(quiz_id, self.ui)
            self.ui.wait_for_key()

    def edit_quiz_time_menu(self, quizzes: list):
        """Menu for editing quiz time."""
        self.ui.clear_screen()
        self.ui.show_quiz_list(quizzes)
        quiz_id = self.select_quiz(quizzes, "edit")
        if quiz_id:
            self.quiz_manager.edit_quiz_time(quiz_id, self.ui)
            self.ui.wait_for_key()

    def delete_quiz_menu(self, quizzes: list):
        """Menu for deleting a quiz."""
        self.ui.clear_screen()
        self.ui.show_quiz_list(quizzes)
        quiz_id = self.select_quiz(quizzes, "delete")
        if quiz_id:
            self.quiz_manager.delete_quiz(quiz_id, self.ui)
            self.ui.wait_for_key()

    def select_quiz(self, quizzes: list, action: str) -> int:
        """Helper to select a quiz from list."""
        quiz_id_input = self.ui.show_input_prompt(
            f"Enter quiz ID to {action} (or 0 to cancel): "
        )

        if quiz_id_input == "0":
            return None

        try:
            quiz_id = int(quiz_id_input)
            quiz = self.db.get_quiz(quiz_id)

            if quiz:
                return quiz_id
            else:
                self.ui.show_error("Quiz not found.")
                return None
        except ValueError:
            self.ui.show_error("Please enter a valid number.")
            return None

    def exit_system(self):
        """Exit the application."""
        self.ui.clear_screen()
        self.ui.show_title("SHUTTING DOWN")
        self.ui.show_message("Saving data...")
        self.ui.show_message("Closing neural interface...")
        self.ui.show_success("System shutdown complete.")

        self.running = False

    def cleanup(self):
        """Clean up resources."""
        self.db.close()


def main():
    """Main entry point."""
    try:
        app = NeuralQuizSystem()
        app.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
