from argparse import ArgumentParser
from os import getenv

from dotenv import load_dotenv

load_dotenv()

AMBIENTE_PRINCIPAL = getenv("AMBIENTE_PRINCIPAL")
AMBIENTE_TESTE = getenv("AMBIENTE_TESTE")


def obter_argumentos():
    parser = ArgumentParser(description="Conexão com Fonte de Dados")
    parser.add_argument(
        "-p",
        "--principal",
        action="store_const",
        const=AMBIENTE_PRINCIPAL,
        default=AMBIENTE_TESTE,
        help="escolha do servidor: principal (teste definido por padrão)",
        required=False,
    )

    args = parser.parse_args()
    servidor = args.principal
    banco_dados = "SISTEMA_DB"
    return servidor, banco_dados
