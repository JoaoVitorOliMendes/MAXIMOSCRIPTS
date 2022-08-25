from java.lang import System
from java.util import Calendar
from psdi.server import MXServer

data = [
    {
        "XXXX": "XXXX",
        "ZZZZ": 0
    }
]

mboSet = MXServer.getMXServer().getMboSet('XXXXX', mbo.getUserInfo())

for i in data:
    if i["XXXX"] and i["ZZZZ"]:
        mbo = mboSet.add()
        mbo.setValue('XXXX', i["XXXX"], mbo.NOACCESSCHECK)
        mbo.setValue('ZZZZ', i["ZZZZ"], mbo.NOACCESSCHECK)
        mboSet.save()
