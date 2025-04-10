import json

import MyUtils as MU
import UnasConnectHelper as UCH
import UnasCustomerCache as UCC
import UnasOrderCache as UOC
import UnasProductCache as UPC

BASEDIR = 'WebContent'

def replaceTplTags(ct:str) ->str:
    ct.replace()
    return ct

def doWebPageTemplate(pPath, queryParams):
    path = BASEDIR + '/tpl' + '/'.join(pPath)
    with open(path) as dox:
        content = dox.read()
    content = replaceTplTags(content)
    return content

def doWebPageMD(pPath, queryParams):
    path = f"{BASEDIR}/pg{'/'.join(pPath)}.md"
    with open(path) as dox:
        content = dox.read()
    return content

def doWebPageHTML(pPath, queryParams):
    path = f"{BASEDIR}/pg{'/'.join(pPath)}.html"
    with open(path) as dox:
        content = dox.read()
    return content

def doWebPageJS(pPath, queryParams):
    path = f"{BASEDIR}/pg{'/'.join(pPath)}.jsprxy"
    with open(path) as dox:
        content = dox.read()
    return content

def doWebPageFile(pPath, queryParams):
    path = f"{BASEDIR}{'/'.join(pPath)}"
    with open(path, 'rb') as dox:
        content = dox.read()
    return content

   
def doWebControlQuery(pPath, queryParams):
    if 'getpacketcount' == pPath[1]:
        resp = {}
        resp['maxPcktsHourly'] = MU.UNASCOMM_SENDPACKETMAX
        resp['warningAtCnt']   = MU.UNASCOMM_SENDPACKETWARN
        resp['cntIn60mins']    = MU.getPacketLastIntervalCnt(60)
        resp['cntIn50mins']    = MU.getPacketLastIntervalCnt(50)
        resp['cntIn40mins']    = MU.getPacketLastIntervalCnt(40)
        resp['cntIn30mins']    = MU.getPacketLastIntervalCnt(30)
        resp['cntIn20mins']    = MU.getPacketLastIntervalCnt(20)
        resp['cntIn10mins']    = MU.getPacketLastIntervalCnt(10)
        resp['free']            = MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(60)
        resp['free10']          = MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(50)
        resp['free20']          = MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(40)
        resp['free30']          = MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(30)
        resp['free40']          = MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(20)
        resp['free50']          = MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(10)
        return json.dumps(resp)
    elif 'getunascontext' == pPath[1]:
        return MU.getUnasContext().toJson()
    elif 'unascache' == pPath[1]:
        resp = []
        if 'customer' == pPath[2] or 'all' == pPath[2]:
            return json.dumps(list(MU.UnasCustomerList.values()), indent=3, cls=UCC.UnasCustomerCacheEncoder)
        if 'product' == pPath[2] or 'all' == pPath[2]:
            return json.dumps(list(MU.UnasProductList.values()), indent=3, cls=UPC.UnasProductCacheEncoder)
        if 'order' == pPath[2] or 'all' == pPath[2]:
            return json.dumps(list(MU.UnasOrderList.values()), indent=3, cls=UOC.UnasOrderCacheEncoder)
        if 'badorder' == pPath[2] or 'all' == pPath[2]:
            return json.dumps(list(MU.UnasBadOrderList.values()), indent=3, cls=UOC.UnasOrderCacheEncoder)
        return json.dumps(resp)
    else:
        pass
    return '{%s}' % f'"path" : "{"/".join(pPath)}", "prms" : {queryParams},  "msg": "Ez meg az uzenet"'

def doWebControlCommand(pPath, queryParams):
    if 'dofeedback' == pPath[1]:
        resp = UCH.updateCustomerSymbolIdList(MU.UnasCustomerFeedbackList)
        return resp or '[]', 'text/plain' # TODO Ki kellene elemezni a valaszt Jo/Rossz
    elif 'customer' == pPath[1]:
        resp = None
        if 'setsymbolid' == pPath[2]:
            custList = {}
            for sc in MU.getSymbolCustomerList():
                item = (sc[0] , sc[1] , sc[2] )
                custList[sc[0] ] = item # MU.UnasCustomerFeedbackList.append(item2)
            resp = UCH.updateCustomerSymbolIdList(custList.values()) # analyze RESP if OK remove from UnasCustomerFeedbackList
            return resp, 'application/xml'
        else:
            pass
        return ('[]', 'text/plain') if resp is None else (json.dumps(resp), 'application/json')
    else:
        pass
    return '{%s}' % f'"path" : "{"/".join(pPath)}", "prms" : {queryParams},  "msg": "Ez meg az uzenet"', 'application/json'

def doWebPost(pPath, queryParams):
    return (200, '{%s}' % f'"path" : "{"/".join(pPath)}", "prms" : {queryParams},  "msg": "Ez meg az uzenet"' )

def doWebPut(pPath, queryParams):
    return (200, '{%s}' % f'"path" : "{"/".join(pPath)}", "prms" : {queryParams},  "msg": "Ez meg az uzenet"' )

def doWebDelete(pPath, queryParams):
    return (200, '{%s}' % f'"path" : "{"/".join(pPath)}", "prms" : {queryParams},  "msg": "Ez meg az uzenet"' )

def doWebOption(pPath, queryParams):
    return (200, '{%s}' % f'"path" : "{"/".join(pPath)}", "prms" : {queryParams},  "msg": "Ez meg az uzenet"' )
