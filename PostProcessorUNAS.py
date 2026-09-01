import datetime as date
import json
import logging
import sys
import tempfile

import lxml as LXML
import requests
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from lxml import objectify

import FdbUtils as FBU
import MySmtpClient as SM
import MyUtils as MU
import UnasAuth
import UnasConnectHelper as UCH
import UnasCustomerCache as UCC
from MyUtilsTypes import (AlertMailType, MyProgramFlowErrorException,
                          MyProgramFlowWarningException, ProxyErrCode,
                          UnasTransactionType)
from UnasProductCache import UnasProductCache as UPC
from xmlclazz.customerOffer import CustomerOffers
from xmlclazz.discountRules import DiscountRules 

GBL_ErrorMessages = []

def isCustomerTypeChecked(cust):
    # TODO MyUTils CONTSTANT kent kezelni felteteles ellenorzeskent
    return cust.customerstatus == 1 and cust.supplierstatus == 0 and cust.code.text.startswith(MU.CUSTOMER_CODE_PREFIXES["default"])

#TRANSFORMERS
def transformUnasRequestObject(root, xsltFilename):
    if   xsltFilename == 'Product':
        for prod in root.getchildren():
            if MU.isLogLevelTrace:
                print(prod.code)
            upc = MU.UnasProductList.get(str(prod.code))
            if upc is not None and upc.state == UPC.ProductState_PENDING:
                upc = MU.refreshProductItem(upc)
            if prod.webdisplay == 1 or ((UPC.ProductStatus_INACTIVE  if upc is None else upc.status) != UPC.ProductStatus_INACTIVE):
                #if upc:
                #    postDiffTime = MU.getCurrTime() - upc.lastmod
                #    logging.error("p-Product:%s, diff:%i %s", upc.sku, postDiffTime, 'CYCLIC!!!' if postDiffTime < 2*MU.GETPRODUCT_INTERVAL else '')
                if upc == None: # UNAS-bol hianyzik
                    if (prod.deleted == 0):
                        prod.unasProductAction = 'add'
                        prod.unasProductStatus = UPC.ProductStatus_INACTIVE if prod.webdisplay == 0 else UPC.ProductStatus_NEW # Active+ New
                        MU.UnasProductList[prod.code] = UPC(0, prod.code, prod.id, 0.0, 27, UPC.ProductState_LIVE)
                    else:
                        prod.SkipThisItem = '1'
                        #return None # Nem viszem fel, ha mar ugyis deleted a symbolban
                elif upc.symbolId > 0 and MU.UtcNow(MU.GETPRODUCT_INTERVAL * 2 + 1) < upc.lastmod: # Perhaps cyclic mod
                    # prod.SkipThisItem = '1'
                    _m = "Cust SKIPPED while possible(1) cyclic-mod.\n ** uid:%i, sid:%i, code:%s, lastMod:%i TSdiff:%i" % (
                                upc.unasId, upc.symbolId, upc.sku, upc.lastmod, MU.getCurrTime() - upc.lastmod )
                    GBL_ErrorMessages.append(_m)
                    logging.warning(_m )
                else:  # UNAS-ban azonositottam SKU alapjan es LIVE
                    prod.unasProductId = upc.unasId
                    upc.state = UPC.ProductState_PENDING
                    if prod.deleted == 1:
                        prod.unasProductAction = 'delete'
                        prod.unasProductStatus = UPC.ProductStatus_INACTIVE
                    else:
                        prod.unasProductAction = 'modify'
                        if prod.webdisplay == 0:
                            prod.unasProductStatus = UPC.ProductStatus_INACTIVE
                            upc.status = UPC.ProductStatus_INACTIVE
                        elif upc.status == UPC.ProductStatus_INACTIVE:
                        # elif prod.webdisplay == 1 and upc.status != UPC.ProductStatus_NEW and upc.status != UPC.ProductStatus_NOTAVAILABLE:
                            # TODO @20260106 Igazibol UNAS-Inactive kellene nezni!!
                            # upc.status == UPC.ProductStatus_INACTIVE
                            prod.unasProductStatus = UPC.ProductStatus_ACTIVE
                            upc.status = UPC.ProductStatus_ACTIVE
                #
                # GuaranteeMonths, Attributes, TargetCategory (symbolId, Gyarto, VTSZ, EAN)
                attribs = ''
                if len(prod.findall('productattributes')) > 0:
                    for attr in prod.productattributes.getchildren():
                        attribs = ' | ' if len(attribs) > 0 else '' + attr.name + ':'+ attr.value
                prod.Attributes = None if len(attribs) < 1 else attribs
                #
                prod.unasActionWebCategory = None if MU.UnasProductWebCategoryId is None else MU.UnasProductWebCategoryId
                prod.unasActionWebCategoryName = None if MU.UnasProductWebCategoryName is None else MU.UnasProductWebCategoryName
                prod.unasExtendedAttributes = 1 if MU.PRODUCT_EXTATTRIBS else None
            else:
                logging.debug(f"Product skipped while webDisplay=0 Code:{prod.code}")
                prod.SkipThisItem = '1'

    elif xsltFilename == 'ProductPrice':
        for prod in root.getchildren():
            #if prod.webdisplay == 1:
            if "ObjectifiedElement" in str(type(prod)): # azt hiszem, a pepita prod-okol tudott jonni StringElement
                upc = None if not hasattr(prod,'productcode') else MU.UnasProductList.get(str(prod.productcode))
                if upc == None: # UNAS-bol hianyzik
                    logging.warning("Skipped - UNASban nem letezo termek CODE/Sku: " + str(prod.productcode))
                    prod.SkipThisItem = '1'
                else:  # UNAS-ban azonositottam SKU alapjan es LIVE
                    prod.unasProductId = upc.unasId
                    prod.symbolIdIsNull = 1 if upc.symbolId == 0 else 0
                    # 20250529@joe prod.retValProduct = 0
                    isPriceFound = False
                    foundCat = -99999
                    for pi in prod.price:
                        # 20250529@joe prod.retValProduct = 1
                        specialPriceCat = next(( x[1] for x in MU.PRODUCT_PRICECAT_SPECIALS if x[0] == pi.pricecategoryName.text), None)
                        if pi.pricecategory == MU.PRODUCT_PRICECAT_BASE and pi.priceCurrency == 'HUF':
                            pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                        elif pi.pricecategory == MU.PRODUCT_PRICECAT_UNIQUE:
                            raise MyProgramFlowErrorException("Nem lekezelt EGYEDI ProductPrice", ProxyErrCode.UNKNOWN)
                        elif specialPriceCat:
                            pi.unasPriceSpecial = 1
                            pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                            pi.groupName  = pi.pricecategoryName.text
                            pi.offerStart = pi.validfrom.text.replace('-', '.')
                            pi.offerEnd   = MU.EPOCH_ENDDATE
                            MU.checkUnasCustomerGroup(pi.groupName)
                        else:
                            pi.SkipThisItem = 1  # Issue:0003 - joe@20250625 Multiple Price in PriceCat:18
                            #  pi.retValValid = 0
                        #
            #else:
            #    logging.debug(f"Product skipped while webDisplay=0 Code:{prod.code}")
        if next((False for x in prod.findall('price') if x.find('SkipThisItem') is None ), True):
            prod.SkipThisItem = '1'
        # ProductPrice endz
    elif xsltFilename == 'ProductQuantity':
        for prod in root.getchildren():
            upc = MU.UnasProductList.get(prod.ProductCode)
            upc = None if not hasattr(prod,'ProductCode') else MU.UnasProductList.get(str(prod.ProductCode))
            if upc == None: # UNAS-bol hianyzik
                # raise ValueError("Modositasi kiserlet UNASban nem letezo termekre CODE/Sku: " + prod.ProductCode)
                logging.warning("Skipped - UNASban nem letezo termek CODE/Sku: " + str(prod.ProductCode))
                print("Warning: SKIPPED-Modositasi kiserlet UNASban nem letezo termekre CODE/Sku: " + str(prod.ProductCode))
                prod.SkipThisItem = '1'
            else:  # UNAS-ban azonositottam SKU alapjan es LIVE
                prod.unasProductId = upc.unasId
                prod.symbolIdIsNull = 1 if upc.symbolId == 0 else 0
                # TODO Ha tobb raktar lesz, akkor raktarankent kell nyilvantartanom a upc.stocks -ban
                if prod.Warehouse == -1:
                    upc.qty = prod.Quantity
                _Quant = int( prod.Quantity 
                                        - ( 0 if prod.find('StrictAllocate') is None else prod.StrictAllocate ) 
                                        - ( 0 if prod.find('NonStrictAllocate') is None else prod.NonStrictAllocate)
                                        )
                prod.CurrentQuantity = '0' if _Quant <= 0 else str(_Quant)
                prod.retValValid = 2
    elif xsltFilename == 'BilledOrder':
        # <CustomerOrder> <Id>8</Id> <VoucherNumber>RECW2024/00004</VoucherNumber> <PrimeVoucherNumber>H24-75175-100004</PrimeVoucherNumber> <VoucherSequenceCode>B2C</VoucherSequenceCode> </CustomerOrder>            
        for ord in root.getchildren():
            unasOrderKey = str(ord.PrimeVoucherNumber)[ 1 + len(MU.SYMBOLORDERIDPREFIX): ]
            ord.PrimeVoucherNumber = unasOrderKey
            ord.unasOrderStatus = MU.ORDER_STATUS_CLOSE # vagy 
            ord.unasOrderStatus = 'Megrendelés lezárva'
            # xmlResp = UCH.unasSetOrderStatus( unasOrderKey, ord.unasOrderStatus, ord.Id, True, "Rendelését számláztuk, kiszállítása folyamatban van.")
    elif xsltFilename == 'Customer':
        for cust in root.getchildren():
            if cust.id > 0 and isCustomerTypeChecked(cust):
                try:
                    # Cache ??
                    # ucc = MU.getCustomerFormCache(cust.email, cust.taxnumber, cust.id ) joe@20250401 custAzon kivezetes
                    ucc = MU.getCustomerFormCacheByCode(cust.code )
                    if ucc is None:
                        ucc = next((x for x in  MU.UnasCustomerList.values() if x.code == cust.code), None )
                        logging.warning("PostCust:MISSING! Eml:%s - Ado:%s", cust.email, cust.taxnumber )
                        # Skipping ?? UNAS-bol hianyzik
                        if cust.deleted == 1 or cust.id == -2: # SKIP
                            logging.warning( "PtrfCust-Skipping DELETED nonexisting(UNAS) cust** sid:%i, code:%s", cust.id, cust.code )
                            if ucc is None:
                                ucc = UCC.UnasCustomerCache()
                            ucc.state = MU.CACHESTATE_deleted # type: ignore
                            cust.unasCustomerAction = 'skip'
                            cust.SkipThisItem = '1' 
                        else: # NEW 
                            cust.unasCustomerAction = MU.UNASACTION_add
                            ucc = UCC.UnasCustomerCache(emil=cust.email, taxNo=cust.taxnumber, state='new' )
                            ucc.lastmod = 0
                            MU.putCustomerIntoCache(ucc) # MU.UnasCustomerList[ucc.custAzon] = ucc
                            logging.error( f"WARNING only! New Cust added From SYMBOL to UNAS!:{ucc.toStr}"  )
                        #
                    elif ucc.state == "unreg" or str(cust.code).startswith( MU.CUSTOMER_CODE_PREFIXES["unregistered"] ): # type: ignore # Unregistered, nem kell felvinni
                            cust.SkipThisItem = '1' 
                            logging.warning( "PtrfCust-Skipping Unregged cust** sid:%i, code:%s", cust.id, cust.code )
                    elif MU.UtcNow(ucc.lastmod) < MU.CUSTOMER_CYCLIC_INTERVAL: # Cyclic Update? skipping
                        cust.SkipThisItem = '1'
                        _m = "Cust(p) SKIPPED while possible(2) cyclic-mod.**uid:%i, sid:%i, code:%s, lastMod:%i TSdiff:%i" % (
                                        ucc.unasId, ucc.symbolId, ucc.code, ucc.lastmod, MU.UtcNow(ucc.lastmod)) 
                        # ??? SM.sendAlertMail(_m)
                        logging.warning(_m)
                    else: # UNAS-ban azonositottam SKU alapjan es LIVE
                        # logging.warning( "POST-trfCust:%s ", ucc.toStr())
                        cust.unasCustomerId = ucc.unasId
                        if  cust.deleted == 1:             # 'live' == ucc.state and
                            logging.info( f"PostCust-DELETE** sid:{ucc.symbolId}, code:{ucc.code}, lastMod:{ucc.lastmod}")
                            # cust.unasCustomerAction = 'delete'
                            cust.SkipThisItem = '1'   # 20260202 delete ignore
                            ucc.state = MU.CACHESTATE_marked4delete
                        else:
                            cust.unasCustomerAction = 'modify'
                            logging.debug( f"PostCust-mod: uid:{ucc.unasId}, sid:{ucc.symbolId}, code:{ucc.code}, lastMod:{ucc.lastmod}")
                    #
                    # Cimek - hibajavitas:
                    if MU.HANDLE_CUSTOMERADDRESS and cust.find('SkipThisItem') is None:
                        cust.handleCustomerAddresses = 1
                        prepareCustomerAddresses(cust)
                    else:
                        pass
                except Exception as e:
                    GBL_ErrorMessages.append( f"Customer: {cust.name},SID:{cust.id}, Err: {str(e)}" )
                    cust.SkipThisItem = '1'
            # end try
            else:
                ucc = None
                logging.debug(f"Customer skipped while ID < 0:{cust.id}")
                cust.SkipThisItem = '1' 
                if MU.isLogLevelTrace():
                    logging.error(f"Customer skipped via custId:{cust.id}/{cust.code.text}, status:{cust.customerstatus}, supplier:{ cust.supplierstatus}" )
                    logging.debug(f"Customer skipped tag:: {ET.tostring(cust)}" )
            if MU.isLogLevelTrace():
                print( f"Posting wo UCC:{cust.code}" if ucc is None else f"Posting custUCC:{ucc.toStr()}" )
    elif xsltFilename == 'CustomerX':
        for cust in root.getchildren():
            if cust.id > 0:
                try:
                    # ucc = MU.UnasCustomerList.get( UCC.buildAzonData( cust.email, cust.taxnumber ))
                    # ucc = MU.getCustomerFormCache(cust.email, cust.taxnumber, cust.id )  joe@20250401 custAzon kivezetes
                    ucc = MU.getCustomerFromCache(cust.id)
                    postDiffTime = MU.getCurrTime()
                    if ucc:
                        postDiffTime -= ucc.lastmod
                        logging.error("PtrfCust:%d, LM:%i:%s diff:%i %s", ucc.unasId, ucc.lastmod, MU.tsToDateStr(ucc.lastmod),
                                    postDiffTime, 'CYCLIC!!!' if postDiffTime < 2*MU.CUSTOMER_CYCLIC_INTERVAL else '')
                    #elif cust.id == -2: # mar lew van kezelve if id > 0 -val
                    #    cust.SkipThisItem = '1' 
                    else:
                        # try with Code ????
                        ucc = next((x for x in  MU.UnasCustomerList.values() if x.code == cust.code), None )
                        logging.warning("PtrfCust:MISSING! Eml:%s - Ado:%s", cust.email, cust.taxnumber )
                    #
                    if ucc.state == "unreg" or str(cust.code).startswith( MU.CUSTOMER_CODE_PREFIXES["unregistered"] ): # type: ignore # Unregistered, nem kell felvinni
                            cust.SkipThisItem = '1' 
                            logging.warning( "PtrfCust-Skipping Unregged cust** sid:%i, code:%s", cust.id, cust.code )
                    elif ucc == None: # UNAS-bol hianyzik
                        if cust.deleted == 1 or cust.id == -2:
                            cust.SkipThisItem = '1' 
                            logging.warning( "PtrfCust-Skipping DELETED nonexisting(UNAS) cust** sid:%i, code:%s", cust.id, cust.code )
                            cust.unasCustomerAction = 'skip'
                        elif str(cust.code).startswith('UCU'): # Unregistered, nem kell felvinni
                            cust.SkipThisItem = '1' 
                            logging.warning( "PtrfCust-Skipping Unregged cust** sid:%i, code:%s", cust.id, cust.code )
                        else:
                            cust.unasCustomerAction = 'add'
                            #ucc = UCC.UnasCustomerCache(None, cust.email, None, 0, 'new')
                            ucc = UCC.UnasCustomerCache(emil=cust.email, taxNo=cust.taxnumber, state='new' )
                            ucc.lastmod = 0
                            MU.putCustomerIntoCache(ucc) # MU.UnasCustomerList[ucc.custAzon] = ucc
                    #elif ucc.symbolId > 0 and MU.UtcNow(MU.GETCUSTOMER_INTERVAL * 2 + 1) < ucc.lastmod: # Perhaps cyclic mod
                    elif postDiffTime < MU.CUSTOMER_CYCLIC_INTERVAL:
                        cust.SkipThisItem = '1'
                        logging.warning( "Cust(p) SKIPPED while possible(3) cyclic-mod.**uid:%i, sid:%i, code:%s, lastMod:%i TSdiff:%i",
                                        ucc.unasId, ucc.symbolId, ucc.code, ucc.lastmod, postDiffTime )
                    else: # UNAS-ban azonositottam SKU alapjan es LIVE
                        logging.warning( "POST-trfCust:%s ", ucc.toStr())
                        cust.unasCustomerId = ucc.unasId
                        if ucc.symbolId is None:
                            ucc.symbolId = 0
                        if ucc.lastmod is None:
                            ucc.lastmod = 0
                        if  cust.deleted == 1:             # 'live' == ucc.state and
                            logging.warning( "PtrfCust-DELETE** sid:%i, code:%s, lastMod:%i",
                                            ucc.symbolId, 'None' if ucc.code is None else ucc.code, ucc.lastmod )
                            # cust.unasCustomerAction = 'delete'
                            cust.SkipThisItem = '1'   # 20260202 delete ignore
                            ucc.state = MU.CACHESTATE_marked4delete
                        else:
                            cust.unasCustomerAction = 'modify'
                            logging.warning( "PtrfCust-mod: uid:%i, sid:%i, code:%s, lastMod:%i",
                                        0 if ucc.unasId is None  else ucc.unasId,
                                        0 if ucc.symbolId is None else ucc.symbolId,
                                        'None' if ucc.code is None else ucc.code,
                                        ucc.lastmod )
                    #
                    # Cimek - hibajavitas:
                    if MU.HANDLE_CUSTOMERADDRESS and cust.find('SkipThisItem') is None:
                        # invoice cimek defa/hianyzo values???
                        cust.handleCustomerAddresses = 1
                        cust.invoicestreet = addressDefaValue(cust.invoicestreet, 'HIANYZO ADAT **')
                        cust.unasCountryCode = MU.getCountryCode(cust.invoicecountry.text, False) or 'hu'
                        # ShippingAddress = ET.SubElement(cust, "shippingaddress", nsmap=None, attrib=None)
                        selectedOther4ShipAddr = None
                        if len(cust.findall('customeraddresses')) > 0:
                            for addr in cust.customeraddresses.getchildren():
                                if addr.deleted == 1:
                                    addr.SkipThisItem = 1
                                elif isEmptyCA(addr):
                                    addr.SkipThisItem = 1
                                else:
                                    if addr.preferred == 1:
                                        # copyAddrTag(addr, ShippingAddress)
                                        selectedOther4ShipAddr = addr
                                        cust.shippingaddress = addr
                                        addr.unasCountryCode = MU.getCountryCode(cust.invoicecountry if addr.country.text is None else addr.country.text, False) or 'hu'
                                    elif selectedOther4ShipAddr is None:
                                        selectedOther4ShipAddr = addr # Ha nem lenne preferred, akkor az elso lesz
                        #
                        if cust.find('shippingaddress') is None:
                            shippin = ET.SubElement(cust, 'shippingaddress', None, None)
                        if selectedOther4ShipAddr is None:
                            cust.shippingaddress.name             = cust.name            
                            cust.shippingaddress.zip              = cust.invoicezip             
                            cust.shippingaddress.city             = cust.invoicecity            
                            cust.shippingaddress.region           = cust.invoiceregion          
                            cust.shippingaddress.street           = cust.invoicestreet          
                            cust.shippingaddress.house            = cust.invoicehousenumber           
                            cust.shippingaddress.country          = cust.invoicecountry         
                            cust.shippingaddress.companytaxnumber = cust.taxnumber
                            cust.shippingaddress.iscompany        = cust.iscompany       
                            cust.shippingaddress.unasCountryCode  = MU.getCountryCode(cust.invoicecountry, False) or 'hu'
                        else:
                            cust.shippingaddress.name             = selectedOther4ShipAddr.name            
                            cust.shippingaddress.zip              = selectedOther4ShipAddr.zip             
                            cust.shippingaddress.city             = selectedOther4ShipAddr.city            
                            cust.shippingaddress.region           = selectedOther4ShipAddr.region          
                            cust.shippingaddress.street           = selectedOther4ShipAddr.street          
                            cust.shippingaddress.house            = selectedOther4ShipAddr.housenumber           
                            cust.shippingaddress.country          = selectedOther4ShipAddr.country         
                            cust.shippingaddress.companytaxnumber = selectedOther4ShipAddr.companytaxnumber
                            cust.shippingaddress.iscompany        = selectedOther4ShipAddr.iscompany       
                            cust.shippingaddress.unasCountryCode  = MU.getCountryCode(selectedOther4ShipAddr.country, False) or 'hu'
                            selectedOther4ShipAddr.SkipThisItem = 1
                    # Cimek endz
                except Exception as e:
                    GBL_ErrorMessages.append( f"Customer: {cust.name},SID:{cust.id}, Err: {str(e)}" )
                    cust.SkipThisItem = '1'
            # end try
            else:
                logging.debug(f"Customer skipped while ID < 0:{cust.id}")
                cust.SkipThisItem = '1' 
    #
    #
    elif xsltFilename == 'DiscountRules':
        rules = DiscountRules.from_xml(root)
        # OR simple check root tag just now
        for rule in root.getchildren():
            match (rule.tag):
                case "CustomerVoucherDiscounts":
                    pass
                case "PaymentMethods":
                    logging.debug("PaymentMethods")
                    for pm in rule.getchildren():
                        logging.debug("PaymentMethod: %s, %d" , pm.PaymentMethodName, pm.DiscountPercent)
                case "ProductCategoryDiscounts":
                    pass
                case "ProductCustomerDiscounts":
                    pass
                case "TransportModes":
                    pass
                case "TransportModes":
                    logging.debug("TransportMode")
                    for pm in rule.getchildren():
                        logging.debug("TransportMode: %s, %d" , pm.TransportModeName, pm.Discountpercent)
                case _:
                    logging.debug("Default Rule: %s" , rule.text)
        return None
    # 
    elif xsltFilename == 'CustomerOffer':
        offers = CustomerOffers.from_xml(root)
        for offer in offers.customer_offers or []:
            isNewRecord = MU.createShadowOffer(offer)
            #
            if isNewRecord:
                for cust in ([] if offer.customer_offer_customers is None else offer.customer_offer_customers.customer_offer_customer or []):
                    ucc = next((x for x in  MU.UnasCustomerList.values() if x.symbolId == int(cust.customer)), None )
                    if ucc is not None:
                        grpName = MU.mkUniqueGroupName(cust.customer) # or offer.name or 'Unknown'
                        MU.addCustomerToUnasCustomerGroup( ucc.unasId, ucc.email, grpName)
                        cg = FBU.getField( 'select CC."Name" from "Customer" as CU  join "CustomerCategory" as  CC on (CC."Id" = CU."CustomerCategory") where CU."Id" = ?' , cust.customer ) or None
                        if cg !=  ucc.specialCustomerCategory:
                            MU.setSpecialPrices(cust, ucc, cg)
                        #
                        for det in [] if offer.customer_offer_details is None else offer.customer_offer_details.customer_offer_detail or []:
                            sku = MU.getSkuBySymbolId(int(det.product or 0))
                            upc = next((x for x in  MU.UnasProductList.values() if x.sku == sku), None )
                            if upc:
                                MU.checkUnasCustomerDetail(grpName, det, sku, offer.valid_from.replace('-', '.') or MU.todayStr(), offer.valid_to.replace('-', '.') or MU.EPOCH_ENDDATE )
            # Termek kedvezmeny
            # ???
        return None
    #
    else: # Untransformed action
        logging.warning( "Untransformed action:%s", xsltFilename)
    #
    objectify.deannotate(root)
    ET.cleanup_namespaces(root) # type: ignore
    obj_xml = ET.tostring(root)
    #        return str(outBytes, 'utf-8').replace('<?xml version="1.0"?>',"")
    # print(type(obj_xml))
    return str(obj_xml, encoding='utf-8').replace('<?xml version="1.0"?>',"")

