#!/usr/bin/python3

import logging
import html
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote, parse_qs
import MyUtils as MU
import MySmtpClient as SM
import FdbUtils as FBU
import MySqlService as sqlSrv
# import urllib
#
import GetProcessor as getProc
import PostProcessorUNAS as PPU
import PostProcessorEMAG as PPE
import json
global GBL_ErrorMessages
GBL_ErrorMessages = []
 
def aboutProxy():
  return MU.mdConverter( 'ABOUT' )

class MyServer(BaseHTTPRequestHandler):
  def do_GET(self): # the do_GET method is inherited from BaseHTTPRequestHandler
    global GBL_ErrorMessages
    pPath = self.path.split("/")
    parsedUlParts = urlparse(self.path)
    pPath = parsedUlParts.path.split("/")
    queryParams = parse_qs( parsedUlParts.query )
    retData = None
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
          try:
            fb_Conn = FBU.getFbConn()
            unasErrors = []
            retData = getProc.doUnasGetRequest(pPath , unasErrors)
            for errItem in unasErrors:
              GBL_ErrorMessages.append(errItem)
          except Exception as e:
            logging.error('Unas GET X:%s', e)
            GBL_ErrorMessages.append( 'Unexpected(UNAS) error:' + str(e))
          finally:
            try:
              FBU.dbClose(fb_Conn)
            except Exception as e:
              logging.error('Firebird-DB-Close error X:%s', e)
          # end try
        elif (pPath[1] == "batch"):
          #logging.warning('Batch ccommad:%s not implementes YET! path:%s', pPath[2], pPath)
          pass
        elif (pPath[1] == "sql"):
          srv = sqlSrv.MySqlService()
          try:
            resp = srv.doSql(pPath[2:])
            retData = ','.join(resp)
            retData = "OKJ:%s" % ('[]' if retData is None else "[" + retData + "]")
          except Exception as e:
            return 'OKJ:{ "Error": "%s" }' % str(e)
          finally:
            try:
              srv.close()
            except Exception as e:
              logging.error('MySQL-DB-Close error X:%s', e)
            # end try

        elif (pPath[1] == "fbunas"):
          retData = getProc.doUnasFeedback(pPath, self.path)
        elif (pPath[1] == "fbemag"):
          retData = getProc.doEmagFeedback(self.path)
          self.send_response(501)
          return
        elif (pPath[1] == 'refresh-config'):
          retData = MU.reReadYaml()
          retData = None if retData is None  else f"OKJ:{retData}"
        elif (pPath[1] == "returnEmptyTag"):
          retData = '<{0}></{0}>'.format(pPath[2])
        elif (pPath[1] == "favicon.ico"):
          self.send_response(404)
          return
        else:
          raise ValueError("Bad (GET) request: " + self.path)
      else:
          retData = "[[HTML]]" + aboutProxy()
        
    except ValueError as e:
        logging.error("Bad GET Request: %s" % self.path)
        self.send_response(200) # @20240614  NEZDMEG!
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        errMsg = str(e) if not hasattr(e, 'message') else e.message # type: ignore
        logging.error(errMsg)
        GBL_ErrorMessages.append( errMsg ) # self.wfile.write(bytes("Raised ValueErr:%s" % errMsg, "utf-8"))

    except Exception as e:
        logging.error("Fatal ERROR - GET Request: %s" % self.path)
        errMsg = str(e) if not hasattr(e, 'message') else e.message # type: ignore
        logging.error(errMsg)
        self.send_response(200) # @20240614  NEZDMEG!
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        GBL_ErrorMessages.append( errMsg ) # self.wfile.write(bytes("FATAL-Excptn:%s" % errMsg, "utf-8"))

    if (retData == None):
      self.send_response(204)
      self.end_headers()
      self.flush_headers()
      retData = ''
    else:
      self.send_response(200)
    #
    # self.wfile.write(bytes("<html><head><title>https://testserver.com</title></head>", "utf-8"))
    # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
    # self.wfile.write(bytes("<ody>", "utf-8"))
    # self.wfile.write(bytes("<p>This is the DATA</p>", "utf-8"))
    if (retData == "OK"):
      self.send_header("Content-type", "text/plain")
      self.end_headers()
      self.flush_headers()
      #self.wfile.flush()
    elif (retData.startswith("OK::")):
      self.send_header("Content-type", "text/plain")
      self.end_headers()
      self.flush_headers()
      self.wfile.write(bytes(retData[4:], "utf-8"))
      #self.wfile.flush()
    elif (retData.startswith("OKJ:")):
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.flush_headers()
      self.wfile.write(bytes(retData[4:], "utf-8"))
      #self.wfile.flush()
    elif (retData.startswith("@@errors@@")):
      self.send_header("Content-type", "text/xml")
      self.end_headers()
      self.flush_headers()
      if len(GBL_ErrorMessages) > 0:
        self.wfile.write(bytes( MU.XMLTAG + "<Errors>", "utf-8"))
        for errorItm in GBL_ErrorMessages:
          self.wfile.write(bytes( str(errorItm), "utf-8"))
          self.wfile.write(bytes( "\r\n", "utf-8"))
        self.wfile.write(bytes( "</Errors>", "utf-8"))
      else:
        self.wfile.write(bytes( "<Errors />", "utf-8"))
      GBL_ErrorMessages.clear()
    elif (retData[0:8] ==  "[[HTML]]"):
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.flush_headers()
      self.wfile.write(bytes('<!DOCTYPE html><html><head><title>Symbol - WebSyx Proxy Doc.Pages</title></head><body>', "utf-8"))
      self.wfile.write(bytes(retData[8:], "utf-8"))
      self.wfile.write(bytes('</body></html>', "utf-8"))
    elif (retData.startswith(MU.XMLTAG)):
      self.send_header("Content-type", "text/xml")
      self.end_headers()
      self.flush_headers()
      self.wfile.write(bytes( html.unescape(retData), "utf-8"))
    elif len(retData) > 0:
      self.send_header("Content-type", "text/xml")
      self.end_headers()
      self.flush_headers()
      self.wfile.write(bytes( MU.XMLTAG + html.unescape(retData), "utf-8"))
    else:
      pass
    #
    self.wfile.flush()
    logging.debug("GET Request response: %s",  'NONE' if retData is None else html.unescape(retData) )


  def do_POST(self):
    content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
    post_data = self.rfile.read(content_length) # <--- Gets the data itself
    # parsedFields = urllib.parse.parse_qs(str(post_data))
    #self._set_response()
    
    clientReferrer = self.client_address[0]
    pPath = self.path.split("/")
    retMessage = None
    logging.info('symbol POST: %s, len:%i' % (self.path, content_length))
    if MU.isLogLevelDebug():
      print('symbol POST: %s, len:%i' % (self.path, content_length))
    
    try:
      if (len(pPath) > 0): ### POST
        if (pPath[1] == "symbol"):
          retMessage = PPE.doSymbolRequest(self.path, 'dummyData')
        elif (pPath[1] == "proxycontrol"):
          postParams = post_data.decode('utf-8')
          # parsedFields = parse_qs( postParams )
          # cAction =  None if not parsedFields else list(parsedFields.keys())[0]
          # resp = PPU.doProxyControl(cAction, parsedFields[cAction][0], pPath[2:] )
          retMessage = PPU.doProxyControl( postParams, pPath[2:] )

        elif (pPath[1] == "unas"):
          logging.debug("POST request,\nReferrer: %s\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n"
                ,clientReferrer, str(self.path), str(self.headers), unquote(post_data.decode('utf-8')).replace('+', ' ') )
          postParams = post_data.decode('utf-8')
          parsedFields = parse_qs( postParams )
          try:
            fb_Conn = FBU.getFbConn()
          
            if pPath[2] == 'finalize':
              # lehet torolni a cikk szart
              retMessage = PPU.unasPostFinalize(postParams)
            elif pPath[2] == 'bulkupload':
              # UPLOAD valtozoba mentett BULK Products and Customers
              retMessage = PPU.unasBulkUpload()
            elif pPath[2] == 'freexml':
              retMessage = PPU.unasFreeXml(pPath[3], postParams)
            elif pPath[2] == 'symbolxml':
              retMessage = PPU.unasSymbolXml(pPath[3], postParams)
            elif len(parsedFields) == 0:
              retMessage = 'OK'
            elif postParams[0] == '\ufeff' and postParams[1:7] == '<?xml ':
              retMessage = PPU.doUnasRequest(pPath[2],postParams[1:] , errors=GBL_ErrorMessages )
            elif postParams.startswith('<?xml '):
              retMessage = PPU.doUnasRequest(pPath[2],postParams, None if len(pPath) < 4 else pPath[3], errors=GBL_ErrorMessages)
            elif 'xmldata' == list(parsedFields.keys())[0]: # type: ignore
              xmlData = parsedFields['xmldata'][0]
              retMessage = PPU.doUnasRequest(pPath[2], xmlData, 17, errors=GBL_ErrorMessages)
            else:
              cFld = list(parsedFields.keys())[0] # type: ignore
              xmlData = parsedFields[cFld][0]
              retMessage = PPU.doUnasRequest(pPath[2], xmlData, cFld, errors=GBL_ErrorMessages)

          except Exception as e:
            logging.error('Unas POST FATAL-X:%s', e)
            GBL_ErrorMessages.append( "FATAL (POST): " + self.path )
            GBL_ErrorMessages.append( "FATAL Excptn: " + str(e) )
            # raise  ValueError( str(e) if not hasattr(e, 'message') else e.message ) # type: ignore
          finally:
            try:
              FBU.dbClose(fb_Conn)
            except Exception as e:
              logging.error('DB-Close error X:%s', e)
          # end try UnasPostProcess
        elif (pPath[1] == "emag"):
          retData = PPE.doEmagRequest(self.path, 'DummyData')
          retMessage = 'OK'
        elif (pPath[1] == "synclog"):
          #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n"
          #      ,str(self.path), str(self.headers), post_data.decode('utf-8'))
          postParams = post_data.decode('utf-8')
          parsedFields = parse_qs( postParams )
          retMessage = PPE.symbolSynclog(parsedFields['xmldata'][0])
        elif (pPath[1] == "favicon.ico"):
          self.send_response(404)
          return
        else:
          GBL_ErrorMessages.append( "Unhandled (POST) request: " + self.path )
          #raise ValueError("Bad (POST) request: " + self.path)
        
    except ValueError as e:
        logging.error("ValueError-POST Referrer: %s, Request: %s" , clientReferrer, self.path)
        errMsg = str(e) if not hasattr(e, 'message') else e.message # type: ignore
        logging.error(errMsg)
        GBL_ErrorMessages.append('Raised ValueError:' + str(errMsg))
        retMessage = ''
        # self.send_response(200)
        # self.send_header("Content-type", "text/plain")
        # self.end_headers()
        # self.wfile.write(bytes("Err:%s" % errMsg, "utf-8"))
        # self.wfile.flush()
        # return

    self.send_response(200)
    # logging.error("retMessage type:%s", type(retMessage))
    retMsg = 'OK' if retMessage is None else retMessage
    if retMsg != 'OK' and False if retMsg is None else len(retMsg) > 0:
       if (retMsg.startswith("OKJ:")):
          self.send_header("Content-Type", "application/json")
          self.end_headers()
          self.flush_headers()
          self.wfile.write(bytes(retMsg[4:], "utf-8"))
       elif (retMsg.startswith("<?xml ")):
          self.send_header("Content-type", "application/xml")
          self.end_headers()
          self.flush_headers()
          self.wfile.write(bytes(retMsg, "utf-8"))
       else:
          self.send_header("Content-type", "text/plain")
          self.end_headers()
          self.flush_headers()
          self.wfile.write(bytes(retMsg, "utf-8"))
    elif retMsg == 'OK' or True if retMsg is None else len(retMsg.strip()) == 0:
      if len(GBL_ErrorMessages) > 0:
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.flush_headers()
        self.wfile.write(bytes(str('<Errors>'), "utf-8"))
        for errItm in GBL_ErrorMessages:
          self.wfile.write(bytes(str(errItm), "utf-8"))
        self.wfile.write(bytes(str('</Errors>'), "utf-8"))
        GBL_ErrorMessages.clear()
      elif len('' if retMsg is None else retMsg) >0:
        self.end_headers()
        self.flush_headers()
        self.wfile.write(bytes(retMsg, "utf-8"))
      else:
        self.end_headers()
        self.flush_headers()
    self.wfile.flush()
    # self.wfile.write(bytes("<html><head><title>https://testserver.com</title></head>", "utf-8"))
    # self.wfile.write(bytes("<p>POST Request: %s</p>" % self.path, "utf-8"))
    # self.wfile.write(bytes("<body>", "utf-8"))
    # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
    # self.wfile.write(bytes("</body></html>", "utf-8"))
    logging.info("POST Ref: %s, uri: %s, resp: %s" , clientReferrer, self.path, retMessage)

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
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes("<html><head><title>https://testserver.com</title></head>", "utf-8"))
    self.wfile.write(bytes("<p>OPTION Request: %s</p>" % self.path, "utf-8"))
    self.wfile.write(bytes("<body>", "utf-8"))
    self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
    self.wfile.write(bytes("</body></html>", "utf-8"))


