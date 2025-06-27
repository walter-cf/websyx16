#!/usr/bin/python3
import html
import logging
import os
import sys
import threading
import time
import traceback as SysTB
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, unquote, urlparse

import FdbUtils as FBU
# import urllib
#
import GetProcessor as getProc
import MyBatch as MB
import MySmtpClient as SM
import MySocket
import MyUtils as MU
import PostProcessorUNAS as PPU
from MyUtilsTypes import *

global GBL_ErrorMessages
GBL_ErrorMessages = []

def stopControlWebThread():
    if controlWebThread is not None:
        if MySocket.myControlWebServer is not None:
            MySocket.myControlWebServer.shutdown()
            time.sleep(2)
            controlWebThread.join()
            logging.info('controlWebThread - stopped %s', MySocket.myControlWebServer )
        else:
          logging.info('controlWebThread(!) - already stopped? %s', MySocket.myControlWebServer )
    else:
        logging.info('controlWebThread is zero? Already stopped?' )

 
def aboutProxy():
  return MU.mdConverter( 'WebContent/dox/ABOUT' )

def logrotate(fn:str):
  if os.path.exists(fn):
    maxIdx = 0
    LOGDIR = 'logz'
    for f in os.listdir(LOGDIR):
      if f.startswith(fn[:-4]) and f.endswith('log'):
          idx = -1  if '-' not in f else int(f[1+f.rindex('-'):-4])
          maxIdx = maxIdx if idx < maxIdx else idx
    os.rename(fn , f'./{LOGDIR}/{fn[:-4]}-{1+maxIdx}.log')

