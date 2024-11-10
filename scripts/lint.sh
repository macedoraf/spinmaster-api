#!/bin/bash

# Exit on error
set -e

echo "Running linting checks..."

# Run black for code formatting
echo "Checking code formatting with black..."
black --check app tests

# Run isort for import sorting
echo "Checking import sorting with isort..."
isort --check-only app tests

# Run flake8 for code style
echo "Checking code style with flake8..."
flake8 app tests

# Run mypy for type checking
echo "Running type checking with mypy..."
mypy app

# Run security checks with bandit
echo "Running security checks with bandit..."
bandit -r app

# If all checks pass
echo "All linting checks passed successfully!"