#!/bin/bash
# This script sets up a development environment for a code space.
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/game.py