#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo -e "Strarting... $SCRIPT_DIR"


# Check if PYTHONPATH is already set to avoid redundant export
if [[ ":$PYTHONPATH:" != *":$SCRIPT_DIR:"* ]]; then
  SCRIPT_DIR = "$SCRIPT_DIR/../"
  export PYTHONPATH=$SCRIPT_DIR:$PYTHONPATH
fi

# Check if the virtual environment is already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
  source $SCRIPT_DIR/../.venv/bin/activate
fi

echo -e "Run... $SCRIPT_DIR/app.py\n\n"
python $SCRIPT_DIR/app.py

