from __future__ import annotations

from pprint import pprint

import questionary

from app.commands.commands import converter_para_inteiro
from app.constants import TIPOS_CONDICOES
from core.domain.models import (
    Categoria,
    Condicao,
    CondicaoNivel,
    Registro,
    Retorno,
    idCondicaoNiveis,
)
from infra.db.repositories import insert_statement
from infra.db.tables import (
    table_categoria,
    table_condicao,
    table_condicao_nivel,
    table_registro,
    table_retorno,
)


class Configuracao:
    def __init__(
        self,
        registro_principal: Registro,
        categoria_vinculada: Categoria,
        retornos: Retorno,
        condicoes: Condicao,
        condicoes_nivel: CondicaoNivel,
    ) -> None:
        self.registro_principal = registro_principal
        self.categoria_vinculada = categoria_vinculada
        self.retornos = retornos
        self.condicoes = condicoes
        self.condicoes_nivel = condicoes_nivel

    @property
    def preview(self) -> bool:
        previews = [
            ("---tblRegistro---", self.registro_principal.values()),
            ("---tblCategoriaVinculada---", self.categoria_vinculada.values()),
            ("---tblRetorno---", self.retornos.values()),
            ("---tblRegistroCondicao---", self.condicoes.values()),
            ("---tblRegistroCondicaoNivel---", self.condicoes_nivel.values()),
        ]
        for titulo, preview in previews:
            questionary.print(f"\n{titulo}\n")
            pprint(preview)
            resposta = input("\nContinuar? [s]im, [n]ão ou [p]ular preview: ")

            if resposta.lower().strip().startswith("p"):
                return True

            if resposta.lower().strip().startswith("n"):
                print("Abortar.")
                return False

        return True

    def values(self):
        return [
            self.registro_principal.values(),
            self.categoria_vinculada.values(),
            self.retornos.values(),
            self.condicoes.values(),
            self.condicoes_nivel.values(),
        ]

    def reset_pks(self):
        self.registro_principal.id_registro = None

        self.categoria_vinculada.id_registro = None
        self.categoria_vinculada.id_categoria = None

        self.retornos.reset_id_registro()
        self.retornos.reset_id_categoria()

        self.condicoes.reset_id_registro()

        for index, _ in enumerate(self.condicoes_nivel.values()):
            self.condicoes_nivel.reset_id_condicao(index)

    def insert_data(self, motor):
        id_condicoes = []

        with motor.begin() as conn:
            try:
                idRegistro = insert_statement(
                    conn, table_registro(), self.registro_principal.values()
                )
                self.categoria_vinculada.id_registro = idRegistro
                idCategoriaVinculada = insert_statement(
                    conn, table_categoria(), self.categoria_vinculada.values()
                )
                self.retornos.set_id_registro(idRegistro)
                self.retornos.set_id_categoria(idCategoriaVinculada)

                for retorno in self.retornos.values():
                    insert_statement(conn, table_retorno(), retorno)

                self.condicoes.set_id_registro(idRegistro)

                for condicao in self.condicoes.values():
                    idCondicao = insert_statement(conn, table_condicao(), condicao)
                    id_condicao = idCondicaoNiveis(
                        id_condicao=idCondicao,
                        descricao_condicao=next(
                            key
                            for key, value in TIPOS_CONDICOES.items()
                            if value == condicao["idTipoCondicao"]
                        ),
                    )

                    id_condicoes.append(
                        tuple(valor for valor in id_condicao._asdict().values())
                    )

                if len(self.condicoes.values()) > 1:
                    lista_id_condicoes = [str(nivel) for nivel in id_condicoes]
                    for i, nivel in enumerate(self.condicoes_nivel.values()):
                        id_selecionado = questionary.select(
                            f"Selecione a Condição (id) que o nível {i + 1} será associado:",
                            choices=lista_id_condicoes,
                            show_selected=True,
                        ).ask()

                        self.condicoes_nivel.set_id_condicao(
                            i, converter_para_inteiro(id_selecionado)
                        )
                        insert_statement(conn, table_condicao_nivel(), nivel)

                for i, nivel in enumerate(self.condicoes_nivel.values()):
                    self.condicoes_nivel.set_id_condicao(i, id_condicoes[0][0])
                    insert_statement(conn, table_condicao_nivel(), nivel)

            except Exception as e:
                print("Erro ao inserir dados: ", e)
                print("Abortando execução")
                raise e

        print("Dados inseridos com sucesso.")
        return (
            self.registro_principal,
            self.categoria_vinculada,
            self.retornos,
            self.condicoes,
            self.condicoes_nivel,
        )
