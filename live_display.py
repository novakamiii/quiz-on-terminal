#!/usr/bin/env python3
"""
Rich Live implementation for quiz display with cross-platform support.
"""

import sys
import time
import threading
import platform
from typing import Optional, Callable
from rich.live import Live
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich import box


class CrossPlatformInput:
    """Cross-platform keyboard input handler."""

    def __init__(self):
        self.system = platform.system()
        self.old_settings = None

    def setup(self):
        if self.system == "Windows":
            try:
                import msvcrt

                self.msvcrt = msvcrt
            except ImportError:
                raise RuntimeError("msvcrt not available on Windows")
        else:
            import termios, tty

            self.termios = termios
            self.tty = tty
            try:
                self.old_settings = termios.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin.fileno())
            except termios.error as e:
                raise RuntimeError(f"Cannot set terminal to raw mode: {e}")

    def get_key(self) -> Optional[str]:
        try:
            if self.system == "Windows":
                if self.msvcrt.kbhit():
                    return self.msvcrt.getch().decode("utf-8")
            else:
                import select

                if select.select([sys.stdin], [], [], 0)[0]:
                    return sys.stdin.read(1)
        except Exception:
            pass
        return None

    def cleanup(self):
        if self.system != "Windows" and self.old_settings:
            self.termios.tcsetattr(sys.stdin, self.termios.TCSADRAIN, self.old_settings)


