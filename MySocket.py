import logging
import socketserver
import threading
import typing
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, unquote, urlparse

import MyProxyControl as MPC
import MyUtils as MU
import MyUtilsTypes as MUT

# from websocket_server import WebsocketServer
# from simple_websocket_server import WebSocket, WebSocketServer

class MyControlWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsedUlParts = urlparse(self.path)
            pPath = parsedUlParts.path.split("/")
            queryParams = parse_qs( parsedUlParts.query )
            contentType = 'text/html'
            htmlResponseCode = 200
            htmlResponseMessage = None
            binaryRead = False
            if ['',''] == pPath:
                 pPath[1] = "index.html"
                #
            if 'favicon.ico' == pPath[1]:
                 try:
                    with open('WebContent/dox/favicon.ico', 'rb') as img:
                        htmlResponseMessage = img.read()
                    contentType = 'image/x-icon'
                 except:
                    self.send_response(404)
                    htmlResponseMessage = ''
                    return
            elif 'qry' == pPath[1]:
                htmlResponseCode = 200
                contentType = "application/json"
                htmlResponseMessage = MPC.doWebControlQuery(pPath[2:], queryParams)
            elif 'ctrl' == pPath[1]:
                htmlResponseCode = 200
                htmlResponseMessage, content_type = MPC.doWebControlCommand(pPath[2:], queryParams)
                contentType = content_type or "application/json"
            elif 'tpl' == pPath[1]:
                contentType = 'text/html'
                htmlResponseMessage = MPC.doWebPageTemplate(pPath[2:], queryParams)
            elif 'md' == pPath[1]:
                # contentType = 'text/x-markdown'
                contentType = 'text/html'
                _doc = MPC.doWebPageMD(pPath[2:], queryParams)
                htmlResponseMessage = f'<html><head><meta charset="UTF-8"></head><body>{_doc}</body></html>'
            elif 'ffmd' == pPath[1]:
                # contentType = 'text/x-markdown'
                contentType = 'text/markdown'
                _doc = MPC.doWebPageFile(pPath[2:], queryParams, binaryRead=False )
                htmlResponseMessage = bytes( _doc, 'cp1252', errors='replace') 
            elif 'js' == pPath[1]:
                htmlResponseMessage = MPC.doWebPageJS(pPath[2:], queryParams)
                contentType = "application/javascript"
                htmlResponseCode = 200
            elif 'html' == pPath[1]: # Ez nar ELSE ag , csak kiterjesztes szerint mas a mediaType
                htmlResponseMessage = MPC.doWebPageHTML(pPath[2:], queryParams)
                contentType = "text/html"
                htmlResponseCode = 200
            else:
                if '.json' == pPath[-1][:-5].lower():
                    contentType = 'application/json'
                elif '.xml' == pPath[-1][:-4].lower():
                    contentType = 'text/xml'
                elif '-1252.md' == pPath[-1][-8:].lower():
                    contentType = 'text/markdown'
                    binaryRead = True
                elif '.md' == pPath[-1][-3:].lower():
                    contentType = 'text/markdown'
                elif '.js' == pPath[-1][-3:].lower():
                    contentType = 'text/javascript'
                elif pPath[-1][-4:].lower() in ['.jpg', 'jpeg'] :
                    contentType = 'image/jpeg'
                    binaryRead = True
                elif '.ico' == pPath[-1][-4:].lower():
                    contentType = 'image/x-icon'
                    binaryRead = True
                elif '.png' == pPath[-1][-4:].lower():
                    contentType = 'image/png'
                    binaryRead = True
                elif pPath[-1][-4:].lower() in ['.jpg', 'jpeg'] :
                    contentType = 'image/jpeg'
                    binaryRead = True
                elif '.html' == pPath[-1][-5:].lower():
                    contentType = 'text/html'
                else:
                    contentType = 'text/plain'
                htmlResponseMessage = MPC.doWebPageFile(pPath, queryParams, binaryRead )
                htmlResponseCode = 200

        except Exception as e:
            htmlResponseMessage = str(e)
            htmlResponseCode = 400
        #        
        self.send_response(htmlResponseCode)
        self.send_header("Content-type", contentType )
        self.end_headers()
        if htmlResponseMessage is not None:
            respBytes = htmlResponseMessage if isinstance(htmlResponseMessage, bytes) else bytes(str(htmlResponseMessage),'utf-8')
            self.wfile.write( respBytes )
            self.wfile.flush()
        
    def do_POST(self):
        # Handle GET requests here
        pass
    def do_PUT(self):
        # Handle GET requests here
        pass
    def do_DELETE(self):
        # Handle GET requests here
        pass
    def do_OPTION(self):
        # Handle GET requests here
        pass
    def __init__(self,  *args, **kwargs):
        super(MyControlWebServer, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
class MyTCPHandler(socketserver.BaseRequestHandler):

    log: logging.Logger
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        pieces = [b'']
        total = 0
        while b'\n' not in pieces[-1] and total < 10_000:
            pieces.append(self.request.recv(2000))
            total += len(pieces[-1])
        self.data = b''.join(pieces)
        print(f"Received from {self.client_address[0]}:")
        receivedData = self.data.decode("utf-8")
        response = MU.processControl(receivedData)
        # just send back the same data, but upper-cased
        self.request.sendall(bytes(response, 'utf-8'))
        # after we return, the socket will be closed.

mySocketServer: typing.Optional[socketserver.TCPServer] = None
def setSocketServer(host, port):
    # Create the server, binding to localhost on port 9999
    try:
        #socketserver.TCPServer.allow_reuse_address = True
        mySocketServer = socketserver.TCPServer((host,port), MyTCPHandler)
        mySocketServer.serve_forever()
        print('Stopping socket server')
        mySocketServer.server_close()
    except MUT.ControlProcessSocketExit:
        logging.info("control Process Socketsever Thread exiting")
    except Exception:
        logging.error("control Process Socketsever Thread ABORTED")

###########################################################
# https://github.com/r66ff/multithreaded-server/blob/master/src/server.py
###########################################################
myControlWebServer: typing.Optional[socketserver.ThreadingTCPServer] = None
def setWebServer(host, port):
    global myControlWebServer
    try:
        #socketserver.ThreadingTCPServer.allow_reuse_address = True
        ### myControlWebServer = socketserver.ThreadingTCPServer((host, port), MyControlWebServer,  bind_and_activate=False)
        ### myControlWebServer.allow_reuse_address = False # Prevent 'cannot bind to address' errors on restart
        ### myControlWebServer.server_bind()     # Manually bind, to support allow_reuse_address
        ### myControlWebServer.server_activate() # (see above comment)
        myControlWebServer = socketserver.ThreadingTCPServer((host, port), MyControlWebServer)
        myControlWebServer.serve_forever()
        #with socketserver.TCPServer((host,port), MyTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            # server.serve_forever()
        print('stopping controlServer')
        myControlWebServer.server_close()
    except MUT.ControlProcessWebExit:
        logging.info("control Process SocketServer Thread exiting")
    except Exception:
        logging.error("control Process WebServer Thread ABORTED")

def stopSocketServer():
    raise MUT.ControlProcessSocketExit

def stopWebServer():
    raise MUT.ControlProcessWebExit
