#!/bin/bash

# Exit on error
set -e

# Load environment variables
if [ -f .env.test ]; then
    export $(cat .env.test | grep -v '^#' | xargs)
elif [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Ensure we're using test database
export POSTGRES_DB="${POSTGRES_DB}_test"

echo "Running tests..."

# Check if running in CI
if [ "${CI}" = "true" ]; then
    # Run tests with coverage in CI
    pytest --cov=app --cov-report=xml --cov-report=term-missing
else
    # Run tests with verbose output in development
    pytest -v \
        --cov=app \
        --cov-report=term-missing \
        --cov-report=html:coverage_report

    echo "Coverage report generated in coverage_report/index.html"
fi

# Clean up test database if needed
if [ "${CLEANUP_TEST_DB}" = "true" ]; then
    echo "Cleaning up test database..."
    psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -c "DROP DATABASE IF EXISTS ${POSTGRES_DB};"
fi