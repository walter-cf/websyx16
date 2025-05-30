import json
import os
import logging
import traceback as SysTB
import typing
from datetime import datetime, timezone
from time import time
from typing import Dict, List

import xmltodict
import yaml
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from lxml import objectify
from markdown2 import Markdown

import FdbUtils as FBU
import MyBatch
import MySmtpClient as SM
import MyUtilsTypes as MUT
import UnasConnectHelper as UCH
import UnasCustomerCache as UCC
import UnasOrderCache as UOC
from MySqlUtils import MySqlWrapper
from UnasProductCache import UnasProductCache as UPC

#

CONFIG_FILE = None
FaviconData = None
def reReadYaml():
    return readYaml(CONFIG_FILE)

PROXYCONFIG = None
def readYaml(yamlFile) -> str:
    global CONFIG_FILE, PROXYCONFIG
    CONFIG_FILE = yamlFile 
    with open(yamlFile, 'r') as stream:
        try:
            PROXYCONFIG = yaml.safe_load(stream)
            if isLogLevelInfo():
                print(PROXYCONFIG)
            setConstants(PROXYCONFIG)
        except yaml.YAMLError as exc:
            print(exc)
    return json.dumps(PROXYCONFIG)

def valDef(val, defa):
    return defa if val is None else val

def itemValDef(tag, key, defa):
    return defa if key not in tag else tag[key]

def nullSafe(tag, field, defa):
    return defa if field not in tag.keys() else tag[ field ]

def nullSafeStru(obj, tagList:List,  defa):
    item = obj
    for f in tagList:
        if item.find(f) is None:
            return defa
        else:
            item = item[f]
    return defa if item is None else item

def setConstants(cfg):
    global BATCH_PROCESSES, BATCH_GRANULARITY, BATCH_INLINE_ENABLED
    if (cfg["batch"]):
        cfgItm = cfg["batch"]
        BATCH_PROCESSES   = cfgItm.get("processes") or []
        BATCH_GRANULARITY = cfgItm.get("granularity") or 10
        BATCH_INLINE_ENABLED = cfgItm.get("enabled") or False

    global FB_HOST, FB_USER, FB_PASSWORD, FB_DBDATA_ROOT, FB_DBDATA_DEFAULT
    FB_HOST              = valDef(cfg["firebird"]["dbHost"], FB_HOST          )
    FB_USER              = valDef(cfg["firebird"]["dbUser"], FB_USER          )
    FB_PASSWORD          = valDef(cfg["firebird"]["dbPass"], FB_PASSWORD      )
    FB_DBDATA_ROOT       = valDef(cfg["firebird"]["dbRoot"], FB_DBDATA_ROOT   )
    FB_DBDATA_DEFAULT    = valDef(cfg["firebird"]["dbFile"], FB_DBDATA_DEFAULT)
 
    global SOCKET_CONTROL_HOST, SOCKET_CONTROL_PORT, SOCKET_CONTROL_ENABLED
    if "controlSocket" in cfg:
        SOCKET_CONTROL_HOST              = valDef(cfg["controlSocket"]["host"],    SOCKET_CONTROL_HOST )
        SOCKET_CONTROL_PORT              = valDef(cfg["controlSocket"]["port"],    SOCKET_CONTROL_PORT )
        SOCKET_CONTROL_ENABLED           = valDef(cfg["controlSocket"]["enabled"], SOCKET_CONTROL_ENABLED )
    else:
        SOCKET_CONTROL_ENABLED           = False
     
    global WEB_CONTROL_HOST, WEB_CONTROL_PORT, WEB_CONTROL_ENABLED
    if "controlWeb" in cfg:
        WEB_CONTROL_HOST              = valDef(cfg["controlWeb"]["host"],    WEB_CONTROL_HOST )
        WEB_CONTROL_PORT              = valDef(cfg["controlWeb"]["port"],    WEB_CONTROL_PORT )
        WEB_CONTROL_ENABLED           = valDef(cfg["controlWeb"]["enabled"], WEB_CONTROL_ENABLED )
    else:
        WEB_CONTROL_ENABLED           = False
 
    global MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
    MYSQL_HOST              = valDef(cfg["mysql"]["dbHost"], MYSQL_HOST       )
    MYSQL_USER              = valDef(cfg["mysql"]["dbUser"], MYSQL_USER       )
    MYSQL_PASSWORD          = valDef(cfg["mysql"]["dbPass"], MYSQL_PASSWORD   )
    MYSQL_DB                = valDef(cfg["mysql"]["dbFile"], MYSQL_DB         )
     
    global UnasCustomerCategoryName, UnasProductWebCategoryId, UnasProductWebCategoryName, IGNORE_BLOCKED_UNAS, UNASAPI_URL, API_KEY, UNAS_FEEDBACK_URL
    IGNORE_BLOCKED_UNAS = cfg["unas"]["ignoreBlockedClient"]
    UNASAPI_URL = cfg["unas"]["apiUrl"]
    API_KEY = cfg["unas"]["apiKey"]
    UNAS_FEEDBACK_URL          = cfg["unas"]["feedbackUrl"]
    UnasCustomerCategoryName   = cfg["unas"]["customer"]["categoryName"]
    UnasProductWebCategoryId   =  itemValDef(cfg["unas"]["webcategory"], "id", None) # 'x' if 'name' not in cfg["unas"]["webcategory"] else 'AAAAAAA'
    UnasProductWebCategoryName = itemValDef(cfg["unas"]["webcategory"],"name", None)

    global hostName, serverPort
    hostName   = cfg["proxy"]["hostName"]
    serverPort = cfg["proxy"]["serverPort"]

    UNAS_FEEDBACK_URL=eval(cfg["unas"]["feedbackUrl"])

    global XMLTAG, XMLTAG16, LOGLEVEL, CurrentLogLevel, CACHE_FORCE_RELOAD_PERIOD, PRODUCT_EXTATTRIBS
    XMLTAG   = cfg["prghelper"]["xmltag"]
    XMLTAG16 = cfg["prghelper"]["xmltag16"]
    LOGLEVEL = cfg["logLevel"]
    PRODUCT_EXTATTRIBS = cfg["prghelper"]["extendedProductAttributes"]
  
    CurrentLogLevel = MUT.LogLvl.getLevelFromStr(LOGLEVEL)
    CACHE_FORCE_RELOAD_PERIOD = cfg["unas"]["cacheForceReload"]

    global PRODUCT_PRICECAT_BASE, PRODUCT_PRICECAT_FALLBACK, PRODUCT_PRICECAT_FALLBACK2, PRODUCT_BULK, PRODUCTNAME_OVERWRITE, PRODUCTCNT_CACHE_GETLIMIT
    # ProductPriceCat
    PRODUCT_PRICECAT_BASE      = cfg["unas"]["product"]["pricecat"]["base"]
    PRODUCT_PRICECAT_FALLBACK  = cfg["unas"]["product"]["pricecat"]["fallback1"]
    PRODUCT_PRICECAT_FALLBACK2 = cfg["unas"]["product"]["pricecat"]["fallback2"]
    PRODUCT_BULK               = cfg["unas"]["product"]["bulk"]
    PRODUCTNAME_OVERWRITE      = cfg["unas"]["product"]["overwriteName"]
    PRODUCTCNT_CACHE_GETLIMIT  = cfg["unas"]["product"]["getproductLimit"]

    #global GETORDER_INTERVAL
    #GETORDER_INTERVAL = cfg["order"]["getInterval"]
    global SYMBOLVOUCHERSEQUENCECODE, SYMBOLORDERIDPREFIX, SYMBOLORDERSTATUS,ORDER_STATUS_SENDMAIL, ORDER_ITEM_FROMDB_ON_MISSING, ORDER_ITEM_FROMDB_FORCE
    if (cfg["unas"]["order"]):
        cfgItm = cfg["unas"]["order"]
        SYMBOLVOUCHERSEQUENCECODE  = cfgItm.get("vouchersequencecode")
        SYMBOLORDERIDPREFIX        = cfgItm.get("symbolOrderPrefix")
        SYMBOLORDERSTATUS          = cfgItm.get("symbolOrderStatusNew")
        ORDER_STATUS_SENDMAIL      = cfgItm.get("sendOrderStatusEmail")
        ORDER_ITEM_FROMDB_FORCE    = cfgItm.get("itemFromDbForce") or False          # TODO Elavult, mar nem kell
        ORDER_ITEM_FROMDB_ON_MISSING=cfgItm.get("itemFromDbOnMissing") or False    # TODO Elavult, mar nem kell
    # Intervals
    global GETPRODUCT_INTERVAL, GETCUSTOMER_INTERVAL, CUSTOMER_CYCLIC_INTERVAL
    GETPRODUCT_INTERVAL      = cfg["unas"]["product"]["getInterval"]
    GETCUSTOMER_INTERVAL     = cfg["unas"]["customer"]["getInterval"]
    CUSTOMER_CYCLIC_INTERVAL = cfg["unas"]["customer"]["ignoreCyclicInterval"]
    global CUSTOMER_COUNTRIES, WAREHOUSES, CUSTOMER_BULK, CUSTOMER_CODE_PREFIXES, CREATE_CUSTOMER_MISSING, CUSTOMER_FORCENEW, HANDLE_CUSTOMERADDRESS, BULK_FEEDBACK_CUSTOMER, JOETESTCustomer
    # Customer
    if (cfg["unas"]["customer"]):
        cfgCust = cfg["unas"]["customer"]
        CUSTOMER_COUNTRIES      = cfgCust["countries"]    # print(list(CUSTOMER_COUNTRIES.keys())[list(CUSTOMER_COUNTRIES.values()).index('Magyarország')])
        CUSTOMER_BULK           = cfgCust["bulk"]
        CUSTOMER_CODE_PREFIXES  = cfgCust["codePrefix"]
        CREATE_CUSTOMER_MISSING = cfgCust["cerateMissingCustomer"]
        CUSTOMER_FORCENEW       = cfgCust["forceNewState"]
        HANDLE_CUSTOMERADDRESS  = cfgCust.get("handleCustomerAddress") or False
        BULK_FEEDBACK_CUSTOMER  = cfgCust.get("bulkFeedback") or False
        JOETESTCustomer         = cfgCust.get("JOETESTCustomer") or False
    # Inventory warehouses
    WAREHOUSES            = cfg["unas"]["inventory"]["warehouses"]

    global     ORDER_STATUS_NEW, ORDER_STATUS_ACCEPTED, ORDER_STATUS_PREP,ORDER_STATUS_SHIP, ORDER_STATUS_CLOSE,ORDER_STATUS_RETURN, ORDER_STATUS_CANCEL
    # Order params - statuses
    ORDER_STATUS_NEW      = cfg["unas"]["order"]["status"]['new']
    ORDER_STATUS_ACCEPTED = cfg["unas"]["order"]["status"]['accepted']
    ORDER_STATUS_PREP     = cfg["unas"]["order"]["status"]['prepared']
    ORDER_STATUS_SHIP     = cfg["unas"]["order"]["status"]['shipping']
    ORDER_STATUS_CLOSE    = cfg["unas"]["order"]["status"]['closed']
    ORDER_STATUS_RETURN   = cfg["unas"]["order"]["status"]['returned']
    ORDER_STATUS_CANCEL   = cfg["unas"]["order"]["status"]['cancel']

    # Order FLOW Control
    global     ORDER_HandleUnregistered, ORDER_getMissingCust, ORDER_autoAcknowledge
    ORDER_HandleUnregistered  = cfg["unas"]["order"]["flow"]['getUnregistered'] # Leszedjem az Order elott a hianyzo Customereket? most ki lesz kapcsolva
    ORDER_getMissingCust      = cfg["unas"]["order"]["flow"]['getMissingCust']
    ORDER_autoAcknowledge     = cfg["unas"]["order"]['autoAcknowledge']


    global PRICERULE_TRANSPORTMODES, PRICERULE_PAYMENTMETHODS
    PRICERULE_TRANSPORTMODES = cfg["unas"]["priceRules"]['transportModes']
    PRICERULE_PAYMENTMETHODS = cfg["unas"]["priceRules"]['paymentMethods']
 
    global MAIL_SERVER, MAIL_ME, MAIL_OPERATOR
    MAIL_SERVER    = cfg["mail"]["server"]
    MAIL_ME        = cfg["mail"]["sender"]
    MAIL_OPERATOR  = cfg["mail"]["operator"]

    # Comm Stats
    global UNASCOMM_MAXERRCNT, UNASCOMM_MAXLOGINERRCNT, UNASCOMM_BLOCKEDTIME, UNASCOMM_SENDPACKETMAX, UNASCOMM_SENDPACKETWARN,UNASCOMM_ALERTRETRYAFTER, UNASCOMM_MASTER_CHALLENGE, UNASCOMM_MASTER_IDLE,UNASCOMM_CLIENT_CHALLENGE
    cfgItm = cfg["unas"].get("commstat") or {}
    UNASCOMM_MAXERRCNT       = cfgItm.get("maxerrorcnt") or 3
    UNASCOMM_MAXLOGINERRCNT  = cfgItm.get("maxloginerr") or 3
    UNASCOMM_BLOCKEDTIME     = cfgItm.get("blockedTimeMax") or 1800
    UNASCOMM_ALERTRETRYAFTER = cfgItm.get("alertRetryAfter") or 600
    UNASCOMM_SENDPACKETWARN  = cfgItm.get("sendPacketWarningThreshold") or 1600
    UNASCOMM_SENDPACKETMAX   = cfgItm.get("sendPacketStopLimit") or 1900
    UNASCOMM_MASTER_CHALLENGE= cfgItm.get("enableMasterChallenger") or False
    UNASCOMM_MASTER_IDLE     = cfgItm.get("preserveIdleMaster") or 300
    UNASCOMM_CLIENT_CHALLENGE= cfgItm.get("clientChallenge") or  {'idleTime': 100, 'machines': [], 'method': 'None'}
