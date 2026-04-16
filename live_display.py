#!/usr/bin/env python3
"""Quiz display - using same pattern as main UI dashboard."""

import sys
import os
import time
import threading
import platform
import shutil
from typing import Optional, Callable

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
from rich.align import Align


class SimpleInput:
    """Simple input handler."""

    def __init__(self):
        self.system = platform.system()
        self.old_settings = None

    def setup(self):
        if self.system == "Windows":
            try:
                import msvcrt

                self.msvcrt = msvcrt
            except:
                pass
        else:
            try:
                import termios
                import tty

                self.termios = termios
                self.tty = tty
                # Only try to get terminal attributes if stdin is a terminal
                if hasattr(sys.stdin, 'fileno') and os.isatty(sys.stdin.fileno()):
                    self.old_settings = termios.tcgetattr(sys.stdin)
                    tty.setraw(sys.stdin.fileno())
            except:
                pass

    def get_key(self):
        try:
            if self.system == "Windows":
                if hasattr(self, 'msvcrt') and self.msvcrt.kbhit():
                    return self.msvcrt.getch().decode("utf-8")
            else:
                import select
                import sys

                # Check if there's input available and stdin is a terminal
                if hasattr(sys.stdin, 'fileno') and os.isatty(sys.stdin.fileno()) and select.select([sys.stdin], [], [], 0)[0]:
                    # Read the input
                    char = sys.stdin.read(1)
                    # If it's a newline (ENTER key), consume it and return None
                    # to avoid processing it as a regular keypress
                    if char == "\n" or char == "\r":
                        return None
                    return char
        except:
            pass
        return None

    def cleanup(self):
        if self.system != "Windows" and self.old_settings:
            try:
                # Only try to restore terminal attributes if stdin is a terminal
                if hasattr(sys.stdin, 'fileno') and os.isatty(sys.stdin.fileno()):
                    self.termios.tcsetattr(
                        sys.stdin, self.termios.TCSADRAIN, self.old_settings
                    )
            except:
                pass


