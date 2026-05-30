from sqlalchemy import Engine

from app.commands.commands import ask_parametros_setup
from core.domain.models import Campanha, Gatilho, GatilhosNivel, GrupoProduto, Premiacao
from core.domain.setup import Setup
from infra.db.connection import servidor


def call_setup():
    print(f"\nServidor Atual: {servidor.server_name}")

    quantidade_premiacoes, quantidade_gatilhos = ask_parametros_setup()

    campanha = Campanha()
    grupo_produto = GrupoProduto()
    premiacao = (
        Premiacao(campanha.nu_ano_mes_inicio, quantidade_premiacoes)
        if quantidade_premiacoes
        else Premiacao(campanha.nu_ano_mes_inicio)
    )
    gatilhos = Gatilho(
        grupo_produto.values, campanha.nu_ano_mes_inicio, quantidade_gatilhos
    )
    gatilhos_nivel = GatilhosNivel(premiacao.values)

    new_setup = Setup(campanha, grupo_produto, premiacao, gatilhos, gatilhos_nivel)
    return new_setup


def execute_setup(new_setup: Setup, eng: Engine):
    if not new_setup.preview:
        raise ValueError("Preview cancelado pelo usuário.")
    new_setup.insert_data(eng)
    return new_setup


def setup_main(engine: Engine):
    created_setup = call_setup()
    execute_setup(created_setup, engine)

    print(f"Dados inseridos no servidor: {servidor.server_name}")

    return created_setup
