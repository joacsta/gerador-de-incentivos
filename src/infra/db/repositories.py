from sqlalchemy import Engine, Table, select, insert

from infra.db.tables import table_grupo_produto


def insert_statement(conn, table: Table, data: dict):
    coluna_pk = list(table.primary_key.columns)[0]
    statement = insert(table).values(data).returning(coluna_pk)
    return conn.execute(statement).scalar_one()


def select_statement_grupo_produto(id_campanha, engine: Engine):
    with engine.begin() as conn:
        table = table_grupo_produto()
        statement = select(table.c["idGrupoProdutoCampanha"]).where(
            table.c["idCampanha"] == id_campanha
        )
        return conn.execute(statement).scalar_one_or_none()