#
# Utilz
#
def unasXmltoJSON(xml : str = '<a></a>' ):
    data_dict = xmltodict.parse( xml )
    return json.dumps(data_dict)

def getCountryCode(country, raisError = True):
    if country is None:
         return 'hu'
    if len(country) < 1:
         return 'hu'
    if country in list(CUSTOMER_COUNTRIES.values()):
        uccContryCodeIdx = list(CUSTOMER_COUNTRIES.values()).index(country)
        cc = list(CUSTOMER_COUNTRIES.keys())[uccContryCodeIdx]
        return cc
    elif raisError:
        raise MUT.MyProgramFlowErrorException("Bad/Missed country: " + country)
    # else
    return None

def addCountryCode(country, code):
    CUSTOMER_COUNTRIES[code] = country

def collectCustItems(xml):
    global UnasCustomerList
    root=ET.fromstring(xml,None)
    for cust in root.getchildren():
        custId = 0 if len(cust.findall('Id')) == 0 else int(cust.find('Id').text)
        if custId > 0:
            custEmail = cust.find('Email').text
            symbolId = '0'
            symbolCode = None
            unasLastMod = cust.find('Dates')
            if unasLastMod is not None and unasLastMod.find('Modification') is not None:
                unasLastMod = cust.find('Dates').find('Modification').text
            if len(cust.findall('Params')) > 0 :
                for ppp in cust.find('Params'):
                    pName = ppp.find('Name')
                    if (pName.text == 'symbolId'):
                        symbolId = ppp.find('Value').text
                    elif (pName.text == 'symbolCode'):
                        symbolCode = ppp.find('Value').text
            # Addresses CountryCode / TaxNUmber
            custTaxNo = None
            if len(cust.findall('Addresses')) > 0:
                for addr in cust.find('Addresses'): # TODO Kikapcsolt cimkezelesnel nem kellen basztatni a cimeket - asszem
                        country = addr.find('Country')
                        countryCode = addr.find('CountryCode')
                        if addr.tag == "Invoice":
                            custTaxNo = next((x.text for x in addr if x.tag == 'TaxNumber') , None )
                        cc = getCountryCode( country.text, False) or 'hu'
                        if cc is None:
                            addCountryCode(country.text, countryCode.text)
            #
            ucc = UCC.UnasCustomerCache(int(custId), custEmail, custTaxNo, symbolCode, int(symbolId)) # type: ignore # State NotUsed yet
            for addr in cust.find('Addresses'):
                ucc.unasAddrXml.append( addr ) # type: ignore
            ucc.lastmod = 0 if unasLastMod is None else dateStrToTs( unasLastMod )
            if CUSTOMER_FORCENEW:
                ucc.state = 'new'
            if  UnasCustomerList.get(custId) is None:
                try:
                    putCustomerIntoCache(ucc)
                except Exception as e:
                    logging.error(f"UnasCustomerCache corrupted! Err:{str(e)}, unasId:{custId}")
                # end try
            elif  custId is None:
                logging.error(f"UnasCustomer DATA-ERROR! Customer-unasId is NULL UCC:" + ucc.toStr())
            elif  UnasCustomerList.get(custId) is None:
                putCustomerIntoCache(ucc) # type: ignore
            else:
                logging.error(f"UnasCustomerCache corrupted! tripled, unasId:{custId}")
        #
        else:
            #_m = "xmlData: %s" % ET.tostring(cust , encoding='utf-8', pretty_print=True)
            _m = "xmlData: %s" % ET.tostring(cust)
            SM.sendProxyMail(_m, MUT.AlertMailType(MUT.UnasTransactionType.UNAS_COMM_ERROR), "initCustomerCache: UNAS-data corrupted (Customer:unasId missing)")
    return UnasCustomerList

def putOrderXmlObjectIntoCache(orderKey, xml) ->  UOC.UnasOrderCache:
    for px in xml.getchildren():
        uoc = UOC.UnasOrderCache(orderKey)
        uoc.initFromXmlObj(px)
        UnasOrderList[orderKey] = uoc
        return uoc
    return None # type: ignore

def putOrderXmlIntoCache(orderKey, xml) ->  UOC.UnasOrderCache:
    bajtz = bytes(xml, 'utf-8')
    prodObj = objectify.fromstring(bajtz, None)
    for px in prodObj.getchildren():
        uoc = UOC.UnasOrderCache(orderKey)
        uoc.initFromXml(px)
        UnasOrderList[orderKey] = uoc
        return uoc
    return None # type: ignore

def collectOrderItems(xml) -> Dict[str, UOC.UnasOrderCache ] :
    global UnasOrderList
    bajtz = bytes(xml, 'utf-8')
    #utf8_parser = ET.XMLParser(encoding='utf-8')    
    #prodObj = objectify.fromstring(bajtz,parser= utf8_parser)
    prodObj = objectify.fromstring(bajtz, None)
    for px in prodObj.getchildren():
        # TODO: undeveloped part. Not ready Yet!
        # Ez Mi  F*? putOrderXmlIntoCache(orderKey, px)
        orderKey = px.find('Key').text
        oo = UOC.UnasOrderCache(orderKey)
        oo.initFromXml(px)
        UnasOrderList[orderKey] = oo
    return UnasOrderList

def collectProdItems(xml):
    pList = {}
    root=ET.fromstring(xml,None)
    for prod in root.getchildren():
        item = createProdItem(prod)
        if (item.unasId > 0 and item.sku is not None):
            pList[item.sku] = item
    return pList


def createProdItem(prod) -> UPC:
        productId = int(findTagVal(prod, 'Id', 0))
        productSku = findTagVal(prod, 'Sku')
        productState = findTagVal(prod, 'State', UPC.ProductState_PENDING)
        productStatus = int(find3rdTagV2(prod, 'Statuses', 'Type', 'base', 'Value', UPC.ProductStatus_INACTIVE))
        symbolId = int(find3rdTagV2(prod, 'Params', 'Name', 'symbolId', 'Value', 0))
        qty = float(find3rdTag(prod, 'Stocks', 'Stock', 'Qty', 0))
        pVat = 27.0
        productVat = find2ndTag( prod, 'Prices', 'Vat', defa = '27')
        if productVat.rstrip().endswith('%'):
            pVat = float(productVat.rstrip()[0:-1])
        else:
            pVat = float(productVat)
            # __init__(self, unasid, sku, sid = 0, q = 0.0,  vat = 27.0, state = ProductState_LIVE, status = ProductStatus_NEW, sts = ({ -1, 0 })):
        item = UPC(productId, productSku, symbolId, qty, pVat, productState, productStatus)
        return item

