# Gerador de Incentivos - Sistema de gamificação em CLI com Python

CLI para criar programas de incentivo e gerar/executar apurações no banco configurado. O fluxo é guiado por perguntas e grava os dados das campanhas nas tabelas do schema selecionado, além de gerar scripts SQL via templates Jinja.
 
## A Motivação por Trás do Projeto
 
Esse projeto nasceu de uma tarefa repetitiva do meu dia a dia em ambiente corporativo que eu queria otimizar. Sempre que era preciso configurar um novo programa de incentivo, eu precisava escrever manualmente os scripts `setup.sql` e `apuracao.sql` do zero — um processo arcaico que facilmente levava algumas horas. Pior do que o tempo gasto era a forma como isso era feito: cada script tinha que ser revisado linha a linha, comparando manualmente com apurações anteriores para garantir que nenhum atributo tivesse ficado inconsistente ou fora do padrão esperado.
 
Percebi que praticamente todas as apurações seguiam a mesma lógica estrutural, mudando apenas os atributos específicos de cada campanha. Foi esse padrão repetitivo que me levou a criar o Gerador de Incentivos: em vez de escrever SQL na mão a cada nova campanha, o usuário responde a um conjunto de perguntas guiadas, e a ferramenta se encarrega de montar os scripts a partir de templates Jinja, respeitando a estrutura já validada.
 
O resultado foi um processo que passou de horas de trabalho manual e propenso a erros para poucos minutos de execução guiada, com scripts consistentes e revisáveis desde o primeiro rascunho — inclusive com um fluxo de stage antes de qualquer coisa chegar em produção.
 
Vale reforçar que este repositório contém apenas a estrutura e a lógica do sistema, construídas para fins de estudo e portfólio: nenhum código, dado ou detalhe confidencial da empresa onde a ideia surgiu foi utilizado ou exposto aqui.
 
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
