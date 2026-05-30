from __future__ import annotations

from pathlib import Path

from app.constants import PATH_DEV, STAGE, path_prod
from core.domain.models import Campanha, GrupoProduto
from infra.db.connection import servidor
from infra.filesystem.paths import (
    criar_diretorio_campanha,
    criar_diretorio_campanha_dev,
    nome_campanha_diretorio,
)


def gerar_apuracao(query, bind_params, grupo_produto: GrupoProduto, campanha: Campanha):
    diretorio = nome_campanha_diretorio(grupo_produto, campanha)
    path_producao = Path(path_prod(campanha.nu_ano_mes_inicio, diretorio))
    sql_query = query % tuple(bind_params)

    if servidor.server_name == STAGE:
        diretorio_desenvolvimento = criar_diretorio_campanha_dev(PATH_DEV, diretorio)
        arquivo = Path(diretorio_desenvolvimento) / "rascunho-apuracao.sql"
        arquivo.write_text(sql_query, encoding="utf-8")
        return diretorio_desenvolvimento

    diretorio_producao = criar_diretorio_campanha(path_producao)
    arquivo = Path(diretorio_producao) / "apuracao.sql"
    arquivo.write_text(sql_query, encoding="utf-8")
    return diretorio_producao