class SimpleQuizDisplay:
    """Quiz display using main UI pattern."""

    def __init__(self):
        self.console = Console()
        self.input_handler = SimpleInput()

    def clear_screen(self):
        os.system("clear")
        sys.stdout.flush()

    def render_question(
        self, question: dict, current: int, total: int, time_remaining: int, paused: bool = False, hidden: bool = False
    ):
        q_text = question["question_text"]
        options = question.get("options")
        self.clear_screen()

        # Build header with status indicators
        status_parts = [f"QUESTION {current}/{total}"]
        if paused:
            status_parts.append("PAUSED")
        status_parts.append(f"TIME: {time_remaining}s")
        header = " | ".join(status_parts)

        header_style = "bold yellow" if paused else "bold cyan"
        border_style = "yellow" if paused else "cyan"

        self.console.print(
            Panel(
                Text(header, style=header_style),
                box=box.ROUNDED,
                border_style=border_style,
                padding=(0, 1),
            )
        )
        self.console.print()

        if hidden:
            # Show minimal interface when hidden
            self.console.print(
                Panel(
                    Text("[INTERFACE HIDDEN - Press H to show]", style="bold yellow"),
                    box=box.ROUNDED,
                    border_style="yellow",
                    padding=(1, 2),
                )
            )
        else:
            self.console.print(
                Panel(
                    Text(q_text, style="bold white on_black"),
                    title="[QUESTION]",
                    border_style="cyan",
                    padding=(0, 1),
                )
            )
            self.console.print()
            if options:
                options_table = Table(
                    show_header=False, box=box.SIMPLE, border_style="cyan", padding=(0, 1)
                )
                options_table.add_column("Key", style="bold cyan", width=6)
                options_table.add_column("Option", style="bold white")
                for i, opt in enumerate(options, 1):
                    key = chr(64 + i)
                    options_table.add_row(f"[{key}]", opt)
                self.console.print(Align.center(options_table))
                self.console.print()
            else:
                self.console.print(
                    Panel(
                        Text("(Write your answer on paper)", style="dim"),
                        box=box.SIMPLE,
                        border_style="dim",
                        padding=(0, 1),
                    )
                )
                self.console.print()

        # Show pause instruction in status bar
        pause_hint = " [P=Resume]" if paused else ""
        self.console.print(
            Align.center(
                Panel(
                    Text(
                        f"R=Prev N=Next 1-9=Jump H=Hide P=Pause F=Finish Q=Quit{pause_hint}",
                        style="bold cyan",
                    ),
                    box=box.SIMPLE,
                    border_style="dim",
                    padding=(0, 1),
                )
            )
        )

    def show_times_up(self):
        """Show TIME'S UP with a simple Rich panel."""
        # Restore terminal settings for input() to work properly
        if (
            hasattr(self, "input_handler")
            and hasattr(self.input_handler, "old_settings")
            and self.input_handler.old_settings
        ):
            try:
                self.input_handler.termios.tcsetattr(
                    sys.stdin,
                    self.input_handler.termios.TCSADRAIN,
                    self.input_handler.old_settings,
                )
            except:
                pass

        self.clear_screen()
        term_width = shutil.get_terminal_size().columns
        panel_width = int(term_width * 0.8)
        panel_width = max(40, min(panel_width, int(term_width * 0.9)))
        times_up_panel = Panel(
            Text("TIME'S UP!", style="bold red blink"),
            box=box.ROUNDED,
            border_style="red",
            padding=(1, 2),
            width=panel_width,
        )
        instruction = Text("Press ENTER to continue to the next question", style="dim")
        self.console.print()
        self.console.print(Align.center(times_up_panel))
        self.console.print()
        self.console.print(Align.center(instruction))
        self.console.print()

        # Clear any buffered input before waiting
        try:
            import select

            # Flush any pending input to prevent double processing
            if hasattr(select, 'select'):
                while select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.read(1024)  # Read and discard any buffered input

            # Wait for user to press ENTER
            user_input = input()

            # Clear any remaining input that might be buffered
            # This prevents the ENTER key from being processed again
            if hasattr(select, 'select'):
                while select.select([sys.stdin], [], [], 0)[0]:
                    try:
                        sys.stdin.read(1024)  # Read and discard any buffered input
                    except:
                        break
        except (EOFError, KeyboardInterrupt):
            time.sleep(2)
        except Exception:
            # If input() fails, just wait a bit and continue
            time.sleep(2)

        # Restore raw mode for continued input handling
        if hasattr(self, "input_handler") and hasattr(self.input_handler, "setup"):
            try:
                self.input_handler.setup()
            except:
                pass

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
            "hidden": False,
        }
        state_lock = threading.Lock()

        def timer_worker():
            while state["timer_running"]:
                time.sleep(1)
                with state_lock:
                    # Only decrement timer if not paused
                    if state["timer_running"] and not state["paused"] and state["time_remaining"] > 0:
                        state["time_remaining"] -= 1
                    elif state["timer_running"] and not state["paused"] and state["time_remaining"] == 0:
                        state["action"] = "TIME_UP"
                        # Clear any buffered input to prevent double processing
                        try:
                            import sys
                            import select

                            # Try to flush any pending input
                            if select.select([sys.stdin], [], [], 0)[0]:
                                sys.stdin.read(
                                    1024
                                )  # Read and discard any buffered input
                        except:
                            pass

        def input_worker():
            try:
                self.input_handler.setup()
                while state["timer_running"]:
                    key = self.input_handler.get_key()
                    if key is None:
                        time.sleep(0.05)
                        continue
                    with state_lock:
                        key_lower = key.lower() if key else ""
                        # Process navigation keys (case-insensitive)
                        if key_lower == "r" and state["current_index"] > 0:
                            state["current_index"] -= 1
                            state["time_remaining"] = time_per_question
                        elif key_lower == "n" and state["current_index"] < len(questions) - 1:
                            state["current_index"] += 1
                            state["time_remaining"] = time_per_question
                        elif key_lower == "h":  # Hide interface functionality - also pauses timer
                            state["hidden"] = not state.get("hidden", False)
                            state["paused"] = state["hidden"]  # Pause when hidden
                        elif key_lower == "p":  # Pause functionality
                            state["paused"] = not state.get("paused", False)
                            if not state["paused"]:
                                # Unhiding when unpausing if currently hidden
                                state["hidden"] = False
                        elif key_lower == "f":
                            state["timer_running"] = False
                        elif key_lower == "q":
                            state["timer_running"] = False
                        elif key and key.isdigit():
                            q_num = int(key)
                            if 1 <= q_num <= min(9, len(questions)):
                                state["current_index"] = q_num - 1
                                state["time_remaining"] = time_per_question
                        # Clear the key to prevent double processing
                        key = None
            except Exception as e:
                # Handle any exceptions gracefully
                pass

        timer_thread = threading.Thread(target=timer_worker, daemon=True)
        input_thread = threading.Thread(target=input_worker, daemon=True)
        timer_thread.start()
        input_thread.start()

        last_index = -1
        last_time = time_per_question + 999
        last_paused = False
        last_hidden = False
        try:
            while state["timer_running"]:
                with state_lock:
                    current_index = state["current_index"]
                    current_time = state["time_remaining"]
                    current_paused = state.get("paused", False)
                    current_hidden = state.get("hidden", False)
                    action = state.get("action")
                    if action == "TIME_UP":
                        state["action"] = None
                if action == "TIME_UP":
                    self.show_times_up()
                    with state_lock:
                        if current_index < len(questions) - 1:
                            state["current_index"] += 1
                            state["time_remaining"] = time_per_question
                            state["action"] = None  # Clear the action
                            last_index = -1
                            last_time = -1
                        else:
                            state["timer_running"] = False
                            break
                # Re-render if question, time, paused, or hidden state changed
                if (current_index != last_index or current_time != last_time or
                    current_paused != last_paused or current_hidden != last_hidden):
                    self.render_question(
                        questions[current_index],
                        current_index + 1,
                        len(questions),
                        current_time,
                        paused=current_paused,
                        hidden=current_hidden,
                    )
                    last_index = current_index
                    last_time = current_time
                    last_paused = current_paused
                    last_hidden = current_hidden
                time.sleep(0.05)
        finally:
            with state_lock:
                state["timer_running"] = False
            try:
                self.input_handler.cleanup()
            except:
                pass
        results = {
            "current_index": state["current_index"],
            "total_questions": len(questions),
            "completed": state["current_index"] == len(questions) - 1,
        }
        if on_finish:
            on_finish(results)
        return results


if __name__ == "__main__":
    sample_questions = [
        {"question_text": "What does HTML stand for?", "options": None},
        {"question_text": "What is 2 + 2?", "options": ["3", "4", "5", "6"]},
    ]
    print("Quiz Display Test")
    print("")
    SimpleQuizDisplay().display_quiz(
        sample_questions, time_per_question=3, on_finish=lambda r: print(f"\nDone!")
    )