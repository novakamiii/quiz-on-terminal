"""
UI module for quiz game with techno/AI styled interface.
Uses rich library for terminal formatting and styling.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.box import Box, ROUNDED, DOUBLE, HEAVY
from rich.layout import Layout
from rich.live import Live
from rich import box
from typing import List, Optional
import time


class CustomBox(Box):
    """Custom box drawing characters for techno style."""

    def __init__(self):
        super().__init__("╭─╮│╰─╯", "─", "│", "│", "├─┤┴┬", "─", "│", "│")


class QuizUI:
    """Techno/AI styled UI for quiz game."""

    # Panel height constants for dynamic layout
    _TIMER_H = 2
    _CONTROLS_H = 2
    _MIN_MID_H = 3

    def __init__(self):
        self.console = Console()
        self.colors = {
            "primary": "#00ff00",  # Matrix green
            "secondary": "#00ffff",  # Cyan
            "accent": "#ff00ff",  # Magenta
            "warning": "#ffff00",  # Yellow
            "error": "#ff0000",  # Red
            "dim": "#666666",  # Gray
            "bg": "#0a0a0a",  # Dark background
        }

    def clear_screen(self):
        """Clear the terminal screen."""
        self.console.clear()

    def show_title(self, title: str = "NEURAL QUIZ SYSTEM"):
        """Display the main title with techno styling."""
        title_text = Text(title, style="bold cyan")
        title_text.stylize("blink", 0, len(title))
        panel = Panel(
            Align.center(title_text),
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 3),
        )
        self.console.print(panel)
        self.console.print()

    def show_menu(self, options: List[str], title: str = "MAIN MENU") -> int:
        """Display menu and return selected option."""
        self.clear_screen()
        self.show_title(title)

        table = Table(
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(0, 2),
        )
        table.add_column("Option", style="cyan", width=8)
        table.add_column("Action", style="white")

        for i, option in enumerate(options, 1):
            table.add_row(f"[{i}]", option)

        self.console.print(Align.center(table))
        self.console.print()

        while True:
            try:
                choice = input("Select option [1-{}]: ".format(len(options)))
                choice_int = int(choice)
                if 1 <= choice_int <= len(options):
                    return choice_int - 1
                self.console.print("[red]Invalid option. Try again.[/red]")
            except ValueError:
                self.console.print("[red]Please enter a number.[/red]")

    def show_question(
        self,
        question_num: int,
        total_questions: int,
        question_text: str,
        options: Optional[List[str]] = None,
        time_remaining: Optional[int] = None,
        question_type: str = "multiple_choice",
    ) -> str:
        """Display a question and return user's answer."""
        self.clear_screen()

        # Header with progress
        header = f"QUESTION {question_num}/{total_questions}"
        if time_remaining is not None:
            header += f" | TIME: {time_remaining}s"

        header_text = Text(header, style="bold cyan")
        self.console.print(
            Panel(header_text, box=box.ROUNDED, border_style="cyan", padding=(0, 1))
        )
        self.console.print()

        # Question - Make it larger
        question_text_large = Text(question_text, style="bold white on_black")
        question_panel = Panel(
            question_text_large, title="[QUESTION]", border_style="cyan", padding=(0, 1)
        )
        self.console.print(question_panel)
        self.console.print()

        # Options for multiple choice - Make them larger too
        if question_type == "multiple_choice" and options:
            options_table = Table(
                show_header=False, box=box.SIMPLE, border_style="cyan", padding=(0, 1)
            )
        self.console.print()

        # Question - Make it larger
        question_text_large = Text(question_text, style="bold white on_black")
        question_panel = Panel(
            question_text_large, title="[QUESTION]", border_style="cyan", padding=(0, 2)
        )
        self.console.print(question_panel)
        self.console.print()

        # Options for multiple choice - Make them larger too
        if question_type == "multiple_choice" and options:
            options_table = Table(
                show_header=False, box=box.SIMPLE, border_style="cyan", padding=(0, 2)
            )
            options_table.add_column("Key", style="bold cyan", width=6)
            options_table.add_column("Option", style="bold white")

            for i, option in enumerate(options, 1):
                key = chr(64 + i)  # A, B, C, D
                options_table.add_row(f"[{key}]", option)

            self.console.print(Align.center(options_table))
            self.console.print()

        # Instructions
        if question_type == "multiple_choice":
            instructions = "Enter your answer (A, B, C, D) or use ← → to navigate"
        else:
            instructions = "Type your answer or use ← → to navigate"

        self.console.print(Align.center(Text(instructions, style="dim")))
        self.console.print()

        return input("Your answer: ").strip().upper()

    def show_results(
        self,
        score: int,
        total_points: int,
        correct_answers: int,
        total_questions: int,
        time_taken: float,
    ):
        """Display quiz results."""
        self.clear_screen()
        self.show_title("QUIZ COMPLETE")

        percentage = (score / total_points * 100) if total_points > 0 else 0

        results_table = Table(
            show_header=True,
            header_style="bold cyan",
            box=box.DOUBLE,
            border_style="cyan",
            padding=(0, 2),
        )
        results_table.add_column("Metric", style="cyan", width=20)
        results_table.add_column("Value", style="white")

        results_table.add_row("Score", f"{score}/{total_points}")
        results_table.add_row("Percentage", f"{percentage:.1f}%")
        results_table.add_row("Correct Answers", f"{correct_answers}/{total_questions}")
        results_table.add_row("Time Taken", f"{time_taken:.1f}s")

        self.console.print(Align.center(results_table))
        self.console.print()

        # Performance message
        if percentage >= 80:
            message = "🎯 EXCELLENT! Neural pathways optimized!"
            style = "bold green"
        elif percentage >= 60:
            message = "⚡ GOOD! System functioning within parameters."
            style = "bold yellow"
        elif percentage >= 40:
            message = "⚠️ ADEQUATE. Recalibration recommended."
            style = "bold orange"
        else:
            message = "🔴 CRITICAL. System requires immediate attention."
            style = "bold red"

        self.console.print(Align.center(Text(message, style=style)))
        self.console.print()

    def show_quiz_list(self, quizzes: List[dict]):
        """Display list of available quizzes."""
        self.clear_screen()
        self.show_title("AVAILABLE QUIZZES")

        if not quizzes:
            self.console.print(
                Align.center(Text("No quizzes available.", style="yellow"))
            )
            self.console.print()
            return

        table = Table(
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(0, 2),
        )
        table.add_column("ID", style="cyan", width=4)
        table.add_column("Name", style="white", width=30)
        table.add_column("Type", style="cyan", width=15)
        table.add_column("Time/Question", style="cyan", width=15)

        for quiz in quizzes:
            table.add_row(
                str(quiz["id"]),
                quiz["name"],
                quiz["quiz_type"],
                f"{quiz['time_per_question']}s",
            )

        self.console.print(Align.center(table))
        self.console.print()

    def show_input_prompt(self, prompt: str) -> str:
        """Show input prompt and return user input."""
        self.console.print(f"[cyan]{prompt}[/cyan]", end=" ")
        return input().strip()

    def show_message(self, message: str = "", style: str = "white"):
        """Display a message."""
        self.console.print(f"[{style}]{message}[/{style}]")

    def show_error(self, message: str):
        """Display an error message."""
        self.console.print(f"[red]ERROR: {message}[/red]")

    def show_success(self, message: str):
        """Display a success message."""
        self.console.print(f"[green]✓ {message}[/green]")

    def show_warning(self, message: str):
        """Display a warning message."""
        self.console.print(f"[yellow]⚠ {message}[/yellow]")

    def show_loading(self, message: str = "Processing..."):
        """Show loading animation."""
        self.console.print(f"[cyan]⏳ {message}[/cyan]")

    def show_progress(self, current: int, total: int, message: str = ""):
        """Show progress bar."""
        percentage = (current / total * 100) if total > 0 else 0
        bar_length = 40
        filled = int(bar_length * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)

        self.console.print(f"[cyan]{message}[/cyan]")
        self.console.print(f"[cyan][{bar}] {percentage:.0f}%[/cyan]")

    def wait_for_key(self, message: str = "Press any key to continue..."):
        """Wait for user to press a key."""
        self.console.print(f"[dim]{message}[/dim]")
        input()

    def show_timer_warning(self, time_remaining: int):
        """Show warning when time is running low."""
        if time_remaining <= 5:
            self.console.print(
                f"[red blink]⏰ TIME RUNNING LOW: {time_remaining}s![/red blink]"
            )

    def show_large_text(self, text: str, style: str = "bold white"):
        """Display text in large format."""
        large_text = Text(text, style=style)
        self.console.print(large_text)

    def show_large_question(
        self, question_text: str, question_num: int = None, total_questions: int = None
    ):
        """Display a question in large format."""
        # Large question text
        question_large = Text(question_text, style="bold white on_black")
        question_panel = Panel(
            question_large, title="[QUESTION]", border_style="cyan", padding=(0, 1)
        )
        self.console.print(question_panel)
        self.console.print()

    def show_large_answer(self, answer_text: str, label: str = "Answer"):
        """Display an answer in large format."""
        answer_large = Text(answer_text, style="bold green on_black")
        answer_panel = Panel(
            answer_large, title=f"[{label}]", border_style="green", padding=(0, 1)
        )
        self.console.print(answer_panel)
        self.console.print()

    def show_timer_display(
        self,
        time_per_question: int,
        current_question: int = None,
        total_questions: int = None,
    ):
        """Display timer information for paper mode."""
        timer_text = f"⏱️  Time per Question: {time_per_question} seconds"
        if current_question is not None and total_questions is not None:
            timer_text += f" | Question {current_question}/{total_questions}"

        timer_panel = Panel(
            Text(timer_text, style="bold yellow"),
            box=box.ROUNDED,
            border_style="yellow",
            padding=(0, 1),
        )
        self.console.print(timer_panel)
        self.console.print()

    def get_countdown_timer_text(
        self, time_remaining: int, current_question: int, total_questions: int
    ):
        """Get countdown timer text without displaying it."""
        # Color based on time remaining
        if time_remaining <= 5:
            style = "bold red blink"
        elif time_remaining <= 10:
            style = "bold yellow"
        else:
            style = "bold green"

        return Text(
            f"⏱️  Time Remaining: {time_remaining}s | Question {current_question}/{total_questions}",
            style=style,
        )

    def show_countdown_timer(
        self, time_remaining: int, current_question: int, total_questions: int
    ):
        """Display countdown timer with remaining time."""
        timer_text = self.get_countdown_timer_text(
            time_remaining, current_question, total_questions
        )

        # Color border based on time remaining
        if time_remaining <= 5:
            border_style = "red"
        elif time_remaining <= 10:
            border_style = "yellow"
        else:
            border_style = "green"

        timer_panel = Panel(
            timer_text, box=box.DOUBLE, border_style=border_style, padding=(0, 1)
        )
        self.console.print(timer_panel)
        self.console.print()

    def show_large_options(self, options: List[str]):
        """Display options in large format."""
        options_table = Table(
            show_header=False, box=box.SIMPLE, border_style="cyan", padding=(0, 1)
        )
        options_table.add_column("Key", style="bold cyan", width=6)
        options_table.add_column("Option", style="bold white")

        for i, option in enumerate(options, 1):
            key = chr(64 + i)  # A, B, C, D
            options_table.add_row(f"[{key}]", option)

        self.console.print(Align.center(options_table))
        self.console.print()

    def create_timer_panel(
        self, time_remaining: int, current_question: int, total_questions: int
    ) -> Panel:
        """Create a timer panel for live display."""
        # Color based on time remaining
        if time_remaining <= 5:
            style = "bold red blink"
            border_style = "red"
        elif time_remaining <= 10:
            style = "bold yellow"
            border_style = "yellow"
        else:
            style = "bold green"
            border_style = "green"

        timer_text = Text(
            f"⏱️  Time Remaining: {time_remaining}s | Question {current_question}/{total_questions}",
            style=style,
        )

        return Panel(
            timer_text, box=box.DOUBLE, border_style=border_style, padding=(0, 1)
        )

    def create_question_layout(
        self,
        quiz_name: str,
        question_text: str,
        question_num: int,
        total_questions: int,
        options: Optional[List[str]] = None,
        question_type: str = "multiple_choice",
        time_remaining: int = 30,
    ) -> Group:
        """Create a complete question layout for live display with compact sizing."""
        from rich.console import Group

        # Timer panel
        timer_panel = self.create_timer_panel(
            time_remaining, question_num, total_questions
        )

        # Question panel
        question_large = Text(question_text, style="bold white on_black")
        question_panel = Panel(
            question_large,
            title=f"[QUESTION {question_num}/{total_questions}]",
            border_style="cyan",
            padding=(0, 1),
        )

        # Options
        if question_type == "multiple_choice" and options:
            options_table = Table(
                show_header=False, box=box.SIMPLE, border_style="cyan", padding=(0, 1)
            )
            options_table.add_column("Key", style="bold cyan", width=6)
            options_table.add_column("Option", style="bold white")

            for i, option in enumerate(options, 1):
                key = chr(64 + i)  # A, B, C, D
                options_table.add_row(f"[{key}]", option)

            options_renderable = Align.center(options_table)
        else:
            options_renderable = Text("(Write your answer on paper)", style="dim")

        # Controls
        controls_text = Text()
        controls_text.append("Controls: ", style="bold cyan")
        controls_text.append("← ", style="white")
        controls_text.append("Previous  ", style="dim")
        controls_text.append("→ ", style="white")
        controls_text.append("Next  ", style="dim")
        controls_text.append("F ", style="white")
        controls_text.append("Finish  ", style="dim")
        controls_text.append("⏱️ Auto-advance when timer expires", style="yellow")

        # Use Group to stack panels without forcing expansion
        return Group(
            timer_panel,
            question_panel,
            Align.center(options_renderable),
            Align.center(controls_text),
        )

    def build_timer_panel(
        self, time_remaining: int, current_question: int, total_questions: int
    ) -> Panel:
        """Build timer panel for live display."""
        # Color based on time remaining
        if time_remaining <= 5:
            style = "bold red blink"
            border_style = "red"
        elif time_remaining <= 10:
            style = "bold yellow"
            border_style = "yellow"
        else:
            style = "bold green"
            border_style = "green"

        timer_text = Text(
            f"⏱️  Time Remaining: {time_remaining}s | Question {current_question}/{total_questions}",
            style=style,
        )

        return Panel(
            timer_text, box=box.DOUBLE, border_style=border_style, padding=(0, 1)
        )

    def build_question_display(
        self,
        question_text: str,
        options: Optional[List[str]],
        current_question: int,
        total_questions: int,
        time_remaining: int,
        quiz_name: str = "QUIZ",
    ) -> Panel:
        """Build complete question display for live rendering."""
        from rich.layout import Layout

        layout = Layout()

        # Timer section
        timer_panel = self.build_timer_panel(
            time_remaining, current_question, total_questions
        )

        # Question section
        question_panel = Panel(
            Text(question_text, style="bold white on_black"),
            title="[QUESTION]",
            border_style="cyan",
            padding=(0, 1),
        )

        # Options section
        if options:
            options_table = Table(
                show_header=False, box=box.SIMPLE, border_style="cyan", padding=(0, 1)
            )
            options_table.add_column("Key", style="bold cyan", width=6)
            options_table.add_column("Option", style="bold white")

            for i, option in enumerate(options, 1):
                key = chr(64 + i)
                options_table.add_row(f"[{key}]", option)

            options_renderable = Align.center(options_table)
        else:
            options_renderable = Text("(Write your answer on paper)", style="dim")

        # Instructions
        instructions = Text(
            "← Previous | → Next | F Finish | ⏱️ Auto-advance on timeout", style="dim"
        )

        # Combine all sections
        from rich.console import Group

        content = Group(
            timer_panel,
            Text(),
            question_panel,
            Text(),
            options_renderable,
            Text(),
            Align.center(instructions),
        )

        return Panel(
            content,
            title=f"[bold cyan]{quiz_name}[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
