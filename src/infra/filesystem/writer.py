from __future__ import annotations

from pathlib import Path

from app.config import AMBIENTE_TESTE
from app.constants import obter_caminho_producao, obter_caminho_rascunho
from core.domain.models import Registro, Categoria
from infra.db.conn import servidor
from infra.filesystem.paths import criar_diretorio, nome_diretorio_registro


def gerar_script_processamento(
    query, parametros_bind, categoria_vinculada: Categoria, registro_principal: Registro
):
    diretorio = nome_diretorio_registro(categoria_vinculada, registro_principal)
    sql_query = query % tuple(parametros_bind)

    if servidor.nome_servidor == AMBIENTE_TESTE:
        diretorio_rascunho = obter_caminho_rascunho(
            registro_principal.nu_ano_mes_inicio, diretorio
        )
        criar_diretorio(diretorio_rascunho)

        with open(
            Path(diretorio_rascunho) / "draft-passo-1-processamento.sql",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(sql_query)
            return diretorio_rascunho

    diretorio_producao = obter_caminho_producao(
        registro_principal.nu_ano_mes_inicio, diretorio
    )
    criar_diretorio(diretorio_producao)

    with open(
        Path(diretorio_producao) / "passo-1-processamento.sql", "w", encoding="utf-8"
    ) as f:
        f.write(sql_query)
        return diretorio_producao
