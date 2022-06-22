# ------------------------------------------------------
# MaximoCon, Março de 2022
# Objetivo: Script para manipulação do objeto JM_BCSITES
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

from psdi.server import MXServer
from psdi.mbo import MboConstants

# INIT
# Seta os campos "REPLICAR" para readonly
if launchPoint == "INIT" and not onadd:
    if mbo.getBoolean('REPLICAR'):
        mbo.setFlag(mbo.READONLY, True)

# SAVE
# Ao salvar um novo conhecimento cria uma nova entrada "JM_BCSITES"
if launchPoint == "SAVE" and onadd:
    siteMboSet = MXServer.getMXServer().getMboSet('SITE', mbo.getUserInfo())
    # Where clause para selecionar apenas os sites ativos da mesma organizacao
    siteMboSet.setWhere("ORGID = \'" + mbo.getString("ORGID") + "\' AND active = 1 and siteid <> '" + mbo.getString("SITEID") + "'")
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
        #bcsiteMboSet.save()

# UPDATE
# Ao atualizar uma entrada "JM_BCSITES" checa se esta marcada ara replicamento, 
# se sim relpica o conhecimento para o novo site
if launchPoint == "UPDATE":
    ownerTable = mbo.getOwner()
    if ownerTable and ownerTable.getName() == "ASSET":
        assetMboSet = ownerTable.getThisMboSet()
        if mbo.getBoolean("REPLICAR"):
            
            siteid = mbo.getString("SITEID")
            
            assetMbo = assetMboSet.add()
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
            
            itemMboSet = ownerTable.getMboSet('JM_REL')
            if not itemMboSet.isEmpty():
                itemMbo = itemMboSet.moveFirst()
                while itemMbo:
                    itemMboNew = assetMbo.getMboSet('JM_REL').add()
                    itemMboNew.setValue('SCOPE',itemMbo.getString('SCOPE'),mbo.NOACCESSCHECK) 
                    itemMboNew.setValue('IMPACT',itemMbo.getString('IMPACT'),mbo.NOACCESSCHECK) 
                    itemMboNew.setValue('DESCRIPTION',itemMbo.getString('DESCRIPTION'),mbo.NOACCESSCHECK) 
                    itemMboNew.setValue('DESCRIPTION_LONGDESCRIPTION',itemMbo.getString('DESCRIPTION_LONGDESCRIPTION'),mbo.NOACCESSCHECK) 
                    itemMboNew.setValue('OWNERID',assetMbo.getString('ASSETUID'),mbo.NOACCESSCHECK) 
                    itemMboNew.setValue('OWNERTABLE','JM_BC',mbo.NOACCESSCHECK) 
                    itemMbo = itemMboSet.moveNext()
