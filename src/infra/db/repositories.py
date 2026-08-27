from sqlalchemy import Engine, Table, insert, select

from infra.db.conn import metadata, servidor
from infra.db.tables import table_categoria


def insert_statement(conn, table: Table, data: dict) -> int:
    coluna_pk = list(table.primary_key.columns)[0]
    statement = insert(table).values(data)
    if conn.dialect.insert_returning:
        return conn.execute(statement.returning(coluna_pk)).scalar_one()

    result = conn.execute(statement)
    return result.inserted_primary_key[0]


def select_statement_categoria(id_registro: int, motor: Engine) -> int | None:
    table = table_categoria()

    with motor.begin() as conn:
        return conn.execute(
            select(table.c.idCategoriaVinculada).where(
                table.c.idRegistro == id_registro
            )
        ).scalar_one_or_none()


def select_stmt_registros():
    motor = servidor.conectar()
    tabela_usuario = Table(
        "tblRegistro", metadata=metadata, autoload_with=motor, schema=servidor.schema
    )
    return select(tabela_usuario).order_by(tabela_usuario.c.idRegistro.desc()).limit(10)
