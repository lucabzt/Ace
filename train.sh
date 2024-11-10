#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Check if PYTHONPATH is already set to avoid redundant export
if [[ ":$PYTHONPATH:" != *":$SCRIPT_DIR:"* ]]; then
  export PYTHONPATH=$SCRIPT_DIR:$PYTHONPATH
fi

# Check if the virtual environment is already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
  source $SCRIPT_DIR/venv/bin/activate
fi

python3 $SCRIPT_DIR/src/classifier/train.py

