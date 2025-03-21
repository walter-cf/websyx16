import logging
import pprint as pp
import datetime as date
import urllib.parse as urlParse
import MyUtils as MU
from  MyUtilsTypes import UnasTransactionType as UTSTYPE
import FdbUtils as FBU
import UnasCustomerCache as UCC
import UnasOrderCache as UOC
from CustomerAddressHelper import CustomerAddress as CA, CustomerAddressHelper as CAH
import UnasOrderCache as UOC
import UnasConnectHelper as UCH
import MySmtpClient as SM
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from lxml import objectify
from typing import List
import json
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

GBL_ErrorMessages = []

def transformGetRequestObject(root, action, xmlPart):
    if action == 'Product':
        for prod in root.getchildren():
            sku = prod.Sku
            upc = MU.UnasProductList.get(sku)
            if upc:
                prod.symbolId = upc.symbolId
                logging.info('p-Product:%s TsDiff:%i', upc.sku, MU.getCurrTime() - upc.lastmod)
            else:
                logging.info("p-Prod %s not found in cache", sku)
                prod.symbolId = FBU.getProductSymbolId(sku.text)
            logging.info("trfGet-Product:%s (%i), %s", sku,prod.symbolId, 'Nincs.Neve' if prod.find('Name') is None else prod.Name)
            if (MU.PRODUCTNAME_OVERWRITE):
                if prod.find('Name') and prod.Name.text:
                    prod.NameEncoded =  urlParse.quote(prod.Name.text)
    elif action == 'Order' or action == 'OrderBy' :
        for ord in root.getchildren():
            if MU.isLogLevelTrace():
                print(ord)
            email = ord.Customer.Email
            custTaxNo = ord.Customer.Addresses.Invoice.TaxNumber
            ucc = MU.getCustomerFormCache(email, custTaxNo, ord.Customer.find('Id'))
            unasCustXmlItem = ord.Customer
            #
            ord.symbolVouchersequenceCode = MU.SYMBOLVOUCHERSEQUENCECODE
            ord.prefixOrderId = MU.SYMBOLORDERIDPREFIX
            #
            if unasCustXmlItem.find('Id') == None: # ucc == None:
                unasCustXmlItem.CustSymbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["unregistered"], ord.Id) # rendeles ID, mert CustId nincs
                ucc = UCC.UnasCustomerCache(None, email, custTaxNo, unasCustXmlItem.CustSymbolCode, None, 'nonRegged' ) # type: ignore
                try:
                    MU.putCustomerIntoCache(ucc, ucc.custAzon)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                except Exception as e:
                    GBL_ErrorMessages.append(str(e))
                # end try
            else: #  TODO !!!!!  Ezzel vigyaznom kellene !!!!! UCO vs UCU nincs rendesen atgondolva!
                unasCustXmlItem.CustSymbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["default"], ord.Customer.Id) if ucc.code is None else ucc.code
            if ucc:
                ucc.unasAddrXml = [] if ord.Customer.Addresses is None else [ ord.Customer.Addresses.Invoice, ord.Customer.Addresses.Shipping ] 
            #
            # get symbolId
            xmlCustSymbolId = 0
            if ord.find('Params'):
                for prm in ord.Params.getchildren():
                    if 'symbolId' == prm.Name:
                        if prm.Value and 'OrderBy' != xmlPart: 
                                ord.SkipThisOrderItem = 1
            if unasCustXmlItem.find('Params'):
                for prm in unasCustXmlItem.Params.getchildren():
                    if 'symbolId' == prm.Name:
                        if prm.Value:
                            xmlCustSymbolId = int(prm.Value)
            atp = transformOrderOptions(ord.Shipping.Name, ord.Payment.Name) # Transform UNAS-name to Symbol-Name
            ord.Shipping.Name = atp[0]
            if atp[1].startswith('specialFunction'):
                paymentName, paymentDays = getPaymentSpecial( atp[1][len('specialFunction'):], xmlCustSymbolId, unasCustXmlItem.Id )
                ord.paymentMethodName      = paymentName
                ord.paymentMethodTolerance = paymentDays
            else:
                ord.paymentMethodName      = atp[1]
            #
            if MU.isLogLevelTrace():
                print(unasCustXmlItem.CustSymbolCode)
            logging.info("trfGet-Ord:%s (%s)", ord.Id, email )
    elif action == 'OrderCustomers':
        for ord in root.getchildren():
            if MU.isLogLevelTrace():
                print(ord)
            unasCustXmlItem = ord.Customer
            custTaxNo = unasCustXmlItem.Addresses.Invoice.TaxNumber
            ucc = MU.getCustomerFormCache(unasCustXmlItem.Email, custTaxNo, unasCustXmlItem.Id)
            if ucc == None:
                ord.CustSymbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % ( MU.CUSTOMER_CODE_PREFIXES["unregistered"],  ord.Id)
                ucc = UCC.UnasCustomerCache(emil=unasCustXmlItem.Email, taxNo=custTaxNo, code=ord.CustSymbolCode, state='nonRegged')
                try:
                    MU.putCustomerIntoCache(ucc, ucc.custAzon)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                except Exception as e:
                    GBL_ErrorMessages.append(str(e))
            elif ucc.symbolId > 0:
                pass # unasCustXmlItem.SkipThisCustomerItem =  1
            else:
                ord.CustSymbolCode = MU.mkCustomerCode( ucc )  if ucc.code is None else ucc.code
            ucc.unasAddrXml = [] if unasCustXmlItem.find('Addresses') is None else unasCustXmlItem.find('Addresses').getchildren()
            if len(ucc.unasAddrXml) > 0 and  CAH(0,0).compareCA(CA(0).initAddr(ucc.unasAddrXml[0]), CA(0).initAddr(ucc.unasAddrXml[1])):
                unasCustXmlItem.SkipAddressShipping = 1
            logging.info("trfGet-OrdCust:%s (%s)", ord.Id, unasCustXmlItem.Email )
            if ucc.symbolId == 0:
                xmlPart.append(unasCustXmlItem)
        return None
    elif action == 'Customers':
        # Recheck CustomersCache
        # sCode = None #  if MU.CREATE_CUSTOMER_MISSING: a kepzett Code ertek!
        for unasCustXmlItem in root.getchildren():
            if unasCustXmlItem.find('Authorize') and unasCustXmlItem.find('Authorize').find('Admin') and unasCustXmlItem.Authorize.Admin != 'yes':
                unasCustXmlItem.SkipThisCustomerItem =  1
            else:
                custTaxNo = unasCustXmlItem.Addresses.Invoice.TaxNumber
                unasCustSymbolId = 0 
                if unasCustXmlItem.find('Params') is not None:
                    for prm in unasCustXmlItem.Params.getchildren():
                        if 'symbolId' == prm.Name:
                            unasCustSymbolId = int(prm.Value.text)
                            if MU.CREATE_CUSTOMER_MISSING:
                                unasCustXmlItem.customerAddressCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % ( MU.CUSTOMER_CODE_PREFIXES["default"],  unasCustXmlItem.Id)
                                unasCustSymbolId = FBU.createCustomerIfNotExists(unasCustSymbolId, 
                                        xmlCode=unasCustXmlItem.customerAddressCode, xmlEmail=unasCustXmlItem.Email, xmlTaxno=custTaxNo)
                # Get UCC cache Item
                #ucc = MU.UnasCustomerList.get(  UCC.buildAzonData( unasCustXmlItem.Email, custTaxNo ))
                #if ucc is None: # try with unasId if TaxNo duplicated HACK
                #    ucc = MU.UnasCustomerList.get('#'+str(unasCustXmlItem.Id ))
                ucc = MU.getCustomerFormCache(unasCustXmlItem.Email, custTaxNo, unasCustXmlItem.Id)
                #
                if ucc == None:
                    custCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["default"], unasCustXmlItem.Id)
                    ucc = UCC.UnasCustomerCache(unasCustXmlItem.Id, unasCustXmlItem.Email, custTaxNo, custCode, 0, 'new')
                    ucc.symbolId = unasCustSymbolId
                    try:
                        MU.putCustomerIntoCache(ucc, ucc.custAzon)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                    except Exception as e:
                        GBL_ErrorMessages.append(str(e))
                    # end try
                    logging.info('g-Customer:%s TsDiff:NEW', ucc.custAzon )
                    ucc.unasAddrXml = [] if unasCustXmlItem.find('Addresses') is None else unasCustXmlItem.find('Addresses').getchildren() # type: ignore
                elif unasCustXmlItem.Email != ucc.email:
                    logging.warning('u-Customer[%i] in Unas-only!:%s', unasCustXmlItem.Id, ucc.custAzon )
                    GBL_ErrorMessages.append(f"Warning! Possible Duplicate TaxNo:{ucc.custAzon}, emils:{unasCustXmlItem.Email} / {ucc.email} ")
                    custCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["default"], unasCustXmlItem.Id)
                    ucc = UCC.UnasCustomerCache(unasCustXmlItem.Id, unasCustXmlItem.Email, custTaxNo, custCode, 0, 'new')
                    ucc.symbolId = unasCustSymbolId
                    ucc.custAzon = UCC.buildCustAzonById(unasCustXmlItem.Id) # type: ignore
                    try:
                        MU.putCustomerIntoCache(ucc, ucc.custAzon)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                    except Exception as e:
                        GBL_ErrorMessages.append(str(e))
                    # end try
                    logging.info('g-Customer:%s,%s TsDiff:NEW', ucc.custAzon, ucc.email )
                    ucc.unasAddrXml = [] if unasCustXmlItem.find('Addresses') is None else unasCustXmlItem.find('Addresses').getchildren() # type: ignore
                if ucc.symbolId == 0:
                    # ucc = UCC.UnasCustomerCache(cust.Id, cust.Email, custTaxNo, None, 0, 'new')
                    #@1 result = FBU.addCust(ucc.unasId, 'UCO-%i' % ucc.unasId)
                    #@1 ucc.symbolId = 0 if result < 0 else result
                    #@1 cust.forcedCustomerId = ucc.symbolId ### MAR NINCS az xml-ben
                    try:
                        MU.putCustomerIntoCache(ucc, ucc.custAzon)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                    except Exception as e:
                        GBL_ErrorMessages.append(str(e))
                    # end try
                    ucc.unasAddrXml = [] if unasCustXmlItem.find('Addresses') is None else unasCustXmlItem.find('Addresses').getchildren() # type: ignore
                    GBL_ErrorMessages.append( f"Warning[W002]:- Customer in Unas-only! Id:{unasCustXmlItem.Id} Azon:{ucc.custAzon}")
                    logging.error('u-Customer[%i] in Unas-only!:%s', unasCustXmlItem.Id, ucc.custAzon )
                else:
                    uldStr = None if unasCustXmlItem.Dates.Modification is None else unasCustXmlItem.Dates.Modification.text
                    unasLastMod = 0 if uldStr is None else MU.dateStrToTs(uldStr)
                    logging.info('g-Customer:%s lastMod-symb/unas/diff:%s/%s/%i TsDiff:%i', ucc.custAzon,
                                MU.tsToDateStr(ucc.lastmod), uldStr, unasLastMod - ucc.lastmod, MU.getCurrTime() - ucc.lastmod)
                    ucc.unasAddrXml = [] if unasCustXmlItem.find('Addresses') is None else unasCustXmlItem.find('Addresses').getchildren() # type: ignore
                    symbolModTime = FBU.getModTime( ucc.symbolId, "Customer" )
                    if symbolModTime is None:
                        logging.warning('Gyanus, HIANYZO SymbolID! Azon:%s Id:%d', ucc.custAzon,ucc.symbolId )
                        GBL_ErrorMessages.append( f"Warning[W001]:- Gyanus, HIANYZO SymbolID! Azon:{ucc.custAzon} Id:{ucc.symbolId}")
                        ## Quick HACK - mert NINCS Symbolban es ha van symbolId-je, akkor ki kell nullazni
                        if unasCustXmlItem.find('Params') is not None:
                            for prm in unasCustXmlItem.Params.getchildren():
                                if 'symbolId' == prm.Name:
                                    prm.Value = ''
                        ucc.symbolId = 0
                    else: 
                        logging.warning('Cust(g):%s %s lastMod:%s(%i), unasMod:%s(%i), symbolMod:%s(%i)' % (
                                ucc.custAzon, 'Gyanus SKIP!' if unasLastMod - symbolModTime.timestamp()  < 100000   else '',
                                MU.tsToDateStr(ucc.lastmod), ucc.lastmod, MU.tsToDateStr(unasLastMod), unasLastMod,
                                str(symbolModTime), symbolModTime.timestamp()))
                logging.info("trf-trfGet:%s", unasCustXmlItem.Email )
                unasCustXmlItem.unasCustomerCategory = MU.UnasCustomerCategoryName
                if MU.HANDLE_CUSTOMERADDRESS:
                    unasCustXmlItem.handleCustomerAddresses = 1
                #
                # Joe test texts
                unasCustXmlItem.joeComment = 'noAuth' if unasCustXmlItem.Authorize is None else unasCustXmlItem.Authorize
                # Preferred address ...
                try:
                    if MU.HANDLE_CUSTOMERADDRESS:
                        processCAddresses(ucc,unasCustSymbolId, unasCustXmlItem)
                except Exception as e:
                    GBL_ErrorMessages.append(str(e))
                    logging.error('processCAddresses X:{}', str(e))
                # end try
            # Unregistered Customer, direct order wo regg
            # END IF Authorize.Admin == yes
        # END FOR CustomerItem cycle
        if xmlPart is not None:
            for unregCust in  xmlPart.getchildren():
                root.append(unregCust)
        #
    else:
        pass
    #
    root.unasFeedbackURL = MU.UNAS_FEEDBACK_URL
    #
    objectify.deannotate(root)
    ET.cleanup_namespaces(root) # type: ignore
    obj_xml = ET.tostring(root, encoding='utf-8', pretty_print=True) # type: ignore
    if MU.isLogLevelTrace():
        print(obj_xml)
    return obj_xml

