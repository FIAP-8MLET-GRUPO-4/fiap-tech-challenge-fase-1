# Tech Challenge - Fase 1

API desenvolvida com FastAPI e PostgreSQL para o Tech Challenge da FIAP.

## Pré-requisitos

### Para execução com Docker (recomendado)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Para execução local
- Python 3.12+
- PostgreSQL 17+

## Configuração

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd fiap-tech-challenge-fase-1
```

2. Crie o arquivo de variáveis de ambiente:
```bash
cp .env.example .env
```

3. (Opcional) Edite o arquivo `.env` para personalizar as configurações.

## Execução

### Com Docker (Padrão)

Inicie todos os serviços (PostgreSQL + API):
```bash
docker compose up -d
```

Para visualizar os logs:
```bash
docker compose logs -f
```

Para parar os serviços:
```bash
docker compose down
```

Para parar e remover os volumes (apaga dados do banco):
```bash
docker compose down -v
```

### Sem Docker (Terminal)

1. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o PostgreSQL localmente e ajuste o `DATABASE_URL` no arquivo `.env`:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tech_challenge
```

4. Inicialize o banco de dados:
```bash
python main.py
```

5. Execute a aplicação:
```bash
uvicorn main:app --reload
```

## Acesso

- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

## Estrutura do Projeto

```
.
├── api/
│   ├── core/
│   │   └── db.py          # Configuração do banco de dados
│   └── models/
│       ├── books.py       # Modelo de livros
│       └── users.py       # Modelo de usuários
├── data/                  # Dados do projeto
├── docs/                  # Documentação
├── scripts/               # Scripts auxiliares
├── tests/                 # Testes
├── main.py                # Ponto de entrada da aplicação
├── requirements.txt       # Dependências Python
├── Dockerfile             # Configuração do container da API
├── docker-compose.yml     # Orquestração dos containers
└── .env.example           # Template de variáveis de ambiente
```

## Tecnologias

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **PostgreSQL 17** - Banco de dados
- **Docker** - Containerização
- **Uvicorn** - Servidor ASGI

### Ricardo 