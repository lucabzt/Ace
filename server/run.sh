#!/bin/bash

# Determine the OS to handle different paths and activation methods
OS="$(uname -s)"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo -e "Starting... $SCRIPT_DIR"

# Set PYTHONPATH for all platforms
SCRIPT_DIR="${SCRIPT_DIR}"
echo "PYTHONPATH:= $SCRIPT_DIR/../"
export PYTHONPATH="${SCRIPT_DIR}/../"

# Check if the virtual environment is already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
  if [[ "$OS" == "Darwin" || "$OS" == "Linux" ]]; then
    # For macOS and Linux
    source $SCRIPT_DIR/../.venv/bin/activate
  elif [[ "$OS" == "CYGWIN"* || "$OS" == "MINGW"* || "$OS" == "MSYS"* ]]; then
    # For Windows (Git Bash or similar)
    source $SCRIPT_DIR/../.venv/Scripts/activate
  fi
fi

echo "PYTHONPATH: $PYTHONPATH"
echo -e "Running... $SCRIPT_DIR/app.py\n\n"

# Run the app with Gunicorn
if [[ "$OS" == "Darwin" || "$OS" == "Linux" ]]; then
  # For macOS and Linux
  gunicorn $SCRIPT_DIR/app.py:app
elif [[ "$OS" == "CYGWIN"* || "$OS" == "MINGW"* || "$OS" == "MSYS"* ]]; then
  # For Windows (Git Bash or similar)
  python app.py
fi
