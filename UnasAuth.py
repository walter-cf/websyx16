#
import time
import logging
import requests
import MyUtils as MU
from MyUtilsTypes import UnasTransactionType as UTSTYPE
import MySmtpClient as SM
import xml.etree.ElementTree as ET

unasToken : str = 'x'
unasTokenTime = time.time()

def doLogin() -> str:
  if MU.IGNORE_BLOCKED_UNAS:
      return '123456'
    
  MU.checkCommError()
  alertMessage = 'Empty errorMessage'
  #logging.basicConfig(level=logging.INFO)
  xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><ApiKey>'+MU.API_KEY+'</ApiKey></Params>'
  MU.createStatEntry('xx-login', xmlParam)
  x = requests.post( MU.UNASAPI_URL + '/login', data=xmlParam)
  if (200 == x.status_code):
    if (x.text[0:15] == '<!DOCTYPE html>'):
      MU.createStatEntryERR(404, 'Login err! Reply is HTML-like - UNAS account is expired/denied')
      raise ValueError("Login err! Reply is HTML-like - UNAS account is expired/denied" )

    dom=ET.fromstring(x.text)
    #  for itm in dom.findall('Login'):
    _st = dom.find('Status')
    if not _st is None:
      currStatus = _st.text
      if 'ok' == currStatus:
        _tkn = dom.find('Token')
        if _tkn is not None:
          currToken = _tkn.text
          logging.debug("Token: %s, Status: %s", currToken, currStatus)
          MU.createStatEntryOK(currToken)
          return str(currToken)
      else:
        alertMessage = "Login response:%s not OK:%s" % (  str(currStatus) , x.text )
        MU.createStatEntryERR(403, alertMessage)
        # raise ValueError("Login response not OK:" + str(currStatus) + "\n" + x.text )
    else:
      alertMessage = "Login resp XML-err:%d\r\n%s" % ( x.status_code, x.text )
      MU.createStatEntryERR(404, alertMessage)
      # raise ValueError("Login resp XML-err:" + str(x.status_code) + "\n" + x.text )
  else:
    alertMessage = 'Login err:%s' % x.text
    MU.createStatEntryERR(x.status_code, alertMessage)
  #
  SM.sendAlertMail( alertMessage )
  raise ValueError("Login err:" + str(x.status_code) + "\n" + x.text )

def doAuth(force=False) -> str:
    global unasToken
    global unasTokenTime
    if len(unasToken) < 10 or force:
        unasToken = doLogin()
        unasTokenTime = time.time()
    elif time.time() - unasTokenTime > 7000: # 2 ora kb...
        unasToken = doLogin()
    #
    return unasToken
