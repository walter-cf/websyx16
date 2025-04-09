# Import smtplib for the actual sending function
import smtplib
import threading
# Import the email modules we'll need
from email.message import EmailMessage

import MyUtils as MU
import MyUtilsTypes as MUT


#
# https://docs.python.org/3/library/email.examples.html
#
def sendProxyMail(message:str, alertTyp:MUT.AlertMailType, subject :str = 'alert from WebSyx-Proxy'):
    unasCtx = MU.getUnasContext()
    if alertTyp is None:
        actionType = MU.getActionTypeFromTS()                         # Ez itt nagyon kulon van a levelkuldestol
        alertTyp = MUT.AlertMailType(actionType)
    alertTyp.sent = MU.getCurrTime()
    unasCtx.lastAlertMailSent.append(alertTyp)

    # Create a text/plain message
    msg = EmailMessage()
    uCtx = MU.getUnasContext()
    _ctxMsg = f"Context:: client:{uCtx.lastIpAddress}, action:{uCtx.lastAction} -+- TS:{uCtx.lastTS}, tsTime:{MU.getTimeStringTS()}, tsType:{MU.getActionTypeNameFromTS()}"
    msg.set_content( _ctxMsg + "\r\n\r\n" + message )
    msg['Subject'] = f"[WebSyx-{MU.getUnasContext().processName}] {subject}"
    msg['From'] = MU.MAIL_ME     # me == the sender's email address
    msg['To'] = MU.MAIL_OPERATOR # you == the recipient's email address
    # Send the message via our own SMTP server.
    s = smtplib.SMTP(MU.MAIL_SERVER)
    s.send_message(msg)
    s.quit()