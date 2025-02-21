#!/bin/bash

# Exit on error
set -e

echo "Setting up Hand Gesture Game..."

# Check if Python 3.8 or higher is installed
python_version=$(python3 -c 'import sys; v = sys.version_info; print(f"{v.major}.{v.minor}")')
required_version="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "Error: Python $required_version or higher is required (found Python $python_version)"
    exit 1
fi

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies using uv
echo "Installing dependencies..."
uv pip install -e .

# Install development dependencies
echo "Installing development dependencies..."
uv pip install -e ".[dev]"

echo "Setup complete! You can now run the game with: python main.py"