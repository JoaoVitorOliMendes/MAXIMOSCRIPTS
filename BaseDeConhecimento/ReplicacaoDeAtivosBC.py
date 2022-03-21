from psdi.mbo import MboConstants

def selectAllRegistersThatCanBeDuplicated():
    #bcsiteMboSet = mbo.getMboSet("JM_BCSITES")
    #bcsiteMboSet.setWhere("ownerid = :assetuid and ownertable = 'JM_BC' and REPLICAR = 1 and REPLICADO = 0")
    #bcsiteMboSet = mbo.getMboSet("$JM_BCSITES1", "JM_BCSITES", "ownerid = '" + str(mbo.getOwner().getString('ASSETUID')).replace(".","") + "' and ownertable = 'JM_BC' and replicar = 1 and replicado = 0")
    bcsiteMboSet = mbo.getMboSet("$JM_BCSITES1", "JM_BCSITES", "ownerid = :assetuid and ownertable = 'JM_BC' and replicar = 1 and replicado = 0")
    bcsiteMboSet.reset()

    return bcsiteMboSet

def replicateEntries():
    pass


if launchPoint == "UPDATE":
    bcsiteMboSet = selectAllRegistersThatCanBeDuplicated()

    if not bcsiteMboSet.isEmpty():
        bcsiteMbo = bcsiteMboSet.getMbo(0)
        service.error("configure","BlankMsg", [bcsiteMboSet.getName()])
        assetSet = mbo.getOwner().getThisMboSet()

        assetNumVal = assetSet.getString('ASSETNUM')
        descriptionVal = assetSet.getString('DESCRIPTION')
        orgIdVal = assetSet.getString('ORGID')
        statusVal = assetSet.getString('STATUS')
        jmApproverVal = assetSet.getString('JM_APPROVER')
        jmTypeVal = assetSet.getString('JM_TYPE')
        jmAssetNumVal = assetSet.getString('JM_ASSETNUM')

        while bcsiteMbo:
            
            #bcsiteMbo.setValue("REPLICADO", 1 ,mbo.NOACCESSCHECK)
            #bcsiteMbo.setValue("REPLICAR", 0 ,mbo.NOACCESSCHECK)
            
            sideid = bcsiteMbo.getString("SITEID")
            
            assetMbo = assetSet.addAtEnd()
            assetMbo.setValue("SITEID", sideid ,mbo.NOACCESSCHECK)
            assetMbo.setValue('ASSETNUM', assetNumVal + " - " + sideid , mbo.NOACCESSCHECK)
            assetMbo.setValue('DESCRIPTION', descriptionVal , mbo.NOACCESSCHECK)
            assetMbo.setValue('ORGID', orgIdVal, mbo.NOACCESSCHECK)
            assetMbo.setValue('STATUS', statusVal, mbo.NOACCESSCHECK)
            assetMbo.setValue('JM_APPROVER', jmApproverVal, mbo.NOACCESSCHECK)
            assetMbo.setValue('JM_TYPE', jmTypeVal, mbo.NOACCESSCHECK)
            assetMbo.setValue('JM_ASSETNUM', jmAssetNumVal, mbo.NOACCESSCHECK)
            assetMbo.setValue('JM_RECORDTYPE', "JM_BC", mbo.NOACCESSCHECK)
            bcsiteMbo = bcsiteMboSet.moveNext()
            assetSet.save()