class LiveQuizDisplay:
    """Live quiz display with dynamic layout scaling."""

    # These are the true rendered heights of the pinned panels.
    # Formula: 1 top-border + 0 v-pad + 1 content + 0 v-pad + 1 bot-border = 3
    # (padding=(0, 2) means no vertical padding)
    _TIMER_H = 2
    _CONTROLS_H = 2
    # Minimum rows to give the two flexible middle panels so they don't collapse
    _MIN_MID_H = 3

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.input_handler = CrossPlatformInput()

    # ------------------------------------------------------------------
    # Panel builders
    # ------------------------------------------------------------------

    def _urgency(self, t: int):
        if t <= 5:
            return "bold red blink", "red", "red"
        if t <= 10:
            return "bold yellow", "yellow", "yellow"
        return "bold green", "green", "green"

    def create_timer_panel(
        self,
        time_remaining: int,
        total_time: int,
        current_question: int,
        total_questions: int,
        paused: bool = False,
    ) -> Panel:
        """
        Timer panel - simplified without progress bar to prevent visual artifacts.
        """
        ts, bs, _ = self._urgency(time_remaining)

        timer_text = f"Q{current_question}/{total_questions} | Time: {time_remaining}s"
        if paused:
            timer_text += " [PAUSED]"

        t = Text(timer_text, style=ts)

        return Panel(t, box=box.ROUNDED, border_style=bs, padding=(0, 1))

    def create_question_panel(
        self, question_text: str, current_q: int, total_q: int
    ) -> Panel:
        return Panel(
            Text(question_text, style="bold white"),
            title=f"[cyan]Q{current_q}/{total_q}[/cyan]",
            border_style="cyan",
            padding=(0, 1),
        )

    def create_options_panel(self, options: Optional[list]) -> Panel:
        if options:
            t = Text()
            for i, opt in enumerate(options):
                t.append(f"{chr(65 + i)}. ", style="bold cyan")
                t.append(
                    str(opt) + ("\n" if i < len(options) - 1 else ""),
                    style="bold white",
                )
            body = t
        else:
            body = Text("Write answer on paper", style="dim italic")
        return Panel(body, box=box.SIMPLE, border_style="dim", padding=(0, 1))

    def create_controls_panel(self) -> Panel:
        t = Text(justify="center")
        for label, style in [
            ("◀ Prev", "bold cyan"),
            ("│", "dim"),
            ("▶ Next", "bold cyan"),
            ("│", "dim"),
            ("1-9 Jump", "bold cyan"),
            ("│", "dim"),
            ("P Pause", "bold yellow"),
            ("│", "dim"),
            ("F Finish", "bold green"),
            ("│", "dim"),
            ("Q Quit", "bold red"),
        ]:
            t.append(label, style=style)
        return Panel(t, box=box.SIMPLE, border_style="dim", padding=(0, 1))

    # ------------------------------------------------------------------
    # Dynamic layout — recalculated fresh on every render call
    # ------------------------------------------------------------------

    def _build_display(
        self, questions: list, state: dict, time_per_question: int
    ) -> Group:
        """
        Build a compact display using Group without outer Panel.
        This prevents the appending issue and ensures proper content replacement.
        """
        from rich.console import Group

        idx = state["current_index"]
        question = questions[idx]

        # Build panels
        timer_p = self.create_timer_panel(
            state["time_remaining"],
            time_per_question,
            idx + 1,
            len(questions),
            paused=state["paused"],
        )
        question_p = self.create_question_panel(
            question["question_text"], idx + 1, len(questions)
        )
        options_p = self.create_options_panel(question.get("options"))
        controls_p = self.create_controls_panel()

        # Group all content together without outer Panel
        return Group(
            timer_p,
            question_p,
            options_p,
            controls_p,
        )

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def display_quiz(
        self,
        questions: list,
        time_per_question: int,
        on_finish: Optional[Callable] = None,
        on_question_change: Optional[Callable] = None,
    ) -> dict:

        state = {
            "current_index": 0,
            "time_remaining": time_per_question,
            "timer_running": True,
            "action": None,
            "paused": False,
        }
        state_lock = threading.Lock()

        def get_display():
            return self._build_display(questions, state, time_per_question)

        # ---- timer thread ------------------------------------------------
        def timer_worker():
            while state["timer_running"]:
                time.sleep(1)
                with state_lock:
                    if (
                        state["timer_running"]
                        and not state["paused"]
                        and state["time_remaining"] > 0
                    ):
                        state["time_remaining"] -= 1
                        if state["time_remaining"] <= 0:
                            state["action"] = "NEXT"

        # ---- input setup -------------------------------------------------
        try:
            self.input_handler.setup()
            input_ok = True
        except Exception as e:
            self.console.print(f"[yellow]Warning: raw input unavailable: {e}[/yellow]")
            input_ok = False

        timer_thread = threading.Thread(target=timer_worker, daemon=True)
        timer_thread.start()

        # ---- display loop ------------------------------------------------
        try:
            # Use auto_refresh=False and manually control updates to prevent
            # content from being appended instead of replaced
            with Live(
                get_display(),
                console=self.console,
                auto_refresh=False,
                refresh_per_second=10,
            ) as live:
                while True:
                    # Timer-driven advance
                    advance = False
                    with state_lock:
                        if state["action"] == "NEXT":
                            state["action"] = None
                            if state["current_index"] < len(questions) - 1:
                                state["current_index"] += 1
                                state["time_remaining"] = time_per_question
                                advance = True
                            else:
                                state["timer_running"] = False
                                break

                    if advance:
                        if on_question_change:
                            on_question_change(state["current_index"])
                        live.update(get_display(), refresh=True)
                        continue

                    # Keyboard input
                    if input_ok:
                        key = self.input_handler.get_key()
                        if key == "\x1b":
                            # Arrow key prefix - read remaining characters
                            nk = self.input_handler.get_key()
                            if nk == "[":
                                ak = self.input_handler.get_key()
                                changed = False
                                with state_lock:
                                    if ak == "D":  # Left arrow - previous
                                        if state["current_index"] > 0:
                                            state["current_index"] -= 1
                                            state["time_remaining"] = time_per_question
                                            changed = True
                                    elif ak == "C":  # Right arrow - next
                                        if state["current_index"] < len(questions) - 1:
                                            state["current_index"] += 1
                                            state["time_remaining"] = time_per_question
                                            changed = True
                                    elif ak == "H":  # Home
                                        state["current_index"] = 0
                                        state["time_remaining"] = time_per_question
                                        changed = True
                                    elif ak == "F":  # End
                                        state["current_index"] = len(questions) - 1
                                        state["time_remaining"] = time_per_question
                                        changed = True
                                if changed:
                                    if on_question_change:
                                        on_question_change(state["current_index"])
                                    live.update(get_display(), refresh=True)
                            elif nk == "O":
                                # Some terminals use this for Home/End
                                ak = self.input_handler.get_key()
                                changed = False
                                with state_lock:
                                    if ak == "H":  # Home
                                        state["current_index"] = 0
                                        state["time_remaining"] = time_per_question
                                        changed = True
                                    elif ak == "F":  # End
                                        state["current_index"] = len(questions) - 1
                                        state["time_remaining"] = time_per_question
                                        changed = True
                                if changed:
                                    if on_question_change:
                                        on_question_change(state["current_index"])
                                    live.update(get_display(), refresh=True)
                        elif key and key.lower() == "f":
                            with state_lock:
                                state["timer_running"] = False
                            break
                        elif key and key.lower() == "p":
                            with state_lock:
                                state["paused"] = not state["paused"]
                            live.update(get_display(), refresh=True)
                        elif key and key.lower() == "q":
                            with state_lock:
                                state["timer_running"] = False
                            break
                        elif key and key.isdigit():
                            # Number key to jump to question (1-9)
                            q_num = int(key)
                            if 1 <= q_num <= min(9, len(questions)):
                                with state_lock:
                                    state["current_index"] = q_num - 1
                                    state["time_remaining"] = time_per_question
                                if on_question_change:
                                    on_question_change(state["current_index"])
                                live.update(get_display(), refresh=True)

                    # Push updated state every tick so the timer updates
                    live.update(get_display(), refresh=True)
                    time.sleep(0.1)

        finally:
            with state_lock:
                state["timer_running"] = False
            timer_thread.join(timeout=1)
            if input_ok:
                self.input_handler.cleanup()

        results = {
            "current_index": state["current_index"],
            "total_questions": len(questions),
            "completed": state["current_index"] == len(questions) - 1,
        }
        if on_finish:
            on_finish(results)
        return results


# ---------------------------------------------------------------------------
# Smoke-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_questions = [
        {
            "question_text": "What is the capital of France?",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "question_type": "multiple_choice",
            "correct_answer": "C",
            "points": 10,
        },
        {
            "question_text": "What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "question_type": "multiple_choice",
            "correct_answer": "B",
            "points": 10,
        },
        {
            "question_text": "What is the largest planet in our solar system?",
            "options": ["Earth", "Mars", "Jupiter", "Saturn"],
            "question_type": "multiple_choice",
            "correct_answer": "C",
            "points": 10,
        },
    ]

    LiveQuizDisplay().display_quiz(
        sample_questions,
        time_per_question=30,
        on_finish=lambda r: print(
            f"\nDone — viewed {r['current_index'] + 1}/{r['total_questions']} questions"
        ),
    )