def transformOrderOptions(shipping, payment):
    transportMode = shipping
    for f in MU.PRICERULE_TRANSPORTMODES:
        if f[1] == shipping:
            transportMode = str(f[0])
    paymentMethod = payment
    for f in MU.PRICERULE_PAYMENTMETHODS:
        if f[1] == payment:
            paymentMethod = str(f[0])
    return [transportMode, paymentMethod]

def getPaymentSpecial(specCode:str, custId:int, unasId:int):
    if "01" == specCode:
        retv = FBU.getPaymentMethodByCustomerId(custId) if custId > 0 else FBU.getPaymentMethodByCustomerCode('UC_-%d' % unasId) 
        return retv[0], retv[1]
    return None, None

def postProcessCAddresses(customerId:int, uccAddrs: List[CA]):
    for uu in uccAddrs:
        if CA.CAstate_dummy == uu.state:
            FBU.reassignCA(uu.Id, customerId)

def processCAddresses0(ucc: UCC.UnasCustomerCache, cah:CAH, unasCustXml):
    otherAddressIndex = 0
    for addr in unasCustXml.Addresses.getchildren():
        if addr.tag == "Invoice":
            pass # Ezt nem adom hozza a cache Cimlistajahoz! Elvileg ezt kezeli az XSLT
        else:
            otherAddressIndex += 1
            sAddr = CA(unasid=unasCustXml.Id, idx=otherAddressIndex)
            sAddr.initAddr(addr, state=CA.CAstate_unasOnly)
            addr.otherAddressIndex = otherAddressIndex
            streetName  = addr.Street # houseNumber eliminated!
            #streetName  = addr.Street if addr.find('StreetName') is None else (
            #                addr.StreetName.text + ( '' if addr.find('StreetType') is None else addr.StreetType.text )  
            #                )
            # houseNumber = None if addr.find('StreetNumber') is None else addr.StreetNumber.text
            houseNumber = None # TODO Hack !! 
            if addr.tag == "Shipping":
                addr.unasFirstAddresItem = 1
                sAddr.state = CA.CAtype_shipping
                sAddr.presetCode(unasCustXml.Id, otherAddressIndex)
            else:
                sAddr.Id = FBU.addCustAddrDummy(-2, ucc.unasId, otherAddressIndex,
                        name=addr.Name, city=addr.City, zip=addr.ZIP, region=addr.County, country=addr.Country,
                        street=streetName, house=houseNumber) # type: ignore
                sAddr.state = CA.CAstate_dummy
                addr.skipOtherAddress = 1
            #
            addr.customerAddressCode = sAddr.Code
            cah.unasAddresses.append(sAddr)

