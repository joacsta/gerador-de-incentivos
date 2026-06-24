from __future__ import annotations

import calendar as c
import locale as l
from pathlib import Path

l.setlocale(l.LC_ALL)
MESES = {c.month_name[i]: i for i in range(1, 13)}


def obter_caminho_rascunho(periodo: int, diretorio: str) -> Path:
    return (
        Path(__file__).parents[1] / "modelos" / ".rascunhos" / str(periodo) / diretorio
    )


def obter_caminho_producao(periodo: int, diretorio: str) -> Path:
    return (
        Path.home()
        / "Projetos"
        / "sistema"
        / "processamento"
        / str(periodo)
        / diretorio
    )


OPCOES_USUARIO = ["1) Gerar novo processamento", "2) Gerar nova configuração"]
OPCOES_GRUPOS = ["Grupo A", "Grupo B", "Grupo C"]
TIPOS_RETORNOS = {"Retorno Físico": 3, "Retorno Virtual": 3}
DESCRICOES_PADRAO = [
    "Acelere os resultados, alcance os marcos e troque por retornos ao final do período!",
    "Os eventos gerados e validados serão reconhecidos com um retorno especial!",
    "As ramificações com melhor desempenho ganharão vantagens extras!",
    "As entidades que atingirem ou superarem o objetivo estipulado garantem o retorno exclusivo.",
    "Atinja a meta estabelecida e resgate os retornos disponíveis!",
    "Fique entre os primeiros colocados na classificação e garanta sua vantagem!",
    "Os destaques do período serão bonificados conforme a regra de negócio!",
    "Processos validados e concluídos serão recompensados com retornos proporcionais!",
    "Realize o primeiro evento do ciclo e ganhe retornos exclusivos!",
    "Conclua a etapa inicial e seja reconhecido no sistema!",
    "Suas entregas validadas podem proporcionar excelentes retornos!",
]
