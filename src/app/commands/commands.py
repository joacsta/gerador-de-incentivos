import questionary

from app.constants import (
    DESCRICOES_PADRAO,
    MODELOS_PROCESSAMENTO,
    MESES,
    OPCOES_GRUPOS,
    CATEGORIAS,
    SUB_GRUPOS,
    TIPO_REGISTRO,
    TIPOS_CONDICOES,
    TIPOS_RETORNOS,
)


def ask_categoria() -> str:
    return questionary.select(
        "Qual categoria o registro atual promove?",
        list(CATEGORIAS.keys()),
        show_selected=True,
    ).ask()


def ask_grupo(grupo_escolhido) -> int:
    opcoes_grupos_selecionada = None

    for grupo in grupo_escolhido.title().split():
        opcoes_grupos_selecionada = (
            [
                nome_grupo
                for nome_grupo in list(SUB_GRUPOS.keys())
                if grupo == nome_grupo.split()[0]
            ]
            if grupo in OPCOES_GRUPOS
            else None
        )

    resposta = (
        questionary.select(
            "Qual o grupo principal do registro?",
            opcoes_grupos_selecionada,
            show_selected=True,
        ).ask()
        if opcoes_grupos_selecionada
        else questionary.select(
            "Qual o grupo principal do registro?",
            list(SUB_GRUPOS.keys()),
            show_selected=True,
        ).ask()
    )
    return SUB_GRUPOS[resposta]


def ask_descricao() -> str:
    questionary.print("Preencha a descrição do novo registro: ", style="bold")
    predefinicao = questionary.confirm(
        "Deseja escolher entre as descrições pré-definidas?"
    ).ask()

    if predefinicao:
        return questionary.select(
            "Selecione a descrição base para a configuração:",
            DESCRICOES_PADRAO,
        ).ask()
    descricao_usuario = questionary.text("Escreva a descrição do registro: ").ask()
    return descricao_usuario


def ask_tipo_registro() -> int:
    tipo_registro = questionary.select(
        "Qual o tipo estrutural do registro?",
        list(TIPO_REGISTRO.keys()),
        show_selected=True,
    ).ask()
    return TIPO_REGISTRO[tipo_registro]


def ask_link_recurso(tipo_recurso: str) -> str:
    url_str = questionary.text(f"Qual a url do recurso ({tipo_recurso})? ").ask()
    index_url = url_str.find("/uploads")
    return url_str[index_url::]


def ask_link_nivel(indice_nivel: int) -> str:
    url_nivel = questionary.text(
        f"Qual a url associada ao nível (índice: {indice_nivel})? "
    ).ask()
    index_url = url_nivel.find("/uploads")
    return url_nivel[index_url::]


def ask_tipo_fonte() -> int:
    tipo_fonte = questionary.select(
        "Selecione a fonte de dados primária: ",
        ["Entidades Individuais", "Ramificações"],
        show_selected=True,
    ).ask()
    return 1 if tipo_fonte.lower().startswith("e") else 2


def ask_tipo_retorno() -> int:
    tipo_retorno = questionary.select(
        "Selecione o tipo de retorno do registro: ",
        choices=list(TIPOS_RETORNOS.keys()),
        show_selected=True,
    ).ask()
    return TIPOS_RETORNOS[tipo_retorno]


def ask_tipo_condicao() -> int:
    tipo_condicao = questionary.select(
        "Qual o tipo de condição que será inserida? ",
        choices=list(TIPOS_CONDICOES.keys()),
        show_selected=True,
    ).ask()
    return TIPOS_CONDICOES[tipo_condicao]


def ask_valor_decimal(pergunta: str, tipo_retorno: int = 1) -> float:

    if tipo_retorno != 1:
        return 0.0

    valor = questionary.text(pergunta).ask()

    if not valor.isnumeric():
        raise ValueError("O valor precisa ser numérico para continuar.")

    return float(valor)


def ask_valor_inteiro(pergunta: str) -> int | None:
    valor = questionary.text(pergunta).ask()

    if not valor:
        return None
    if not valor.isnumeric():
        raise ValueError("O valor precisa ser inteiro para continuar.")

    return int(valor)


def converter_para_inteiro(texto: str) -> int | None:
    if texto.isnumeric():
        return int(texto)
    return None


def ask_booleano(pergunta: str) -> bool:
    return questionary.confirm(pergunta).ask()


def ask_parametros_inicializacao() -> tuple[int, int]:
    quantidade_retornos = ask_valor_inteiro(
        "Quantos retornos serão disponibilizados? (insira números inteiros): "
    )
    mais_condicoes = questionary.confirm(
        "Este registro possui mais de uma condição atrelada?"
    ).ask()

    quantidade_retornos = quantidade_retornos if quantidade_retornos else 1
    quantidade_condicoes = 1

    if mais_condicoes:
        resposta = ask_valor_inteiro("Quantas condições serão associadas ao registro? ")
        quantidade_condicoes = resposta if resposta else 1

    return quantidade_retornos, quantidade_condicoes


def ask_periodo_especifico() -> int | None:

    reposta_usuario = questionary.confirm(
        "Deseja selecionar um mês específico para o processamento?"
    ).ask()

    if not reposta_usuario:
        return None

    mes_escolhido = questionary.select(
        "Selecione o mês: ",
        choices=list(MESES.keys()),
    ).ask()
    return int(MESES[mes_escolhido])


def ask_modelo_processamento() -> str:
    escolha = questionary.select(
        "Selecione o modelo de processamento:",
        choices=list(MODELOS_PROCESSAMENTO.keys()),
    ).ask()
    return MODELOS_PROCESSAMENTO[escolha]
