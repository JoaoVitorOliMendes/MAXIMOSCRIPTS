from java.util import Calendar

today = MXServer.getMXServer().getDate()
calToday = Calendar.getInstance()
calToday.setTime(today)
calToday.getTime()



from java.text import SimpleDateFormat

parser = SimpleDateFormat('yyyy-MM-dd')
parsedDate = parser.parse(calToday.getTime())
formatedDate = parser.format(calToday.getTime())
