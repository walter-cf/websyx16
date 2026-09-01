import datetime as date
import html as HTML
import json, logging
import pprint as pp
import sys
import urllib.parse as urlParse
from typing import List

import lxml. etree as ET
import lxml. objectify as objectify

import FdbUtils as FBU
import MyServer
import MySmtpClient as SM
import MyUtils as MU
import UnasConnectHelper as UCH
import UnasCustomerCache as UCC
import UnasOrderCache as UOC
import UnasProductCache as UPC
from CustomerAddressHelper import CustomerAddress as CA
from CustomerAddressHelper import CustomerAddressHelper as CAH
#from MyServer import startControlWebThread, stopControlWebThread
from MyUtilsTypes import (AlertMailType, MyProgramFlowErrorException,
                          MyProgramFlowWarningException,
                          MyWarningBreakException, ProxyErrCode,
                          ProxyObjectType)
from MyUtilsTypes import UnasTransactionType
from MyUtilsTypes import UnasTransactionType as UTSTYPE

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
            try:
                sku = prod.Sku
                upc = MU.UnasProductList.get(sku)
                if upc:
                    prod.symbolId = upc.symbolId
                    MU.getLogger().logger.info('p-Product:%s TsDiff:%i', upc.sku, MU.getCurrTime() - upc.lastmod)
                else:
                    MU.getLogger().logger.info("p-Prod %s not found in cache", sku)
                    prod.symbolId = FBU.getProductSymbolId(sku.text)
                MU.getLogger().logger.info("trfGet-Product:%s (%i), %s", sku,prod.symbolId, 'Nincs.Neve' if prod.find('Name') is None else prod.Name)
                if (MU.PRODUCTNAME_OVERWRITE):
                    if prod.find('Name') and prod.Name.text:
                        prod.NameEncoded =  urlParse.quote(prod.Name.text)
            except Exception as e:
                prod.SkipThisOrderItem = 1      # Try continue without  Bad Object
                errMsg = f"getProducts processError - Skipped : {prod.Sku}"
                MU.errorHandler(errMsg, AlertMailType(UnasTransactionType.PRODUCTS, code=ProxyErrCode.E23,
                            oid=prod.Id, otyp=ProxyObjectType.UNASPRODUCT), level = logging.ERROR, eDescr=sys.exc_info())
            finally:
                pass
    elif action == 'Order' or action == 'OrderBy' :
        for ord in root.getchildren():
            try:
                email = None if len(ord.Customer.findall('Email')) == 0 else ord.Customer.Email
                custTaxNo = ord.Customer.Addresses.Invoice.TaxNumber
                #ucc = MU.getCustomerFormCache(email, custTaxNo, ord.Customer.find('Id'))   joe@20250401 custAzon kivezetes
                ucc = MU.getCustomerFromCacheByOrder(ord.Customer)
                cust = ord.Customer
                #
                ord.symbolVouchersequenceCode = MU.SYMBOLVOUCHERSEQUENCECODE
                ord.prefixOrderId = MU.SYMBOLORDERIDPREFIX
                #
                if ucc is None or len(cust.findall('Id')) == 0: # ucc == None:
                    cust.CustSymbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["unregistered"], ord.Id) # rendeles ID, mert CustId nincs
                    ucc = UCC.UnasCustomerCache(None, email, custTaxNo, cust.CustSymbolCode, None, 'nonRegged' ) # type: ignore
                    MU.putCustomerIntoCache(ucc)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                    # end try
                else: #  TODO !!!!!  Ezzel vigyaznom kellene !!!!! UCO vs UCU nincs rendesen atgondolva!
                    cust.CustSymbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["default"], ord.Customer.Id) if ucc.code is None else ucc.code
                if ucc:
                    ucc.unasAddrXml = [] if ord.Customer.Addresses is None else [ ord.Customer.Addresses.Invoice, ord.Customer.Addresses.Shipping ] 
                #
                # get symbolId
                xmlCustSymbolId = 0

                for prms in ord.findall('Params'):
                    for prm in prms.getchildren():
                        if 'symbolId' == prm.Name:
                            if prm.Value and 'OrderBy' != xmlPart: 
                                    ord.SkipThisOrderItem = 1
                for prms in cust.findall('Params'):
                    for prm in prms.getchildren():
                        if 'symbolId' == prm.Name:
                            if prm.Value:
                                xmlCustSymbolId = int(prm.Value)
                transport, payment = transformOrderOptions(ord.Shipping.Name, ord.Payment.Name) # Transform UNAS-name to Symbol-Name
                ord.Shipping.Name = transport
                if payment.startswith('specialFunction'):
                    paymentName, paymentDays = getPaymentSpecial( payment[len('specialFunction'):], xmlCustSymbolId, cust.Id )
                    ord.paymentMethodName      = paymentName
                    ord.paymentMethodTolerance = paymentDays
                else:
                    ord.paymentMethodName      = payment
                #
                # Transport Address
                if len(cust.findall('Addresses')) > 0:
                    for addr in cust.Addresses.getchildren():
                        MU.trimAddressAttributes(addr)
                MU.getLogger().logger.info("trfGet-Ord:%s (%s)", ord.Id, email )
                # Item processing
                if len(ord.findall('Items'))>0:
                    for itm in ord.Items.getchildren():
                        if 'shipping-cost' != itm.Sku:
                            itm.computedPriceGross = itm.Quantity * itm.PriceGross
            except Exception as e:
                ord.SkipThisOrderItem = 1      # Try continue without  Bad Object
                errMsg = f"getOrder processError - Skipped : {ord.Key}"
                MU.errorHandler(errMsg, AlertMailType(UnasTransactionType.ORDERS, code=ProxyErrCode.E23,
                            oid=ord.Id, otyp=ProxyObjectType.UNASORDER), level = logging.ERROR, eDescr=sys.exc_info())
            finally:
                pass
        if len(MU.PepitaOrderList) > 0:
            for ord in MU.PepitaOrderList.values():
                pepitaOrdersXmls = ET.Element('pepitaOrdersXmls')
                pepTag = ET.SubElement(pepitaOrdersXmls, 'pepXml')
                pepTag.text = MU.toSymbolOrderXml(ord)
                root.append(pepitaOrdersXmls)
    # 
    elif action == 'OrderCustomers':
        # TODO Nincs atirva - elhanyagoltam, mert soha nem hasznaltam
        for ord in root.getchildren():
            try:
                if MU.isLogLevelTrace():
                    print(HTML.unescape(ET.tostring(ord).decode('utf-8')))        
                cust = ord.Customer
                custTaxNo = cust.Addresses.Invoice.TaxNumber
                ucc = MU.getCustomerFromCacheByOrder(cust)
                if ucc == None:
                    ord.CustSymbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % ( MU.CUSTOMER_CODE_PREFIXES["unregistered"],  ord.Id)
                    ucc = UCC.UnasCustomerCache(emil=cust.Email, taxNo=custTaxNo, code=ord.CustSymbolCode, state='nonRegged')
                    MU.putCustomerIntoCache(ucc)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                elif ucc.symbolId > 0:
                    pass # cust.SkipThisCustomerItem =  1
                else:
                    ord.CustSymbolCode = MU.mkCustomerCode( ucc )  if ucc.code is None else ucc.code
                ucc.unasAddrXml = [] if cust.find('Addresses') is None else cust.find('Addresses').getchildren()
                if len(ucc.unasAddrXml) > 0 and  CAH(0,0).compareCA(CA(0).initAddr(ucc.unasAddrXml[0]), CA(0).initAddr(ucc.unasAddrXml[1])):
                    cust.SkipAddressShipping = 1
                MU.getLogger().logger.info("trfGet-OrdCust:%s (%s)", ord.Id, cust.Email )
                if ucc.symbolId == 0:
                    xmlPart.append(cust)
            except Exception as e:
                ord.SkipThisOrderItem = 1      # Try continue without  Bad Object
                ord.Customer.SkipThisOrderItem = 1      # Try continue without  Bad Object
                errMsg = f"getOrderCustomer processError - Skipped : {ord.Key}"
                MU.errorHandler(errMsg, AlertMailType(UnasTransactionType.ORDERS, code=ProxyErrCode.E23,
                            oid=ord.Id, otyp=ProxyObjectType.UNASORDER), level = logging.ERROR, eDescr=sys.exc_info())
            finally:
                pass
        return None # az xmlPart a visszateresi ertek !
    elif action == 'Customers':
        # Recheck CustomersCache
        # sCode = None #  if MU.CREATE_CUSTOMER_MISSING: a kepzett Code ertek!
        for cust in root.getchildren():
            custTaxNo = ''
            custCode = ''
            unasCustSymbolId = 0
            ucc = None
            try:
                if len(cust.findall('Authorize')) and len(cust.find('Authorize').findall('Admin')) and cust.Authorize.Admin != 'yes':
                    cust.SkipThisCustomerItem =  1
                else:
                    custTaxNo = cust.Addresses.Invoice.TaxNumber
                    for prms in cust.findall('Params'):
                        for prm in prms.getchildren():
                            if 'symbolId' == prm.Name:
                                unasCustSymbolId = int(prm.Value.text)
                                if MU.CREATE_CUSTOMER_MISSING:
                                    cust.customerAddressCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % ( MU.CUSTOMER_CODE_PREFIXES["default"],  cust.Id)
                                    unasCustSymbolId = FBU.createCustomerIfNotExists(unasCustSymbolId, 
                                            xmlCode=cust.customerAddressCode, xmlEmail=cust.Email, xmlTaxno=custTaxNo)
                    # Get UCC cache Item
                    #ucc = MU.UnasCustomerList.get(  UCC.buildAzonData( cust.Email, custTaxNo ))
                    #if ucc is None: # try with unasId if TaxNo duplicated HACK
                    #    ucc = MU.UnasCustomerList.get('#'+str(cust.Id ))
                    unasCustUnasId = 0 if cust.Id is None else int(cust.Id.text)
                    if unasCustUnasId <= 0:
                        # Kihagyom a feldolgozasbol
                        GBL_ErrorMessages.append('UNAS-Customer ID missing from XML! NOW: %s, TS:%d, email:%s, tax:%s' % (
                                            MU.tsToDateSql( MU.getCurrTime()), MU.getTS(), cust.Email, custTaxNo ))
                        cust.SkipThisCustomerItem =  1
                    #
                    ucc = MU.getCustomerFromCache(unasCustUnasId)
                    #
                    if ucc == None:
                        custCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["default"], cust.Id)
                        ucc = UCC.UnasCustomerCache(unasCustUnasId, cust.Email, custTaxNo, custCode, 0, 'new')
                        ucc.symbolId = unasCustSymbolId
                        MU.putCustomerIntoCache(ucc)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                        ucc.unasAddrXml = [] if cust.find('Addresses') is None else cust.find('Addresses').getchildren() # type: ignore
                    elif cust.Email != ucc.email:
                        MU.getLogger().logger.warning('u-Customer[%i] in Unas-only!:%s', unasCustUnasId, ucc.email )
                        GBL_ErrorMessages.append(f"Warning! Possible Duplicate TaxNo:{ucc.taxNumber}, emils:{cust.Email} / {ucc.email} ")
                        custCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["default"], unasCustUnasId)
                        ucc = UCC.UnasCustomerCache(unasCustUnasId, cust.Email, custTaxNo, custCode, 0, 'new')
                        ucc.symbolId = unasCustSymbolId
                        #ucc.custAzon = UCC.buildCustAzonById(unasCustUnasId)
                        MU.putCustomerIntoCache(ucc)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                        MU.getLogger().logger.info('g-Customer:%d,%s TsDiff:NEW', ucc.unasId, ucc.email )
                        ucc.unasAddrXml = [] if cust.find('Addresses') is None else cust.find('Addresses').getchildren() # type: ignore
                    if ucc.symbolId == 0:
                        # ucc = UCC.UnasCustomerCache(cust.Id, cust.Email, custTaxNo, None, 0, 'new')
                        #@1 result = FBU.addCust(ucc.unasId, 'UCO-%i' % ucc.unasId)
                        #@1 ucc.symbolId = 0 if result < 0 else result
                        #@1 cust.forcedCustomerId = ucc.symbolId ### MAR NINCS az xml-ben
                        MU.putCustomerIntoCache(ucc)   # MU.UnasCustomerList[ucc.custAzon] = ucc
                        ucc.unasAddrXml = [] if cust.find('Addresses') is None else cust.find('Addresses').getchildren() # type: ignore
                        GBL_ErrorMessages.append( f"Warning[W002]:- Customer in Unas-only! Id:{cust.Id} emil:{ucc.email}")
                        MU.getLogger().logger.debug('u-Customer[%i] in Unas-only!:%s', cust.Id, ucc.email )
                    else:
                        uldStr = None if cust.Dates.Modification is None else cust.Dates.Modification.text
                        unasLastMod = 0 if uldStr is None else MU.dateStrToTs(uldStr)
                        MU.getLogger().logger.info('g-Customer:%s lastMod-symb/unas/diff:%s/%s/%i TsDiff:%i', ucc.email,
                                    MU.tsToDateStr(ucc.lastmod), uldStr, unasLastMod - ucc.lastmod, MU.getCurrTime() - ucc.lastmod)
                        ucc.unasAddrXml = [] if cust.find('Addresses') is None else cust.find('Addresses').getchildren() # type: ignore
                        symbolModTime = FBU.getModTime( ucc.symbolId, "Customer" )
                        if symbolModTime is None:
                            MU.getLogger().logger.warning('Gyanus, HIANYZO SymbolID! Azon:%d Id:%d', ucc.unasId,ucc.symbolId )
                            GBL_ErrorMessages.append( f"Warning[W001]:- Gyanus, HIANYZO SymbolID! Azon:{ucc.unasId} Id:{ucc.symbolId}")
                            ## Quick HACK - mert NINCS Symbolban es ha van symbolId-je, akkor ki kell nullazni
                            if len(cust.findall('Params')) >0:
                                for prm in cust.Params.getchildren():
                                    if 'symbolId' == prm.Name:
                                        prm.Value = ''
                            ucc.symbolId = 0
                        else: 
                            MU.getLogger().logger.warning('Cust(g):%d %s lastMod:%s(%i), unasMod:%s(%i), symbolMod:%s(%i)' % (
                                    ucc.unasId, 'Gyanus SKIP!' if unasLastMod - symbolModTime.timestamp()  < 100000   else '',
                                    MU.tsToDateStr(ucc.lastmod), ucc.lastmod, MU.tsToDateStr(unasLastMod), unasLastMod,
                                    str(symbolModTime), symbolModTime.timestamp()))
                    MU.getLogger().logger.info("trf-trfGet:%s", cust.Email )
                    # joe@20260820
                    # cust.unasCustomerCategory = MU.UnasCustomerCategoryName
                    if ucc.symbolId <= 0: # and ucc.unasId == 0 csak akkor szeretnem belerakni az xml-be, ha meg nem letezik a symbolban
                        specCatz = MU.Conf("customer.specialCategories") or []
                        if specCatz:
                            cust.unasCustomerCategory = next((x[0] for x in specCatz.values() if x[1] == cust.unasCustomerCategory), MU.UnasCustomerCategoryName ) # pyright: ignore[reportAttributeAccessIssue]

                    if len(cust.findall('Addressess')) > 0:
                        for addr in cust.Addresses.getchildren():
                            MU.trimAddressAttributes(addr)

                    # Preferred address ...
                    try:
                        if MU.HANDLE_CUSTOMERADDRESS:
                            cust.handleCustomerAddresses = 1
                            processCAddresses(ucc,unasCustSymbolId, cust)
                    except Exception as e:
                        errMsg = f"Customer-Cime hiba - valoszinuleg - nem zavar. A tesztuzemben figyelem, kesobb talan nem kell."
                        MU.errorHandler(errMsg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E08), level = logging.WARNING, eDescr=sys.exc_info())
                    # end try
                # Unregistered Customer, direct order wo regg
                # END IF Authorize.Admin == yes
            except Exception as e:
                cust.SkipThisOrderItem = 1      # Try continue without  Bad Object
                errMsg  = f"getCustomer processError - Skipped : {cust.Id}, symbolId:{unasCustSymbolId}, code:{custCode}, TaxNo:{custTaxNo}"
                errMsg += f"\r\n\t CacheItem:{ 'None' if ucc is None else ucc.toStr()}"
                MU.errorHandler(errMsg, AlertMailType(UnasTransactionType.CUSTOMERS, code=ProxyErrCode.E23,
                            oid=cust.Id or 0, otyp=ProxyObjectType.UNASCUSTOMER), level = logging.ERROR, eDescr=sys.exc_info())
            finally:
                pass

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
        print(HTML.unescape(obj_xml.decode('utf-8')))        
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
    return str(transportMode), str(paymentMethod)

