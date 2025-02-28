import logging
import requests
import datetime as date
import urllib.parse as urlParse
import UnasAuth
import MyUtils as MU
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

    token = UnasAuth.doAuth()
    xmlParam = MU.XMLTAG + '<Params><StatusID>%i</StatusID></Params>' % MU.ORDER_STATUS_NEW
    x = requests.post( MU.UNASAPI_URL + '/getOrder', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getOrder')
        print(xmlParam)
        print(x.status_code)
        print(x.text)
    return x.text

def unasSetOrderStatus( orderKey, status, symbolId, statusEmail = False, statusMessage = None):
    token = UnasAuth.doAuth()
    statusMessageStr = "" if statusMessage is None else "<StatusDetails>%s</StatusDetails>" % statusMessage
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
    x = requests.post(  MU.UNASAPI_URL + '/setOrder', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token } )
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/setOrder')
        print(xmlParam)
        print(x.status_code)
        print(x.text)
    return x.text

def unasGetOrderBy( tag, val): # elso ID : 146194506
    token = UnasAuth.doAuth()
    xmlParam = MU.XMLTAG + '<Params><{0}>{1}</{0}></Params>'.format(tag, val)
    x = requests.post(MU.UNASAPI_URL + '/getOrder', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    return x.text if x.status_code == 200 else None
    ## #fromDay="2023.10.04"
    ## #today = date.datetime.today()
    ## #todayStr = today.strftime("%Y.%m.%d")
    ## invStatus = '' if invoiceStatus is None else '<InvoiceStatus>'+ invoiceStatus +'</InvoiceStatus>'
    ## dateStr  = '<TimeStart>' + str(MU.UtcNow(3600)) +'</TimeStart>'  # 1 ora
    ## # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><InvoiceStatus>'+ status +'</InvoiceStatus><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    ## xmlParam = MU.XMLTAG + '<Params>' + dateStr + invStatus +'</Params>'
    ## x = requests.post(  MU.UNASAPI_URL + '/getOrder', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    ## print(x.status_code)
    ## print(x.text)
    ## return x.text

def unasGetProducts( status, limitStart, limitNum):
    if MU.IGNORE_BLOCKED_UNAS:
        return MU.PRODUCT_TESTDATA1

    token = UnasAuth.doAuth()
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

    x = requests.post(MU.UNASAPI_URL + '/getProduct', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getProduct')
        print(xmlParam)
        print(x.status_code)
        print(x.text)
    return x.text

def unasGetProductByAzon(xmlItem, xmlValue):
    token = UnasAuth.doAuth()
    xmlParam = MU.XMLTAG + '<Params><{0}>{1}</{0}></Params>'.format(xmlItem, xmlValue)
    x = requests.post(MU.UNASAPI_URL + '/getProduct', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getProduct')
        print(xmlParam)
        print(x.status_code)
        print(x.text)
    return x.text

def unasGetStorage(tag = None, val = None):
    token = UnasAuth.doAuth()
    xmlTag = '<{0}>{1}</{0}>'.format(tag, val.replace('Q','/')) if tag is not None else '<Type>file</Type>' # type: ignore
    xmlParam = MU.XMLTAG + '<Params>'+ xmlTag +'</Params>'
    x = requests.post(MU.UNASAPI_URL + '/getStorage', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getStorage')
        print(xmlParam)
        print(x.status_code)
        print(x.text)
    return x.text

def unasGetInquirers(prodId):
    token = UnasAuth.doAuth()
    return None

def unasGetActiveCustomers():
    token = UnasAuth.doAuth()
    tsStart = MU.UtcNow(0)
    logging.info("GET CustomersCache started:%d", tsStart)
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><ContentType>full</ContentType></Params>'
    x = requests.post(MU.UNASAPI_URL + '/getCustomer', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getCustomer')
        print(xmlParam)
        print(x.status_code)
        print(x.text)

    xml = bytes(bytearray(x.text, encoding="utf-8"))
    #_retV = MU.collectCustItems(xml)
    logging.info("GOT CustomersCache in:%i sec", MU.UtcNow(0) - tsStart)
    return xml

def unasGetActiveProducts( limitNum, limitStart ):
    tsStart = MU.UtcNow(0)
    token = UnasAuth.doAuth()
    logging.info("GET ProductCache started:%d", tsStart)
    if MU.UnasProductWebCategoryId is None:
        xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><Name>%s</Name><ContentType>minimal</ContentType></Params>' % MU.UnasProductWebCategoryName
        x = requests.post(MU.UNASAPI_URL + '/getCategory', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
        if MU.isLogLevelTrace():
            print(x.text)

        catObj = objectify.fromstring(bytes(x.text, 'utf-8'), None)
        if (len(catObj.getchildren()) < 1):
            MU.UnasProductWebCategoryId = -1
        else:
            cid = catObj.Category.Id
            if cid.text is not None and len(cid.text) > 0:
                MU.UnasProductWebCategoryId = cid.text
    # MU.UnasProductWebCategoryId

    limitTag = ''
    if limitNum is not None and limitNum > 0:
        limitStartTag = '' if limitStart < 1 else '<LimitStart>%d</LimitStart>' % (1+limitStart)
        limitTag = '<LimitNum>%d</LimitNum>%s' % (limitNum, limitStartTag)

    # limitTag = '' if limitNum is None or limitNum < 5 else '<LimitNum>%d</LimitNum><LimitStart>%d</LimitStart>' % (limitNum, limitStart)
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><State>live</State><ContentType>minimum</ContentType>%s</Params>' % limitTag
    
    x = requests.post(MU.UNASAPI_URL + '/getProduct', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getProduct')
        print(x.status_code)
        print(x.text)

    xml = bytes(bytearray(x.text, encoding="utf-8"))

    #_retV = MU.collectProdItems(xml)
    logging.info("GOT ProductCache in:%i sec", MU.UtcNow(0) - tsStart)
    return xml

def unasGetActiveOrders():
    if MU.IGNORE_BLOCKED_UNAS:
        return MU.ORDERSCUSTOMER_TESTDATA1

    token = UnasAuth.doAuth()
    xmlParam = MU.XMLTAG + '<Params><Status>open_normal</Status></Params>'
    x = requests.post( MU.UNASAPI_URL + '/getOrder', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getOrder')
        print(xmlParam)
        print(x.status_code)
        print(x.text)
    return x.text
#
# POST requests for UNAS
#
# Getters
def unasGetOrderTodayFromDay(fromDay="2023.07.30"):
    token = UnasAuth.doAuth()
    today = date.datetime.today()
    todayStr = today.strftime("%Y.%m.%d")
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><InvoiceStatus>'+ status +'</InvoiceStatus><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    x = requests.post(MU.UNASAPI_URL + '/getOrder', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelDebug():
        print(x.status_code)
        print(x.text)
    return x.text

def unasGetProductsFromDay(fromDay="2024.08.01"):
    token = UnasAuth.doAuth()
    todayStr = date.datetime.today().strftime("%Y.%m.%d")
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><InvoiceStatus>'+ status +'</InvoiceStatus><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><State>live</State><Params><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    x = requests.post(MU.UNASAPI_URL + '/getProduct', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelDebug():
        print(x.status_code)
        print(x.text)
    return x.text

def unasGetCustomers(tag = None, val = None):
    if MU.IGNORE_BLOCKED_UNAS:
        return MU.CUSTOMER_TESTDATA1
    token = UnasAuth.doAuth()
    if (tag == "all"):
        xmlParam = MU.XMLTAG + '<Params><ContentType>full</ContentType></Params>'
    else:
        xmlTag = '<{0}>{1}</{0}>'.format(tag, val) if tag is not None else '<ModTimeStart>{0}</ModTimeStart>'.format( str(MU.UtcNow(MU.GETCUSTOMER_INTERVAL)))
        xmlParam = MU.XMLTAG + '<Params>'+ xmlTag +'</Params>'
    x = requests.post(MU.UNASAPI_URL + '/getCustomer', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getCustomer')
        print(xmlParam)
        print(x.status_code)
        print(x.text)
    return x.text

# Setters
def unasProduct_Direct(xml):
    token = UnasAuth.doAuth()
    #print(ET.tostring(ET.XML('<aaa>' + xml.strip('\n') + '</aaa>'), pretty_print=True, encoding='utf-8')) # type: ignore
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Products>{0}</Products>'.format(xml)
    x = requests.post( MU.UNASAPI_URL + '/setProduct', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelDebug():
        print(x.status_code)
        print(x.text)
    return x.text
#     return '''<Products>
# 	<Product>
# 		<Id>159850145</Id>
# 		<Sku>FN0571</Sku>
# 		<Action>modify</Action>
# 		<Status>ok</Status>
# 	</Product></Products>
#     '''

def UploadProductsXml(xmlPart):
    token = UnasAuth.doAuth()
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Products>{0}</Products>'.format( xmlPart )
    x = requests.post( MU.UNASAPI_URL + '/setProduct', data=xmlParam.encode("UTF-8"), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelDebug():
        print(x.status_code)
        print(x.text)
    return x.text

def UploadCustomersXml(xmlPart):
    token = UnasAuth.doAuth()
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Customers>' + xmlPart +'</Customers>'
    x = requests.post(MU.UNASAPI_URL + '/setCustomer', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelDebug():
        print(x.status_code)
        print(x.text)
    return x.text    

def unasFreeXml(action, xmlTag):
    token = UnasAuth.doAuth()
    print("Token: %s" % token)
    logging.info("Token: %s", token)
    xmlParam = MU.XMLTAG + xmlTag
    x = requests.post("%s/%s" % (MU.UNASAPI_URL, action), data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    print(x.status_code)
    print(x.text)
    return x.text
#
# Posts-End
UNAS_SETSYMBOLID_XML = """<Customers>
    <Customer>
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
</Customers>
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
            <Param>
                <Name>VTSZ</Name>
                <Value>%s</Value>
            </Param>
        </Params>
    </Product>
</Products>
"""
def updateProductSymbolId(unasId, symbolId, sku):
    token = UnasAuth.doAuth()
    xmlParam = UNAS_SETPRODUCTSYMBOLID_XML % (unasId, sku, str(symbolId), sku)
    x = requests.post(MU.UNASAPI_URL + '/setProduct', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + str(token) })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/setProduct')
        print(x.status_code)
        print(xmlParam)
        print(x.text)
    return x.text

def updateCustomerSymbolId(unasId, symbolId, symbolCode):
    token = UnasAuth.doAuth()
    xmlParam = UNAS_SETSYMBOLID_XML % (unasId, str(symbolId), symbolCode)
    x = requests.post(MU.UNASAPI_URL + '/setCustomer', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + str(token) })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/setCustomer')
        print(x.status_code)
        print(xmlParam)
        print(x.text)
    return x.text


def updateCustomer(xmlPart):
    token = UnasAuth.doAuth()
    xmlParam = f"{MU.XMLTAG}<CustomersUp>{xmlPart}</CustomersUp>"
    x = requests.post(MU.UNASAPI_URL + '/setCustomer', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + str(token) })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/setCustomer')
        print(x.status_code)
        print(xmlParam)
        print(x.text)
    return x.text

UNAS_DELETECUSTOMER_XML = "<CustomersUp><Customer><Action>delete</Action><Id>%i</Id></Customer></CustomersUp>"
def deleteCustomer(unasId):
    token = UnasAuth.doAuth()
    xmlParam = UNAS_DELETECUSTOMER_XML % unasId
    x = requests.post(MU.UNASAPI_URL + '/setCustomer', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + str(token) })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/setCustomer')
        print(x.status_code)
        print(xmlParam)
        print(x.text)
    return x.text
#
# Cats
#
UNAS_DELETECATEGORY_XML = "<Category><Action>delete</Action><Id>%s</Id></Category>"
def deleteCats(catIds):
    token = UnasAuth.doAuth()
    xmlParam = ''
    if catIds is None:
        return '<Categories />'
    
    for cid in catIds:
        xmlParam += UNAS_DELETECATEGORY_XML % str(cid)
    if len(xmlParam) > 0:
        xmlParam =  MU.XMLTAG + f"<Categories>{xmlParam}</Categories>"
        x = requests.post(MU.UNASAPI_URL + '/setCategory', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + str(token) })
        if MU.isLogLevelTrace():
            print(MU.UNASAPI_URL + '/setCategory')
            print(x.status_code)
            print(xmlParam)
            print(x.text)
        return x.text
    return '<Categories />'

def getCats(tag = None, val = None):
    token = UnasAuth.doAuth()
    xmlTag = '' if tag is None else '<{0}>{1}</{0}>'.format(tag, str(val).replace('Q','/'))
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params>%s<ContentType>minimal</ContentType></Params>' % xmlTag
    x = requests.post(MU.UNASAPI_URL + '/getCategory', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getCategory')
        print(x.status_code)
        print(x.text)
    return x.text


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
    token = UnasAuth.doAuth()
    xmlParam =  MU.XMLTAG + f"<Categories>{xmlTag}</Categories>"
    x = requests.post(MU.UNASAPI_URL + '/setCategory', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/setCategory')
        print(x.status_code)
        print(x.text)
    return x.text

def unasDirectXml(action, xmlTag:str, trailer = None):
    token = UnasAuth.doAuth()
    xmlParam =  MU.XMLTAG + xmlTag if trailer is None else f"<{trailer}>{xmlTag}</{trailer}>"
    x = requests.post(MU.UNASAPI_URL + '/' + action , data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/' + action)
        print(x.status_code)
        print(x.text)
    return x.text
#
# Prods
#
UNAS_DELETEPRODUCT_XML = "<Product><Action>delete</Action><Id>%s</Id></Product>"
def deleteProds(catIds):
    token = UnasAuth.doAuth()
    xmlParam = ''
    if catIds is None:
        return '<Products />'
    
    for cid in catIds:
        xmlParam += UNAS_DELETEPRODUCT_XML % str(cid)
    if len(xmlParam) > 0:
        xmlParam =  MU.XMLTAG + f"<Products>{xmlParam}</Products>"
        x = requests.post(MU.UNASAPI_URL + '/setProduct', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + str(token) })
        if MU.isLogLevelTrace():
            print(MU.UNASAPI_URL + '/setCategory')
            print(x.status_code)
            print(xmlParam)
            print(x.text)
        return x.text
    return '<Categories />'

def getProds(tag = None, val = None):
    token = UnasAuth.doAuth()
    xmlTag = '' if tag is None else '<{0}>{1}</{0}>'.format(tag, str(val).replace('Q','/'))
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params>%s<ContentType>minimal</ContentType></Params>' % xmlTag
    x = requests.post(MU.UNASAPI_URL + '/getProduct', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/getProduct')
        print(x.status_code)
        print(x.text)
    return x.text

def addProdsXml(xmlTag:str):
    token = UnasAuth.doAuth()
    xmlParam =  MU.XMLTAG + f"<Categories />{xmlTag}</Categories>"
    x = requests.post(MU.UNASAPI_URL + '/getCategory', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelTrace():
        print(MU.UNASAPI_URL + '/setProduct')
        print(x.status_code)
        print(x.text)
    return x.text

