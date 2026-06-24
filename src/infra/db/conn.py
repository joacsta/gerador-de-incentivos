from dataclasses import dataclass

from pyodbc import drivers
from sqlalchemy import MetaData, create_engine

from app.config import AMBIENTE_TESTE, obter_argumentos


nome_servidor, nome_banco = obter_argumentos()
metadata = MetaData()


@dataclass
class Servidor:
    nome_servidor: str = AMBIENTE_TESTE
    nome_banco: str = "SISTEMA_DB"

    def conectar(self):
        return create_engine(
            "mssql+pyodbc:///?odbc_connect="
            f"DRIVER={drivers()[1]}"
            f"SERVER={self.nome_servidor};"
            f"DATABASE={self.nome_banco};"
            "Trusted_Connection=yes;",
            echo=True,
        )


servidor = Servidor(nome_servidor, nome_banco)
