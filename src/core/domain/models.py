from __future__ import annotations

from datetime import datetime

from app.commands.commands import (
    ask_descricao,
    ask_nome_campanha,
    ask_produto,
    ask_rede,
    ask_tipo_campanha,
    ask_tipo_gatilho,
    ask_tipo_premiacao,
    ask_tipo_produtos,
    ask_url_faixa,
    ask_valor_decimal,
    ask_valor_inteiro,
)
from app.constants import (
    EMPRESA_PRODUTO,
    REDES,
    TIPO_CAMPANHA,
    TIPO_GATILHOS,
    TIPO_PREMIACOES,
)
from app.services.calendar import seleciona_data


class Campanha:
    def __init__(self) -> None:
        nu_ano_mes, data_fim_apuracao = seleciona_data()
        tipo_campanha = ask_tipo_campanha()
        tipo_participante = ask_rede()

        self.id_campanha = None
        self.nome_campanha = ask_nome_campanha()
        self.descricao = ask_descricao()
        self.nu_ano_mes_inicio = nu_ano_mes
        self.nu_ano_mes_fim = nu_ano_mes
        self.url_banner = ""
        self.url_card = ""
        self.tipo_campanha = int(TIPO_CAMPANHA[tipo_campanha])
        self.dt_apuracao = data_fim_apuracao
        self.tipo_participante = int(REDES[tipo_participante])

    @property
    def values(self) -> dict:
        return {
            "noCampanha": self.nome_campanha,
            "deCampanha": self.descricao,
            "nuAnoMesInicio": self.nu_ano_mes_inicio,
            "nuAnoMesFim": self.nu_ano_mes_fim,
            "deImagemCampanha": self.url_banner,
            "deLogoCampanha": "",
            "deBackgroundCampanha": self.url_card,
            "dhCriacao": datetime.now(),
            "dhAlteracao": datetime.now(),
            "idSituacaoCampanha": 1,
            "idTipoCampanha": self.tipo_campanha,
            "icApuracaoMensal": 1,
            "dtFimApuracao": self.dt_apuracao,
            "idTipoParticipante": self.tipo_participante,
            "icEmAtualizacao": 0,
        }


class GrupoProduto:
    def __init__(self) -> None:
        nome_grupo_produto = ask_produto()
        tipo_produto = ask_tipo_produtos()

        self.id_grupo_produto = None
        self.id_campanha = None
        self.nome_grupo_produto = nome_grupo_produto
        self.tipo_produto = tipo_produto
        self.empresa_id = EMPRESA_PRODUTO[nome_grupo_produto]

    @property
    def values(self) -> dict:
        return {
            "idCampanha": self.id_campanha,
            "noGrupoProduto": self.nome_grupo_produto,
            "idTipoProduto": self.tipo_produto,
            "deIcone": "",
            "deCor": "",
            "idEmpresa": self.empresa_id,
            "idTipoApuracao": 1,
            "nuOrdemApresentacao": 0,
        }


class Premiacao:
    def __init__(self, nu_ano_mes: int, quantidade_premiacoes: int = 1) -> None:
        self.id_campanha = None
        self.id_grupo_produto = None
        self.lista_premiacoes = []
        for premiacao in range(quantidade_premiacoes):
            print(f"{premiacao + 1}ª recompensa: ")
            tipo_premiacao = ask_tipo_premiacao()
            id_tipo_premiacao = int(TIPO_PREMIACOES[tipo_premiacao])
            vr_premiacao = ask_valor_decimal(
                f"Insira o valor da {premiacao + 1}ª recompensa (somente números):"
            )
            descricao_premiacao = input(
                f"Insira o nome da {premiacao + 1}ª recompensa: "
            )
            vr_objetivo_premiacao = ask_valor_decimal(
                f"Insira o valor do objetivo da {premiacao + 1}ª recompensa:"
            )
            nu_qtd_limite_premiacao = ask_valor_inteiro(
                f"Insira quantas unidades a {premiacao + 1}ª recompensa possui:"
            )
            coluna_premiacao = {
                "dePremiacao": descricao_premiacao,
                "nuAnoMes": nu_ano_mes,
                "noTipoUnidade": None,
                "noTipoRede": None,
                "nuPorteUnidade": None,
                "vrPremiacao": vr_premiacao,
                "vrObjetivoPremiacao": vr_objetivo_premiacao,
                "idTipoPremiacao": id_tipo_premiacao,
                "nuQtdLimitePremiacao": nu_qtd_limite_premiacao,
                "deImgPremiacao": "",
                "idCampanha": self.id_campanha,
                "idGrupoProdutoCampanha": self.id_grupo_produto,
            }
            self.lista_premiacoes.append(coluna_premiacao)

    def set_id_grupo_produto(self, id_grupo_produto: int) -> None:
        self.id_grupo_produto = id_grupo_produto
        for premiacao in self.lista_premiacoes:
            premiacao["idGrupoProdutoCampanha"] = id_grupo_produto

    def reset_id_campanha(self) -> None:
        for premiacao in self.lista_premiacoes:
            premiacao["idCampanha"] = None

    def reset_id_grupo_produto(self) -> None:
        for premiacao in self.lista_premiacoes:
            premiacao["idGrupoProdutoCampanha"] = None

    def set_id_campanha(self, id_campanha: int) -> None:
        self.id_campanha = id_campanha
        for premiacao in self.lista_premiacoes:
            premiacao["idCampanha"] = id_campanha

    @property
    def values(self) -> list[dict]:
        return self.lista_premiacoes


