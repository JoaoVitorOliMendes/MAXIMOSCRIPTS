# ------------------------------------------------------
# MaximoCon, 2022-05-23 15:02:47-0300
# Objetivo: Script to manipulate JM_WORKENTRY, register hours and log remarks
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

from psdi.server import MXServer
from java.util import Calendar
from java.text import SimpleDateFormat

def setAllDaysStatus(status):
    for i in range(7):
        if mbo.getFloat('JM_ACTUAL' + str(i)) != 0:
            if status == 'CANCELLED':
                mbo.setValue('JM_WORKSTATUS' + str(i), 'CANCELLED', mbo.NOACCESSCHECK)
                mbo.setValue('JM_ACTUAL' + str(i), 0, mbo.NOACCESSCHECK|mbo.NOACTION)
            elif mbo.getString('JM_WORKSTATUS' + str(i)) != 'APPROVED':
                mbo.setValue('JM_WORKSTATUS' + str(i), status, mbo.NOACCESSCHECK)
        else:
            mbo.setValue('JM_WORKSTATUS' + str(i), 'CANCELLED', mbo.NOACCESSCHECK)

def checkStatus(number):
    if mbo.getFloat('JM_ACTUAL' + str(number)) != 0:
        mbo.setValue('JM_WORKSTATUS' + str(number), 'IN PROGRESS', mbo.NOACCESSCHECK)
    else:
        mbo.setValue('JM_WORKSTATUS' + str(number), 'CANCELLED', mbo.NOACCESSCHECK)

def validateStatus():
    if mbo.getString('JM_WORKSTATUS') == 'SUBMITTED':
        for i in range(7):
            if mbo.getFloat('JM_ACTUAL' + str(i)) == 0:
                mbo.setValue('JM_WORKSTATUS' + str(i), 'CANCELLED', mbo.NOACCESSCHECK)
            if mbo.getString('JM_WORKSTATUS' + str(i)) not in ('CANCELLED', 'SUBMITTED'):
                service.error('JM_WORKLOG', 'JM_CannotApproveRow')
    elif mbo.getString('JM_WORKSTATUS') == 'CANCELLED':
        for i in range(7):
            if mbo.getString('JM_WORKSTATUS' + str(i)) == 'SUBMITTED':
                service.error('JM_WORKLOG', 'JM_CannotCancelApprovedRow')
    for i in range(7):
        if mbo.getString('JM_WORKSTATUS' + str(i)) == 'SUBMITTED':
            if mbo.getFloat('JM_ACTUAL' + str(i)) == 0:
                service.error('JM_WORKLOG', 'JM_CannotSubmitZeroHours')

def addHours():
    wEntryMboSet = mbo.getMboSet('JM_WORKENTRY')
    wLogMboSet = mbo.getMboSet('JM_WORKLOGGING')
    
    if wEntryMboSet:
        totalSum = 0
        for i in range(7):
            wEntryMbo = wEntryMboSet.moveFirst()
            wLogMbo = wLogMboSet.moveFirst()
            sum = 0
        
            while wEntryMbo:
                sum += wEntryMbo.getFloat('JM_ACTUAL' + str(i))
                wEntryMbo = wEntryMboSet.moveNext()
            
            wLogMbo.setValue('JM_TOTAL' + str(i), sum,  mbo.NOACCESSCHECK)
            totalSum += sum
        wLogMbo.setValue('JM_TOTACTUALHRS', totalSum,  mbo.NOACCESSCHECK)
        wLogMboSet.save()

def addEntryHours():
    sum = 0
    
    for i in range(7):
        sum += mbo.getFloat('JM_ACTUAL' + str(i))
        
    mbo.setValue('JM_TOTACTUALHRS', sum, mbo.NOACCESSCHECK)
    
    #Converting decimal to minutes - 0.50 = 30 min
    #   *Not necessary since maximo duration type already converts it back
    #minutesString = sum - int(sum)
    #minutes = str(int(round(minutesString * 60)))
    
    #hours = str(int(sum))
    #finalString = hours + ':' + minutes
    #mbo.setValue('JM_TOTACTUALHRS', finalString, mbo.NOACCESSCHECK)

def setEntryVisibility():
    if mbo.getString('JM_WORKSTATUS') == 'APPROVED':
        mbo.setFlag(mbo.READONLY, True)
    else:
        for i in range(7):
            if mbo.getString('JM_WORKSTATUS' + str(i)) == 'APPROVED':
                mbo.setFieldFlag('JM_ACTUAL' + str(i), mbo.READONLY, True)
                mbo.setFieldFlag('JM_WORKLOCATION' + str(i), mbo.READONLY, True)
                mbo.setFieldFlag('JM_REMARKSTS' + str(i), mbo.READONLY, True)
                mbo.setFieldFlag('JM_COMMENTS' + str(i), mbo.READONLY, True)
                mbo.setFieldFlag('JM_WORKSTATUS' + str(i), mbo.READONLY, True)

