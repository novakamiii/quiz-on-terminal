# Mixed Question Types

The Neural Quiz System now supports mixing different question types within a single quiz!

## Quiz Types

### 1. Multiple Choice Only
All questions use A, B, C, D options.

### 2. Enumeration Only
All questions require text input answers.

### 3. Mixed (NEW!)
Combine both multiple choice and enumeration questions in the same quiz.

## Creating a Mixed Quiz

When creating a new quiz, select option **3** for "Mixed" type:

```
Quiz Types:
1. Multiple Choice Only (A, B, C, D)
2. Enumeration Only (text input)
3. Mixed (both types in same quiz)

Select quiz type [1-3]: 3
```

Then, for each question you add, you'll be prompted to choose the type:

```
Question Type:
1. Multiple Choice (A, B, C, D)
2. Enumeration (text input)

Select question type [1-2]: 1
```

## Example Mixed Quiz

Here's an example of a mixed quiz structure:

**Question 1 (Multiple Choice):**
```
What is 2 + 2?
A. 3
B. 4
C. 5
D. 6
```

**Question 2 (Enumeration):**
```
What is the capital of Japan?
Your answer: Tokyo
```

**Question 3 (Multiple Choice):**
```
Which programming language is known for its simplicity?
A. C++
B. Java
C. Python
D. Assembly
```

**Question 4 (Enumeration):**
```
What does CPU stand for?
Your answer: Central Processing Unit
```

## Benefits of Mixed Quizzes

- **Variety**: Keep users engaged with different question formats
- **Flexibility**: Test different types of knowledge
- **Comprehensive**: Combine factual recall (multiple choice) with deeper understanding (enumeration)
- **Customizable**: Mix and match to suit your needs

## Playing Mixed Quizzes

The game automatically handles the different question types:

- **Multiple Choice**: Type A, B, C, or D and press Enter
- **Enumeration**: Type your answer and press Enter
- **Navigation**: Use ← → to navigate between questions
- **Timer**: Works the same for all question types

## Sample Mixed Quiz

The setup script now creates a sample mixed quiz called "Mixed Challenge" (ID: 3) with 4 questions demonstrating both types.

Run it:
```bash
python setup_sample.py
```

Then play it:
```bash
python quiz_game.py
```

Select quiz ID 3 to try the mixed quiz!

## Tips for Creating Mixed Quizzes

1. **Balance**: Mix question types evenly for variety
2. **Difficulty**: Use enumeration for harder questions that require recall
3. **Time**: Adjust time per question based on question type (enumeration may need more time)
4. **Points**: Award more points for enumeration questions if they're harder

## Technical Details

- Each question stores its own type in the database
- The quiz type field indicates the default or "mixed" status
- The game checks each question's type individually during gameplay
- No changes needed to existing quizzes - they continue to work as before

---

Enjoy creating diverse and engaging quizzes! 🎯
