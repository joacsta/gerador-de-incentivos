from __future__ import annotations

from dataclasses import dataclass

from jinjasql import JinjaSql

from app.constants.enums import CategoriaEnum, ModeloProcessamento
from core.domain.models import Categoria, Condicao, CondicaoNivel
from infra.db.conn import servidor
from infra.db.repositories import select_statement_categoria

from .jinja_builder import (
    aux_parametros_template,
    carregar_template,
)


@dataclass(frozen=True)
class TemplateProcessamentoStrategy:
    template_key: str
    solicita_entidades: bool = False

    @property
    def template(self) -> str:
        return carregar_template(self.template_key)

    def construir_parametros(
        self,
        nome_categoria: str,
        nova_categoria: Categoria,
        condicoes: Condicao,
        condicoes_niveis: CondicaoNivel,
    ) -> tuple[str, list]:
        dicionario_categoria = {c.label: c.empresa_id for c in CategoriaEnum}
        lista_condicoes = []

        if len(condicoes.lista_condicoes) > 1:
            print("\nRevise os ID's após a geração do processamento.\n")
            lista_condicoes = [
                nivel["idCondicao"] for nivel in condicoes_niveis.lista_niveis
            ]

        lista_item_id = aux_parametros_template(
            "O registro especifica um item ou métrica secundária?",
            ["sim", "não"],
            "insira os id's dos itens (separe por espaços, exemplo: '10 11 13'...): ",
        )
        lista_periodo_id = aux_parametros_template(
            "O registro possui delimitação de períodos específicos?",
            ["sim", "não"],
            "insira os id's dos períodos (separe por espaços, exemplo: '1 2'...): ",
        )
        lista_siglas_entidades = []
        if self.solicita_entidades:
            lista_siglas_entidades = aux_parametros_template(
                "Deseja especificar as entidades para o registro?",
                ["sim", "não"],
                "insira a sigla das entidades (ex: ENT, RAM, SEC): ",
            )
        lista_sub_grupos_id = aux_parametros_template(
            "O registro especifica sub-grupos ou ramificações exclusivas?",
            ["sim", "não"],
            "insira os id's dos sub-grupos (separe por espaços, exemplo: '3 4 5'...): ",
        )

        id_categoria = dicionario_categoria.get(nome_categoria)
        lista_categoria = (
            (id_categoria if isinstance(id_categoria, list) else [id_categoria])
            if id_categoria is not None
            else []
        )

        dados = {
            "registro_id": nova_categoria.id_registro,
            "registro_categoria_id": select_statement_categoria(
                nova_categoria.id_registro, servidor.conectar()
            ),
            "categorias_id": lista_categoria,
            "item_id": lista_item_id,
            "periodo_id": lista_periodo_id,
            "siglas_entidades": lista_siglas_entidades,
            "sub_grupos": lista_sub_grupos_id,
            "condicoes_variaveis": lista_condicoes,
        }
        return JinjaSql().prepare_query(self.template, dados)


class RamificacaoProcessamentoStrategy(TemplateProcessamentoStrategy):
    def __init__(self) -> None:
        super().__init__("metodo_ramificacao", solicita_entidades=True)


_ESTRATEGIAS = {
    modelo.modelo: TemplateProcessamentoStrategy(modelo.modelo)
    for modelo in ModeloProcessamento
    if modelo.modelo != "metodo_ramificacao"
}
_ESTRATEGIAS["metodo_ramificacao"] = RamificacaoProcessamentoStrategy()


def selecionar_estrategia() -> TemplateProcessamentoStrategy:
    from app.commands.commands import ask_modelo_processamento

    return _ESTRATEGIAS[ask_modelo_processamento()]


def estrategia_para_processamento(
    processamento: str,
) -> TemplateProcessamentoStrategy:
    for estrategia in _ESTRATEGIAS.values():
        if estrategia.template == processamento:
            return estrategia
    raise ValueError("Modelo de processamento não reconhecido.")
