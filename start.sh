#!/bin/bash

# Start script for Jouster LLM Knowledge Extractor
# This script handles different deployment scenarios

# Check if PORT environment variable is set
if [ -z "$PORT" ]; then
    PORT=8000
fi

# Start the application with uvicorn
echo "Starting Jouster API on port $PORT..."
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
