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
