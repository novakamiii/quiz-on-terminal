# Paper Mode Quiz System

The Neural Quiz System now supports **Paper Mode** - perfect for classroom settings where students view questions on the terminal and answer on paper.

## What is Paper Mode?

In Paper Mode:
- ✅ Students view quiz questions on the terminal
- ✅ Students write answers on paper (not in the terminal)
- ✅ No interactive input during the quiz
- ✅ After the quiz, answer key is displayed
- ✅ Choose how to view answers (one by one or all at once)

## How to Use Paper Mode

### Step 1: Display a Quiz

From the main menu:
```
1. Display Quiz (Paper Mode)
```

### Step 2: Choose Display Mode

You'll be asked how to display questions:

**Option 1: Show all questions at once**
- All questions displayed in a list
- Good for printing or taking screenshots
- Students can see the entire quiz at once

**Option 2: Show questions one by one**
- Navigate with arrow keys (← →)
- Press F to finish
- Good for controlled pacing

### Step 3: Students Answer on Paper

Students write their answers on paper while viewing the questions.

### Step 4: View Answer Key

After the quiz finishes, you can view the answer key:

**Option 1: Show answers one by one**
- Navigate with arrow keys (← →)
- Press Q to quit
- Good for reviewing each question

**Option 2: Show all answers at once**
- All answers displayed in a list
- Good for quick grading
- Shows total points

## Example Workflow

### Classroom Scenario

1. **Teacher creates a quiz** using "Create New Quiz"
2. **Teacher displays the quiz** using "Display Quiz (Paper Mode)"
3. **Students view questions** on the terminal/projector
4. **Students write answers** on paper
5. **Teacher shows answer key** after everyone finishes
6. **Teacher grades papers** using the answer key

## Display Modes Comparison

### All Questions at Once

**Pros:**
- Students can see entire quiz
- Can skip ahead and come back
- Good for longer quizzes
- Easy to screenshot/print

**Cons:**
- May overwhelm students
- Less control over pacing

**Best for:**
- Short quizzes (5-10 questions)
- Self-paced study
- Review sessions

### One by One

**Pros:**
- Controlled pacing
- Less overwhelming
- Teacher can explain each question
- Good for timed quizzes

**Cons:**
- Can't skip ahead easily
- Takes longer to complete
- Requires more interaction

**Best for:**
- Classroom presentations
- Timed assessments
- Teaching scenarios

## Answer Key Display

### One by One

Shows each question with its correct answer:
- Question text
- Correct answer (highlighted in green)
- Points value
- Navigation controls

### All at Once

Shows all answers in a list:
- Question number and preview
- Correct answer
- Points value
- Total questions and points

## Tips for Teachers

### Before the Quiz
1. Create your quiz with clear questions
2. Test the display mode
3. Prepare answer sheets for students
4. Set up the terminal/projector

### During the Quiz
1. Choose appropriate display mode
2. Give students time to answer
3. Monitor progress
4. Be ready to show answer key

### After the Quiz
1. Display answer key
2. Review difficult questions
3. Collect papers for grading
4. Discuss results

## Keyboard Controls

### During Quiz Display (One by One)
- **←** Previous question
- **→** Next question
- **F** Finish quiz

### During Answer Key (One by One)
- **←** Previous answer
- **→** Next answer
- **Q** Quit

## Benefits of Paper Mode

### For Teachers
- No need to print quizzes
- Easy to update questions
- Reusable quiz bank
- Quick answer key access
- Professional presentation

### For Students
- Clear, readable questions
- Can write at own pace
- No technical issues with input
- Focus on content, not interface

### For Institutions
- Cost-effective (no printing)
- Environmentally friendly
- Easy to maintain
- Scalable to large classes

## Technical Details

### Display Format
- Questions are displayed with clear formatting
- Multiple choice shows A, B, C, D options
- Enumeration shows "(Write your answer on paper)"
- Answer key highlights correct answers in green

### Navigation
- Arrow keys work in both display modes
- Smooth transitions between questions
- Clear progress indicators

### Answer Key
- Automatically generated from quiz data
- Shows correct answers for all question types
- Displays point values
- Calculates totals

## Example Quiz Display

### All Questions at Once

```
==================================================
QUIZ: General Knowledge
==================================================

==================================================
Question 1/5
==================================================
What is the capital of France?

Options:
  A. London
  B. Berlin
  C. Paris
  D. Madrid

==================================================
Question 2/5
==================================================
Which planet is known as the Red Planet?

Options:
  A. Venus
  B. Mars
  C. Jupiter
  D. Saturn

[... more questions ...]

==================================================
END OF QUIZ - 5 questions total
==================================================
```

### Answer Key (All at Once)

```
==================================================
ANSWER KEY - ALL QUESTIONS
==================================================

==================================================
Question 1: What is the capital of France?...
==================================================
Answer: C. Paris
Points: 10

==================================================
Question 2: Which planet is known as the Red P...
==================================================
Answer: B. Mars
Points: 10

[... more answers ...]

==================================================
Total Questions: 5
Total Points: 50
==================================================
```

## Troubleshooting

**Questions not displaying clearly?**
- Increase terminal window size
- Use a larger font
- Try "one by one" mode for better readability

**Answer key not showing?**
- Make sure you pressed F to finish the quiz
- Check that the quiz has questions
- Try restarting the application

**Navigation not working?**
- Make sure terminal supports arrow keys
- Try using a different terminal emulator
- Check that no other app is capturing keyboard input

---

Perfect for classrooms, training sessions, and any scenario where you need to display quizzes for paper-based answering! 📝✏️
