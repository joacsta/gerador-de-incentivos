from sqlalchemy import Table

from infra.db.conn import metadata, servidor


def _table(nome: str) -> Table:
    return Table(
        nome, metadata, autoload_with=servidor.conectar(), schema=servidor.schema
    )


def table_registro() -> Table:
    return _table("tblRegistro")


def table_categoria() -> Table:
    return _table("tblCategoriaVinculada")


def table_retorno() -> Table:
    return _table("tblRetorno")


def table_condicao() -> Table:
    return _table("tblRegistroCondicao")


def table_condicao_nivel() -> Table:
    return _table("tblRegistroCondicaoNivel")