class MyServer(BaseHTTPRequestHandler):
  
  def do_GET(self): # the do_GET method is inherited from BaseHTTPRequestHandler
    global GBL_ErrorMessages
    parsedUlParts = urlparse(self.path)
    pPath = parsedUlParts.path.split("/")
    queryParams = parse_qs( parsedUlParts.query )
    MU.getUnasContext().lastIpAddress, clientIpPort = self.client_address
    retData = None
    htmlResponseMessage = 'Garbled-No-Message'
    htmlResponseCode = 404
    try:
      logging.info('symbol GET: %s' % self.path)
      if MU.isLogLevelDebug():
          print('symbol GET: %s' % self.path)
      if (len(pPath) > 0): ### GET
        if (pPath[1] == "about"):
          retData = "[[HTML]]" + aboutProxy()
        elif (pPath[1] == "md"):
          pp =('readme' if len(pPath) < 3 else pPath[2]).rstrip().lstrip()
          retData = "[[HTML]]" + MU.mdConverter( ('readme' if len(pp) < 1  else pp).upper())
        elif (pPath[1] == "newOrder"):
          retData = getProc.doEmagOrder("newOrder", pPath[1])
        elif (pPath[1] == "cancelOrder"):
          retData = getProc.doEmagOrder("cancelOrder", pPath[1])
        elif (pPath[1] == "returnOrder"):
          retData = getProc.doEmagOrder("returnOrder", pPath[1])
        elif (pPath[1] == "HU"):
          retData = getProc.doEmagOrder(pPath[2], pPath[3])
        elif (pPath[1] == "RO"):
          retData = getProc.doEmagOrder(pPath[2], pPath[3])
        elif (pPath[1] == "symbol"):
          retData = getProc.doSymbolRequest(self.path)
        elif (pPath[1] == "unas"):
          if MU.isClientIpDisabled(self.client_address):
            raise UnasCommIpDisabledException(client = self.client_address)

          try:
            fb_Conn = FBU.getFbConn()
            unasErrors = []
            retData = getProc.doUnasGetRequest(pPath , unasErrors, qry=queryParams)
            for errItem in unasErrors:
              GBL_ErrorMessages.append(errItem)
          # TODO a communacation errort itt kezelhetnem, esetleg - mert ujrakuldom az egeszet, megjelolve a feldolgozottakat
          # except Exception as e:
          #    logging.error('Unas GET X:%s', e)
          #    errMsg = 'Unexpected(UNAS-Get) error:' + str(e)
          #    MU.errorHandler(errMsg, code=1, level = logging.ERROR)
          #    htmlResponseCode = 500
          #    retData = errMsg
          #    htmlResponseMessage = errMsg
          #    raise Exception(errMsg) 
          finally:
            try:
              FBU.dbClose(fb_Conn)
            except Exception as e:
              logging.error('Firebird-DB-Close error X:%s', e)
          # end try
        elif (pPath[1] == "batch"): # Ki kellene innen torolni - csak a Batch hivhassa?
          if pPath[2] == "orderStatusUnas":
            uts = MU.createTransactionId( UnasTransactionType.ORDERSTATUS )
            prc = next((x["orderStatus"] for x in  MU.BATCH_PROCESSES if   list(filter(lambda key: key == 'orderStatus', x))), {})
            MB.orderStatusUnasProxy(prc)
            retData = "OK"
          elif pPath[2] == "logfiles-rotate":
            uts = MU.createTransactionId( UnasTransactionType.LOGROTATE )
            changeLogFile()
            logging.warning("logger changed/reloaded")
            MU.batchMethodWrapper('logrotate', methodName='archiveLogFiles' )
            retData = "OK"
          elif pPath[2] == "xmlfiles-rotate":
            uts = MU.createTransactionId( UnasTransactionType.XMLROTATE )
            prc = next((x for x in  MU.BATCH_PROCESSES if   list(filter(lambda key: key == 'xmlrotate', x))), {}) or {}
            MU.batchMethodWrapper('xmlrotate', methodName='archiveXmlFiles' )
            retData = "OK"
          elif pPath[2] == "dummy":
            retData = "OK"
          else:
            pass # simply ignore
        elif (pPath[1] == "sql"):
          retData = 'NoData'
          try:
            resp = MU.doMySql(pPath[2:], ())
            retData = ','.join(resp or [])
            retData = "%s" % ('[]' if retData is None else "[" + retData + "]")
            self.send_response(200)
          except Exception as e:
            self.send_response(400)
            retData = '{ "Error": "%s" }' % str(e)
          finally:
            pass # Talan le kellene zarni a session/cursor-t, commit/rollback ???
          self.wfile.write(bytes(retData, 'utf-8'))
          self.wfile.flush()
          return
        elif (pPath[1] == "fbunas"):
          retData = getProc.doUnasFeedback(pPath, self.path, queryParams)
        elif (pPath[1] == "fbemag"):
          retData = getProc.doEmagFeedback(self.path)
          self.send_response(501)
          return
        elif (pPath[1] == 'refresh-config'):
          retData = MU.reReadYaml()
          retData = 'OKJ:{"err":"Something BAD, no config data"}' if retData is None  else f"OKJ:{retData}"
        elif (pPath[1] == "returnEmptyTag"):
          retData = '<{0}></{0}>'.format(pPath[2])
        elif (pPath[1] == "favicon.ico"):
          contentType = ''
          try:
            if MU.FaviconData is None:
              with open('WebContent/dox/favicon.ico', 'rb') as img:
                  MU.FaviconData = img.read()
            self.send_header('Content-type', 'image/x-icon')
            self.end_headers()
            self.wfile.write(MU.FaviconData or b'') # type: ignore
          except:
            self.send_response(404)
            MU.FaviconData = None
          return
        else:
          raise MyProgramFlowWarningException("Bad (GET) request: " + self.path) # @IgnoreException
      else:
          retData = "[[HTML]]" + aboutProxy()
      #
      htmlResponseCode = 200
      htmlResponseMessage = retData
    except MyWarningBreakException as e:
        logging.error("Bad GET Request: %s" % self.path)
        # self.send_header("Content-type", "text/plain")
        # self.end_headers()
        htmlResponseCode = 207
        htmlResponseMessage = str(e) if not hasattr(e, 'message') else e.message
        retData = htmlResponseMessage
        if not isinstance(e, MyProgramFlowWarningException ):
          MU.errorHandler(retData, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.KET), level = logging.WARNING, eDescr=sys.exc_info(), lastFrameStr=SysTB.format_exc())

    except UnasCommErrException as ce:
      ctx = MU.getUnasContext()
      # # msg = f"ERROR - UCh-req:{action}. TS:{ MU.getTS()}\r\n({x.status_code}) -> {x.text}"
      # # SM.sendProxyMail(msg, MUT.AlertMailType(MUT.UnasTransactionType.UNAS_COMM_ERROR), '[UNAS-Comm-Err] Sikertelen UNAS keres ST:%s' % x.status_code )
      # TODO Ha idaig eljutott, akkor mar NAGY baj van! Ezert gondoltam, hog a a commErrCnt figyelembe veszem!
      ctx.commErrCnt = 1 + ctx.commErrCnt
      if ctx.commErrCnt > MU.UNASCOMM_MAXERRCNT:
        ctx.commBlocked = 1
      #
      exception_type, exception_value, traceback = sys.exc_info()
      print("Exception Type:", exception_type)
      print("Exception Value:", exception_value)
      print("Traceback:", traceback)
      #
      logging.error("Fatal Comm-ERROR - GET Request: %s" % self.path)
      logging.error("%s\r\n%s\r\n%s" % (exception_type, exception_value, traceback))
      htmlResponseCode = 500
      htmlResponseMessage = str(ce) if not hasattr(ce, 'message') else ce.message # type: ignore
      retData = htmlResponseMessage
      MU.errorHandler(htmlResponseMessage, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.HAA), level = logging.ERROR, eDescr=sys.exc_info())
      
    except UnasCommIpDisabledException as e:
      htmlResponseCode = 418
      htmlResponseMessage = e.message # f'IP {e.ip} disabled, e:{e.message}' 
      retData = htmlResponseMessage
        
    except Exception as e:
        htmlResponseCode = 500
        htmlResponseMessage = str(e) if not hasattr(e, 'message') else f"type:{type(e)}, message:{e}"
        retData = htmlResponseMessage
        if not isinstance(e, MyProgramFlowErrorException):
          MU.errorHandler(htmlResponseMessage, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E04), level = logging.ERROR, eDescr=sys.exc_info())

    self.send_response(htmlResponseCode)
    if (retData is None):
      self.send_header("Content-type", "text/plain")
      htmlResponseMessage = 'OK'
      retData = 'OK'
    elif (retData == "OK"):
      self.send_header("Content-type", "text/plain")
      htmlResponseMessage = 'OK'
    elif (retData.startswith("OK::")):
      self.send_header("Content-type", "text/plain")
      htmlResponseMessage =retData[4:]
      htmlResponseMessage =retData[4:]
    elif (retData.startswith("OKJ:")):
      self.send_header("Content-type", "application/json")
      htmlResponseMessage =retData[4:]
    elif (retData[0:8] ==  "[[HTML]]"):
      self.send_header("Content-type", "text/html")
      htmlResponseMessage = f"<!DOCTYPE html><html><head><title>Symbol-WebSyx.Proxy Dox.Pg</title></head><body>{retData[8:]}</body></html>"
    elif (retData.startswith(MU.XMLTAG)):
      self.send_header("Content-type", "text/xml")
      htmlResponseMessage = html.unescape(retData)
    elif len(retData) > 0:
      self.send_header("Content-type", "text/plain" if htmlResponseCode > 200 else  "text/xml" )
      htmlResponseMessage =  ('' if htmlResponseCode > 200 else  MU.XMLTAG) + html.unescape(retData)
    else:
      pass
    #
    self.end_headers()
    self.flush_headers()
    self.wfile.write(bytes(htmlResponseMessage, "utf-8")) # type: ignore
    self.wfile.flush()
    if MU.isLogLevelTrace():
      logging.debug("GET Request response: %s",  'NONE' if htmlResponseMessage is None else html.unescape(htmlResponseMessage) )

  def do_POST(self):
    content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
    post_data = self.rfile.read(content_length) # <--- Gets the data itself
    # parsedFields = urllib.parse.parse_qs(str(post_data))
    #self._set_response()
    
    clientReferrer = self.client_address[0]
    MU.getUnasContext().lastIpAddress, clientIpPort = self.client_address

    pPath = self.path.split("/")
    logging.info('symbol POST: %s, len:%i' % (self.path, content_length))
    
    #retData = None
    htmlResponseMessage = 'Garbled-No-Message'
    htmlResponseCode = 404
    try:
      if (len(pPath) > 0): ### POST
        if (pPath[1] == "symbol Noy Udsed Blaaaa"):
          pass # htmlResponseMessage = PPE.doSymbolRequest(self.path, 'dummyData')
        elif (pPath[1] == "proxycontrol"):
          postParams = post_data.decode('utf-8')
          # parsedFields = parse_qs( postParams )
          # cAction =  None if not parsedFields else list(parsedFields.keys())[0]
          # resp = PPU.doProxyControl(cAction, parsedFields[cAction][0], pPath[2:] )
          htmlResponseMessage = PPU.doProxyControl( postParams, pPath[2:] )

        elif (pPath[1] == "unas"):
          if MU.isClientIpDisabled(self.client_address):
                raise UnasCommIpDisabledException(client = self.client_address)

          logging.debug("POST request,\nReferrer: %s\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n"
                ,clientReferrer, str(self.path), str(self.headers), unquote(post_data.decode('utf-8')).replace('+', ' ') )
          postParams = post_data.decode('utf-8')
          parsedFields = parse_qs( postParams )
          try:
            fb_Conn = FBU.getFbConn()
          
            if pPath[2] == 'finalize':
              # lehet torolni a cikk szart
              htmlResponseMessage = PPU.unasPostFinalize(postParams)
            elif pPath[2] == 'bulkupload':
              # UPLOAD valtozoba mentett BULK Products and Customers
              htmlResponseMessage = PPU.unasBulkUpload()
            elif pPath[2] == 'xmlfile':
              htmlResponseMessage = PPU.unasFreeXmlData(pPath[3], pPath[4], postParams)
            elif pPath[2] == 'freexml':
              htmlResponseMessage = PPU.unasFreeXml(pPath[3], postParams)
            elif pPath[2] == 'symbolxml':
              htmlResponseMessage = PPU.unasSymbolXml(pPath[3], postParams)
            elif postParams[0] == '\ufeff' and postParams[1:7] == '<?xml ':
              htmlResponseMessage = PPU.doUnasRequest(pPath[2],postParams[1:] , errors=GBL_ErrorMessages )
            elif postParams.startswith('<?xml '):
              htmlResponseMessage = PPU.doUnasRequest(pPath[2],postParams, None if len(pPath) < 4 else pPath[3], errors=GBL_ErrorMessages)
            elif len(parsedFields) == 0:
              htmlResponseMessage = 'No POST DATA!?'
            elif 'xmldata' == list(parsedFields.keys())[0]: # type: ignore
              xmlData = parsedFields['xmldata'][0]
              htmlResponseMessage = PPU.doUnasRequest(pPath[2], xmlData, 17, errors=GBL_ErrorMessages)
            else:
              cFld = list(parsedFields.keys())[0] # type: ignore
              xmlData = parsedFields[cFld][0]
              htmlResponseMessage = PPU.doUnasRequest(pPath[2], xmlData, cFld, errors=GBL_ErrorMessages)
          # Talan itt mar nem kell az exceptionoket figyelnem???
          ###   # raise  WalueError( str(e) if not hasattr(e, 'message') else e.message ) # type: ignore
          finally:
            try:
              FBU.dbClose(fb_Conn)
            except Exception as e:
              logging.error('DB-Close error X:%s', e)
          # end try UnasPostProcess
        elif (pPath[1] == "emag Not Used Blaaaa"):
          pass # htmlResponseMessage = PPE.doEmagRequest(self.path, 'DummyData')
        elif (pPath[1] == "synclog Not Used Blaaaa"):
          #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n"
          #      ,str(self.path), str(self.headers), post_data.decode('utf-8'))
          postParams = post_data.decode('utf-8')
          parsedFields = parse_qs( postParams )
          logging.debug(parsedFields['xmldata'][0])
          htmlResponseMessage = 'OK'
        else:
          GBL_ErrorMessages.append( "Unhandled (POST) request: " + self.path )
          raise MyProgramFlowWarningException("Bad (POST) request: " + self.path)
        
      htmlResponseCode = 200 # Everything is All Right?
    #########################################
    except MyWarningBreakException as e:
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        htmlResponseCode = 204
        htmlResponseMessage = str(e) if not hasattr(e, 'message') else e.message
        retData = htmlResponseMessage
        if not isinstance(e, MyProgramFlowWarningException ):
          MU.errorHandler(retData, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E05), level = logging.WARNING, eDescr=sys.exc_info(), lastFrameStr=SysTB.format_exc())

  # TODO setXXX error 400 eseten ki kell elemzni a hibat es ha lehet, akkor ujra kuldeni a hibas tetel nelkul
  # TODO a communacation errort itt kezelhetnem, esetleg - mert ujrakuldom az egeszet, megjelolve a feldolgozottakat
    except UnasCommErrException as ce:
      ctx = MU.getUnasContext()
      # # msg = f"ERROR - UCh-req:{action}. TS:{ MU.getTS()}\r\n({x.status_code}) -> {x.text}"
      # # SM.sendProxyMail(msg, MUT.AlertMailType(MUT.UnasTransactionType.UNAS_COMM_ERROR), '[UNAS-Comm-Err] Sikertelen UNAS keres ST:%s' % x.status_code )
      # TODO Ha idaig eljutott, akkor mar NAGY baj van! Ezert gondoltam, hog a a commErrCnt figyelembe veszem!
      ctx.commErrCnt = 1 + ctx.commErrCnt
      if ctx.commErrCnt > MU.UNASCOMM_MAXERRCNT:
        ctx.commBlocked = 1
      #
      exception_type, exception_value, traceback = sys.exc_info()
      print("Exception Type:", exception_type)
      print("Exception Value:", exception_value)
      print("Traceback:", traceback)
      #
      logging.error("Fatal Comm-ERROR - GET Request: %s\r\n%s\r\n%s\r\n%s" % (self.path, exception_type, exception_value, traceback))
      htmlResponseCode = 500
      htmlResponseMessage = str(ce) if not hasattr(ce, 'message') else ce.message # type: ignore
      MU.errorHandler(htmlResponseMessage, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E06), level = logging.ERROR, eDescr=sys.exc_info())
      
    except UnasCommIpDisabledException as e:
      htmlResponseCode = 418
      htmlResponseMessage = 'Client IP"%s disabled (%d)' % self.client_address
        
    except Exception as e:
        logging.error("Fatal ERROR-POST Referrer: %s, Request: %s" , clientReferrer, self.path)
        htmlResponseCode = 500
        htmlResponseMessage = str(e) #if not hasattr(e, 'message') else e.message
        if not isinstance(e, MyProgramFlowErrorException):
          MU.errorHandler(htmlResponseMessage, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E07), level = logging.ERROR, eDescr=sys.exc_info())
    #########################################

    self.send_response(htmlResponseCode)
    #
    if htmlResponseMessage is not None and len(htmlResponseMessage) > 0:
      if htmlResponseMessage.startswith("OKJ:"):
        self.send_header("Content-Type", "application/json")
        htmlResponseMessage = htmlResponseMessage[4:]
      elif (htmlResponseMessage.startswith("<?xml ")):
        self.send_header("Content-type", "application/xml")
      else:
        self.send_header("Content-type", "text/plain")
      #
      self.end_headers()
      self.flush_headers()
      self.wfile.write(bytes(htmlResponseMessage, "utf-8"))
    else:
      self.send_header("Content-type", "text/plain")
      self.end_headers()
      self.wfile.write(bytes('Error(unhandled)' if htmlResponseCode > 200 else 'OK', "utf-8"))
    #
    self.wfile.flush()
    '''
      ########################################################################################################################
      ### retMsg = 'OK' if retMessage is None else retMessage
      ### if retMsg != 'OK' and False if retMsg is None else len(retMsg) > 0:
      ###    if (retMsg.startswith("OKJ:")):
      ###       self.send_header("Content-Type", "application/json")
      ###       self.end_headers()
      ###       self.flush_headers()
      ###       self.wfile.write(bytes(retMsg[4:], "utf-8"))
      ###    elif (retMsg.startswith("<?xml ")):
      ###       self.send_header("Content-type", "application/xml")
      ###       self.end_headers()
      ###       self.flush_headers()
      ###       self.wfile.write(bytes(retMsg, "utf-8"))
      ###    else:
      ###       self.send_header("Content-type", "text/plain")
      ###       self.end_headers()
      ###       self.flush_headers()
      ###       self.wfile.write(bytes(retMsg, "utf-8"))
      ### elif retMsg == 'OK' or True if retMsg is None else len(retMsg.strip()) == 0:
      ###   if len(GBL_ErrorMessages) > 0:
      ###     self.send_header("Content-type", "text/plain")
      ###     self.end_headers()
      ###     self.flush_headers()
      ###     self.wfile.write(bytes(str('<Errors>'), "utf-8"))
      ###     for errItm in GBL_ErrorMessages:
      ###       self.wfile.write(bytes(str(errItm), "utf-8"))
      ###     self.wfile.write(bytes(str('</Errors>'), "utf-8"))
      ###     GBL_ErrorMessages.clear()
      ###   elif len('' if retMsg is None else retMsg) >0:
      ###     self.end_headers()
      ###     self.flush_headers()
      ###     self.wfile.write(bytes(retMsg, "utf-8"))
      ###   else:
      ###     self.end_headers()
      ###     self.flush_headers()
      ### self.wfile.flush()
      # self.wfile.write(bytes("<html><head><title>https://testserver.com</title></head>", "utf-8"))
      # self.wfile.write(bytes("<p>POST Request: %s</p>" % self.path, "utf-8"))
      # self.wfile.write(bytes("<body>", "utf-8"))
      # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
      # self.wfile.write(bytes("</body></html>", "utf-8"))
    '''
    if MU.isLogLevelTrace():
      logging.info("POST Ref: %s, uri: %s, resp: %s" , clientReferrer, self.path, 'NEmpty-Response' if htmlResponseMessage is None else htmlResponseMessage )

  def do_PUT(self): # the do_GET method is inherited from BaseHTTPRequestHandler
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes("<html><head><title>https://testserver.com</title></head>", "utf-8"))
    self.wfile.write(bytes("<p>PUT Request: %s</p>" % self.path, "utf-8"))
    self.wfile.write(bytes("<body>", "utf-8"))
    self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
    self.wfile.write(bytes("</body></html>", "utf-8"))

  def do_DELETE(self): # the do_GET method is inherited from BaseHTTPRequestHandler
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes("<html><head><title>https://testserver.com</title></head>", "utf-8"))
    self.wfile.write(bytes("<p>DELETE Request: %s</p>" % self.path, "utf-8"))
    self.wfile.write(bytes("<body>", "utf-8"))
    self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
    self.wfile.write(bytes("</body></html>", "utf-8"))

  def do_OPTION(self): # the do_GET method is inherited from BaseHTTPRequestHandler
    parsedUlParts = urlparse(self.path)
    pPath = parsedUlParts.path.split("/")
    queryParams = parse_qs( parsedUlParts.query )
    responseCode = 200
    contentType = 'text/plain'
    response = 'Done'

    if parsedUlParts.path == '/stopcontrol':
      try:
        if controlWebThread is not None:
          if MySocket.myControlWebServer is not None:
            MySocket.myControlWebServer.shutdown()
          #threading.sleep(2)
          #controlWebThread.join()
          logging.info('controlWebThread - stopped? %s', MySocket.myControlWebServer )
        #
      except Exception as e:
        responseCode = 400
        response = str(e) #if not e.hasattr('message') else e.message
    elif parsedUlParts.path == '/startcontrol':
      try:
        startControlWebThread()
      except Exception as e:
        responseCode = 400
        response = str(e) #if not e.hasattr('message') else e.message
    elif parsedUlParts.path == '/stopsocket':
      try:
        if controlSocketThread is not None:
          logging.error('Beragadt, Ki kellene loni')
          if MySocket.mySocketServer is not None:
            MySocket.mySocketServer.shutdown()
        #
      except Exception as e:
        responseCode = 400
        response = str(e) # if not e.hasattr('message') else e.message
    elif parsedUlParts.path == '/startsocket':
      try:
        startSocketThread()
      except Exception as e:
        responseCode = 400
        response = str(e) # if not e.hasattr('message') else e.message
    else:
      responseCode = 200
      contentType = "text/html"
      response = f"<html><head><title>https://testserver.com</title></head><body><p>OPTION Request: {self.path}</p></body></html>"

    self.send_response(responseCode)
    self.send_header("Content-type", contentType)
    self.end_headers()
    self.wfile.write(bytes(response,'utf-8'))
    self.wfile.flush()

