from java.lang import System
from java.util import Calendar
from psdi.server import MXServer

mboSet = MXServer.getMXServer().getMboSet('XXXXX', mbo.getUserInfo())
mbo = mboSet.moveFirst()
while mbo:
    if mbo.getInt('XXXXX') == 0:
        mbo.delete()
    mbo = mboSet.moveNext()
mboSet.save()