def processCAddresses1(ucc: UCC.UnasCustomerCache, cah:CAH, unasCustXml):
    otherAddressIndex = cah.getSymbolCAmaxIndx()
    for addr in unasCustXml.Addresses.getchildren():
        #
        sAddr = CA(unasid=unasCustXml.Id)
        sAddr.initAddr(addr, state=CA.CAstate_unasOnly)
        # houseNumber = None if addr.find('StreetNumber') is None else addr.StreetNumber
        # TODO Ez HACK es nem tudom, mi a hatasa, megprobalom a houseNumbert None-nak tartani
        houseNumber = None # Nem hasznaljuk a hazszamot
        if houseNumber is None:
            streetName  = addr.Street
        elif len(houseNumber.text) > 19:
            houseNumber = None
            streetName = addr.Street
        elif addr.find('StreetName') is None:
            streetName  = addr.Street
            houseNumber = None
        else:
            streetName  = addr.Street
        #
        if addr.tag == "Invoice":
            addr.StreetNumber = houseNumber
            addr.StreetName   = streetName
        else:
            addr.StreetNumber = houseNumber
            addr.StreetName   = streetName
            _pairedCA = cah.identfyCA(sAddr)
            if _pairedCA is None:
                sAddr.state = CA.CAstate_dummy
                otherAddressIndex += 1
                sAddr.presetCode( unasCustXml.Id, otherAddressIndex )
                sAddr.Id = FBU.addCustAddrDummy(cah.customerid, ucc.unasId, otherAddressIndex,
                        name=addr.Name, city=addr.City, zip=addr.ZIP, region=addr.County, country=addr.Country,
                        street=streetName, house=houseNumber) # type: ignore
                sAddr.state = CA.CAstate_dummy
                addr.customerAddressCode = sAddr.Code
            else:
                sAddr.Id = _pairedCA.Id
                sAddr.state = CA.CAstate_paired
                sAddr.Code = _pairedCA.Code
                if _pairedCA.Deleted > 0:
                    FBU.undeleteCAbyId(sAddr.Id)
                addr.customerAddressCode = sAddr.Code
            # Preferred Shipping Address
            if addr.tag == "Shipping":
                addr.unasFirstAddresItem = 1
            #
            cah.unasAddresses.append(sAddr)

def processCAddresses(ucc: UCC.UnasCustomerCache, unasCustSymbolId, unasCustXml):
    cahErrors = []
    cah = CAH( cahErrors, cid = unasCustSymbolId, uid = unasCustXml.Id, tag = unasCustXml.Addresses.getchildren() )
    if len(cahErrors) > 0:
        GBL_ErrorMessages.append(cahErrors)
    # caSymbolCnt = cah.getSymbolCAactiveCnt()    
    if ucc.symbolId > 0:
        processCAddresses1(ucc, cah,unasCustXml)
        cah.analyzeCAlist()
        cah.rebuildCAlist(ucc.symbolId if ucc.symbolId > 0 else -2 ) # felesleget kitorolni  ujakat felvinni NEM Dummy kent
        for uu in cah.symbAddresses:
            if CA.CAstate_symbolOnly == uu.state or CA.CAstate_duplicate == uu.state:
                FBU.deleteCAbyId(uu.Id)
        ucc.unasAddrObj = cah.unasAddresses
    else:
        processCAddresses0(ucc, cah, unasCustXml)
        ucc.unasAddrObj = cah.unasAddresses

def transformResponse(xmlResp, action, xmlPart):
    if xmlResp is None:
        return None
    xmlEnc='utf-8'
    if xmlResp[30:36] == 'utf-16':
        xmlEnc='utf-16'
    #
    xml = bytes(bytearray(xmlResp, encoding=xmlEnc))
    try:
        preparedXml = transformGetRequestObject(objectify.fromstring(xml,None), action, xmlPart)
        if (preparedXml == None):
            return None
    except ET.XMLSyntaxError as e:
        _msg = "transformGetRequestObject Err-X: " + str(e)
        logging.error(_msg)
        GBL_ErrorMessages.append(_msg)
        return None

    preparedXmlStr = preparedXml.decode()
    outfileReq = open("xmlfiles/get"+ action +".resp." + str( MU.getTS() ) + ".xml", 'a')
    outfileReq.write(preparedXmlStr)
    outfileReq.close()
    # xml = bytes(bytearray(preparedXml, encoding="utf-8"))
    dom=ET.fromstring (preparedXml, None)
    # read xsl file
    try:
        xcv = open('xslt/unas/get'+ action +'.xslt').read()
        transform = ET.XSLT(ET.XML(xcv, None))
    except Exception as e:
        GBL_ErrorMessages.append(f"Error while Transform-Action:{action}")
        GBL_ErrorMessages.append(e)
        return None
    # end try
    # transform xml with xslt
    newdom = transform(dom)
    # newdom.unasFeedbackURL = None

    outBytes=ET.tostring(newdom, encoding='utf-8', pretty_print=True) # type: ignore
    if outBytes is not None:
        if MU.isLogLevelTrace():
            print(outBytes.decode())
        outfile = open("xmlfiles/get"+ action + ".symb." + str(MU.getTS()) + ".xml", 'a')
        outBytesStr = outBytes.decode()
        outfile.write(outBytesStr)
        return outBytesStr.replace('<?xml version="1.0"?>',"")
    return None

def preProcessUnasGetResponse(xml, action):
    if action == 'orders':
        pass
    elif action == 'products':
        pass
    elif action == 'prodbyid':
        pass
    elif action == 'customers':
        pass
    elif action == 'inquirers':
        pass
    elif action == 'simpleTransform':
        pass
    else:
        raise ValueError('Unknown action:' + action)
    #
    return xml

def postProcessUnasGetResponse(xml, action):
    if action == 'orders':
        pass
    elif action == 'products':
        pass
    elif action == 'prodbyid':
        pass
    elif action == 'customers':
        pass
    elif action == 'inquirers':
        pass
    elif action == 'simpleTransform':
        pass
    else:
        raise ValueError('Unknown action:' + action)
    #
    return xml

def doUnasActionRequest(xmlResp, action, actionXslt, xmlPart = None):
    MU.checkCacheState()
    xmlPre = preProcessUnasGetResponse(xmlResp, action)
    xmlTrd = transformResponse(xmlPre, actionXslt, xmlPart)
    xmlRet = postProcessUnasGetResponse(xmlTrd, action)
    return xmlRet or 'OK'


