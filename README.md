# Gerador de Incentivos - Sistema de gamificação em CLI com Python

Um utilitário de linha de comando para configurar programas de incentivo/campanhas e gerar/executar apurações no banco de dados. Ele coleta dados via prompts, grava entidades no banco e gera scripts SQL de apuração a partir de templates Jinja, com a opção de rodar em stage e replicar em produção.

```md
# gerador-de-incentivos
CLI para criar programas de incentivo e gerar/executar apurações no banco configurado.
O fluxo é guiado por perguntas e grava os dados das campanhas nas tabelas
do schema selecionado, além de gerar scripts SQL via templates Jinja.

## Requisitos
- Python 3.10+
- Driver correspondente ao banco escolhido (SQL Server/ODBC, PostgreSQL ou MySQL)
- Uma cópia de .env

## Instalação
cp .env-example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução

```bash
PYTHONPATH=src python -m app.main
```

As conexões usam URLs do SQLAlchemy em `DATABASE_URL_TESTE` e
`DATABASE_URL_PRINCIPAL`. SQLite usa, por exemplo,
`sqlite:///./incentivos.db`; PostgreSQL e MySQL usam os formatos demonstrados
em `.env-example`.

Os templates de processamento ainda contêm sintaxe específica do SQL Server.
Para executar os processamentos em PostgreSQL ou MySQL, eles precisam ser
adaptados ao dialeto correspondente; a persistência das configurações já usa
o dialeto configurado.

## Saídas geradas

- **STAGE**: `output/drafts/templates/<diretorio>/rascunho-apuracao.sql`
- **PROD**: `output/programas/<AAAAMM>/<diretorio>/apuracao.sql`

## Templates de apuração

- Arquivos em `src/templates/.sql/*.j2`
- Os nomes exibidos no menu estão em `app/constants.py`
