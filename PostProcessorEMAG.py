import logging

def symbolSynclog(postData):
        logging.debug(postData)
        ## root=ET.fromstring(bytes(postData, 'utf-8'))
        ## logging.debug(root)
        return 'OK'
    
def doEmagOrder(cmd, orderId):
    
    if cmd == "newOrder":
        retData = "OK:" + orderId
    elif cmd == "cancelOrder":
        retData = "OK canceled:" + orderId
    elif cmd == "returnOrder":
        retData = "OK returned:" + orderId
    else:
        raise ValueError("Bad (GET) request: %s" % cmd )

    return "doEmagOrder returned! CMD: %s, OrderID: %s DATA: %s" % cmd, orderId, retData

def doEmagRequest(action, postData):
        logging.debug(action )
        logging.debug(postData)
        ## xmlReq = preProcessUnasPostRequest(action, postData, ts)
        ## xmlReq = transformPostRequest(xmlReq, "Product", ts)
        ## xmlResp = unasProduct(xmlReq, token)
        ## postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"

def doSymbolRequest(action, postData):
        logging.debug(action )
        logging.debug(postData)
        ## xmlReq = preProcessUnasPostRequest(action, postData, ts)
        ## xmlReq = transformPostRequest(xmlReq, "Product", ts)
        ## xmlResp = unasProduct(xmlReq, token)
        ## postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