def doUnasFeedback(pathArray, path):
    MU.checkCacheState()
    if (pathArray[2] == 'oke' ):
        try:
            logging.warning("FBUNAS-OKE: {0}".format( urlParse.unquote('/'.join(pathArray)[10:] )))
            unasId:int  = None # type: ignore
            symbolId:int = None # type: ignore
            symbolCode:str  = None # type: ignore
            ipAddr = None
            prodname = ''
            orderKey = None
            uriParts = path.split('?')
            dats = uriParts[-1].split('&')
            for itm in dats:
                key, val = itm.split('=')
                if key == 'id':
                    unasId = int(val)
                elif key == 'symbolid':
                    symbolId = int(val)
                elif key == 'code':
                    symbolCode = val
                elif key == 'orderkey':
                    orderKey = val
                elif key == 'ipaddr':
                    ipAddr = val
                elif key == 'prodname':
                    prodname = val
                elif key == 'sku':
                    productSku = val

            if pathArray[3].startswith('order'):
                #FBU.updateSymbolCode(symbolId, 'URE-%s-UI-%i' % (orderKey, unasId), 'CustomerOrder', 'PrimeVoucherNumber' )
                uoc = None if orderKey is None else  MU.UnasOrderList.get(orderKey)
                if uoc is None:
                    raise ValueError(f"FB-Order-Cacche corrupted! Missing : {orderKey}")
                if uoc.symbolId <= 0 or not uoc.acknowledged:
                    FBU.updateSymbolCode(symbolId, '%s-%s' % ( MU.SYMBOLORDERIDPREFIX, orderKey), 'CustomerOrder', 'PrimeVoucherNumber' )
                    uoc.symbolId = symbolId
                    xmlResp ='x'
                    FBU.updateOrderStatus(symbolId, MU.SYMBOLORDERSTATUS)
                    if MU.ORDER_autoAcknowledge:
                        # set Order status to Visszaigazolva
                        uoc.acknowledged = True
                        xmlResp = UCH.unasSetOrderStatus( orderKey, MU.ORDER_STATUS_ACCEPTED,
                                        symbolId, True, "Rendelését befogadtuk, az előkeszítést megkezdtük.")
                    else:
                        xmlResp = UCH.unasSetOrderStatus( orderKey, None, symbolId )
                        
                    return getErrorTextOrder('newOrder', xmlResp, symbolId, '3')
                elif (symbolId != uoc.symbolId):
                    raise ValueError(f"FB-Order-Cacche corrupted! order:{orderKey}: symbolId-s differ [Sym]{symbolId}/[Cache]{uoc.symbolId}")

            elif pathArray[3] .startswith('orderstatus'):
                pass
            elif pathArray[3] .startswith('cust'):
                if uriParts[0] == 'unregistered':
                    symbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["unregistered"],unasId)
                    FBU.updateSymbolCode(symbolId, symbolCode, 'Customer' )
                elif pathArray[3] == 'customer':

                    ucc = next((x for x in  MU.UnasCustomerList.values() if x.unasId == unasId), None )
                    if ucc is not None:
                        ucc.lastmod = MU.getCurrTime()
                        if ucc.state == 'new' or (0 if ucc.symbolId is None else ucc.symbolId) == 0:
                            symbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["default"],unasId)
                            try:
                                FBU.updateSymbolCodeIfChanged(symbolId, symbolCode, 'Customer' ) # csak a NEW statusnal kellene!!!!
                                ucc.state = 'symb'
                            except Exception as e:
                                mmm = f"DB-Error:{e}"
                                SM.sendAlertMail(mmm)
                                # FBU.updateSymbolCode(symbolId, symbolCode+"-a", 'Customer' ) # csak a NEW statusnal kellene!!!!
                            # end try
                            if ucc.code != symbolCode or ucc.symbolId != symbolId:
                                ucc.code = symbolCode
                                ucc.symbolId = symbolId
                                UCH.updateCustomerSymbolId(unasId, symbolId, symbolCode)
                                logging.warning("CustomerCode:%s(%i) modified at:%i,%s in cache",
                                        ucc.code, symbolId, ucc.lastmod, MU.tsToDateStr(ucc.lastmod) )
                            else:
                                logging.debug("CustomerCode:%s(%i) SKIPP mod at:%i,%s in cache",
                                        ucc.code, symbolId, ucc.lastmod, MU.tsToDateStr(ucc.lastmod) )

                        logging.info("Customer:%s(%i) lastMod:%i/%s ", ucc.code, symbolId, ucc.lastmod, MU.tsToDateStr(ucc.lastmod) )
                        logging.debug( "fbUnas-Cust:%s ", ucc.toStr())
                        # ?????    Cimek !!!!
                        if MU.HANDLE_CUSTOMERADDRESS:
                            postProcessCAddresses(symbolId, ucc.unasAddrObj)
                        #
                    else:
                        errorMailtoOperator(f'Path: {pathArray[3]}\nCustomer cache corrupted, missing unasId:{unasId}')
                        logging.error("Customer cache corrupted, missing unasId:%i", unasId)
                        # raise ValueError("Customer cache corrupted, missing unasId:%i", unasId)
                elif uriParts[0] == 'custshipaddr':
                    pass # logging.warning('Not written Yet')
                elif uriParts[0] == 'custinvaddr':
                    pass # logging.warning('Not written Yet')
                elif uriParts[0] == 'custcontact':
                    pass # logging.warning('Not written Yet')
                elif uriParts[0] == 'custothaddr':
                    pass # logging.warning('Not written Yet')
                else:
                    logging.error('Not handled Customer Feedback action: %s', uriParts[0])
            elif pathArray[3] == 'product':
                #upc = MU.UnasProductList.get(productSku)
                upc = next((x for x in  MU.UnasProductList.values()  if x.unasId == unasId), None )
                if upc is not None:
                    if upc.symbolId != symbolId:
                        retXml = UCH.updateProductSymbolId(upc.unasId, symbolId, upc.sku )
                        getErrorTextProduct("Product-Set.Unas.SymbolID", retXml)
                        retObj = objectify.fromstring(retXml.replace(MU.XMLTAG, ''), None).getchildren()
                        
                    upc.symbolId = symbolId
                    upc.unasId = unasId
                if MU.PRODUCTNAME_OVERWRITE and symbolId>0:
                    name = urlParse.unquote(prodname, encoding='utf-8')
                    logging.info('Felulvagom a ProdID:%i nevet:%s!!!', symbolId, name )
                    FBU.updateProductName(symbolId, name )
                    
        except Exception as e:
            # comment: 
            errmsg = "FBUNAS-OKE: %s".format( urlParse.unquote('/'.join(pathArray)[10:].replace('+', ' ') ))
            logging.error(errmsg)
            GBL_ErrorMessages.append( "Feedback err:" + errmsg )
            GBL_ErrorMessages.append( "Feedback err:" + str(e) )
        # end try
    else: # Error branch
        try:
            logging.error("FBUNAS-ERR: %s".format( urlParse.unquote('/'.join(pathArray)[10:].replace('+', ' ') )))
            unasId = 0
            symbolId = 0
            symbolCode = ''
            orderKey = ''
            errorMsg = ''
            # Cleaning ...
            uriParts = path.split('?')
            dats = uriParts[1].split('&')
            for itm in dats:
                key, val = itm.split('=')
                if key == 'id':
                    unasId = int(val)
                elif key == 'symbolid':
                    symbolId = int(val)
                elif key == 'code':
                    symbolCode = val
                elif key == 'orderkey':
                    orderKey = val
                elif key == 'errormsg':
                    errorMsg = urlParse.unquote(val).replace('+', ' ')
                #
                SM.sendAlertMail(f"Path:{pathArray[-1]}\r\nUnasId:{unasId}\r\nSymbolId:{symbolId}\r\nCode:{symbolCode}\r\nOrderKey:{orderKey}\r\nError-Msg:{errorMsg}" )
                # Clean DUMMY CustomerAddress rex
                FBU.deleteDummyCArex(unasId)

        except Exception as e:
            # comment: 
            errmsg = "FBUNAS-ERR: %s".format( urlParse.unquote('/'.join(pathArray)[10:].replace('+', ' ') ))
            logging.error(errmsg)
            GBL_ErrorMessages.append( "Feedback err:" + errmsg )
            GBL_ErrorMessages.append( "Feedback err:" + str(e) )
        # end try
    return "OK"

def errorMailtoOperator(ms:str):
    pass

def doEmagFeedback(queryPath) -> str:
    return 'OK'

def getMissingCustomersFromOrder(xml:str):
    cl = []
    orders = objectify.fromstring(xml.replace(MU.XMLTAG, ''), None)
    for ord in orders.findall('Order'):
        cust = ord.Customer
        taxTag = None if cust.Addresses is None else None if cust.Addresses.Invoice is None else cust.Addresses.Invoice.TaxNumber
        ucc = MU.getCustomerFormCache(cust.Email, taxTag, cust.find('Id'))
        if ucc is None:
            unasCust = UCH.unasGetCustomers('Id', None if not cust.find('Id') else cust.Id.text )
            if unasCust is None:
                _m = "getOrder failed!\r\nOrder Azon:%s, ID:%d\r\n\r\ngetMissingCustomersFromOrder unasCust:[%s, %s] NOT exist in UNAS" % (
                    ord.Key.text,  ord.Id.text, cust.Id, cust.Email)
                SM.sendAlertMail(_m, '[UNAS-Proxy]: megrendeles lekeres hiba! Id:%s, Azon:%s' % ( ord.Id.text, ord.Key.text))
                raise ValueError(_m)

            ucc = UCC.UnasCustomerCache(cust.find('Id') and int(cust.Id.text), cust.Email.text, None if taxTag is None else taxTag.text) # type: ignore
            unasCustObj = objectify.fromstring(unasCust.replace(MU.XMLTAG, ''), None).getchildren()
            if len(unasCustObj) == 1:
                ucc.fromXml(unasCustObj[0])

            MU.putCustomerIntoCache(ucc, UCC.buildCustAzonById(ucc.unasId)) # type: ignore

        if ucc.symbolId < 1:
            # Most kell DUMMY-REC ???
            cid = createUnregisteredCustomer(ucc)
            ucc.symbolId = cid
            retXml = UCH.updateCustomerSymbolId(ucc.unasId, ucc.symbolId, ucc.code)
            retStatus = objectify.fromstring(retXml.replace(MU.XMLTAG, ''), None).getchildren()
            if "ok" == '-' if len(retStatus) < 1 else retStatus[0].Status:
                cl.append(ucc)
            else:
                raise ValueError("getMissingCustomersFromOrder :%s, Nem vart customer-Update err:%s" % ( ord.Key, retXml))
    return cl

