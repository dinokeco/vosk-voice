#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download a small English model if it doesn't exist
if [ ! -d "model" ]; then
    echo "Downloading Vosk model..."
    wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
    unzip vosk-model-small-en-us-0.15.zip
    mv vosk-model-small-en-us-0.15 model
    rm vosk-model-small-en-us-0.15.zip
    echo "Model downloaded and extracted to 'model/'."
else
    echo "Model directory already exists."
fi

echo "Setup complete. Run 'python transcribe.py' to start."
