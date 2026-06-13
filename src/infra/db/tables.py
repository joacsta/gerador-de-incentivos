from sqlalchemy import MetaData, Table, select

from infra.db.conn import servidor

metadata = MetaData()


def table_registro() -> Table:
    motor = servidor.conectar
    return Table("tblRegistro", metadata, autoload_with=motor, schema="ModuloPrincipal")


def table_categoria() -> Table:
    motor = servidor.conectar
    return Table(
        "tblCategoriaVinculada", metadata, autoload_with=motor, schema="ModuloPrincipal"
    )


def table_retorno() -> Table:
    motor = servidor.conectar
    return Table("tblRetorno", metadata, autoload_with=motor, schema="ModuloPrincipal")


def table_condicao() -> Table:
    motor = servidor.conectar
    return Table(
        "tblRegistroCondicao", metadata, autoload_with=motor, schema="ModuloPrincipal"
    )


def table_condicao_nivel() -> Table:
    motor = servidor.conectar
    return Table(
        "tblRegistroCondicaoNivel",
        metadata,
        autoload_with=motor,
        schema="ModuloPrincipal",
    )


def select_stmt_registros():
    motor = servidor.conectar
    tabela_usuario = Table(
        "tblRegistro", metadata, autoload_with=motor, schema="ModuloPrincipal"
    )
    return (
        select(tabela_usuario)
        .order_by(tabela_usuario.columns.idRegistro.desc())
        .limit(10)
    )