def createUnregisteredCustomer(cust:UCC.UnasCustomerCache):
    _code = cust.code if cust.code is not None and len(cust.code.strip()) > 0 else MU.mkCustomerCode(cust)
    customerId = FBU.createCustomerIfNotExists(0, xmlCode=_code, xmlEmail=cust.email, xmlTaxno=cust.taxNumber)
    cust.code = _code
    return customerId
    
def doUnasGetRequest(path, errors) -> str:
    # reset errors
    GBL_ErrorMessages.clear()
    #
    logging.debug(path)
    actionPath = path[2]
    tsStart = MU.getCurrTime()
    GBL_ErrorMessages.append("Test GET errMsg:%d" % tsStart)
    unasresp : str = None # type: ignore
    if (actionPath == 'orders'):
        uts = MU.createTransactionId( UTSTYPE.ORDERS )
        logging.debug("getOrderToday-TS:%d" % uts)
        xmlResp = UCH.unasGetOrderNew()
        
        # Ha nincs a symbolban, csinaljak egy dummy rekordot?
        if MU.ORDER_getMissingCust:
            MU.checkCacheState()
            # Create FB rekord from orderXml-CustomerPart
            custList = getMissingCustomersFromOrder(xmlResp)
            _sMsg = ''
            for c in custList:
                _m = "Hianyzo Customer :%s" % c.toStr()
                GBL_ErrorMessages.append("Megrendeles lekeres hiba: %s" % _m)
                _sMsg += '\r\n** ' + _m 
            if len(_sMsg) > 0:
                SM.sendAlertMail(_sMsg, '[UNAS-Proxy]: megrendeles lekeres hiba! Id:%s, Azon:%s' % ( c.unasId, c.code))

        unasresp = doUnasActionRequest(xmlResp, 'orders', 'Order' )
    elif actionPath == 'orderby':
        uts = MU.createTransactionId( UTSTYPE.ORDERBY )
        logging.debug("getOrderBy-TS:%d" , uts)
        xmlResp = UCH.unasGetOrderBy( path[3], path[4])
        unasresp = doUnasActionRequest(xmlResp, 'orders', 'Order', 'OrderBy')
    elif actionPath == 'products':
        uts = MU.createTransactionId( UTSTYPE.PRODUCTS )
        logging.debug("getProducts-TS:%d" , uts)
        xmlResp = UCH.unasGetProducts( '1' , 1, 0 )
        unasresp =  doUnasActionRequest(xmlResp, 'products','Product')
    elif actionPath.startswith('prodby'):
        uts = MU.createTransactionId( UTSTYPE.PRODBY )
        logging.debug("getProduct BY-TS:%d Item:%s, val:%s", uts, path[3], path[4] )
        xmlResp = UCH.unasGetProductByAzon( path[3], path[4])
        unasresp = doUnasActionRequest(xmlResp, 'prodbyid','Product')
    elif actionPath.startswith('unasprod'):
        uts = MU.createTransactionId( UTSTYPE.UNASPROD )
        logging.debug("unasprod BY-TS:%d Item:%s, val:%s", uts, path[3], path[4] )
        unasresp = UCH.unasGetProductByAzon( path[3], path[4])              # NINCS checkCacheState
    elif actionPath.startswith('inquirers'):
        prodId = actionPath[9:]
        uts = MU.createTransactionId( UTSTYPE.INQUIRERS )
        logging.debug("getProducts-TS:%d, Inquirer:%s" , uts,prodId)
        xmlResp = UCH.unasGetInquirers( prodId)
        unasresp = doUnasActionRequest(xmlResp, 'inquirers','Inquirer')
        if "OK" == "OK" if unasresp is None else unasresp:
            unasresp = '@@errors@@ - inquirers'
    elif actionPath.startswith('customers'):
        if MU.ORDER_HandleUnregistered:
            uts = MU.createTransactionId( UTSTYPE.CUSTOMERORDER )
            logging.debug("getCustomers - Unregistered in Order-TS:%d" , uts)
            xmlResp = UCH.unasGetOrderNew()
            orderCustomers = ET.fromstring('<customerPartXmlObj></customerPartXmlObj>', None)
            retV = doUnasActionRequest(xmlResp, 'orders', 'OrderCustomers', orderCustomers)
            logging.debug("getCustomers - Unregistered in Order:%s", ET.tostring(orderCustomers, encoding='utf-8', pretty_print=True)) # type: ignore
        else:
            orderCustomers = None

        # if MU.ORDER_getMissingCust:
        #     logging.debug("getCustomers - MISSING Customers (Cust in cache but missed from Symbol)")
        #     xmlResp = UCH.unasGetOrderNew()
        #     orderCustomers = doUnasActionRequest(xmlResp, 'orders', 'OrderCustomers')
        #     logging.debug("getCustomers - Unregistered in Order:%s", orderCustomers)
        # else:
        #     orderCustomers = None

        uts = MU.createTransactionId( UTSTYPE.CUSTOMERS )
        logging.debug("getCustomer-TS:%d" , uts)
        xmlResp = UCH.unasGetCustomers()
        unasresp = doUnasActionRequest(xmlResp, 'customers','Customers', orderCustomers)
    elif actionPath.startswith('unascust'):
        uts = MU.createTransactionId( UTSTYPE.UNASCUST )
        logging.debug("getCustomers-TS:%d - unascust %s, %s", uts, path[3], 'NoNe' if len(path) < 5 else path[4])
        unasresp = UCH.unasGetCustomers( path[3], None if len(path) < 5 else path[4])                # NINCS checkCacheState
    elif actionPath.startswith('customerby'):
        uts = MU.createTransactionId( UTSTYPE.CUSTOMERBY )
        logging.debug("getCustomers-TS:%d - customerby %s, %s", uts, '3-None' if len(path) < 4 else path[3], '4-None' if len(path) < 5 else path[4])
        xmlResp = UCH.unasGetCustomers( None if len(path) < 4 else path[3], None if len(path) < 5 else path[4])
        unasresp = doUnasActionRequest(xmlResp, 'customers','Customers', None)
    elif actionPath.startswith('storage'):
        uts = MU.createTransactionId( UTSTYPE.STORAGE )
        logging.debug("get Storage files-TS:%d" , uts)
        xmlResp = UCH.unasGetStorage( None if len(path) < 4 else path[3], None if len(path) < 5 else path[4]) # NOT TESTED!! NINCS checkCacheState
        unasresp = xmlResp
    elif actionPath.startswith('logger'):
        uts = MU.createTransactionId( UTSTYPE.LOGGER )
        logging.debug("Logger GET called-TS:%d" , uts)
        raise ValueError("Logger GET Not Implmented Yet!")
    elif actionPath.startswith('initcache'):
        uts = MU.createTransactionId( UTSTYPE.INITCACHE )
        logging.debug("InitCache-TS:%d" , uts)
        MU.reinitCacheState()
        unasresp = 'OKJ:{ "custs":%i , "prods":%i , "orders":%i  }' % ( len(MU.UnasCustomerList), len(MU.UnasProductList), len(MU.UnasOrderList) )
    elif actionPath.startswith('proxytest'):
        try:
            uts = MU.createTransactionId( UTSTYPE.TESTGET )
            logging.debug("proxytest-TS:%d" , uts)
            unasresp =  doProxyTest(path, None if len(path) < 4 else path[3], None if len(path) < 5 else path[4])
        except Exception as e:
            errors.append( "FATAL TEST   req: " + "/".join(path) )
            errors.append( "FATAL TEST Xcptn: " + str(e) )
        # end try
    elif actionPath.startswith('proxycontrol'):
        try:
            uts = MU.createTransactionId( UTSTYPE.PROXYCONTROLS )
            logging.debug("proxycontrol-TS:%d" , uts)
            resp =  doProxyControl(path, None if len(path) < 4 else path[3], None if len(path) < 5 else path[4])
            unasresp =  'err' if not resp else  ("OKJ:" + resp)
        except Exception as e:
            errors.append( "FATAL CONTROL   req: " + "/".join(path) )
            errors.append( "FATAL CONTROL Xcptn: " + str(e) )
        # end try
    elif actionPath.startswith('test'):
        uts = MU.createTransactionId( UTSTYPE.TESTJOE )
        logging.debug("test-TS:%d" , uts)
        unasresp =  doJoeTest(path, None if len(path) < 4 else path[3], None if len(path) < 5 else path[4])
    elif actionPath.startswith('TEST'):
        uts = MU.createTransactionId( UTSTYPE.TESTJOE )
        logging.debug("testJOE-TS:%d" , uts)
        unasresp = doJoeTEST(path)
    else:
        errors.append( "Unhandled GET req: " + "/".join(path) )
    #
    logging.info("GetReq:%s handled in:%i secs" , actionPath, MU.getCurrTime() - tsStart)
    for errItm in GBL_ErrorMessages:
        errors.append( str(errItm) )
    return unasresp    #raise  ValueError( "Err: unresolved action: %s" % actionPath)

