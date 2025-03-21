import logging
import requests
import datetime as date
import tempfile

import UnasAuth
import MyUtils as MU
from  MyUtilsTypes import UnasTransactionType as UTSTYPE
import FdbUtils as FBU
from UnasProductCache import UnasProductCache as UPC
import UnasCustomerCache as UCC
import UnasConnectHelper as UCH
import MySmtpClient as SM
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from lxml import objectify
import lxml as LXML 
import json

GBL_ErrorMessages = []

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

def unasOrder_Direct(xml, token):
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Orders>' + xml +'</Orders>'
    x = requests.post(MU.UNASAPI_URL + '/setOrder', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelDebug():
        print(x.status_code)
        print(x.text)
    return x.text

def unasCustomer_Direct(xml, token):
    xmlParam = '<?xml version="1.0" encoding="UTF-8" ?><Customers>' + xml +'</Customers>'
    x = requests.post(MU.UNASAPI_URL + '/setCustomer', data=xmlParam.encode('utf-8'), headers={ "Authorization" : "Bearer " + token })
    if MU.isLogLevelDebug():
        print(x.status_code)
        print(x.text)
    return x.text

def unasPricerule(xml, token):
    return '<pRicErUlez>Not Used Yet</pRicErUlez>'

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
                    _m = "Cust SKIPPED while possible cyclic-mod.\n ** uid:%i, sid:%i, code:%s, lastMod:%i TSdiff:%i" % (
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
                        if prod.webdisplay == 1:
                            prod.unasProductStatus = UPC.ProductStatus_ACTIVE
                #
                # GuaranteeMonths, Attributes, TargetCategory (symbolId, Gyarto, VTSZ, EAN)
                attribs = ''
                if prod.findall('productattributes') is not None:
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
                upc = None if not hasattr(prod,'productcode') else MU.UnasProductList.get(str(prod.productcode))
                if upc == None: # UNAS-bol hianyzik
                    logging.warning("Skipped - UNASban nem letezo termek CODE/Sku: " + str(prod.productcode))
                    print("Warning: SKIPPED-Modositasi kiserlet UNASban nem letezo termekre CODE/Sku: " + str(prod.productcode))
                    prod.SkipThisItem = '1'
                    # raise ValueError("Modositasi kiserlet UNASban nem letezo termekre CODE/Sku: " + prod.productcode)
                else:  # UNAS-ban azonositottam SKU alapjan es LIVE
                    prod.unasProductId = upc.unasId
                    prod.symbolIdIsNull = 1 if upc.symbolId == 0 else 0
                    prod.retValProduct = 0
                    isPriceFound = False
                    foundCat = -99999
                    for pi in prod.price:
                        prod.retValProduct = 1
                        if pi.pricecategory == MU.PRODUCT_PRICECAT_BASE and pi.priceCurrency == 'HUF':
                            isPriceFound = True
                            pi.retValValid = 2
                            pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                            foundCat = int(pi.pricecategory.text)
                        elif isPriceFound == False and pi.pricecategory == MU.PRODUCT_PRICECAT_FALLBACK and pi.priceCurrency == 'HUF':
                            foundCat = int(pi.pricecategory.text)
                            pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                        elif isPriceFound == False and pi.pricecategory == MU.PRODUCT_PRICECAT_FALLBACK2 and pi.priceCurrency == 'HUF':
                            foundCat = int(pi.pricecategory.text)
                            pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                        elif isPriceFound == False and foundCat < 0 and pi.priceCurrency == 'HUF':
                            foundCat = int(pi.pricecategory.text)
                            pi.calculatedGrossPrice = pi.value * ( 1.27 if upc.vat > 27 or upc.vat < 0 else (100 + upc.vat) / 100 )
                        else:
                            pass # pi.retValValid = 0
                        #
                    if foundCat > 0:
                        for pi in prod.price:
                            if foundCat == int(pi.pricecategory.text):
                                pi.retValValid = 4
                                foundCat = -1234567
                    elif not isPriceFound:
                        pi.retValValid = 0
                    else:
                        pass
            #else:
            #    logging.debug(f"Product skipped while webDisplay=0 Code:{prod.code}")
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
                prod.CurrentQuantity = str(int( prod.Quantity 
                                        - ( 0 if prod.find('StrictAllocate') is None else prod.StrictAllocate ) 
                                        - ( 0 if prod.find('NonStrictAllocate') is None else prod.NonStrictAllocate)
                                        ))
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
                    ucc = MU.getCustomerFormCache(cust.email, cust.taxnumber, cust.id )
                    if ucc is None:
                        ucc = next((x for x in  MU.UnasCustomerList.values() if x.code == cust.code), None )
                        logging.warning("PostCust:MISSING! Eml:%s - Ado:%s", cust.email, cust.taxnumber )
                    # Skipping ??
                    if ucc == None: # UNAS-bol hianyzik
                        if cust.deleted == 1 or cust.id == -2: # SKIP
                            logging.warning( "PtrfCust-Skipping DELETED nonexisting(UNAS) cust** sid:%i, code:%s", cust.id, cust.code )
                            ucc.state = MU.CACHESTATE_deleted # type: ignore
                            cust.unasCustomerAction = 'skip'
                            cust.SkipThisItem = '1' 
                        else: # NEW 
                            cust.unasCustomerAction = MU.UNASACTION_add
                            ucc = UCC.UnasCustomerCache(emil=cust.email, taxNo=cust.taxnumber, state='new' )
                            ucc.lastmod = 0
                            MU.putCustomerIntoCache(ucc, ucc.custAzon) # MU.UnasCustomerList[ucc.custAzon] = ucc
                        #
                    elif ucc.state == "unreg" or str(cust.code).startswith( MU.CUSTOMER_CODE_PREFIXES["unregistered"] ): # type: ignore # Unregistered, nem kell felvinni
                            cust.SkipThisItem = '1' 
                            logging.warning( "PtrfCust-Skipping Unregged cust** sid:%i, code:%s", cust.id, cust.code )
                    elif MU.UtcNow(ucc.lastmod) < MU.CUSTOMER_CYCLIC_INTERVAL: # Cyclic Update? skipping
                        cust.SkipThisItem = '1'
                        _m = "Cust(p) SKIPPED while possible cyclic-mod.**uid:%i, sid:%i, code:%s, lastMod:%i TSdiff:%i" % (
                                        ucc.unasId, ucc.symbolId, ucc.code, ucc.lastmod, MU.UtcNow(ucc.lastmod)) 
                        SM.sendAlertMail(_m)
                        logging.warning(_m)
                    else: # UNAS-ban azonositottam SKU alapjan es LIVE
                        # logging.warning( "POST-trfCust:%s ", ucc.toStr())
                        cust.unasCustomerId = ucc.unasId
                        if  cust.deleted == 1:             # 'live' == ucc.state and
                            logging.info( f"PostCust-DELETE** sid:{ucc.symbolId}, code:{ucc.code}, lastMod:{ucc.lastmod}")
                            cust.unasCustomerAction = 'delete'
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
                logging.error(f"Customer tag: {ET.tostring(cust)}" )
                print( f"Posting wo UCC:{cust.code}" if ucc is None else f"Posting custUCC:{ucc.toStr()}" )
    elif xsltFilename == 'CustomerX':
        for cust in root.getchildren():
            if cust.id > 0:
                try:
                    # ucc = MU.UnasCustomerList.get( UCC.buildAzonData( cust.email, cust.taxnumber ))
                    ucc = MU.getCustomerFormCache(cust.email, cust.taxnumber, cust.id )
                    postDiffTime = MU.getCurrTime()
                    if ucc:
                        postDiffTime -= ucc.lastmod
                        logging.error("PtrfCust:%s, LM:%i:%s diff:%i %s", ucc.custAzon, ucc.lastmod, MU.tsToDateStr(ucc.lastmod),
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
                            MU.putCustomerIntoCache(ucc, ucc.custAzon) # MU.UnasCustomerList[ucc.custAzon] = ucc
                    #elif ucc.symbolId > 0 and MU.UtcNow(MU.GETCUSTOMER_INTERVAL * 2 + 1) < ucc.lastmod: # Perhaps cyclic mod
                    elif postDiffTime < MU.CUSTOMER_CYCLIC_INTERVAL:
                        cust.SkipThisItem = '1'
                        logging.warning( "Cust(p) SKIPPED while possible cyclic-mod.**uid:%i, sid:%i, code:%s, lastMod:%i TSdiff:%i",
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
                            cust.unasCustomerAction = 'delete'
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
                        cust.unasCountryCode = MU.getCountryCode(cust.invoicecountry.text)
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
                                        addr.unasCountryCode = MU.getCountryCode(cust.invoicecountry if addr.country.text is None else addr.country.text)
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
                            cust.shippingaddress.unasCountryCode  = MU.getCountryCode(cust.invoicecountry)
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
                            cust.shippingaddress.unasCountryCode  = MU.getCountryCode(selectedOther4ShipAddr.country)
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
    cust.unasCountryCode = MU.getCountryCode(cust.invoicecountry.text)
    # ShippingAddress = ET.SubElement(cust, "shippingaddress", nsmap=None, attrib=None)
    selectedOther4ShipAddr = None
    if len(cust.findall('customeraddresses')) > 0:
        for addr in cust.customeraddresses.getchildren():
            if addr.deleted == 1:
                addr.SkipThisItem = 1
            elif isEmptyCA(addr):
                addr.SkipThisItem = 1
            else:
                addr.unasCountryCode = MU.getCountryCode(cust.invoicecountry if addr.country.text is None else addr.country.text)
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
        shippin.unasCountryCode  = MU.getCountryCode(cust.invoicecountry)
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
        shippin.unasCountryCode  = MU.getCountryCode(selectedOther4ShipAddr.country)
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

def prepareUnasReply(xmlReq, xsltFilename, ts):
    xmlEnc='utf-8'
    if xmlReq[30:36] == 'utf-16':
        xmlEnc='utf-16'
    #
    xml = bytes(bytearray(xmlReq, encoding=xmlEnc))
    try:
        xmlObj = objectify.fromstring(xml,None)
        preparedXml = transformUnasRequestObject(xmlObj, xsltFilename)
    except ET.XMLSyntaxError as e:
        logging.debug(e.msg)
        logging.debug(xml)
        logging.debug(xml.decode())
        raise  ValueError('XML Err:' + e.msg)

    if (preparedXml == None):
        return None

    # read xslt file
    xcv_0 = open('xslt/unas/set'+ xsltFilename + '.xslt').read()
    xcv = prepareXslt(xsltFilename, xmlReq, xcv_0)
    transform = ET.XSLT(ET.XML( bytes(xcv, 'utf-8'), None))
    # transform xml with xslt
    dom = ET.fromstring(preparedXml, None)
    newdom = transform( dom )

    if xsltFilename == 'ProductPrice':
        new_fileDescriptor, filename = tempfile.mkstemp()
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
            outfile = open("xmlfiles/set"+ xsltFilename + ".unas." + str(ts) + ".xml", 'a')
            outfile.write(outStr)
            return outStr.replace('<?xml version="1.0"?>','')
    return None

def prepareUnasReply_TEST(xmlReq, xsltFilename, ts):
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
        raise  ValueError('XML Err:' + e.msg)

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
        outfile = open("xmlfiles/set"+ xsltFilename + ".unas." + str(ts) + ".xml", 'a')
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
    elif action == 'billed':
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
        raise ValueError('Unknown action:' + action)
    #
    outfileReq = open("xmlfiles/post-"+ action +".req." + str(ts) + ".xml", 'a')
    outfileReq.write(xml)
    #
    return xml

# @request Processor
def doUnasRequest(action, postData, pathParam3 = None, errors = []):
    # reInit errors holder
    GBL_ErrorMessages.clear()
    # print(postData)
    token = UnasAuth.doAuth() # '7526191af38b98c0ce0334b0325a6be92adb7df3'
    ts = MU.getCurrTime()
    GBL_ErrorMessages.append("Test POST errMsg:%d" % ts)
    logging.info("unasPost-path:%s", action)
    logging.debug("token:%s, xml:%s", token, postData)
    MU.checkCacheState()
    unasResp ='OK'
    if (action == 'product'):
        unasResp = "???"
        uts = MU.createTransactionId( UTSTYPE.PRODUCT )
        logging.debug("setProduct-TS:%d" % uts)
        if MU.isLogLevelDebug():
            print(postData)
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        xmlReq = prepareUnasReply(xmlReq, "Product", ts )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            if (not MU.PRODUCT_BULK) or (pathParam3 == 'direct'):
                xmlResp = UCH.unasProduct_Direct(xmlReq)
                unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
            else:
                MU.UnasSetProductsXmlPart += xmlReq.replace('<?xml version="1.0"?>', '')
                MU.LastActivity = MU.UtcNow(0)
        # return "OK"
    elif action == 'inventory':
        uts = MU.createTransactionId( UTSTYPE.INVENTORY )
        logging.debug("setInventory-TS:%d" % uts)
        unasResp = "???"
        xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
        xmlReq = prepareUnasReply(xmlReq_0, "ProductQuantity", ts )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            #xmlResp = unasProduct( xmlReq, token ) # Ez valojaban Product modositas az UNASban
            #postProcessUnasPostRequest(action, xmlResp, ts)
            if (not MU.PRODUCT_BULK) or (pathParam3 == 'direct'):
                xmlResp = UCH.unasProduct_Direct(xmlReq)
                unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
            else:
                MU.UnasSetProductsXmlPart += xmlReq.replace('<?xml version="1.0"?>', '')
                MU.LastActivity = MU.UtcNow(0)
        # return "OK"
    elif action == 'price':
        uts = MU.createTransactionId( UTSTYPE.PRICE )
        logging.debug("setPrice-TS:%d" % uts)
        unasResp = "???"
        #
        xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
        xmlReq = prepareUnasReply(xmlReq_0, "ProductPrice", ts )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            # xmlReq = xmlReq.replace('<?xml version="1.0"?>', '')            
            if (not MU.PRODUCT_BULK) or (pathParam3 == 'direct'):
                xmlResp = UCH.unasProduct_Direct(xmlReq)
                unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
            else:
                MU.UnasSetProductsXmlPart += xmlReq.replace('<?xml version="1.0"?>', '')
                MU.LastActivity = MU.UtcNow(0)
        # return "OK"
    elif action == 'doc':
        uts = MU.createTransactionId( UTSTYPE.DOC )
        logging.debug("setDocuments-TS:%d" % uts)

        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        # ????? preProcessUnasPostRequest ??? transformResponse(xmlResp, 'Document')
        xmlResp = unasDocuments( xmlReq, token )
        unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
        # return "OK"
    elif action == 'pic':
        uts = MU.createTransactionId( UTSTYPE.PIC )
        logging.debug("setPictures-TS:%d" % uts)

        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        xmlResp = unasPics( xmlReq, token )
        #  ????? preProcessUnasPostRequest ??? transformResponse(xmlResp, 'Picture')
        unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
        # return "OK"
    elif action == 'cat':
        uts = MU.createTransactionId( UTSTYPE.CAT )
        logging.debug("setCategory-TS:%d" % uts)

        xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
        # Egyelore nincs megvalositva
        # xmlReq = prepareUnasReply(xmlReq_0, "Category", ts )
        # xmlResp = unasCats( xmlReq, token )
        # unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
        unasResp = "OK"
    elif action == 'customer':
        unasResp = "???"
        uts = MU.createTransactionId( UTSTYPE.CUSTOMER )
        logging.debug("setCustomer-TS:%d" % uts)

        postData = postData.replace('&amp;#', '&#')
        xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
        xmlReq = prepareUnasReply(xmlReq_0, "Customer", ts)
        if len('' if xmlReq is None else xmlReq) > 0:
            # xmlReq = xmlReq.replace('<?xml version="1.0"?>', '')            
            if (not MU.CUSTOMER_BULK) or (pathParam3 == 'direct'):
                xmlResp = unasCustomer_Direct(xmlReq, token)
                unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
            else:
                MU.UnasSetCustomersXmlPart += xmlReq # type: ignore
                logging.debug("LEN xml:%i, tot:%s", len( xmlReq ), len( MU.UnasSetCustomersXmlPart )) # type: ignore
                MU.LastActivity = MU.UtcNow(0)
        # return "OK"
    elif action == 'pricerule':
        uts = MU.createTransactionId( UTSTYPE.PRICERULE )
        logging.debug("Pricerule-TS:%d" % uts)

        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        xmlResp = '<PriRulz>'
        xml = prepareUnasReply(xmlReq, "PriceruleMethod", ts )
        if xml is not None:
            xmlResp += unasPricerule(xml, token)
            # meg hozzadadoik ... !!! unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
        xml = prepareUnasReply(xmlReq, "PriceruleDiscountCustomer", ts )
        if xml is not None:
            xmlResp += unasPricerule(xml, token)
            # meg hozzadadoik ... !!! unasResp += "\n" + postProcessUnasPostRequest(action, xmlResp, ts)
        xml = prepareUnasReply(xmlReq, "PriceruleDiscountProdCategory", ts )
        if xml is not None:
            xmlResp += unasPricerule(xml, token)
            # meg hozzadodik ... !!! unasResp += "\n" + postProcessUnasPostRequest(action, xmlResp, ts)
        xml = prepareUnasReply(xmlReq, "PriceruleDiscountVoucher", ts )
        if xml is not None:
            xmlResp += unasPricerule(xml, token)
            # meg hozzadadoik ... !!! unasResp += "\n" + postProcessUnasPostRequest(action, xmlResp, ts)
        xmlResp = xmlResp + '</PriRulz>'
        unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
        #return "OK"
    elif action == 'billed':
        uts = MU.createTransactionId( UTSTYPE.BILLED )
        logging.debug("Order - szamlazva-TS:%d" % uts)
        if MU.isLogLevelDebug():
            print(postData)
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        xmlReq = prepareUnasReply(xmlReq, "BilledOrder", ts )
        # Ha nem csinaltam UNAS requestet vmilyen feltetel teljesulese miatt!
        if xmlReq != None:            # Lehet NEM OK-val kellene visszaterni?
            xmlResp = unasOrder_Direct(xmlReq, token)
            unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
        # return "OK"
    elif action == 'bulkupload':
        uts = MU.createTransactionId( UTSTYPE.BLKUPLOAD )
        logging.debug("Bulk Upload-TS:%d" % uts)
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        xmlResp = unasBulkUpload()
        #  ????? preProcessUnasPostRequest ???  transformResponse(xmlResp, 'Finalize')
        unasResp = postProcessUnasPostRequest(action, xmlResp, ts)
        #return "OK"
    elif action.startswith('returnOK'):
        uts = MU.createTransactionId( UTSTYPE.RETURNOK )
        logging.debug("returnOK-TS:%d" % uts)
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        logging.debug(xmlReq)
        unasResp = "OK"
    elif action.startswith('synclog'):
        # logging.error("synclog NOT IMPLEMENTED")
        xmlReq = preProcessUnasPostRequest(action, postData, ts)
        uts = MU.createTransactionId( UTSTYPE.SYNCLOG )
        logging.debug("syncLog-TS:%d" % uts)
        logging.debug(xmlReq)
        # print(xmlReq)
        unasResp = ''
    elif action =='proxycontrol':
        uts = MU.createTransactionId( UTSTYPE.PROXYCONTROL )
        logging.debug("setProduct-TS:%d" % uts)
        return doProxyControl(pathParam3, postData )
    elif action.startswith('TEST'):
        uts = MU.createTransactionId( UTSTYPE.TESTPOST )
        logging.debug("setProduct-TS:%d" % uts)
        return doJoetest(pathParam3, postData, ts )

    logging.info("PostReq:%s handled in:%i" , action, MU.getCurrTime() - ts)
    if len(GBL_ErrorMessages) > 0:
        for errItm in GBL_ErrorMessages:
            errors.append(errItm)
    return unasResp

def doProxyControl(postData, pPath = []):
    ts = MU.UtcNow()
    postData = postData.replace('&amp;#', '&#')
    #xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
    #
    xmlReq = None
    if len(pPath) > 1:
        action = pPath[1]
        if 'unasDirectAction' == pPath[0]:
            xmlReq = prepareUnasReply(postData, action, ts)
            return 'OK' if xmlReq is None or len(xmlReq) < 1 else UCH.unasDirectXml(pPath[1], xmlReq, None if len(pPath) < 3 else pPath[2])
        elif 'customer' == pPath[0]:
            if 'create199' == pPath[1]:
                jsObj = json.loads(postData)
                xml = jsObj["customerXml"] # next(iter(jsObj.values()))
                xmlReq = prepareUnasReply(xml, 'Customer', ts)
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
            xmlReq = prepareUnasReply(postData, action, ts)
        #
        parser = ET.XMLParser(remove_blank_text=True )
        element = ET.XML(xmlReq, parser)   # LXML.etree.ElementTree.XML(xmlResp, parser=None, encoding='unicode')
        # ET.indent(element,space=4)
        xmlReq = ET.tostring(element, encoding='unicode', pretty_print=True, method='xml') # type: ignore
        return xmlReq
    else:
        logging.error("Bad POST-ProxyControl request: %s" % " , ".join(pPath))
        return None

    
def doJoetest(action, postData, ts):
    postData = postData.replace('&amp;#', '&#')
    xmlReq_0 = preProcessUnasPostRequest(action, postData, ts)
    xmlReq = prepareUnasReply(xmlReq_0, "Customer", ts)
    return xmlReq
    #return 'TestPOSTresp:%s, %s, %s' % path % str(FBU.getProductNames('HF716544'))
#
# Egyelore csak logol,
# de itt lehet az ID-ket visszairni a symbolba (xmlResp-ban benne van)
def getErrorTextOrder(action, xmlResp, ts, pathParam3 = None):
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

def getErrorTextProduct(action, xmlResp, ts, pathParam3 = None):
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
                MU.UnasProductList[productSku].lastmod = ts # MU.UtcNow()
                logging.info( "%s-ok:%s", 'NoneAction' if action is None else action.text, productSku)
            else:
                errMsg = prod.find('Error').text
                GBL_ErrorMessages.append(errMsg)
                errorMessage = errMsg if errorMessage is None else  errorMessage + ' | ' + errMsg
                logging.error( "%s-%s ERR:%s", 'NoneAction' if action is None else action.text, productSku, '-' if errMsg is None else errMsg )
    return 'OK' if errorMessage is None else errorMessage

def getErrorTextCustomer(act, xmlResp, ts) -> str:
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
                    ucc.lastmod = ts # MU.UtcNow()
                    logging.info("%s-ok:%s lastMod:%i,%s",
                            'NoneAction' if action is None else action,
                            ucc.custAzon,
                            ucc.lastmod,
                            MU.tsToDateStr(ucc.lastmod))
                else:
                    logging.info("%s-ok:%s ",'NoneAction' if action is None else action.text, email)
            else:
                errMsg = "[uid:%d, emil:%s, trIdL%d]::%s" % (unasId, email, ts, cust.find('Error').text)
                GBL_ErrorMessages.append(errMsg)
                logging.error( "%s-ERR:%s", 'NoneAction' if action is None else action, xmlResp)
                errorMessage = errMsg if errorMessage is None else  errorMessage + ' | ' + errMsg
    return errorMessage # type: ignore


def postProcessUnasPostRequest(action, xmlResp, ts) -> str:
    # valszeg adatbazisba kellene irni a visszajovo adatokat, vagy , hogyan a fenebe rendeljem ossze maskeppen az ID-ket?
    logging.info("UNAS-Set-postprocess: {0}, TS: {1}".format(action, ts))
    logging.debug("UNAS-Set-response: {0}".format(xmlResp))
    if (action == 'product'):
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextProduct(action, xmlResp, ts)
    elif action == 'inventory':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextProduct(action, xmlResp, ts)
    elif action == 'price':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextProduct(action, xmlResp, ts)
    elif action == 'billed':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextOrder(action, xmlResp, ts)
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
        return getErrorTextCustomer(action, xmlResp, ts)
    elif action == 'customerby':
        root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
        logging.debug(root.tag)
        return getErrorTextCustomer(action, xmlResp, ts)
    elif action == 'pricerule':
        if xmlResp == None:
            logging.debug("Null pricerule response?")
        else:
            root=ET.fromstring(bytes(xmlResp, 'utf-8'), None)
            logging.debug(root.tag)
        return 'OK'
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
            response = postProcessUnasPostRequest( 'product', xmlResp, ts)
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
            response = postProcessUnasPostRequest( 'customer', xmlResp, ts) 
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