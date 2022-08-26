userInfo = mbo.getUserInfo()

from psdi.server import MXServer
mxServer = MXServer.getMXServer()
userInfo = mxServer.getUserInfo("maxadmin")

from psdi.server import MXServer
mxServer = MXServer.getMXServer()
userInfo = mxServer.getSystemUserInfo()

from psdi.server import MXServer
from psdi.iface.mic import MicService
 
mxServer = MXServer.getMXServer()
micService = MicService(mxServer)
micService.init()
userInfo = micService.getNewUserInfo()

print "User Name        : " + str(userInfo.getUserName())
print "User Display Name: " + str(userInfo.getDisplayName())
print "User ID          : " + str(userInfo.getLoginUserName())
print "e-Mail           : " + str(userInfo.getEmail())
print "Default Language : " + str(userInfo.getDefaultLang())
print "Current Language : " + str(userInfo.getLangCode())
print "Timezone         : " + str(userInfo.getTimeZone())
 
# Check if we are running in Interactive mode or from a System Job
if not userInfo.isInteractive():
    print "------"
    print "Setting Language code to EN"
    print "------"
 
    userInfo.setLangCode("EN")
 
    print "Current Language : " + str(userInfo.getLangCode())
