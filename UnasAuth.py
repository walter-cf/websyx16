#
import time
import logging
import requests
import MyUtils as MU
import xml.etree.ElementTree as ET

unasToken : str = 'x'
unasTokenTime = time.time()

def doLogin() -> str:
  if MU.IGNORE_BLOCKED_UNAS:
      return '123456'
  
  logging.basicConfig(level=logging.INFO)
  xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><ApiKey>'+MU.API_KEY+'</ApiKey></Params>'
  x = requests.post( MU.UNASAPI_URL + '/login', data=xmlParam)
  if (200 == x.status_code):
    if (x.text[0:15] == '<!DOCTYPE html>'):
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
          return str(currToken)
      else:
        raise ValueError("Login response not OK:" + str(currStatus) + "\n" + x.text )
    else:
      raise ValueError("Login resp XML-err:" + str(x.status_code) + "\n" + x.text )
  else:
    print(x.status_code)
    print(x.text)

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
