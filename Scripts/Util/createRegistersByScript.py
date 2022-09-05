from psdi.mbo import MboConstants
from psdi.server import MXServer

data = [
    {
        "XXXX": "XXXX",
        "ZZZZ": 0
    }
]

xMboSet = MXServer.getMXServer().getMboSet('XXXXX', MXServer.getMXServer().getSystemUserInfo())

for i in data:
    if i["XXXX"] and i["ZZZZ"]:
        xMbo = xMboSet.add()
        xMbo.setValue('XXXX', i["XXXX"], MboConstants.NOACCESSCHECK)
        xMbo.setValue('ZZZZ', i["ZZZZ"], MboConstants.NOACCESSCHECK)
xMboSet.save()