def isEmptyCA(ca) :
    # ca.zip is None
    return True  if not isXmlTagNotEmpty(ca.zip) else int(ca.zip.text) < 1

def isXmlTagNotEmpty(s):
    return len('' if s is None else '' if s.text is None else s.text.strip()) > 0

def prepareCustomerAddresses(cust):
    # invoice cimek defa/hianyzo values???
    cust.invoicestreet = addressDefaValue(cust.invoicestreet, 'HIANYZO ADAT **')
    cust.unasCountryCode = MU.getCountryCode(cust.invoicecountry.text, False) or 'hu'
    # ShippingAddress = ET.SubElement(cust, "shippingaddress", nsmap=None, attrib=None)
    selectedOther4ShipAddr = None
    if len(cust.findall('customeraddresses')) > 0:
        for addr in cust.customeraddresses.getchildren():
            if addr.deleted == 1:
                addr.SkipThisItem = 1
            elif isEmptyCA(addr):
                addr.SkipThisItem = 1
            else:
                addr.unasCountryCode = MU.getCountryCode(cust.invoicecountry if addr.country.text is None else addr.country.text, False) or 'hu'
                if addr.preferred == 1:
                    # copyAddrTag(addr, ShippingAddress)
                    selectedOther4ShipAddr = addr
                    # cust.shippingaddress = addr
                elif selectedOther4ShipAddr is None:
                    selectedOther4ShipAddr = addr # Ha nem lenne preferred, akkor az elso lesz
    #
    # Create Addresses.Shipping 
    shippin = cust.find('shippingaddress')
    if shippin is None:
        shippin = ET.SubElement(cust, 'shippingaddress', None, None)
    if selectedOther4ShipAddr is None: # Create Shippin from Invoice addr
        shippin.name             = cust.name
        shippin.zip              = cust.invoicezip
        shippin.city             = cust.invoicecity
        shippin.region           = cust.invoiceregion
        shippin.street           = cust.invoicestreet
        # shippin.house            = cust.invoicehousenumber
        shippin.country          = cust.invoicecountry
        shippin.companytaxnumber = cust.taxnumber
        shippin.iscompany        = cust.iscompany
        shippin.unasCountryCode  = MU.getCountryCode(cust.invoicecountry, False) or 'hu'
    else: # copy Selected to Shippin AND Skip Addr in customerAddresses struct
        shippin.name             = selectedOther4ShipAddr.name            
        shippin.zip              = selectedOther4ShipAddr.zip             
        shippin.city             = selectedOther4ShipAddr.city            
        shippin.region           = None if selectedOther4ShipAddr.find("region") is None  else selectedOther4ShipAddr.region
        shippin.street           = selectedOther4ShipAddr.street          
        # shippin.house            = selectedOther4ShipAddr.housenumber           
        shippin.country          = selectedOther4ShipAddr.country         
        shippin.companytaxnumber = selectedOther4ShipAddr.companytaxnumber
        shippin.iscompany        = selectedOther4ShipAddr.iscompany       
        shippin.unasCountryCode  = MU.getCountryCode(selectedOther4ShipAddr.country, False) or 'hu'
        selectedOther4ShipAddr.SkipThisItem = 1