def submitWorkEntry(fieldNumber):
    condition = mbo.getString('JM_WORKSTATUS' + str(fieldNumber)) == 'SUBMITTED'
    mbo.setFieldFlag('JM_ACTUAL' + str(fieldNumber), mbo.REQUIRED, condition)
    mbo.setFieldFlag('JM_WORKLOCATION' + str(fieldNumber), mbo.REQUIRED, condition)
    mbo.setFieldFlag('JM_REMARKSTS' + str(fieldNumber), mbo.REQUIRED, condition)
    mbo.setFieldFlag('JM_WORKSTATUS' + str(fieldNumber), mbo.REQUIRED, condition)

def submitDayToLabTrans():
    laborMboSet = MXServer.getMXServer().getMboSet('LABTRANS', mbo.getUserInfo())
    wLogMboSet = mbo.getMboSet('JM_WORKLOGGING')
    wLogMbo = wLogMboSet.moveFirst()
    parser = SimpleDateFormat('MMM dd, YYYY')
    formater = SimpleDateFormat('YYYY-MM-DD')
    
    for i in range(7):
        laborMboSet.setWhere(
            'STARTDATE = \'' + formater.format(parser.parse(wLogMbo.getString('JM_DAY' + str(i)))) + '\''
            + ' and LABORCODE = \'' + wLogMbo.getString('JM_LABORCODE') + '\''
            + ' and WONUM = \'' + mbo.getString('JM_WONUM') + '\''
        )
        laborMboSet.reset()
        
        service.error(str(laborMboSet.count()), '')
        laborMbo = laborMboSet.add()
        laborMbo.setValue('ORGID', mbo.getString('ORGID'), mbo.NOACCESSCHECK)
        laborMbo.setValue('SITEID', mbo.getString('SITEID'), mbo.NOACCESSCHECK)
        laborMbo.setValue('JM_FROMWORKLOGGING', 1, mbo.NOACCESSCHECK)
        laborMbo.setValue('LABORCODE', wLogMbo.getString('JM_LABORCODE'), mbo.NOACCESSCHECK)
        laborMbo.setValue('REGULARHRS', mbo.getString('JM_ACTUAL' + str(i)), mbo.NOACCESSCHECK)
        laborMbo.setValue('STARTDATE', wLogMbo.getString('JM_DAY' + str(i)), mbo.NOACCESSCHECK)
        laborMbo.setValue('WONUM', mbo.getString('JM_WONUM'), mbo.NOACCESSCHECK)
        laborMbo.setValue('TRANSTYPE','WORK',mbo.NOACCESSCHECK)

    laborMboSet.save()

#Init lp
if launchPoint == 'INIT':
    if onadd:
        for i in range(7):
            mbo.setValue('JM_ACTUAL' + str(i), 0,  mbo.NOACCESSCHECK|mbo.NOVALIDATION|mbo.NOACTION)
        mbo.setValue('JM_WORKNUMBER', mbo.getOwner().getString('JM_WORKNUMBER'), mbo.NOACCESSCHECK)
    setEntryVisibility()

#Save lp - add, update | before save
if launchPoint == 'SAVE':
    addEntryHours()
    validateStatus()
    #submitDayToLabTrans()

#AftSave lp - add, update, delete | after save
if launchPoint == 'AFTSAVE':
    addHours()
    
if launchPoint == 'ALLOWOBJCREATION':
    if mboset.getOwner().toBeAdded():
        service.error('JM_WORKLOG', 'JM_NeedToSave')

if launchPoint == 'ALLOWDELETE':
    for i in range(7):
        if mbo.getString('JM_WORKSTATUS' + str(i)) == 'SUBMITTED':
            service.error('JM_WORKLOG', 'JM_CannotDeleteRow')

if launchPoint == 'JM_WORKSTATUS0':
    submitWorkEntry(0)
elif launchPoint == 'JM_WORKSTATUS1':
    submitWorkEntry(1)
elif launchPoint == 'JM_WORKSTATUS2':
    submitWorkEntry(2)
elif launchPoint == 'JM_WORKSTATUS3':
    submitWorkEntry(3)
elif launchPoint == 'JM_WORKSTATUS4':
    submitWorkEntry(4)
elif launchPoint == 'JM_WORKSTATUS5':
    submitWorkEntry(5)
elif launchPoint == 'JM_WORKSTATUS6':
    submitWorkEntry(6)
elif launchPoint == 'JM_WORKSTATUS':
    setAllDaysStatus(str(mbovalue))

if launchPoint == 'JM_ACTUAL0':
    checkStatus(0)
elif launchPoint == 'JM_ACTUAL1':
    checkStatus(1)
elif launchPoint == 'JM_ACTUAL2':
    checkStatus(2)
elif launchPoint == 'JM_ACTUAL3':
    checkStatus(3)
elif launchPoint == 'JM_ACTUAL4':
    checkStatus(4)
elif launchPoint == 'JM_ACTUAL5':
    checkStatus(5)
elif launchPoint == 'JM_ACTUAL6':
    checkStatus(6)
