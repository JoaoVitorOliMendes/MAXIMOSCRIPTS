# ------------------------------------------------------
# MaximoCon, 2022-05-20 14:44:58-0300
# Objetivo: Script to manipulate JM_WORKLOGGING app
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

from psdi.server import MXServer
from java.util import Calendar
from java.text import SimpleDateFormat

if launchPoint == "SAVE":
    validate()

    wEntryMboSet = mbo.getMboSet('$JM_WORKENTRY', 'JM_WORKENTRY', 'JM_WORKNUMBER = \'' + mbo.getString('JM_WORKNUMBER') + '\'')

    wEntryMbo = wEntryMboSet.moveFirst()
    sum = 0
    
    while wEntryMbo:
        sum += wEntryMbo.getFloat('JM_TOTACTUALHRS')
        wEntryMbo = wEntryMboSet.moveNext()
    service.error(str(sum), 'CanAddDelet')

def validate():
    laborCode = mbo.getString('JM_LABORCODE')
    weekNumber = mbo.getString('JM_WEEKNUMBER')
    
    if weekNumber and laborCode:
        #Where clause to get JM_WORKLOGGING with the same LABORCODE and WEEKNUMBER
        laborMboSet = mbo.getMboSet('$JM_WORKLOGGING', 'JM_WORKLOGGING', 'JM_LABORCODE = \'' + laborCode + '\' and JM_WEEKNUMBER = \'' + weekNumber + '\'')
        
        laborMbo = laborMboSet.moveFirst()
        
        if laborMbo:
            service.error('JM_WORKLOG', 'JM_WorkLogAlreadyExists')
        else:
            addDays()

def addDays():
    maxDate = mbo.getDate('JM_WEEKSTARTDATE')
            
    cal = Calendar.getInstance()
    dateFormat = SimpleDateFormat("MMM dd, YYYY");
            
    cal.setTime(maxDate)
            
    #Adding date to each JM_DAY field
    for i in range(1, 7):
        mbo.setValue('JM_DAY' + str(i), str(dateFormat.format(cal.getTime())))
        cal.add(Calendar.DATE, 1)
    #Sunday - Last day
    mbo.setValue('JM_DAY0', dateFormat.format(cal.getTime()))
