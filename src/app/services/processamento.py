from sqlalchemy import Engine

from core.domain.models import Categoria, Condicao, CondicaoNivel, Registro
from core.domain.processamento import Processamento


def processamento_main(
    categoria_vinculada: Categoria,
    registro_principal: Registro,
    condicoes: Condicao,
    condicoes_niveis: CondicaoNivel,
    motor: Engine,
):
    processamento = Processamento(
        categoria_vinculada, registro_principal, condicoes, condicoes_niveis
    )
    processamento_selecionado = processamento.selecionar_processamento()

    query, parametros = processamento.selecionar_modelo(processamento_selecionado)
    declaracao_processamento = processamento.criar_declaracao(query, parametros)

    processamento.criar_registro(query, parametros)
    processamento.execute(declaracao_processamento, motor)

    return processamento
