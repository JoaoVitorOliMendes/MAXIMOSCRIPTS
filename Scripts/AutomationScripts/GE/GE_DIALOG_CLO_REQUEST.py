from psdi.server import MXServer
from psdi.common.context import UIContext
from psdi.webclient.system.controller import SessionContext, Utility, WebClientEvent

mxServer = MXServer.getMXServer()
context = UIContext.getCurrentContext()
if context:
    wcs = context.getWebClientSession()
    Utility().sendEvent(WebClientEvent("GE_request_close", wcs.getCurrentPageId(), None, SessionContext(wcs)))
