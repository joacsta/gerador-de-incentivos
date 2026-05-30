from __future__ import annotations

from sqlalchemy import text

from core.domain.models import Campanha, GrupoProduto
from infra.db.connection import servidor
from infra.filesystem.writer_apuracao import gerar_apuracao
from templates.jinja_builder import select_template, template_params


class Apuracao:
    def __init__(self, grupo_produto: GrupoProduto, campanha: Campanha) -> None:
        self.nome_produto = grupo_produto.nome_grupo_produto
        self.grupo_produto = grupo_produto
        self.tipo_participante = campanha.tipo_participante
        self.nu_ano_mes = campanha.nu_ano_mes_inicio
        self.campanha = campanha

        self.apuracao_selecionada = None
        self.statement = None
        self.query = None
        self.params = None

    def select_apuracao(self) -> str:
        self.apuracao_selecionada = select_template()
        return self.apuracao_selecionada

    def select_template(self, apuracao: str):
        return template_params(apuracao, self.nome_produto, self.grupo_produto)

    def create_statement(self, query, params):
        self.params = params
        self.query = query

        template_query = query % tuple(params)
        self.statement = text(template_query)
        return self.statement

    def create_apuracao(self, query, params) -> None:
        selected_path = gerar_apuracao(query, params, self.grupo_produto, self.campanha)
        print(f"Script gerado em: {selected_path}")

    def execute(self, stmt, engine) -> None:
        print(f"Executando a apuração no servidor {servidor.server_name}...")

        with engine.begin() as conn:
            try:
                conn.execute(stmt)
                conn.commit()
                print("Feito!")
            except Exception as exc:
                print("Erro ao executar a apuração:", exc)
                print("Abortando execução.")
                raise
