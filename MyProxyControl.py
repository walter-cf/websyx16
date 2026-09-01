import json
import xmltodict

import MyUtils as MU
import UnasConnectHelper as UCH
import UnasCustomerCache as UCC
import UnasOrderCache as UOC
import UnasProductCache as UPC

from lxml import objectify

BASEDIR = 'WebContent'

def processProxyTpl(ct, tplTag):
    # Top level TAGs, az Embed tageket kulon kell kiertekelni -felek nem tudom recursive modon
    startTag = f'<PRXT_{tplTag}>'
    endTag = f'</PRXT_{tplTag}>'
    if 'COMMENT' == tplTag:
        ct = f"{ct[0:ct.index(startTag)]}{ ct[len(endTag) + ct.index(endTag):]}"
    elif 'EVAL' == tplTag:
        expr = f"{ct[len(startTag) + ct.index('<PRXT_EVAL>'):ct.index('</PRXT_EVAL>')]} "
        exprValue = eval(expr)
        ct = f"{ct[0:ct.index(startTag)]}{exprValue}{ ct[len(endTag) + ct.index(endTag):]}"
    else:
        pass
    return ct
        
TplTagList = ['COMMENT', 'EVAL']
def replaceTplTags(ct:str) ->str:
    for tplTag in TplTagList:
        while f'<PRXT_{tplTag}>' in ct:
            ct = processProxyTpl(ct, tplTag)
    return ct

def doWebPageTemplate(pPath, queryParams):
    path = BASEDIR + '/tpl/' + '/'.join(pPath)
    with open(path) as dox:
        content = dox.read()
    content = replaceTplTags(content)
    return content

def doWebPageMD(pPath, queryParams=()):
    path = BASEDIR + '/dox/' + '/'.join(pPath)
    return MU.mdConverter(path)


def doWebPageHTML(pPath, queryParams):
    path = f"{BASEDIR}/pg/{'/'.join(pPath)}.html"
    with open(path) as dox:
        content = dox.read()
    return content

def doWebPageJS(pPath, queryParams):
    path = f"{BASEDIR}/pg{'/'.join(pPath)}.jsprxy"
    with open(path) as dox:
        content = dox.read()
    return content

# TODO Ext meg azert at kell nezni, kell-e a binaris read egyaltalan?
def doWebPageFile(pPath, queryParams, binaryRead = False):
    docPath = '/'.join(pPath)
    path = f"{BASEDIR}/{ 'index.html' if '/' == docPath else '/'.join(pPath).lstrip('/')}"
    with open(path, 'rb' if binaryRead else 'r') as dox:
        content = dox.read()
    return content

   
def doWebControlQuery(pPath, queryParams):
    if 'getpacketcount' == pPath[0]:
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
    elif 'getunascontext' == pPath[0]:
        return MU.getUnasContext().toJson()
    elif 'dofeedback' == pPath[0]:
        return '{"x":"Igazibol, nem csinaltam meg, egyelore nem volt kedvem hozza, mert ugysem kell"}'
    elif 'unascache' == pPath[0]:
        resp = []
        if 'customer' == pPath[1] or 'all' == pPath[1]:
            return json.dumps(list(MU.UnasCustomerList.values()), indent=3, cls=UCC.UnasCustomerCacheEncoder)
        if 'product' == pPath[1] or 'all' == pPath[1]:
            return json.dumps(list(MU.UnasProductList.values()), indent=3, cls=UPC.UnasProductCacheEncoder)
        if 'order' == pPath[1] or 'all' == pPath[1]:
            return json.dumps(list(MU.UnasOrderList.values()), indent=3, cls=UOC.UnasOrderCacheEncoder)
        if 'badorder' == pPath[1] or 'all' == pPath[1]:
            return json.dumps(list(MU.UnasBadOrderList.values()), indent=3, cls=UOC.UnasOrderCacheEncoder)
        return json.dumps(resp)
    else:
        pass
    return '{%s}' % f'"path" : "{"/".join(pPath)}", "prms" : {queryParams},  "msg": "Ez meg az uzenet"'

def doWebControlCommand(pPath, queryParams):
    if 'dofeedback' == pPath[0]:
        resp = UCH.updateCustomerSymbolIdList(MU.UnasCustomerFeedbackList)
        return resp or '[]', 'text/plain' # TODO Ki kellene elemezni a valaszt Jo/Rossz
    elif 'customer' == pPath[0]:
        resp = None
        if 'setsymbolid' == pPath[1]:
            custList = {}
            for sc in MU.getSymbolCustomerList():
                item = (sc[0] , sc[1] , sc[2] )
                custList[sc[0] ] = item # MU.UnasCustomerFeedbackList.append(item2)
            resp = UCH.updateCustomerSymbolIdList(custList.values()) # analyze RESP if OK remove from UnasCustomerFeedbackList
            return resp, 'application/xml'
        else:
            pass
        return ('[]', 'text/plain') if resp is None else (json.dumps(resp), 'application/json')
    elif 'order' == pPath[0]:
        resp = None
        if 'clearsymbolid' == pPath[1]:
            xmlResp = UCH.unasGetOrderNew()
            if xmlResp is None:
                return None
            xmlEnc='utf-8'
            if xmlResp[30:36] == 'utf-16':
                xmlEnc='utf-16'            
            xml = bytes(bytearray(xmlResp, encoding=xmlEnc))
            # 
            xmlArray = []
            root = objectify.fromstring(xml,None)
            for ord in root.getchildren():
                xmlArray.append(UCH.UNAS_SETORDERSYMBOLID_XML % (ord.Key, '') )
            resp = '<error>No Data</error>'
            if len(xmlArray) > 0:
                xmlReq = "\n".join(xmlArray)
                resp = UCH.unasOrder_Direct(xmlReq)
                # python_dict=xmltodict.parse(resp)
                # return json.dumps(python_dict)
                return resp, 'application/xml'
            else:
                return "Nincs modositando ", 'text/text'
        else:
            pass
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
