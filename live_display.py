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
                if hasattr(sys.stdin, "fileno") and os.isatty(sys.stdin.fileno()):
                    self.old_settings = termios.tcgetattr(sys.stdin)
                    tty.setraw(sys.stdin.fileno())
            except:
                pass

    def get_key(self):
        try:
            if self.system == "Windows":
                if hasattr(self, "msvcrt") and self.msvcrt.kbhit():
                    return self.msvcrt.getch().decode("utf-8")
            else:
                import select
                import sys

                # Check if there's input available and stdin is a terminal
                if (
                    hasattr(sys.stdin, "fileno")
                    and os.isatty(sys.stdin.fileno())
                    and select.select([sys.stdin], [], [], 0)[0]
                ):
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
                if hasattr(sys.stdin, "fileno") and os.isatty(sys.stdin.fileno()):
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
        # Use Rich's console clear - works across terminals
        self.console.clear()

    def render_question(
        self,
        question: dict,
        current: int,
        total: int,
        time_remaining: int,
        time_per_question: int = 30,
        paused: bool = False,
        hidden: bool = False,
    ):
        q_text = question["question_text"]
        options = question.get("options")

        self.clear_screen()

        # Time-based styling
        if time_remaining <= 5:
            time_style = "bold red blink"
            bar_color = "red"
            border_style = "red"
        elif time_remaining <= 10:
            time_style = "bold #FFA500 blink"
            bar_color = "#FFA500"
            border_style = "#FFA500"
        else:
            time_style = "bold yellow" if paused else "bold cyan"
            bar_color = "yellow" if paused else "cyan"
            border_style = "yellow" if paused else "cyan"

        # Progress bar
        term_width = shutil.get_terminal_size().columns
        # Account for panel borders + padding (6 chars) and the label on the right
        label = f" {chr(0xF252)} {time_remaining:>3}s"
        prefix = f"{chr(0xF05F)} {current}/{total}  "
        bar_area_width = term_width - 6 - len(label) - len(prefix)
        bar_area_width = max(bar_area_width, 10)
        ratio = time_remaining / time_per_question if time_per_question > 0 else 0
        ratio = max(0.0, min(1.0, ratio))
        filled = int(bar_area_width * ratio)
        empty = bar_area_width - filled

        bar_line = Text()
        bar_line.append(prefix, style=time_style)
        bar_line.append("\u2588" * filled, style=bar_color)
        bar_line.append("\u2591" * empty, style="dim")
        bar_line.append(label, style=time_style)

        from rich.console import Group

        if paused:
            paused_line = Align.center(Text(f"{chr(0xF28C)} PAUSED", style="bold yellow"))
            panel_content = Group(bar_line, paused_line)
        else:
            panel_content = bar_line

        # Header Panel
        self.console.print(
            Panel(
                panel_content,
                box=box.ROUNDED,
                border_style=border_style,
                padding=(0, 1),
            )
        )

        if hidden:
            self.console.print(
                Panel(
                    Text("[INTERFACE HIDDEN - Press H to show]", style="bold yellow"),
                    box=box.ROUNDED,
                    border_style="yellow",
                    padding=(1, 1),
                )
            )
        else:
            # Question Panel - NO width, auto-size
            self.console.print(
                Panel(
                    Text(q_text, style="bold white"),
                    title=f"{chr(0xF07E)} [QUESTION]",
                    border_style="cyan",
                    padding=(0, 1),
                )
            )

            # Options table - auto-fit, centered
            if options:
                opt_table = Table(
                    show_header=False,
                    box=box.SIMPLE,
                    border_style="cyan",
                    padding=(0, 1),
                )
                opt_table.add_column("Key", style="bold cyan", width=6)
                opt_table.add_column("Option", style="bold white")
                for i, opt in enumerate(options, 1):
                    opt_table.add_row(f"[{chr(64 + i)}]", opt)
                self.console.print(Align.center(opt_table))
            else:
                self.console.print(
                    Align.center(
                        Panel(
                            Text("(Think your answer carefully!)", style="dim"),
                            box=box.SIMPLE,
                            border_style="dim",
                            padding=(0, 1),
                        )
                    )
                )

        # Navigation - with color-coded icons (fa-regular)
        nav = Text()
        nav.append(f"{chr(0xF362)} ", style="blue")  # fa-circle-left (Prev)
        nav.append("R=Prev ", style="white")
        nav.append(f"{chr(0xF363)} ", style="blue")  # fa-circle-right (Next)
        nav.append("N=Next ", style="white")
        nav.append(f"{chr(0xF070)} ", style="dim")  # fa-eye-slash (Hide)
        nav.append("H=Hide ", style="white")
        nav.append(f"{chr(0xF28C)} ", style="yellow")  # fa-circle-pause (Pause)
        nav.append("P=Pause ", style="white")
        nav.append(f"{chr(0xF058)} ", style="green")  # fa-circle-check (Finish)
        nav.append("F=Finish ", style="white")
        nav.append(f"{chr(0xF05E)} ", style="red")  # fa-circle-xmark (Quit)
        nav.append("Q=Quit", style="white")

        self.console.print(
            Align.center(
                Panel(
                    nav,
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

        # Center the TIME'S UP message
        times_up_text = Text()
        times_up_text.append(f"{chr(0xF252)} ", style="bold red blink")  # fa-clock
        times_up_text.append("TIME'S UP!", style="bold red blink")

        times_up_panel = Panel(
            Align.center(times_up_text),
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
            if hasattr(select, "select"):
                while select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.read(1024)  # Read and discard any buffered input

            # Wait for user to press ENTER
            user_input = input()

            # Clear any remaining input that might be buffered
            # This prevents the ENTER key from being processed again
            if hasattr(select, "select"):
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

        self.clear_screen()

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
                    # Only decrement timer if not paused and no action is TIME_UP
                    if (
                        state["timer_running"]
                        and not state["paused"]
                        and state["action"] != "TIME_UP"
                        and state["time_remaining"] > 0
                    ):
                        state["time_remaining"] -= 1
                    elif (
                        state["timer_running"]
                        and not state["paused"]
                        and state["time_remaining"] == 0
                    ):
                        state["action"] = "TIME_UP"
                        # Clear any buffered input to prevent double processing
                        try:
                            import select

                            # Try to flush any pending input
                            if select.select([sys.stdin], [], [], 0)[0]:
                                sys.stdin.read(1024)  # Read and discard any buffered input
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
                        elif (
                            key_lower == "n"
                            and state["current_index"] < len(questions) - 1
                        ):
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
            except Exception:
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
                if (
                    current_index != last_index
                    or current_time != last_time
                    or current_paused != last_paused
                    or current_hidden != last_hidden
                ):
                    self.render_question(
                        questions[current_index],
                        current_index + 1,
                        len(questions),
                        current_time,
                        time_per_question=time_per_question,
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
