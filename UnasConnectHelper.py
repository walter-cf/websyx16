import logging
import requests
import datetime as date
import urllib.parse as urlParse
import UnasAuth
import MyUtils as MU
import MySmtpClient as SM
from lxml import objectify
#
#  neworder, cancelOrder, returnOrder
#
#
# MARKETPLACE_URL https://marketplace.emag.hu https://marketplace.emag.pl
# MARKETPLACE_API_URL https://marketplace-api.emag.hu/api-3 https://marketplace-api.emag.pl/api-3
# MARKETPLACE_API_URL/resource/action
#   Ex: https://marketplace-api.emag.ro/api-3/product_offer/save
#   RESOURCES AND AVAILABLE ACTIONS
#   Resource Resource URL Available actions
#   product_offer MARKETPLACE_API_URL/product_offer read save count match
#   measurements MARKETPLACE_API_URL/measurements save
#   offer_stock MARKETPLACE_API_URL/offer_stock/{resourceId}
#   campaign_proposals MARKETPLACE_API_URL/campaign_proposals save
#   order MARKETPLACE_API_URL/api-3/order read save count acknowledge
#   order/attachments MARKETPLACE_API_URL/order/attachments save
#   message MARKETPLACE_API_URL/message read save count
#   category MARKETPLACE_API_URL/category read count
#   vat MARKETPLACE_API_URL/vat read
#   handling_time MARKETPLACE_API_URL/handling_time read
#   locality MARKETPLACE_API_URL/locality read count
#   courier_accounts MARKETPLACE_API_URL/courier_accounts read
#   awb MARKETPLACE_API_URL/awb read save
#   rma MARKETPLACE_API_URL/rma read save
#   invoice/categories MARKETPLACE_API_URL/api-3/invoice/categories read
#   invoice MARKETPLACE_API_URL/api-3/invoice read
#   customer-invoice MARKETPLACE_API_URL/api-3/customer-invoice read7
#
#   Below a code example using the resource "category" and the action "read"
#   Resource Example Context
#   category/read     reading_categories. #   txt
#   http method: POST
#   The API needs authorization and has an IP level filtering. Before testing, sellers should provide a list of #
#

def unasGetOrderIZE_OLD(token, invoicestatus):
    # fromDay="2023.10.04"
    # today = date.datetime.today()
    # todayStr = today.strftime("%Y.%m.%d")
    # invStatus = '' if invoiceStatus is None else '<InvoiceStatus>'+ invoiceStatus +'</InvoiceStatus>'
    
    # dateStr  = '<TimeStart>' + str(MU.UtcNow(MU.GETORDER_INTERVAL)) +'</TimeStart>'  # 1 ora
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><InvoiceStatus>'+ status +'</InvoiceStatus><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    # xmlParam = MU.XMLTAG + '<Params>' + dateStr + invStatus +'</Params>'
    pass

def unasGetOrderNew():
    if MU.IGNORE_BLOCKED_UNAS:
        return MU.ORDERSCUSTOMER_TESTDATA1

    xmlParam = MU.XMLTAG + '<Params><StatusID>%i</StatusID></Params>' % MU.ORDER_STATUS_NEW
    return doPostReq('getOrder', xmlParam)

def unasSetOrderStatus( orderKey, status, symbolId, statusEmail = False, statusMessage = None):
    xmlParam = MU.XMLTAG + '''<Orders><Order>
        <Action>modify</Action>
        <Key>%s</Key>
        %s
        <StatusEmail>%s</StatusEmail>
        <Params><Param><Name>symbolId</Name><Value>%i</Value></Param></Params>
        </Order></Orders>
    ''' % (orderKey, "" if status is None else "<Status>%s</Status><StatusDetail>%s</StatusDetail>" % (status,statusMessage),
                            "Yes" if statusEmail else "No", symbolId)
    #
    return doPostReq('setOrder', xmlParam)

def unasGetOrderBy( tag, val): # elso ID : 146194506
    xmlParam = MU.XMLTAG + '<Params><{0}>{1}</{0}></Params>'.format(tag, val)
    return doPostReq('getProduct', xmlParam)

