# ------------------------------------------------------
# MaximoCon, 2022-05-20 14:44:58-0300
# Objetivo: Script to manipulate JM_WORKLOGGING app, relate labors and add workentrys
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

from java.util import Calendar
from java.text import SimpleDateFormat
from psdi.server import MXServer

def setAllEntriesStatus(status):
    wEntryMboSet = mbo.getMboSet('JM_WORKENTRY')
    wEntryMbo = wEntryMboSet.moveFirst()
    while wEntryMbo:
        if wEntryMboSet.getString('JM_WORKSTATUS') != 'APPROVED':
            wEntryMboSet.setValue('JM_WORKSTATUS', status, mbo.NOACCESSCHECK)
        wEntryMbo = wEntryMboSet.moveNext()
    #wEntryMboSet.save()

def validateLaborcodeWeeknumber():
    laborCode = mbo.getString('JM_LABORCODE')
    weekNumber = mbo.getString('JM_WEEKNUMBER')
    workNumber = mbo.getString('JM_WORKNUMBER')

    if weekNumber and laborCode:
        #Where clause to get JM_WORKLOGGING with the same LABORCODE and WEEKNUMBER
        laborMboSet = mbo.getMboSet(
            '$JM_WORKLOGGING',
            'JM_WORKLOGGING',
            'JM_LABORCODE = \'' + laborCode
            + '\' and JM_WEEKNUMBER = \'' + weekNumber
            + '\' and JM_WORKNUMBER <> \'' + workNumber + '\'')

        laborMbo = laborMboSet.moveFirst()

        if laborMbo:
            service.error('JM_WORKLOG', 'JM_WorkLogAlreadyExists')
        else:
            defineDays()

def defineDays():
    maxDate = mbo.getDate('JM_WEEKSTARTDATE')

    cal = Calendar.getInstance()
    dateFormat = SimpleDateFormat("MMM dd, YYYY");

    cal.setTime(maxDate)

    #Adding date to each JM_DAY field
    for i in range(1, 7):
        mbo.setValue('JM_DAY' + str(i), str(dateFormat.format(cal.getTime())))
        cal.add(Calendar.DATE, 1)
    #Sunday - Start at next week
    mbo.setValue('JM_DAY0', dateFormat.format(cal.getTime()))

def validateFutureDate():
    maxDate = mbo.getDate('JM_WEEKSTARTDATE')
    cal = Calendar.getInstance()
    
    cal.setTime(maxDate)
    
    today = MXServer.getMXServer().getDate();
    
    if today.getTime() < cal.getTime().getTime():
        service.error('JM_WORKLOG', 'JM_FutureDate')

def validateEntryStatusBeforeSubmit():
    wEntryMboSet = mbo.getMboSet('JM_WORKENTRY')
    wEntryMbo = wEntryMboSet.moveFirst()
    if mbo.getString('JM_STATUS') == 'SUBMITTED':
        while wEntryMbo:
            if wEntryMbo.getString('JM_WORKSTATUS') not in ('SUBMITTED', 'CANCELLED'):
                service.error('JM_WORKLOG', 'JM_NeedSubmitt')
            wEntryMbo = wEntryMboSet.moveNext()

#Save lp - add, update | before save
if launchPoint == 'SAVE':
    if onadd:
        validateLaborcodeWeeknumber()
    validateFutureDate()
    validateEntryStatusBeforeSubmit()

#Init lp
if launchPoint == 'INIT':
    if onadd:
        #Set laborcode as users laborcode
        laborMboSet = mbo.getMboSet('$LABOR', 'LABOR', 'PERSONID = \'' + mbo.getUserName() + '\'')
        laborMbo = laborMboSet.moveFirst()
        if laborMbo and laborMbo.getString('LABORCODE'):
            labor = laborMbo.getString('LABORCODE')
            mbo.setValue('JM_LABORCODE',labor, mbo.NOACCESSCHECK)
        else:
            #If user does not have a labor code associated display error
            service.error('JM_WORKLOG', 'JM_UserHasNoLabor')
    else:
        mbo.setFieldFlag('JM_WEEKNUMBER',mbo.READONLY, True)
        mbo.setFieldFlag('JM_LABORCODE',mbo.READONLY, True)

if launchPoint == 'JM_STATUS':
    setAllEntriesStatus(str(mbovalue))
