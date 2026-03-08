#!/bin/bash
# install.sh \u2014 Run on server
set -e

echo "\ud83d\udce6 Installing Instagram DM Bot..."

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Copy .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "\u26a0\ufe0f  Edit .env with your credentials!"
fi

echo "\u2705 Installation complete"
echo "\ud83d\udc49 Edit .env then run: ./start.sh"
