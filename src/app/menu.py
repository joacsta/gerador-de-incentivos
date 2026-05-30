from __future__ import annotations

from os import name
from subprocess import run
from time import sleep

from app.commands.commands import ask_boolean
from app.constants import PROD, STAGE, USER_OPTIONS
from app.services.apuracao import apuracao_main
from app.services.setup import execute_setup, setup_main
from infra.db.connection import servidor


def opcao_errada() -> None:
    print("Opção inválida.")
    sleep(1)


def sair() -> None:
    raise SystemExit(0)


def executa_apuracao() -> None:
    eng = servidor.database_connection
    setup_created = setup_main(eng)
    apuracao = apuracao_main(setup_created.grupo_produto, setup_created.campanha, eng)

    if servidor.server_name == STAGE:
        ask = ask_boolean(f"Deseja inserir esse mesmo programa em produção ({PROD})?")
        if ask:
            servidor.change_connection
            new_engine = servidor.database_connection

            setup_created.reset_pks
            execute_setup(setup_created, new_engine)

            apuracao.create_apuracao(apuracao.query, apuracao.params)
            apuracao.execute(apuracao.statement, new_engine)


def executa_setup() -> None:
    eng = servidor.database_connection
    setup_created = setup_main(eng)
    if servidor.server_name == STAGE:
        ask = ask_boolean(f"Deseja inserir estes mesmos dados em produção ({PROD})?")
        if ask:
            servidor.change_connection
            new_engine = servidor.database_connection

            setup_created.reset_pks
            execute_setup(setup_created, new_engine)


USER_CHOICES = {
    "1": executa_apuracao,
    "2": executa_setup,
    "apuração": executa_apuracao,
    "setup": executa_setup,
    "q": sair,
}


def menu() -> None:
    while True:
        run("cls" if name == "nt" else "clear", shell=True, check=False)

        print("GERADOR DE PROGRAMAS DE INCENTIVO")
        print(*USER_OPTIONS, sep="\n")
        input_user = input("Selecione o que deseja fazer: ")

        USER_CHOICES.get(input_user.strip().lower(), opcao_errada)()
        return