def getPaymentSpecial(specCode:str, custId:int, unasId:int):
    if "01" == specCode:
        retv = FBU.getPaymentMethodByCustomerId(custId) if custId > 0 else FBU.getPaymentMethodByCustomerCode('UC_-%d' % unasId) 
        if retv is not None and len(retv) == 2:
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
        elif len(addr.findall('StreetName')) == 0:
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
        _msg = "transformGetRequestObject XMLErr-X: " + str(e)
        _msg += f"\r\nAz XML - feldolgozast -{action}/{MU.getTS()}- megszakitottam"
        MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E09), level = logging.ERROR, eDescr=sys.exc_info())
        raise MyProgramFlowErrorException(f'a megelozo xml error terminalo exceptionje(uzenetismetles), Azon:-{action}/{MU.getTS()}-')

    preparedXmlStr = preparedXml.decode('utf-8')
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
        _msg = "transformPostRequestObject XMLErr-X: " + str(e)
        _msg += f"\r\nAz XML - feldolgozast -{action}/{MU.getTS()}- megszakitottam."
        MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E10), level = logging.ERROR, eDescr=sys.exc_info())
        raise MyProgramFlowWarningException(f'a megelozo xml error terminalo exceptionje(uzenetismetles), Azon: E10-{action}/{MU.getTS()}')

    # end try
    # transform xml with xslt
    newdom = transform(dom)
    # newdom.unasFeedbackURL = None

    outBytes=ET.tostring(newdom, encoding='utf-8', pretty_print=True) # type: ignore
    if outBytes is not None:
        if MU.isLogLevelTrace():
            print(HTML.unescape(outBytes.decode('utf-8')))
        outfile = open("xmlfiles/get"+ action + ".symb." + str(MU.getTS()) + ".xml", 'a')
        outBytesStr = outBytes.decode('utf-8')
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
        raise MyWarningBreakException('Unknown action:' + action)
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
        raise MyWarningBreakException('Unknown action:' + action)
    #
    return xml