def getErrorTextProduct(act, xmlResp):
    if xmlResp == None:
        logging.debug("Null %s response?", act.upper())
    else:
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        errorMessage = None
        for prod in root.getchildren():
            #productId = prod.find('Id').text
            productSku = prod.find('Sku').text
            status = prod.find('Status').text
            action = prod.find('Action')
            if status.lower() ==  'ok':
                MU.UnasProductList[productSku].lastmod = MU.getNowFromTS() # MU.UtcNow()
                logging.info( "%s-ok:%s", 'NoneAction' if action is None else action.text, productSku)
            else:
                errMsg = prod.find('Error').text
                GBL_ErrorMessages.append(errMsg)
                errorMessage = errMsg if errorMessage is None else  errorMessage + ' | ' + errMsg
                logging.error( "%s-%s ERR:%s", 'NoneAction' if action is None else action.text, productSku, '-' if errMsg is None else errMsg )
    return 'OK' if errorMessage is None else errorMessage

def getErrorTextOrder(act, xmlResp, symbolId, statusCode) -> str:  # @20240914 NEZDMEG!
    if xmlResp == None:
        logging.warning("Null %s response?", act.upper())
    else:
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        errorMessage = None
        for tt  in root.getchildren():
            key = tt.find('Key').text
            status = tt.find('Status').text
            action = tt.find('Action')
            if status.lower() ==  'ok':
                # find by ID
                # uoc = next((x for x in  MU.UnasOrderList.values() if x["orderKey"] == key), None )
                uoc = MU.UnasOrderList[key]
                if uoc:
                    uoc.lastmod = MU.getNowFromTS()
                    logging.info("%s-ok:%s lastMod:%i,%s",
                            'NoneAction' if action is None else action.text,
                            key,
                            uoc.lastmod, # uoc["lastmod"],
                            MU.tsToDateStr(uoc.lastmod))
                else:
                    logging.info("%s-ok:%s ",'NoneAction' if action is None else action.text, key)
                    orderRow = FBU.getOrderById(symbolId)
                    if orderRow is not None:
                        uoc = UOC.UnasOrderCache(ordKey=key, status=statusCode,
                                    sid=orderRow['Id'],lastmod = MU.getNowFromTS(), custid=orderRow["Customer"],
                                    ordcode=orderRow["PrimeVoucherNumber"]  )
            else:
                errMsg = tt.find('Error').text
                logging.error( "(setOrderStatus) %s-ERR:%s", 'NoneAction' if action is None else action, xmlResp)
                errorMessage = errMsg if errorMessage is None else  errorMessage + ' | ' + errMsg
                GBL_ErrorMessages.append(errorMessage)
    return errorMessage # type: ignore

def getXmlTag( itm, tag:str ):
    xval = None if itm.find(tag) is None else itm.find(tag).text
    return None if xval is None else xval.strip()

def doProxyTest(path, unit, id) -> str:
    logging.error("proxyTest path:%s", path)
    if "cust" == unit:
        if "caddrall" == id:
            xrx = MU.CUSTOMER_CYCLIC_INTERVAL
            MU.CUSTOMER_CYCLIC_INTERVAL = 9999999
            xmlResp = UCH.unasGetCustomers( 'ModTimeStart', str(MU.UtcNow(999999999)))
            MU.CUSTOMER_CYCLIC_INTERVAL = xrx 
            unasresp = doUnasActionRequest(xmlResp, 'customers','TestCustAddr', None)
            dom=ET.fromstring (unasresp, None)
            root=ET.fromstring(bytes('<?xml version="1.0"?><A></A>', 'utf-8'), None)
            for custItem in dom.getchildren():
                unasId = getXmlTag(custItem, 'unasId')
                custEmail = getXmlTag(custItem, 'email')
                print( f"Id:{unasId}:E:{custEmail}" )
                if custItem.find('customeraddresses') is not None:
                    for addr in custItem.find('customeraddresses').getchildren():
                        cim1 = getXmlTag(addr, 'CIM1')
                        cim2 = getXmlTag(addr, 'CIM2')
                        if cim1 is not None and cim1 != cim2 and cim1 + '.' != cim2:
                            xmlTag0 = ET.SubElement(root, 'diffed', None, None)
                            xmlTagA = ET.SubElement(xmlTag0, 'ID', None, None)
                            xmlTagA.text = f"Id:{unasId}:E:{custEmail}"
                            xmlTag1 = ET.SubElement(xmlTag0, 'cim1', None, None)
                            xmlTag2 = ET.SubElement(xmlTag0, 'cim2', None, None)
                            xmlTag1.text = cim1
                            xmlTag2.text = cim2
            outBytes=ET.tostring(root, encoding='utf-8', pretty_print=True) # type: ignore
            addresses = outBytes.decode('utf-8')
            return addresses
        elif "nullparams" == id:
            xmlArray = []
            retV = UCH.unasGetActiveCustomers()
            customers = MU.collectCustItems(retV)
            for cust in customers.values():
                xmlArray.append(UCH.UNAS_SETSYMBOLID_XML % (cust.unasId, '','') )
            if len(xmlArray) > 0:
                # xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
                xmlreq = "<Customers>%s</Customers>" % "\n".join(xmlArray)
                resp = UCH.updateCustomer(xmlreq)
                retV = UCH.unasGetActiveCustomers()
                customers = MU.collectCustItems(retV)
            MU.checkCacheState(True)
            return resp
        elif "nullsymazon" == id:
            xmlArray = []
            retV = UCH.unasGetActiveCustomers()
            customers = MU.collectCustItems(retV)
            resp = []
            for cust in customers.values():
                ucc : UCC.UnasCustomerCache = cust
                xml = UCH.updateCustomerSymbolId(ucc.unasId, '', '')
                item = ET.fromstring(bytes(xml.strip(), 'utf-8'), None).getchildren()
                resp.append(item)
            MU.checkCacheState(True)
            root = ET.Element("nullsymazon", None, None)
            #doc = ET.SubElement(root, "nullsymazon", None, None)
            for itm in resp:
                child = itm[0]
                root.append(child)
            outBytes=ET.tostring(root, encoding='utf-8', pretty_print=True) # type: ignore
            return MU.XMLTAG + outBytes.decode('utf-8')
        elif "deleteall" == id:
            xmlArray = []
            retV = UCH.unasGetActiveCustomers()
            customers = MU.collectCustItems(retV)
            xmlArray = []
            for cust in customers.values():
                ucc : UCC.UnasCustomerCache = cust
                # UCH.deleteCustomer(ucc.unasId)
                xmlArray.append( f"<Customer><Action>delete</Action><Id>{ucc.unasId}</Id></Customer>" )
            if len(xmlArray) > 0:
                resp = UCH.updateCustomer(  " ".join(xmlArray) )
            return resp
        else:
            return MU.CUSTOMER_TESTDATA1
    elif "ord" == unit:
        if "1" == id:
            pass
        else:
            return MU.ORDERSCUSTOMER_TESTDATA2
    elif "prod" == unit:
        if "nano" == id:
            pass
        else:
            return MU.PRODUCT_TESTDATA1
    else:
        pass
    return 'test-OK-x'

def doProxyControl(path, unit, id) -> str:
    if  "base" == unit:
        if "nano" == id:
            pass
        else:
            pass
    elif "customer" == unit:
