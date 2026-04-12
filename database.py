"""
Database module for quiz game using SQLite.
Handles quiz storage, retrieval, and management.
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json


class QuizDatabase:
    """SQLite database manager for quiz game."""

    def __init__(self, db_path: str = "quiz_database.db"):
        self.db_path = db_path
        self.conn = None
        self._initialize_database()

    def _initialize_database(self):
        """Create database tables if they don't exist."""
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self):
        """Create all necessary tables."""
        cursor = self.conn.cursor()

        # Quizzes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                time_per_question INTEGER DEFAULT 30,
                quiz_type TEXT DEFAULT 'multiple_choice'
            )
        """)

        # Questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                question_type TEXT NOT NULL,
                options TEXT,
                correct_answer TEXT NOT NULL,
                points INTEGER DEFAULT 10,
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
            )
        """)

        # Quiz results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                player_name TEXT,
                score INTEGER,
                total_points INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    def create_quiz(self, name: str, description: str = "",
                    time_per_question: int = 30,
                    quiz_type: str = "multiple_choice") -> int:
        """Create a new quiz and return its ID."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO quizzes (name, description, time_per_question, quiz_type)
                VALUES (?, ?, ?, ?)
            """, (name, description, time_per_question, quiz_type))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Quiz with name '{name}' already exists")

    def add_question(self, quiz_id: int, question_text: str,
                     question_type: str, options: Optional[List[str]] = None,
                     correct_answer: str = "", points: int = 10) -> int:
        """Add a question to a quiz and return its ID."""
        cursor = self.conn.cursor()
        options_json = json.dumps(options) if options else None
        cursor.execute("""
            INSERT INTO questions (quiz_id, question_text, question_type, options, correct_answer, points)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (quiz_id, question_text, question_type, options_json, correct_answer, points))
        self.conn.commit()
        return cursor.lastrowid

    def get_quiz(self, quiz_id: int) -> Optional[Dict]:
        """Get quiz details by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'created_at': row[3],
                'time_per_question': row[4],
                'quiz_type': row[5]
            }
        return None

    def get_quiz_by_name(self, name: str) -> Optional[Dict]:
        """Get quiz details by name."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quizzes WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'created_at': row[3],
                'time_per_question': row[4],
                'quiz_type': row[5]
            }
        return None

    def get_all_quizzes(self) -> List[Dict]:
        """Get all available quizzes."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quizzes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [{
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'created_at': row[3],
            'time_per_question': row[4],
            'quiz_type': row[5]
        } for row in rows]

    def get_questions(self, quiz_id: int) -> List[Dict]:
        """Get all questions for a quiz."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE quiz_id = ? ORDER BY id", (quiz_id,))
        rows = cursor.fetchall()
        questions = []
        for row in rows:
            options = json.loads(row[4]) if row[4] else None
            questions.append({
                'id': row[0],
                'quiz_id': row[1],
                'question_text': row[2],
                'question_type': row[3],
                'options': options,
                'correct_answer': row[5],
                'points': row[6]
            })
        return questions

    def save_result(self, quiz_id: int, player_name: str, score: int, total_points: int):
        """Save quiz result."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO quiz_results (quiz_id, player_name, score, total_points)
            VALUES (?, ?, ?, ?)
        """, (quiz_id, player_name, score, total_points))
        self.conn.commit()

    def get_results(self, quiz_id: int) -> List[Dict]:
        """Get all results for a quiz."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM quiz_results WHERE quiz_id = ?
            ORDER BY completed_at DESC
        """, (quiz_id,))
        rows = cursor.fetchall()
        return [{
            'id': row[0],
            'quiz_id': row[1],
            'player_name': row[2],
            'score': row[3],
            'total_points': row[4],
            'completed_at': row[5]
        } for row in rows]

    def delete_quiz(self, quiz_id: int):
        """Delete a quiz and all its questions."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
        self.conn.commit()

    def update_quiz_time(self, quiz_id: int, time_per_question: int):
        """Update time per question for a quiz."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE quizzes SET time_per_question = ?
            WHERE id = ?
        """, (time_per_question, quiz_id))
        self.conn.commit()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Ensure connection is closed."""
        self.close()
