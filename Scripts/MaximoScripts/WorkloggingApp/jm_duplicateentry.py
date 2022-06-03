from java.text import SimpleDateFormat
from java.util import Calendar
from java.lang import System
from psdi.server import MXServer

def duplicate():
    maxDate = mbo.getDate('JM_WEEKSTARTDATE')
    calStartDay = Calendar.getInstance()
    calStartDay.setTime(maxDate)
    calEndDay = Calendar.getInstance()
    calEndDay.setTime(maxDate)
    calEndDay.add(Calendar.DATE, 6)
    
    today = MXServer.getMXServer().getDate()
    calToday = Calendar.getInstance()
    calToday.setTime(today)
    dayOfTheWeek = calToday.get(Calendar.DAY_OF_WEEK)
    calToday.add(Calendar.DATE, 2 - (dayOfTheWeek % 7))
    
    if calToday.getTime().getTime() < calStartDay.getTime().getTime() or calToday.getTime().getTime() > calEndDay.getTime().getTime():
        service.error('JM_WORKLOG', 'JM_NotCurrentWeek')
        
    wEntryMboSet = mbo.getMboSet('JM_WORKENTRY')
    weeksMboSet = mbo.getMboSet('WEEKS')
    weeksMbo = weeksMboSet.moveFirst()
    if weeksMbo:
        cal = Calendar.getInstance()
        parser = SimpleDateFormat('yyyy-MM-dd')
        endDate = parser.parse(weeksMbo.getString('WEEK_START'))
        cal.setTime(endDate)
        cal.add(Calendar.DATE, -1)
        lastWeekMbo = mbo.getMboSet('$WEEKS', 'WEEKS', 'week_end = \'' + parser.format(cal.getTime()) + '\'').moveFirst()
        if lastWeekMbo:
            wLogLastWeekMboSet = mbo.getMboSet('$JM_WORKLOGGING', 'JM_WORKLOGGING', 'jm_weeknumber = \'' + lastWeekMbo.getString('week') + '\' and jm_laborcode = \'' + mbo.getString('JM_LABORCODE') + '\'')
            wLogLastWeekMbo = wLogLastWeekMboSet.moveFirst()
            if wLogLastWeekMbo:
                wEntryLastWeekMboSet = wLogLastWeekMbo.getMboSet('JM_WORKENTRY')
                wEntryLastWeekMbo = wEntryLastWeekMboSet.moveFirst()
                while wEntryLastWeekMbo:
                    w = wEntryMboSet.add()
                    w.setValue('JM_WORKNUMBER', mbo.getString('JM_WORKNUMBER'), mbo.NOACCESSCHECK)
                    w.setValue('JM_WONUM', wEntryLastWeekMbo.getString('JM_WONUM'), mbo.NOACCESSCHECK)
                    wEntryLastWeekMbo = wEntryLastWeekMboSet.moveNext()
                return
    service.error('JM_WORKLOG','JM_NoMoreLines')

if launchPoint == 'JM_DUPLICATEENTRY':
    duplicate()
