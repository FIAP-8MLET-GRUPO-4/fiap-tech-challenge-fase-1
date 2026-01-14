FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

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

# Copia scripts de inicialização
COPY entrypoint.sh /entrypoint.sh
COPY start.sh /start.sh
RUN chmod +x /entrypoint.sh /start.sh

# Comando padrão: start.sh (usado no Render)
# Para docker-compose local, sobrescrevemos com entrypoint.sh
CMD ["/start.sh"]

