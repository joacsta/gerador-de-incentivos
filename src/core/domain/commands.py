from datetime import datetime

import questionary

from app.commands.commands import (
    ask_link_nivel,
    ask_tipo_condicao,
    ask_tipo_retorno,
    ask_valor_decimal,
    ask_valor_inteiro,
)


def _build_attr_retornos(
    nu_ano_mes: int,
    id_registro: int | None,
    id_categoria: int | None,
    quantidade_retornos: int = 1,
):
    lista = []

    for i in range(quantidade_retornos):
        questionary.print(f"{i + 1}º retorno", style="bold")

        id_tipo_retorno = ask_tipo_retorno()
        vr_retorno = ask_valor_decimal(
            f"Insira o valor do {i + 1}º retorno do registro (valor a ser computado):",
            id_tipo_retorno,
        )
        descricao_retorno = questionary.text(
            f"Qual o nome do {i + 1}º retorno do registro? "
        ).ask()
        vr_objetivo_retorno = ask_valor_decimal(
            f"Qual o valor do objetivo do {i + 1}º retorno? "
        )
        nu_qtd_limite_retorno = ask_valor_inteiro(
            f"Quantas entidades o {i + 1}º retorno abrange? "
        )
        lista.append(
            {
                "deRetorno": descricao_retorno,
                "nuAnoMes": nu_ano_mes,
                "noTipoEntidade": None,
                "noTipoGrupo": None,
                "nuPorteEntidade": None,
                "vrRetorno": vr_retorno,
                "vrObjetivoRetorno": vr_objetivo_retorno,
                "idTipoRetorno": id_tipo_retorno,
                "nuQtdLimiteRetorno": nu_qtd_limite_retorno,
                "deImgRetorno": "",
                "idRegistro": id_registro,
                "idCategoriaVinculada": id_categoria,
            }
        )
    return lista


def _build_attr_condicoes(
    id_registro: int | None,
    nu_ano_mes: int,
    dicionario: dict,
    quantidade_condicoes: int = 1,
):
    lista = []

    for i in range(quantidade_condicoes):
        questionary.print(f"{i + 1}º condição:", style="bold")
        tipo_condicao = ask_tipo_condicao()
        nome_base = ("Modelo Especial") if tipo_condicao == 6 else "Modelo Padrão"
        grupo = dicionario["noCategoria"]
        lista.append(
            {
                "idRegistro": id_registro,
                "noCondicao": f"{nome_base} - {grupo}",
                "deCondicao": f"{nome_base} {grupo} - {nu_ano_mes}",
                "noCampoCondicao": "icAtingido",
                "nuAnoMes": nu_ano_mes,
                "icExibido": False,
                "icObrigatorio": True,
                "vrRealizadoGlobal": None,
                "icProcessamentoValor": tipo_condicao in (1, 3, 6),
                "idTipoCondicao": tipo_condicao,
            }
        )

    return lista


def _build_attr_niveis(lista_retornos: list):
    lista = []

    for i, retorno in enumerate(lista_retornos, start=1):
        de_retorno = retorno.get("deRetorno", "")
        vr_objetivo = retorno.get("vrObjetivoRetorno")
        nu_qtd_limite = retorno.get("nuQtdLimiteRetorno")

        lista.append(
            {
                "nuNivel": i,
                "deNivel": de_retorno,
                "vrNivel": vr_objetivo,
                "nuQtdLimite": nu_qtd_limite,
                "icObrigatorio": 1 if i == 1 else 0,
                "dhAtualizacao": datetime.now(),
                "deImgNivel": ask_link_nivel(i),
                "deRetorno": "",
            }
        )

    return lista
