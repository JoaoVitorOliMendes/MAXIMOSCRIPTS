from psdi.server import MXServer
from psdi.mbo import MboConstants

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
    assetSet = mbo.getOwner().getThisMboSet()
    bcsiteSet = mbo.getThisMboSet()
    bcsiteMbo = bcsiteSet.moveFirst()
    if bcsiteMbo.getString("REPLICAR"):
        bcsiteMbo.setValue("REPLICADO", 1 ,mbo.NOACCESSCHECK)
        bcsiteMbo.setValue("REPLICAR", 0 ,mbo.NOACCESSCHECK)
        
        siteid = bcsiteMbo.getString("SITEID")
        
        assetMbo = assetSet.add()
        assetMbo.setValue("SITEID", siteid ,mbo.NOACCESSCHECK)
        assetMbo.setValue('ASSETNUM', siteid[0:3] + " - " + assetSet.getString('ASSETNUM'), mbo.NOACCESSCHECK)
        assetMbo.setValue('DESCRIPTION', assetSet.getString('DESCRIPTION') , mbo.NOACCESSCHECK)
        assetMbo.setValue('ORGID', assetSet.getString('ORGID'), mbo.NOACCESSCHECK)
        assetMbo.setValue('STATUS', assetSet.getString('STATUS'), mbo.NOACCESSCHECK)
        assetMbo.setValue('JM_APPROVER', assetSet.getString('JM_APPROVER'), mbo.NOACCESSCHECK)
        assetMbo.setValue('JM_TYPE', assetSet.getString('JM_TYPE'), mbo.NOACCESSCHECK)
        assetMbo.setValue('JM_ASSETNUM', assetSet.getString('JM_ASSETNUM'), mbo.NOACCESSCHECK)
        assetMbo.setValue('JM_RECORDTYPE', "JM_BC", mbo.NOACCESSCHECK)
        assetSet.save()