def isAddressesSame(a1, a2):
    if a1 is None or a2 is None:
        return False
    bName = a1.name.text == a2.name.text
    bStreet = a1.street.text == a2.street.text
    bStreetnumber = a1.housenumber.text == a2.housenumber.text
    bCity = a1.city.text == a2.city.text
    bCounty = a1.region.text == a2.region.text
    bCountry = a1.country.text == a2.country.text
    bZip = a1.zip.text == a2.zip.text
    return bName and bStreet and bStreetnumber and bCity and bCounty and bCountry and bZip 

def addressDefaValue(tag, defa:str='HIANYZO ADAT *') -> str:
    if tag is None:
        return defa
    if tag.text is None:
        return defa
    return tag.text if len(tag.text) > 0 else defa

def prepareXslt(xsltFilename, xml, xcv):
    if xsltFilename == 'Product':
        pass
    #
    return xcv

def prepareUnasReply(xmlReq, xsltFilename):
    xmlEnc='utf-8'
    if xmlReq[30:36] == 'utf-16':
        xmlEnc='utf-16'
    #
    xml = bytes(bytearray(xmlReq, encoding=xmlEnc))
    try:
        xmlObj = objectify.fromstring(xml,None)
        preparedXml = transformUnasRequestObject(xmlObj, xsltFilename)
    except ET.XMLSyntaxError as e:
        alertType = AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E21)
        MU.writeErrorSql(xml, alertType)
        MU.errorHandler(e.msg, alertType, level = logging.ERROR, eDescr=sys.exc_info())        
        raise  MyProgramFlowErrorException('XML Err:' + e.msg)

    if (preparedXml == None):
        return None

    # read xslt file
    xcv_0 = open('xslt/unas/set'+ xsltFilename + '.xslt').read()
    xcv = prepareXslt(xsltFilename, xmlReq, xcv_0)
    transform = ET.XSLT(ET.XML( bytes(xcv, 'utf-8'), None))
    # transform xml with xslt
    dom = ET.fromstring(preparedXml, None)
    newdom = transform( dom )

    if xsltFilename in [ 'ProductPrice', 'CustomerOffer']:
        # new_fileDescriptor, filename = tempfile.mkstemp()
        filename = f"xmlfiles/set{xsltFilename}.unas.{str(MU.getTS())}.xml"
        newdom.write_output(filename)
        content = open(filename).read()

        if content.startswith('<?xml version="1.0"'):
            startPos = content.index('?>')
            content = content[3+startPos:]
        elif content.startswith('<?xml version="1.0" encoding="utf-16" ?>'):
            content = content.replace('<?xml version="1.0" encoding="utf-16" ?>', '')

        return content
    elif newdom is not None:
        outBytes = bytes(newdom) # ET.tostring(newdom, pretty_print=True)
        if outBytes is not None:
            outStr = outBytes.decode()
            if MU.isLogLevelDebug():
                print(outStr)
            outfile = open("xmlfiles/set"+ xsltFilename + ".unas." + str(MU.getTS()) + ".xml", 'a')
            outfile.write(outStr)
            return outStr.replace('<?xml version="1.0"?>','')
    return None

