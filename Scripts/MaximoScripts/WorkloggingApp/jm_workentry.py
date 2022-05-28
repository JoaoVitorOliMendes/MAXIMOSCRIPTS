# ------------------------------------------------------
# MaximoCon, 2022-05-23 15:02:47-0300
# Objetivo: Script to manipulate JM_WORKENTRY in JM_WORKLOGGING app
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

def addWeeklyHours():
    wEntryMboSet = mbo.getMboSet('JM_WORKENTRY')
    wLogMboSet = mbo.getMboSet('JM_WORKLOGGING')
    
    if wEntryMboSet:
        wEntryMbo = wEntryMboSet.moveFirst()
        wLogMbo = wLogMboSet.moveFirst()
        
        sum = 0
        
        while wEntryMbo:
            sum += wEntryMbo.getFloat('JM_TOTACTUALHRS')
            wEntryMbo = wEntryMboSet.moveNext()
            
        #Converting decimal to minutes - 0.50 = 30 min
        #Not necessary since maximo duration already converts it back
        #minutesString = sum - int(sum)
        #minutes = str(int(round(minutesString * 60)))
        
        #hours = str(int(sum))
        #finalString = hours + ':' + minutes
        
        wLogMbo.setValue('JM_TOTACTUALHRS', sum,  mbo.NOACCESSCHECK)
        wLogMboSet.save()

def addDayOfWeekHours():
    wEntryMboSet = mbo.getMboSet('JM_WORKENTRY')
    wLogMboSet = mbo.getMboSet('JM_WORKLOGGING')
    
    if wEntryMboSet:
        for i in range(7):
            wEntryMbo = wEntryMboSet.moveFirst()
            wLogMbo = wLogMboSet.moveFirst()
            sum = 0
        
            while wEntryMbo:
                sum += wEntryMbo.getFloat('JM_ACTUAL' + str(i))
                wEntryMbo = wEntryMboSet.moveNext()
            
            wLogMbo.setValue('JM_TOTAL' + str(i), sum,  mbo.NOACCESSCHECK)
            wLogMboSet.save()

#Init lp
if launchPoint == 'INIT':
    if onadd:
        mbo.setValue('JM_WORKNUMBER',mbo.getOwner().getString('JM_WORKNUMBER'), mbo.NOACCESSCHECK)

#Save lp - add, update | before save
if launchPoint == 'SAVE':
    sum = 0
    
    #Adding all the durations
    for i in range(7):
        sum += mbo.getFloat('JM_ACTUAL' + str(i))
        
    #Converting decimal to minutes - 0.50 = 30 min
    minutesString = sum - int(sum)
    minutes = str(int(round(minutesString * 60)))
    
    hours = str(int(sum))
    finalString = hours + ':' + minutes
    
    mbo.setValue('JM_TOTACTUALHRS', finalString, mbo.NOACCESSCHECK)

#AftSave lp - add, update | after save
if launchPoint == 'AFTSAVE':
    addDayOfWeekHours()
    addWeeklyHours()
