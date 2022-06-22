# ------------------------------------------------------
# MaximoCon, 2022-05-23 15:02:47-0300
# Objetivo: Script to manipulate JM_WORKENTRY, register hours and log remarks
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

from psdi.server import MXServer
from java.util import Calendar
from java.text import SimpleDateFormat
from java.lang import System

#Set week status based on all the days
def setWeekStatus():
    statusDict = {
        'CANCELLED': 0,
        'NOT STARTED': 0,
        'IN PROGRESS': 0,
        'SUBMITTED': 0,
        'APPROVED': 0
    }
    if mbo.getString('JM_WORKSTATUS') == 'APPROVED':
        return
    else:
        for i in range(7):
            if mbo.getString('JM_WORKSTATUS') != 'NOT STARTED':
                if mbo.getFloat('JM_ACTUAL' + str(i)) == 0:
                    mbo.setValue('JM_WORKSTATUS' + str(i), 'CANCELLED', mbo.NOACCESSCHECK)
                elif mbo.getString('JM_WORKSTATUS' + str(i)) == 'CANCELLED':
                    mbo.setValue('JM_ACTUAL' + str(i), 0, mbo.NOACCESSCHECK|mbo.NOACTION)
            statusDict[mbo.getString('JM_WORKSTATUS' + str(i))] += 1
    if statusDict['CANCELLED'] == 7:
        mbo.setValue('JM_WORKSTATUS', 'CANCELLED', mbo.NOACCESSCHECK)
    elif statusDict['NOT STARTED'] == 7:
        mbo.setValue('JM_WORKSTATUS', 'NOT STARTED', mbo.NOACCESSCHECK)
    elif statusDict['SUBMITTED'] == 7:
        mbo.setValue('JM_WORKSTATUS', 'SUBMITTED', mbo.NOACCESSCHECK)
    elif statusDict['APPROVED'] >= 2 and statusDict['APPROVED'] + statusDict['CANCELLED'] == 7:
        mbo.setValue('JM_WORKSTATUS', 'APPROVED', mbo.NOACCESSCHECK)
    elif statusDict['SUBMITTED'] + statusDict['APPROVED'] + statusDict['CANCELLED'] == 7:
        mbo.setValue('JM_WORKSTATUS', 'SUBMITTED', mbo.NOACCESSCHECK)
    else:
        mbo.setValue('JM_WORKSTATUS', 'IN PROGRESS', mbo.NOACCESSCHECK|mbo.NOVALIDATION)

#If day is submitted the fields become required
def submitWorkEntry(fieldNumber):
    mboValue = mbo.getMboValue('JM_WORKSTATUS' + str(fieldNumber))
    initialValue = mboValue.getInitialValue().asString()
    currentValue = mboValue.getCurrentValue().asString()
    
    if currentValue == 'APPROVED' and initialValue != 'SUBMITTED':
        service.error('JM_WORKLOG','JM_NeedSubmitBeforeApprove')
    elif currentValue == 'SUBMITTED':
        wLogMboSet = mbo.getMboSet('JM_WORKLOGGING')
        wLogMbo = wLogMboSet.moveFirst()
        if wLogMbo:
            parser = SimpleDateFormat('MMM dd, yyyy')
            dateFormat = parser.parse(wLogMbo.getString('JM_DAY' + str(fieldNumber)))
            cal = Calendar.getInstance()
            cal.setTime(dateFormat)
            today = MXServer.getMXServer().getDate()
            calToday = Calendar.getInstance()
            calToday.setTime(today)
        
            if calToday.getTime().getTime() < cal.getTime().getTime():
                service.error('JM_WORKLOG', 'JM_FutureDate', [wLogMbo.getString('JM_DAY' + str(fieldNumber))])
    
    condition = mbo.getString('JM_WORKSTATUS' + str(fieldNumber)) in ('SUBMITTED', 'APPROVED')
    mbo.setFieldFlag('JM_WORKLOCATION' + str(fieldNumber), mbo.REQUIRED, condition)
    mbo.setFieldFlag('JM_REMARKSTS' + str(fieldNumber), mbo.REQUIRED, condition)

