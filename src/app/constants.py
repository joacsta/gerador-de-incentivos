from __future__ import annotations

from pathlib import Path

BASE_OUTPUT_DIR = Path.cwd() / "output"
PATH_DEV = BASE_OUTPUT_DIR / "drafts"

PROD = "SQL-PROD"
STAGE = "SQL-STAGE"

USER_OPTIONS = [
    "1) Criar programa e gerar apuração",
    "2) Criar programa (sem apuração)",
]

OPCOES_REDES = [
    "Todos os segmentos",
    "Canal A - Nacional",
    "Canal A - Regional",
    "Canal B - Online",
    "Canal B - Parceiros",
    "Canal C - Premium",
]

REDES = {
    "Todos os segmentos": 0,
    "Canal A - Nacional": 1,
    "Canal A - Regional": 2,
    "Canal B - Online": 3,
    "Canal B - Parceiros": 4,
    "Canal C - Premium": 5,
}

TIPO_CAMPANHA = {
    "Incentivo de performance": 1,
    "Incentivo de adoção": 2,
    "Competição interna": 3,
    "Programa por unidades": 4,
}

PRODUTOS = [
    "Produto A",
    "Produto B",
    "Produto C",
    "Produto D",
]

GRUPO_PRODUTOS = {
    "Produto A": [101, 102],
    "Produto B": [201],
    "Produto C": [301],
    "Produto D": [401],
}

EMPRESA_PRODUTO = {
    "Produto A": 10,
    "Produto B": 20,
    "Produto C": 30,
    "Produto D": 40,
}

DICIONARIO_APURACOES = {
    "Valor total (geral)": "padrao",
    "Quantidade de eventos (geral)": "padrao_quantidade",
    "Produto especial - valor": "consorcio",
    "Produto especial - quantidade": "consorcio_quantidade",
    "Primeiro evento (produto especial)": "consorcio_primeira_venda",
    "Programa de badges": "selo_mania",
    "Programa de badges (produto especial)": "selo_consorcio",
    "Ranking por unidade": "unidades",
}

DESCRICOES_CAMPANHAS = {
    "Reconhecer resultados do período": (
        "Programa para reconhecer resultados e incentivar melhores práticas."
    ),
    "Incentivar ativação de novos serviços": (
        "Programa focado na ativação e uso recorrente dos serviços."
    ),
    "Engajar unidades em metas locais": (
        "Programa de metas regionais para fortalecer o engajamento."
    ),
}

TIPO_GATILHOS = {
    "Meta única": 1,
    "Meta por faixa": 2,
    "Meta por produto": 3,
    "Meta por segmento": 4,
    "Meta por unidade": 5,
    "Meta por badges": 6,
}

TIPO_PREMIACOES = {
    "Bônus": 1,
    "Experiência": 2,
    "Brinde": 3,
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

ID_PERIODOS = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

TIPO_APURACAO = {
    "Mensal": 1,
    "Data específica": 2,
}


def path_prod(nu_ano_mes: int, diretorio: str) -> str:
    return str(BASE_OUTPUT_DIR / "programas" / str(nu_ano_mes) / diretorio)
