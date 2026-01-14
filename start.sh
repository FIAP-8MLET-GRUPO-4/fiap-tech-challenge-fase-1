#!/bin/bash
set -e

echo "🚀 Iniciando aplicação..."

# Roda as migrações do Alembic
echo "📦 Executando migrações do banco de dados..."
alembic upgrade head

# Inicia o servidor
echo "✅ Iniciando servidor FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
