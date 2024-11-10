#!/bin/bash

# Exit on error
set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Warning: .env file not found"
    echo "Using default configuration"
fi

# Check if running in development or production mode
ENV=${ENVIRONMENT:-development}

if [ "$ENV" = "production" ]; then
    echo "Starting in production mode..."
    docker-compose -f docker-compose.prod.yml up --build
else
    echo "Starting in development mode..."
    
    # Check if poetry is installed
    if ! command -v poetry &> /dev/null; then
        echo "Poetry not found. Installing dependencies with pip..."
        pip install -r requirements.txt
    else
        echo "Installing dependencies with poetry..."
        poetry install
    fi

    # Run database migrations
    echo "Running database migrations..."
    alembic upgrade head

    # Start the application
    echo "Starting FastAPI server..."
    uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT:-8000}
fi