def doUnasActionRequest(xmlResp, action, actionXslt, xmlPart = None):
    MU.checkCacheState()
    if len(MU.UnasCustomerFeedbackList) > 0:
        MU.UnasCustomerFeedbackList = UCH.updateCustomerSymbolIdList(MU.UnasCustomerFeedbackList)
    #
    xmlPre = preProcessUnasGetResponse(xmlResp, action)
    xmlTrd = transformResponse(xmlPre, actionXslt, xmlPart)
    xmlRet = postProcessUnasGetResponse(xmlTrd, action)
    return xmlRet or 'OK'


def doUnasFeedback(pathArray, path, queryParams):
    MU.checkCacheState()
    if (pathArray[2] == 'oke' ):
        try:
            MU.getLogger().logger.debug("FBUNAS-OKE: {0}".format( urlParse.unquote('/'.join(pathArray)[10:] )))
            unasId = MU.getQueryParamInt(queryParams, 'id')
            symbolId = MU.getQueryParamInt(queryParams, 'symbolid')
            symbolCode = MU.getQueryParam(queryParams, 'code')
            orderKey = MU.getQueryParam(queryParams, 'orderkey')
            productSku = MU.getQueryParam(queryParams, 'sku')

            if pathArray[3].startswith('order'):
                #FBU.updateSymbolCode(symbolId, 'URE-%s-UI-%i' % (orderKey, unasId), 'CustomerOrder', 'PrimeVoucherNumber' )
                uoc = None if orderKey is None else  MU.UnasOrderList.get(orderKey)
                if orderKey is None:
                    pass # error
                elif uoc is None:
                    uoc = UOC.UnasOrderCache(ordKey=orderKey, sid=symbolId, status="pending" )# raise WalueError(f"FB-Order-Cache corrupted! Missing : {orderKey}")
                if uoc is None:
                    pass # error
                if uoc is not None and (uoc.symbolId <= 0 or not uoc.acknowledged):
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
                elif (symbolId != 0 if uoc is None else uoc.symbolId):
                    _msg = f"FB-Order-Cacche corrupted! order:{orderKey}: symbolId-s differ [Sym]{symbolId}/[Cache]{0 if uoc is None else uoc.symbolId}"
                    MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E11), level = logging.WARNING)
                    raise MyProgramFlowErrorException(_msg)
            elif  pathArray[3].startswith('pepitaorder'):
                uoc = MU.PepitaOrderList.get(unasId) # igazibol Pepita OrderId
                if uoc is None:
                    _msg = f"FBack-Pepita-Order-Cache corrupted, missing order:{unasId}"
                    MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.F50), level = logging.WARNING)
                    raise MyProgramFlowErrorException(_msg)
                #  else
                FBU.updateSymbolCode(symbolId, '%s-%s' % ( MU.getCfgVal("pepita.OrderPrefix"), unasId), 'CustomerOrder', 'PrimeVoucherNumber' )
                uoc.symbolId = symbolId
                #
                FBU.updateOrderStatus(symbolId, MU.SYMBOLORDERSTATUS)
                MU.removePepitaOrderFromCache(unasId)
                return None
            elif pathArray[3] .startswith('orderstatus'):
                pass
            elif pathArray[3] .startswith('cust'):
                if pathArray[:-1] == 'unregistered':
                    symbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["unregistered"],unasId)
                    FBU.updateSymbolCode(symbolId, symbolCode, 'Customer' )
                elif pathArray[3] == 'customer':
                    #if unasId == 256150765 or unasId == 256150420:
                    #    print(unasId)
                    ucc = next((x for x in  MU.UnasCustomerList.values() if x.unasId == unasId), None )
                    if ucc is None:
                        _msg = f'{pathArray[3]}\nCustomer cache corrupted, missing unasId:{unasId}'
                        MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E12), level=logging.ERROR )
                        MU.getLogger().logger.error("Customer cache corrupted, missing unasId:%i", unasId)
                        # raise WalueError("Customer cache corrupted, missing unasId:%i", unasId)
                    else:
                        ucc.lastmod = MU.getCurrTime()
                        if ucc.state == 'new' or (0 if ucc.symbolId is None else ucc.symbolId) == 0:
                            symbolCode = MU.CUSTOMER_CODE_PREFIXES["pattern"] % (MU.CUSTOMER_CODE_PREFIXES["default"],unasId)
                            try:
                                FBU.updateSymbolCodeIfChanged(symbolId, symbolCode, 'Customer' ) # csak a NEW statusnal kellene!!!!
                                ucc.state = 'symb'
                            except Exception as e:
                                _msg = f"feedBack-process-error: {e}\r\nstatement: updateSymbolCodeIfChanged({symbolId},{symbolCode},'Customer')"
                                _msg += f"\r\nFeedback process bmegszakitva! Az esetleges ismetleshez a keres URL: {path}"
                                MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E13), level = logging.ERROR, eDescr=sys.exc_info())
                                raise MyProgramFlowErrorException(f'a megelozo feedback errort terminalo exceptionje(uzenetismetles)', ProxyErrCode.E13)

                                # FBU.updateSymbolCode(symbolId, symbolCode+"-a", 'Customer' ) # csak a NEW statusnal kellene!!!!
                            # end try
                            if ucc.code != symbolCode or ucc.symbolId != symbolId:
                                ucc.code = symbolCode
                                ucc.symbolId = symbolId
                                if MU.BULK_FEEDBACK_CUSTOMER:
                                    MU.UnasCustomerFeedbackList.append( (unasId, symbolId, symbolCode) )
                                else:
                                    UCH.updateCustomerSymbolId(unasId, symbolId, symbolCode)
                                MU.getLogger().logger.debug("CustomerCode:%s(%i) modified at:%i,%s in cache",
                                        ucc.code, symbolId, ucc.lastmod, MU.tsToDateStr(ucc.lastmod) )
                            else:
                                MU.getLogger().logger.debug("CustomerCode:%s(%i) SKIPP mod at:%i,%s in cache",
                                        ucc.code, symbolId, ucc.lastmod, MU.tsToDateStr(ucc.lastmod) )

                        MU.getLogger().logger.info("Customer:%s(%i) lastMod:%i/%s ", ucc.code, symbolId, ucc.lastmod, MU.tsToDateStr(ucc.lastmod) )
                        MU.getLogger().logger.debug("fbUnas-Cust:%s ", ucc.toStr())
                        # ?????    Cimek !!!!
                        if MU.HANDLE_CUSTOMERADDRESS and ucc is not None :
                            if isinstance(ucc.unasAddrObj, List) and  len(ucc.unasAddrObj) > 0:
                                postProcessCAddresses(symbolId, ucc.unasAddrObj)
                        #
                elif pathArray[:-1] == 'custshipaddr':
                    pass # MU.getLogger().logger.warning('Not written Yet')
                elif pathArray[:-1] == 'custinvaddr':
                    pass # MU.getLogger().logger.warning('Not written Yet')
                elif pathArray[:-1] == 'custcontact':
                    pass # MU.getLogger().logger.warning('Not written Yet')
                elif pathArray[:-1] == 'custothaddr':
                    pass # MU.getLogger().logger.warning('Not written Yet')
                else:
                    MU.getLogger().logger.error('Not handled Customer Feedback action: %s', pathArray[:-1])
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
                    prodname = MU.getQueryParam(queryParams, 'prodname')
                    if prodname is not None:
                        name = urlParse.unquote(prodname, encoding='utf-8')
                        MU.getLogger().logger.info('Felulvagom a ProdID:%i nevet:%s!!!', symbolId, name )
                        FBU.updateProductName(symbolId, name )

        except Exception as e:
            if isinstance(e, MyProgramFlowErrorException) or isinstance(e, MyProgramFlowWarningException):
                MU.getLogger().logger.debug("MyProgramFlowErrorException : ", str(e), " / ignored")
            else:
                _err = str(e) # if not hasattr(e, 'message') else e.message
                _msg = f"\r\nFeedback-OKE process megszakitva!\r\nX: {_err}\r\nIsmetleshez az URL: {path}"
                MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E14), level = logging.ERROR, eDescr=sys.exc_info())
                raise MyProgramFlowErrorException(f'a megelozo feedback errort terminalo exceptionje(uzenetismetles)',ProxyErrCode.E14)
        # end try
    else: # Error branch
        try:
            unasId = MU.getQueryParamInt(queryParams, 'id')
            symbolId = MU.getQueryParamInt(queryParams, 'symbolid')
            symbolCode = MU.getQueryParam(queryParams, 'code')
            orderKey = MU.getQueryParam(queryParams, 'orderkey')
            errorMsg = MU.getQueryParam(queryParams, 'errormsg')
            _msg = f"""Unas adatletoltes ({pathArray[-1]}) visszaigazolas - HIBA:
                    Muvelet:{pathArray[-1]}
                    UnasId:{unasId}
                    SymbolId:{symbolId}
                    Code:{symbolCode}
                    OrderKey:{orderKey}
                    Error-Msg:{errorMsg}"
                    ----------------------------------
                    fullPath: {path}
            """
            # _subj = f"UNAS-feedBack error:({pathArray[-1]}) / {queryParams.get('orderkey') if  queryParams.get('orderkey') else queryParams.get('code')}"
            MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E15), level=logging.ERROR)
            # Clean DUMMY CustomerAddress rex
            FBU.deleteDummyCArex(unasId)

        except MyProgramFlowErrorException as pfe:
            MU.getLogger().logger.error("MyProgramFlowErrorException : ", str(pfe), " / ignored")
        except Exception as e:
            if isinstance(e, MyProgramFlowErrorException) or isinstance(e, MyProgramFlowWarningException):
                MU.getLogger().logger.debug("MyProgramFlow-Exception : ", str(e), " / ignored")
            else:
                _msg = f"FBUNAS-ERR process error:{e}"
                _msg += f"\r\nFeedback-ERR process megszakitva! Az esetleges ismetleshez a keres URL: {path}"
                MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E16), level = logging.ERROR, eDescr=sys.exc_info())
                raise MyProgramFlowErrorException(f'a megelozo feedback errort terminalo exceptionje(uzenetismetles)', ProxyErrCode.E16)

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
        unasId = 0 if len(cust.findall('Id')) == 0 else int(cust.Id.text)
        if unasId > 0:
            ucc = MU.getCustomerFromCache(unasId)
            if ucc is None: # next((x for x in UnasCustomerList.values() if x.unasId == 256185675) , None )
                unasCust = UCH.unasGetCustomers('Id', None if not cust.find('Id') else cust.Id.text )
                if unasCust is None:
                    _m = "getOrder failed!\r\nOrder Azon:%s, ID:%d\r\n\r\ngetMissingCustomersFromOrder unasCust:[%s, %s] NOT exist in UNAS" % (
                        ord.Key.text,  ord.Id.text, cust.Id, cust.Email)
                    MU.errorHandler(_m, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E17), level=logging.ERROR, subject='[UNAS-Proxy]: megrendeles lekeres hiba! Id:%s, Azon:%s' % ( ord.Id.text, ord.Key.text))
                    raise MyProgramFlowWarningException(_m, ProxyErrCode.E17)

                ucc = UCC.UnasCustomerCache(cust.find('Id') and int(cust.Id.text), cust.Email.text, None if taxTag is None else taxTag.text) # type: ignore
                unasCustObj = objectify.fromstring(unasCust.replace(MU.XMLTAG, ''), None).getchildren()
                if len(unasCustObj) == 1:
                    ucc.fromXml(unasCustObj[0])

                MU.putCustomerIntoCache(ucc) # type: ignore

            if ucc.symbolId < 1:
                # Most kell DUMMY-REC ???
                cid = createUnregisteredCustomer(ucc)
                ucc.symbolId = cid
                retXml = UCH.updateCustomerSymbolId(ucc.unasId, ucc.symbolId, ucc.code)
                retStatus = objectify.fromstring(retXml.replace(MU.XMLTAG, ''), None).getchildren()
                if "ok" == '-' if len(retStatus) < 1 else retStatus[0].Status:
                    cl.append(ucc)
                else:
                    MU.getLogger().logger.error("getMissingCustomersFromOrder :%s, Nem vart customer-Update err:%s" % ( ord.Key, retXml))
                    # raise WalueError()
        # else:: unasId == 0
    return cl

