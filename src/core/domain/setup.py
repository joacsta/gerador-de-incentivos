from __future__ import annotations

from pprint import pprint

from questionary import select

from app.commands.commands import get_converte_inteiro
from app.constants import TIPO_GATILHOS
from core.domain.models import Campanha, Gatilho, GatilhosNivel, GrupoProduto, Premiacao
from infra.db.repositories import insert_statement
from infra.db.tables import (
    table_campanha,
    table_gatilho,
    table_gatilho_nivel,
    table_grupo_produto,
    table_premiacao,
)


class Setup:
    def __init__(
        self,
        campanha: Campanha,
        grupo_produto: GrupoProduto,
        premiacoes: Premiacao,
        gatilhos: Gatilho,
        gatilho_nivel: GatilhosNivel,
    ) -> None:
        self.campanha = campanha
        self.grupo_produto = grupo_produto
        self.premiacao = premiacoes
        self.gatilhos = gatilhos
        self.gatilho_nivel = gatilho_nivel

    def values(self) -> list:
        return [
            self.campanha.values,
            self.grupo_produto.values,
            self.premiacao.values,
            self.gatilhos.values,
            self.gatilho_nivel.values,
        ]

    @property
    def reset_pks(self) -> None:
        self.campanha.id_campanha = None

        self.grupo_produto.id_campanha = None
        self.grupo_produto.id_grupo_produto = None

        self.premiacao.reset_id_campanha()
        self.premiacao.reset_id_grupo_produto()

        self.gatilhos.reset_id_campanha()

        for index, _ in enumerate(self.gatilho_nivel.values):
            self.gatilho_nivel.set_id_gatilho(index, None)

    @property
    def preview(self) -> bool:
        previews = [
            ("---tblCampanha---", self.campanha.values),
            ("---tblGrupoProdutoCampanha---", self.grupo_produto.values),
            ("---tblPremiacao---", self.premiacao.values),
            ("---tblCampanhaGatilho---", self.gatilhos.values),
            ("---tblCampanhaGatilhoNivel---", self.gatilho_nivel.values),
        ]
        for titulo, preview in previews:
            print(f"\n{titulo}\n")
            pprint(preview)
            resposta = input("\nContinuar? [s]im ou [n]ão: ")
            if resposta.lower().startswith("n"):
                print("Abortar.")
                return False
        return True

    def insert_data(self, engine):
        id_gatilhos = []
        with engine.begin() as conn:
            try:
                id_campanha = insert_statement(
                    conn, table_campanha(), self.campanha.values
                )
                self.grupo_produto.id_campanha = id_campanha
                id_grupo_produto = insert_statement(
                    conn, table_grupo_produto(), self.grupo_produto.values
                )
                self.premiacao.set_id_campanha(id_campanha)
                self.premiacao.set_id_grupo_produto(id_grupo_produto)

                for premiacao in self.premiacao.values:
                    insert_statement(conn, table_premiacao(), premiacao)
                self.gatilhos.set_id_campanha(id_campanha)

                for gatilho in self.gatilhos.values:
                    id_gatilho = insert_statement(conn, table_gatilho(), gatilho)
                    id_gatilho_com_nome = (
                        id_gatilho,
                        next(
                            (
                                key
                                for key, value in TIPO_GATILHOS.items()
                                if value == gatilho["idTipoGatilho"]
                            ),
                            None,
                        ),
                    )
                    id_gatilhos.append(id_gatilho_com_nome)
                if len(self.gatilhos.values) == 1:
                    self.gatilho_nivel.set_id_gatilho(0, id_gatilhos[0][0])

                    for gatilho_nivel in self.gatilho_nivel.values:
                        insert_statement(conn, table_gatilho_nivel(), gatilho_nivel)
                else:
                    lista_id_gatilhos = [
                        str(gatilho_nivel) for gatilho_nivel in id_gatilhos
                    ]
                    for index_gatilho, gatilho_nivel in enumerate(
                        self.gatilho_nivel.values
                    ):
                        id_gatilho_selecionado = select(
                            "Selecione a meta (id) para associar este nível:",
                            choices=lista_id_gatilhos,
                            show_selected=True,
                        ).ask()
                        numero_id_gatilho = get_converte_inteiro(id_gatilho_selecionado)
                        self.gatilho_nivel.set_id_gatilho(
                            index_gatilho, numero_id_gatilho
                        )
                        insert_statement(conn, table_gatilho_nivel(), gatilho_nivel)
            except Exception as exc:
                print("Erro ao inserir dados:", exc)
                print("Abortando execução.")
                raise

        print("Dados inseridos com sucesso.")
        return (
            self.campanha,
            self.grupo_produto,
            self.premiacao,
            self.gatilhos,
            self.gatilho_nivel,
        )
