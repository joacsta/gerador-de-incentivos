from datetime import date, datetime, timedelta
from holidays import country_holidays
from calendar import monthrange

from app.commands.commands import ask_data_especifica


class CalendarioCampanha:
    def __init__(self, mes: int | None = None) -> None:
        self.ano_atual = datetime.now().year
        self.mes_atual = mes or datetime.now().month
        self.final_ano = date(self.ano_atual + 1, 12, 31)
        self.ultimo_dia_mes = monthrange(self.ano_atual, self.mes_atual)[1]
        self.feriados = country_holidays("BR", years=self.ano_atual)
        self.nu_ano_mes = int(date(self.ano_atual, self.mes_atual, 1).strftime("%Y%m"))
        self.data_fim_periodo_campanha = date(
            self.ano_atual, self.mes_atual, self.ultimo_dia_mes
        )

    def dias_uteis(self, start_date: date) -> dict[int, date]:
        start = start_date or self.inicio_ano
        index_dia_util = 1
        calendario_de_dias_uteis = dict()
        while start <= self.final_ano:
            if start.weekday() < 5 and start not in self.feriados:
                calendario_de_dias_uteis[index_dia_util] = start
                index_dia_util += 1
            start += timedelta(days=1)
        return calendario_de_dias_uteis


class CalendarioEspecificoCampanha(CalendarioCampanha):
    def __init__(self, mes_selecionado: int) -> None:
        super().__init__(mes=mes_selecionado)


def seleciona_data():
    data_especificada = ask_data_especifica()

    if data_especificada:
        calendario = CalendarioEspecificoPrograma(data_especificada)
        periodo_campanha_mes_especifico = calendario.data_fim_periodo_campanha
        calendario_dias_uteis_mes_especifico = calendario.dias_uteis(
            periodo_campanha_mes_especifico
        )
        fim_apuracao = calendario_dias_uteis_mes_especifico[9]
        nu_ano_mes_especifico = calendario.nu_ano_mes
        return nu_ano_mes_especifico, fim_apuracao
    calendario = CalendarioPrograma()
    periodo_campanha = calendario.data_fim_periodo_campanha
    calendario_dias_uteis = calendario.dias_uteis(periodo_campanha)
    fim_apuracao = calendario_dias_uteis[9]
    nu_ano_mes = calendario.nu_ano_mes
    return nu_ano_mes, fim_apuracao