def new_controlSocketClient(srv):
  srv.send_message_to_all("Hey all, a new client has joined us")

YAML_CONFIG_FILE = 'web6proxy.yaml'

controlWebThread:typing.Optional[threading.Thread] = None
def startControlWebThread():
    global controlWebThread
    try:
      controlWebThread = threading.Thread( target = MySocket.setWebServer, name = "controlWeb", args=(MU.WEB_CONTROL_HOST, MU.WEB_CONTROL_PORT ), daemon=True )
      controlWebThread.start()
      MSG_serverStarting.append(f'WEB-ControlServer started on => {MU.WEB_CONTROL_HOST}:{MU.WEB_CONTROL_PORT}')
      logging.info(f'WEB-ControlServer started on => {MU.WEB_CONTROL_HOST}:{MU.WEB_CONTROL_PORT}')
      print(f'WEB-ControlServer started on => {MU.WEB_CONTROL_HOST}:{MU.WEB_CONTROL_PORT}')
    except Exception as x:
      logging.info('Websocket Server closing:', x)

controlSocketThread:typing.Optional[threading.Thread] = None
def startSocketThread():
    global controlSocketThread
    try:
      controlSocketThread = threading.Thread( target = MySocket.setSocketServer, name = "controlSocket", args=(MU.SOCKET_CONTROL_HOST, MU.SOCKET_CONTROL_PORT ), daemon=True )
      controlSocketThread.start()
      logging.info(f'socket Server starting {MU.SOCKET_CONTROL_HOST}:{MU.SOCKET_CONTROL_PORT}')
      print(f'Socket Server started on => {MU.SOCKET_CONTROL_HOST}:{MU.SOCKET_CONTROL_PORT}')
      MSG_serverStarting.append(f'TCP-SocketServer started on => {MU.SOCKET_CONTROL_HOST}:{MU.SOCKET_CONTROL_PORT}')
    except Exception as x:
      logging.info('socket Server closing:', x)

