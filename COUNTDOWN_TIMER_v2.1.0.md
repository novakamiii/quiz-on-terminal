# Countdown Timer Feature - v2.1.0

## New Feature

### Automatic Countdown Timer

The "One by One" display mode now includes a **countdown timer** that automatically advances to the next question when time runs out.

## How It Works

### Timer Display

The countdown timer shows:
- **Time Remaining**: Counts down from the quiz's time_per_question setting
- **Question Number**: Shows current question (e.g., "Question 1/5")
- **Color Coding**:
  - 🟢 **Green** (>10 seconds remaining)
  - 🟡 **Yellow** (5-10 seconds remaining)
  - 🔴 **Red** (≤5 seconds remaining, blinking)

### Timer Behavior

1. **Start**: Timer starts at the quiz's `time_per_question` value
2. **Countdown**: Timer counts down every second
3. **Auto-Advance**: When timer reaches 0, automatically moves to next question
4. **Reset**: Timer resets when navigating to a new question
5. **Manual Override**: Arrow keys still work to navigate manually

### Controls

**During Countdown:**
- **←** Previous question (resets timer)
- **→** Next question (resets timer)
- **F** Finish quiz early

**Timer Behavior:**
- Timer counts down automatically
- Auto-advances when time expires
- Manual navigation resets timer
- Can finish early with 'F'

## Display Example

### Countdown Timer Display

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║ ⏱️  Time Remaining: 15s | Question 1/5                                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Low Time Warning (Red, Blinking)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║ ⏱️  Time Remaining: 3s | Question 1/5                                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Use Cases

### Classroom Presentations

**Scenario:** Teacher wants to pace the quiz automatically

**Setup:**
1. Create quiz with `time_per_question = 30` seconds
2. Select "Display Quiz (Paper Mode)"
3. Choose "2. Show questions one by one"

**Result:**
- Each question displays for 30 seconds
- Timer counts down prominently
- Auto-advances when time expires
- Teacher can still navigate manually if needed

### Timed Assessments

**Scenario:** Students have limited time per question

**Setup:**
1. Create quiz with `time_per_question = 15` seconds
2. Select "Display Quiz (Paper Mode)"
3. Choose "2. Show questions one by one"

**Result:**
- Students see countdown timer
- Time pressure creates urgency
- Auto-advance keeps quiz moving
- Fair timing for all students

### Self-Paced Study

**Scenario:** Students want to control their own pace

**Setup:**
1. Create quiz with `time_per_question = 60` seconds
2. Select "Display Quiz (Paper Mode)"
3. Choose "2. Show questions one by one"

**Result:**
- Generous time per question
- Students can pace themselves
- Timer provides guidance
- Manual navigation available

## Technical Details

### Implementation

- **Thread-based Timer**: Uses Python threading for non-blocking countdown
- **Thread-safe**: Uses locks to prevent race conditions
- **Non-blocking Input**: Uses select() for responsive keyboard input
- **Auto-advance**: Automatically moves to next question when timer expires

### Timer States

1. **Running**: Timer is counting down
2. **Expired**: Timer reached 0, auto-advance triggered
3. **Reset**: Timer reset to time_per_question on navigation
4. **Stopped**: Timer stopped when quiz finishes

### Color Coding

```python
if time_remaining <= 5:
    style = "bold red blink"      # Urgent!
    border_style = "red"
elif time_remaining <= 10:
    style = "bold yellow"         # Warning
    border_style = "yellow"
else:
    style = "bold green"          # Normal
    border_style = "green"
```

## Files Modified

### ui.py
- Added `show_countdown_timer()` method
- Displays countdown with color coding
- Shows question number and time remaining

### quiz_game.py
- Updated `display_questions_one_by_one()` with countdown timer
- Added timer thread for non-blocking countdown
- Implemented auto-advance when timer expires
- Added manual navigation with timer reset
- Updated `display_all_questions()` with note about countdown timer

### test_countdown.py (New)
- Test script for countdown timer functionality
- Tests timer display and color changes

## Benefits

### For Teachers
- ✅ Automatic pacing - no need to manually advance
- ✅ Consistent timing - all questions get same time
- ✅ Visual feedback - students see time remaining
- ✅ Flexible control - can still navigate manually

### For Students
- ✅ Clear time limits - know how much time remains
- ✅ Visual warnings - color changes as time runs low
- ✅ Fair timing - everyone gets same time per question
- ✅ Reduced anxiety - can see time remaining

### For Presentations
- ✅ Professional appearance - prominent timer display
- ✅ Smooth transitions - auto-advance keeps flow
- ✅ Time management - easy to pace the quiz
- ✅ Flexibility - manual override available

## Testing

### Test Countdown Timer
```bash
python test_countdown.py
```

**Tests:**
- Timer display for different time values
- Color changes at different thresholds
- Timer countdown functionality

### Manual Testing

**Test 1: Countdown Display**
```bash
python quiz_game.py
# Select "Display Quiz (Paper Mode)"
# Choose "2. Show questions one by one"
# Watch countdown timer
```

**Test 2: Auto-Advance**
```bash
# Wait for timer to expire
# Should auto-advance to next question
# Timer should reset
```

**Test 3: Manual Navigation**
```bash
# Use arrow keys to navigate
# Timer should reset on navigation
# Auto-advance still works
```

## Comparison: All Questions vs One by One

### All Questions at Once
- ✅ See entire quiz at once
- ✅ Good for printing/screenshots
- ❌ No countdown timer
- ❌ No auto-advance

### One by One (NEW with Countdown)
- ✅ One question at a time
- ✅ Countdown timer display
- ✅ Auto-advance when time expires
- ✅ Manual navigation available
- ✅ Color-coded time warnings

## Tips

### Setting Time Per Question

**Short Quizzes (5-10 questions):**
- 15-20 seconds per question
- Good for quick assessments

**Medium Quizzes (10-20 questions):**
- 20-30 seconds per question
- Balanced pace

**Long Quizzes (20+ questions):**
- 30-60 seconds per question
- Allows more time per question

### Using Countdown Timer Effectively

1. **Set Appropriate Time**: Consider question difficulty
2. **Test First**: Run through quiz to check timing
3. **Be Flexible**: Manual navigation still available
4. **Communicate**: Tell students about timer beforehand

## Troubleshooting

**Timer not counting down?**
- Check that time_per_question is set correctly
- Ensure quiz has questions
- Try restarting the application

**Auto-advance not working?**
- Make sure you're in "One by One" mode
- Check that timer thread is running
- Verify time_per_question > 0

**Colors not changing?**
- Check terminal supports color
- Try different terminal emulator
- Kitty terminal recommended

## Future Enhancements

Potential improvements for future versions:
- Configurable timer sounds
- Pause/resume timer
- Different time per question
- Timer extension option
- Custom timer colors

---

**Version 2.1.0** - Countdown timer with auto-advance feature! ⏱️
