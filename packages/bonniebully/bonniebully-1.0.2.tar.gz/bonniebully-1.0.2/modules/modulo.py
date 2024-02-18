# -*- coding: latin-1 -*-
from datetime import date, datetime
import calendar
import holidays
from dateutil.relativedelta import relativedelta


class bonniebully():
    """Pacote para manipulação de datas. - bonniebully

    - Created By: Delvidio Demarchi Neto
    - Created Date: 03/04/2023
    - Laste Update: 17/02/2024
    - Version: '1.0.3'

    bonniebully(Interval, Date, Increment, Alignment)

    Atributos: 
        Interval (str): Intervalo do periodo de calculo (Year: ano, Month: Mês,
        Day: Dias, Bday: Dias Uteis.).
        Date (date ou str): Data de referência de calculo no formado
        yyyy-mm-dd.
        Increment: Incremento de calculo, número inteiro positivo ou negativo.
        Alignment: Alinhamento da data (B: Primeiro dia do mês,
        E: Ultimo dia do mês e S: Mesmo dia de referencia).

        Caso utilize dia Util:

        Country: Pais de deseja consultar o dia util
        State: Caso seja necessario localizar o estado
        Weekend: False Sabado não é dia util, True Sabado é dia util
    """

    def __init__(self, Interval: str, Date: date, Increment: int,
                 Alignment: str, County: str = "", State: str = "", Weekend: bool = False):

        self._Interval = Interval
        self._Increment = Increment
        self._Alignment = Alignment
        self._Contry = County
        self._State = State
        self._Weekend = Weekend
        self._EndDate = ''

        if isinstance(Date, str) is True:
            self._Date = datetime.strptime(Date, '%Y-%m-%d')
        else:
            self._Date = datetime.combine(Date, datetime.min.time())

    def getDates(self) -> date:
        """ getDates: Método que retorna o dia no formato YYYY-MM-DD """

        vDayClass = self._Date.day

        def __getAlignment(vYearMeth: int, vMonthMeth: int, vDayMeth: int):

            if self._Alignment.upper() == "B":
                vDateMeth = date(vYearMeth, vMonthMeth, 1)

            elif self._Alignment.upper() == "S":
                vDateMeth = date(vYearMeth, vMonthMeth, vDayMeth)

            elif self._Alignment.upper() == "E":
                endOfMonth = calendar.monthrange(vYearMeth, vMonthMeth)
                vDateMeth = date(vYearMeth, vMonthMeth, endOfMonth[1])
            return vDateMeth

        def __checkNegative(value: int):
            if value < 0:
                check = True
            else:
                check = False
            return check

        def __getYear():

            vInterYear = self._Date + relativedelta(years=self._Increment)
            vGetDate = __getAlignment(
                vInterYear.year, vInterYear.month, vDayClass)
            vInterDate = date(vGetDate.year, vGetDate.month, vGetDate.day)

            return vInterDate

        def __getMonth():

            vInterMonth = self._Date + relativedelta(months=self._Increment)
            vGetDate = __getAlignment(
                vInterMonth.year, vInterMonth.month, vDayClass)
            vInterDate = date(vGetDate.year, vGetDate.month, vGetDate.day)
            return vInterDate

        def __getDay(Increment: int):
            vInterDay = self._Date + relativedelta(days=Increment)

            vGetDate = __getAlignment(
                vInterDay.year, vInterDay.month, vInterDay.day)
            vInterDate = date(vGetDate.year, vGetDate.month, vGetDate.day)
            return vInterDate

        def __getBDay(vDate: date, vContry: str, vState: str):

            vHoliday = holidays.country_holidays(
                vContry, subdiv=vState).get(vDate)

            if vHoliday is not None or (self._Weekend is False and vDate.weekday() > 5):
                vBday = 1
            elif vHoliday is not None or (self._Weekend is True and vDate.weekday() == 6):
                vBday = 1
            else:
                vBday = 0

            return vBday

        if self._Interval.upper() == "YEAR":
            vInterDate = __getYear()

        elif self._Interval.upper() == "MONTH":
            vInterDate = __getMonth()

        elif self._Interval.upper() == "DAY":
            vInterDate = __getDay(self._Increment)

        elif self._Interval.upper() == "BDAY":

            checkNegativeIncrement = __checkNegative(self._Increment)
            Increment = self._Increment
            rBday = 1
            vBusinessDay = None

            while rBday != 0:

                vDate = __getDay(Increment)
                rBday = __getBDay(vDate, self._Contry, self._State)

                if checkNegativeIncrement is True:
                    Increment -= 1
                else:
                    Increment += 1

                vBusinessDay = vDate

            vInterDate = vBusinessDay

        return vInterDate

    def getYearMonth(self) -> int:
        """ getAnoMes: Método que trás o ano mês """

        vData = self.getDates()
        getYearMonth = int(vData.strftime("%Y%m"))

        return int(getYearMonth)
