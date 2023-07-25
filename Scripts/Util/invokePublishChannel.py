from psdi.server import MXServer
server = MXServer.getMXServer()
userInfo = mbo.getUserInfo()
mic = server.lookup("MIC")
mic.exportData("PUBLISHCHANNEL","EXTERNALSYSTEM","WHERE", userInfo, AMOUNTOFRECORDS)
