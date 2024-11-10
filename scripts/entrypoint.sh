#!/bin/bash
set -e

echo "Waiting for services to start..."
sleep 10

# Executar migrações
echo "Running migrations"
alembic upgrade head

# Iniciar a aplicação
echo "Starting application"
uvicorn app.main:app --host $HOST --port $PORT --workers $WORKERS