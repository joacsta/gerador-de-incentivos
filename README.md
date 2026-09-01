# Gerador de Incentivos - Sistema de gamificação em CLI com Python

Um utilitário de linha de comando para configurar programas de incentivo/campanhas e gerar/executar apurações no banco de dados. Ele coleta dados via prompts, grava entidades no banco e gera scripts SQL de apuração a partir de templates Jinja, com a opção de rodar em stage e replicar em produção.

## Requisitos

- Python 3.10+
- Docker e Docker Compose (para MSSQL)
- Uma cópia de .env

## Instalação

1. Clone ou abra o repositório
2. Copie o arquivo de exemplo:

```bash
cp .env-example .env
```

1. Inicie o banco de dados (MSSQL via Docker):

```bash
docker-compose up -d
```

1. Configure o ambiente Python:

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Execução

```bash
PYTHONPATH=src python -m app.main
```

A conexão usa a URL do SQLAlchemy configurada em `DATABASE_URL_TESTE` (para stage) ou
`DATABASE_URL_PRINCIPAL` (para produção), ambas no `.env`. O padrão é usar MSSQL via Docker.

## Saídas geradas

- **STAGE**: `output/drafts/templates/<diretorio>/rascunho-apuracao.sql`
- **PROD**: `output/programas/<AAAAMM>/<diretorio>/apuracao.sql`

## Templates de apuração

- Arquivos em `src/templates/.sql/*.j2`
- Os nomes exibidos no menu estão em `app/constants.py`
