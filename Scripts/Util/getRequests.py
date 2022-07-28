from psdi.iface.router import HTTPHandler
from java.util import HashMap
from java.util import String

handler = HTTPHandler()
map = HashMap()
map.put("URL",url)
map.put("HTTPMETHOD","GET")
responseBytes = handler.invoke(map,None)
response = String(responseBytes,"utf-8")
