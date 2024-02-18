# Bonnie Bully

This package was developed to simplify date manipulation.

How to use?

### Importing the packages and creating the current day variable for manipulation.
###### (Importando os pacotes e criando a variavem de dia atual para manipulação.)

```
import bonniebully as bb
from datetime import date 

current_day = date.today()
print('Current day:', current_day)

```

### One month ahead of the current date with the start date of the month
###### (Um mês a frente da data atual com a data inicial do mês)

```
M1 = bb('MONTH', current_day, 1,'B').getDates()
M1_yearMonth = bb('MONTH',current_day, 1,'B').getYearMonth()

print('M1_dia:', M1)
print('M1_yearMonth:', M1_yearMonth)
```

### Same day 12 months previous to current date
###### Mesmo dia 12 meses anteriores a data atual

```
M12 = bb('MONTH', current_day, -12,'S').getDates()
M12_yearMonth = bb('MONTH',current_day, -12,'S').getyearMonth()

print('M1_dia:', M1)
print('M1_yearMonth:', M1_yearMonth)
```

### 2 years previous to the current date with the last day of the month
###### 2 anos anterior da data atual com o ultimo dia do mês

```
Y2 = bb('YEAR', current_day, -2,'E').getDates()
Y2_yearMonth = bb('YEAR',current_day, -2,'E').getyearMonth()

```
