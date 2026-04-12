# Quick Start Guide

Get up and running with Neural Quiz System in 5 minutes!

## Step 1: Install Dependencies

```bash
cd ~/Programming/AppDevQuiz/
pip install -r requirements.txt
```

## Step 2: Create Sample Quizzes (Optional)

Run the setup script to create sample quizzes for testing:

```bash
python setup_sample.py
```

This creates two sample quizzes:
- **General Knowledge** (5 multiple choice questions)
- **Programming Basics** (3 enumeration questions)

## Step 3: Run the Game

```bash
python quiz_game.py
```

Or if you made it executable:

```bash
./quiz_game.py
```

## First Time Playing

1. **Select "Play Quiz"** from the main menu
2. **Choose a quiz** by entering its ID (1 or 2 for sample quizzes)
3. **Answer questions** using the keyboard:
   - Type A, B, C, or D for multiple choice
   - Type your answer for enumeration questions
   - Press Enter to submit
4. **Navigate** with arrow keys:
   - `←` Go back (timer resets)
   - `→` Skip forward (timer ignored)
5. **Press F** to finish and see your results

## Creating Your Own Quiz

1. Select **"Create New Quiz"** from the main menu
2. Enter a **name** for your quiz
3. Choose **quiz type** (Multiple Choice or Enumeration)
4. Set **time per question** (default: 30 seconds)
5. **Add questions** one by one:
   - Enter the question text
   - For multiple choice: enter 4 options (A, B, C, D)
   - Enter the correct answer
   - Set points for the question
6. Keep adding questions or finish when done

## Managing Quizzes

From **"Manage Quizzes"** you can:
- **View Quiz Details** - See all questions and settings
- **Edit Quiz Time** - Change time limits
- **Delete Quiz** - Remove quizzes you don't need

## Viewing Statistics

Select **"View Quiz Statistics"** to see:
- Total questions and points
- Number of attempts
- Average and best scores
- Recent results history

## Tips

- **Time Management**: The timer resets when you go back, so use this strategically!
- **Review Answers**: You can go back and change answers before finishing
- **Skip Questions**: Use the right arrow to skip difficult questions and come back later
- **Practice**: Start with the sample quizzes to get familiar with the interface

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| A, B, C, D | Select answer (multiple choice) |
| Enter | Submit answer |
| ← | Previous question |
| → | Next question |
| F | Finish quiz |
| Q | Quit quiz |

## Troubleshooting

**Game won't start?**
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.7+)

**Arrow keys not working?**
- Try using a different terminal emulator
- Kitty terminal is recommended for best experience

**Database errors?**
- Delete `quiz_database.db` and run `setup_sample.py` again
- Ensure you have write permissions in the directory

## Next Steps

- Create your own quizzes on topics you love
- Challenge friends and compare scores
- Customize the colors in `ui.py` to match your style
- Add more questions to the sample quizzes

---

Need more help? Check the full [README.md](README.md) for detailed documentation.