#Set days status based on week status
def setAllDaysStatus(status):
    if status == 'APPROVED':
        for i in range(7):
            if mbo.getString('JM_WORKSTATUS' + str(i)) not in ('APPROVED', 'SUBMITTED', 'CANCELLED'):
                service.error('JM_WORKLOG', 'JM_CannotApproveRow')
    for i in range(7):
        if status == 'NOT STARTED':
            mbo.setValue('JM_WORKSTATUS' + str(i), 'NOT STARTED', mbo.NOACCESSCHECK|mbo.NOVALIDATION)
            mbo.setValue('JM_ACTUAL' + str(i), 0, mbo.NOACCESSCHECK|mbo.NOVALIDATION)
            submitWorkEntry(i)
        elif mbo.getFloat('JM_ACTUAL' + str(i)) != 0:
            if status == 'CANCELLED':
                mbo.setValue('JM_WORKSTATUS' + str(i), 'CANCELLED', mbo.NOACCESSCHECK|mbo.NOVALIDATION)
                mbo.setValue('JM_ACTUAL' + str(i), 0, mbo.NOACCESSCHECK|mbo.NOVALIDATION)
                #mbo.NOVALIDATION since there is an attribute lp on the field
            elif mbo.getString('JM_WORKSTATUS' + str(i)) != 'APPROVED':
                mbo.setValue('JM_WORKSTATUS' + str(i), status, mbo.NOACCESSCHECK|mbo.NOVALIDATION)
                submitWorkEntry(i)
        else:
            mbo.setValue('JM_WORKSTATUS' + str(i), 'CANCELLED', mbo.NOACCESSCHECK|mbo.NOVALIDATION)

#On changing the actual hours update the day status
def checkStatus(number):
    if mbo.getFloat('JM_ACTUAL' + str(number)) != 0 :
        if mbo.getString('JM_WORKSTATUS' + str(number)) in ('CANCELLED', 'NOT STARTED'):
            mbo.setValue('JM_WORKSTATUS' + str(number), 'IN PROGRESS', mbo.NOACCESSCHECK)
    elif mbo.getString('JM_WORKSTATUS' + str(number)) != 'NOT STARTED':
        mbo.setValue('JM_WORKSTATUS' + str(number), 'CANCELLED', mbo.NOACCESSCHECK)

#If entry is approved the fields become readonly
def setEntryVisibility():
    if mbo.getString('JM_WORKSTATUS') == 'APPROVED':
        mbo.setFlag(mbo.READONLY, True)
    else:
        for i in range(7):
            if mbo.getString('JM_WORKSTATUS' + str(i)) == 'APPROVED':
                mbo.setFieldFlag('JM_ACTUAL' + str(i), mbo.READONLY, True)
                mbo.setFieldFlag('JM_WORKLOCATION' + str(i), mbo.READONLY, True)
                mbo.setFieldFlag('JM_REMARKSTS' + str(i), mbo.READONLY, True)
                mbo.setFieldFlag('JM_WORKSTATUS' + str(i), mbo.READONLY, True)
            elif mbo.getString('JM_WORKSTATUS' + str(i)) == 'SUBMITTED':
                mbo.setFieldFlag('JM_WORKLOCATION' + str(i), mbo.REQUIRED, True)
                mbo.setFieldFlag('JM_REMARKSTS' + str(i), mbo.REQUIRED, True)

#Add entry total hours
def addEntryHours():
    sum = 0
    for i in range(7):
        sum += mbo.getFloat('JM_ACTUAL' + str(i))
    mbo.setValue('JM_TOTACTUALHRS', sum, mbo.NOACCESSCHECK)

#Validate status before approving
def validateStatus():
    if mbo.getString('JM_WORKSTATUS') != 'NOT STARTED':
        for i in range(7):
            if mbo.getFloat('JM_ACTUAL' + str(i)) == 0:
                mbo.setValue('JM_WORKSTATUS' + str(i), 'CANCELLED', mbo.NOACCESSCHECK)
    if mbo.getString('JM_WORKSTATUS') == 'APPROVED':
        for i in range(7):
            if mbo.getString('JM_WORKSTATUS' + str(i)) not in ('CANCELLED', 'APPROVED'):
                service.error('JM_WORKLOG', 'JM_CannotApproveRow')
    elif mbo.getString('JM_WORKSTATUS') == 'CANCELLED':
        for i in range(7):
            if mbo.getString('JM_WORKSTATUS' + str(i)) == 'APPROVED':
                service.error('JM_WORKLOG', 'JM_CannotCancelApprovedRow')

