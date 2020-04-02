#!/bin/bash

echo "Intalling requirements..."
pip install -r requirements.txt
pip install pytest
sudo apt install clang
export PYTHONPATH="$PWD"
echo "Done installing."

echo "Starting tests."
pytest ./Source/test_compiler.py
