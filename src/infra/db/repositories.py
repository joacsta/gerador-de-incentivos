from sqlalchemy import Engine, Table, insert, select

from infra.db.conn import metadata, servidor
from infra.db.tables import table_categoria


def insert_statement(conn, table: Table, data: dict):
    coluna_pk = list(table.primary_key.columns)[0]
    statement = insert(table).values(data).returning(coluna_pk)
    return conn.execute(statement).scalar_one()


def select_statement_categoria(id_registro, motor: Engine):
    with motor.begin() as conn:
        table = table_categoria()
        statement = select(table.c["idCategoriaVinculada"]).where(
            table.c["idRegistro"] == id_registro
        )
        return conn.execute(statement).scalar_one_or_none()


def select_stmt_registros():
    motor = servidor.conectar()
    tabela_usuario = Table(
        "tblRegistro", metadata=metadata, autoload_with=motor, schema="ModuloPrincipal"
    )
    return (
        select(tabela_usuario)
        .order_by(tabela_usuario.columns.idRegistro.desc())
        .limit(10)
    )