#Add day to labtrans
def submitDayToLabTrans():
    laborMboSet = MXServer.getMXServer().getMboSet('LABTRANS', mbo.getUserInfo())
    
    for i in range(7):
        mboValue = mbo.getMboValue('JM_WORKSTATUS' + str(i))
        previous = mboValue.getPreviousValue().asString()
        current = mboValue.getCurrentValue().asString()
        if previous == 'SUBMITTED' and current not in ('APPROVED', 'SUBMITTED'):
            laborMboSet.setWhere(
                'JM_ENTRYID = \'' + mbo.getString('JM_WORKENTRYID') + str(i) + '\''
            )
            laborMboSet.reset()
            laborMboFirst = laborMboSet.moveFirst()
            if laborMboFirst:
                laborMboFirst.delete()
                laborMboSet.save()
        elif previous == 'SUBMITTED' and current == 'APPROVED' and app:
            laborMboSet.setWhere(
                'JM_ENTRYID = \'' + mbo.getString('JM_WORKENTRYID') + str(i) + '\''
            )
            laborMboSet.reset()
            laborMboFirst = laborMboSet.moveFirst()
            if laborMboFirst:
                service.error(str(laborMboFirst.getBoolean('GENAPPRSERVRECEIPT')), '')
                if not laborMboFirst.getBoolean('GENAPPRSERVRECEIPT'):
                    laborMboFirst.setValue('GENAPPRSERVRECEIPT', 1, mbo.NOACCESSCHECK)
                    laborMboSet.save()
        elif mbo.getString('JM_WORKSTATUS' + str(i)) == 'SUBMITTED':
            laborMboSet.setWhere(
                'JM_ENTRYID = \'' + mbo.getString('JM_WORKENTRYID') + str(i) + '\''
            )
            laborMboSet.reset()
            laborMboFirst = laborMboSet.moveFirst()
            if not laborMboFirst:
                wLogMboSet = mbo.getMboSet('JM_WORKLOGGING')
                wLogMbo = wLogMboSet.moveFirst()
                parser = SimpleDateFormat('MMM dd, yyyy')
                dateFormat = parser.parse(wLogMbo.getString('JM_DAY' + str(i)))
                cal = Calendar.getInstance()
                cal.setTime(dateFormat)
                
                laborMbo = laborMboSet.add()
                laborMbo.setValue('ORGID', mbo.getString('ORGID'), mbo.NOACCESSCHECK)
                laborMbo.setValue('SITEID', mbo.getString('SITEID'), mbo.NOACCESSCHECK)
                laborMbo.setValue('JM_ENTRYID', mbo.getString('JM_WORKENTRYID') + str(i), mbo.NOACCESSCHECK)
                laborMbo.setValue('LABORCODE', wLogMbo.getString('JM_LABORCODE'), mbo.NOACCESSCHECK)
                laborMbo.setValue('REGULARHRS', mbo.getString('JM_ACTUAL' + str(i)), mbo.NOACCESSCHECK)
                laborMbo.setValue('STARTDATE', cal.getTime(), mbo.NOACCESSCHECK)
                laborMbo.setValue('WONUM', mbo.getString('JM_WONUM'), mbo.NOACCESSCHECK)
                laborMbo.setValue('TRANSTYPE','WORK',mbo.NOACCESSCHECK)
                laborMboSet.save()
            else:
                mboActualValue = mbo.getMboValue('JM_ACTUAL' + str(i))
                mboWonumValue = mbo.getMboValue('JM_WONUM')
                actualCondition = mboActualValue.getInitialValue().asString() == mboActualValue.getCurrentValue().asString()
                wonumCondition = mboWonumValue.getInitialValue().asString() == mboWonumValue.getCurrentValue().asString()
                if wonumCondition or actualCondition:
                    laborMboFirst.setValue('REGULARHRS', mbo.getString('JM_ACTUAL' + str(i)), mbo.NOACCESSCHECK)
                    laborMboFirst.setValue('WONUM', mbo.getString('JM_WONUM'), mbo.NOACCESSCHECK)
'''Init lp'''
if launchPoint == 'INIT':
    if onadd:
        for i in range(7):
            mbo.setValue('JM_ACTUAL' + str(i), 0,  mbo.NOACCESSCHECK|mbo.NOVALIDATION|mbo.NOACTION)
        if mbo.getOwner():
            mbo.setValue('JM_WORKNUMBER', mbo.getOwner().getString('JM_WORKNUMBER'), mbo.NOACCESSCHECK)
    else:
        mbo.setFieldFlag('JM_WONUM', mbo.READONLY, True)
    setEntryVisibility()

'''Save lp - add, update | before save'''
if launchPoint == 'SAVE':
    addEntryHours()
    validateStatus()
    setWeekStatus()
    submitDayToLabTrans()

'''Save lp - delete | before save'''
if launchPoint == 'SAVE_DELETE':
    laborMboSet = MXServer.getMXServer().getMboSet('LABTRANS', mbo.getUserInfo())
    for i in range(7):
        mboValue = mbo.getMboValue('JM_WORKSTATUS' + str(i)).getInitialValue().asString()
        if mboValue == 'SUBMITTED':
            laborMboSet.setWhere(
                'JM_ENTRYID = \'' + mbo.getString('JM_WORKENTRYID') + str(i) + '\''
            )
            laborMboSet.reset()
            laborMboFirst = laborMboSet.moveFirst()
            if laborMboFirst:
                laborMboFirst.delete()
                laborMboSet.save()