def createUnregisteredCustomer(cust:UCC.UnasCustomerCache):
    _code = cust.code if cust.code is not None and len(cust.code.strip()) > 0 else MU.mkCustomerCode(cust)
    customerId = FBU.createCustomerIfNotExists(0, xmlCode=_code, xmlEmail=cust.email, xmlTaxno=cust.taxNumber)
    cust.code = _code
    return customerId
    
def doUnasGetRequest(path, errors, qry={}) -> str:
    # reset errors
    GBL_ErrorMessages.clear()
    #
    MU.getLogger().logger.debug(path)
    actionPath = path[2]
    tsStart = MU.getCurrTime()
    # GBL_ErrorMessages.append("Test GET errMsg:%d" % tsStart)
    unasresp : str = None # type: ignore
    if (actionPath == 'orders'):
        uts = MU.createTransactionId( UTSTYPE.ORDERS )
        MU.getLogger().logger.debug("getOrderToday-TS:%d" % uts)
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
                MU.errorHandler(_sMsg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E18), level=logging.WARNING, subject='megrendeles lekeres hiba (ORDER_getMissingCust)')

        unasresp = doUnasActionRequest(xmlResp, 'orders', 'Order' )
        MU.getUnasContext().lastGetOrder = int(uts / 1000)
    elif actionPath == 'orderby':
        uts = MU.createTransactionId( UTSTYPE.ORDERBY )
        MU.getLogger().logger.debug("getOrderBy-TS:%d" , uts)
        xmlResp = UCH.unasGetOrderBy( path[3], path[4])
        unasresp = doUnasActionRequest(xmlResp, 'orders', 'Order', 'OrderBy')
    elif actionPath == 'products':
        uts = MU.createTransactionId( UTSTYPE.PRODUCTS )
        MU.getLogger().logger.debug("getProducts-TS:%d" , uts)
        xmlResp = UCH.unasGetProducts( '1' , 1, 0 )
        unasresp =  doUnasActionRequest(xmlResp, 'products','Product')
    elif actionPath.startswith('prodby'):
        uts = MU.createTransactionId( UTSTYPE.PRODBY )
        MU.getLogger().logger.debug("getProduct BY-TS:%d Item:%s, val:%s", uts, path[3], path[4] )
        xmlResp = UCH.unasGetProductByAzon( path[3], path[4])
        unasresp = doUnasActionRequest(xmlResp, 'prodbyid','Product')
    elif actionPath.startswith('unasprod'):
        uts = MU.createTransactionId( UTSTYPE.UNASPROD )
        MU.getLogger().logger.debug("unasprod BY-TS:%d Item:%s, val:%s", uts, path[3], path[4] )
        unasresp = UCH.unasGetProductByAzon( path[3], path[4])              # NINCS checkCacheState
    elif actionPath.startswith('inquirers'):
        prodId = actionPath[9:]
        uts = MU.createTransactionId( UTSTYPE.INQUIRERS )
        MU.getLogger().logger.debug("getProducts-TS:%d, Inquirer:%s" , uts,prodId)
        xmlResp = UCH.unasGetInquirers( prodId)
        unasresp = doUnasActionRequest(xmlResp, 'inquirers','Inquirer')
    elif actionPath.startswith('customers'):
        if MU.ORDER_HandleUnregistered:
            uts = MU.createTransactionId( UTSTYPE.CUSTOMERORDER )
            MU.getLogger().logger.debug("getCustomers - Unregistered in Order-TS:%d" , uts)
            xmlResp = UCH.unasGetOrderNew()
            orderCustomers = ET.fromstring('<customerPartXmlObj></customerPartXmlObj>', None)
            retV = doUnasActionRequest(xmlResp, 'orders', 'OrderCustomers', orderCustomers)
            MU.getLogger().logger.debug("getCustomers - Unregistered in Order:%s", ET.tostring(orderCustomers, encoding='utf-8', pretty_print=True)) # type: ignore
        else:
            orderCustomers = None

        # if MU.ORDER_getMissingCust:
        #     MU.getLogger().logger.debug("getCustomers - MISSING Customers (Cust in cache but missed from Symbol)")
        #     xmlResp = UCH.unasGetOrderNew()
        #     orderCustomers = doUnasActionRequest(xmlResp, 'orders', 'OrderCustomers')
        #     MU.getLogger().logger.debug("getCustomers - Unregistered in Order:%s", orderCustomers)
        # else:
        #     orderCustomers = None

        uts = MU.createTransactionId( UTSTYPE.CUSTOMERS )
        MU.getLogger().logger.debug("getCustomer-TS:%d" , uts)
        xmlResp = UCH.unasGetCustomers()
        unasresp = doUnasActionRequest(xmlResp, 'customers','Customers', orderCustomers)
        MU.getUnasContext().lastGetCustomer = int(uts / 1000)
    elif actionPath.startswith('unascust'):
        uts = MU.createTransactionId( UTSTYPE.UNASCUST )
        MU.getLogger().logger.debug("getCustomers-TS:%d - unascust %s, %s", uts, path[3], 'NoNe' if len(path) < 5 else path[4])
        unasresp = UCH.unasGetCustomers( path[3], None if len(path) < 5 else path[4])                # NINCS checkCacheState
    elif actionPath.startswith('customerby'):
        uts = MU.createTransactionId( UTSTYPE.CUSTOMERBY )
        MU.getLogger().logger.debug("getCustomers-TS:%d - customerby %s, %s", uts, '3-None' if len(path) < 4 else path[3], '4-None' if len(path) < 5 else path[4])
        xmlResp = UCH.unasGetCustomers( None if len(path) < 4 else path[3], None if len(path) < 5 else path[4])
        unasresp = doUnasActionRequest(xmlResp, 'customers','Customers', None)
    elif actionPath.startswith('storage'):
        uts = MU.createTransactionId( UTSTYPE.STORAGE )
        MU.getLogger().logger.debug("get Storage files-TS:%d" , uts)
        xmlResp = UCH.unasGetStorage( None if len(path) < 4 else path[3], None if len(path) < 5 else path[4]) # NOT TESTED!! NINCS checkCacheState
        unasresp = xmlResp
    elif actionPath.startswith('logger'):
        uts = MU.createTransactionId( UTSTYPE.LOGGER )
        MU.getLogger().logger.debug("Logger GET called-TS:%d" , uts)
        raise MyProgramFlowWarningException("Logger GET Not Implmented Yet!")
    elif actionPath.startswith('initcache'):
        uts = MU.createTransactionId( UTSTYPE.INITCACHE )
        MU.getLogger().logger.debug("InitCache-TS:%d" , uts)
        MU.reinitCacheState()
        unasresp = 'OKJ:{ "custs":%i , "prods":%i , "orders":%i  }' % ( len(MU.UnasCustomerList), len(MU.UnasProductList), len(MU.UnasOrderList) )
    elif actionPath.startswith('proxytest'):
        try:
            uts = MU.createTransactionId( UTSTYPE.TESTGET )
            MU.getLogger().logger.debug("proxytest-TS:%d" , uts)
            unasresp =  doProxyTest(path, None if len(path) < 4 else path[3], None if len(path) < 5 else path[4])
        except Exception as e:
            errors.append( "FATAL TEST   req: " + "/".join(path) )
            errors.append( "FATAL TEST Xcptn: " + str(e) )
        # end try
    elif actionPath.startswith('proxycontrol'):
        try:
            uts = MU.createTransactionId( UTSTYPE.PROXYCONTROLS )
            MU.getLogger().logger.debug("proxycontrol-TS:%d" , uts)
            resp =  doProxyControl(path, None if len(path) < 4 else path[3], None if len(path) < 5 else path[4], queryParams=qry)
            unasresp =  'err' if not resp else  ("OKJ:" + resp)
        except Exception as e:
            errors.append( "FATAL CONTROL   req: " + "/".join(path) )
            errors.append( "FATAL CONTROL Xcptn: " + str(e) )
        # end try
    elif actionPath.startswith('test'):
        uts = MU.createTransactionId( UTSTYPE.TESTJOE )
        MU.getLogger().logger.debug("test-TS:%d" , uts)
        unasresp =  doJoeTest(path, None if len(path) < 4 else path[3], None if len(path) < 5 else path[4])
    elif actionPath.startswith('TEST'):
        uts = MU.createTransactionId( UTSTYPE.TESTJOE )
        MU.getLogger().logger.debug("testJOE-TS:%d" , uts)
        unasresp = doJoeTEST(path)
    else:
        raise MyProgramFlowWarningException(f"Unhandled GET req: {'/'.join(path)}")
    #
    MU.getLogger().logger.info("GetReq:%s handled in:%i secs" , actionPath, MU.getCurrTime() - tsStart)
    for errItm in GBL_ErrorMessages:
        errors.append( str(errItm) )
    return unasresp

