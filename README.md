# Gerador de Incentivos - Sistema de gamificação em CLI com Python

Um utilitário de linha de comando para configurar programas de incentivo/campanhas e gerar/executar apurações no SQL Server. Ele coleta dados via prompts, grava entidades no banco e gera scripts SQL de apuração a partir de templates Jinja, com a opção de rodar em stage  replicar em produção.

```md
# gerador-de-incentivos
CLI para criar programas de incentivo e gerar/executar apurações no SQL Server.
O fluxo é guiado por perguntas e grava os dados das campanhas nas tabelas
do schema Campanha, além de gerar scripts SQL via templates Jinja.

## Requisitos
- Python 3.10+
- Driver ODBC para SQL Server (ex.: *ODBC Driver 18 for SQL Server*)
- Acesso aos servidores STAGE/PROD configurados no código

## Instalação
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução

```bash
PYTHONPATH=src python -m app.main          # usa STAGE (padrão)
PYTHONPATH=src python -m app.main --prod   # aponta para PROD
```

## Saídas geradas

- **STAGE**: `output/drafts/templates/<campanha>/rascunho-apuracao.sql`
- **PROD**: `output/programas/<AAAAMM>/<campanha>/apuracao.sql`

## Templates de apuração

- Arquivos em `src/templates/.sql/*.j2`
- Os nomes exibidos no menu estão em `app/constants.py`

## Banco de dados

Tabelas esperadas (schema `Campanha`):
`tblCampanha`, `tblGrupoProdutoCampanha`, `tblPremiacao`,
`tblCampanhaGatilho`, `tblCampanhaGatilhoNivel`.
