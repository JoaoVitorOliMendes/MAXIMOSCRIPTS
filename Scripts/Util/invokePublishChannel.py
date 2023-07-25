from psdi.server import MXServer
server = MXServer.getMXServer()
userInfo = mbo.getUserInfo()
mic = server.lookup("MIC")
mic.exportData("PUBLISHCHANNEL","EXTERNALSYSTEM","WHERE", userInfo, AMOUNTOFRECORDS)

from psdi.iface.mic import PublishChannelCache
PublishChannelCache.getInstance().getPublishChannel("PUBLISHCHANNEL").publish(mbo, True);