batchThread:typing.Optional[threading.Thread] = None
def startBatchThread():
    global batchThread
    try:
      batchThread = threading.Thread( target = MB.startService, name = "controlWeb", args=(MU.WEB_CONTROL_HOST, MU.WEB_CONTROL_PORT ), daemon=True )
      batchThread.start()
      MSG_serverStarting.append(f'BATCH-Server started (inline)')
      logging.info('BATCH-Server started (inline)')
      print('BATCH-Server started (inline)')
    except Exception as x:
      logging.info('BATCH Server closing:', x)


def getGlobalLogLevel():
  if MU.LOGLEVEL[0].upper() == 'I':
      logLevel = logging.INFO
  elif MU.LOGLEVEL[0].upper() == 'W':
      logLevel = logging.WARNING
  elif MU.LOGLEVEL[0].upper() == 'E':
      logLevel = logging.ERROR
  else:
      logLevel = logging.DEBUG
  return logLevel


import MyLogger
def changeLogFile():

  myLogger = MU.getLogger()
  logFileName = 'syxProxy{0}.log'.format( '' if MU.serverPort == 3301 else '_'+str(MU.serverPort))
  logLevel = getGlobalLogLevel()
  if logger is None:
    myLogger = MyLogger(logFileName, level='debug')
    # logging.basicConfig(filename=,level=logLevel,format='%(asctime)s %(levelname)s %(name)s %(message)s')
    # logger=logging.getLogger('w6p')
    # logging.info("logger created")
  #
  # close filehandles
  for handler in myLogger.handlers[:]:  # make a copy of the list
    handler.close()
    myLogger.removeHandler(handler)    
    # logger.handlers[0].stream.close()
    # logger.removeHandler(logger.handlers[0])
    #
  logrotate(logFileName)
  # reopen file
  file_handler = logging.FileHandler(logFileName)
  file_handler.setLevel(logLevel)
  formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s:%(lineno)d [%(funcName)s]: %(message)s")
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)  
  MU.setLogger(logger)
  return logger