def getErrorTextProduct(act, xmlResp):
    errorMessage = None
    if xmlResp == None:
        MU.getLogger().logger.debug("Null %s response?", act.upper())
    else:
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        MU.getLogger().logger.debug(root.tag)
        for prod in root.getchildren():
            #productId = prod.find('Id').text
            productSku = prod.find('Sku').text
            status = prod.find('Status').text
            action = prod.find('Action')
            if status.lower() ==  'ok':
                MU.UnasProductList[productSku].lastmod = MU.getTimeFromTS() # MU.UtcNow()
                MU.getLogger().logger.info("%s-ok:%s", 'NoneAction' if action is None else action.text, productSku)
            else:
                errMsg = prod.find('Error').text
                GBL_ErrorMessages.append(errMsg)
                errorMessage = errMsg if errorMessage is None else  errorMessage + ' | ' + errMsg
                MU.getLogger().logger.error("%s-%s ERR:%s", 'NoneAction' if action is None else action.text, productSku, '-' if errMsg is None else errMsg )
    return 'OK' if errorMessage is None else errorMessage

def getErrorTextOrder(act, xmlResp, symbolId, statusCode) -> str:  # @20240914 NEZDMEG!
    if xmlResp == None:
        MU.getLogger().logger.warning("Null %s response?", act.upper())
    else:
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        MU.getLogger().logger.debug(root.tag)
        errorMessage = None
        for tt  in root.getchildren():
            key = tt.find('Key').text
            status = tt.find('Status').text
            action = tt.find('Action')
            if status.lower() ==  'ok':
                # find by ID
                # uoc = next((x for x in  MU.UnasOrderList.values() if x["orderKey"] == key), None )
                uoc = MU.UnasOrderList.get(key)
                if uoc:
                    uoc.lastmod = MU.getTimeFromTS()
                    MU.getLogger().logger.info("%s-ok:%s lastMod:%i,%s",
                            'NoneAction' if action is None else action.text,
                            key,
                            uoc.lastmod, # uoc["lastmod"],
                            MU.tsToDateStr(uoc.lastmod))
                else:
                    MU.getLogger().logger.info("%s-ok:%s ",'NoneAction' if action is None else action.text, key)
                    orderRow = FBU.getOrderById(symbolId)
                    if orderRow is not None:
                        uoc = UOC.UnasOrderCache(ordKey=key, status=statusCode,
                                    sid=orderRow[0],lastmod = MU.getTimeFromTS(), symbCustid=orderRow[1],
                                    ordcode=orderRow[2]  )
            else:
                errMsg = tt.find('Error').text
                MU.getLogger().logger.error("(setOrderStatus) %s-ERR:%s", 'NoneAction' if action is None else action, xmlResp)
                errorMessage = errMsg if errorMessage is None else  errorMessage + ' | ' + errMsg
                GBL_ErrorMessages.append(errorMessage)
    return errorMessage # type: ignore

