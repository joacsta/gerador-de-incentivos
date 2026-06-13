from __future__ import annotations

from pathlib import Path


def obter_caminho_rascunho(periodo: int, diretorio: str) -> str:
    return str(
        Path(__file__).parents[1] / "modelos" / ".rascunhos" / str(periodo) / diretorio
    )


def obter_caminho_producao(periodo: int, diretorio: str) -> str:
    return str(
        Path.home()
        / "Projetos"
        / "sistema"
        / "processamento"
        / str(periodo)
        / diretorio
    )


OPCOES_USUARIO = ["1) Gerar novo processamento", "2) Gerar nova configuração"]
OPCOES_GRUPOS = ["Grupo A", "Grupo B", "Grupo C"]

CATEGORIAS = {
    "Categoria 1": [11, 12],
    "Categoria 2": 8,
    "Categoria 3": 10,
    "Categoria 4": 1,
    "Categoria 5": 16,
    "Categoria 6": [5, 14],
    "Categoria 7": [3, 4],
}
VINCULO_CATEGORIA = {
    "Categoria 1": 20,
    "Categoria 2": 17,
    "Categoria 3": 15,
    "Categoria 4": 15,
    "Categoria 5": 14,
    "Categoria 6": 22,
    "Categoria 7": 15,
}
ID_PERIODOS = {
    "MENSAL": 1,
    "ANUAL": 2,
    "UNICO": 3,
}
TIPO_REGISTRO = {
    "Grupo B": 3 or 1,
    "Grupo A": 4,
    "Grupo C": 5,
    "Grupo B - Ramificações": 6,
    "Grupo A - Ramificações": 7,
    "Especial (Grupo B)": 10,
    "Especial (Grupo A)": 12,
}
TIPOS_RETORNOS = {"Retorno Físico": 2, "Retorno Virtual": 3}
SUB_GRUPOS = {
    "Grupo A Integral": 6,
    "Grupo A Subdivisão 1": 8,
    "Grupo A Subdivisão 2": 7,
    "Grupo C Externo - B": 11,
    "Grupo C Externo - A": 10,
    "Grupo C Base": 9,
    "Todos os Grupos": 0,
    "Grupo B (Subtipo 1)": 2,
    "Grupo B (Subtipo 2)": 5,
    "Grupo B (Subtipo 3)": 3,
    "Grupo B (Subtipo 4)": 4,
    "Grupo B Integral": 1,
    "Grupo B | Subtipo 1": 14,
    "Grupo B | Subtipo 3 | Subtipo 1": 13,
    "Grupo B | Subtipo 3": 12,
}
MODELOS_PROCESSAMENTO = {
    "Processamento Padrão (Métrica A e B)": "metodo_padrao",
    "Processamento Padrão (Quantidade)": "metodo_padrao_quantidade",
    "Categoria 2 - Métrica de Valor": "metodo_especial_valor",
    "Categoria 2 - Métrica de Quantidade": "metodo_especial_quantidade",
    "Categoria 2 - Evento Inicial": "metodo_especial_inicial",
    "Sistema de Classificação": "metodo_classificacao",
    "Sistema de Classificação Especial": "metodo_classificacao_especial",
    "Agrupamento por Ramificação": "metodo_ramificacao",
}
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
TIPOS_CONDICOES = {
    "Métrica de Valor": 1,
    "Métrica de Quantidade": 2,
    "Classificação Geral": 3,
    "Percentual Atingido": 4,
    "Métrica Global": 5,
    "Métrica de Nível": 6,
}
MESES = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12,
}
