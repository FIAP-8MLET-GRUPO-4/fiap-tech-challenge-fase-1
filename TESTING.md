# Guia de Testes Automatizados

Este documento fornece informações detalhadas sobre a suíte de testes do projeto.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Instalação](#instalação)
- [Executando Testes](#executando-testes)
- [Estrutura dos Testes](#estrutura-dos-testes)
- [Cobertura de Código](#cobertura-de-código)
- [CI/CD](#cicd)
- [Escrevendo Testes](#escrevendo-testes)
- [Boas Práticas](#boas-práticas)

## 🎯 Visão Geral

O projeto possui **39 testes automatizados** divididos em:
- **17 testes unitários** - Testam funcionalidades isoladas (services)
- **22 testes de integração** - Testam endpoints da API

**Cobertura mínima exigida**: 70%

## 📦 Instalação

Instale as dependências de teste:

```bash
pip install -r requirements.txt
```

### Dependências de Teste

- `pytest==8.3.4` - Framework de testes
- `pytest-asyncio==0.25.2` - Suporte para testes assíncronos
- `pytest-cov==6.0.0` - Relatórios de cobertura
- `httpx==0.28.1` - Cliente HTTP para testar FastAPI
- `faker==33.5.0` - Geração de dados fake para testes

## 🚀 Executando Testes

### Comandos Básicos

```bash
# Executar todos os testes
pytest

# Executar com verbosidade
pytest -v

# Executar com extra verbosidade
pytest -vv

# Executar e mostrar prints
pytest -s
```

### Testes por Categoria

```bash
# Apenas testes unitários
pytest tests/unit/ -m unit

# Apenas testes de integração
pytest tests/integration/ -m integration

# Testes lentos (quando marcados)
pytest -m slow
```

### Testes Específicos

```bash
# Executar arquivo específico
pytest tests/unit/test_book_service.py

# Executar classe específica
pytest tests/unit/test_book_service.py::TestListBooks

# Executar teste específico
pytest tests/unit/test_book_service.py::TestListBooks::test_list_books_default_pagination

# Executar testes que contêm palavra-chave no nome
pytest -k "book"
```

### Cobertura de Código

```bash
# Ver cobertura no terminal
pytest --cov=api --cov-report=term-missing

# Gerar relatório HTML
pytest --cov=api --cov-report=html
# Depois abra: htmlcov/index.html

# Gerar relatório XML (para CI/CD)
pytest --cov=api --cov-report=xml

# Falhar se cobertura < 70%
pytest --cov=api --cov-fail-under=70
```

### Opções Avançadas

```bash
# Parar no primeiro erro
pytest -x

# Parar após N falhas
pytest --maxfail=3

# Executar último teste que falhou
pytest --lf

# Executar testes falhados primeiro
pytest --ff

# Modo paralelo (requer pytest-xdist)
pytest -n auto
```

## 📁 Estrutura dos Testes

```
tests/
├── conftest.py                       # Fixtures compartilhadas
├── unit/                             # Testes unitários
│   ├── test_book_service.py         # 9 testes - Serviço de livros
│   ├── test_category_service.py     # 3 testes - Serviço de categorias
│   ├── test_stats_service.py        # 4 testes - Serviço de estatísticas
│   └── test_health_service.py       # 1 teste - Serviço de saúde
└── integration/                      # Testes de integração
    ├── test_auth_endpoints.py       # 6 testes - Autenticação
    ├── test_book_endpoints.py       # 7 testes - Endpoints de livros
    ├── test_category_endpoints.py   # 3 testes - Endpoints de categorias
    ├── test_stats_endpoints.py      # 4 testes - Endpoints de estatísticas
    ├── test_health_endpoints.py     # 1 teste - Health check
    └── test_main_endpoints.py       # 1 teste - Endpoint raiz
```

### Detalhamento dos Testes

#### Testes Unitários (17 testes)

**test_book_service.py (9 testes)**
- ✅ Listagem com paginação padrão
- ✅ Listagem com offset customizado
- ✅ Listagem com banco vazio
- ✅ Busca por ID existente
- ✅ Busca por ID inexistente
- ✅ Busca por título
- ✅ Busca por categoria
- ✅ Busca por título e categoria
- ✅ Busca sem resultados

**test_category_service.py (3 testes)**
- ✅ Listagem de categorias
- ✅ Listagem ordenada alfabeticamente
- ✅ Listagem com banco vazio

**test_stats_service.py (4 testes)**
- ✅ Estatísticas gerais com livros
- ✅ Estatísticas gerais com banco vazio
- ✅ Estatísticas por categoria com livros
- ✅ Estatísticas por categoria com banco vazio

**test_health_service.py (1 teste)**
- ✅ Verificação de saúde do sistema

#### Testes de Integração (22 testes)

**test_auth_endpoints.py (6 testes)**
- ✅ Login com sucesso
- ✅ Login com senha errada
- ✅ Login com usuário inexistente
- ✅ Refresh token com sucesso
- ✅ Refresh token inválido
- ✅ Registro de admin (sucesso e duplicado)

**test_book_endpoints.py (7 testes)**
- ✅ Listar todos os livros
- ✅ Listar com paginação
- ✅ Listar com banco vazio
- ✅ Buscar por título
- ✅ Buscar por categoria
- ✅ Buscar por título e categoria
- ✅ Buscar sem resultados
- ✅ Detalhes de livro existente
- ✅ Detalhes de livro inexistente (404)

**test_category_endpoints.py (3 testes)**
- ✅ Listar todas as categorias
- ✅ Categorias ordenadas alfabeticamente
- ✅ Listar com banco vazio

**test_stats_endpoints.py (4 testes)**
- ✅ Estatísticas gerais com dados
- ✅ Estatísticas gerais vazias
- ✅ Estatísticas por categoria com dados
- ✅ Estatísticas por categoria vazias

**test_health_endpoints.py (1 teste)**
- ✅ Health check endpoint

**test_main_endpoints.py (1 teste)**
- ✅ Endpoint raiz (Hello World)

## 🎨 Fixtures Disponíveis

O arquivo `conftest.py` fornece fixtures reutilizáveis:

### Fixtures de Banco de Dados

```python
def test_example(db_session):
    # db_session: Sessão SQLAlchemy isolada
    # Criada e destruída para cada teste
```

### Fixtures de Cliente HTTP

```python
def test_example(client):
    # client: TestClient do FastAPI
    response = client.get("/api/v1/books/")
```

### Fixtures de Dados

```python
def test_example(test_user, test_category, test_book):
    # test_user: Usuário pré-criado
    # test_category: Categoria "Fiction"
    # test_book: Livro com todas as relações
```

### Fixtures de Autenticação

```python
def test_example(auth_token, auth_headers):
    # auth_token: Token JWT válido
    # auth_headers: {"Authorization": "Bearer <token>"}
```

## 📊 Cobertura de Código

### Verificar Cobertura Atual

```bash
pytest --cov=api --cov-report=term-missing
```

Saída esperada:
```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
api/services/book_service.py         45      2    96%   12, 34
api/services/category_service.py      8      0   100%
api/services/stats_service.py        32      1    97%   56
api/services/health_service.py       18      0   100%
---------------------------------------------------------------
TOTAL                               450     45    90%
```

### Meta de Cobertura

- **Mínimo exigido**: 70%
- **Meta ideal**: 80%+
- **Arquivos críticos**: 90%+

### Áreas Não Cobertas

Algumas áreas são intencionalmente excluídas:
- Scripts de scraping (execução manual)
- Configurações de logging
- Arquivos de migração
- Dashboard Streamlit

## 🤖 CI/CD

### GitHub Actions

Arquivo: `.github/workflows/tests.yml`

**Triggers:**
- Push para `main`, `develop`
- Pull requests para `main`, `develop`

**Ambiente:**
- Ubuntu Latest
- Python 3.11
- PostgreSQL 15

**Pipeline:**
1. Checkout do código
2. Setup Python com cache
3. Instalação de dependências
4. Execução de testes com pytest
5. Upload de cobertura para Codecov

### Variáveis de Ambiente no CI

```yaml
DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb
JWT_SECRET_KEY: test-secret-key-for-testing-only
JWT_ALGORITHM: HS256
ACCESS_TOKEN_EXPIRE_MINUTES: 30
REFRESH_TOKEN_EXPIRE_DAYS: 7
```

### Badge de Status

Adicione ao README.md:

```markdown
![Tests](https://github.com/FIAP-8MLET-GRUPO-4/fiap-tech-challenge-fase-1/actions/workflows/tests.yml/badge.svg)
```

## ✍️ Escrevendo Testes

### Teste Unitário Exemplo

```python
import pytest
from api.services import book_service

@pytest.mark.unit
class TestBookService:
    """Testes para o serviço de livros."""

    def test_list_books(self, db_session, test_book):
        """Testa listagem de livros."""
        # Arrange (preparação)
        # test_book já criado pela fixture

        # Act (ação)
        books = book_service.list_books(db_session)

        # Assert (verificação)
        assert len(books) == 1
        assert books[0].title == test_book.title
```

### Teste de Integração Exemplo

```python
import pytest

@pytest.mark.integration
class TestBookEndpoints:
    """Testes para os endpoints de livros."""

    def test_get_all_books(self, client, test_book):
        """Testa GET /api/v1/books/."""
        # Act
        response = client.get("/api/v1/books/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == test_book.title
```

### Teste com Autenticação

```python
@pytest.mark.integration
def test_protected_endpoint(client, auth_headers):
    """Testa endpoint que requer autenticação."""
    response = client.post(
        "/scraper/run",
        headers=auth_headers,
        json={"limit": 10}
    )
    assert response.status_code == 200
```

## 📚 Boas Práticas

### Nomenclatura

- ✅ Arquivos: `test_*.py`
- ✅ Classes: `TestNomeDoRecurso`
- ✅ Métodos: `test_o_que_esta_sendo_testado`
- ✅ Use docstrings descritivas

### Estrutura AAA

```python
def test_example():
    # Arrange - Preparação
    user = create_test_user()

    # Act - Ação
    result = authenticate(user)

    # Assert - Verificação
    assert result.is_authenticated
```

### Isolamento

- ✅ Cada teste deve ser independente
- ✅ Use fixtures para setup/teardown
- ✅ Não dependa da ordem de execução
- ✅ Use banco em memória (SQLite)

### Clareza

- ✅ Um conceito por teste
- ✅ Nomes descritivos
- ✅ Mensagens de erro úteis
- ✅ Evite lógica complexa nos testes

### Performance

- ✅ Testes rápidos < 1 segundo
- ✅ Marque testes lentos com `@pytest.mark.slow`
- ✅ Use mocks para operações lentas
- ✅ Evite sleeps desnecessários

### Cobertura

- ✅ Teste casos de sucesso
- ✅ Teste casos de erro
- ✅ Teste edge cases
- ✅ Teste validações
- ✅ Não busque 100% sem razão

## 🐛 Troubleshooting

### Testes Falhando Localmente

```bash
# Limpar cache
pytest --cache-clear

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar ambiente
python --version  # Deve ser 3.11+
pip list | grep pytest
```

### Erro de Import

```bash
# Adicionar projeto ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Banco de Dados em Uso

Os testes usam SQLite em memória, mas se houver problemas:

```bash
# Parar containers Docker
docker compose down -v
```

### Debug de Testes

```python
# Adicionar breakpoint
import pdb; pdb.set_trace()

# Ou usar pytest com debug
pytest --pdb  # Para no primeiro erro
pytest --trace  # Inicia debug no início
```

## 📞 Suporte

Se encontrar problemas com os testes:

1. Verifique este documento
2. Execute testes localmente com `-vv`
3. Verifique os logs do GitHub Actions
4. Abra uma issue no repositório

---

**Última atualização**: 2026-01-11
**Versão do pytest**: 8.3.4
**Cobertura atual**: 70%+
