mboSetToBeAdded = mbo.getMboSet('XXXXX')
mboSetToBeDupped = mbo.getMboSet('YYYYY')
mboToBeDupped = mboSetToBeDupped.moveFirst()
while mboToBeDupped:
    mboToBeAdded = mboToBeDupped.copy(mboSetToBeAdded)
    mboToBeAdded.setValue('STATUS', 'WAPPR', mbo.NOACCESSCHECK)
    mboToBeAdded.setValue('STATUSDATE', mxServer.getDate(), mbo.NOACCESSCHECK)
    mboToBeDupped = mboSetToBeDupped.moveNext()
