import logging
import requests
import datetime as date
import UnasAuth
import html
import MyUtils as MU
import UnasProductCache as UPC
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from lxml import objectify

PRICECATEGORY = 17

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


def unasGetOrderToday(token, status):
    fromDay="2023/07.30"
    today = date.datetime.today()
    todayStr = today.strftime("%Y.%m.%d")
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><InvoiceStatus>'+ status +'</InvoiceStatus><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    x = requests.post(MU.UNASAPI_URL + '/getOrder', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    print(x.status_code)
    print(x.text)
    return x.text

def unasGetProducts(token, status):
    fromDay="2023/07.30"
    today = date.datetime.today()
    todayStr = today.strftime("%Y.%m.%d")
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><InvoiceStatus>'+ status +'</InvoiceStatus><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    x = requests.post(MU.UNASAPI_URL + '/getProduct', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    print(x.status_code)
    print(x.text)
    return x.text

def unasGetCustomers(token, status):
    fromDay="2023/07.30"
    today = date.datetime.today()
    todayStr = today.strftime("%Y.%m.%d")
    # xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><InvoiceStatus>'+ status +'</InvoiceStatus><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><DateStart>'+fromDay+'</DateStart><DateEnd>'+todayStr+'</DateEnd></Params>'
    x = requests.post(MU.UNASAPI_URL + '/getCustomer', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    print(x.status_code)
    print(x.text)
    return x.text

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

def doSymbolRequest(action, postData):
        logging.debug(action )
        logging.debug(postData)
        ## xmlReq = preProcessUnasPostRequest(action, postData, ts)
        ## xmlReq = transformPostRequest(xmlReq, "Product", ts)
        ## xmlResp = unasProduct(xmlReq, token)
        ## postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"

def transformPostRequestPrepare(dom, xsltFilename):
    if xsltFilename == 'Product':
        for prod in dom.getchildren():
            prodObj = objectify(prod)
            print(prod)
            #appt['Id'].text
            #
            #root = dom.tag
            prod['Action'] = 'modifyMostmarAfenebeIs'
        return dom
    else:
        return dom
    
def transformPostRequestObject(root, xsltFilename):
    if xsltFilename == 'Product':
        for prod in root.getchildren():
            if unasProductList.get(prod.code) == None: # UNAS-bol hianyzik
                if (prod.deleted == 0):
                    prod.unasProductAction = 'add'
                    prod.unasActionWebCategory = unasProductWebCategory
                else:
                    return None # Nem viszem fel, ha mar ugyis deleted a symbolban
            else:  # UNAS-ban azonositottam SKU alapjan es LIVE
                upc = unasProductList.get(str(prod.code))
                prod.unasProductId = upc.unasId
                if prod.deleted == 1:
                    prod.unasProductAction = 'delete'
                    prod.unasActionWebCategory = unasProductWebCategory
                else:
                    prod.unasProductAction = 'modify'
            # Mostantol 20231003 - csak a LIVE UNAS productokkal foglalkozom - ezert nem kell az alabbi kod:
            # elif unasProductStates.get(str(prod.code)) == 'live':  # UNAS-ban azonositottam SKU alapjan es LIVE
            #     prod.unasProductId = unasProductList.get(str(prod.code))
            #     if prod.deleted == 1:
            #         prod.unasProductAction = 'delete'
            #         prod.unasActionWebCategory = unasProductWebCategory
            #     else:
            #         prod.unasProductAction = 'modify'
            # elif unasProductList.get(str(prod.id)) == 'deleted':  # UNAS-ban deleted - KELL MEG EZZEL vmit csinalni?
            #     prod.unasProductAction = 'modify'
            #     prod.unasActionWebCategory = unasProductWebCategory
    elif xsltFilename == 'ProductPrice':
        for prod in root.getchildren():
            upc = None if not hasattr(prod,'productcode') else unasProductList.get(str(prod.productcode))
            if upc == None: # UNAS-bol hianyzik
                logging.error("Modositasi kiserlet UNASban nem letezo termekre CODE/Sku: " + str(prod.productcode))
                print("ERROR: Modositasi kiserlet UNASban nem letezo termekre CODE/Sku: " + str(prod.productcode))
                # raise ValueError("Modositasi kiserlet UNASban nem letezo termekre CODE/Sku: " + prod.productcode)
            else:  # UNAS-ban azonositottam SKU alapjan es LIVE
                prod.unasProductId = upc.unasId
                prod.symbolIdIsNull = 1 if upc.symbolId == 0 else 0
                prod.retValProduct = 0
                isPriceFound = False
                foundCat = -99999
                for pi in prod.price:
                    prod.retValProduct = 1
                    if pi.pricecategory == MU.PRODUCT_PRICECAT_BASE:
                        isPriceFound = True
                        pi.retValValid = 2
                        pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                    elif isPriceFound == False and pi.pricecategory == MU.PRODUCT_PRICECAT_FALLBACK:
                        foundCat = pi.pricecategory
                        pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                    elif isPriceFound == False and pi.pricecategory == MU.PRODUCT_PRICECAT_FALLBACK2:
                        foundCat = pi.pricecategory
                        pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                    elif isPriceFound == False and pi.priceCurrency == 'HUF':
                        foundCat = pi.pricecategory
                        pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                    else:
                        pi.retValValid = 0
                    #
                    if foundCat > 0:
                        for pi in prod.price:
                            if foundCat == pi.pricecategory:
                                pi.retValValid = 4

    elif xsltFilename == 'ProductQuantity':
        for prod in root.getchildren():
            upc = unasProductList.get(prod.ProductCode)
            upc = None if not hasattr(prod,'ProductCode') else unasProductList.get(str(prod.ProductCode))
            if upc == None: # UNAS-bol hianyzik
                raise ValueError("Modositasi kiserlet UNASban nem letezo termekre CODE/Sku: " + prod.ProductCode)
            else:  # UNAS-ban azonositottam SKU alapjan es LIVE
                prod.unasProductId = upc.unasId
                prod.symbolIdIsNull = 1 if upc.symbolId == 0 else 0
                upc.qty += prod.Quantity
                prod.CurrentQuantity = str(int(upc.qty))
                prod.retValValid = 2
    else:
        pass
    #
    objectify.deannotate(root)
    ET.cleanup_namespaces(root)
    obj_xml = ET.tostring(root, pretty_print=True)
    return obj_xml


def prepareXslt(xsltFilename, xml, xcv):
    if xsltFilename == 'Product':
        pass
    #
    return xcv

def transformPostRequest(xmlReq, xsltFilename, ts):
    xmlEnc='utf-8'
    if xmlReq[30:36] == 'utf-16':
        xmlEnc='utf-16'
    #
    xml = bytes(bytearray(xmlReq, encoding=xmlEnc))
    try:
        xmlObj = objectify.fromstring(xml)
        preparedXml = transformPostRequestObject(xmlObj, xsltFilename)
    except ET.XMLSyntaxError as e:
        logging.debug(e.msg)
        logging.debug(xml)
        logging.debug(xml.decode())
        raise  ValueError('XML Err:' + e.msg)

    if (preparedXml == None):
        return None
    # ##sztem jobb Objectkent kezelni##  preparedXml2 = transformPostRequestPrepare(ET.fromstring(xml), xsltFilename)
    # read xslt file
    xcv_0 = open('xslt/unas/set'+ xsltFilename + '.xslt').read()
    xcv = prepareXslt(xsltFilename, xmlReq, xcv_0)
    transform = ET.XSLT(ET.XML(xcv))
    # transform xml with xslt
    dom = ET.fromstring(preparedXml)
    newdom = transform( dom )
    outBytes=ET.tostring(newdom, pretty_print=True)
    if outBytes is not None:
        outStr = outBytes.decode()
        print(outStr)
        outfile = open("xmlfiles/set"+ xsltFilename + ".unas." + ts + ".xml", 'a')
        outfile.write(outStr)
        return outStr
    return None

def preProcessUnasPostRequest(action, xml, ts ):
    if action == 'product':
        pass
    elif action == 'inventory':
        pass
    elif action == 'price':
        pass
    elif action == 'pic':
        pass
    elif action == 'cat':
        pass
    elif action == 'customer':
        pass
    elif action == 'pricerule':
        pass
    elif action == 'finalize':
        pass
    elif action == 'synclog':
        pass
    else:
        raise ValueError('Unknown action:' + action)
    #
    outfileReq = open("xmlfiles/post-"+ action +".req." + ts + ".xml", 'a')
    outfileReq.write(xml)
    #
    return xml

# product
# inventory
# price
# doc
# pic
# cat
# customer
# pricerule
# finalize
#
def doUnasRequest(action, postData, pathParam3):
    logging.debug("path:%s, xml:%s", action, postData)
    token = UnasAuth.doAuth() # '7526191af38b98c0ce0334b0325a6be92adb7df3'
    logging.debug("token:%s",  token)
    ts = str(MU.getCurrTime())
    if (action == 'product'):
        logging.debug("Product")
        if len(unasProductList) == 0:
            prods = unasGetActiveProducts(token)
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        xmlReq = transformPostRequest(xmlReq, "Product", ts )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            xmlResp = unasProduct(xmlReq, token)
            postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
    elif action == 'inventory':
        logging.debug("Inventory")
        if len(unasProductList) == 0:
            prods = unasGetActiveProducts(token)
        xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
        xmlReq = transformPostRequest(xmlReq_0, "ProductQuantity", ts )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            xmlResp = unasProduct( xmlReq, token ) # Ez valojaban Product modositas az UNASban
            postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
    elif action == 'price':
        logging.debug("Price")
        if len(unasProductList) == 0:
            prods = unasGetActiveProducts(token)
        PRICECATEGORY = int(pathParam3) if pathParam3 is not None else -1
        xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
        xmlReq = transformPostRequest(xmlReq_0, "ProductPrice", ts )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            xmlResp = unasProduct( xmlReq, token ) # Ez valojaban Product modositas az UNASban
            postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
    elif action == 'doc':
        logging.debug("Documents")
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        # transformResponse(xmlResp, 'Document')
        xmlResp = unasDocuments( xmlReq, token )
        postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
    elif action == 'pic':
        logging.debug("Pictures")
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        xmlResp = unasPics( xmlReq, token )
        # transformResponse(xmlResp, 'Picture')
        postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
    elif action == 'cat':
        logging.debug("Category")
        if len(unasProductList) == 0:
            prods = unasGetActiveProducts(token)
        xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
        # Egyelore nincs megvalositva
        # xmlReq = transformPostRequest(xmlReq_0, "Category", ts )
        # xmlResp = unasCats( xmlReq, token )
        # postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
    elif action == 'customer':
        logging.debug("Customer")
        postData = postData.replace('&amp;#', '&#')
        xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
        xmlReq = transformPostRequest(xmlReq_0, "Customer", ts)
        if xmlReq != None:
            xmlResp = unasCustomer(xmlReq, token)
            postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
    elif action == 'pricerule':
        logging.debug("Pricerule")
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        xml = transformPostRequest(xmlReq, "Pricerule", ts )
        if xml is not None:
            xmlResp = unasPricerule(xml, token)
            postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
    elif action == 'finalize':
        logging.debug("Finalize")
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        xmlResp = unasFinalized(xmlReq, token)
        # transformResponse(xmlResp, 'Finalize')
        postProcessUnasPostRequest(action, xmlResp, ts)
        return "OK"
    elif action.startswith('synclog'):
        logging.error("synclog NOT IMPLEMENTED")
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        #logging.debug(xmlReq)
        print(xmlReq)
        return "OK"

    return  "Something wrong action:" + action

def postProcessUnasPostRequest(action, xmlResp, ts):
    # valszeg adatbazisba kellene irni a visszajovo adatokat, vagy , hogyan a fenebe rendeljem ossze maskeppen az ID-ket?
    logging.info("UNAS-Set-Action: {0}".format(action))
    logging.info("UNAS-Set-TS: {0}".format(ts))
    logging.info("UNAS-Set-response: {0}".format(xmlResp))
    if (action == 'product'):
        root=ET.fromstring(bytes(xmlResp, 'utf-8'))
        logging.debug(root.tag)
        return True
    elif action == 'inventory':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'))
        logging.debug(root.tag)
        return True
    elif action == 'price':
        if xmlResp == None:
            logging.debug("Null PRICE response?")
        else:
            root=ET.fromstring(bytes(xmlResp, 'utf-8'))
            logging.debug(root.tag)
        return True
    elif action == 'doc':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'))
        logging.debug(root.tag)
        return True
    elif action == 'pic':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'))
        logging.debug(root.tag)
        return True
    elif action == 'cat':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'))
        logging.debug(root.tag)
        return True
    elif action == 'customer':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'))
        logging.debug(root.tag)
        return True
    elif action == 'pricerule':
        if xmlResp == None:
            logging.debug("Null pricerule response?")
        else:
            root=ET.fromstring(bytes(xmlResp, 'utf-8'))
            logging.debug(root.tag)
        return True
    elif action == 'finalize':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'))
        logging.debug(root.tag)
        return True
    elif action == 'synclog':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'))
        logging.debug(root.tag)
        return True
    
    else:
        return False
    
    return True

def unasProduct(xml, token):
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Products>{0}</Products>'.format(xml)
    x = requests.post(MU.UNASAPI_URL + '/setProduct', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    print(x.status_code)
    print(x.text)
    return x.text

def unasInventory(xml, token):
    return

def unasPrice(xml, token):
    return

def unasDocuments(xml, token):
    return

def unasPics(xml, token):
    return

def unasCats(xml, token):
    return

def unasCustomer(xml, token):
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Customers>' + xml +'</Customers>'
    x = requests.post(MU.UNASAPI_URL + '/setCustomer', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    print(x.status_code)
    print(x.text)
    return x.text

def unasPricerule(xml, token):
    return

unasProductList = dict({})
#unasProductStates = dict({})
unasProductWebCategory = 677549 # ACHMED / q1+w2+e3+

def unasGetActiveProducts(token):
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><Name>WebÁruház</Name><ContentType>minimal</ContentType></Params>'
    x = requests.post(MU.UNASAPI_URL + '/getCategory', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    print(x.text)

    catObj = objectify.fromstring(bytes(x.text, 'utf-8'))
    global unasProductWebCategory
    unasProductWebCategory = catObj.Category.Id.text or 677549

    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Params><ContentType>full</ContentType></Params>'
    x = requests.post(MU.UNASAPI_URL + '/getProduct', data=xmlParam, headers={ "Authorization" : "Bearer " + token })
    print(x.status_code)
    print(x.text)

    xml = bytes(bytearray(x.text, encoding="utf-8"))
    prodObj = objectify.fromstring(xml)
    for px in prodObj.Product:
        productId = None
        productSku = None
        productVat = 27
        productState = None
        qty = 0
        sid = 0
        if hasattr(px, 'Params'):
            for pxp in px.Params.Param:
                if (pxp.Name == 'symbolId'):
                    sid = pxp.Value.text
            pVat = px.Prices.Vat.text  if hasattr(px, 'Prices') and hasattr(px.Prices, 'Vat') else '27'
        if hasattr(px, 'Stocks'):
            if hasattr(px, 'Stocks.Stock'):
                for pxp in px.Stocks.Stock:
                    if (pxp.Name == 'Qty'):
                        qty = pxp.Qty.text
            pVat = px.Prices.Vat.text  if hasattr(px, 'Prices') and hasattr(px.Prices, 'Vat') else '27'
        logging.debug("Id:%s, Sku:%s, Vat:%s, SID:%s, Qty:%s, State:%s", px.Id.text, px.Sku.text, pVat , sid, qty, px.State.text)
    root=ET.fromstring(xml)
    for prod in root.getchildren():
        productId = prod.find('Id').text
        productSku = prod.find('Sku').text
        productVat = '27' if not(hasattr(prod, 'Prices') and hasattr(prod.Prices, 'Vat')) else prod.find('Prices/Vat').text
        productState = prod.find('State').text
        symbolId = '0'
        if hasattr(prod, 'Params'):
            for ppp in prod.find('Params'):
                if (ppp.find('Name').text == 'symbolId'):
                    symbolId = ppp.find('Value').text
        if hasattr(prod, 'Stocks'):
            for ppp in prod.find('Stocks'):
                if (ppp.find('Name').text == 'symbolId'):
                    symbolId = ppp.find('Value').text
        if productId is not None :
            if productVat.rstrip().endswith('%'):
                pVat = float(productVat.rstrip()[0:-1])
            else:
                pVat = float(productVat)
            unasProductList[productSku] = UPC.UnasProductCache(int(productId), productSku, int(symbolId), float(qty), pVat, productState) #    def __init__(self, wid, sku, sid = 0, qty = 0, vat = 27, state = 'live'):
            #unasProductStates[productSku] = productState
        #        for elem in appt.getchildren():
        #            if not elem.text:
        #                text = "None"
        #            else:
        #                text = elem.text
        #                if elem.tag == 'Id':
        #                    productId = elem.text
        #                elif elem.tag == 'Sku':
        #                    productSku = elem.text
        #                elif elem.tag == 'Vat':
        #                    productVat = elem.text
        #                elif elem.tag == 'Value':
        #                    symbolId = elem.text
        #                elif elem.tag == 'State':
        #                    productState = elem.text
        #            #
        #            print(elem.tag + " => " + text)
        # print('---------------------------')
    
    return unasProductList

def unasFinalize(postData):
    unasProductList = []
    return "OK"

def unasFinalized(xml, token):
    return

def symbolSynclog(postData):
        logging.debug(postData)
        ## root=ET.fromstring(bytes(postData, 'utf-8'))
        ## logging.debug(root)
        return 'OK'
    