def findTagVal(xml, tag, defa=None):
    return  defa if xml.find(tag) is None else xml.find(tag).text
    
def find2ndTag( prod, tag1, tag2, defa = None):
    if len(prod.findall(tag1))>0:
        for ppp in prod.find(tag1):
            xTag = ppp.find(tag2)
            return defa if xTag is None else xTag.text
    return defa

def find3rdTag( prod, tag1, tag2, tag3 = 'Value', defa = None):
    if len(prod.findall(tag1))>0:
        for ppp in prod.find(tag1):
            if (ppp.tag ==  tag2):
                return ppp.find(tag3).text
    return defa

def find3rdTagV2( prod, tag1, tag2, tag2Value, tag3 = 'Value', defa = None):
    if len(prod.findall(tag1))>0:
        for ppp in prod.find(tag1):
            if ppp.find(tag2) is not None:
                if (ppp.find(tag2).text == tag2Value):
                    return ppp.find(tag3).text
    return defa

def refreshProductItem(prod:UPC):
    # Get Product from UNAS by ID
    retV = UCH.unasGetProductByAzon('Id', prod.unasId)
    pList = collectProdItems(bytes(retV, 'utf-8'))
    UnasProductList.update(pList)
    return pList.get(prod.sku)

LastCacheUpdated : int = 0
def reinitCacheState():
    global LastCacheUpdated
    checkCacheState(True)
    LastCacheUpdated = UtcNow()

def getUnasActiveCustomers():
    responseText = UCH.unasGetActiveCustomers()
    xml = bytes(bytearray(responseText, encoding="utf-8"))
    return collectCustItems(xml)

CACHE_FORCE_RELOAD_PERIOD = 10000
def checkCacheState(force: bool = False, typ:MUT.ProxyObjectType = MUT.ProxyObjectType.ALL):
    global UnasCustomerList, UnasProductList, UnasOrderList, LastCacheUpdated,UNASCOMM_SENDPACKETMAX
    saved_SENDPACKETMAX = UNASCOMM_SENDPACKETMAX
    UNASCOMM_SENDPACKETMAX =  2000
    if force or typ == MUT.ProxyObjectType.CUSTOMER:
        UnasCustomerList.clear()
        UnasCustomerList = getUnasActiveCustomers()
        if typ == MUT.ProxyObjectType.ALL:
            LastCacheUpdated = UtcNow()
    if force or typ == MUT.ProxyObjectType.PRODUCT:
        retrivedProductCount = 1
        limitStart = 0
        UnasProductList.clear()
        while retrivedProductCount > 0:
            retV = UCH.unasGetActiveProducts(PRODUCTCNT_CACHE_GETLIMIT, limitStart)
            retrivedProductCount = -1
            if PRODUCTCNT_CACHE_GETLIMIT < 5:
                UnasProductList = collectProdItems(retV)
            else:
                pList = collectProdItems(retV)
                retrivedProductCount = len(pList)
                if retrivedProductCount > 0:
                    UnasProductList.update(pList)
                    limitStart += retrivedProductCount
        if typ == MUT.ProxyObjectType.ALL:
            LastCacheUpdated = UtcNow()
    if force or typ == MUT.ProxyObjectType.ORDER: # Rendelesnek nem kell a minimum delay, az lehet ures
        pass # Megyeztunk, hogy a cache-t a programlogika tolti, uriti polah@20250519
        ## UnasOrderList.clear()
        ## retV = UCH.unasGetActiveOrders()
        ## UnasOrderList = collectOrderItems(retV)
        ## if typ == MUT.ProxyObjectType.ALL:
        ##     LastCacheUpdated = UtcNow()
    #
    UNASCOMM_SENDPACKETMAX =  saved_SENDPACKETMAX
    #

LastSetCustomerDT:str = None # type: ignore
LastSetProductDT:str = None # type: ignore
LastSetOrderDT:str = None # type: ignore
def saveDBcurrentDT(varSel: str = None) -> str: # type: ignore
    global LastSetCustomerDT, LastSetProductDT, LastSetOrderDT
    dt = FBU.getCurrentDT()
    if varSel is not None:
        if varSel.startswith('c'):
            LastSetCustomerDT = dt
        elif varSel.startswith('p'):
            LastSetProductDT = dt
        elif varSel.startswith('o'):
            LastSetOrderDT = dt
        else:
            pass
    else:
        LastSetCustomerDT = dt
        LastSetProductDT = dt
        LastSetOrderDT = dt
    #
    return dt

def getCurrTime() -> int:
    sex = time()
    return int(sex)

