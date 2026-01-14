# Guia de Deploy - Render

Este documento descreve como fazer o deploy da aplicação Tech Challenge no [Render](https://render.com).

## Arquitetura no Render

A aplicação é composta por 3 serviços:

| Serviço | Tipo | Descrição |
|---------|------|-----------|
| **fiap-tech-challenge-api** | Web Service | API FastAPI principal |
| **fiap-tech-challenge-dashboard** | Web Service | Dashboard Streamlit |
| **fiap-tech-challenge-db** | PostgreSQL | Banco de dados |

## Pré-requisitos

- Conta no [Render](https://render.com)
- Repositório conectado ao GitHub
- Branch `main` com código atualizado

## Opção 1: Deploy via Blueprint (Recomendado)

O projeto inclui um arquivo `render.yaml` que configura automaticamente todos os serviços.

### Passos:

1. Acesse o [Dashboard do Render](https://dashboard.render.com)
2. Clique em **New** → **Blueprint**
3. Conecte seu repositório GitHub
4. Selecione o repositório `fiap-tech-challenge-fase-1`
5. O Render detectará o `render.yaml` automaticamente
6. Revise os serviços que serão criados e clique em **Apply**

O Render irá criar:
- ✅ API FastAPI com Docker
- ✅ Dashboard Streamlit com Docker
- ✅ Banco PostgreSQL
- ✅ Variáveis de ambiente conectadas automaticamente

## Opção 2: Deploy Manual

### 1. Criar Banco de Dados PostgreSQL

1. No Dashboard do Render, clique em **New** → **PostgreSQL**
2. Configure:
   - **Name**: `fiap-tech-challenge-db`
   - **Database**: `tech_challenge`
   - **User**: `tech_challenge_user`
   - **Region**: Oregon (ou sua preferência)
   - **Plan**: Free
3. Clique em **Create Database**
4. Aguarde o banco ser provisionado
5. Copie a **Internal Database URL** (você vai precisar dela)

### 2. Criar Serviço da API

1. Clique em **New** → **Web Service**
2. Conecte seu repositório GitHub
3. Configure:
   - **Name**: `fiap-tech-challenge-api`
   - **Region**: Oregon (mesma do banco)
   - **Branch**: `main`
   - **Runtime**: Docker
   - **Plan**: Free
4. Em **Environment Variables**, adicione:

| Variável | Valor |
|----------|-------|
| `DATABASE_URL` | (cole a Internal Database URL do banco) |
| `PYTHON_ENV` | `production` |
| `LOG_LEVEL` | `INFO` |
| `SCRAPER_LIMIT` | `10` |

5. Em **Health Check Path**, configure: `/api/v1/health`
6. Clique em **Create Web Service**

### 3. Criar Serviço do Dashboard (Opcional)

1. Clique em **New** → **Web Service**
2. Configure:
   - **Name**: `fiap-tech-challenge-dashboard`
   - **Region**: Oregon
   - **Branch**: `main`
   - **Runtime**: Docker
   - **Dockerfile Path**: `./Dockerfile.dashboard`
   - **Plan**: Free
3. Em **Environment Variables**, adicione:

| Variável | Valor |
|----------|-------|
| `API_URL` | URL da API (ex: `https://fiap-tech-challenge-api.onrender.com`) |

4. Clique em **Create Web Service**

## Variáveis de Ambiente

### API (Obrigatórias)

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DATABASE_URL` | URL de conexão PostgreSQL | `postgresql://user:pass@host/db` |

### API (Opcionais)

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `PYTHON_ENV` | Ambiente de execução | `production` |
| `LOG_LEVEL` | Nível de logs | `INFO` |
| `SCRAPER_LIMIT` | Limite de livros no scraper | `10` |

### Dashboard

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `API_URL` | URL da API para métricas | `https://api.onrender.com` |

## URLs de Produção

Após o deploy, os serviços estarão disponíveis em:

| Serviço | URL |
|---------|-----|
| API | `https://fiap-tech-challenge-api.onrender.com` |
| Swagger | `https://fiap-tech-challenge-api.onrender.com/docs` |
| ReDoc | `https://fiap-tech-challenge-api.onrender.com/redoc` |
| Dashboard | `https://fiap-tech-challenge-dashboard.onrender.com` |
| Health Check | `https://fiap-tech-challenge-api.onrender.com/api/v1/health` |
| Métricas | `https://fiap-tech-challenge-api.onrender.com/metrics` |

> **Nota**: As URLs exatas dependem do nome dos seus serviços no Render.

## CI/CD com GitHub Actions

O projeto está configurado com pipelines de CI/CD:

### CI - Testes (`.github/workflows/ci.yml`)

Executado em cada push/PR para `main`, `master` ou `develop`:
- ✅ Testes automatizados com pytest
- ✅ Cobertura de código (mínimo 60%)
- ✅ Verificação de qualidade (Ruff)
- ✅ Análise de segurança (Bandit + Safety)

### CD - Deploy (`.github/workflows/cd.yml`)

Executado após CI passar na branch `main`:
- ✅ Trigger automático de deploy no Render

#### Configurar Deploy Automático via API (Opcional)

Para habilitar deploy via GitHub Actions:

1. No Render, vá em **Account Settings** → **API Keys**
2. Crie uma nova API Key
3. No seu repositório GitHub, vá em **Settings** → **Secrets and variables** → **Actions**
4. Adicione os secrets:

| Secret | Descrição |
|--------|-----------|
| `RENDER_API_KEY` | Sua API Key do Render |
| `RENDER_SERVICE_ID` | ID do serviço (começa com `srv-`) |

> **Nota**: Sem esses secrets, o Render ainda faz deploy automático via webhook do GitHub.

## Monitoramento

### Health Check

Endpoint: `GET /api/v1/health`

Retorna status da API e conectividade com o banco:

```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

### Métricas Prometheus

Endpoint: `GET /metrics`

Métricas disponíveis:
- Requisições por segundo
- Latência de requisições
- Erros por endpoint
- Uso de recursos

### Logs

Os logs estão disponíveis no Dashboard do Render:
1. Acesse o serviço
2. Clique na aba **Logs**
3. Visualize logs em tempo real

Os logs são estruturados em JSON para facilitar análise.

## Troubleshooting

### Erro: "could not translate host name 'db'"

**Causa**: `DATABASE_URL` está configurada com host `db` (do docker-compose local).

**Solução**: Atualize `DATABASE_URL` com a URL interna do PostgreSQL do Render.

### Erro: "DATABASE_URL não está definida"

**Causa**: Variável de ambiente não configurada.

**Solução**: Adicione `DATABASE_URL` nas Environment Variables do serviço.

### Deploy falha com "health check failed"

**Causa**: A aplicação não está respondendo no endpoint de health.

**Soluções**:
1. Verifique se `DATABASE_URL` está correta
2. Verifique os logs para erros de inicialização
3. Confirme que o health check path é `/api/v1/health`

### Aplicação lenta ou timeout

**Causa**: Plano Free tem cold starts (serviço "dorme" após inatividade).

**Soluções**:
1. Aguarde ~30 segundos na primeira requisição
2. Considere upgrade para plano pago
3. Configure um uptime monitor externo para manter o serviço ativo

## Custos

### Plano Free (Atual)

- ✅ 750 horas/mês de Web Services
- ✅ 1 banco PostgreSQL (90 dias)
- ⚠️ Cold starts após inatividade
- ⚠️ Recursos limitados

### Plano Starter ($7/mês por serviço)

- ✅ Sem cold starts
- ✅ Mais recursos
- ✅ SSL automático
- ✅ Preview environments

## Rollback

Para reverter para uma versão anterior:

1. No Dashboard do Render, acesse o serviço
2. Vá em **Events**
3. Encontre o deploy anterior que funcionava
4. Clique nos **...** → **Rollback to this deploy**

## Suporte

- [Documentação do Render](https://render.com/docs)
- [Status do Render](https://status.render.com)
- [Troubleshooting Deploys](https://render.com/docs/troubleshooting-deploys)