class Gatilho:
    def __init__(
        self,
        dicionario_grupo_produto: dict,
        nu_ano_mes: int,
        quantidade_gatilhos: int = 1,
    ) -> None:
        self.lista_gatilhos = []
        self.id_campanha = None
        self.nome_produto = dicionario_grupo_produto["noGrupoProduto"]
        for gatilhos in range(quantidade_gatilhos):
            print(f"{gatilhos + 1}ª meta:")
            tipo_gatilho = ask_tipo_gatilho()
            id_tipo_gatilho = int(TIPO_GATILHOS[tipo_gatilho])
            ic_apuracao_valor = True if id_tipo_gatilho in (1, 3, 6) else False
            coluna_gatilhos = (
                {
                    "idCampanha": self.id_campanha,
                    "noGatilho": f"Badges - {self.nome_produto}",
                    "deGatilho": f"Badges {self.nome_produto} - {nu_ano_mes}",
                    "noCampoGatilho": "icAtingido",
                    "nuAnoMes": nu_ano_mes,
                    "icExibido": False,
                    "icObrigatorio": True,
                    "vrRealizadoGlobal": None,
                    "icApuracaoValor": ic_apuracao_valor,
                    "idTipoGatilho": id_tipo_gatilho,
                }
                if id_tipo_gatilho == 6
                else {
                    "idCampanha": self.id_campanha,
                    "noGatilho": f"Meta - {self.nome_produto}",
                    "deGatilho": f"Meta {self.nome_produto} - {nu_ano_mes}",
                    "noCampoGatilho": "icAtingido",
                    "nuAnoMes": nu_ano_mes,
                    "icExibido": False,
                    "icObrigatorio": True,
                    "vrRealizadoGlobal": None,
                    "icApuracaoValor": ic_apuracao_valor,
                    "idTipoGatilho": id_tipo_gatilho,
                }
            )
            self.lista_gatilhos.append(coluna_gatilhos)

    def reset_id_campanha(self) -> None:
        for gatilho in self.lista_gatilhos:
            gatilho["idCampanha"] = None

    def set_id_campanha(self, id_campanha: int) -> None:
        self.id_campanha = id_campanha
        for gatilho in self.lista_gatilhos:
            gatilho["idCampanha"] = id_campanha

    @property
    def values(self) -> list[dict]:
        return self.lista_gatilhos


class GatilhosNivel:
    def __init__(self, lista_premiacoes: list[dict]):
        self.lista_gatilho_nivel = []
        self.id_gatilho: int | None = None

        for index_premiacao, premiacao in enumerate(lista_premiacoes, start=1):
            de_premiacao = premiacao.get("dePremiacao", "")
            vr_objetivo = premiacao.get("vrObjetivoPremiacao")
            nu_qtd_limite = premiacao.get("nuQtdLimitePremiacao")
            gatilho_nivel = {
                "nuNivel": index_premiacao,
                "deNivel": de_premiacao,
                "vrNivel": vr_objetivo,
                "nuQtdLimite": nu_qtd_limite,
                "icObrigatorio": 1 if index_premiacao == 1 else 0,
                "dhAtualizacao": datetime.now(),
                "deImgPremiacao": ask_url_faixa(index_premiacao),
                "dePremiacao": "",
            }
            self.lista_gatilho_nivel.append(gatilho_nivel)

    def reset_id_gatilho(self, index: int) -> None:
        self.lista_gatilho_nivel[index]["idGatilho"] = None

    def set_id_gatilho(self, index: int, id_gatilho: int | None) -> None:
        self.lista_gatilho_nivel[index]["idGatilho"] = id_gatilho

    @property
    def values(self) -> list[dict]:
        return self.lista_gatilho_nivel
