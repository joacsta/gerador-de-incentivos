from sqlalchemy import Engine
from core.domain.apuracao import Apuracao
from core.domain.models import Campanha, GrupoProduto


def apuracao_main(grupo_produto: GrupoProduto, campanha: Campanha, engine: Engine):
    apuracao = Apuracao(grupo_produto, campanha)
    selected_apuracao = apuracao.select_apuracao()

    query, params = apuracao.select_template(selected_apuracao)
    statement_apuracao = apuracao.create_statement(query, params)

    apuracao.create_apuracao(query, params)
    apuracao.execute(statement_apuracao, engine)
    return apuracao
