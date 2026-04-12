# Neural Quiz System

A terminal-based quiz system with a techno/AI styled interface. Built with Python, featuring SQLite database storage, customizable quizzes, and **Paper Mode** for classroom use.

## Features

- **📝 Paper Mode**: Display quizzes for students to answer on paper
- **🎯 Multiple Quiz Types**: Support for multiple choice (A, B, C, D), enumeration, and mixed quizzes
- **🔀 Mixed Question Types**: Combine different question formats in a single quiz
- **💾 SQLite Database**: Persistent storage for quizzes and questions
- **🎨 Techno/AI Interface**: Styled terminal interface with rich formatting
- **🧹 Clean Interface**: Automatic screen clearing for a clean reading experience
- **🔧 Quiz Management**: Create, edit, and delete quizzes easily
- **📋 Answer Key Display**: View answers one by one or all at once

## Requirements

- Python 3.7 or higher
- Kitty terminal (recommended for best experience)
- See `requirements.txt` for Python dependencies

## Installation

1. Clone or download this repository:
```bash
cd ~/Programming/AppDevQuiz/
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the main script executable (optional):
```bash
chmod +x quiz_game.py
```

## Usage

### Starting the Game

Run the game with Python:
```bash
python quiz_game.py
```

Or if you made it executable:
```bash
./quiz_game.py
```

### Main Menu

The main menu offers the following options:

1. **Display Quiz (Paper Mode)** - Display quiz for students to answer on paper
2. **Create New Quiz** - Create a new quiz with custom questions
3. **Manage Quizzes** - View, edit, or delete existing quizzes
4. **Exit System** - Close the application

### Creating a Quiz

When creating a new quiz, you'll be prompted for:

1. **Quiz Name** - A unique name for your quiz
2. **Description** - Optional description of the quiz
3. **Quiz Type** - Choose between:
   - Multiple Choice Only (A, B, C, D options)
   - Enumeration Only (text input answers)
   - Mixed (combine both types in the same quiz)
4. **Time per Question** - Seconds allowed for each question (default: 30)
5. **Questions** - Add as many questions as you want

For mixed quizzes, you'll be prompted to choose the type for each question individually.

### Displaying a Quiz (Paper Mode)

**Step 1: Select a Quiz**
```
1. Display Quiz (Paper Mode)
Enter quiz ID to display: 1
```

**Step 2: Choose Display Mode**
```
Display Mode:
1. Show all questions at once
2. Show questions one by one

Select display mode [1-2]: 1
```

**Step 3: Students Answer on Paper**
- Students view questions on the terminal
- Students write answers on paper
- No input required during the quiz

**Step 4: View Answer Key**
```
How would you like to view the answers?
1. Show answers one by one
2. Show all answers at once

Select answer display mode [1-2]: 2
```

### Display Modes

#### All Questions at Once
- Shows entire quiz in a list
- Good for printing or screenshots
- Students can see all questions at once

#### One by One
- Navigate with arrow keys (← →)
- Press F to finish
- Good for controlled pacing

### Answer Key Display

#### One by One
- Navigate with arrow keys (← →)
- Press Q to quit
- Shows question, answer, and points

#### All at Once
- Shows all answers in a list
- Displays total questions and points
- Good for quick grading

### Quiz Types

#### Multiple Choice
- 4 options (A, B, C, D)
- User selects one option
- Correct answer is a single letter (A, B, C, or D)

#### Enumeration
- Open-ended text input
- User types their answer
- Correct answer is text (case-sensitive by default)

#### Mixed (NEW!)
- Combine both multiple choice and enumeration questions
- Each question can have its own type
- Great for varied and engaging quizzes
- See [MIXED_QUIZZES.md](MIXED_QUIZZES.md) for details

### Managing Quizzes

From the "Manage Quizzes" menu, you can:

1. **View Quiz Details** - See all questions and settings
2. **Edit Quiz Time** - Change the time per question
3. **Delete Quiz** - Remove a quiz permanently

## Database

The game uses SQLite for data persistence. The database file `quiz_database.db` is created automatically in the same directory as the script.

**Database Schema:**
- `quizzes` - Quiz metadata (name, description, time, type)
- `questions` - Individual questions with options and answers
- `quiz_results` - Player results and scores

## Customization

### Changing Colors

Edit the `colors` dictionary in `ui.py` to customize the color scheme:

```python
self.colors = {
    'primary': '#00ff00',      # Matrix green
    'secondary': '#00ffff',    # Cyan
    'accent': '#ff00ff',        # Magenta
    # ... more colors
}
```

### Adjusting Default Settings

Modify default values in the relevant modules:
- Default time per question: `database.py` (line 48)
- Default points per question: `database.py` (line 73)
- Default quiz type: `database.py` (line 48)

## Troubleshooting

### Terminal Issues

If the interface doesn't display correctly:
- Ensure you're using a modern terminal emulator
- Kitty terminal is recommended for best results
- Try increasing your terminal window size

### Arrow Keys Not Working

If arrow keys don't respond:
- Make sure your terminal supports arrow key input
- Try using a different terminal emulator
- Check that no other application is capturing keyboard input

### Database Errors

If you encounter database errors:
- Ensure you have write permissions in the directory
- Delete `quiz_database.db` and restart to recreate
- Check that SQLite is properly installed

## Development

### Project Structure

```
AppDevQuiz/
├── quiz_game.py      # Main application entry point
├── database.py       # SQLite database management
├── ui.py             # Terminal UI with rich formatting
├── quiz_manager.py   # Quiz creation and management
├── game.py           # Game logic and gameplay
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

### Adding New Features

The modular design makes it easy to extend:

- **New quiz types**: Add to `quiz_manager.py` and update `game.py`
- **New UI elements**: Extend `ui.py` with new methods
- **Database changes**: Update `database.py` schema

## License

This project is open source and available for educational purposes.

## Credits

Built with:
- Python 3
- Rich library for terminal formatting
- SQLite for data persistence
- Kitty terminal for enhanced display

---

Enjoy your neural quiz experience! 🧠⚡