##########################
        if "caddrall" == id:
            xrx = MU.CUSTOMER_CYCLIC_INTERVAL
            MU.CUSTOMER_CYCLIC_INTERVAL = 9999999
            xmlResp = UCH.unasGetCustomers( 'ModTimeStart', str(MU.UtcNow(999999999)))
            MU.CUSTOMER_CYCLIC_INTERVAL = xrx 
            unasresp = doUnasActionRequest(xmlResp, 'customers','TestCustAddr', None)
            dom=ET.fromstring (unasresp, None)
            root=ET.fromstring(bytes('<?xml version="1.0"?><A></A>', 'utf-8'), None)
            for custItem in dom.getchildren():
                unasId = getXmlTag(custItem, 'unasId')
                custEmail = getXmlTag(custItem, 'email')
                print( f"Id:{unasId}:E:{custEmail}" )
                if custItem.find('customeraddresses') is not None:
                    for addr in custItem.find('customeraddresses').getchildren():
                        cim1 = getXmlTag(addr, 'CIM1')
                        cim2 = getXmlTag(addr, 'CIM2')
                        if cim1 is not None and cim1 != cim2 and cim1 + '.' != cim2:
                            xmlTag0 = ET.SubElement(root, 'diffed', None, None)
                            xmlTagA = ET.SubElement(xmlTag0, 'ID', None, None)
                            xmlTagA.text = f"Id:{unasId}:E:{custEmail}"
                            xmlTag1 = ET.SubElement(xmlTag0, 'cim1', None, None)
                            xmlTag2 = ET.SubElement(xmlTag0, 'cim2', None, None)
                            xmlTag1.text = cim1
                            xmlTag2.text = cim2
            outBytes=ET.tostring(root, encoding='utf-8', pretty_print=True) # type: ignore
            addresses = outBytes.decode('utf-8')
            return addresses
        elif "nullparams" == id:
            xmlArray = []
            retV = UCH.unasGetActiveCustomers()
            customers = MU.collectCustItems(retV)
            for cust in customers.values():
                xmlArray.append(UCH.UNAS_SETSYMBOLID_XML % (cust.unasId, '','') )
            if len(xmlArray) > 0:
                # xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
                xmlreq = "\n".join(xmlArray)
                resp = UCH.updateCustomer(xmlreq)
                retV = UCH.unasGetActiveCustomers()
                customers = MU.collectCustItems(retV)
            #       ucc : UCC.UnasCustomerCache = cust
            #       ucc.symbolId = 0
            #       ucc.code = ''
            #       xmlArray.append(ucc.toXml())
            #   if len(xmlArray) > 0:
            #       xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
            #   resp = UCH.updateCustomer(xmlreq)
            #   retV = UCH.unasGetActiveCustomers()
            #   customers = MU.collectCustItems(retV)
            MU.checkCacheState(True)
            return resp
        elif "nullsymazon" == id:
            xmlArray = []
            retV = UCH.unasGetActiveCustomers()
            customers = MU.collectCustItems(retV)
            resp = []
            for cust in customers.values():
                ucc : UCC.UnasCustomerCache = cust
                xml = UCH.updateCustomerSymbolId(ucc.unasId, '', '')
                item = ET.fromstring(bytes(xml.strip(), 'utf-8'), None).getchildren()
                resp.append(item)
            MU.checkCacheState(True)
            root = ET.Element("nullsymazon", None, None)
            #doc = ET.SubElement(root, "nullsymazon", None, None)
            for itm in resp:
                child = itm[0]
                root.append(child)
            outBytes=ET.tostring(root, encoding='utf-8', pretty_print=True) # type: ignore
            return MU.XMLTAG + outBytes.decode('utf-8')
        elif "deleteall" == id:
            xmlArray = []
            retV = UCH.unasGetActiveCustomers()
            customers = MU.collectCustItems(retV)
            xmlArray = []
            for ucc in customers.values():
                xmlArray.append( f"<Customer><Action>delete</Action><Id>{ucc.unasId}</Id></Customer>" )
            if len(xmlArray) > 0:
                resp = UCH.updateCustomer(  " ".join(xmlArray) )
            return resp
##########################        
        elif "getAll" == id:
            resp = UCH.getCusts()
            return resp
        elif "clearparams" == id:
            xmlTag = ''
            for cust in MU.UnasCustomerList.values():
                xmlTag += UCH.UNAS_SETSYMBOLID_XML % (cust.unasId, '', '') 
            resp = UCH.updateCustomer(xmlTag)
            return resp
        elif "getby" == id:
            resp = UCH.unasGetCustomers( path[5] , path[6] )
            return resp
        elif "deletebycache" == id:
            xmlTag = ''
            for cust in MU.UnasCustomerList.values():
                xmlTag += f"<Customer><Action>delete</Action><Id>{ucc.unasId}</Id></Customer>" 
            resp = UCH.updateCustomer(xmlTag)
            return resp
        else:
            pass
    elif "initcat" == unit:
        if "getall" == id:
            resp = UCH.getCats()
            #o1 = objectify.fromstring(resp, None)
            #o2 = objectify.deannotate(o1)
            #o3 = ET.cleanup_namespaces(o2, None, None)
            #print(type(o3), o3)
            #xssss = json.dumps(o3)
            #xmlReq = None if not resp else 'OKJ:{"xmlResp" : "%s" }' % resp.replace('"', '\\"').replace("\n", "\\n").replace("\r", "").replace("\t", "")
            xmlReq = resp
            return xmlReq # type: ignore
        elif "getby" == id:
            resp = UCH.getCats( path[5] , path[6] )
            xmlReq = None if not resp else 'OKJ:{"xmlResp" : "%s" }' % resp.replace('"', '\\"').replace("\n", "\\n").replace("\r", "").replace("\t", "")
            return xmlReq # type: ignore
        elif "deleteall" == id:
            catsXml = UCH.getCats()
            cats = objectify.fromstring(catsXml[41:], None)
            req = dict({})
            xmlReq = 'OK'
            for c in cats.getchildren():
                catId = c.Id
                if catId not in req:
                    req[catId] = 0
                if c.Parent.Id > 0:
                    parentId = c.Parent.Id 
                    req[parentId] += 1 if parentId not in req else 1 + req[parentId] 
                    print(req)
            catIds = []
            for cc in req.keys():
                if req[cc] == 0:
                    catIds.append(cc)
            if len(catIds) > 0:
                resp = UCH.deleteCats(catIds)
                print(resp)
                xmlReq = resp
            return xmlReq # type: ignore
        elif "deletebyid" == id:
            # urlTags = urlParse.parse_qs(path)
            return UCH.deleteCats([ path[5] ])
        else:
            pass
    elif "initprod" == unit:
        if "getall" == id:
            return UCH.getProds()
        elif "getby" == id:
            return UCH.getProds( path[5] , path[6] )
        elif "nullparam" == id:
            xmlArray = []
            # MU.checkCacheState(True)
            idx = 0
            for prod in MU.UnasProductList.values():
                xmlArray.append(UCH.UNAS_SETPRODUCTSYMBOLID_XML % (prod.unasId, prod.sku, '1a') )
                idx = 1 + idx
                if idx > 5:
                    xmlreq = "\n".join(xmlArray)
                    resp = UCH.unasProduct_Direct(xmlreq)
                    errors = getErrorTextProduct(resp)
                    xmlArray = []
                    idx = 0
            if len(xmlArray) > 0:
                # xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
                xmlreq = "\n".join(xmlArray)
                resp = UCH.unasProduct_Direct(xmlreq)
                return resp

        elif "deleteall" == id:
            prodsXml = UCH.getProds()
            cats = objectify.fromstring(prodsXml[41:], None)
            catIds = []
            for cc in cats.getchildren():
                catIds.append(cc.Id)
            if len(catIds) > 0:
                resp = UCH.deleteProds(catIds)
                print(resp)
                xmlReq = resp
            else:
                xmlReq = 'OK'
            return xmlReq # type: ignore
        elif "deletebyid" == id:
            # urlTags = urlParse.parse_qs(path)
            return UCH.deleteProds([ path[5] ])
        else:
            pass
    return 'control-OK-x'

