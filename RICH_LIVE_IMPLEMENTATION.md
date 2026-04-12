# Rich Live Display Implementation

## Overview

The Neural Quiz System now uses the Rich library's `Live` display feature for real-time quiz presentation with countdown timers and smooth navigation.

## Features

### ✅ Implemented Features

- **Real-time Countdown Timer**: Visual timer with color-coded urgency
  - Green (>10 seconds remaining)
  - Yellow (5-10 seconds remaining)
  - Red (≤5 seconds remaining, blinking)

- **Auto-Advance**: Automatically moves to next question when timer expires

- **Smooth Navigation**: Arrow key navigation between questions
  - ← Previous question (resets timer)
  - → Next question (resets timer)

- **Pause/Resume**: Press `P` to pause/resume the timer

- **Keyboard Controls**:
  - `←` / `→` : Navigate questions
  - `F` : Finish quiz early
  - `P` : Pause/Resume timer
  - `Q` : Quit

- **Cross-Platform Support**: Works on Linux, macOS, and Windows

- **Thread-Safe Timer**: Uses threading and locks for reliable countdown

## Architecture

### Module Structure

```
AppDevQuiz/
├── live_display.py          # Rich Live display implementation
├── quiz_game.py             # Main application (uses LiveQuizDisplay)
├── test_live_display.py     # Test script for live display
└── RICH_LIVE_IMPLEMENTATION.md  # This file
```

### Key Classes

#### `LiveQuizDisplay`

Main class for live quiz display with Rich.

**Methods:**

- `create_timer_panel()` - Creates timer panel with progress bar
- `create_question_panel()` - Creates question display panel
- `create_options_panel()` - Creates options display panel
- `create_controls_panel()` - Creates controls help panel
- `create_layout()` - Creates complete layout
- `display_quiz()` - Main display method with live updates

#### `CrossPlatformInput`

Cross-platform keyboard input handler.

**Methods:**

- `setup()` - Setup terminal for raw input
- `get_key()` - Get single key press (non-blocking)
- `cleanup()` - Restore terminal settings

## Usage

### Basic Usage

```python
from live_display import LiveQuizDisplay
from rich.console import Console

# Create display instance
console = Console()
display = LiveQuizDisplay(console)

# Define questions
questions = [
    {
        'question_text': 'What is the capital of France?',
        'options': ['London', 'Berlin', 'Paris', 'Madrid'],
        'question_type': 'multiple_choice',
        'correct_answer': 'C',
        'points': 10
    }
]

# Display quiz
results = display.display_quiz(
    questions=questions,
    time_per_question=30,
    on_finish=lambda r: print(f"Finished! {r}"),
    on_question_change=lambda i: print(f"Question {i}")
)
```

### Integration with Quiz Game

The `display_questions_one_by_one` method in `quiz_game.py` now uses `LiveQuizDisplay`:

```python
def display_questions_one_by_one(self, quiz: dict, questions: list):
    """Display questions one by one with Rich Live display."""
    from rich.console import Console

    console = Console()
    display = LiveQuizDisplay(console)

    def on_finish(results):
        self.ui.show_message(f"Quiz completed! Viewed {results['current_index'] + 1}/{results['total_questions']} questions")

    def on_question_change(index):
        pass  # Can add logging or other actions here

    display.display_quiz(
        questions=questions,
        time_per_question=quiz['time_per_question'],
        on_finish=on_finish,
        on_question_change=on_question_change
    )
```

## Testing

### Run the Test Script

```bash
cd /home/nova/Programming/AppDevQuiz
python3 test_live_display.py
```

### Test the Full Application

```bash
cd /home/nova/Programming/AppDevQuiz
python3 quiz_game.py
```

Then:
1. Select "Display Quiz (Paper Mode)"
2. Choose a quiz
3. Select "2. Show questions one by one"
4. Test navigation and timer functionality

## Technical Details

### Timer Implementation

The timer uses a separate thread that decrements the time remaining every second:

