import questionary as q

from app.constants.constants import (
    DESCRICOES_PADRAO,
    MESES,
    OPCOES_GRUPOS,
    TIPOS_RETORNOS,
)
from app.constants.enums import (
    CategoriaEnum,
    ModeloProcessamento,
    SubGrupos,
    TipoCondicoes,
    TipoRegistro,
)


def ask_categoria() -> str:
    return q.select(
        "Qual categoria o registro atual promove?", [c.label for c in CategoriaEnum]
    ).ask()


def ask_grupo(grupo_escolhido: str) -> int:
    opcoes_grupos_selecionada: list[str] | None = None
    dicionario_subgrupos = {sb.name: sb.value for sb in SubGrupos}

    for grupo in grupo_escolhido.title().split():
        opcoes_grupos_selecionada = (
            [
                nome_grupo
                for nome_grupo in list(dicionario_subgrupos.keys())
                if grupo == nome_grupo.split()[0]
            ]
            if grupo in OPCOES_GRUPOS
            else None
        )

    resposta = (
        q.select("Qual o grupo principal do registro?", opcoes_grupos_selecionada).ask()
        if opcoes_grupos_selecionada
        else q.select(
            "Qual o grupo principal do registro?", list(dicionario_subgrupos.keys())
        ).ask()
    )
    return dicionario_subgrupos[resposta]


def ask_descricao() -> str:
    q.print("Preencha a descrição do novo registro: ", style="bold")
    predefinicao = q.confirm("Deseja escolher entre as descrições pré-definidas?").ask()

    if predefinicao:
        return q.select(
            "Selecione a descrição base para a configuração:", DESCRICOES_PADRAO
        ).ask()

    descricao_usuario = q.text("Escreva a descrição do registro: ").ask()
    return descricao_usuario


def ask_tipo_registro() -> int:
    dicionario_tipo_registro = {tp.name: tp.value for tp in TipoRegistro}
    tipo_registro = q.select(
        "Qual o tipo estrutural do registro?", list(dicionario_tipo_registro.keys())
    ).ask()

    return dicionario_tipo_registro[tipo_registro]


def ask_link_recurso(tipo_recurso: str) -> str:
    url_str = q.text(f"Qual a url do recurso ({tipo_recurso})? ").ask()
    index_url = url_str.find("/uploads")
    return url_str[index_url::]


def ask_link_nivel(indice_nivel: int) -> str:
    url_nivel = q.text(
        f"Qual a url associada ao nível (índice: {indice_nivel})? "
    ).ask()
    index_url = url_nivel.find("/uploads")
    return url_nivel[index_url::]


def ask_tipo_fonte() -> int:
    tipo_fonte = q.select(
        "Selecione a fonte de dados primária: ", ["Entidades", "Ramificações"]
    ).ask()
    return 1 if tipo_fonte.lower().startswith("e") else 2


def ask_tipo_retorno() -> int:
    tipo_retorno = q.select(
        "Selecione o tipo de retorno do registro: ", choices=list(TIPOS_RETORNOS.keys())
    ).ask()
    return TIPOS_RETORNOS[tipo_retorno]


def ask_tipo_condicao() -> int:
    dicionario_tipo_condicoes = {tp.name: tp.value for tp in TipoCondicoes}

    tipo_condicao = q.select(
        "Qual o tipo de condição que será inserida? ",
        choices=list(dicionario_tipo_condicoes.keys()),
    ).ask()
    return dicionario_tipo_condicoes[tipo_condicao]


def ask_valor_decimal(pergunta: str, tipo_retorno: int = 1) -> float:
    if tipo_retorno != 1:
        return 0.0

    valor = q.text(pergunta).ask()

    if not valor.isnumeric():
        raise ValueError("O valor precisa ser numérico para continuar.")

    return float(valor)


def ask_valor_inteiro(pergunta: str) -> int | None:
    valor = q.text(pergunta).ask()

    if not valor:
        return None
    if not valor.isnumeric():
        raise ValueError("O valor precisa ser inteiro para continuar.")

    return int(valor)


def converter_para_inteiro(texto: str) -> int:
    return int(texto)


def ask_booleano(pergunta: str) -> bool:
    return q.confirm(pergunta).ask()


def ask_parametros_inicializacao() -> tuple[int, int]:
    quantidade_retornos = 1
    quantidade_condicoes = 1

    mais_retornos = q.confirm("Este registro possui mais de um retorno atrelado?").ask()

    if mais_retornos:
        resposta = ask_valor_inteiro("Quantos retornos serão associados ao registro? ")
        quantidade_retornos = resposta if resposta else 1

    mais_condicoes = q.confirm(
        "Este registro possui mais de uma condição atrelada?"
    ).ask()

    if mais_condicoes:
        resposta = ask_valor_inteiro("Quantas condições serão associadas ao registro? ")
        quantidade_condicoes = resposta if resposta else 1

    return quantidade_retornos, quantidade_condicoes


def ask_periodo_especifico() -> int | None:
    resposta = q.confirm(
        "Deseja selecionar um mês específico para o processamento?"
    ).ask()

    if resposta:
        mes_escolhido = q.select(
            "Selecione o mês: ", choices=list(MESES.keys()), show_selected=True
        ).ask()
        return int(MESES[mes_escolhido])
    return None


def ask_modelo_processamento() -> str:
    dicionario_modelo = {mp.tipo_processamento: mp.modelo for mp in ModeloProcessamento}
    escolha = q.select(
        "Selecione o modelo de processamento:", choices=list(dicionario_modelo.keys())
    ).ask()
    return dicionario_modelo[escolha]
