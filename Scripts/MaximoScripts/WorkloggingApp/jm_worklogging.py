# ------------------------------------------------------
# MaximoCon, 2022-05-20 14:44:58-0300
# Objetivo: Script to manipulate JM_WORKLOGGING app
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

from java.util import Calendar
from java.text import SimpleDateFormat

if launchPoint == "SAVE":
    cal = Calendar.getInstance()
    dateFormat = SimpleDateFormat("MMM dd, YYYY");
    maxDate = mbo.getDate('JM_WEEKSTARTDATE')
    
    cal.setTime(maxDate)
    
    cal.add(Calendar.DATE, -1)
    for i in range(6):
        mbo.setValue('JM_DAY' + str(i), dateFormat.format(cal.getTime()))
        cal.add(Calendar.DATE, 1)
    #service.error(, "CanEditCancel")
