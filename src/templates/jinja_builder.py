from __future__ import annotations

from pathlib import Path

from jinjasql import JinjaSql
from questionary import select

from app.commands.commands import ask_apuracao
from app.constants import GRUPO_PRODUTOS
from core.domain.models import GrupoProduto
from infra.db.connection import servidor
from infra.db.repositories import select_statement_grupo_produto

TEMPLATES_DIR = Path(__file__).parent / ".sql"


def select_template() -> str:
    return ask_apuracao()


def aux_template_params(pergunta: str, escolhas: list[str], input_user: str):
    id_specified = select(pergunta, escolhas, show_selected=True).ask()
    if id_specified.startswith("s"):
        id_input = input(input_user)
        lista_especificada_id = [
            int(x) if x.isdigit() else str(x) for x in id_input.split()
        ]
        return lista_especificada_id
    return None


def load_template(apuracao_key: str) -> str:
    template_path = TEMPLATES_DIR / f"{apuracao_key}.j2"
    return template_path.read_text(encoding="utf-8")


def template_params(apuracao: str, nome_produto: str, novo_grupo_produto: GrupoProduto):
    list_id_grupo_produto = []
    list_siglas_unidades = []
    list_subredes = []

    jinja = JinjaSql()
    engine = servidor.database_connection

    list_produto_id = aux_template_params(
        "Deseja limitar a apuração a produtos específicos?",
        ["sim", "não"],
        "Insira os IDs dos produtos (separe por espaços, exemplo: '10 11 13'): ",
    )
    list_periodo_id = aux_template_params(
        "Deseja limitar a apuração a períodos específicos?",
        ["sim", "não"],
        "Insira os IDs dos períodos (separe por espaços, exemplo: '1 2'): ",
    )

    if apuracao == "unidades":
        list_siglas_unidades = aux_template_params(
            "Deseja especificar as unidades participantes?",
            ["sim", "não"],
            "Insira as siglas das unidades (ex: SEC, SEV, SEE): ",
        )

    list_subredes = aux_template_params(
        "Deseja limitar a apuração a subsegmentos?",
        ["sim", "não"],
        "Insira os IDs de subsegmentos (separe por espaços, exemplo: '3 4 5'): ",
    )

    if nome_produto in list(GRUPO_PRODUTOS.keys()):
        id_grupo_produto = GRUPO_PRODUTOS[nome_produto]
        list_id_grupo_produto.extend(
            id_grupo_produto
            if isinstance(id_grupo_produto, list)
            else [id_grupo_produto]
        )

    data = {
        "campanha_id": novo_grupo_produto.id_campanha,
        "campanha_grupo_prd_id": select_statement_grupo_produto(
            novo_grupo_produto.id_campanha, engine
        ),
        "grupos_id": list_id_grupo_produto,
        "produto_id": list_produto_id,
        "periodo_id": list_periodo_id,
        "siglas_unidades": list_siglas_unidades,
        "sub_redes": list_subredes,
    }

    template = load_template(apuracao)
    query, bind_params = jinja.prepare_query(template, data)
    return query, bind_params
