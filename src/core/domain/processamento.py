from __future__ import annotations

from sqlalchemy import text

from core.domain.models import Categoria, Condicao, CondicaoNivel, Registro
from infra.db.conn import servidor
from infra.filesystem.writer import gerar_script_processamento
from templates.strategies import (
    TemplateProcessamentoStrategy,
    estrategia_para_processamento,
    selecionar_estrategia,
)


class Processamento:
    def __init__(
        self,
        categoria_vinculada: Categoria,
        registro_principal: Registro,
        condicoes: Condicao,
        condicoes_nivel: CondicaoNivel,
    ) -> None:
        self.nome_categoria = categoria_vinculada.nome_categoria
        self.categoria_vinculada = categoria_vinculada
        self.condicoes = condicoes
        self.condicoes_nivel = condicoes_nivel
        self.tipo_participante = registro_principal.tipo_participante
        self.nu_ano_mes = registro_principal.nu_ano_mes_inicio
        self.registro_principal = registro_principal

        self.processamento_selecionado = None
        self.estrategia: TemplateProcessamentoStrategy | None = None
        self.declaracao = None
        self.query = None
        self.parametros = None

    def selecionar_processamento(self) -> str:
        self.estrategia = selecionar_estrategia()
        self.processamento_selecionado = self.estrategia.template
        return self.processamento_selecionado

    def selecionar_modelo(self, processamento):
        estrategia = self.estrategia or estrategia_para_processamento(processamento)
        return estrategia.construir_parametros(
            self.nome_categoria,
            self.categoria_vinculada,
            self.condicoes,
            self.condicoes_nivel,
        )

    def criar_declaracao(self, query, parametros):
        self.parametros = parametros
        self.query = query

        template_query = query % tuple(parametros)
        self.declaracao = text(template_query)
        return self.declaracao

    def criar_registro(self, query, parametros) -> None:
        caminho_selecionado = gerar_script_processamento(
            query, parametros, self.categoria_vinculada, self.registro_principal
        )
        print(f"Script gerado em: {caminho_selecionado}")

    def execute(self, stmt, motor) -> None:
        print(f"Executando o processamento no servidor: {servidor.nome_servidor}...")

        with motor.begin() as conn:
            try:
                conn.execute(stmt)
                conn.commit()
                print("Feito!")

            except Exception as exc:
                print("Erro ao executar o processamento:", exc)
                print("Abortando execução.")
                raise exc
