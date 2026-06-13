from sqlalchemy import create_engine
from pyodbc import drivers

from app.config import obter_argumentos, AMBIENTE_PRINCIPAL

nome_servidor, nome_banco = obter_argumentos()


class Servidor:
    def __init__(self, nome_servidor: str, nome_banco: str) -> None:
        self.nome_servidor = nome_servidor
        self.nome_banco = nome_banco

    @property
    def conectar(self):
        driver_name = drivers()[1]
        return create_engine(
            "mssql+pyodbc:///?odbc_connect="
            f"DRIVER={driver_name};"
            f"SERVER={self.nome_servidor};"
            f"DATABASE={self.nome_banco};"
            "Trusted_Connection=yes;",
            echo=True,
        )

    @property
    def alterar_conexao(self):
        self.nome_servidor = AMBIENTE_PRINCIPAL

    def servidor_atual(self):
        print(f"Servidor Atual: {self.nome_servidor}")


servidor = Servidor(nome_servidor, nome_banco)
