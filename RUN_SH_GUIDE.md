# run.sh Script - Updated

## What is run.sh?

The `run.sh` script is a quick start script that:
- Activates the Python virtual environment
- Checks that the activation was successful
- Runs the Neural Quiz System

## How to Use

### Option 1: Make Executable and Run
```bash
cd ~/Programming/AppDevQuiz/
chmod +x run.sh
./run.sh
```

### Option 2: Run with Bash
```bash
cd ~/Programming/AppDevQuiz/
bash run.sh
```

### Option 3: Run with Source
```bash
cd ~/Programming/AppDevQuiz/
source run.sh
```

## What the Script Does

1. **Displays Welcome Message**
   - Shows system name and features
   - Lists current capabilities

2. **Activates Virtual Environment**
   - Activates the venv in the project directory
   - Ensures Python dependencies are available

3. **Checks Activation**
   - Verifies that the venv is active
   - Shows Python version

4. **Runs the System**
   - Starts `quiz_game.py`
   - Displays the main menu

## Features Listed

The script now displays the current features:
- ✅ Paper Mode - Display quizzes for students to answer on paper
- ✅ Large text display - Questions and answers in large, readable format
- ✅ Countdown timer - Auto-advance in one-by-one mode
- ✅ Mixed question types - Multiple choice and enumeration

## Script Content

```bash
#!/bin/bash
# Quick start script for Neural Quiz System
# This script activates the venv and runs the system

echo "🧠 Neural Quiz System - Quick Start"
echo "===================================="
echo ""
echo "Features:"
echo "  • Paper Mode - Display quizzes for students to answer on paper"
echo "  • Large text display - Questions and answers in large, readable format"
echo "  • Countdown timer - Auto-advance in one-by-one mode"
echo "  • Mixed question types - Multiple choice and enumeration"
echo ""
echo "===================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if activation was successful
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ Virtual environment activated"
    echo "✓ Python: $(python --version)"
    echo ""
    echo "Starting system..."
    echo ""
    python quiz_game.py
else
    echo "✗ Failed to activate virtual environment"
    echo "Please run: source venv/bin/activate"
    exit 1
fi
```

## Output Example

When you run `./run.sh`, you'll see:

```
🧠 Neural Quiz System - Quick Start
====================================

Features:
  • Paper Mode - Display quizzes for students to answer on paper
  • Large text display - Questions and answers in large, readable format
  • Countdown timer - Auto-advance in one-by-one mode
  • Mixed question types - Multiple choice and enumeration

====================================

✓ Virtual environment activated
✓ Python: Python 3.x.x

Starting system...

[Main menu appears]
```

## Troubleshooting

### "Permission denied" Error

If you get a permission denied error:
```bash
chmod +x run.sh
./run.sh
```

### "Failed to activate virtual environment"

If the venv activation fails:
```bash
cd ~/Programming/AppDevQuiz/
source venv/bin/activate
python quiz_game.py
```

### "Python: command not found"

If Python is not found:
```bash
# Make sure you're in the correct directory
cd ~/Programming/AppDevQuiz/

# Check if venv exists
ls -la venv/

# Recreate venv if needed
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Benefits

### Why Use run.sh?

1. **Convenience**: One command to start everything
2. **Consistency**: Always uses the correct venv
3. **Information**: Shows system features and status
4. **Error Handling**: Checks for venv activation
5. **Cross-platform**: Works on Linux, macOS, and WSL

### vs Manual Commands

**Manual:**
```bash
cd ~/Programming/AppDevQuiz/
source venv/bin/activate
python quiz_game.py
```

**With run.sh:**
```bash
cd ~/Programming/AppDevQuiz/
./run.sh
```

## Customization

You can customize the script to:

### Add Custom Environment Variables
```bash
export QUIZ_DEFAULT_TIME=30
source venv/bin/activate
python quiz_game.py
```

### Run with Specific Python Options
```bash
source venv/bin/activate
python -u quiz_game.py  # Unbuffered output
```

### Add Logging
```bash
source venv/bin/activate
python quiz_game.py 2>&1 | tee quiz.log
```

## Version History

### v2.1.0 (Current)
- Updated feature list
- Added countdown timer mention
- Updated description for Paper Mode

### v1.0.0 (Initial)
- Created basic run.sh script
- Added venv activation
- Added error checking

## Related Files

- `quiz_game.py` - Main application
- `requirements.txt` - Python dependencies
- `VENV_SETUP.md` - Virtual environment setup guide
- `QUICKSTART.md` - Quick start guide

---

**Updated for v2.1.0** - Reflects current system features