def prepareUnasReply_TEST(xmlReq, xsltFilename):
    xmlEnc='utf-8'
    if xmlReq[30:36] == 'utf-16':
        xmlEnc='utf-16'
    #
    xml = bytes(bytearray(xmlReq, encoding=xmlEnc))
    try:
        xmlObj = objectify.fromstring(xml, None)
        preparedXml = transformUnasRequestObject(xmlObj, xsltFilename)
    except ET.XMLSyntaxError as e:
        logging.debug(e.msg)
        logging.debug(xml)
        logging.debug(xml.decode())
        raise  MyProgramFlowWarningException('XML Err:' + e.msg)

    if (preparedXml == None):
        return None

#      preparedXml = '''<?xml version="1.0" encoding="UTF-8"?>
#  <ProductPrices>
#    <ProductPrice>
#      <product>11119</product>
#      <productcode>LSUFAN1</productcode>
#      <price>
#        <pricecategory>-1</pricecategory>
#        <pricecategoryName>Lista ar</pricecategoryName>
#        <priceCurrency>HUF</priceCurrency>
#        <quantityunit>db</quantityunit>
#        <value>1190</value>
#        <validfrom>2019-08-02</validfrom>
#      </price>
#      <price>
#        <pricecategory>14</pricecategory>import tempfile
#  
#        <pricecategoryName>Ivory</pricecategoryName>
#        <priceCurrency>EUR</priceCurrency>
#        <quantityunit>db</quantityunit>
#        <value>2.5</value>
#        <validfrom>2020-02-13</validfrom>
#      </price>
#      <price>?xmldata='
#        <pricecategory>21</pricecategory>
#        <pricecategoryName>Emag HU</pricecategoryName>
#        <priceCurrency>HUF</priceCurrency>
#        <quantityunit>db</quantityunit>
#        <value>392.91</value>
#        <validfrom>2022-08-31</validfrom>
#      </price>
#    </ProductPrice>
#    <ProductPrice>
#      <product>120</product>
#      <productcode>44443</productcode>
#      <price>
#        <pricecategory>21</pricecategory>
#        <pricecategoryName>Emag HU</pricecategoryName>
#        <priceCurrency>HUF</priceCurrency>
#        <quantityunit>db</quantityunit>
#        <value>3148.818</value>
#        <validfrom>2021-03-16</validfrom>
#      </price>
#      <price>
#        <pricecategory>11</pricecategory>
#        <pricecategoryName>RETAIL-1</pricecategoryName>
#        <priceCurrency>HUF</priceCurrency>?xmldata='
#        <quantityunit>db</quantityunit>
#        <value>4399</value>
#        <validfrom>2018-10-25</validfrom>
#      </price>
#    </ProductPrice>
#    <ProductPrice>
#      <product>114</product>
#      <productcode>43554</productcode>
#      <price>
#        <pricecategory>21</pricecategory>
#        <pricecategoryName>Emag HU</pricecategoryName>
#        <priceCurrency>HUF</priceCurrency>
#        <quantityunit>db</quantityunit>
#        <value>2755.118</value>
#        <validfrom>2021-03-16</validfrom>
#      </price>
#      <price>
#        <pricecategory>11</pricecategory>
#        <pricecategoryName>RETAIL-1</pricecategoryName>
#        <priceCurrency>HUF</priceCurrency>
#        <quantityunit>db</quantityunit>
#        <value>3999</value>
#        <validfrom>2018-10-25</validfrom>
#      </price>
#    </ProductPrice>
#  </ProductPrices>    
#    '''.replace('\n','')
#    bytes(preparedXml, 'utf-8')
    # read xslt file
    xcv_0 = open('xslt/unas/set'+ xsltFilename + '.xslt').read()
    xcv = prepareXslt(xsltFilename, xmlReq, xcv_0)
    transform = ET.XSLT(ET.XML( bytes(xcv, 'utf-8'), None))
    # transform xml with xslt
    dom = ET.fromstring(bytes(preparedXml, 'utf-8'), None)
    newdom = transform( dom )
    outBytes=ET.tostring(newdom, pretty_print=True) # type: ignore
    if outBytes is not None:
        outStr = outBytes.decode()
        outStr = outStr.replace('<?xml version="1.0"?>','')
        if MU.isLogLevelDebug():
            print(outStr)
        outfile = open("xmlfiles/set"+ xsltFilename + ".unas." + str(MU.getTS()) + ".xml", 'a')
        outfile.write(outStr)
        return outStr
    return None