```python
def timer_worker():
    while state['timer_running']:
        time.sleep(1)
        with state_lock:
            if state['timer_running'] and not state['paused'] and state['time_remaining'] > 0:
                state['time_remaining'] -= 1
                if state['time_remaining'] <= 0:
                    state['action'] = 'NEXT'
```

### Display Updates

The display is updated at 4 frames per second using Rich's `Live` context manager:

```python
with Live(create_display(), console=console, refresh_per_second=4) as live:
    while True:
        # Check for timer actions
        # Check for keyboard input
        # Update display
        live.update(create_display())
```

### Keyboard Input Handling

Keyboard input is handled using platform-specific methods:

- **Unix/Linux/macOS**: Uses `termios` and `tty` for raw input
- **Windows**: Uses `msvcrt` for keyboard input

```python
class CrossPlatformInput:
    def __init__(self):
        self.system = platform.system()

    def setup(self):
        if self.system == "Windows":
            import msvcrt
            self.msvcrt = msvcrt
        else:
            import termios
            import tty
            self.termios = termios
            self.tty = tty
            self.old_settings = self.termios.tcgetattr(sys.stdin)
```

## Customization

### Changing Timer Colors

Edit the color logic in `create_timer_panel()`:

```python
if time_remaining <= 5:
    timer_style = "bold red blink"
    timer_border = "red"
    progress_color = "red"
elif time_remaining <= 10:
    timer_style = "bold yellow"
    timer_border = "yellow"
    progress_color = "yellow"
else:
    timer_style = "bold green"
    timer_border = "green"
    progress_color = "green"
```

### Adjusting Refresh Rate

Change the `refresh_per_second` parameter:

```python
with Live(create_display(), console=console, refresh_per_second=4) as live:
```

Higher values = smoother updates but more CPU usage.

### Modifying Panel Sizes

Adjust the `size` parameter in the layout:

```python
layout.split_column(
    Layout(timer_panel, size=5),      # Timer panel height
    Layout(question_panel, size=10),  # Question panel height
    Layout(options_panel, size=7),   # Options panel height
    Layout(controls_panel, size=4),  # Controls panel height
)
```

## Troubleshooting

### Arrow Keys Not Working

**Problem**: Arrow keys don't respond.

**Solution**:
- Ensure you're using a terminal that supports arrow key input
- Try a different terminal emulator
- Check that no other application is capturing keyboard input

### Timer Not Updating

**Problem**: Timer doesn't count down.

**Solution**:
- Check that threading is working correctly
- Verify that `state['timer_running']` is True
- Ensure no exceptions are being raised in the timer thread

### Display Flickering

**Problem**: Display flickers or updates slowly.

**Solution**:
- Reduce `refresh_per_second` to 2 or 3
- Check terminal performance
- Try a different terminal emulator

### Cross-Platform Issues

**Problem**: Application doesn't work on Windows/macOS.

**Solution**:
- Ensure `platform` module is available
- Check that `msvcrt` is installed on Windows
- Verify terminal compatibility

## Performance Considerations

- **Refresh Rate**: 4 FPS is a good balance between smoothness and CPU usage
- **Thread Safety**: All state access is protected by locks
- **Memory Usage**: Minimal - only stores current question and timer state
- **CPU Usage**: Low - timer thread sleeps for 1 second between updates

## Future Enhancements

Potential improvements for future versions:

- [ ] Add sound effects for timer expiration
- [ ] Support for custom key bindings
- [ ] Progress bar for overall quiz completion
- [ ] Question preview (peek at next question)
- [ ] Bookmark questions for later review
- [ ] Display question difficulty rating
- [ ] Show hints during quiz
- [ ] Support for image-based questions

## Credits

Built with:
- Python 3
- Rich library for terminal formatting
- Threading for timer functionality
- Cross-platform input handling

---

**Version**: 1.0.0
**Last Updated**: 2026-04-12
**Status**: ✅ Complete and Tested
