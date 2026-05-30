from sqlalchemy import create_engine
from pyodbc import drivers

from app.config import argument
from app.constants import PROD

server_name, db_name = argument()


class Server:
    def __init__(self, server_name: str, db_name: str) -> None:
        self.server_name = server_name
        self.db_name = db_name

    @property
    def database_connection(self):
        driver_name = drivers()[1]
        database_connection_str = (
            "mssql+pyodbc:///?odbc_connect="
            f"DRIVER={driver_name};"
            f"SERVER={self.server_name};"
            f"DATABASE={self.db_name};"
            "Trusted_Connection=yes;"
        )
        return create_engine(database_connection_str, echo=False)

    @property
    def change_connection(self):
        self.server_name = PROD

    def show_server(self):
        print(f"Servidor Atual: {self.server_name}")


servidor = Server(server_name, db_name)
