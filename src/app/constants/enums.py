from enum import Enum, IntEnum, auto


class CategoriaEnum(Enum):
    CATEGORIA_UM = ("Categoria 1", [11, 12], 20)
    CATEGORIA_DOIS = ("Categoria 2", [8], 17)
    CATEGORIA_TRES = ("Categoria 3", [10], 15)
    CATEGORIA_QUATRO = ("Categoria 4", [1], 15)
    CATEGORIA_CINCO = ("Categoria 5", [16], 14)
    CATEGORIA_SEIS = ("Categoria 6", [5, 14], 22)
    CATEGORIA_SETE = ("Categoria 7", [3, 4], 15)

    def __init__(self, label: str, grupo_id: list[int], empresa_id: int) -> None:
        self.label = label
        self.grupo_id = grupo_id
        self.empresa_id = empresa_id


class Periodizacao(IntEnum):
    MENSAL = 1
    ANUAL = 2
    UNICO = 3


class ModeloProcessamento(Enum):
    PADRAO = ("Padrão (Métrica A e B)", "metodo_padrao")
    METRICA_VALOR = ("Categoria 2 - Métrica de Valor", "metodo_especial_valor")
    CLASSIFICACAO = ("Sistema de Classificação", "metodo_classificacao")
    PADRAO_QUANTIDADE = ("Padrão (Quantidade)", "metodo_padrao_quantidade")
    METRICA_QTD = ("Categoria 2 - Métrica de Quantidade", "metodo_especial_quantidade")
    EVENTO_INICIAL = ("Categoria 2 - Evento Inicial", "metodo_especial_inicial")
    CLASSIFICAO_ESPECIAL = ("Classificação Especial", "metodo_classificacao_especial")
    AGRUPAMENTO = ("Agrupamento por Ramificação", "metodo_ramificacao")

    def __init__(self, tipo_processamento: str, modelo: str) -> None:
        self.tipo_processamento = tipo_processamento
        self.modelo = modelo


class TipoRegistro(IntEnum):
    GRUPO_A = 3
    GRUPO_B = 4
    GRUPO_C = 5
    GRUPO_A_RAMIFICACAO = 6
    GRUPO_B_RAMIFICACAO = 7
    ESPECIAl_GRUPO_A = 10
    ESPECIAl_GRUPO_B = 12


class TipoCondicoes(IntEnum):
    METRICA_VALOR = auto()
    METRICA_QTD = auto()
    CLASSIFICACAO_GERAL = auto()
    METRICA_GLOBAL = auto()
    METRICA_NIVEL = auto()


class SubGrupos(IntEnum):
    TODOS = 0
    GRUPO_B_INTEGRAL = 1
    GRUPO_B_SUBTIPO_UM = 2
    GRUPO_B_SUBTIPO_DOIS = 3
    GRUPO_B_SUBTIPO_TRES = 4
    GRUPO_B_SUBTIPO_QUATRO = 5
    GRUPO_A_INTEGRAL = 6
    GRUPO_A_SUBDIVISAO_UM = 7
    GRUPO_A_SUBDIVISAO_DOIS = 8
    GRUPO_C_BASE = 9
    GRUPO_C_EXTERNO_A = 10
    GRUPO_C_EXTERNO_B = 11
    GRUPO_B_SUBTIPO_TRES_UM = 14
