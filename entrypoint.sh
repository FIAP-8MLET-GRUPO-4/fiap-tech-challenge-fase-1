#!/bin/sh
set -e

cd /app

# Aguarda o postgres subir
echo "Aguardando o banco subir..."
sleep 5

echo "Rodando migrações..."
alembic upgrade head

echo "Subindo aplicação..."
exec uvicorn main:app --host 0.0.0.0 --port 8000