# ------------------------------------------------------
# MaximoCon, Março de 2022
# Objetivo: Script para manipulação do objeto JM_LOG
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

#from java.time import LocalDateTime
from psdi.server import MXServer

# INIT
# Se o campo MANUAL estiver desativado, ou o usuário for diferente do criador do LOG, o usuario não poderá editar o LOG
if launchPoint == "INIT" and not onadd:
    if mbo.isNull("MANUAL") or not mbo.getBoolean("MANUAL") or mbo.getString('CHANGEBY') != mbo.getUserName():
        mbo.setFieldFlag('DESCRIPTION', mbo.READONLY, True)
        mbo.setFieldFlag('DESCRIPTION_LONGDESCRIPTION', mbo.READONLY, True)

# SAVE
# Preenchimento automatico dos campos CHANGEBY & CHANGEDATE
if launchPoint == "SAVE" and onadd and mbo.getBoolean("MANUAL"):
    #service.error("configure", "BlankMsg", [mbo.getUserName()])
    mbo.setValue("CHANGEBY", mbo.getUserName(), mbo.NOACCESSCHECK)
    #mbo.setValue("CHANGEDATE", LocalDateTime.now()) // Versao java
    mbo.setValue("CHANGEDATE", MXServer.getMXServer().getDate(), mbo.NOACCESSCHECK)
    
# DELETE
# Erro se alguém além do autor tentar deletar o log
if launchPoint == "DELETE":
    if (mbo.getString("CHANGEBY") != mbo.getUserName()) or not mbo.getBoolean("MANUAL"):
        service.error("configure", "BlankMsg", [u"Você não está autorizado para alterar este log!"])

# ACTION
# Preencher automaticamente novo log pelo workflow
if launchPoint == "JM_WCACTION":
    mboLogSet = mbo.getMboSet('JM_LOG')
    mboLog = mboLogSet.add()
    mboLog.setValue('DESCRIPTION', 'Justificativa', mbo.NOACCESSCHECK)
    mboLog.setValue('DESCRIPTION_LONGDESCRIPTION',mbo.getString("JM_LOG") , mbo.NOACCESSCHECK)
    mboLog.setValue('CHANGEDATE', MXServer.getMXServer().getDate(), mbo.NOACCESSCHECK)
    mboLog.setValue("CHANGEBY",mbo.getUserName(),mbo.NOACCESSCHECK)
    mboLog.setValue("MANUAL",False,mbo.NOACCESSCHECK)
    mboLog.setValue("OWNERTABLE","JM_BC",mbo.NOACCESSCHECK)
    mboLog.setValue("OWNERID",mbo.getUniqueIDValue(),mbo.NOACCESSCHECK)
    mbo.setValueNull("JM_LOG")
