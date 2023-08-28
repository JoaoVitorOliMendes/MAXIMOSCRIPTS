actionSet = mbo.getMboSet("$EMXOKACTION","ACTION","action='OKSTATUS'")
actionMbo=actionSet.moveFirst()
if actionMbo:
    actionMbo.executeAction(mbo)
