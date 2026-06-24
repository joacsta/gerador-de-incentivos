from __future__ import annotations

from pathlib import Path

from jinjasql import JinjaSql
import questionary as q

from app.commands.commands import ask_modelo_processamento
from app.constants.enums import CategoriaEnum
from core.domain.models import Categoria, Condicao, CondicaoNivel
from infra.db.conn import servidor
from infra.db.repositories import select_statement_categoria


DIRETORIO_TEMPLATES = Path(__file__).parent / ".sql"


def aux_parametros_template(pergunta: str, escolhas: list[str], input_usuario: str):
    id_especificado = q.select(pergunta, escolhas, show_selected=True).ask()
    if id_especificado.startswith("s"):
        entrada_id = input(input_usuario)
        lista_especificada_id = [
            int(x) if x.isnumeric() else str(x) for x in entrada_id.split()
        ]
        return lista_especificada_id
    return None


def carregar_template(chave_processamento: str) -> str:
    caminho_template = DIRETORIO_TEMPLATES / f"{chave_processamento}.j2"
    return caminho_template.read_text(encoding="utf-8")


def selecionar_template() -> str:
    template_processamento = ask_modelo_processamento()
    return carregar_template(template_processamento)


def parametros_template(
    processamento,
    nome_categoria: str,
    nova_categoria: Categoria,
    condicoes: Condicao,
    condicoes_niveis: CondicaoNivel,
):

    dicionario_categoria = {c.label: c.empresa_id for c in CategoriaEnum}

    lista_categoria = []
    lista_siglas_entidades = []
    lista_condicoes = []

    processamento_entidades = carregar_template("metodo_ramificacao")
    jinja = JinjaSql()
    motor = servidor.conectar()

    if len(condicoes.lista_condicoes) > 1:
        print("\nRevise os ID's após a geração do processamento.\n")
        for nivel in condicoes_niveis.lista_niveis:
            lista_condicoes.append(nivel["idCondicao"])

    lista_item_id = aux_parametros_template(
        "O registro especifica um item ou métrica secundária?",
        ["sim", "não"],
        "insira os id's dos itens (separe por espaços, exemplo: '10 11 13'...): ",
    )
    lista_periodo_id = aux_parametros_template(
        "O registro possui delimitação de períodos específicos?",
        ["sim", "não"],
        "insira os id's dos períodos (separe por espaços, exemplo: '1 2'...): ",
    )

    if processamento == processamento_entidades:
        lista_siglas_entidades = aux_parametros_template(
            "Deseja especificar as entidades para o registro?",
            ["sim", "não"],
            "insira a sigla das entidades (ex: ENT, RAM, SEC): ",
        )

    lista_sub_grupos_id = aux_parametros_template(
        "O registro especifica sub-grupos ou ramificações exclusivas?",
        ["sim", "não"],
        "insira os id's dos sub-grupos (separe por espaços, exemplo: '3 4 5'...): ",
    )

    if nome_categoria in list(dicionario_categoria.keys()):
        id_categoria = dicionario_categoria[nome_categoria]
        lista_categoria.extend(
            id_categoria if isinstance(id_categoria, list) else [id_categoria]
        )

    dados = {
        "registro_id": nova_categoria.id_registro,
        "registro_categoria_id": select_statement_categoria(
            nova_categoria.id_registro, motor
        ),
        "categorias_id": lista_categoria,
        "item_id": lista_item_id,
        "periodo_id": lista_periodo_id,
        "siglas_entidades": lista_siglas_entidades,
        "sub_grupos": lista_sub_grupos_id,
        "condicoes_variaveis": lista_condicoes,
    }

    query, parametros_bind = jinja.prepare_query(processamento, dados)
    return query, parametros_bind
