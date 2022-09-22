from psdi.webclient.system.controller import Utility, WebClientEvent

webSession = service.webclientsession()
webSession.getCurrentApp().getAppBean().reset()
# Abre a aplicação de acordo com o workorderid
webSession.getCurrentApp().getAppBean().moveToUniqueId("WONUM")

Utility.sendEvent(WebClientEvent("click", "plans", "", None, None, None, -1, webSession))



'''
CREDITO: FELIPE COSTA
*** Apenas depois do save
'''
