from psdi.server import MXServer

def sendEmail(toSend, subject, message):
    send = 'maxadmin@ge.com'
    message += '\n\nPlease do not reply, this is an email sent automatically.\n'  
    message += 'Maximo system - GE.'

    if toSend:
        mx = MXServer.getMXServer()
        mx.sendEMail(toSend,send, subject,message)
