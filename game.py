"""
Main game module for quiz gameplay.
Handles question navigation, timing, and scoring.
"""

import time
import threading
from typing import List, Dict, Optional
from database import QuizDatabase
from ui import QuizUI


class QuizGame:
    """Main game controller for quiz gameplay."""

    def __init__(self, db: QuizDatabase, ui: QuizUI):
        self.db = db
        self.ui = ui
        self.current_quiz_id = None
        self.current_question_index = 0
        self.questions = []
        self.answers = {}  # Store user answers: {question_index: answer}
        self.score = 0
        self.start_time = None
        self.end_time = None
        self.timer_thread = None
        self.time_remaining = 0
        self.timer_running = False
        self.timer_lock = threading.Lock()

    def start_quiz(self, quiz_id: int, player_name: str = "Player"):
        """Start a quiz session."""
        quiz = self.db.get_quiz(quiz_id)
        if not quiz:
            self.ui.show_error("Quiz not found.")
            return False

        self.current_quiz_id = quiz_id
        self.questions = self.db.get_questions(quiz_id)
        self.current_question_index = 0
        self.answers = {}
        self.score = 0
        self.start_time = time.time()
        self.time_per_question = quiz['time_per_question']
        self.quiz_type = quiz['quiz_type']

        if not self.questions:
            self.ui.show_error("Quiz has no questions.")
            return False

        return True

    def play(self):
        """Main game loop."""
        if not self.questions:
            return

        self.ui.show_title("STARTING QUIZ")
        self.ui.show_message(f"Total questions: {len(self.questions)}")
        self.ui.show_message(f"Time per question: {self.time_per_question}s")
        self.ui.show_message(f"Quiz type: {self.quiz_type}")
        self.ui.show_message("\nControls:")
        self.ui.show_message("  • Answer the question to proceed")
        self.ui.show_message("  • Use ← → arrow keys to navigate")
        self.ui.show_message("  • Time resets when going back")
        self.ui.show_message("  • Time is ignored when skipping forward")
        self.ui.wait_for_key()

        while True:
            self.display_current_question()

            # Get user input
            user_answer = self.get_user_input()

            if user_answer == "QUIT":
                break
            elif user_answer == "NEXT":
                self.go_to_next_question()
            elif user_answer == "PREV":
                self.go_to_previous_question()
            elif user_answer == "FINISH":
                if self.finish_quiz():
                    break
            else:
                # User provided an answer
                self.answers[self.current_question_index] = user_answer
                self.go_to_next_question()

        self.end_time = time.time()

    def display_current_question(self):
        """Display the current question with timer."""
        question = self.questions[self.current_question_index]
        question_num = self.current_question_index + 1
        total_questions = len(self.questions)

        # Start timer for this question
        self.start_timer()

        # Display question
        self.ui.show_question(
            question_num,
            total_questions,
            question['question_text'],
            question['options'],
            self.time_remaining,
            question['question_type']
        )

    def start_timer(self):
        """Start the timer for the current question."""
        with self.timer_lock:
            self.timer_running = False
            if self.timer_thread:
                self.timer_thread.join(timeout=0.1)

            self.time_remaining = self.time_per_question
            self.timer_running = True
            self.timer_thread = threading.Thread(target=self._timer_worker)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def _timer_worker(self):
        """Timer worker thread."""
        while self.timer_running and self.time_remaining > 0:
            time.sleep(1)
            with self.timer_lock:
                if self.timer_running:
                    self.time_remaining -= 1

    def stop_timer(self):
        """Stop the timer."""
        with self.timer_lock:
            self.timer_running = False
            if self.timer_thread:
                self.timer_thread.join(timeout=0.1)

    def get_user_input(self) -> str:
        """Get user input with arrow key support."""
        import sys
        import tty
        import termios

        # Save terminal settings
        old_settings = termios.tcgetattr(sys.stdin)

        try:
            tty.setraw(sys.stdin.fileno())

            while True:
                char = sys.stdin.read(1)

                # Check for arrow keys (escape sequence)
                if char == '\x1b':
                    # Read next two characters
                    next_char = sys.stdin.read(1)
                    if next_char == '[':
                        arrow_char = sys.stdin.read(1)
                        if arrow_char == 'C':  # Right arrow
                            self.stop_timer()
                            return "NEXT"
                        elif arrow_char == 'D':  # Left arrow
                            self.stop_timer()
                            return "PREV"

                # Check for quit
                elif char == 'q' or char == 'Q':
                    self.stop_timer()
                    return "QUIT"

                # Check for finish
                elif char == 'f' or char == 'F':
                    self.stop_timer()
                    return "FINISH"

                # Regular input
                elif char in ['A', 'B', 'C', 'D', 'a', 'b', 'c', 'd']:
                    self.stop_timer()
                    return char.upper()

                # Enter key
                elif char == '\r' or char == '\n':
                    # For enumeration, we need to read the full line
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    answer = input().strip()
                    tty.setraw(sys.stdin.fileno())
                    self.stop_timer()
                    return answer

        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    def go_to_next_question(self):
        """Navigate to the next question."""
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
        else:
            # Last question, ask if user wants to finish
            self.ui.show_warning("This is the last question.")
            self.ui.show_message("Press 'F' to finish or answer to submit.")

    def go_to_previous_question(self):
        """Navigate to the previous question (resets timer)."""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            # Timer will reset when display_current_question is called
        else:
            self.ui.show_warning("This is the first question.")

    def finish_quiz(self) -> bool:
        """Finish the quiz and calculate score."""
        # Check if all questions are answered
        unanswered = [i for i in range(len(self.questions)) if i not in self.answers]

        if unanswered:
            self.ui.show_warning(f"You have {len(unanswered)} unanswered question(s).")
            proceed = self.ui.show_input_prompt("Finish anyway? (y/n): ").lower()
            if proceed != 'y':
                return False

        # Calculate score
        self.calculate_score()

        # Display results
        time_taken = self.end_time - self.start_time if self.end_time else 0
        total_points = sum(q['points'] for q in self.questions)
        correct_count = sum(1 for i, q in enumerate(self.questions)
                          if i in self.answers and self.answers[i] == q['correct_answer'])

        self.ui.show_results(
            self.score,
            total_points,
            correct_count,
            len(self.questions),
            time_taken
        )

        # Save result to database
        player_name = self.ui.show_input_prompt("Enter your name: ")
        self.db.save_result(self.current_quiz_id, player_name, self.score, total_points)

        self.ui.show_success("Result saved!")
        self.ui.wait_for_key()

        return True

    def calculate_score(self):
        """Calculate the final score based on answers."""
        self.score = 0

        for i, question in enumerate(self.questions):
            if i in self.answers:
                user_answer = self.answers[i]
                correct_answer = question['correct_answer']

                if user_answer == correct_answer:
                    self.score += question['points']

    def get_score(self) -> int:
        """Get current score."""
        return self.score

    def get_time_taken(self) -> float:
        """Get total time taken."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0

    def cleanup(self):
        """Clean up resources."""
        self.stop_timer()
