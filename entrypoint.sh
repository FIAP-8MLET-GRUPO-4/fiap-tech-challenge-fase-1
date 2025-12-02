#!/bin/sh
set -e

cd /app

# Aguarda o postgres subir
until pg_isready -h db -U postgres; do
    echo "Aguardando Postgres..."
    sleep 1
done

echo "Rodando migrações..."
alembic upgrade head

echo "Subindo aplicação..."
exec uvicorn main:app --host 0.0.0.0 --port 8000