YAML_CONFIG_FILE = 'web6proxy.yaml'

if __name__ == "__main__":
  configPath = YAML_CONFIG_FILE
  if (len(sys.argv)>1):
    configPath = sys.argv[1]
  MU.readYaml(configPath)

  GBL_ErrorMessages = []
  if MU.LOGLEVEL[0].upper() == 'I':
      logLevel = logging.INFO
  elif MU.LOGLEVEL[0].upper() == 'W':
      logLevel = logging.WARNING
  elif MU.LOGLEVEL[0].upper() == 'E':
      logLevel = logging.ERROR
  else:
      logLevel = logging.DEBUG
      
  logging.basicConfig(filename='syxProxy%s.log' % '' if MU.serverPort == 3301 else str(MU.serverPort),level=logLevel,format='%(asctime)s %(levelname)s %(name)s %(message)s')
  logger=logging.getLogger(__name__)

  logger.info( 'Test FB connect; Customer table rowCount: %s' % FBU.testDbConnect() )
  FBU.insertDummyCustomer()
  webServer = HTTPServer((MU.hostName, MU.serverPort), MyServer)
  if MU.isLogLevelWarn():
      print("Server started http://%s:%s" % (MU.hostName, MU.serverPort))  #Server starts
      SM.sendAlertMail(f'Server starting on => {MU.hostName}:{MU.serverPort}')
  #
  try:
      webServer.serve_forever()
  except KeyboardInterrupt:
      FBU.dbClose
      logging.info('Server closing...')

  FBU.dbClose
  webServer.server_close()  #Executes when you hit a keyboard interrupt, closing the server
  if MU.isLogLevelWarn():
        print("Server stopped.")
        SM.sendAlertMail("Server stopped")