def getXmlTag( itm, tag:str ):
    xval = None if itm.find(tag) is None else itm.find(tag).text
    return None if xval is None else xval.strip()

def doProxyTest(path, unit, id) -> str:
    MU.getLogger().logger.error("proxyTest path:%s", path)
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
                if len(custItem.findall('customeraddresses')) > 0:
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
            customers = MU.getUnasActiveCustomers()
            for cust in customers.values():
                xmlArray.append(UCH.UNAS_SETSYMBOLID_XML % (cust.unasId, '','') )
            if len(xmlArray) > 0:
                # xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
                xmlreq = "<Customers>%s</Customers>" % "\n".join(xmlArray)
                resp = UCH.updateCustomer(xmlreq)
                customers = MU.getUnasActiveCustomers()
                return resp
            MU.checkCacheState(typ=ProxyObjectType.CUSTOMER)
            return 'NoData'
        elif "nullsymazon" == id:
            xmlArray = []
            customers = MU.getUnasActiveCustomers()
            resp = []
            for cust in customers.values():
                ucc : UCC.UnasCustomerCache = cust
                xml = UCH.updateCustomerSymbolId(ucc.unasId, '', '')
                item = ET.fromstring(bytes(xml.strip(), 'utf-8'), None).getchildren()
                resp.append(item)
            MU.checkCacheState(typ=ProxyObjectType.CUSTOMER)
            root = ET.Element("nullsymazon", None, None)
            #doc = ET.SubElement(root, "nullsymazon", None, None)
            for itm in resp:
                child = itm[0]
                root.append(child)
            outBytes=ET.tostring(root, encoding='utf-8', pretty_print=True) # type: ignore
            return MU.XMLTAG + outBytes.decode('utf-8')
        elif "deleteall" == id:
            xmlArray = []
            customers =MU.getUnasActiveCustomers()
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
        if "nullparams" == id:
            pass
        elif "getNew" == id:
            pass
        elif "getAll" == id:
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

