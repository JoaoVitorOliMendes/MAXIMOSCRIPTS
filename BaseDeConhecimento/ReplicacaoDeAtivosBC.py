from psdi.server import MXServer
from psdi.mbo import MboConstants

if launchPoint == "INIT" and not onadd:
    if mbo.getBoolean('REPLICAR'):
        mbo.setFlag(mbo.READONLY, True)

if launchPoint == "SAVE" and onadd:
    siteMboSet = MXServer.getMXServer().getMboSet('SITE', mbo.getUserInfo())
    siteMboSet.setWhere('ORGID = \'' + mbo.getString("ORGID") + '\' AND active = 1 ')
    siteMboSet.reset()
    
    if not siteMboSet.isEmpty():
        siteMbo = siteMboSet.moveFirst()
        bcsiteMboSet = mbo.getMboSet("JM_BCSITES")
        
        while siteMbo:
            bcsiteMbo = bcsiteMboSet.add()
            bcsiteMbo.setValue("SITEID", siteMbo.getString("SITEID"))
            bcsiteMbo.setValue("OWNERTABLE", "JM_BC", MboConstants.NOACCESSCHECK)
            bcsiteMbo.setValue('OWNERID', mbo.getInt("assetuid") ,mbo.NOACCESSCHECK) 
            siteMbo = siteMboSet.moveNext()
        bcsiteMboSet.save()

if launchPoint == "UPDATE":
    ownerTable = mbo.getOwner()
    if ownerTable and ownerTable.getName() == "ASSET":
        assetSet = ownerTable.getThisMboSet()
        if mbo.getBoolean("REPLICAR"):
            
            siteid = mbo.getString("SITEID")
            
            assetMbo = assetSet.add()
            assetMbo.setValue("SITEID", siteid ,mbo.NOACCESSCHECK)
            assetMbo.setValue('ASSETNUM', siteid[0:3] + " - " + ownerTable.getString('ASSETNUM'), mbo.NOACCESSCHECK)
            assetMbo.setValue('DESCRIPTION', ownerTable.getString('DESCRIPTION') , mbo.NOACCESSCHECK)
            assetMbo.setValue('ORGID', ownerTable.getString('ORGID'), mbo.NOACCESSCHECK)
            assetMbo.setValue('STATUS', ownerTable.getString('STATUS'), mbo.NOACCESSCHECK)
            assetMbo.setValue('JM_APPROVER', ownerTable.getString('JM_APPROVER'), mbo.NOACCESSCHECK)
            assetMbo.setValue('JM_TYPE', ownerTable.getString('JM_TYPE'), mbo.NOACCESSCHECK)
            assetMbo.setValue('JM_ASSETNUM', ownerTable.getString('JM_ASSETNUM'), mbo.NOACCESSCHECK)
            assetMbo.setValue('JM_RECORDTYPE', "JM_BC", mbo.NOACCESSCHECK)
            mbo.setValue('REPLICADO', True, mbo.NOACCESSCHECK)
            #assetSet.save()