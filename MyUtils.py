from time import time
from datetime import datetime, timezone
from markdown import  markdown, markdownFromFile
from typing import List

import yaml
import json
import logging
#

import MyUtilsTypes
import MyBatch
from UnasProductCache import UnasProductCache as UPC
import UnasCustomerCache as UCC
import UnasConnectHelper as UCH
import UnasOrderCache as UOC
import FdbUtils as FBU
import MySqlUtils as MyDB
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from lxml import objectify
from typing import Dict

import mysql.connector
import json

CONFIG_FILE = None
def reReadYaml():
	return readYaml(CONFIG_FILE)

def readYaml(yamlFile) -> str:
    global CONFIG_FILE
    CONFIG_FILE = yamlFile 
    with open(yamlFile, 'r') as stream:
        try:
            cfg = yaml.safe_load(stream)
            if isLogLevelInfo():
                print(cfg)
            setConstants(cfg)
        except yaml.YAMLError as exc:
            print(exc)
    return json.dumps(cfg)

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
	global BATCH_PROCESSES, BATCH_GRANULARITY
	BATCH_PROCESSES   = valDef(cfg["batch"]["processes"], [])
	BATCH_GRANULARITY = valDef(cfg["batch"]["granularity"], 10)

	global FB_HOST, FB_USER, FB_PASSWORD, FB_DBDATA_ROOT, FB_DBDATA_DEFAULT
	FB_HOST              = valDef(cfg["firebird"]["dbHost"], FB_HOST          )
	FB_USER              = valDef(cfg["firebird"]["dbUser"], FB_USER          )
	FB_PASSWORD          = valDef(cfg["firebird"]["dbPass"], FB_PASSWORD      )
	FB_DBDATA_ROOT       = valDef(cfg["firebird"]["dbRoot"], FB_DBDATA_ROOT   )
	FB_DBDATA_DEFAULT    = valDef(cfg["firebird"]["dbFile"], FB_DBDATA_DEFAULT)
 
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
  
	CurrentLogLevel = MyUtilsTypes.LogLvl.getLevelFromStr(LOGLEVEL)
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
	global SYMBOLVOUCHERSEQUENCECODE, SYMBOLORDERIDPREFIX, SYMBOLORDERSTATUS
	SYMBOLVOUCHERSEQUENCECODE  = cfg["unas"]["order"]["vouchersequencecode"]
	SYMBOLORDERIDPREFIX        = cfg["unas"]["order"]["symbolOrderPrefix"]
	SYMBOLORDERSTATUS        = cfg["unas"]["order"]["symbolOrderStatusNew"]
	# Intervals
	global GETPRODUCT_INTERVAL, GETCUSTOMER_INTERVAL, CUSTOMER_CYCLIC_INTERVAL
	GETPRODUCT_INTERVAL      = cfg["unas"]["product"]["getInterval"]
	GETCUSTOMER_INTERVAL     = cfg["unas"]["customer"]["getInterval"]
	CUSTOMER_CYCLIC_INTERVAL = cfg["unas"]["customer"]["ignoreCyclicInterval"]
	global CUSTOMER_COUNTRIES, WAREHOUSES, CUSTOMER_BULK, CUSTOMER_CODE_PREFIXES, CREATE_CUSTOMER_MISSING, CUSTOMER_FORCENEW, HANDLE_CUSTOMERADDRESS
	# Customer
	CUSTOMER_COUNTRIES     = cfg["unas"]["customer"]["countries"]	# print(list(CUSTOMER_COUNTRIES.keys())[list(CUSTOMER_COUNTRIES.values()).index('Magyarország')])
	CUSTOMER_BULK          = cfg["unas"]["customer"]["bulk"]
	CUSTOMER_CODE_PREFIXES = cfg["unas"]["customer"]["codePrefix"]
	CREATE_CUSTOMER_MISSING = cfg["unas"]["customer"]["cerateMissingCustomer"]
	CUSTOMER_FORCENEW       = cfg["unas"]["customer"]["forceNewState"]
	HANDLE_CUSTOMERADDRESS  = nullSafe( cfg["unas"]["customer"], "handleCustomerAddress", False)
	# Inventory warehouses
	WAREHOUSES            = cfg["unas"]["inventory"]["warehouses"]

	global 	ORDER_STATUS_NEW, ORDER_STATUS_ACCEPTED, ORDER_STATUS_PREP,ORDER_STATUS_SHIP, ORDER_STATUS_CLOSE,ORDER_STATUS_RETURN, ORDER_STATUS_CANCEL
	# Order params - statuses
	ORDER_STATUS_NEW      = cfg["unas"]["order"]["status"]['new']
	ORDER_STATUS_ACCEPTED = cfg["unas"]["order"]["status"]['accepted']
	ORDER_STATUS_PREP     = cfg["unas"]["order"]["status"]['prepared']
	ORDER_STATUS_SHIP     = cfg["unas"]["order"]["status"]['shipping']
	ORDER_STATUS_CLOSE    = cfg["unas"]["order"]["status"]['closed']
	ORDER_STATUS_RETURN   = cfg["unas"]["order"]["status"]['returned']
	ORDER_STATUS_CANCEL   = cfg["unas"]["order"]["status"]['cancel']

	# Order FLOW Control
	global 	ORDER_HandleUnregistered, ORDER_getMissingCust, ORDER_autoAcknowledge
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
	global UNASCOMM_MAXERRCNT, UNASCOMM_MAXLOGINERRCNT, UNASCOMM_BLOCKEDTIME, UNASCOMM_SENDPACKETMAX 
	UNASCOMM_MAXERRCNT      = cfg["unas"]["commstat"]["maxerrorcnt"]
	UNASCOMM_MAXLOGINERRCNT = cfg["unas"]["commstat"]["maxloginerr"]
	UNASCOMM_BLOCKEDTIME    = cfg["unas"]["commstat"]["blockedTimeMax"]
	UNASCOMM_SENDPACKETMAX  = cfg["unas"]["commstat"]["sendPacketThreshold"]