def preProcessUnasPostRequest(action, xml):
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
    elif action == 'fulfilled':
        pass
    elif action == 'offer':
        pass
    elif action == 'finalize':
        pass
    elif action == 'returnOK':
        pass
    elif action == 'synclog':
        pass
    elif action == 'logger':
        pass
    else:
        raise MyProgramFlowWarningException('Unknown action:' + action)
    #
    outfileReq = open("xmlfiles/post-"+ action +".req." + str(MU.getTS()) + ".xml", 'a')
    outfileReq.write(xml)
    #
    return xml

# @request Processor
def doUnasRequest(action, postData, pathParam3 = None, errors = []):
    # reInit errors holder
    GBL_ErrorMessages.clear()
    transStarted = MU.getCurrTime()
    # print(postData)
    # XXXXtoken = UnasAuth.doAuth() # '7526191af38b98c0ce0334b0325a6be92adb7df3'
    logging.info("unasPost-path:%s", action)
    logging.debug("token:%s, xml:%s", 'xxx', postData)
    MU.checkCacheState()
    unasResp ='OK'
    if (action == 'product'):
        unasResp = "???"
        uts = MU.createTransactionId( UnasTransactionType.PRODUCT )
        logging.debug("setProduct-TS:%d" % uts)
        if MU.isLogLevelDebug():
            print(postData)

        xmlReq = preProcessUnasPostRequest(action, postData)
        if xmlReq.count('<?xml version="1.0"') > 1:
            _m=f"Multiple xml tag in product request! TS:{MU.getTS()}"
            logging.error(_m)
            logging.error(postData)
            raise MyProgramFlowErrorException(_m, ProxyErrCode.E41)
        xmlReq = prepareUnasReply(xmlReq, "Product" )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            if (not MU.PRODUCT_BULK) or (pathParam3 == 'direct'):
                xmlResp = UCH.unasProduct_Direct(xmlReq)
                unasResp = postProcessUnasPostRequest(action, xmlResp)
            else:
                MU.UnasSetProductsXmlPart += xmlReq.replace('<?xml version="1.0"?>', '')
                MU.LastActivity = MU.UtcNow(0)
        # return "OK"
    elif action == 'inventory':
        uts = MU.createTransactionId( UnasTransactionType.INVENTORY )
        logging.debug("setInventory-TS:%d" % uts)
        unasResp = "???"
        xmlReq_0 = preProcessUnasPostRequest(action, postData)
        xmlReq = prepareUnasReply(xmlReq_0, "ProductQuantity" )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            #xmlResp = unasProduct( xmlReq, token ) # Ez valojaban Product modositas az UNASban
            #postProcessUnasPostRequest(action, xmlResp, ts)
            if (not MU.PRODUCT_BULK) or (pathParam3 == 'direct'):
                xmlResp = UCH.unasProduct_Direct(xmlReq)
                unasResp = postProcessUnasPostRequest(action, xmlResp)
            else:
                MU.UnasSetProductsXmlPart += xmlReq.replace('<?xml version="1.0"?>', '')
                MU.LastActivity = MU.UtcNow(0)
        # return "OK"
    elif action == 'price':
        uts = MU.createTransactionId( UnasTransactionType.PRICE )
        logging.debug("setPrice-TS:%d" % uts)
        unasResp = "???"
        #
        xmlReq_0 = preProcessUnasPostRequest(action, postData)
        xmlReq = prepareUnasReply(xmlReq_0, "ProductPrice" )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            # xmlReq = xmlReq.replace('<?xml version="1.0"?>', '')            
            if (not MU.PRODUCT_BULK) or (pathParam3 == 'direct'):
                xmlResp = UCH.unasProduct_Direct(xmlReq)
                unasResp = postProcessUnasPostRequest(action, xmlResp)
            else:
                MU.UnasSetProductsXmlPart += xmlReq.replace('<?xml version="1.0"?>', '')
                MU.LastActivity = MU.UtcNow(0)
        # return "OK"
    elif action == 'doc':
        uts = MU.createTransactionId( UnasTransactionType.DOC )
        logging.debug("setDocuments-TS:%d" % uts)

        xmlReq = preProcessUnasPostRequest(action, postData)
        # ????? preProcessUnasPostRequest ??? transformResponse(xmlResp, 'Document')
        xmlResp = UCH.unasDummyAction( xmlReq, action )
        unasResp = postProcessUnasPostRequest(action, xmlResp)
        # return "OK"
    elif action == 'pic':
        uts = MU.createTransactionId( UnasTransactionType.PIC )
        logging.debug("setPictures-TS:%d" % uts)

        xmlReq = preProcessUnasPostRequest(action, postData)
        xmlResp = UCH.unasDummyAction( xmlReq, action )
        #  ????? preProcessUnasPostRequest ??? transformResponse(xmlResp, 'Picture')
        unasResp = postProcessUnasPostRequest(action, xmlResp)
        # return "OK"
    elif action == 'cat':
        uts = MU.createTransactionId( UnasTransactionType.CAT )
        logging.debug("setCategory-TS:%d" % uts)

        xmlReq_0 = preProcessUnasPostRequest(action, postData)
        # Egyelore nincs megvalositva
        # xmlReq = prepareUnasReply(xmlReq_0, "Category", ts )
        # xmlResp = unasCats( xmlReq, token )
        # unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
        unasResp = "OK"
    elif action == 'customer':
        unasResp = "???"
        uts = MU.createTransactionId( UnasTransactionType.CUSTOMER )
        logging.debug("setCustomer-TS:%d" % uts)

        postData = postData.replace('&amp;#', '&#')
        xmlReq_0 = preProcessUnasPostRequest(action, postData)
        xmlReq = prepareUnasReply(xmlReq_0, "Customer")
        if len('' if xmlReq is None else xmlReq) > 0:
            # xmlReq = xmlReq.replace('<?xml version="1.0"?>', '')            
            if (not MU.CUSTOMER_BULK) or (pathParam3 == 'direct'):
                xmlResp = UCH.unasCustomer_Direct(xmlReq)
                unasResp = postProcessUnasPostRequest(action, xmlResp)
            else:
                MU.UnasSetCustomersXmlPart += xmlReq # type: ignore
                logging.debug("LEN xml:%i, tot:%s", len( xmlReq ), len( MU.UnasSetCustomersXmlPart )) # type: ignore
                MU.LastActivity = MU.UtcNow(0)
        # return "OK"
    elif action == 'pricerule':
        uts = MU.createTransactionId( UnasTransactionType.PRICERULE )
        logging.debug("Pricerule-TS:%d" % uts)

        xmlReq = preProcessUnasPostRequest(action, postData)
        xmlResp = '<PriRulz>'
        xml = prepareUnasReply(xmlReq, "PriceruleMethod")
        if xml is not None:
            xmlResp += UCH.unasDummyAction( xml, "PriceruleMethod" )
            # meg hozzadadoik ... !!! unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
        xml = prepareUnasReply(xmlReq, "PriceruleDiscountCustomer")
        if xml is not None:
            xmlResp += UCH.unasDummyAction( xml, "PriceruleDiscountCustomer" )
            # meg hozzadadoik ... !!! unasResp += "\n" + postProcessUnasPostRequest(action, xmlResp, ts)
        xml = prepareUnasReply(xmlReq, "PriceruleDiscountProdCategory")
        if xml is not None:
            xmlResp += UCH.unasDummyAction( xml, "PriceruleDiscountProdCategory" )
            # meg hozzadodik ... !!! unasResp += "\n" + postProcessUnasPostRequest(action, xmlResp, ts)
        xml = prepareUnasReply(xmlReq, "PriceruleDiscountVoucher")
        if xml is not None:
            xmlResp += UCH.unasDummyAction( xml, "PriceruleDiscountVoucher" )
            # meg hozzadadoik ... !!! unasResp += "\n" + postProcessUnasPostRequest(action, xmlResp, ts)
        xmlResp = xmlResp + '</PriRulz>'
        unasResp = postProcessUnasPostRequest(action, xmlResp)
        #return "OK"
    elif action == 'offer':
        uts = MU.createTransactionId( UnasTransactionType.OFFER )
        logging.debug("Vevoi akcio - TS:%d" % uts)
        if MU.isLogLevelDebug():
            print(postData)
        xmlReq = preProcessUnasPostRequest(action, postData)
        xmlReq = prepareUnasReply(xmlReq, "CustomerOffer")
        #if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
        #    xmlResp = "pillanatnyilag SKIP ALL !" # UCH.unasOrder_Direct(xmlReq)
        #    unasResp = postProcessUnasPostRequest(action, xmlResp)
        return "OK" if xmlReq is None else xmlReq # Always return OK!!!
    elif action == 'fulfilled':
        uts = MU.createTransactionId( UnasTransactionType.BILLED )
        logging.debug("Order - szamlazva-TS:%d" % uts)
        if MU.isLogLevelDebug():
            print(postData)
        xmlReq = preProcessUnasPostRequest(action, postData)
        xmlReq = prepareUnasReply(xmlReq, "BilledOrder")
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            xmlResp = UCH.unasOrder_Direct(xmlReq)
            unasResp = postProcessUnasPostRequest(action, xmlResp)
        # return "OK"
    elif action == 'bulkupload':
        uts = MU.createTransactionId( UnasTransactionType.BLKUPLOAD )
        logging.debug("Bulk Upload-TS:%d" % uts)
        xmlReq = preProcessUnasPostRequest(action, postData)
        xmlResp = unasBulkUpload()
        #  ????? preProcessUnasPostRequest ???  transformResponse(xmlResp, 'Finalize')
        unasResp = postProcessUnasPostRequest(action, xmlResp)
        #return "OK"
    elif action.startswith('returnOK'):
        uts = MU.createTransactionId( UnasTransactionType.RETURNOK )
        logging.debug("returnOK-TS:%d" % uts)
        xmlReq = preProcessUnasPostRequest(action, postData)
        logging.debug(xmlReq)
        unasResp = "OK"
    elif action.startswith('synclog'):
        # logging.error("synclog NOT IMPLEMENTED")
        xmlReq = preProcessUnasPostRequest(action, postData)
        uts = MU.createTransactionId( UnasTransactionType.SYNCLOG )
        logging.debug("syncLog-TS:%d" % uts)
        logging.debug(xmlReq)
        # print(xmlReq)
        unasResp = ''
    elif action =='proxycontrol':
        uts = MU.createTransactionId( UnasTransactionType.PROXYCONTROL )
        logging.debug("setProduct-TS:%d" % uts)
        return doProxyControl(pathParam3, postData )
    elif action.startswith('TEST'):
        uts = MU.createTransactionId( UnasTransactionType.TESTPOST )
        logging.debug("setProduct-TS:%d" % uts)
        return doJoetest(pathParam3, postData )

    logging.info("PostReq:%s handled in:%i" , action, MU.getCurrTime() - transStarted)
    if len(GBL_ErrorMessages) > 0:
        for errItm in GBL_ErrorMessages:
            errors.append(errItm)
    return unasResp