def unasGetProducts( status, limitStart, limitNum):
    if MU.IGNORE_BLOCKED_UNAS:
        return MU.PRODUCT_TESTDATA1

    today = date.datetime.today()
    dateStr  = '<TimeStart>' + str(MU.UtcNow(MU.GETPRODUCT_INTERVAL)) +'</TimeStart>'  # 1 ora
    limit = "<LimitNum>{0}</LimitNum><LimitStart>{1}</LimitStart>".format(limitNum, limitStart)
    #
    xmlParam = MU.XMLTAG + '<Params><State>live</State><ContentType>full</ContentType>' + limit + dateStr + '</Params>'
    ##  xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><LimitNum>3</LimitNum><ContentType>full</ContentType></Params>'
    # lmn = "<LimitStart>{0}</LimitStart>".format(limitStart) if limitStart >=0 else "<xxx></xxx>"
    # lms = "<LimitNum>{0}</LimitNum>".format(limitNum) if limitNum >=0 else "<yyyy></yyyy>"
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params>{0}{1}<ContentType>full</ContentType></Params>'.format(lmn, lms )
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><Id>702433156</Id><ContentType>full</ContentType></Params>'
    return doPostReq('getProduct', xmlParam)

def unasGetProductByAzon(xmlItem, xmlValue):
    xmlParam = MU.XMLTAG + '<Params><{0}>{1}</{0}></Params>'.format(xmlItem, xmlValue)
    return doPostReq('getProduct', xmlParam)

def unasGetStorage(tag = None, val = None):
    xmlTag = '<{0}>{1}</{0}>'.format(tag, val.replace('Q','/')) if tag is not None else '<Type>file</Type>' # type: ignore
    xmlParam = MU.XMLTAG + '<Params>'+ xmlTag +'</Params>'
    return doPostReq('getStorage', xmlParam)

def unasGetInquirers(prodId):
    return None

def unasGetActiveCustomers():
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><ContentType>full</ContentType></Params>'
    responseText =  doPostReq('getCustomer', xmlParam)
    xml = bytes(bytearray(responseText, encoding="utf-8"))
    return xml

def unasGetActiveProducts( limitNum, limitStart ):
    if MU.UnasProductWebCategoryId is None:
        xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><Name>%s</Name><ContentType>minimal</ContentType></Params>' % MU.UnasProductWebCategoryName
        responseText =  doPostReq('getProduct', xmlParam)

        catObj = objectify.fromstring(bytes(responseText, 'utf-8'), None)
        if (len(catObj.getchildren()) < 1):
            MU.UnasProductWebCategoryId = -1
        else:
            cid = catObj.Category.Id
            if cid.text is not None and len(cid.text) > 0:
                MU.UnasProductWebCategoryId = cid.text

    limitTag = ''
    if limitNum is not None and limitNum > 0:
        limitStartTag = '' if limitStart < 1 else '<LimitStart>%d</LimitStart>' % (1+limitStart)
        limitTag = '<LimitNum>%d</LimitNum>%s' % (limitNum, limitStartTag)

    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><State>live</State><ContentType>minimum</ContentType>%s</Params>' % limitTag
    responseText =  doPostReq('getProduct', xmlParam)

    xml = bytes(bytearray(responseText, encoding="utf-8"))
    return xml

def unasGetActiveOrders():
    if MU.IGNORE_BLOCKED_UNAS:
        return MU.ORDERSCUSTOMER_TESTDATA1

    xmlParam = MU.XMLTAG + '<Params><Status>open_normal</Status></Params>'
    return doPostReq('getOrder', xmlParam)
#
# POST requests for UNAS
#
# Getters
def unasGetOrderTodayFromDay(fromDay="2023.07.30"):
    todayStr = date.datetime.today().strftime("%Y.%m.%d")
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><InvoiceStatus>'+ status +'</InvoiceStatus><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    return doPostReq('getOrder', xmlParam)

def unasGetProductsFromDay(fromDay="2024.08.01"):
    todayStr = date.datetime.today().strftime("%Y.%m.%d")
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><InvoiceStatus>'+ status +'</InvoiceStatus><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><State>live</State><Params><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    return doPostReq('getProduct', xmlParam)

