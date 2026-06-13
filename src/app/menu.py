from __future__ import annotations

from os import name
from subprocess import run
from time import sleep

import questionary

from app.commands.commands import ask_booleano
from app.config import AMBIENTE_PRINCIPAL, AMBIENTE_TESTE
from app.constants import OPCOES_USUARIO
from app.services.configuracao import configuracao_main, executar_configuracao
from app.services.processamento import processamento_main
from infra.db.conn import servidor


def opcao_invalida() -> None:
    print("Opção inválida.")
    sleep(1)


def sair() -> None:
    print("\nAté logo.")
    raise SystemExit(0)


def fluxo_processamento() -> None:
    motor = servidor.conectar()
    configuracao_criada = configuracao_main(motor)
    processamento = processamento_main(
        configuracao_criada.categoria_vinculada,
        configuracao_criada.registro_principal,
        configuracao_criada.condicoes,
        configuracao_criada.condicoes_nivel,
        motor,
    )

    if servidor.nome_servidor == AMBIENTE_TESTE:
        replicar = ask_booleano(
            f"Deseja inserir este mesmo registro no ambiente principal ({AMBIENTE_PRINCIPAL})?"
        )
        if replicar:
            servidor.alterar_conexao
            novo_motor = servidor.conectar()

            configuracao_criada.reset_pks()
            executar_configuracao(configuracao_criada, novo_motor)

            nova_query, novos_parametros = processamento.selecionar_modelo(
                processamento.processamento_selecionado
            )
            declaracao = processamento.criar_declaracao(nova_query, novos_parametros)

            processamento.criar_registro(nova_query, novos_parametros)
            processamento.execute(declaracao, novo_motor)


def fluxo_configuracao() -> None:
    motor = servidor.conectar()
    configuracao_criada = configuracao_main(motor)

    if servidor.nome_servidor == AMBIENTE_TESTE:
        replicar = ask_booleano(
            f"Deseja inserir estes mesmos dados no ambiente principal ({AMBIENTE_PRINCIPAL})?"
        )
        if replicar:
            servidor.alterar_conexao
            novo_motor = servidor.conectar()

            configuracao_criada.reset_pks()
            executar_configuracao(configuracao_criada, novo_motor)


OPCOES_SELECAO = {
    "1": fluxo_processamento,
    "2": fluxo_configuracao,
    "processamento": fluxo_processamento,
    "p": fluxo_processamento,
    "configuracao": fluxo_configuracao,
    "c": fluxo_configuracao,
    "q": sair,
    "exit": sair,
}


def menu() -> None:
    while True:
        run("cls" if name == "nt" else "clear", shell=True, check=False)

        questionary.print("SISTEMA GERADOR DE REGISTROS\n", style="bold")
        print(*OPCOES_USUARIO, sep="\n")
        pergunta = input("\nSelecione o que deseja fazer: ")

        OPCOES_SELECAO.get(pergunta.strip().lower(), lambda: opcao_invalida)()
