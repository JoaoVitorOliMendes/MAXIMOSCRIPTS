# ------------------------------------------------------
# MaximoCon, terça, jul 26, 2022 11:00
# Objetivo: Script to interact with close_req dialog in SNZ_WOTRACK app
# Autor: G. Murta - J. Mendes
# ------------------------------------------------------

from psdi.server import MXServer


sReqMboSet = MXServer.getMXServer().getMboSet('SR', mbo.getUserInfo())
sReqMboSet.setWhere('ticketid = \'' + mbo.getString('RELATEDRECKEY') + '\'')
sReqMboSet.reset()
sReqMbo = sReqMboSet.moveFirst()
if sReqMboSet:
    #service.error("entrou","teste")
    sReqMbo.changeStatus('INPROG', MXServer.getMXServer().getDate(), mbo.getString("GE_NP_MEMO"))
    sReqMboSet.save()
    mbo.getThisMboSet().reset()
service.closeDialog()