def UtcNow( sexBefore = 0 ) -> int:
    # now = datetime.utcnow()
    now = datetime.now(timezone.utc)
    sex = (now - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()
    return int(sex) - sexBefore

def diffLocalTime(fromTime, toTime):
    return None

def tsToDateStr(ts) -> str:
    dt = datetime.fromtimestamp(ts)
    return "%d.%02d.%02d %02d:%02d:%02d" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def tsToDateSql(ts) -> str:
    dt = datetime.fromtimestamp(ts)
    return "%d-%02d-%02d %02d:%02d:%02d" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def dateStrToTs(date:str):  # '2024.03.04 12:51:08'
    if date is None:
        return None
    else:
        return int(datetime.strptime(date, '%Y.%m.%d %H:%M:%S').timestamp())

def mdConverter( fileName: str ):
    try:
        markdowner = Markdown()
        fn = fileName if fileName.endswith('.md') else fileName + '.md'
        with open(fn, 'r') as f:
            txt = f.read()
            return  '' if txt is None else markdowner.convert(txt)
    except OSError as e:
        return "document %s not found! Try <a href='/about'>this</a>" % fileName

def mkCustomerCode( ucc : UCC.UnasCustomerCache, prefix : str = 'unregistered'):
    prfx = CUSTOMER_CODE_PREFIXES[prefix] # type: ignore
    return f"{prfx}-{ucc.unasId}"

#                
# def getCustomerFormCache_NU(email, taxnumber, unasId ) -> UCC.UnasCustomerCache:
#     ucc = UnasCustomerList.get( UCC.buildAzonData( email, taxnumber ))
#     if ucc is None:
#         ucc = UnasCustomerList.get( UCC.buildCustAzonById(unasId))
#     if ucc is not None:
#         if ucc.symbolId is None:
#             ucc.symbolId = 0
#         if ucc.lastmod is None:
#             ucc.lastmod = 0
#     return ucc # type: ignore

def getCustomerFromCacheByOrder( cust ) -> UCC.UnasCustomerCache:
    unasId = 0 if len(cust.findall('Id')) == 0 else int(cust.find('Id').text)
    return getCustomerFormCache(unasId)

def getCustomerFormCache(unasId:int ) -> UCC.UnasCustomerCache:
    ucc = UnasCustomerList.get( unasId )
    if ucc is not None:
        if ucc.symbolId is None:
            ucc.symbolId = 0
        if ucc.lastmod is None:
            ucc.lastmod = 0
    return ucc # type: ignore

#def putCustomerIntoCache_NU(ucc : UCC.UnasCustomerCache, cc:int):
#    azon = ucc.custAzon if cc is None else cc
#    u = UnasCustomerList.get( azon )
#    if u is None: # Remek hely a programhiba ellenorzesere!!!!!
#        ucc.custAzon = azon
#        UnasCustomerList[azon] = ucc
#    elif u.email == ucc.email and u.unasId == ucc.unasId and u.symbolId == ucc.symbolId:
#        ucc.custAzon = azon
#        UnasCustomerList[azon] = ucc
#    elif u.symbolId == 0 and u.email == ucc.email and u.unasId == ucc.unasId and u.azon == cc:
#        ucc.custAzon = azon
#        UnasCustomerList[azon] = ucc
#    else:
#        _m = f'Figyelmen kivul hagyott CustomerCache hiba!\r\n[CacheItem] {u.toStr()}\r\n[Duplicate] {ucc.toStr()}'
#        errorHandler( _m , MUT.AlertMailType(MUT.UnasTransactionType.UNKNOWN_MAX, code=MUT.ProxyErrCode.E20),
#                     level=logging.WARNING, subject='[putCustomerIntoCache] -+- Duplicate item')
#        raise MUT.MyProgramFlowErrorException( '[putCustomerIntoCache]:Duplicate item:' + u.toStr() + ' :*-*: '+ ucc.toStr() )

def putCustomerIntoCache(ucc : UCC.UnasCustomerCache):
    u = UnasCustomerList.get( ucc.unasId )
    if u is None:
        UnasCustomerList[ucc.unasId] = ucc
    elif u.email == ucc.email and u.unasId == ucc.unasId and u.symbolId == ucc.symbolId:
        UnasCustomerList[ucc.unasId] = ucc
    else:
        _m = '[putCustomerIntoCache]:Duplicate item:' + u.toStr() + ' :*-*: '+ ucc.toStr()
        logging.error( _m, u, ucc)
        raise MUT.MyProgramFlowErrorException( _m, MUT.ProxyErrCode.E40 )
#
# Constants
#
CACHESTATE_live    = "live"
CACHESTATE_new     = "new"
CACHESTATE_deleted = "deleted"
CACHESTATE_marked4delete = "marked4delete"
CACHESTATE_deleted = "deleted"
UNASACTION_add     = "add"
UNASACTION_modify  = "modify"
UNASACTION_delete  = "delete"
#
# CACHE
UnasProductList : Dict[str, UPC] = dict({})
UnasCustomerList: Dict[int, UCC.UnasCustomerCache] = dict({})
#UnasOrderList    = dict({})
UnasOrderList : Dict[str, UOC.UnasOrderCache] = dict({})
UnasBadOrderList : Dict[int, UOC.UnasOrderCache] = dict({})
UnasProductWebCategoryId = 0
UnasProductWebCategoryName = "WebCat"
UnasCustomerCategoryName = "UNAS vevo"

LastActivity = UtcNow(0)
UnasSetProductsXmlPart = ''
UnasSetCustomersXmlPart = ''
UnasPriceSetPricesXmlPart = ''
#UnasSetInventoryXmlPart = ''

hostName = "192.168.10.2"
serverPort = 3301
LOGLEVEL = 'D'
PRODUCT_EXTATTRIBS = None

IGNORE_BLOCKED_UNAS = False
UNASAPI_URL = 'https://api.unas.eu/shop'
UNAS_FEEDBACK_URL = "http://192.168.10.6:3302/fbunas"
API_KEY='c599046e7d37bc7528e994adde3404da97ba6c54' # TIXAR / Aa123456
XMLTAG = '<?xml version="1.0" encoding="UTF-8" ?>'
XMLTAG16 = '<?xml version="1.0" encoding="UTF-16" ?>'

#Batched
BATCH_PROCESSES = List[MyBatch.BatchContext]
BATCH_GRANULARITY : int = 0

# Databases
FB_HOST              = '127.0.0.1'
FB_USER              = 'demo'
FB_PASSWORD          = 'demo'
FB_DBDATA_ROOT       = '/firebird'
FB_DBDATA_DEFAULT    = 'default.fdb'

MYSQL_HOST              = 'localhost'
MYSQL_USER              = 'w6pusr'
MYSQL_PASSWORD          = 'w6p-Abc+123'
MYSQL_DB                = 'web6proxy'

SOCKET_CONTROL_HOST    = "127.0.0.1"
SOCKET_CONTROL_PORT    = 3305
SOCKET_CONTROL_ENABLED = False

WEB_CONTROL_HOST    = "127.0.0.1"
WEB_CONTROL_PORT    = 3306
WEB_CONTROL_ENABLED = False
BATCH_INLINE_ENABLED = False

# ProductPriceCat
PRODUCT_PRICECAT_BASE = -1
PRODUCT_PRICECAT_FALLBACK  = 17
PRODUCT_PRICECAT_FALLBACK2 = 21
PRODUCTNAME_OVERWRITE = False
PRODUCTCNT_CACHE_GETLIMIT = 50
# Intervals
#GETORDER_INTERVAL = 9991200
SYMBOLVOUCHERSEQUENCECODE = "!.NoteDeifined.!"
SYMBOLORDERIDPREFIX = 'H24-'
SYMBOLORDERSTATUS = 1
GETPRODUCT_INTERVAL = 7600
GETCUSTOMER_INTERVAL = 9991200
# Custo shitz
CUSTOMER_CYCLIC_INTERVAL = 1000
CUSTOMER_COUNTRIES       = {}
CUSTOMER_BULK            = 0
CUSTOMER_CODE_PREFIXES   = []
CREATE_CUSTOMER_MISSING  = False
CUSTOMER_FORCENEW        = False
HANDLE_CUSTOMERADDRESS   = False
BULK_FEEDBACK_CUSTOMER   = False
UnasCustomerFeedbackList = []
#
# Orders
ORDER_STATUS_NEW      = 0
ORDER_STATUS_ACCEPTED = 0
ORDER_STATUS_PREP     = 0
ORDER_STATUS_SHIP     = 0
ORDER_STATUS_CLOSE    = 0
ORDER_STATUS_RETURN   = 0
ORDER_STATUS_CANCEL   = 0
ORDER_STATUS_SENDMAIL = 'No'

ORDER_HandleUnregistered  = False
ORDER_getMissingCust      = False
ORDER_autoAcknowledge     = False

PRICERULE_TRANSPORTMODES = None
PRICERULE_PAYMENTMETHODS = None

MAIL_SERVER    = 'localhost'
MAIL_ME        = 'web6proxy-alert@ledsound.hu'
MAIL_OPERATOR  = 'web6proxy-operator@ledsound.hu'

# TEST datas
PRODUCT_TESTDATA1 = """<?xml version="1.0" encoding="UTF-8" ?>
<Products></Products>
"""
CUSTOMER_TESTDATA1 = """<?xml version="1.0" encoding="UTF-8" ?>
<Customers></Customers>
"""

ORDERSCUSTOMER_TESTDATA2 = """
<?xml version="1.0" encoding="UTF-8" ?>
<Orders>
</Orders>
"""
ORDERSCUSTOMER_TESTDATA1 = """<?xml version="1.0" encoding="UTF-8" ?>
<Orders>
    <Order>
        <Key>54017-285726</Key>
        <Id>146194506</Id>
        <Date>2023.10.10 17:14:43</Date>
        <DateMod>2023.10.10 17:14:43</DateMod>
        <Lang>hu</Lang>
        <Customer>
            <Email><![CDATA[etyepetye@mailinator.com]]></Email>
            <Username><![CDATA[]]></Username>
            <Contact>
                <Name><![CDATA[Etye Petye]]></Name>
                <Phone><![CDATA[+3613216547]]></Phname
                    <Name><![CDATA[Etye Petye]]></Name>
                    <ZIP>2235</ZIP>
                    <City><![CDATA[Mende]]></City>
                    <Street><![CDATA[Kossuth 11]]></Street>
                    <StreetName><![CDATA[Kossuth]]></StreetName>
                    <StreetNumber><![CDATA[11]]></StreetNumber>
                    <County><![CDATA[]]></County>
                    <Country><![CDATA[Magyarország]]></Country>
                    <CountryCode>hu</CountryCode>
                    <TaxNumber><![CDATA[]]></TaxNumber>
                    <EUTaxNumber><![CDATA[]]></EUTaxNumber>
                </Invoice>
                <Shipping>
                    <Name><![CDATA[Etye Petye]]></Name>
                    <ZIP>2235</ZIP>
                    <City><![CDATA[Mende]]></City>
                    <Street><![CDATA[Kossuth 11]]></Street>
                    <StreetName><![CDATA[Kossuth]]></StreetName>
                    <StreetNumber><![CDATA[11]]></StreetNumber>
                    <County><![CDATA[]]></County>
                    <Country><![CDATA[Magyarország]]></Country>
                    <CountryCode>hu</CountryCode>
                </Shipping>
            </Addresses>
        </Customer>
        <Currency>HUF</Currency>
        <Status><![CDATA[Feldolgozásra vár]]></Status>
        <StatusID><![CDATA[4681666]]></StatusID>
        <Authenticated>yes</Authenticated>
        <Payment>
            <Id>4681651</Id>
            <Name><![CDATA[Készpénzzel a helyszínen]]></Name>
            <Type>cash</Type>
        </Payment>
        <Shipping>
            <Id>4681636</Id>
            <Name><![CDATA[Futárral]]></Name>
        </Shipping>
        <Invoice>
            <Status>0</Status>
            <StatusText><![CDATA[]]></StatusText>
        </Invoice>
        <Comments>
            <Comment>
                <Type>customer</Type>
                <Text><![CDATA[Akkuratusan + jegyzem!]]></Text>
            </Comment>
        </Comments>
        <SumPriceGross>23790</SumPriceGross>
        <Items>
            <Item>
                <Id>717298606</Id>
                <Sku>product_009</Sku>
                <Name><![CDATA[Amet sit ipsum]]></Name>
                <ProductParams>
                </ProductParams>
                <Unit>db</Unit>
                <Quantity>1</Quantity>
                <PriceNet>3141.7323</PriceNet>
                <PriceGross>3990</PriceGross>
                <Vat>27%</Vat>
                <Status><![CDATA[]]></Status>
            </Item>
            <Item>
                <Id>717298616</Id>
                <Sku>product_005</Sku>
                <Name><![CDATA[Dolor sit amet]]></Name>
                <ProductParams>
                </ProductParams>
                <Unit>db</Unit>
                <Quantity>2</Quantity>
                <PriceNet>7795.2756</PriceNet>
                <PriceGross>9900</PriceGross>
                <Vat>27%</Vat>
                <Status><![CDATA[]]></Status>
            </Item>
        </Items>
    </Order>
</Orders>
"""

#
#    <id>190</id>
#    <code>WEB199543325</code>
#         <code>WEB00001231</code>
#
#        <sid>4357</sid>

CUSTOMER_TESTDATA_SYMEX = """<?xml version="1.0" encoding="UTF-8" ?>
<Customers>
    <Customer>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/customer?id=90001&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/customer?id=90001&errormsg=</errorurl>    
        <id>1231</id>
          <sid>204</sid>
        <code>UCO-90001-1</code>
        <name>Kovács István</name>
        <country>Hungary</country>
        <region>Baranya</region>
        <zip>1139</zip>
        <city>Budapest</city>
        <street>Fő utca</street>
        <housenumber>1. / J-35</housenumber>
        <mailcountry>Hungary</mailcountry>
        <mailregion>Baranya</mailregion>
        <mailzip>1139</mailzip>
        <mailcity>Kecskemét</mailcity>
        <mailstreet>Mellék utca</mailstreet>
        <mailhousenumber>128</mailhousenumber>
        <taxnumber>12345678-1-21</taxnumber>
        <grouptaxnumber>12345678-1-21</grouptaxnumber>
        <eutaxnumber>HU13581280-2-41</eutaxnumber>
        <bankaccount>25874125-89562385</bankaccount>
        <bankname>OTP Bank</bankname>
        <bankswiftcode>OTPVHUHB</bankswiftcode>
        <contactname>Balázs Piri Balázs-Invo-M1</contactname>
        <email>info@st.hu</email>
        <phone>70-789-4568</phone>
        <sms>70-789-4568</sms>
        <fax>70-789-4569</fax>
        <iscompany>0</iscompany>
        <description>Megjegyzés JOE 2</description>
        <customercategory>HU</customercategory>
        <pricecategoryname>Lista ár</pricecategoryname>
        <discountpercent>1.5</discountpercent>
        <webusername>user1</webusername>
        <webpassword>userpass</webpassword>
        <strexa>aaa</strexa>
        <strexb>bbb</strexb>
        <strexc>ccc</strexc>
        <strexd>ddd</strexd>
        <dateexa>2010-07-12</dateexa>
        <dateexb>2010-07-12</dateexb>
        <dateexc>2010-07-12</dateexc>
        <dateexd>2010-07-12</dateexd>
        <numexa>111</numexa>
        <numexb>222</numexb>
        <numexc>333</numexc>
        <numexd>333</numexd>
        <boolexa>0</boolexa>
        <boolexb>1</boolexb>
        <boolexc>1</boolexc>
        <boolexd>1</boolexd>
        <customeraddresses> 
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custshipaddr?id=90002&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custshipaddr?id=90002&errormsg=</errorurl>
                <preferred>0</preferred>
                <code>WEB9000201</code>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/M/1/b</housenumber>
                <contactname>Balázs Piri Balázs M-1</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=90003&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=90003&errormsg=</errorurl>
                <preferred>0</preferred>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/M/1/Cc</housenumber>
                <contactname>Balázs Piri Balázs M-1/b</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=90004&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=90004&errormsg=</errorurl>
                <preferred>1</preferred>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/M/1/DD</housenumber>
                <contactname>Balázs Piri Balázs M-1/d</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=90005&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=90005&errormsg=</errorurl>
                <preferred>0</preferred>
                <code>UCA-900001-05</code>>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/M/1/Ee</housenumber>
                <contactname>Balázs Piri Balázs M-1/e5</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
        </customeraddresses>
    </Customer>
</Customers>
"""
CUSTOMER_TESTDATA_SYMEX2 = """<?xml version="1.0" encoding="UTF-8" ?><Customers>
    <Customer>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/customer?id=90001&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/customer?id=90001&errormsg=</errorurl>    
        <id>1231</id>
        <sid>4357</sid>
        <code>WEB00001231</code>
        <name>Kovács István</name>
        <country>Hungary</country>
        <region>Baranya</region>
        <zip>1139</zip>
        <city>Budapest</city>
        <street>Fő utca</street>
        <housenumber>1.</housenumber>
        <mailcountry>Hungary</mailcountry>
        <mailregion>Baranya</mailregion>
        <mailzip>1139</mailzip>
        <mailcity>Kecskemét</mailcity>
        <mailstreet>Mellék utca</mailstreet>
        <mailhousenumber>128</mailhousenumber>
        <taxnumber>12345678-1-21</taxnumber>
        <grouptaxnumber>12345678-1-21</grouptaxnumber>
        <eutaxnumber>HU13581280-2-41</eutaxnumber>
        <bankaccount>25874125-89562385</bankaccount>
        <bankname>OTP Bank</bankname>
        <bankswiftcode>OTPVHUHB</bankswiftcode>
        <contactname>Balázs Piri Balázs</contactname>
        <email>info@st.hu</email>
        <phone>70-789-4568</phone>
        <sms>70-789-4568</sms>
        <fax>70-789-4569</fax>
        <iscompany>0</iscompany>
        <description>Megjegyzés</description>
        <customercategory>RO</customercategory>
        <pricecategoryname>Lista ár</pricecategoryname>
        <discountpercent>1.5</discountpercent>
        <webusername>user1</webusername>
        <webpassword>userpass</webpassword>
        <strexa>aaa</strexa>
        <strexb>bbb</strexb>
        <strexc>ccc</strexc>
        <strexd>ddd</strexd>
        <dateexa>2010-07-12</dateexa>
        <dateexb>2010-07-12</dateexb>
        <dateexc>2010-07-12</dateexc>
        <dateexd>2010-07-12</dateexd>
        <numexa>111</numexa>
        <numexb>222</numexb>
        <numexc>333</numexc>
        <numexd>333</numexd>
        <boolexa>0</boolexa>
        <boolexb>1</boolexb>
        <boolexc>1</boolexc>
        <boolexd>1</boolexd>
        <lookupexa>Főcsoport/Alcsoport</lookupexa>
        <lookupexb>Főcsoport/Alcsoport</lookupexb>
        <lookupexc>Főcsoport/Alcsoport</lookupexc>
        <lookupexd>Főcsoport/Alcsoport</lookupexd>
        <customeraddresses> 
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custshipaddr?id=90001&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custshipaddr?id=90001&errormsg=</errorurl>
                <preferred>1</preferred>
                <id>12315</id>
                <sid>12315</sid>
                <code>A12</code>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/a</housenumber>
                <contactname>Balázs Piri Balázs</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=90003&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=90003&errormsg=</errorurl>
                <preferred>1</preferred>
                <id>12315</id>
                <sid>12315</sid>
                <code>A12</code>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/a</housenumber>
                <contactname>Balázs Piri Balázs</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
        </customeraddresses>
        <customercontacts>
            <customercontact>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custcontact?id=90005&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custcontact?id=90005&errormsg=</errorurl>
                <name>Sample</name>
                <sid>12317</sid>
                <responsibility></responsibility>
                <phone>70-785-4587</phone>  -- Kapcsolattartó telefonszáma (CustomerContact.Phone)
                <fax>1-456-7989</fax>
                <sms>70-4587854</sms>
                <email>info@sample.hu</email>
                <url>www.sample.hu</url>
                <skype>something</skype>
                <facebookurl>facebook.com/sample</facebookurl>
                <msn>123ert</msn>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customercontact>
            <customercontact>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custcontact?id=90006&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custcontact?id=90006&errormsg=</errorurl>
                <name>Sample</name>
                <sid>12317</sid>
                <responsibility></responsibility>
                <phone>70-785-4587</phone>  -- Kapcsolattartó telefonszáma (CustomerContact.Phone)
                <fax>1-456-7989</fax>
                <sms>70-4587854</sms>
                <email>info@sample.hu</email>
                <url>www.sample.hu</url>
                <skype>something</skype>
                <facebookurl>facebook.com/sample</facebookurl>
                <msn>123ert</msn>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customercontact>
        </customercontacts>
    </Customer>
</Customers>
"""
CUSTOMER_TESTDATA_SYMEX3 = """<?xml version="1.0" encoding="UTF-8" ?>"""

CUSTOMER_TESTDATA_SYMEXORI = """<?xml version="1.0" encoding="UTF-8" ?>
<Customers>
    <Customer>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/customer?id=90001&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/customer?id=90001&errormsg=</errorurl>    
        <id>1231</id>
        <sid>4357</sid>
        <code>WEB00001231</code>
        <name>Kovács István</name>
        <country>Hungary</country>
        <region>Baranya</region>
        <zip>1139</zip>
        <city>Budapest</city>
        <street>Fő utca</street>
        <housenumber>1.</housenumber>
        <mailcountry>Hungary</mailcountry>
        <mailregion>Baranya</mailregion>
        <mailzip>1139</mailzip>
        <mailcity>Kecskemét</mailcity>
        <mailstreet>Mellék utca</mailstreet>
        <mailhousenumber>128</mailhousenumber>
        <taxnumber>12345678-1-21</taxnumber>
        <grouptaxnumber>12345678-1-21</grouptaxnumber>
        <eutaxnumber>HU13581280-2-41</eutaxnumber>
        <bankaccount>25874125-89562385</bankaccount>
        <bankname>OTP Bank</bankname>
        <bankswiftcode>OTPVHUHB</bankswiftcode>
        <contactname>Balázs Piri Balázs</contactname>
        <email>info@st.hu</email>
        <phone>70-789-4568</phone>
        <sms>70-789-4568</sms>
        <fax>70-789-4569</fax>
        <iscompany>0</iscompany>
        <description>Megjegyzés</description>
        <customercategory>SK</customercategory>
        <pricecategoryname>Lista ár</pricecategoryname>
        <discountpercent>1.5</discountpercent>
        <webusername>user1</webusername>
        <webpassword>userpass</webpassword>
        <strexa>aaa</strexa>
        <strexb>bbb</strexb>
        <strexc>ccc</strexc>
        <strexd>ddd</strexd>
        <dateexa>2010-07-12</dateexa>
        <dateexb>2010-07-12</dateexb>
        <dateexc>2010-07-12</dateexc>
        <dateexd>2010-07-12</dateexd>
        <numexa>111</numexa>
        <numexb>222</numexb>
        <numexc>333</numexc>
        <numexd>333</numexd>
        <boolexa>0</boolexa>
        <boolexb>1</boolexb>
        <boolexc>1</boolexc>
        <boolexd>1</boolexd>
        <lookupexa>Főcsoport/Alcsoport</lookupexa>
        <lookupexb>Főcsoport/Alcsoport</lookupexb>
        <lookupexc>Főcsoport/Alcsoport</lookupexc>
        <lookupexd>Főcsoport/Alcsoport</lookupexd>
        <customeraddresses> 
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custshipaddr?id=90001&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custshipaddr?id=90001&errormsg=</errorurl>
                <preferred>1</preferred>
                <id>12315</id>
                <sid>12315</sid>
                <code>A12</code>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/a</housenumber>
                <contactname>Balázs Piri Balázs</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=90003&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=90003&errormsg=</errorurl>
                <preferred>1</preferred>
                <id>12315</id>
                <sid>12315</sid>
                <code>A12</code>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/a</housenumber>
                <contactname>Balázs Piri Balázs</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
        </customeraddresses>
        <customercontacts>
            <customercontact>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custcontact?id=90005&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custcontact?id=90005&errormsg=</errorurl>
                <name>Sample</name>
                <sid>12317</sid>
                <responsibility></responsibility>
                <phone>70-785-4587</phone>  -- Kapcsolattartó telefonszáma (CustomerContact.Phone)
                <fax>1-456-7989</fax>
                <sms>70-4587854</sms>
                <email>info@sample.hu</email>
                <url>www.sample.hu</url>
                <skype>something</skype>
                <facebookurl>facebook.com/sample</facebookurl>
                <msn>123ert</msn>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customercontact>
            <customercontact>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custcontact?id=90006&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custcontact?id=90006&errormsg=</errorurl>
                <name>Sample</name>
                <sid>12317</sid>
                <responsibility></responsibility>
                <phone>70-785-4587</phone>  -- Kapcsolattartó telefonszáma (CustomerContact.Phone)
                <fax>1-456-7989</fax>
                <sms>70-4587854</sms>
                <email>info@sample.hu</email>
                <url>www.sample.hu</url>
                <skype>something</skype>
                <facebookurl>facebook.com/sample</facebookurl>
                <msn>123ert</msn>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customercontact>
        </customercontacts>
    </Customer>
    <Customer>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/customer?id=900021&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/customer?id=900021&errormsg=</errorurl>    
        <id>1231</id>
        <sid>4357</sid>
        <code>WEB00001231</code>
        <name>Kovács István</name>
        <country>Hungary</country>
        <region>Baranya</region>
        <zip>1139</zip>
        <city>Budapest</city>
        <street>Fő utca</street>
        <housenumber>1.</housenumber>
        <mailcountry>Hungary</mailcountry>
        <mailregion>Baranya</mailregion>
        <mailzip>1139</mailzip>
        <mailcity>Kecskemét</mailcity>
        <mailstreet>Mellék utca</mailstreet>
        <mailhousenumber>128</mailhousenumber>
        <taxnumber>12345678-1-21</taxnumber>
        <grouptaxnumber>12345678-1-21</grouptaxnumber>
        <eutaxnumber>HU13581280-2-41</eutaxnumber>
        <bankaccount>25874125-89562385</bankaccount>
        <bankname>OTP Bank</bankname>
        <bankswiftcode>OTPVHUHB</bankswiftcode>
        <contactname>Balázs Piri Balázs</contactname>
        <email>info@st.hu</email>
        <phone>70-789-4568</phone>
        <sms>70-789-4568</sms>
        <fax>70-789-4569</fax>
        <iscompany>0</iscompany>
        <description>Megjegyzés</description>
        <customercategory>CZ</customercategory>
        <pricecategoryname>Lista ár</pricecategoryname>
        <discountpercent>1.5</discountpercent>
        <webusername>user1</webusername>
        <webpassword>userpass</webpassword>
        <strexa>aaa</strexa>
        <strexb>bbb</strexb>
        <strexc>ccc</strexc>
        <strexd>ddd</strexd>
        <dateexa>2010-07-12</dateexa>
        <dateexb>2010-07-12</dateexb>
        <dateexc>2010-07-12</dateexc>
        <dateexd>2010-07-12</dateexd>
        <numexa>111</numexa>
        <numexb>222</numexb>
        <numexc>333</numexc>
        <numexd>333</numexd>
        <boolexa>0</boolexa>
        <boolexb>1</boolexb>
        <boolexc>1</boolexc>
        <boolexd>1</boolexd>
        <lookupexa>Főcsoport/Alcsoport</lookupexa>
        <lookupexb>Főcsoport/Alcsoport</lookupexb>
        <lookupexc>Főcsoport/Alcsoport</lookupexc>
        <lookupexd>Főcsoport/Alcsoport</lookupexd>
        <customeraddresses> 
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custshipaddr?id=900022&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custshipaddr?id=900022&errormsg=</errorurl>
                <preferred>1</preferred>
                <id>12315</id>
                <sid>12315</sid>
                <code>A12</code>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/a</housenumber>
                <contactname>Balázs Piri Balázs</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
            <customeraddress>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=900023&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=900023&errormsg=</errorurl>
                <preferred>1</preferred>
                <id>12315</id>
                <sid>12315</sid>
                <code>A12</code>
                <name>Sample</name>
                <country>Hun</country>
                <region>Baranya</region>
                <zip>7624-2</zip>
                <city>Pécs</city>
                <street>Báthory István utca</street>
                <housenumber>20/a</housenumber>
                <contactname>Balázs Piri Balázs</contactname>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <email>info@sample.hu</email>
                <iscompany>0</iscompany>
                <companytaxnumber>12345678-1-21</companytaxnumber>
                <companygrouptaxnumber>12345678-1-21</companygrouptaxnumber>
                <companyeutaxnumber>HU13581280-2-41</companyeutaxnumber>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customeraddress>
        </customeraddresses>
        <customercontacts>
            <customercontact>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custcontact?id=900025&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custcontact?id=900025&errormsg=</errorurl>
                <name>Sample</name>
                <sid>12317</sid>
                <responsibility></responsibility>
                <phone>70-785-4587</phone>  -- Kapcsolattartó telefonszáma (CustomerContact.Phone)
                <fax>1-456-7989</fax>
                <sms>70-4587854</sms>
                <email>info@sample.hu</email>
                <url>www.sample.hu</url>
                <skype>something</skype>
                <facebookurl>facebook.com/sample</facebookurl>
                <msn>123ert</msn>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customercontact>
            <customercontact>
                <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custcontact?id=900026&symbolid=</feedbackurl>
                <errorurl>http://192.168.10.6:3301/fbunas/err/custcontact?id=900026&errormsg=</errorurl>
                <name>Sample</name>
                <sid>12317</sid>
                <responsibility></responsibility>
                <phone>70-785-4587</phone>
                <fax>1-456-7989</fax>
                <sms>70-4587854</sms>
                <email>info@sample.hu</email>
                <url>www.sample.hu</url>
                <skype>something</skype>
                <facebookurl>facebook.com/sample</facebookurl>
                <msn>123ert</msn>
                <description>A kansasi rónaság közepéről Dorkát és Toto kutyát a forgószél csodás vidékre repíti, a mumpicok országába. Kiderül, hogy a kislány messzire elkerült otthonától. A jóságos Északi Boszorkánytól megtudja, hogy Smaragdvárosba kell eljutnia Ozhoz, a legnagyobb varázslóhoz, mert csak az ő segítségével juthat vissza az otthonába. A hosszú vándorút során Dorka igaz barátokra talál: a Madárijesztőre, a Bádog Favágóra és a Gyáva Oroszlánra, ők is a Bölcsek Bölcse segítségére vágynak. Számtalan kaland után elérkeznek Oz fényes palotájába. A nagy varázsló "megajándékozza" a Madárijesztőt ésszel, a Bádogembert szívvel s a Gyáva Oroszlánt is bátorrá teszi. De Dorkát csak a jó Déli Boszorkány útmutatása segíti haza szeretett otthonába.</description>
                <deleted>0</deleted>
            </customercontact>
        </customercontacts>
    </Customer>
</Customers>
"""

CUSTOMER_TESTDATA_NANO = """<Customers>
  <Customer>
    <feedbackurl>http://192.168.10.6:3301/fbunas/oke/customer?id=199543325&ipaddr=&symbolid=</feedbackurl>
    <errorurl>http://192.168.10.6:3301/fbunas/err/customer?id=199543325&errormsg=</errorurl>    
    <customerstatus>1</customerstatus>
    <supplierstatus>0</supplierstatus>
    <name>Nano Phone Kft</name>
    <searchname />
    <customercategory>HU</customercategory>
    <invoicecountry>Magyarország</invoicecountry>
    <invoiceregion />
    <invoicezip>8446</invoicezip>
    <invoicecity>Kislőd</invoicecity>
    <invoicestreet>Szamlazasi JT - 1</invoicestreet>
    <invoicehousenumber>1/a</invoicehousenumber>
    <mailcountry>Magyarország</mailcountry>
    <mailregion />
    <mailname>Levelezes Name - 1</mailname>
    <mailzip>1221</mailzip>
    <mailcity>Budapest</mailcity>
    <mailstreet>Levelezesi JT-1/L</mailstreet>
    <mailhousenumber>1/L</mailhousenumber>
    <paymentmethod>Készpénz</paymentmethod>
    <paymentmethodtoleranceday />
    <pricecategory>-1</pricecategory>
    <pricecategoryname>Lista ár</pricecategoryname>
    <discountpercent>0</discountpercent>
    <taxnumber>27396104-2-19</taxnumber>
    <eutaxnumber />
    <bankaccount />
    <bankaccountiban />
    <bankname />
    <bankswiftcode />
    <contactname>Csík Albert</contactname>
    <phone>+36706393535</phone>
    <fax />
    <sms />
    <email>slimstoreszeged@gmail.com</email>
    <webusername>slimstoreszeged@gmail.com</webusername>
    <webpassword />
    <iscompany>1</iscompany>
    <description />
    <deleted>0</deleted>
    <strexa />
    <strexb />
    <strexc />
    <strexd />
    <dateexa />
    <dateexb />
    <numexa />
    <numexb />
    <numexc />
    <boolexa>0</boolexa>
    <boolexb>0</boolexb>
    <customeraddresses>
      <customeraddress>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custshipaddr?id=199543325&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/custshipaddr?id=199543325&errormsg=</errorurl>      
        <preferred>1</preferred>
        <id>190</id>
        <code>UCS199543325</code>
        <name>Nano Phone Kft</name>
        <country>Magyarország</country>
        <region />
        <zip>8446</zip>
        <city>Kislőd</city>
        <street>JOA-Tph 1-1</street>
        <housenumber>1/a</housenumber>
        <contactname>Csík Albert</contactname>
        <phone>+36706393535</phone>
        <fax />
        <email />
        <iscompany>0</iscompany>
        <companytaxnumber />
        <description>UNAS Customer Other Address info - Shipping</description>
        <deleted>0</deleted>
      </customeraddress>
      <customeraddress>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=199543325&idx=2&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=199543325&idx=2&errormsg=</errorurl>
        <preferred>0</preferred>
        <id>191</id>
        <code>JOA-1-2</code>
        <name>Nano Phone Kft</name>
        <country>Magyarország</country>
        <region />
        <zip>8446</zip>
        <city>Kislőd</city>
        <street>JOA-1-2 TH 2/b</street>
        <housenumber>1/b</housenumber>
        <contactname>Csík Albert</contactname>
        <phone>+36706393535</phone>
        <fax />
        <email />
        <iscompany>0</iscompany>
        <companytaxnumber />
        <description>UNAS Customer Other Address info - 7</description>
        <deleted>0</deleted>
      </customeraddress>
      <customeraddress>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=199543325&idx=3&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=199543325&idx=3&errormsg=</errorurl>
        <preferred>0</preferred>
        <code>UCA199543325-3</code>
        <name>Nano Phone Kft</name>
        <country>Magyarország</country>
        <region />
        <zip>8446</zip>
        <city>Kislőd</city>
        <street>Borsodpuszta 5 joe TH 3</street>
        <housenumber>1</housenumber>
        <contactname>Csík Albert</contactname>
        <phone>+36706393535</phone>
        <fax />
        <email />
        <iscompany>0</iscompany>
        <companytaxnumber />
        <description>UNAS Customer Other Address info - 3</description>
        <deleted>0</deleted>
      </customeraddress>
      <customeraddress>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=199543325&idx=4&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=199543325&idx=4&errormsg=</errorurl>
        <preferred>0</preferred>
        <code>UCA199543325-4</code>
        <name>Nano Phone Kft</name>
        <country>Magyarország</country>
        <region />
        <zip>8446</zip>
        <city>Kislőd</city>
        <street>Borsodpuszta 5 joe TH 4</street>
        <housenumber>1</housenumber>
        <contactname>Csík Albert</contactname>
        <phone>+36706393535</phone>
        <fax />
        <email />
        <iscompany>0</iscompany>
        <companytaxnumber />
        <description>UNAS Customer Other Address info - 6</description>
        <deleted>0</deleted>
      </customeraddress>
      <customeraddress>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=199543325&idx=5&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=199543325&idx=5&errormsg=</errorurl>
        <preferred>0</preferred>
        <code>UCA199543325-5</code>
        <name>UCA199543325-5</name>
        <country />
        <region />
        <zip>1221</zip>
        <city>Budapest</city>
        <street>Tengeri utca</street>
        <housenumber>5/a</housenumber>
        <contactname>Joe -TH - 5</contactname>
        <phone>+36-1-1234567</phone>
        <fax />
        <email />
        <iscompany>0</iscompany>
        <companytaxnumber />
        <description />
        <deleted>0</deleted>
      </customeraddress>
      <customeraddress>
        <feedbackurl>http://192.168.10.6:3301/fbunas/oke/custothaddr?id=199543325&idx=6&symbolid=</feedbackurl>
        <errorurl>http://192.168.10.6:3301/fbunas/err/custothaddr?id=199543325&idx=6&errormsg=</errorurl>
        <preferred>0</preferred>
        <code>UCA199543325-6</code>
        <name>UCA199543325-6</name>
        <country />
        <region />
        <zip>1221</zip>
        <city>Budapest</city>
        <street>Tengeri utca</street>
        <housenumber>4/a</housenumber>
        <contactname>Joe TH - 6</contactname>
        <phone>+36-1-1234567</phone>
        <fax />
        <email />
        <iscompany>0</iscompany>
        <companytaxnumber />
        <description />
        <deleted>0</deleted>
      </customeraddress>
    </customeraddresses>
  </Customer>
</Customers>
"""

#
# "SALAMON és SALAMON" Kkt
#  Cégjegyzékszám #  01-03-021683
#  Adószám#  28072049-1-41



def isLogLevelTrace():
    return isLogLevel(MUT.LogLvl.TRACE)
def isLogLevelDebug():
    return isLogLevel(MUT.LogLvl.DEBUG)
def isLogLevelInfo():
    return isLogLevel(MUT.LogLvl.INFO)
def isLogLevelWarn():
    return isLogLevel(MUT.LogLvl.WARNING)

CurrentLogLevel:MUT.LogLvl = MUT.LogLvl.INFO
def isLogLevel(lvl:MUT.LogLvl) -> bool: 
    return lvl <= CurrentLogLevel


# get (new) Transaction ID from Tomestamp + xx as originate from
typeMultiplier = 1000
def getTimeFromTS(ts:int = 0):
    return int((getTS() if ts == 0 else ts) // typeMultiplier)
def getTimeStringTS(ts:int = 0):
    return tsToDateStr(getTimeFromTS(ts))
def getActionTypeNameFromTS(ts:int = 0):
    return getActionTypeFromTS(ts).name
def getActionTypeFromTS(ts = 0):
    return MUT.UnasTransactionType(int((getTS() if ts == 0 else ts) % typeMultiplier))

def createTransactionId(tsType:MUT.UnasTransactionType = MUT.UnasTransactionType.CREATENEW):
    getUnasContext().lastTS = typeMultiplier * getCurrTime() + tsType
    return getUnasContext().lastTS # TODO Logoljam a transaction Created Event-t?

def getTS():
    return getUnasContext().lastTS

def createStatEntry(action:str, xmlParam:str): # login, getXXX , setXXX, procycontrol, test, TEST ???
    unasContext.statEntryMySqlId = createStatEntrySql(action, xmlParam ) or 0
    updateStatEntry(action)

def createStatEntryOK(resp:str = ''):
    updateStatEntryStatus(200, xml=resp, myId=unasContext.statEntryMySqlId )
    updateStatEntryOK()

def createStatEntryERR(retCode:int, response:str):
    updateStatEntryStatus(retCode, xml=response, myId=unasContext.statEntryMySqlId )
    updateStatEntryERR(retCode)

unasContext = MUT.UnasContext()
def getUnasContext() -> MUT.UnasContext: 
    global unasContext
    return unasContext

def loadUnasProxyContext():
    sql = 'SELECT * FROM proxy_context'
    ctxRow = mySqlIntance.getRow(sql) or {}
    ctx = getUnasContext()
    ctx.lastGetCustomer = 0 if ctxRow['lastGetCustomer'] is None else ctxRow['lastGetCustomer']
    ctx.lastGetOrder    = 0 if ctxRow['lastGetOrder'   ] is None else ctxRow['lastGetOrder'   ]
    ctx.lastSetCustomer = 0 if ctxRow['lastSetCustomer'] is None else ctxRow['lastSetCustomer']
    ctx.lastSetProduct  = 0 if ctxRow['lastSetProduct' ] is None else ctxRow['lastSetProduct' ]

def loadUnasBatchContext():
    sql = 'SELECT * FROM proxy_context'
    ctxRow = mySqlIntance.getRow(sql) or {}
    ctx = getUnasContext()
    ctx.lastUnasOrderStatus = 0 if len(ctxRow) == 0 else ctxRow['lastUnasOrderStatus']

def saveUnasProxyContext():
    ctx = getUnasContext()
    sql = 'UPDATE proxy_context set lastGetCustomer=%s, lastGetOrder=%s, lastSetCustomer=%s, lastSetProduct=%s, updated = NOW()'
    val = (ctx.lastGetCustomer, ctx.lastGetOrder, ctx.lastSetCustomer, ctx.lastSetProduct )
    return mySqlIntance.execSql(sql, val, True )

def saveUnasBatchContext():
    sql = f"UPDATE proxy_context set lastUnasOrderStatus={getUnasContext().lastUnasOrderStatus}, updated = NOW()"
    return mySqlIntance.execSql(sql, (), True )

def clearUnasContextCounter() -> MUT.UnasContext: 
    unasContext.clearCounters()
    return unasContext

def updateStatEntry(action:str):
    unasContext.lastAction = action
    unasContext.commCnt = unasContext.commCnt + 1
    if action.startswith('get'):
        unasContext.getcnt = 1 + unasContext.getcnt
    elif action.startswith('set'):
        unasContext.setcnt = 1 + unasContext.setcnt
    elif action.startswith('pppp'):
        pass

def updateStatEntryOK():
    unasContext.commOkCnt = 1 + unasContext.commOkCnt

def updateStatEntryERR(retCode:int):
    unasContext.commErrCnt = 1 + unasContext.commErrCnt

def clearCommError():
    unasContext.commBlocked = 0
    unasContext.commErrCnt = 0
    unasContext.lastAlertMailSent = []

UNASCOMM_MAXERRCNT = 3
UNASCOMM_MAXLOGINERRCNT = 3
UNASCOMM_BLOCKEDTIME = 1800
UNASCOMM_ALERTRETRYAFTER = 600
UNASCOMM_SENDPACKETMAX = 1900
UNASCOMM_SENDPACKETWARN = 1600
UNASCOMM_MASTER_CHALLENGE = False
UNASCOMM_MASTER_IDLE = 300
UNASCOMM_CLIENT_CHALLENGE = None

def checkCommError():
    unasCtx = getUnasContext()
    # Clear sent mail AlertTimes if needed
    if UtcNow( UNASCOMM_BLOCKEDTIME ) > unasCtx.lastBlockMailSent:
        unasCtx.lastBlockMailSent = 0
    if UtcNow( UNASCOMM_ALERTRETRYAFTER ) > unasCtx.lastYarnMailSent:
        unasCtx.lastYarnMailSent = 0
        
    if unasContext.commBlocked > 0:
        if getCurrTime() - unasCtx.commBlocked > UNASCOMM_BLOCKEDTIME: # release block
            clearCommError()
            unasCtx.lastBlockMailSent = 0
            unasCtx.lastYarnMailSent = 0
        else:
            # set Context State
            unasCtx.lastAction = getActionTypeFromTS().name
            # send Alert - email + lastAlertEmailType
            errMsg = f'Communication blocked! Packet LOST!\r\n action:%s, TS:%d' % (unasContext.lastAction, getTS()) 
            if unasCtx.lastBlockMailSent == 0:
                SM.sendProxyMail(errMsg, MUT.AlertMailType(MUT.UnasTransactionType.UNAS_COMM_ERROR),'UNAS comm blocked by Proxy!') 
            raise Exception( errMsg )
    elif unasContext.commErrCnt > UNASCOMM_MAXERRCNT:
            unasCtx.commBlocked = getCurrTime()
            errMsg = f"MAXERRCNT - reached: action:%s, TS:%d" % (unasCtx.lastAction, getTS()) 
            if unasCtx.lastBlockMailSent == 0:
                SM.sendProxyMail(errMsg, MUT.AlertMailType(MUT.UnasTransactionType.UNAS_COMM_ERROR), 'UNAS comm blocked by Proxy!')
            raise Exception("MAXERRCNT - reached: Communication droped! action:%s, TS:%d" % (unasCtx.lastAction, getTS()) )
    #elif getPacketLastHourCnt() > UNASCOMM_SENDPACKETMAX:
    #        unasContext.commBlocked = getCurrTime()
    #        errMsg = "Hourly SEND-LIMIT reached - UNAS comm blocked by Proxy! action:%s, TS:%d" % (unasContext.lastAction, getTS()) 
    #        raise Exception(errMsg)
    else:
        currCnt = getPacketLastIntervalCnt(60) # 60 mins
        if isLogLevelTrace():
            print(currCnt)
        if currCnt > UNASCOMM_SENDPACKETMAX:
            unasCtx.commBlocked = getCurrTime()
            blockedUntil = tsToDateStr( UtcNow( -1 * UNASCOMM_BLOCKEDTIME ))
            errMsg = "Hourly SEND-LIMIT reached - UNAS comm BLOCKED Until: %s !" % blockedUntil
            SM.sendProxyMail(errMsg, MUT.AlertMailType(MUT.UnasTransactionType.UNAS_COMM_ERROR), f'[RED-Alert] - UNAS comm blocked because of limit {currCnt} reached!')
            unasCtx.lastBlockMailSent = getCurrTime()
            raise Exception(errMsg)
        elif currCnt < UNASCOMM_SENDPACKETWARN:
            unasCtx.lastYarnMailSent = 0
        elif unasCtx.lastYarnMailSent == 0:
            unasCtx.lastYarnMailSent = getCurrTime()
            errMsg = '''SOFT-Packet-LIMIT:[%d] reached!
                Hard limit: %d
                Available now   : %d
                after 10 mins : %d
                after 20 mins : %d
                after 30 mins : %d
                after 40 mins : %d''' %  (UNASCOMM_SENDPACKETWARN, UNASCOMM_SENDPACKETMAX,
                    UNASCOMM_SENDPACKETMAX - currCnt,
                    UNASCOMM_SENDPACKETMAX - getPacketLastIntervalCnt(50),
                    UNASCOMM_SENDPACKETMAX - getPacketLastIntervalCnt(40),
                    UNASCOMM_SENDPACKETMAX - getPacketLastIntervalCnt(30),
                    UNASCOMM_SENDPACKETMAX - getPacketLastIntervalCnt(20)
                )
            SM.sendProxyMail(errMsg, MUT.AlertMailType(MUT.UnasTransactionType.UNAS_COMM_ERROR), '-[Yellow-Warn] Packet SoftLimit [%d/hour] reached!' % UNASCOMM_SENDPACKETWARN)

#########################################################################################
# MySQL wrapper funtions
#########################################################################################
mySqlIntance = MySqlWrapper()
def mySqlCheckConnection() -> bool :
    try:
        conn = mySqlIntance.getConn()
        return doMySql('select 1') or False
    except:
        conn = mySqlIntance.getConn()
        return conn or False

def doMySql(sql, params = ()):
    return mySqlIntance.doSql( sql, params)

def execMySql(sql, params):
    return mySqlIntance.execSql( sql, params)

def createStatEntrySql(action, xmlParam ):
    sql = "INSERT INTO commstats (action, requestXml, transactionId) VALUES (%s, %s, %s)"
    val = (action, xmlParam, getTS())
    return mySqlIntance.execSql(sql, val, True )

def createStatEntrySql(action, xmlParam ):
    sql = "INSERT INTO commstats (action, requestXml, transactionId) VALUES (%s, %s, %s)"
    val = (action, xmlParam, getTS())
    return mySqlIntance.execSql(sql, val, True )

def updateStatEntryStatus(retCode, xml:str = '', myId:int = 0):
    if myId > 0:
        sql = "UPDATE commstats set responseCode=%s, responseXml = %s WHERE Id = %s"
        val = (retCode, xml, myId)
    else:
        sql = "UPDATE commstats set responseCode=%s, responseXml = %s WHERE transactionId = %s"
        val = (retCode, xml, getTS())
    return mySqlIntance.execSql(sql, val, True )

def getPacketLastHourCnt(fromTime:int=0, toTime:int = 0):
    result =  mySqlIntance.doSql(
            "SELECT count(*) cnt from commstats WHERE createdAt between %s and %s", (
                tsToDateSql( fromTime if fromTime > 0 else UtcNow(3600)),
                tsToDateSql( toTime if toTime > 0 else getCurrTime())     ))  or []
    return 0 if len(result) == 0 else result[0]['cnt']
# Modositott  verzio: count last 10,20,40 60 minutes
def getPacketLastIntervalCnt(interval:int=60):
    result =  mySqlIntance.doSql(f"SELECT count(*) cnt from commstats WHERE createdAt > DATE_SUB(NOW(), interval {interval} MINUTE)") or []
    return 0 if len(result) == 0 else result[0]['cnt']


def getQueryParamInt(queryParams, name:str):
    val = getQueryParam(queryParams, name)
    return 0 if val is None else int(val)

def getQueryParam(queryParams, name:str):
    return None if queryParams.get(name) is None else None if len(queryParams.get(name)) == 0 else queryParams.get(name)[0]

def errorHandler(errMsg:str, alertType:MUT.AlertMailType, level = logging.INFO, subject:typing.Optional[str] = None, eDescr=None, lastFrameStr:typing.Optional[str] = None):
    if subject is None:
        if level == logging.WARNING:
            _subj = f'WARNING - unexpected but ignored error ({alertType.errCode})'
        elif level == logging.ERROR:
            _subj = f'FATAL - unhandled error ({alertType.errCode})'
        else:
            _subj = f'INFO: processflow interrupted ({alertType.errCode})'
    else:
        _subj = subject
    #
    actTS = getTS()
    logErrMsg = f"TS:[{actTS}] - Err:[{alertType.errCode}]: {json.dumps(alertType,cls=MUT.AlertMailTypeEncoder)} %s"
    if eDescr is None:
        SM.sendProxyMail(errMsg, alertType, '%s! TS:%d' % ( _subj, actTS))
        logging.error(logErrMsg, errMsg)
        writeErrorSql(errMsg, alertType,_subj )
    else:
        exception_type, exception_value, tracebackDummy = eDescr
        errMsg += f"\r\n\r\nException:{exception_type} / {exception_value}\r\n{SysTB.format_exc()}"
        if exception_type in ( MUT.MyProgramFlowWarningException, MUT.MyProgramFlowErrorException ):
            logging.debug(logErrMsg, errMsg)
        else:
            SM.sendProxyMail(errMsg, alertType, '%s! TS:%d' % ( _subj, actTS))
            logging.error(logErrMsg, errMsg)
            writeErrorSql(errMsg, alertType,_subj )

def writeErrorSql(errMsg:str, alertType:MUT.AlertMailType, _subj:str='genericDirectWrite', ts:int=0):
    if ts == 0:
        ts = getTS()
    mySqlIntance.writeError(_subj, errMsg, alertType, ts)
    logging.error(errMsg)
#########################################################################################
# MySQL Wrapper section endz....
#########################################################################################
def getSymbolCustomerList():
    # unasId, symbolId, symbolCode
    cur = FBU.doSql('select cast(substring("Code" from 5) as integer) as UnasId, "Id", "Code" from "Customer" where "Id" > 0 and "Code" like ? ' , ('UC_-%',))
    rows = cur.fetchall()
    cur.close()
    return rows

def processControl(req:str):
    return f"Response:{req.upper()}"

def isClientIpDisabled( clientIp ):
    ip, port = clientIp
    putIntoClientList(ip)
    if not UNASCOMM_MASTER_CHALLENGE:
        return False # Challenge not enabled
    mc = challengeMasterPromoter(ip)
    return True if unasContext.masterClient is None else  unasContext.masterClient.ip != ip # TODO ez igy nem jo! Elobb biztosan tudnom kellene miert nics masterclienta promoter miatt

# TODO Not Ready Yet! Under development !!!
def challengeMasterPromoter(ip:str):
    if unasContext.masterClient is None:
        unasContext.masterClient = unasContext.clientList[ip]
        unasContext.masterClient.isMaster = True
    return unasContext.masterClient

def putIntoClientList(ip:str):
    clients = getUnasContext().clientList
    client = clients.get(ip)
    if client is None:
        client = MUT.ProxyClient(ip)
        clients[ip] = client
    else:
        pass
    client.lastActive = getCurrTime()

def trimXmlItem(itm, tag):
    if len(itm.findall(tag)) > 0:
        val = itm.findtext(tag)
        if len(val) > len(val.strip()):
            itm[tag]._setText(val.strip())
    
def trimAddressAttributes(addr):
    trimXmlItem(addr,"Name")
    trimXmlItem(addr,"ZIP")
    trimXmlItem(addr,"City")
    trimXmlItem(addr,"Street")
    trimXmlItem(addr,"StreetName")
    trimXmlItem(addr,"StreetType")
    trimXmlItem(addr,"StreetNumber")
    trimXmlItem(addr,"County")
    trimXmlItem(addr,"Country")
    trimXmlItem(addr,"CountryCode")
    trimXmlItem(addr,"TaxNumber")
    trimXmlItem(addr,"EUTaxNumber")

#
# Log/Xmlfile Rotate
#
## Kell ez? A deveben pont ezt csinalom, assszem
def batchMethodWrapper(configItemName, methodName:str=None, *args, **kwargs ):
    prc = next((x for x in  BATCH_PROCESSES if   list(filter(lambda key: key == configItemName, x))), {}) or {}
    if methodName is None:
        methodName = prc.get('method')
    eval( f"{methodName}(prc, args, kwargs)")
#
def archiveLogFiles(prc, args, kwargs): # szerintem ez csak hetente kell
    '''tar.gz a logz/*.log file-okat EXCEPT utolso (maxIndex) file-t?
       prc[preservetime]::(defa90 nap) - nal regebbi fileokat torli a logz-z kvt-ban'''
    logPath  = prc.get('filePath')
    maxIdx=0
    excludeFilename = None
    # find maxIndex/lastDate file
    for f in os.listdir(logPath):
      if f.endswith('log'):
          idx = -1  if '-' not in f else int(f[1+f.rindex('-'):-4])
          if idx > maxIdx:
            maxIdx = idx
            excludeFilename = f
            ctime = os.stat( f'{logPath}/{f}' ).st_ctime
    # tar cvf syxProxyLog-`currDateStr-`timeStamp-Az egyediseg miatt`.tgz -exclude lastFile *.log
    if maxIdx > 0:
        currDateStr = datetime.today().strftime('%Y-%m-%d')
        excludeStr = '' if excludeFilename is None else f'--exclude {excludeFilename}'
        cmd = f"tar zcvf {prc.get('archivePath')}/syxProxyLog-{currDateStr}-{UtcNow()}.tgz {excludeStr} --remove-files {logPath}/*.log"
        os.system(cmd)
    # remove older than UtNow - 86400*prc[reservetime]
    cmd = f"find {prc.get('archivePath')} -mtime +{prc.get('preserveDays')}"
    os.system(cmd)

def archiveXmlFiles(prc, args, kwargs): # ez meg talan nem is kell, a rotate csinalhatja
    '''tar.gz a xmlfiles/*.xml and move to ../xmlfiles-z/'''
    currDateStr = datetime.today().strftime('%Y-%m-%d')

    cmd = f"tar zcvf {prc.get('archivePath')}/syxProxyXmlz-{currDateStr}-{UtcNow()}.tgz  --remove-files {prc.get('filePath')}/*.log"
    os.system(cmd)
    #
    # remove older than UtNow - 86400*prc[reservetime]
    cmd = f"find {prc.get('archivePath')} -mtime +{prc.get('preserveDays')}"
    os.system(cmd)

from stat import *
def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file
       >>>  https://docs.python.org/3/library/stat.html'''
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.lstat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

def visitfile(file):
    print('visiting', file)

def testWalkTree(path="./"):
    walktree(path, visitfile)