#
# Utilz
#

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
        raise ValueError("Bad/Missed country: " + country)
    # else
    return None

def addCountryCode(country, code):
    CUSTOMER_COUNTRIES[code] = country

def collectCustItems(xml):
    global UnasCustomerList
    root=ET.fromstring(xml,None)
    for prod in root.getchildren():
        custId    = prod.find('Id').text
        custEmail = prod.find('Email').text
        symbolId = '0'
        symbolCode = None
        unasLastMod = prod.find('Dates')
        if unasLastMod is not None and unasLastMod.find('Modification') is not None:
            unasLastMod = prod.find('Dates').find('Modification').text
        if len(prod.findall('Params')) > 0 :
            for ppp in prod.find('Params'):
                pName = ppp.find('Name')
                if (pName.text == 'symbolId'):
                    symbolId = ppp.find('Value').text
                elif (pName.text == 'symbolCode'):
                    symbolCode = ppp.find('Value').text
        # Addresses CountryCode / TaxNUmber
        custTaxNo = None        
        for addr in prod.find('Addresses'):
                country = addr.find('Country')
                countryCode = addr.find('CountryCode')
                if addr.tag == "Invoice":
                    custTaxNo = next((x.text for x in addr if x.tag == 'TaxNumber') , None )
                cc = getCountryCode( country.text, False)
                if cc is None:
                    addCountryCode(country.text, countryCode.text)
        #
        ucc = UCC.UnasCustomerCache(int(custId), custEmail, custTaxNo, symbolCode, int(symbolId)) # type: ignore # State NotUsed yet
        for addr in prod.find('Addresses'):
            ucc.unasAddrXml.append( addr ) # type: ignore
        ucc.lastmod = 0 if unasLastMod is None else dateStrToTs( unasLastMod )
        if CUSTOMER_FORCENEW:
            ucc.state = 'new'
        if  UnasCustomerList.get(ucc.custAzon) is None:
            try:
                putCustomerIntoCache(ucc, ucc.custAzon)
            except Exception as e:
                logging.error(f"UnasCustomerCache corrupted! Err:{str(e)}, IDs:{ucc.custAzon}, unasId:{custId}")
            # end try
        elif  custId is None:
            logging.error(f"UnasCustomer DATA-ERROR! Customer-unasId is NULL UCC:" + ucc.toStr())
        elif  UnasCustomerList.get(UCC.buildCustAzonById(custId)) is None:
            putCustomerIntoCache(ucc, UCC.buildCustAzonById(custId)) # type: ignore
        else:
            logging.error(f"UnasCustomerCache corrupted! tripled custazon:{ucc.custAzon}, unasId:{custId}")
    #
    return UnasCustomerList

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

