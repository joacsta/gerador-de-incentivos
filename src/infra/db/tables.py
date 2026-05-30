from sqlalchemy import MetaData, Table, select

from infra.db.connection import servidor

metadata = MetaData()


def table_campanha() -> Table:
    engine = servidor.database_connection
    return Table("tblCampanha", metadata, autoload_with=engine, schema="Campanha")


def table_grupo_produto() -> Table:
    engine = servidor.database_connection
    return Table(
        "tblGrupoProdutoCampanha", metadata, autoload_with=engine, schema="Campanha"
    )


def table_premiacao() -> Table:
    engine = servidor.database_connection
    return Table("tblPremiacao", metadata, autoload_with=engine, schema="Campanha")


def table_gatilho() -> Table:
    engine = servidor.database_connection
    return Table(
        "tblCampanhaGatilho", metadata, autoload_with=engine, schema="Campanha"
    )


def table_gatilho_nivel() -> Table:
    engine = servidor.database_connection
    return Table(
        "tblCampanhaGatilhoNivel", metadata, autoload_with=engine, schema="Campanha"
    )


def select_stmt_campanhas():
    engine = servidor.database_connection
    user_table = Table("tblCampanha", metadata, autoload_with=engine, schema="Campanha")
    return select(user_table).order_by(user_table.columns.idCampanha.desc()).limit(10)
