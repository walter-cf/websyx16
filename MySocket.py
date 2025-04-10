import logging
import socketserver
import threading
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
            if 'favicon.ico' == pPath[1]:
                self.send_response(404)
                return
            if 'qry' == pPath[1]:
                htmlResponseCode = 200
                contentType = "application/json"
                htmlResponseMessage = MPC.doWebControlQuery(pPath[1:], queryParams)
            elif 'ctrl' == pPath[1]:
                htmlResponseCode = 200
                htmlResponseMessage, content_type = MPC.doWebControlCommand(pPath[1:], queryParams)
                contentType = content_type or "application/json"
            elif 'tpl' == pPath[1]:
                contentType = 'text/html'
                htmlResponseMessage = MPC.doWebPageTemplate(pPath[1:], queryParams)
            elif 'md' == pPath[1]:
                # contentType = 'text/x-markdown'
                contentType = 'text/markdown'
                htmlResponseMessage = MPC.doWebPageMD(pPath[1:], queryParams)
            elif 'js' == pPath[1]:
                htmlResponseMessage = MPC.doWebPageJS(pPath[1:], queryParams)
                contentType = "application/javascript"
                htmlResponseCode = 200
            elif 'js' == pPath[1]:
                htmlResponseMessage = MPC.doWebPageJS(pPath[1:], queryParams)
                contentType = "application/javascript"
                htmlResponseCode = 200
            elif 'html' == pPath[1]: # Ez nar ELSE ag , csak kiterjesztes szerint mas a mediaType
                htmlResponseMessage = MPC.doWebPageHTML(pPath[1:], queryParams)
                contentType = "text/html"
                htmlResponseCode = 200
            else:
                if 'json' == pPath[-1].lower():
                    contentType = 'application/json'
                elif 'xml' == pPath[-1].lower():
                    contentType = 'text/xml'
                elif '.md' == pPath[-1][-3:].lower():
                    contentType = 'text/markdown'
                elif '.ico' == pPath[-1][-4:].lower():
                    contentType = 'image/x-icon'
                else:
                    contentType = 'text/plain'
                htmlResponseMessage = MPC.doWebPageFile(pPath, queryParams)
                htmlResponseCode = 200

        except Exception as e:
            htmlResponseMessage = str(e)
            htmlResponseCode = 400
        #        
        self.send_response(htmlResponseCode)
        self.send_header("Content-type", contentType )
        self.end_headers()
        self.wfile.write( htmlResponseMessage if isinstance(htmlResponseMessage, bytes) else bytes(htmlResponseMessage, 'utf-8'))
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

mySocketServer:socketserver.TCPServer = None
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
myControlWebServer:socketserver.ThreadingTCPServer = None
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
