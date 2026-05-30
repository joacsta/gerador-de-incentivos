from __future__ import annotations

from datetime import datetime

from questionary import confirm, select, text

from app.constants import (
    DICIONARIO_APURACOES,
    DESCRICOES_CAMPANHAS,
    OPCOES_REDES,
    PRODUTOS,
    TIPO_CAMPANHA,
    TIPO_GATILHOS,
    TIPO_PREMIACOES,
)


def ask_nome_campanha() -> str:
    nome_campanha = ""
    while not nome_campanha:
        nome_campanha = text("Qual o nome do programa?").ask()
        if not nome_campanha:
            print("Nome inválido.")
    return nome_campanha


def ask_descricao() -> str:
    descricao = select(
        "Escolha uma descrição-base para o programa:",
        choices=list(DESCRICOES_CAMPANHAS.keys()),
    ).ask()
    return f"{DESCRICOES_CAMPANHAS[descricao]}"


def ask_rede() -> str:
    tipo_participante = select(
        "Qual o segmento do programa?", choices=OPCOES_REDES
    ).ask()
    return tipo_participante


def ask_produto() -> str:
    nome_produto = select(
        "Qual categoria principal do programa?", choices=PRODUTOS
    ).ask()
    return nome_produto


def ask_tipo_produtos() -> int:
    escolha = select(
        "Selecione a fonte principal de dados:",
        choices=["Base A (operações)", "Base B (contratos)"],
    ).ask()
    return 1 if escolha.lower().startswith("base a") else 2


def ask_tipo_campanha() -> str:
    return select(
        "Selecione o tipo do programa:",
        choices=list(TIPO_CAMPANHA.keys()),
    ).ask()


def ask_tipo_premiacao() -> str:
    return select(
        "Qual o tipo de recompensa?", choices=list(TIPO_PREMIACOES.keys())
    ).ask()


def ask_tipo_gatilho() -> str:
    return select("Qual o tipo de meta?", choices=list(TIPO_GATILHOS.keys())).ask()


def ask_valor_decimal(pergunta: str) -> float:
    valor_gatilho = text(pergunta).ask()
    if not valor_gatilho:
        return 0
    valor_gatilho = valor_gatilho.replace(",", ".")
    return float(valor_gatilho)


def ask_valor_inteiro(pergunta: str) -> int | None:
    valor = text(pergunta).ask()
    if not valor:
        return None
    if not valor.isnumeric():
        raise ValueError("valor precisa ser numérico para continuar.")
    return int(valor)


def ask_url_faixa() -> str:
    return text("Cole o link da planilha de faixas:").ask()


def ask_todos_cnpj() -> bool:
    return confirm("Aplicar para todas as organizações?").ask()


def ask_parametros_setup() -> tuple[int | None, int]:
    quantidade_gatilhos = 1
    quantidade_premiacoes = ask_valor_inteiro(
        "Quantas recompensas serão disponibilizadas? (insira números inteiros): "
    )
    mais_gatilhos = confirm("Esse programa possui mais de uma meta?").ask()
    if mais_gatilhos:
        resposta = ask_valor_inteiro("Quantas metas serão associadas ao programa? ")
        quantidade_gatilhos = resposta if resposta else 1
    return quantidade_premiacoes, quantidade_gatilhos


def ask_boolean(texto: str) -> bool:
    return confirm(texto).ask()


def ask_gerar_apuracao() -> bool:
    return confirm("Deseja gerar a apuração agora?").ask()


def ask_apuracao() -> str:
    escolha = select(
        "Selecione o modelo de apuração:", choices=list(DICIONARIO_APURACOES.keys())
    ).ask()
    return DICIONARIO_APURACOES[escolha]


def ask_data_especifica() -> int:
    data = text("Data específica da apuração (mmaaaa):").ask()
    data = str(data or "").strip()
    if len(data) != 6 or not data.isnumeric():
        data = datetime.now().strftime("%m%Y")
    return int(data)


def get_converte_inteiro(valor: str) -> int | None:
    if valor.isnumeric():
        return int(valor)
    return None