CACHE_FORCE_RELOAD_PERIOD = 10000
def checkCacheState(force: bool = False):
    global UnasCustomerList, UnasProductList, UnasOrderList, LastCacheUpdated
    if not force and UtcNow() - LastCacheUpdated > CACHE_FORCE_RELOAD_PERIOD:
        force = True
    minimunDelayed = (UtcNow() - LastCacheUpdated) > 1500 # Ha ures a cache akkor 25 percenkent force megnezem, van-e uj adat
    if force or (minimunDelayed and (len(UnasCustomerList) < 1)):
        UnasCustomerList.clear()
        retV = UCH.unasGetActiveCustomers()
        UnasCustomerList = collectCustItems(retV)
        LastCacheUpdated = UtcNow()
    if force or (minimunDelayed and (len(UnasProductList) < 1)):
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
        LastCacheUpdated = UtcNow()
    if force or minimunDelayed: # Rendelesnek nem kell a minimum delay, az lehet ures
        UnasOrderList.clear()
        retV = UCH.unasGetActiveOrders()
        UnasOrderList = collectOrderItems(retV)
        LastCacheUpdated = UtcNow()
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
    return "%i/%i/%i-%i:%i:%i" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def tsToDateSql(ts) -> str:
    dt = datetime.fromtimestamp(ts)
    return "%i-%i-%i %i:%i:%i" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def dateStrToTs(date):  # '2024.03.04 12:51:08'
    return int(datetime.strptime(date, '%Y.%m.%d %H:%M:%S').timestamp())


def mdConverter( fileName ):
    try:
        with open(fileName + '.md', 'r') as f:
            text = f.read()
            return  markdown(text)
    except OSError as e:
        return "document %s not found! Try <a href='/about'>this</a>" % fileName

def mkCustomerCode( ucc : UCC.UnasCustomerCache, prefix : str = 'unregistered'):
    prfx = CUSTOMER_CODE_PREFIXES[prefix] # type: ignore
    return f"{prfx}-{ucc.unasId}"

#				
def getCustomerFormCache(email, taxnumber, unasId ) -> UCC.UnasCustomerCache:
    ucc = UnasCustomerList.get( UCC.buildAzonData( email, taxnumber ))
    if ucc is None:
        ucc = UnasCustomerList.get( UCC.buildCustAzonById(unasId))
    if ucc is not None:
        if ucc.symbolId is None:
            ucc.symbolId = 0
        if ucc.lastmod is None:
            ucc.lastmod = 0
    return ucc # type: ignore

def putCustomerIntoCache(ucc : UCC.UnasCustomerCache, cc:str):
    azon = ucc.custAzon if cc is None else cc
    u = UnasCustomerList.get( azon )
    if u is None:
        ucc.custAzon = azon
        UnasCustomerList[azon] = ucc
    elif u.email == ucc.email and u.unasId == ucc.unasId and u.symbolId == ucc.symbolId:
        ucc.custAzon = azon
        UnasCustomerList[azon] = ucc
    else:
        raise ValueError( '[putCustomerIntoCache]:Duplicate item:' + u.toStr() + ' :*-*: '+ ucc.toStr() )
    
    
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
UnasCustomerList = dict({})
#UnasOrderList    = dict({})
UnasOrderList : Dict[str, UOC.UnasOrderCache] = dict({})
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

ORDER_STATUS_NEW      = 0
ORDER_STATUS_ACCEPTED = 0
ORDER_STATUS_PREP     = 0
ORDER_STATUS_SHIP     = 0
ORDER_STATUS_CLOSE    = 0
ORDER_STATUS_RETURN   = 0
ORDER_STATUS_CANCEL   = 0

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
# 		<code>WEB00001231</code>
#
#		<sid>4357</sid>

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
    return isLogLevel(MyUtilsTypes.LogLvl.TRACE)
def isLogLevelDebug():
    return isLogLevel(MyUtilsTypes.LogLvl.DEBUG)
def isLogLevelInfo():
    return isLogLevel(MyUtilsTypes.LogLvl.INFO)
def isLogLevelWarn():
    return isLogLevel(MyUtilsTypes.LogLvl.WARNING)

CurrentLogLevel:MyUtilsTypes.LogLvl = MyUtilsTypes.LogLvl.INFO
def isLogLevel(lvl:MyUtilsTypes.LogLvl) -> bool: 
    return lvl <= CurrentLogLevel