def unasGetCustomers(tag = None, val = None):
    if MU.IGNORE_BLOCKED_UNAS:
        return MU.CUSTOMER_TESTDATA1

    if (tag == "all"):
        xmlParam = MU.XMLTAG + '<Params><ContentType>full</ContentType></Params>'
    else:
        xmlTag = '<{0}>{1}</{0}>'.format(tag, val) if tag is not None else '<ModTimeStart>{0}</ModTimeStart>'.format( str(MU.UtcNow(MU.GETCUSTOMER_INTERVAL)))
        xmlParam = MU.XMLTAG + '<Params>'+ xmlTag +'</Params>'
    return doPostReq('getCustomer', xmlParam)

# Setters
def unasProduct_Direct(xml):
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Products>{0}</Products>'.format(xml)
    return doPostReq('setProduct', xmlParam)

def UploadCustomersXml(xmlPart):
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Customers>' + xmlPart +'</Customers>'
    return doPostReq('setCustomer', xmlParam)

def unasFreeXml(action, xmlTag):
    xmlParam = MU.XMLTAG + xmlTag
    return doPostReq(action, xmlParam)

def doPostReq(action, xmlParam):
    MU.checkCommError()
    token = UnasAuth.doAuth()
    MU.createStatEntry(action, xmlParam)
    if MU.isLogLevelTrace():
        print( "UCh-req:", action,  " TS:%s", MU.getTS())
        logging.debug("UCh-req:%ss TS:%d, Token:%s", action, MU.getTS(), token)
        logging.debug("xmlParam: %s", xmlParam)
    else:
        logging.debug("UCh-req:%s", action)
    x = requests.post("%s/%s" % (MU.UNASAPI_URL, action), data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if x.status_code == 200:
        logging.debug("Req returned st:%s", x.status_code)
        MU.createStatEntryOK(x.text)
        if MU.isLogLevelTrace():
            logging.debug("response: %s", x.text)
    else:
        MU.createStatEntryERR(x.status_code, x.text)
        logging.error("Req returned st:%s", x.status_code)
        logging.info("xmlParam: %s", x.text)
        msg = "ERROR - UCh-req:%ss. TS:%d, Token:%s" % (action, MU.getTS(), token)
        msg += '\r\n\r\nxmlResp-status:%s\r\nResponse:%s' % (x.status_code, x.text)
        SM.sendAlertMail(msg, '[UNAS-Comm-Err] Sikertelen UNAS keres ST:%s' % x.status_code )
    return x.text
#
# Posts-End
UNAS_SETSYMBOLID_XML = """<Customer>
        <Action>modify</Action>
        <Id>%i</Id>
        <Params>
            <Param>
                <Name>symbolId</Name>
                <Value>%s</Value>
            </Param>
            <Param>
                <Name>symbolCode</Name>
                <Value>%s</Value>
            </Param>
        </Params>
    </Customer>
"""
UNAS_SETPRODUCTSYMBOLID_XML = """<Products>
    <Product>
        <Action>modify</Action>
        <Id>%i</Id>
        <Sku>%s</Sku>
        <Params>
            <Param>
                <Name>symbolId</Name>
                <Value>%s</Value>
            </Param>
        </Params>
    </Product>
</Products>
"""
def updateProductSymbolId(unasId, symbolId, sku):
    xmlParam = UNAS_SETPRODUCTSYMBOLID_XML % (unasId, sku, '' if symbolId <= 0 else str(symbolId) )
    return doPostReq('setProduct', xmlParam)

def updateCustomerSymbolId(unasId, symbolId, symbolCode):
    xmlParam = UNAS_SETSYMBOLID_XML % (unasId, str(symbolId), symbolCode)
    return updateCustomer(xmlParam)

def updateCustomer(xmlPart):
    xmlParam = f"{MU.XMLTAG}<Customers>{xmlPart}</Customers>"
    return doPostReq('setCustomer', xmlParam)

UNAS_DELETECUSTOMER_XML = "<CustomersUp><Customer><Action>delete</Action><Id>%i</Id></Customer></CustomersUp>"
def deleteCustomer(unasId):
    xmlParam = UNAS_DELETECUSTOMER_XML % unasId
    return doPostReq('setCustomer', xmlParam)
#
# Cats
#
UNAS_DELETECATEGORY_XML = "<Category><Action>delete</Action><Id>%s</Id></Category>"
def deleteCats(catIds):
    xmlParam = ''
    if catIds is None:
        return '<Categories />'
    
    for cid in catIds:
        xmlParam += UNAS_DELETECATEGORY_XML % str(cid)
    if len(xmlParam) > 0:
        xmlParam =  MU.XMLTAG + f"<Categories>{xmlParam}</Categories>"
        return doPostReq('setCustomer', xmlParam)
    return '<Categories />'

def getCats(tag = None, val = None):
    xmlTag = '' if tag is None else '<{0}>{1}</{0}>'.format(tag, str(val).replace('Q','/'))
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params>%s<ContentType>minimal</ContentType></Params>' % xmlTag
    return doPostReq('getCategory', xmlParam)

xxxxxxxxxxxxxxxxxxxxxx  = """
	<Category>
		<Action>add</Action>		
		<Name><![CDATA[N�i divat]]></Name>
		<Url><![CDATA[https://design1600.unas.hu/noi-divat]]></Url>
		<SefUrl><![CDATA[noi-divat]]></SefUrl>
		<AltUrl><![CDATA[https://unas.hu]]></AltUrl>
		<AltUrlBlank>yes</AltUrlBlank>
		<Display>
			<Page>yes</Page>
			<Menu>no</Menu>
		</Display>
		<Texts>
			<Top><![CDATA[<p>Kateg�ria felett megjelen� sz�veg</p>]]></Top>
			<Bottom><![CDATA[<p>Kateg�ria alatt megjelen� sz�veg</p>]]></Bottom>
			<Menu><![CDATA[Kateg�ria men� sz�veg]]></Menu>
		</Texts>
		<Meta>
			<Keywords><![CDATA[keywords]]></Keywords>
			<Description><![CDATA[ez lesz a kateg�ria description]]></Description>
			<Title><![CDATA[A kateg�ria title]]></Title>
			<Robots>index, follow</Robots>
		</Meta>		
		<Image>			
			<OG>https://unas.hu/image.jpg</OG>
		</Image>
		<Tags>
		    <Tag>tag 1</Tag>
		    <Tag>tag 2</Tag>
		</Tags>
	</Category>"""
UNAS_CREATECATEGORY_XML = "<Category><Action>add</Action><Name><![CDATA[%s]]></Name><Display><Page>yes</Page><Menu>no</Menu></Display></Category>"
def addCatBbyName(catName:str):
    catXml = UNAS_CREATECATEGORY_XML % catName
    return addCatsXml(catXml)

def addCatsXml(xmlTag:str):
    xmlParam =  MU.XMLTAG + f"<Categories>{xmlTag}</Categories>"
    return doPostReq('setCategory', xmlParam)

def unasDirectXml(action, xmlTag:str, trailer = None):
    xmlParam =  MU.XMLTAG + xmlTag if trailer is None else f"<{trailer}>{xmlTag}</{trailer}>"
    return doPostReq(action, xmlParam)
#
# Prods
#
UNAS_DELETEPRODUCT_XML = "<Product><Action>delete</Action><Id>%s</Id></Product>"
def deleteProds(catIds):
    xmlParam = ''
    if catIds is None:
        return '<Products />'
    
    for cid in catIds:
        xmlParam += UNAS_DELETEPRODUCT_XML % str(cid)
    if len(xmlParam) > 0:
        xmlParam =  MU.XMLTAG + f"<Products>{xmlParam}</Products>"
        return doPostReq('setCategory', xmlParam)
    return '<Categories />'

def getProds(tag = None, val = None):
    xmlTag = '' if tag is None else '<{0}>{1}</{0}>'.format(tag, str(val).replace('Q','/'))
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params>%s<ContentType>minimal</ContentType></Params>' % xmlTag
    return doPostReq('getProduct', xmlParam)

def addProdsXml(xmlTag:str):
    token = UnasAuth.doAuth()
    xmlParam =  MU.XMLTAG + f"<Categories />{xmlTag}</Categories>"
    return doPostReq('setProduct', xmlParam)

