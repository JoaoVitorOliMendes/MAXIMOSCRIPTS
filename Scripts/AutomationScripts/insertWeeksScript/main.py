import time
import pymssql
from datetime import date, timedelta

conn = pymssql.connect('maximocon.asuscomm.com:31433','maximo','maximocon','maxdb761EN')
cursor = conn.cursor(as_dict=True)

year = input("Digite o ano a ser inserido: ")

firstDay = date(int(year), 1, 1)

if firstDay.weekday() != 0:
    firstDay = firstDay + timedelta(days=7-firstDay.weekday())

for i in range(52):
    weekStart = firstDay
    weekEnd = firstDay + timedelta(days=6)

    executeQ = str(f"insert into WEEKS (WEEK_START, WEEK_END, WEEK, ORGID, SITEID, HASLD, WEEKSID) VALUES ('{weekStart}', '{weekEnd}', 'Week {i} - {year}', 'EAGLENA', 'BEDFORD', 0, {i})")
    cursor.execute(executeQ)
    conn.commit()

    firstDay = firstDay + timedelta(days=7)

conn.close()
