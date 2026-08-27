from __future__ import annotations

from pathlib import Path

import questionary as q

from core.domain.models import Categoria, Condicao, CondicaoNivel


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
    from app.commands.commands import ask_modelo_processamento

    template_processamento = ask_modelo_processamento()
    return carregar_template(template_processamento)


def parametros_template(
    processamento,
    nome_categoria: str,
    nova_categoria: Categoria,
    condicoes: Condicao,
    condicoes_niveis: CondicaoNivel,
):
    from .strategies import estrategia_para_processamento

    return estrategia_para_processamento(processamento).construir_parametros(
        nome_categoria, nova_categoria, condicoes, condicoes_niveis
    )
