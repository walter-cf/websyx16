# Import smtplib for the actual sending function
import smtplib
import MyUtils as MU

# Import the email modules we'll need
from email.message import EmailMessage
#
# https://docs.python.org/3/library/email.examples.html
#
def sendAlertMail(message:str, subject :str = 'alert from WebSyx-Proxy'):
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content( message )
    msg['Subject'] = subject
    msg['From'] = MU.MAIL_ME     # me == the sender's email address
    msg['To'] = MU.MAIL_OPERATOR # you == the recipient's email address
    # Send the message via our own SMTP server.
    s = smtplib.SMTP(MU.MAIL_SERVER)
    s.send_message(msg)
    s.quit()