def doProxyControl(path, unit, id, queryParams = {}) -> str:
    if  "status" == unit:
        if "unaspostcnt" == id:
            return json.dumps( {  "last60min" : MU.getPacketLastIntervalCnt(60), 
                                  "last50min" : MU.getPacketLastIntervalCnt(50) , 
                                  "last40min" : MU.getPacketLastIntervalCnt(40) , 
                                  "last30min" : MU.getPacketLastIntervalCnt(30) , 
                                  "last20min" : MU.getPacketLastIntervalCnt(20) , 
                                  "last10min" : MU.getPacketLastIntervalCnt(10) 
                                } )
        elif "unaspostfree" == id:
            return json.dumps({ "free_InHour" : MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(60) , 
                                "freeAfter10" : MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(50) , 
                                "freeAfter20" : MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(40) , 
                                "freeAfter30" : MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(30) , 
                                "freeAfter40" : MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(20) , 
                                "freeAfter50" : MU.UNASCOMM_SENDPACKETMAX - MU.getPacketLastIntervalCnt(10) 
                                })
        elif "cache" == id:
            R = {}
            R["customers"] = json.dumps( list(MU.UnasCustomerList.values()), indent=3, cls=UCC.UnasCustomerCacheEncoder )
            R["products" ] = json.dumps( list(MU.UnasProductList.values()), indent=3, cls=UPC.UnasProductCacheEncoder )
            R["orders"   ] = json.dumps( list(MU.UnasOrderList.values()), indent=3, cls=UOC.UnasOrderCacheEncoder )
            R["badOrders"] = json.dumps( list(MU.UnasBadOrderList.values()), indent=3, cls=UOC.UnasOrderCacheEncoder )
            return json.dumps( R )
        
        elif "ordercache" == id:
            R = []
            uoc = {}
            if len(queryParams) > 0:
                if queryParams['op'] is None:
                    while uoc is not None:
                        uoc = next((x for x in  MU.UnasOrderList.values() if queryParams['val'] == str(eval(f"x.{queryParams['key']}")) ), None )
                        if uoc is not None:
                            R.append(uoc)
                elif 'eq' == queryParams['op']:
                    while uoc is not None:
                        uoc = next((x for x in  MU.UnasOrderList.values() if queryParams['val'] == str(eval(f"x.{queryParams['key']}")) ), None )
                        if uoc is not None:
                            R.append(uoc)
                elif 'gt' == queryParams['op']:
                    while uoc is not None:
                        uoc = next((x for x in  MU.UnasOrderList.values() if queryParams['val'] > str(eval(f"x.{queryParams['key']}")) ), None )
                        if uoc is not None:
                            R.append(uoc)
                elif 'lt' == queryParams['op']:
                    while uoc is not None:
                        uoc = next((x for x in  MU.UnasOrderList.values() if queryParams['val'] < str(eval(f"x.{queryParams['key']}")) ), None )
                        if uoc is not None:
                            R.append(uoc)
                else:
                    while uoc is not None:
                        uoc = next((x for x in  MU.UnasOrderList.values() if queryParams['val'] in str(eval(f"x.{queryParams['key']}")) ), None )
                        if uoc is not None:
                            R.append(uoc)
            elif len(path) > 6:
                    while uoc is not None:
                        uoc = next((x for x in  MU.UnasOrderList.values() if path[6] == str(eval(f'x.{path[5]}')) ), None )
                        if uoc is not None:
                            R.append(uoc)
            elif len(path) > 5:
                    if path[5].upper().startswith('UC'):
                        uoc = next((x for x in  MU.UnasOrderList.values() if x['Code'] == eval(f'x.{path[5]}').upper()), None )
                    else:
                        uoc = MU.UnasOrderList.get(path[5])
                    if uoc is not None:
                        R.append(uoc)
            else:
                for uoc in MU.UnasOrderList.values():
                    R.append(uoc)
            return json.dumps(R, indent=3, cls=UOC.UnasOrderCacheEncoder)
        elif "customercache" == id:
            R = []
            for ucc in MU.UnasCustomerList.values():
                    R.append(ucc)
            return json.dumps( R, indent=3, cls=UCC.UnasCustomerCacheEncoder )
        elif "productcache" == id:
            R = []
            for upc in MU.UnasProductList.values():
                    R.append(upc)
            return json.dumps( R, indent=3, cls=UPC.UnasProductCacheEncoder )
        elif "badordercache" == id:
            return json.dumps( list(MU.UnasBadOrderList.values()), indent=3, cls=UOC.UnasOrderCacheEncoder )
        else:
            pass
    elif "startwebctrl" == unit:
        MyServer.startControlWebThread()
    elif "stopwebctrl" == unit:
        MyServer.stopControlWebThread()
    elif "saveProxyContext" == unit:
        MU.saveUnasProxyContext()
    elif "saveBatchContext" == unit:
        MU.saveUnasBatchContext()
    elif "order" == unit:
        if "getByCustCode" == id:
            rows = FBU.getOrdersByCustomerCode('UCO%' if len(path) < 6 else path[5])
            return "{}" # custRowsToJson(rows)
        elif "deleteByUCO" == id:
            FBU.delOrdersCustomerCode('UCO%' if len(path) < 6 else path[5])
            return "OK"
    elif "ord" == unit:
        if "nullparams" == id:
            xmlArray = []
            xmlResp = UCH.unasGetActiveOrders()
            orders = MU.collectOrderItems(xmlResp)
            for ord in orders.values():
                xmlArray.append(UCH.UNAS_SETORDERSYMBOLID_XML % (ord.orderKey, '') )
            if len(xmlArray) > 0:
                # xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
                xmlReq = "\n".join(xmlArray)
                resp = UCH.unasOrder_Direct(xmlReq)
                MU.checkCacheState(typ=ProxyObjectType.ORDER)
                return resp
        elif "getnew" == id:
            return UCH.unasGetOrderNew()
        elif "getnewjs" == id:
            return MU.unasXmltoJSON( UCH.unasGetOrderNew() )
        elif "getall" == id:
            return UCH.unasGetActiveOrders()
        elif "getalljs" == id:
            return MU.unasXmltoJSON( UCH.unasGetActiveOrders() )
        else:
            pass
    elif "customer" == unit:
        #
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
                if len(custItem.findall('customeraddresses')) > 0:
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
        elif "nullparamsJoe" == id or "nullparams" == id:
            joeOnly = "nullparamsJoe" == id
            xmlArray = []
            customers = MU.getUnasActiveCustomers()
            resp = 'Error?'
            for cust in customers.values():
                if joeOnly == False or cust.email.lower().startswith('joe'):
                    xmlArray.append(UCH.UNAS_SETSYMBOLID_XML % (cust.unasId, '','') )
            if len(xmlArray) > 0:
                # xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
                xmlreq = "\n".join(xmlArray)
                resp = UCH.updateCustomer(xmlreq)
                customers = MU.getUnasActiveCustomers()
            #       ucc : UCC.UnasCustomerCache = cust
            #       ucc.symbolId = 0
            #       ucc.code = ''
            #       xmlArray.append(ucc.toXml())
            #   if len(xmlArray) > 0:
            #       xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
            #   resp = UCH.updateCustomer(xmlreq)
            #   retV = UCH.unasGetActiveCustomers()
            #   customers = MU.collectCustItems(retV)
            MU.checkCacheState(typ=ProxyObjectType.CUSTOMER)
            return resp
        elif "nullparams" == id:
            xmlArray = []
            customers = MU.getUnasActiveCustomers()
            resp = 'Eerr??'
            for cust in customers.values():
                xmlArray.append(UCH.UNAS_SETSYMBOLID_XML % (cust.unasId, '','') )
            if len(xmlArray) > 0:
                # xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
                xmlreq = "\n".join(xmlArray)
                resp = UCH.updateCustomer(xmlreq)
                customers = MU.getUnasActiveCustomers()
            #       ucc : UCC.UnasCustomerCache = cust
            #       ucc.symbolId = 0
            #       ucc.code = ''
            #       xmlArray.append(ucc.toXml())
            #   if len(xmlArray) > 0:
            #       xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
            #   resp = UCH.updateCustomer(xmlreq)
            #   retV = UCH.unasGetActiveCustomers()
            #   customers = MU.collectCustItems(retV)
            MU.checkCacheState(typ=ProxyObjectType.CUSTOMER)
            return resp
        elif "nullsymazon" == id:
            xmlArray = []
            customers = MU.getUnasActiveCustomers()
            resp = []
            for cust in customers.values():
                ucc : UCC.UnasCustomerCache = cust
                xml = UCH.updateCustomerSymbolId(ucc.unasId, '', '')
                item = ET.fromstring(bytes(xml.strip(), 'utf-8'), None).getchildren()
                resp.append(item)
            MU.checkCacheState(typ=ProxyObjectType.CUSTOMER)
            root = ET.Element("nullsymazon", None, None)
            #doc = ET.SubElement(root, "nullsymazon", None, None)
            for itm in resp:
                child = itm[0]
                root.append(child)
            outBytes=ET.tostring(root, encoding='utf-8', pretty_print=True) # type: ignore
            return MU.XMLTAG + outBytes.decode('utf-8')
        elif "deleteByUCO" == id:
            FBU.delCustomerByUCO('UCO%' if len(path) < 6 else path[5])
            return '{"st":"OK"}'
        elif "deleteByCacheFDB" == id:
            deleted = []
            cursor = None # Szegeny ember tranzakcioja :(
            for cust in MU.UnasCustomerList.values():
                cursor = FBU.delCustomerById(cust.symbolId, False, cursor)
                cust.symbolId = 0
                deleted.append(cust.symbolId)
            FBU.delCustomerById(0, commit=True, cur=cursor)
            return str(deleted)
        #elif "deleteallJoe" == id:
        #    xmlArray = []
        #    retV = UCH.unasGetActiveCustomersJoe()
        #    customers = MU.collectCustItems(retV)
        #    xmlArray = []
        #    for ucc in customers.values():
        #        xmlArray.append( f"<Customer><Action>delete</Action><Id>{ucc.unasId}</Id></Customer>" )
        #    if len(xmlArray) > 0:
        #        resp = UCH.updateCustomer(  " ".join(xmlArray) )
        #    return resp
        elif "deleteall" == id:
            xmlArray = []
            customers = MU.getUnasActiveCustomers()
            xmlArray = []
            for ucc in customers.values():
                xmlArray.append( f"<Customer><Action>delete</Action><Id>{ucc.unasId}</Id></Customer>" )
            if len(xmlArray) > 0:
                resp = UCH.updateCustomer(  " ".join(xmlArray) )
                return resp