def doJoeTest(path, unit, id) -> str:
    logging.error("joeTest path:%s", path)
    if "cust" == unit:
        if "nano" == id:
            return MU.CUSTOMER_TESTDATA_NANO
        elif "symexOri" == id:
            return MU.CUSTOMER_TESTDATA_SYMEXORI
        elif "symex" == id:
            return MU.CUSTOMER_TESTDATA_SYMEX
        elif "symex2" == id:
            return MU.CUSTOMER_TESTDATA_SYMEX2
        elif "symex3" == id:
            return MU.CUSTOMER_TESTDATA_SYMEX3
        else:
            return MU.CUSTOMER_TESTDATA1
    elif "ord" == unit:
        if "1" == id:
            return MU.ORDERSCUSTOMER_TESTDATA1
        else:
            return MU.ORDERSCUSTOMER_TESTDATA2
    elif "prod" == unit:
        if "nano" == id:
            pass
        else:
            return MU.PRODUCT_TESTDATA1
    else:
        pass

    return "OK"

def doJoeTEST(path):
    logging.error("joeTest path:%s ", path)
    xxx = FBU.getCustomerAddressesById(203)
    pp.pprint(xxx)
    return str(xxx)
    # return str(FBU.reassignCAs( UCC.UnasCustomerCache( 12, 'emil', 'taxNo', 'UCA-201151155' )  ))
    # return str(FBU.addCustAddrDummy(-2, 335577,11,name='J1', city='J1', zip='1121', region='J1', country='J1', street='J1', house='J1'))
    #xxx = MU.saveDBcurrentDT()
    #return 'Curr DT:: %s' % xxx
    #xxx = FBU.getOrderIdByInvoice(path[3])
    # xxx = FBU.getProductNames('HF716544')
    # return 'TestResp: %s, %s' % (xxx[0], xxx[1])
    #x = FBU.getOrdersByStatusCode( '1,2,3' )
    #return 'OKJ:' + str(x).replace("{'", '{ "').replace(' None,', ' null,').replace("':", '":').replace(
    #         ", '", ', "').replace( ": '", ': "').replace("', ", '", ').replace("'}", '"}'
    #     )

#############################################################
# EMAG  ???
#############################################################
def doEmagOrder(cmd, orderId):
    if cmd == "newOrder":
        retData = "OK:" + orderId
    elif cmd == "cancelOrder":
        retData = "OK canceled:" + orderId
    elif cmd == "returnOrder":
        retData = "OK returned:" + orderId
    else:
        raise ValueError("Bad (GET) request: %s" % cmd )

    return "doEmagOrder returned! CMD: {0}, OrderID: {1} DATA: {2}".format( cmd, orderId, retData)

def doSymbolRequest(argv):
    return "doSymbolRequest returned! pPath: %s" % argv

############################
# # #def postProcessCAddresses_OLD(ucc: UCC.UnasCustomerCache):
# # #    cah = CAH( cid = ucc.symbolId, uid = ucc.unasId)
# # #    caList = cah.loadSymbolAddresses()
# # #    caDummyList = postProcessCAddresses_loadCAs(cah)
# # #    # cah.rebuildCAlist(ucc.symbolId if ucc.symbolId > 0 else -2 ) # felesleget kitorolni  ujakat felvinni NEM Dummy kent
# # #    # Duplicates
# # #    for uu in caDummyList:
# # #        if 'dummy' == uu.state:
# # #            uu.state = 'check'
# # #            for dd in caDummyList:
# # #                if "dummy" == dd.state:
# # #                    if cah.compareCA(uu, dd):
# # #                        dd.state = 'duplicate'
# # #    # Pairing w/ symbolCAs
# # #    cah.analyzeCA(caList, caDummyList)
# # #    print(caList, caDummyList)
# # #    for uu in caDummyList:
# # #        if "dummy" == uu.state:
# # #            FBU.reassignCA(uu.Id, cah.customerid)
# # #            uu.state = 'assigned'
# # #    for uu in caDummyList:
# # #        if not "assigned" == uu.state:
# # #            FBU.deleteCAbyId(uu.Id)
# # #    
# # #def postProcessCAddresses_loadCAs(cah:CAH)-> List[CA]:
# # #    caList : List[CA] = []
# # #    cols = FBU.colListCA
# # #    custCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["address"], cah.unasid )
# # #    rex = FBU.getCustomerAddressesByCode(custCode)
# # #    for r in rex:
# # #        ca = CA(
# # #            id          = cah.toInt(r[  cols.index("Id") ]),
# # #            preferred   = cah.toInt(r[  cols.index("Preferred") ]),
# # #            country     = r[  cols.index("Country") ],
# # #            region      = r[  cols.index("Region") ],
# # #            zip         = r[  cols.index("Zip") ],
# # #            city        = r[  cols.index("City") ],
# # #            street      = r[  cols.index("Street") ],
# # #            house       = r[  cols.index("HouseNumber") ],
# # #            name        = r[  cols.index("Name") ],
# # #            #contact=
# # #            #idx=
# # #            deleted     = r[  cols.index("Deleted") ],
# # #        )
# # #        ca.Code = r[  cols.index("Code") ]
# # #        ca.idx = cah.toInt(ca.Code.split('-')[2])
# # #        ca.state = 'dummy'
# # #        # cah.symbAddresses.append(ca)
# # #        caList.append(ca)
# # #    return caList
# # #def reassignCAs( custId:int, custCode:str, cust ):
# # #    symbCAs = FBU.getCustomerAddressesById( custId )
# # #    result = FBU.reassignCAs( cust )
# # #
# # #
# # #def processCAddresses_OLD(ucc: UCC.UnasCustomerCache, custSymbolId, unasCust):
# # #        isFirst=True
# # #        otherAddressIndex = 0
# # #        # custAddressesID = FBU.correctCustAddreRecordCount(ucc.symbolId, cust.Id, len(cust.Addresses.getchildren())-1)
# # #        cah = CAH( cid = custSymbolId, uid = unasCust.Id, tag = unasCust.Addresses.getchildren() )
# # #        cah.symbAddresses = cah.loadSymbolAddresses()
# # #        caMaxIdx = cah.getSymbolCAmaxIndx()
# # #        caSymbolCnt = cah.getSymbolCAactiveCnt()
# # #        for addr in unasCust.Addresses.getchildren():
# # #            otherAddressIndex += 1
# # #            sAddr = CA(unasid=unasCust.Id, idx=otherAddressIndex)
# # #            sAddr.initAddr(addr, state='unasOnly')
# # #            addr.customerAddressCode = sAddr.Code
# # #            if addr.tag == "Shipping":
# # #                sAddr.state = 'shipping'
# # #                cah.unasAddresses.append(sAddr)
# # #                if isFirst: 
# # #                    addr.unasFirstAddresItem = 1
# # #                    # Ez kell? kiszedtem az xslt/xml-bol
# # #                    # addr.forceCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["address"], ucc.unasId)
# # #                    # addr.forceSymbolId = ucc.unasId
# # #                else:
# # #                    addr.unasFirstAddresItem = 0
# # #                    isFirst = False
# # #            elif addr.tag == "Invoice":
# # #                pass # Ezt nem adom hozza a cache Cimlistajahoz! Elvileg ezt kezeli az XSLT
# # #            elif addr.tag == "Other":
# # #                if ucc.symbolId < 1:
# # #                    # Insert dummy Addr
# # #                    addr.otherAddressIndex = otherAddressIndex
# # #                    addr.skipOtherAddress = 1
# # #                    # TODO ex itt igy nem jo meg, csak a felesleget kellene felvinni!!
# # #                    # custAddressesID = FBU.correctCustAddreRecordCount(ucc.symbolId, cust.Id, len(cust.Addresses.getchildren())-1)
# # #                    streetName  = addr.Street if addr.find('StreetName') is None else addr.StreetName
# # #                    houseNumber = None if addr.find('StreetNumber') is None else addr.StreetNumber
# # #                    sAddr.Id = FBU.addCustAddrDummy(-2, ucc.unasId, otherAddressIndex,
# # #                            name=addr.Name, city=addr.City, zip=addr.ZIP, region=addr.County, country=addr.Country,
# # #                            street=streetName, house=houseNumber) # type: ignore
# # #                    sAddr.state = 'dummy'
# # #                # 
# # #                cah.unasAddresses.append(sAddr)
# # #            else: # Erre NEM is kerulhet
# # #                raise ValueError('Hibas Unas-CustomerAddressTag! unasId:%d, tag:%s', unasCust.Id, addr.tag)
# # #        #cust.Id
# # #        cah.analyzeCAlist()
# # #        cah.rebuildCAlist(ucc.symbolId if ucc.symbolId > 0 else -2 ) # felesleget kitorolni  ujakat felvinni NEM Dummy kent
# # #        ucc.unasAddrObj = cah.unasAddresses
# # #