# get (new) Transaction ID from Tomestamp + xx as originate from
unasTransactionId:int = 0
typeMultiplier = 1000
def getNowFromTS():
    global unasTransactionId
    return int(unasTransactionId // typeMultiplier)

def getActionTypeFromTS():
    return MyUtilsTypes.UnasTransactionType(int(unasTransactionId % typeMultiplier))

def createTransactionId(tsType:MyUtilsTypes.UnasTransactionType = MyUtilsTypes.UnasTransactionType.CREATENEW):
    global unasTransactionId
    unasTransactionId = typeMultiplier * getCurrTime() + tsType
    return unasTransactionId

def getTS():
    global unasTransactionId
    return unasTransactionId

def createStatEntry(action:str, xmlParam:str): # login, getXXX , setXXX, procycontrol, test, TEST ???
    unasContext.statEntryMySqlId = createStatEntrySql(action, xmlParam, tsId=getTS() )
    updateStatEntry(action)

def createStatEntryOK(resp:str = ''):
    updateStatEntryStatus(200, xml=resp, myId=unasContext.statEntryMySqlId, tsId=getTS() )
    updateStatEntryOK()

def createStatEntryERR(retCode:int, response:str):
    updateStatEntryStatus(retCode, xml=response, ts=getTS(), myId=unasContext.statEntryMySqlId )
    updateStatEntryERR(retCode)

unasContext = MyUtilsTypes.UnasContext()
def getUnasContext() -> MyUtilsTypes.UnasContext: 
    global unasContext
    return unasContext

def clearUnasContextCounter() -> MyUtilsTypes.UnasContext: 
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

def updateStatEntryERR():
    unasContext.commErrCnt = 1 + unasContext.commErrCnt

def clearCommError():
    unasContext.commBlocked = 0
    unasContext.commErrCnt = 0
    unasContext.lastAlertMailSent = 0

UNASCOMM_MAXERRCNT = 3
UNASCOMM_MAXLOGINERRCNT = 3
UNASCOMM_BLOCKEDTIME = 1800
UNASCOMM_SENDPACKETMAX = 1900

def checkCommError():
    if unasContext.commBlocked > 0:
        if getCurrTime() - unasContext.commBlocked > UNASCOMM_BLOCKEDTIME: # release block
            clearCommError()
        else:
            # set Context State
            unasContext.lastAction = getActionTypeFromTS().name
            # send Alert - email + lastAlertEmailType
            # unasContext.lastAlertMailSent = getCurrTime()
            raise ValueError("Communication error! action:%s, TS:%d" % (unasContext.lastAction, getTS()) )
    elif unasContext.commErrCnt > UNASCOMM_MAXERRCNT:
            unasContext.commBlocked = getCurrTime()
            raise ValueError("Communication error! action:%s, TS:%d" % (unasContext.lastAction, getTS()) )
    elif getPacketLastHourCnt() > UNASCOMM_SENDPACKETMAX:
            unasContext.commBlocked = getCurrTime()
            raise ValueError("Communication error! action:%s, TS:%d" % (unasContext.lastAction, getTS()) )
    else:
        pass
#
# MySQL wrapper funtions
#
mySqlIntance = MyDB.MySqlWrapper()
def createStatEntrySql(action, xmlParam, tsId = getTS() ):
    sql = "INSERT INTO commstats (action, requestXml, transactionId) VALUES (%s, %s, %s)"
    val = (action, xmlParam, tsId)
    return mySqlIntance.execSql(sql, val, True )

def updateStatEntryStatus(retCode, xml:str = '', tsId:int =0, myId:int = 0):
    if myId > 0:
        sql = "UPDATE commstats set responseCode=%s, responseXml = %s WHERE Id = %s"
        val = (retCode, xml, myId)
    else:
        sql = "UPDATE commstats set responseCode=%s, responseXml = %s WHERE transactionId = %s"
        val = (retCode, xml, tsId)
    return mySqlIntance.execSql(sql, val, True )

def getPacketLastHourCnt(fromTime:int=0, toTime:int = 0):
    result =  mySqlIntance.doSql(
		    "SELECT count(*) cnt from commstats WHERE createdAt between %s and %s", (
                tsToDateSql( fromTime if fromTime > 0 else UtcNow(3600)),
                tsToDateSql( toTime if toTime > 0 else getCurrTime())     ))
    return result[0]['cnt']

