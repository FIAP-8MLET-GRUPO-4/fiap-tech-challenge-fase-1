# Tech Challenge - Fase 1

API desenvolvida com FastAPI e PostgreSQL para o Tech Challenge da FIAP.

## Integrantes do grupo:

### Integrantes do Grupo

| Nome | E-mail | Perfil Profissional |
| :--- | :--- | :---: |
| **Doglas Parise** | [doglasparise@gmail.com](mailto:doglasparise@gmail.com) | [🔗 Skills Google](https://www.skills.google/public_profiles/c73ebebd-15ad-4883-97f3-02551573d9b9) |
| **Mariana Teixeira Dornelles Parise** | [m.dornelles19@gmail.com](mailto:m.dornelles19@gmail.com) | [🔗 Skills Google](https://www.skills.google/public_profiles/c71a2add-704b-450f-9eba-2ebb17f39191) |
| **Ricardo Gomes de Souza** | [ricardo_g_souza@yahoo.com](mailto:ricardo_g_souza@yahoo.com) | [🔗 Skills Google](https://www.skills.google/public_profiles/3f78cef1-fb4a-4d92-9eef-f03c1c7df021) |
| **Silvio José Meirelles** | [professorsilviomeireles@gmail.com](mailto:professorsilviomeireles@gmail.com) | - |

## Vídeo de apresentação
[Link para vídeo de apresentação](https://youtu.be/_IeboziIPKM?si=3FDX4B64DVHsWmoW)

## Documento arquitetural
[📄 Plano Arquitetural - FIAP Tech Challenge Fase 1](https://github.com/FIAP-8MLET-GRUPO-4/fiap-tech-challenge-fase-1/blob/ef6b432cab7e7977a511730e3acb9f7c56b9275a/docs/FIAP-TECH-CHALLANGE-1-PLANO-ARQUITETURAL.pdf)

## Deploy no Render
[Deploy da API (Swagger / OpenAPI)](https://fiap-tech-challenge-fase-1.onrender.com/docs#/)

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

## Links de Acesso

- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

## Scrapping

Para iniciar o scraper localmente não é necessario autenticação, execute:
```bash
python3 -m scripts.scrape_books --limit 2

```

Para iniciar o scraper pela API, é necessario autenticação, pelo swagger:

1. Crie o usuario administrador
2. Faça login e obtenha um token
3. No botão de autenticação do swagger, insira o token
4. No campo de limit, insira o limite de livros
5. Execute a rota POST /scraper/run

```bash
curl -X 'POST' \
  'http://localhost:8000/scraper/run' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer [YOUR_TOKEN]' \
  -d ''
```

## Monitoramento & Analytics

A aplicação possui monitoramento nativo com Prometheus e dashboard em Streamlit.

- Logs estruturados em JSON para todas as requisições
- Métricas de performance expostas em `/metrics`
- Dashboard em Streamlit consumindo métricas em tempo real

### Como executar localmente
```bash
uvicorn main:app --reload
streamlit run api/dashboard/app.py
```

### Dashboard
Acesse seu dashboard em http://localhost:8501


## Testes Automatizados

O projeto possui uma suíte completa de testes automatizados com cobertura mínima de 70%.

### Estrutura dos Testes

```
tests/
├── conftest.py                       # Fixtures compartilhadas
├── unit/                             # Testes unitários
│   ├── test_book_service.py         # Testes do serviço de livros
│   ├── test_category_service.py     # Testes do serviço de categorias
│   ├── test_stats_service.py        # Testes do serviço de estatísticas
│   └── test_health_service.py       # Testes do serviço de saúde
└── integration/                      # Testes de integração
    ├── test_auth_endpoints.py       # Testes de autenticação
    ├── test_book_endpoints.py       # Testes dos endpoints de livros
    ├── test_category_endpoints.py   # Testes dos endpoints de categorias
    ├── test_stats_endpoints.py      # Testes dos endpoints de estatísticas
    ├── test_health_endpoints.py     # Testes do endpoint de saúde
    └── test_main_endpoints.py       # Testes dos endpoints principais
```

### Executando os Testes

#### 1. Instalar Dependências de Teste

```bash
pip install -r requirements.txt
```

As dependências de teste incluem:
- `pytest` - Framework de testes
- `pytest-asyncio` - Suporte para testes assíncronos
- `pytest-cov` - Cobertura de código
- `httpx` - Cliente HTTP para testes FastAPI
- `faker` - Geração de dados de teste

#### 2. Executar Todos os Testes

```bash
pytest
```

#### 3. Executar Testes com Cobertura

```bash
pytest --cov=api --cov-report=term-missing
```

Para gerar relatório HTML de cobertura:
```bash
pytest --cov=api --cov-report=html
# Abra o arquivo htmlcov/index.html no navegador
```

#### 4. Executar Testes por Categoria

Apenas testes unitários:
```bash
pytest tests/unit/ -m unit
```

Apenas testes de integração:
```bash
pytest tests/integration/ -m integration
```

#### 5. Executar Testes Específicos

Executar um arquivo específico:
```bash
pytest tests/unit/test_book_service.py
```

Executar um teste específico:
```bash
pytest tests/unit/test_book_service.py::TestListBooks::test_list_books_default_pagination
```

#### 6. Executar com Verbosidade

```bash
pytest -v  # Modo verbose
pytest -vv # Modo extra verbose
```

### Cobertura de Código

O projeto está configurado para exigir uma cobertura mínima de **70%**. Os testes falharão se a cobertura ficar abaixo desse threshold.

Para verificar a cobertura atual:
```bash
pytest --cov=api --cov-report=term-missing
```

### CI/CD - GitHub Actions

Os testes são executados automaticamente em cada push e pull request através do GitHub Actions.

**Workflows configurados**:

#### 1. CI - Testes (`.github/workflows/ci.yml`)
- ✅ Executa em Ubuntu Latest com Python 3.12
- ✅ Cache de dependências pip
- ✅ Execução automática de todos os testes com cobertura
- ✅ Verificação de qualidade de código (Ruff)
- ✅ Análise de segurança (Bandit + Safety)
- ✅ Relatórios de cobertura para Codecov
- ✅ Triggers: push e pull requests para `main`, `master` e `develop`

#### 2. CD - Deploy (`.github/workflows/cd.yml`)
- ✅ Deploy automático para Render após CI passar
- ✅ Integração com Render API
- ✅ Notificações de status

**Badges de Status** (adicione ao topo do README):
```markdown
![CI](https://github.com/SEU-USUARIO/fiap-tech-challenge-fase-1/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/SEU-USUARIO/fiap-tech-challenge-fase-1/actions/workflows/cd.yml/badge.svg)
```

## Deploy no Render

O projeto está configurado para deploy no [Render](https://render.com) com PostgreSQL gerenciado.

### Deploy Automático (Recomendado)

1. **Crie uma conta no Render**: https://render.com

2. **Conecte seu repositório GitHub** ao Render

3. **Use o Blueprint** (render.yaml):
   - No dashboard do Render, clique em **New** → **Blueprint**
   - Selecione seu repositório
   - O Render irá detectar o `render.yaml` e criar automaticamente:
     - API FastAPI (Web Service)
     - Dashboard Streamlit (Web Service)
     - Banco PostgreSQL

4. **Configure os Secrets no GitHub** (opcional, para deploy via API):
   - `RENDER_API_KEY`: Sua API Key do Render (Settings → API Keys)
   - `RENDER_SERVICE_ID`: ID do serviço da API (visível na URL do serviço)

### URLs de Produção

Após o deploy, você terá:
- **API**: `https://fiap-tech-challenge-api.onrender.com`
- **Dashboard**: `https://fiap-tech-challenge-dashboard.onrender.com`
- **Swagger**: `https://fiap-tech-challenge-api.onrender.com/docs`

### Variáveis de Ambiente no Render

As seguintes variáveis são configuradas automaticamente via `render.yaml`:
- `DATABASE_URL` - Conexão com PostgreSQL (auto-injetada)
- `PYTHON_ENV` - Ambiente de execução
- `LOG_LEVEL` - Nível de logs
- `SCRAPER_LIMIT` - Limite de scraping

### Monitoramento

- **Health Check**: `/api/v1/health`
- **Métricas**: `/metrics` (Prometheus)
- **Logs**: Disponíveis no dashboard do Render

### Estatísticas dos Testes

- **Total de testes**: 39
- **Testes unitários**: 17
- **Testes de integração**: 22
- **Cobertura mínima**: 70%

### Fixtures Disponíveis

O arquivo `tests/conftest.py` fornece fixtures úteis:

- `db_engine` - Engine SQLite em memória para testes
- `db_session` - Sessão de banco de dados isolada
- `client` - Cliente TestClient do FastAPI
- `test_user` - Usuário de teste pré-criado
- `test_category` - Categoria de teste
- `test_book` - Livro de teste com relações
- `auth_token` - Token JWT válido para autenticação
- `auth_headers` - Headers HTTP com autenticação

### Escrevendo Novos Testes

Exemplo de teste unitário:
```python
import pytest
from api.services import book_service

@pytest.mark.unit
def test_list_books(db_session, test_book):
    books = book_service.list_books(db_session)
    assert len(books) == 1
    assert books[0].title == test_book.title
```

Exemplo de teste de integração:
```python
import pytest

@pytest.mark.integration
def test_get_all_books(client, test_book):
    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    assert len(response.json()) == 1
```


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
