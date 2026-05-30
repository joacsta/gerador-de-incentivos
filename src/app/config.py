from argparse import ArgumentParser

from app.constants import PROD, STAGE


def argument():
    parser = ArgumentParser(description="Conexão com banco de dados (exemplo)")
    parser.add_argument(
        "-p",
        "--prod",
        action="store_const",
        const=PROD,
        default=STAGE,
        help="escolha do servidor: prod (stage definido por padrão)",
        required=False,
    )

    args = parser.parse_args()
    server = args.prod
    database = "DEMO"
    return server, database