def doProxyControl(postData, pPath = []):
    postData = postData.replace('&amp;#', '&#')
    #xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
    #
    xmlReq = None
    if len(pPath) > 1:
        action = pPath[1]
        if 'unasDirectAction' == pPath[0]:
            xmlReq = prepareUnasReply(postData, action)
            return 'OK' if xmlReq is None or len(xmlReq) < 1 else UCH.unasDirectXml(pPath[1], xmlReq, None if len(pPath) < 3 else pPath[2])
        elif 'customer' == pPath[0]:
            if 'create199' == pPath[1]:
                jsObj = json.loads(postData)
                xml = jsObj["customerXml"] # next(iter(jsObj.values()))
                xmlReq = prepareUnasReply(xml, 'Customer')
                # dom = xml.dom.minidom.parseString(xmlResp)
                # xmlReq = dom.toprettyxml()
                
        elif 'unasDirect' == pPath[0]:
            xxx = UCH.unasDirectXml(pPath[1], postData)
        elif 'setcats' == pPath[0]:
            if 'create' == action:
                catName = json.loads(postData)["name"]
                xmlReq = UCH.addCatBbyName( catName )
            else:
                pass
        else:
            xmlReq = prepareUnasReply(postData, action)
        #
        parser = ET.XMLParser(remove_blank_text=True )
        element = ET.XML(xmlReq, parser)   # LXML.etree.ElementTree.XML(xmlResp, parser=None, encoding='unicode')
        # ET.indent(element,space=4)
        xmlReq = ET.tostring(element, encoding='unicode', pretty_print=True, method='xml') # type: ignore
        return xmlReq
    else:
        logging.error("Bad POST-ProxyControl request: %s" % " , ".join(pPath))
        return None

    
