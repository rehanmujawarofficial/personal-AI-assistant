#!/bin/bash

cd "$(dirname "$0")/voice_assistant"
pip install -r ../requirements.txt
python main.py