'''AftSave lp - add, update, delete | after save'''
if launchPoint == 'AFTSAVE' and not mbo.getOwner().toBeDeleted():
    wEntryMboSet = mbo.getMboSet('JM_WORKENTRY')
    wEntryMbo = wEntryMboSet.moveFirst()
    wLogMboSet = mbo.getMboSet('JM_WORKLOGGING')
    wLogMbo = wLogMboSet.moveFirst()
    
    qtt = 0
    statusDict = {
        'CANCELLED': 0,
        'NOT STARTED': 0,
        'IN PROGRESS': 0,
        'SUBMITTED': 0,
        'APPROVED': 0
    }
    while wEntryMbo:
        statusDict[wEntryMbo.getString('JM_WORKSTATUS')] += 1
        qtt += 1
        wEntryMbo = wEntryMboSet.moveNext()
    if statusDict['CANCELLED'] == qtt:
        wLogMbo.setValue('JM_STATUS', 'CANCELLED', mbo.NOACCESSCHECK|mbo.NOVALIDATION)
    elif statusDict['NOT STARTED'] == qtt:
        wLogMbo.setValue('JM_STATUS', 'NOT STARTED', mbo.NOACCESSCHECK|mbo.NOVALIDATION)
    elif statusDict['SUBMITTED'] == qtt:
        wLogMbo.setValue('JM_STATUS', 'SUBMITTED', mbo.NOACCESSCHECK|mbo.NOVALIDATION)
    elif statusDict['APPROVED'] == qtt or statusDict['APPROVED'] + statusDict['CANCELLED'] == qtt:
        wLogMbo.setValue('JM_STATUS', 'APPROVED', mbo.NOACCESSCHECK|mbo.NOVALIDATION)
    elif statusDict['SUBMITTED'] + statusDict['APPROVED'] + statusDict['CANCELLED'] == qtt:
        wLogMbo.setValue('JM_STATUS', 'SUBMITTED', mbo.NOACCESSCHECK|mbo.NOVALIDATION)
    else:
        wLogMbo.setValue('JM_STATUS', 'IN PROGRESS', mbo.NOACCESSCHECK|mbo.NOVALIDATION)
    
    wEntryMboSet = mbo.getMboSet('JM_WORKENTRY')
    wEntryMbo = wEntryMboSet.moveFirst()
    
    if wEntryMboSet:
        totalSum = 0
        for i in range(7):
            wEntryMbo = wEntryMboSet.moveFirst()
            sum = 0
        
            while wEntryMbo:
                sum += wEntryMbo.getFloat('JM_ACTUAL' + str(i))
                wEntryMbo = wEntryMboSet.moveNext()
            
            wLogMbo.setValue('JM_TOTAL' + str(i), sum,  mbo.NOACCESSCHECK)
            totalSum += sum
        wLogMbo.setValue('JM_TOTACTUALHRS', totalSum,  mbo.NOACCESSCHECK)
    wLogMboSet.save()


'''Allow Object Creation lp '''
if launchPoint == 'ALLOWOBJCREATION':
    if mboset.getOwner() and mboset.getOwner().toBeAdded():
        service.error('JM_WORKLOG', 'JM_NeedToSave')

'''Allow Object Deletion lp '''
if launchPoint == 'ALLOWDELETE':
    for i in range(7):
        if mbo.getString('JM_WORKSTATUS' + str(i)) == 'APPROVED':
            service.error('JM_WORKLOG', 'JM_CannotDeleteRow')

'''Attribute lps for status - validade'''
if launchPoint == 'JM_WORKSTATUS0':
    submitWorkEntry(0)
    setWeekStatus()
elif launchPoint == 'JM_WORKSTATUS1':
    submitWorkEntry(1)
    setWeekStatus()
elif launchPoint == 'JM_WORKSTATUS2':
    submitWorkEntry(2)
    setWeekStatus()
elif launchPoint == 'JM_WORKSTATUS3':
    submitWorkEntry(3)
    setWeekStatus()
elif launchPoint == 'JM_WORKSTATUS4':
    submitWorkEntry(4)
    setWeekStatus()
elif launchPoint == 'JM_WORKSTATUS5':
    submitWorkEntry(5)
    setWeekStatus()
elif launchPoint == 'JM_WORKSTATUS6':
    submitWorkEntry(6)
    setWeekStatus()
elif launchPoint == 'JM_WORKSTATUS':
    setAllDaysStatus(str(mbovalue))

'''Attribute lps for actual hours - validade'''
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