def doJoetest(action, postData):
    postData = postData.replace('&amp;#', '&#')
    xmlReq_0 = preProcessUnasPostRequest(action, postData)
    xmlReq = prepareUnasReply(xmlReq_0, "Customer")
    return xmlReq
    #return 'TestPOSTresp:%s, %s, %s' % path % str(FBU.getProductNames('HF716544'))
#
# Egyelore csak logol,
# de itt lehet az ID-ket visszairni a symbolba (xmlResp-ban benne van)
def getErrorTextOrder(action, xmlResp):
    if xmlResp == None:
        logging.debug("Null %s response?", action.upper())
    else:
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        errorMessage = None
        for prod in root.getchildren():
            productSku = prod.find('Key').text
            status = prod.find('Status').text
            action = prod.find('Action')
            if status.lower() ==  'ok':
                logging.info( "%s-ok:%s", 'NoneAction' if action is None else action.text, productSku)
            else:
                errMsg = prod.find('Error').text
                GBL_ErrorMessages.append(errMsg)
                errorMessage = errMsg if errorMessage is None else  errorMessage + ' | ' + errMsg
                logging.error( "%s-%s ERR:%s", 'NoneAction' if action is None else action.text, productSku, '-' if errMsg is None else errMsg )
    return 'OK' if errorMessage is None else errorMessage

def getErrorTextProduct(action, xmlResp):
    if xmlResp == None:
        logging.debug("Null %s response?", action.upper())
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
                MU.UnasProductList[productSku].lastmod = MU.UtcNow()
                logging.info( "%s-ok:%s", 'NoneAction' if action is None else action.text, productSku)
            else:
                errMsg = prod.find('Error').text
                GBL_ErrorMessages.append(errMsg)
                errorMessage = errMsg if errorMessage is None else  errorMessage + ' | ' + errMsg
                logging.error( "%s-%s ERR:%s", 'NoneAction' if action is None else action.text, productSku, '-' if errMsg is None else errMsg )
    return 'OK' if errorMessage is None else errorMessage

def getErrorTextCustomer(act, xmlResp) -> str:
    if xmlResp == None:
        logging.debug("Null %s response?", act.upper())
    else:
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        errorMessage = None
        for cust in root.getchildren():
            # unasId = cust.find('Id').text
            email = cust.find('Email').text
            status = cust.find('Status').text
            action = None if cust.find('Action') is None else cust.find('Action').text 
            unasId = 0 if cust.find('Id') is None else int(cust.find('Id').text)
            if status.lower() ==  'ok':
                # find by ID
                # ucc = next((x for x in  MU.UnasCustomerList.values() if x.unasId == 176553135), None )
                ucc = next((x for x in  MU.UnasCustomerList.values() if x.unasId == unasId), None )
                if ucc:
                    ucc.lastmod = MU.UtcNow()
                    logging.info("%s-ok:%d lastMod:%i,%s",
                            'NoneAction' if action is None else action,
                            ucc.unasId,
                            ucc.lastmod,
                            MU.tsToDateStr(ucc.lastmod))
                else:
                    logging.info("%s-ok:%s ",'NoneAction' if action is None else action.text, email)
            else:
                errMsg = "[uid:%d, emil:%s, trIdL%d]::%s" % (unasId, email, MU.getTS(), cust.find('Error').text)
                GBL_ErrorMessages.append(errMsg)
                logging.error( "%s-ERR:%s", 'NoneAction' if action is None else action, xmlResp)
                errorMessage = errMsg if errorMessage is None else  errorMessage + ' | ' + errMsg
    return errorMessage # type: ignore