if __name__ == "__main__":
  configPath = YAML_CONFIG_FILE
  if (len(sys.argv)>1):
    configPath = sys.argv[1]
  MU.readYaml(configPath)

  GBL_ErrorMessages = []

  logger=changeLogFile()
  ## 
  ## logLevel = getGlobalLogLevel()
  ## logFileName = 'syxProxy{0}.log'.format( '' if MU.serverPort == 3301 else '_'+str(MU.serverPort))
  ## logrotate(logFileName)
  ## logging.basicConfig(filename=logFileName,level=logLevel,format='%(asctime)s %(levelname)s %(name)s %(message)s')
  ## logger=logging.getLogger(__name__) ## 
  
  MSG_serverStarting = []
  MSG_serverStarting.append(f'Server starting on => {MU.hostName}:{MU.serverPort}')
  #
  controlSocketThread:typing.Optional[threading.Thread] = None
  if MU.SOCKET_CONTROL_ENABLED:
    startSocketThread()

  if MU.WEB_CONTROL_ENABLED:
    startControlWebThread()

  if MU.BATCH_INLINE_ENABLED:
    MB.startBatchService()

  uts = MU.createTransactionId( UnasTransactionType.STARTPROXY )
  # TODO DB Connect TEST-eket kellene vegezni es ha nincs, akkor leallni vagy varni 5 percet 3x ujraprobalni es utana fatalExit
  logger.info( 'Test FB connect; Customer table rowCount: %s' % FBU.testDbConnect() )
  FBU.insertDummyCustomer()
  FBU.dbClose()

  MU.mySqlCheckConnection()
  MU.loadUnasProxyContext()
  if not MU.JOETESTCustomer:
    MU.checkCacheState(force=True)
    # MU.UnasOrderList.clear()

  if MU.isLogLevelWarn():
      print("Server started http://%s:%s, PID: %d" % (MU.hostName, MU.serverPort, os.getpid()))  #Server starts
      SM.sendProxyMail('\r\n'.join( MSG_serverStarting ), AlertMailType( UnasTransactionType.STARTPROXY, code=ProxyErrCode.INFO), 'starting')

  try:
      webServer = HTTPServer((MU.hostName, MU.serverPort), MyServer)
      webServer.serve_forever() #@IgnoreException
  except KeyboardInterrupt:
      # FBU.dbClose()
      logging.info('Server closing...')

  if controlSocketThread is not None:
      MySocket.mySocketWebServer.shutdown()
      controlSocketThread.join()
    
  if controlWebThread is not None and MySocket.myControlWebServer is not None:
      MySocket.myControlWebServer.shutdown()
      controlWebThread.join()

  MU.saveUnasProxyContext()
  webServer.server_close()  #Executes when you hit a keyboard interrupt, closing the server
  if MU.isLogLevelWarn():
        print("Server stopped.")
        SM.sendProxyMail("Server stopped", AlertMailType( UnasTransactionType.STARTPROXY, code=ProxyErrCode.INFO), 'stopped')
