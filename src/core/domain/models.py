from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, List, NamedTuple

import questionary

from app.commands.commands import (
    ask_categoria,
    ask_descricao,
    ask_grupo,
    ask_link_recurso,
    ask_tipo_fonte,
    ask_tipo_registro,
)
from app.constants import VINCULO_CATEGORIA
from app.services.calendar import selecionar_data

from .commands import _build_attr_condicoes, _build_attr_niveis, _build_attr_retornos


@dataclass
class Registro:
    nome_registro: str
    tipo_participante: int
    id_registro: int | None
    descricao: str
    nu_ano_mes_inicio: int
    nu_ano_mes_fim: int
    url_recurso_a: str
    url_recurso_b: str
    tipo_registro: int
    dt_processamento: date

    @classmethod
    def create(cls) -> "Registro":
        nome_registro_ = questionary.text("Qual o nome do novo registro? ").ask()
        descricao_ = ask_descricao()
        tipo_participante_ = ask_grupo(nome_registro_)
        nu_ano_mes, data_fim_processamento = selecionar_data()
        url_recurso_a_ = ask_link_recurso("principal")
        url_recurso_b_ = ask_link_recurso("secundario")
        tipo_registro_ = ask_tipo_registro()

        return cls(
            nome_registro=nome_registro_,
            descricao=descricao_,
            tipo_participante=tipo_participante_,
            nu_ano_mes_inicio=nu_ano_mes,
            nu_ano_mes_fim=nu_ano_mes,
            url_recurso_a=url_recurso_a_,
            url_recurso_b=url_recurso_b_,
            tipo_registro=tipo_registro_,
            dt_processamento=data_fim_processamento,
            id_registro=None,
        )

    def values(self):
        return {
            "noRegistro": self.nome_registro,
            "deRegistro": self.descricao,
            "nuAnoMesInicio": self.nu_ano_mes_inicio,
            "nuAnoMesFim": self.nu_ano_mes_fim,
            "deImagemRecursoA": self.url_recurso_a,
            "deLogoRegistro": "",
            "deImagemRecursoB": self.url_recurso_b,
            "dhCriacao": datetime.now(),
            "dhAlteracao": datetime.now(),
            "idSituacaoRegistro": 1,
            "idTipoRegistro": self.tipo_registro,
            "icProcessamentoPeriodico": 1,
            "dtFimProcessamento": self.dt_processamento,
            "idTipoParticipante": self.tipo_participante,
            "icEmAtualizacao": 0,
        }


@dataclass
class Categoria:
    id_categoria: int | None
    id_registro: int | None
    nome_categoria: str
    tipo_fonte: int
    vinculo_id: int

    @classmethod
    def create(cls):
        nome_categoria_ = ask_categoria()
        tipo_fonte_ = ask_tipo_fonte()
        vinculo_id_ = VINCULO_CATEGORIA[nome_categoria_]

        return cls(
            id_categoria=None,
            id_registro=None,
            nome_categoria=nome_categoria_,
            tipo_fonte=tipo_fonte_,
            vinculo_id=vinculo_id_,
        )

    def values(self):
        return {
            "idRegistro": self.id_registro,
            "noCategoria": self.nome_categoria,
            "idTipoFonte": self.tipo_fonte,
            "deIcone": "",
            "deCor": "",
            "idVinculo": self.vinculo_id,
            "idTipoProcessamento": 1,
            "nuOrdemApresentacao": 0,
        }


@dataclass
class Retorno:
    nu_ano_mes: int
    quantidade_retornos: int = 1
    lista_retornos: List[Dict] = field(default_factory=list)
    id_registro: int | None = None
    id_categoria: int | None = None

    @classmethod
    def build(cls, nu_ano_mes: int, quantidade_retornos: int = 1) -> "Retorno":
        return cls(
            nu_ano_mes=nu_ano_mes,
            quantidade_retornos=quantidade_retornos,
            lista_retornos=_build_attr_retornos(
                nu_ano_mes, None, None, quantidade_retornos
            ),
        )

    def reset_id_registro(self):
        for retorno in self.lista_retornos:
            retorno["idRegistro"] = None

    def reset_id_categoria(self):
        for retorno in self.lista_retornos:
            retorno["idCategoriaVinculada"] = None

    def set_id_registro(self, idRegistro: int):
        self.id_registro = idRegistro
        for retorno in self.lista_retornos:
            retorno["idRegistro"] = idRegistro

    def set_id_categoria(self, idCategoriaVinculada: int):
        self.id_categoria = idCategoriaVinculada
        for retorno in self.lista_retornos:
            retorno["idCategoriaVinculada"] = idCategoriaVinculada

    def values(self):
        return self.lista_retornos


@dataclass
class Condicao:
    dicionario_categoria: dict
    nu_ano_mes: int
    quantidade_condicoes: int = 1
    lista_condicoes: List[Dict] = field(default_factory=list)
    id_registro: int | None = None

    @classmethod
    def build(
        cls, nu_ano_mes: int, quantidade_condicoes: int, dicionario_categoria: dict
    ) -> "Condicao":
        return cls(
            dicionario_categoria=dicionario_categoria,
            nu_ano_mes=nu_ano_mes,
            quantidade_condicoes=quantidade_condicoes,
            lista_condicoes=_build_attr_condicoes(
                None, nu_ano_mes, dicionario_categoria, quantidade_condicoes
            ),
        )

    def reset_id_registro(self):
        for condicao in self.lista_condicoes:
            condicao["idRegistro"] = None

    def set_id_registro(self, idRegistro: int):
        self.id_registro = idRegistro
        for condicao in self.lista_condicoes:
            condicao["idRegistro"] = idRegistro

    def values(self):
        return self.lista_condicoes


@dataclass
class CondicaoNivel:
    lista_retornos: List[Dict]
    lista_niveis: List[Dict] = field(default_factory=list)

    @classmethod
    def build(cls, lista_retornos: list):
        return cls(
            lista_retornos=lista_retornos,
            lista_niveis=_build_attr_niveis(lista_retornos),
        )

    def reset_id_condicao(self, index):
        self.lista_niveis[index]["idCondicao"] = None

    def set_id_condicao(self, index: int, idCondicao: int):
        self.lista_niveis[index]["idCondicao"] = idCondicao

    def values(self):
        return self.lista_niveis


class idCondicaoNiveis(NamedTuple):
    id_condicao: int
    descricao_condicao: str