##########################        
        elif "getAll" == id:
            resp = UCH.unasGetActiveCustomers()
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
                xmlTag += f"<Customer><Action>delete</Action><Id>{cust.unasId}</Id></Customer>" 
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
            prods = objectify.fromstring(catsXml[41:], None)
            req = dict({})
            xmlReq = 'OK'
            for c in prods.getchildren():
                catId = c.Id
                if catId not in req:
                    req[catId] = 0
                if c.Parent.Id > 0:
                    parentId = c.Parent.Id 
                    req[parentId] += 1 if parentId not in req else 1 + req[parentId] 
                    print(req)
            prodIds = []
            for cc in req.keys():
                if req[cc] == 0:
                    prodIds.append(cc)
            if len(prodIds) > 0:
                resp = UCH.deleteCats(prodIds)
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
            idx = 0
            for prod in MU.UnasProductList.values():
                xmlArray.append(UCH.UNAS_SETPRODUCTSYMBOLID_XML % (prod.unasId, prod.sku, '1a') )
                idx = 1 + idx
                if idx > 5: # TODO Ez fingom sincs micsoda, vagy mit akartam
                    xmlreq = "\n".join(xmlArray)
                    resp = UCH.unasProduct_Direct(xmlreq)
                    errors = getErrorTextProduct('initprod/nullparam', resp)
                    xmlArray = []
                    idx = 0
            if len(xmlArray) > 0:
                # xmlreq = doUnasActionRequest( "<Customers>%s</Customers>" % "\n".join(xmlArray), 'simpleTransform','CustNullParams')                
                xmlreq = "\n".join(xmlArray)
                resp = UCH.unasProduct_Direct(xmlreq)
                return resp

        elif "deleteall" == id:
            prodsXml = UCH.getProds()
            prods = objectify.fromstring(prodsXml[41:], None)
            prodIds = []
            for cc in prods.getchildren():
                prodIds.append(cc.Id)
            if len(prodIds) > 0:
                resp = UCH.deleteProds(prodIds)
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
    elif "showerror" == unit:
        pass # GBL_Errors if path6 = clear then cleRGBLErr array
    elif "lasterrors" == unit:
        pass # from Mysql?
    return '{"err":"Unhandled action: %s"}' % '/'.join(path)

def doJoeTest(path, unit, id) -> str:
    MU.getLogger().logger.error("joeTest path:%s", path)
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
    MU.getLogger().logger.error("joeTest path:%s ", path)
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
        raise MyProgramFlowWarningException("Bad (GET) request: %s" % cmd )

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
# # #                raise WalueError('Hibas Unas-CustomerAddressTag! unasId:%d, tag:%s', unasCust.Id, addr.tag)
# # #        #cust.Id
# # #        cah.analyzeCAlist()
# # #        cah.rebuildCAlist(ucc.symbolId if ucc.symbolId > 0 else -2 ) # felesleget kitorolni  ujakat felvinni NEM Dummy kent
# # #        ucc.unasAddrObj = cah.unasAddresses
# # #