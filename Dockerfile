FROM python:3.12-slim

WORKDIR /app

# Instala dependências do sistema necessárias para psycopg2 e pg_isready
RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

#ENTRYPOINT vai ser um script que roda alembic upgrade e depois o uvicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Comando para iniciar a aplicação
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

