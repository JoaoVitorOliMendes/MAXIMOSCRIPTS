from java.lang import System
from java.util import Calendar
from psdi.server import MXServer

mboSet = MXServer.getMXServer().getMboSet('GE_WOGEMBA', mbo.getUserInfo())
mbo = mboSet.moveFirst()
while mbo:
    if mbo.getInt('WOCOUNT') == 1:
        mbo.delete()
    mbo = mboSet.moveNext()
mboSet.save()