def postProcessUnasPostRequest(action, xmlResp) -> str:
    # valszeg adatbazisba kellene irni a visszajovo adatokat, vagy , hogyan a fenebe rendeljem ossze maskeppen az ID-ket?
    logging.info("UNAS-Set-postprocess: {0}, TS: {1}".format(action, MU.getTS()))
    logging.debug("UNAS-Set-response: {0}".format(xmlResp))
    if (action == 'product'):
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextProduct(action, xmlResp)
    elif action == 'inventory':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextProduct(action, xmlResp)
    elif action == 'price':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextProduct(action, xmlResp)
    elif action == 'billed':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextOrder(action, xmlResp)
    elif action == 'doc':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return 'OK'
    elif action == 'pic':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return 'OK'
    elif action == 'cat':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return 'OK'
    elif action == 'customer':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextCustomer(action, xmlResp)
    elif action == 'customerby':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextCustomer(action, xmlResp)
    elif action == 'pricerule':
        if xmlResp == None:
            logging.debug("Null pricerule response?")
        else:
            root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
            logging.debug(root.tag)
        return 'OK'
    elif action == 'offer':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return 'OK'  # Product type Response
    elif action == 'fulfilled':
        # root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        # logging.debug(root.tag)
        return 'OK'  # Pillnatnyilag SKIP all
    elif action == 'finalize':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return 'OK'
    elif action == 'synclog':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return 'OK'

    return 'OK'
    
#
# CACHE
#
MU.UnasSetProductsXmlPart = ''
MU.UnasSetCustomersXmlPart = ''
MU.UnasPriceSetPricesXmlPart = ''

def unasFreeXml(action, xmlTag):
    return UCH.unasFreeXml(action, xmlTag)

def unasFreeXmlData(action, xmlTag, xmlData):
    return UCH.unasFreeXmlData(action, xmlTag, xmlData)
    
def unasSymbolXml(action, xmlTag):
    xmlData = xmlTag
    resp = doUnasRequest(action, xmlData, 17)
    return 'OK' if resp is None else resp

def unasFinalize(postData): # ezt csak kezzel hivom:::  curl -d xmldata=lokakilo 192.168.10.6:3301/unas/
    FBU.dbClose()
    MU.UnasSetCustomersXmlPart = ''
    MU.UnasSetProductsXmlPart = ''
    #MU.UnasSetInventoryXmlPart = ''
    MU.UnasCustomerList.clear()
    MU.UnasProductList.clear()
    return "OK"

def unasPostFinalize(postData):
    response = unasBulkUpload()
    #
    if (len(postData) > 0 and postData == 'clearcache'):
        MU.UnasProductList.clear()
        MU.UnasCustomerList.clear()
    return "OK" if response is None else response

def unasBulkUpload():
    retXml = ''
    delayed = MU.UtcNow(0) - MU.LastActivity
    # logging.info("Bulk Upload DELAYED:%i", delayed)
    if delayed > 0:
        logging.debug("Bulk Upload starting")
        token = UnasAuth.doAuth()
        ts = MU.getCurrTime()
        if MU.UnasSetProductsXmlPart:
            logging.debug("Bulk Upload starting PRODUCTS")
            xmlResp = UCH.unasProduct_Direct(MU.UnasSetProductsXmlPart)
            response = postProcessUnasPostRequest( 'product', xmlResp)
            if response is None or 'OK' == response:
                response = ''

            retXml += response
            MU.UnasSetProductsXmlPart = ''
            logging.error("Bulk PRODUCT - response: %s", response)
            # And delete if marked
            # Using a list comprehension to make a list of the keys to be deleted
            # (keys having value in 3.)
            delete = [key for key in MU.UnasProductList if 'marked4delete' == MU.UnasProductList[key].state ]
            # delete the key/s
            for key in delete:
                del MU.UnasProductList[key]

        if MU.UnasSetCustomersXmlPart:
            logging.debug("Bulk Upload starting CUSTOMER")
            xmlResp = UCH.UploadCustomersXml(MU.UnasSetCustomersXmlPart)
            response = postProcessUnasPostRequest( 'customer', xmlResp) 
            if response is None or 'OK' == response:
                response = ''
            retXml += response
            logging.debug("Bulk CUSTOMER - response: %s", response)
            MU.UnasSetCustomersXmlPart = ''
            # And delete if markde
            delete = [key for key in MU.UnasCustomerList if 'marked4delete' == MU.UnasCustomerList[key].state ]
            for key in delete:
                del MU.UnasCustomerList[key]

        # elavult if MU.UnasSetInventoryXmlPart:
        # elavult     logging.error("Bulk Upload starting Inventory UNDER CONSTRUCTION ! Don`t use yet!")
        # elavult     xmlResp = UploadProductsXml(token, MU.UnasSetInventoryXmlPart)
        # elavult     retXml += postProcessUnasPostRequest( 'inventory', xmlResp, ts)
        # elavult     MU.UnasSetInventoryXmlPart = ''

        if len(retXml) > 0:
            logging.debug("Bulk upload result:")
            logging.debug(retXml)
            if MU.isLogLevelDebug():
                print(retXml)

    else:
        logging.warning("Bulk Upload skipped while active transaction")
    return  retXml if len(retXml) > 0 else "OK"
######################################################
#
#
#            #
#            # Cimek - hibajavitas:
#            if cust.find('SkipThisItem') is None:
#                if cust.invoicestreet is None:
#                    cust.invoicestreet = 'HIANYZO ADAT *'
#                elif cust.invoicestreet.text is not None and len(cust.invoicestreet.text) > 0:
#                    # cust.unasStreetName = 'HIANYZO ADAT **' if cust.invoicestreet.text.count(' ') < 1 else cust.invoicestreet.text.split(' ',1)[0]
#                    cust.unasStreetName = None # Nem tudom mar, miert csinaltam
#                else:
#                    # cust.unasStreetName = 'HIANYZO ADAT ***'
#                    cust.unasStreetName = None # Nem tudom mar, miert csinaltam
#                    cust.invoicestreet = 'HIANYZO ADAT ****'
#                #
#                # cust.unasStreetName = 'HIANYZO ADAT **' if cust.invoicestreet.text is None else cust.invoicestreet.text.split(' ',1)[0]
#                # cust.unasStreetType = 'út'
#                cust.unasStreetName = None # Nem tudom mar, miert csinaltam
#                cust.unasStreetType = None
#                
#                cust.unasCountryCode = MU.getCountryCode(cust.invoicecountry.text)
#                
#                ShippingAddress = None
#                looperFirst = 0
#                if len(cust.findall('customeraddresses')) > 0:
#                    for addr in cust.customeraddresses.getchildren():
#                        if addr.deleted == 0:
#                            #
#                            # ?kell ez? if addr.street is None:
#                            # ?kell ez?     addr.street = 'HIANYZO ADAT *'
#                            # ?kell ez? elif addr.street.text is not None and len(addr.street.text) > 0:
#                            # ?kell ez?     addr.unasStreetName = 'HIANYZO ADAT **' if addr.street.text.count(' ') < 1 else addr.street.text.split(' ',1)[0]
#                            # ?kell ez? else:
#                            # ?kell ez?     addr.unasStreetName = 'HIANYZO ADAT ***'
#                            # ?kell ez?     addr.street = 'HIANYZO ADAT ****'
#                            #
#                            addr.unasCountryCode = MU.getCountryCode(cust.invoicecountry if addr.country.text is None else addr.country.text)
#                            if addr.street.text is not None:
#                                # addr.unasStreetName = addr.street.text
#                                # addr.unasStreetType = 'út'
#                                pass
#                            addr.LooperFirst = looperFirst
#                            if looperFirst == 0:
#                                ShippingAddress = addr
#                            elif isAddressesSame(ShippingAddress, addr):
#                                addr.deleted = 1 ### Ezt is at kell gondolni
#                            #
#                            looperFirst += 1
#                if looperFirst > 0:
#                   cust.HasMoreAddress = 99
#