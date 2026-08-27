from dataclasses import dataclass

from sqlalchemy import MetaData, create_engine

from app.config import (
    AMBIENTE_PRINCIPAL,
    AMBIENTE_TESTE,
    DATABASE_URL,
    DATABASE_URL_PRINCIPAL,
    DATABASE_URL_TESTE,
    DB_SCHEMA,
    obter_argumentos,
)


nome_servidor, nome_banco = obter_argumentos()
metadata = MetaData()


@dataclass
class Servidor:
    nome_servidor: str = AMBIENTE_TESTE
    nome_banco: str = "SISTEMA_DB"
    url: str | None = None

    @property
    def schema(self) -> str | None:
        return None if self.url_dialeto == "sqlite" else DB_SCHEMA

    @property
    def url_dialeto(self) -> str:
        return (self.url or self._url_configurada() or "mssql").split(":", 1)[0]

    def _url_configurada(self) -> str | None:
        if self.url:
            return self.url
        if self.nome_servidor == AMBIENTE_PRINCIPAL:
            return DATABASE_URL_PRINCIPAL or DATABASE_URL
        if self.nome_servidor == AMBIENTE_TESTE:
            return DATABASE_URL_TESTE or DATABASE_URL
        return None

    def _url_sql_server(self) -> str:
        # sql server: pyodbc, trusted connection e a string de conexao abaixo precisam
        # ser substituidos quando outro dialeto for usado.
        from pyodbc import drivers

        if len(drivers()) < 2:
            raise RuntimeError("Nenhum driver ODBC adequado foi encontrado.")
        return (
            "mssql+pyodbc:///?odbc_connect="
            f"DRIVER={drivers()[1]}"
            f"SERVER={self.nome_servidor};"
            f"DATABASE={self.nome_banco};"
            "Trusted_Connection=yes;"
        )

    def conectar(self):
        url = self._url_configurada()
        return create_engine(url if url else self._url_sql_server(), echo=True)


servidor = Servidor(nome_servidor, nome_banco)
