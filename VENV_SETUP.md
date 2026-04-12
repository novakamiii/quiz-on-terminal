# Virtual Environment Setup Guide

This project uses a Python virtual environment (venv) to isolate dependencies.

## Quick Setup

### 1. Create the Virtual Environment

```bash
cd ~/Programming/AppDevQuiz/
python3 -m venv venv
```

This creates a `venv/` folder with an isolated Python environment.

### 2. Activate the Virtual Environment

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

You'll see `(venv)` in your terminal prompt when it's active.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Game

```bash
python quiz_game.py
```

## Daily Usage

Every time you want to work on the project:

```bash
cd ~/Programming/AppDevQuiz/
source venv/bin/activate
python quiz_game.py
```

## Deactivate the Virtual Environment

When you're done:

```bash
deactivate
```

The `(venv)` prompt will disappear.

## Why Use a Virtual Environment?

- **Isolation**: Keeps project dependencies separate from system Python
- **Reproducibility**: Same environment across different machines
- **Clean**: Easy to delete and recreate if needed
- **No Conflicts**: Different projects can use different package versions

## Common Commands

```bash
# Check what's installed
pip list

# Install a new package
pip install package-name

# Save current dependencies
pip freeze > requirements.txt

# Upgrade pip
pip install --upgrade pip

# Delete and recreate venv (if something breaks)
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Troubleshooting

**"command not found: python3"**
- Try `python -m venv venv` instead

**"ModuleNotFoundError"**
- Make sure you activated the venv: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**Want to start fresh?**
```bash
deactivate
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## IDE Integration

### VS Code
VS Code usually detects the venv automatically. If not:
1. Open Command Palette (Ctrl+Shift+P)
2. Select "Python: Select Interpreter"
3. Choose the venv Python: `~/Programming/AppDevQuiz/venv/bin/python`

### PyCharm
1. File → Settings → Project → Python Interpreter
2. Click ⚙️ → Add
3. Select "Existing environment"
4. Browse to: `~/Programming/AppDevQuiz/venv/bin/python`

## Notes

- The `venv/` folder is already in `.gitignore` (won't be committed)
- Dependencies are listed in `requirements.txt`
- Always activate the venv before running the game
- Deactivate when you're done working on the project
