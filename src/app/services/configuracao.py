import questionary
from sqlalchemy import Engine

from app.commands.commands import ask_parametros_inicializacao
from core.domain.configuracao import Configuracao
from core.domain.models import Categoria, Condicao, CondicaoNivel, Registro, Retorno
from infra.db.conn import servidor


def criar_configuracao():
    questionary.print(f"\nServidor Atual: {servidor.nome_servidor}", style="bold")

    registro = Registro.create()
    categoria = Categoria.create()

    quantidade_retornos, quantidade_condicoes = ask_parametros_inicializacao()

    retorno = (
        Retorno(registro.nu_ano_mes_inicio, quantidade_retornos)
        if quantidade_retornos
        else Retorno(registro.nu_ano_mes_inicio)
    )
    condicoes = Condicao(
        categoria.values(), registro.nu_ano_mes_inicio, quantidade_condicoes
    )
    condicoes_nivel = CondicaoNivel(retorno.values())

    retorno = retorno.build(registro.nu_ano_mes_inicio, quantidade_retornos)
    condicoes = condicoes.build(
        registro.nu_ano_mes_inicio, quantidade_condicoes, categoria.values()
    )
    condicoes_nivel = condicoes_nivel.build(retorno.values())

    nova_configuracao = Configuracao(
        registro, categoria, retorno, condicoes, condicoes_nivel
    )
    return nova_configuracao


def executar_configuracao(nova_configuracao: Configuracao, motor: Engine):
    if not nova_configuracao.preview:
        raise ValueError("Pré-visualização cancelada pelo usuário.")
    nova_configuracao.insert_data(motor)
    return nova_configuracao


def configuracao_main(motor: Engine):
    configuracao_criada = criar_configuracao()
    executar_configuracao(configuracao_criada, motor)
    print(f"Dados inseridos no servidor: {servidor.nome_servidor}")
    return configuracao_criada
