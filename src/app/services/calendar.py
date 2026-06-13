from calendar import monthrange
from datetime import date, datetime, timedelta

from holidays import country_holidays

from app.commands.commands import ask_periodo_especifico


class CalendarioRegistro:
    def __init__(self, mes: int | None = None) -> None:
        self.ano_atual = datetime.now().year
        self.mes_atual = mes or datetime.now().month
        self.final_ano = date(self.ano_atual + 1, 12, 31)
        self.ultimo_dia_mes = monthrange(self.ano_atual, self.mes_atual)[1]
        self.feriados = country_holidays("BR", years=self.ano_atual)
        self.nu_ano_mes = int(date(self.ano_atual, self.mes_atual, 1).strftime("%Y%m"))
        self.data_fim_periodo_registro = date(
            self.ano_atual, self.mes_atual, self.ultimo_dia_mes
        )

    def dias_uteis(self, data_inicio: date) -> dict[int, date]:
        start = data_inicio or self.inicio_ano
        index_dia_util = 1
        calendario_de_dias_uteis = dict()
        while start <= self.final_ano:
            if start.weekday() < 5 and start not in self.feriados:
                calendario_de_dias_uteis[index_dia_util] = start
                index_dia_util += 1
            start += timedelta(days=1)
        return calendario_de_dias_uteis


class CalendarioEspecificoRegistro(CalendarioRegistro):
    def __init__(self, mes_selecionado: int) -> None:
        super().__init__(mes=mes_selecionado)


def selecionar_data():
    data_especificada = ask_periodo_especifico()

    if data_especificada:
        calendario = CalendarioEspecificoRegistro(data_especificada)
        periodo_registro_mes_especifico = calendario.data_fim_periodo_registro
        calendario_dias_uteis_mes_especifico = calendario.dias_uteis(
            periodo_registro_mes_especifico
        )
        fim_processamento = calendario_dias_uteis_mes_especifico[9]
        nu_ano_mes_especifico = calendario.nu_ano_mes
        return nu_ano_mes_especifico, fim_processamento

    calendario = CalendarioRegistro()
    periodo_registro = calendario.data_fim_periodo_registro
    calendario_dias_uteis = calendario.dias_uteis(periodo_registro)
    fim_processamento = calendario_dias_uteis[9]
    nu_ano_mes = calendario.nu_ano_mes

    return nu_ano_mes, fim_processamento
