#!/bin/python3

import logging
import sys
from typing import Dict, List

import fdb  # type: ignore

import MyUtils as MU
from MyUtilsTypes import (AlertMailType, MyProgramFlowErrorException,
                          ProxyErrCode, UnasTransactionType)

global CON
CON = None

def dbClose(con = None):
    global CON
    con = CON if con is None else con
    if con is not None and not con._Connection__get_closed(): # type: ignore
        try:
            con.rollback()
        except fdb.DatabaseError as e:
            pass        
        if not con._Connection__get_closed(): # type: ignore
            try:
                con.close()
            except fdb.DatabaseError as e:
                pass
        #
    con = None
    CON = None

def fbConnect(dbFileName, dbRoot, fbUser, fbPass, fbHost):
    global CON
    if (CON is not None ):
        dbClose(CON)  # type: ignore
    dbPath = '%s/%s' % (dbRoot, dbFileName)
    CON =  fdb.connect(host=fbHost, database=dbPath, user=fbUser, password=fbPass)
    return CON

def getFbConn(dbFileName = None):
    dbFn = MU.valDef( dbFileName, MU.FB_DBDATA_DEFAULT)
    return fbConnect(dbFn, dbRoot=MU.FB_DBDATA_ROOT, fbUser=MU.FB_USER, fbPass=MU.FB_PASSWORD, fbHost = MU.FB_HOST)

def getFbCursor(con = None):
    global CON
    con = CON if con is None else con
    if con is None:
        con = getFbConn()
        CON=con
    return con.cursor() # type: ignore

def doSqlList( sql, params = () ):
    cur = getFbCursor()
    if len(params) > 0:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    return cur

def doSql( sql, param = None, cursor = None ):
    cur = getFbCursor() if cursor is None else cursor
    try:
        # comment: 
        # end try
        if param is None:
            cur.execute(sql)
        elif "<class 'tuple'>" == str(type (param)):
            cur.execute(sql, param)
        elif "<class 'list'>" == str(type (param)):
            cur.execute(sql, param)
        else:
            cur.execute(sql, [param])
    except Exception as e:
        err = f"DB-Err; sql:{sql},\r\nprms:{param}\r\nX:{e}"
        MU.errorHandler(err, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E19), level = logging.ERROR, eDescr=sys.exc_info())
        raise MyProgramFlowErrorException(err)
    return cur

def insSql(table:str, colList:str='', valuePart:str = '',  param = None ) -> int:
    sql = 'INSERT INTO "' + table + '" ( "Id", ' + colList +  ') VALUES (0+NEXT VALUE FOR "Gen' + table + '", ' +  valuePart  + ' ) RETURNING "Id"'
    cur = getFbCursor()
    if param is None:
        cur.execute(sql)
    elif "<class 'tuple'>" == str(type (param)):
        cur.execute(sql, param)
    elif "<class 'list'>" == str(type (param)):
        cur.execute(sql, param)
    else:
        cur.execute(sql, [param])
    #
    newId = cur.fetchone()
    CON.commit()  # type: ignore /// a getCursor beallitotta, ha nulla volt a con!!! LOGIKATLAN es CSUNYA!!!
    return newId[0] if len(newId) > 0 else 0

def execSql(sql:str,  param = None, comitted=False ):
    # sql = 'INSERT INTO "' + table + '" ( "Id", ' + colList +  ') VALUES (0+NEXT VALUE FOR "Gen' + table + '", ' +  valuePart  + ' ) RETURNING "Id"'
    cur = getFbCursor()
    if param is None:
        cur.execute(sql)
    elif "<class 'tuple'>" == str(type (param)):
        cur.execute(sql, param)
    elif "<class 'list'>" == str(type (param)):
        cur.execute(sql, param)
    else:
        cur.execute(sql, [param])
    #
    if comitted:
        CON.commit()  # type: ignore /// a getCursor beallitotta, ha nulla volt a con!!! LOGIKATLAN es CSUNYA!!!


def prepStatement(sql, cur):
    return cur.prep(sql)

def execSql_OLD( sql, paramList = (), con = CON ):
    cur = getFbCursor(con)
    stmt = cur.prep(sql)
    cur.executemany(stmt, paramList)
    con.commit() # type: ignore
    return cur

def getField( sql, param = None, cursor = None ):
    row = getRow( sql, param , cursor )
    return None if not row else row[0]

def getRow( sql, param = None, cursor = None ):
    cur = getFbCursor() if cursor is None else cursor
    try:
        # comment: 
        # end try
        if param is None:
            cur.execute(sql)
        elif "<class 'tuple'>" == str(type (param)):
            cur.execute(sql, param)
        elif "<class 'list'>" == str(type (param)):
            cur.execute(sql, param)
        else:
            cur.execute(sql, [param])
        return cur.fetchone()
    except Exception as e:
        err = f"DB-Err; sql:{sql},\r\nprms:{param}\r\nX:{e}"
        MU.errorHandler(err, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.E19), level = logging.ERROR, eDescr=sys.exc_info())
        raise MyProgramFlowErrorException(err)

#####################################################
# Specials
#####################################################

def getPriceBySku(sku:str):
    sql = f'''select "Price" from "ProductPrice" 
                join "Product" on "Product"."Id"="ProductPrice"."Product"  where "Product"."Code"=? and "PriceCategory"=-1 and "Currency"=-1
                order by "ProductPrice"."Id" desc'''
    return getField(sql, sku)


def getPaymentMethodByCustomer( customerId ) :
    sql = f'select "Name" from "PaymentMethod" where "Id"  in (select "PaymentMethod" from "Customer" where "Id" = {customerId})'
    res = doSql( sql )
    return res.fetchone()[0]
    
def getModifiedOrders(sqlCols, interval, unasOrdType):
    cols = '","'.join(sqlCols)
    sql = f"""select "{cols}" from "CustomerOrder"
                where "RowModify" > ( select dateadd (second, ?, cast(\'now\' as timestamp))  from rdb$database)
                and "VoucherSequence" = ?
        """
    res = doSql(sql, (-1*interval, unasOrdType) )
    rex = []    
    for _R in res.fetchall():
        rex.append(_R)
    return rex

    # dbLen = result.fetchone()[0]
    # if ( dbLen > cntAddr):
    #     doSql( 'delete from "CustomerAddress" where "Customer" = %i order by "Id" DESC rows %i' % (custId, dbLen - cntAddr) )
    # elif (dbLen < cntAddr):
    #     for i in range(cntAddr - dbLen ):
    #         res = addCustAddr(custId, unasId, dbLen  + i + 1 )
    #         if MU.isLogLevelDebug():
    #           print("ID:%i" % res)
    
def correctCustAddreRecordCount(custId, unasId, cntAddr):
    result = doSql('select count(*) from "CustomerAddress" where "Customer" = ? ', custId)
    dbLen = result.fetchone()[0]
    if ( dbLen > cntAddr):
        doSql( 'delete from "CustomerAddress" where "Customer" = %i order by "Id" DESC rows %i' % (custId, dbLen - cntAddr) )
    elif (dbLen < cntAddr):
        for i in range(cntAddr - dbLen ):
            res = addCustAddr(custId, unasId, dbLen  + i + 1 )
            if MU.isLogLevelDebug():
              print("ID:%i" % res)
    pass # es Most ???

def addCust(unasId, custCode):
    custName = custCode
    try:
        result = insSql('Customer', ' "Code", "Name" ', ' ?, ? ', (  custCode, custName ))
        return result
    except Exception as e:
        MU.getLogger().logError("DatabaseError :%s", e.args)
        print(e.args)
        return -1 

def addCustAddr(custSymbolId, unasId, addressIdx,
                     name:str    = None, # type: ignore
                     city:str    = None, # type: ignore
                     zip:str     = None, # type: ignore
                     region:str  = None, # type: ignore
                     country:str = None, # type: ignore
                     street:str  = None, # type: ignore
                     house:str   = None # type: ignore
            ):
    custCode = MU.CUSTOMER_CODE_PREFIXES["patternAddr"] % (MU.CUSTOMER_CODE_PREFIXES["address"], unasId, addressIdx)
    result = insSql('CustomerAddress', '"Customer", "Code", "Name","City","Zip","Country","Region","Street","HouseNumber"',
                "%i , ?, ? , ? , ? , ? , ? , ? , ?" % custSymbolId, (custCode, name, city, zip, country, region, street, house ))
    return result; 

def addCustAddrDummy(custSymbolId, unasId, addressIdx,
                     name:str,
                     city:str    = None, # type: ignore
                     zip:str     = None, # type: ignore
                     region:str  = None, # type: ignore
                     country:str = None, # type: ignore
                     street:str  = None, # type: ignore
                     house:str   = None  # type: ignore
            ):
    custCode = MU.CUSTOMER_CODE_PREFIXES["patternAddr"] % (MU.CUSTOMER_CODE_PREFIXES["address"], unasId, addressIdx)
    result = insSql('CustomerAddress', '"Customer", "Code", "Name","City","Zip","Country","Region","Street","HouseNumber"',
                "%i , ?, ? , ? , ? , ? , ? , ? , ?" % custSymbolId, (custCode, name, city, zip, country, region, street, house ))
    return result; 

def getCustomerAddressesById( _sid:int ) -> List: # type: ignore
    return getCustomerAddresses('"Customer" = ? ', _sid )

def getCustomerAddressesByCode( _caCode: str ) -> List: # type: ignore
    return getCustomerAddresses('"Code" like ' + ("'%s%%'" % _caCode), None)

colListCA = ["Id", "Customer", "Code", "Name", "Country","Region","Zip", "City", "Street", "HouseNumber",
               "Deleted", "IsCompany", "Preferred", "RowVersion", "RowModify" ]

def getCustomerAddresses( sqlWhere, prm ) -> List: # type: ignore
    cols = '","'.join( map (str,colListCA))
    res = doSql( 'select "%s" from "CustomerAddress" where %s' % (cols, sqlWhere), prm)
    rex = []    
    for _R in res.fetchall():
        rex.append(_R)
    return rex

# # # def reassignCAs( cust : UnasCustomerCache ):
# # #     # nem tom, mit akarok
# # #     _caCode = cust.code
# # #     _sid = cust.symbolId
# # #     _al = cust.unasAddrObj
# # #     # 1 a -2 -es rex modositani kell a custId-t
# # #     result = execSql('update "CustomerAddress" set "Customer" = ? where "Customer" = -2 and "Code" like ' + "'%s%%'" % _caCode )
# # #     print(result)
# # #     rex = doSql('select "Id", "Code" from "CustomerAddress" where "Customer" = ? and "Code" like ' + "'%s%%'" % _caCode, _sid )
# # #     resppp = ''
# # #     for r in rex.fetchall():
# # #         print(r)
# # #         resppp += str(r)
# # #         rex = execSql('update "CustomerAddress" set "Customer" = ? where "')
# # #     return resppp

def reassignCA( id:int, newCustomerId:int ):
    cur = doSql('update "CustomerAddress" set "Customer" = ? where "Id" = ?', (newCustomerId, id ))
    CON.commit() # type: ignore
    cur.close()

def deleteCAbyId( id:int ):
    setDeletedAddrById(id, 1)

def undeleteCAbyId( id:int ):
    setDeletedAddrById(id, 0)
    
def setDeletedAddrById(id:int, deleted:int=1):
    cur = doSql('update "CustomerAddress" set "Deleted" = ? where "Id" = ? ', (deleted, id ))
    CON.commit() # type: ignore
    cur.close()
    
def delCustomerById(id : int, commit:bool = True, cur = None):
    if id > 0:
        cur = doSql('delete from "CustomerAddress" where "Customer" = ? ', (id, ), cursor = cur )
        cur = doSql('delete from "Customer" where "Id" = ? ', (id, ), cursor = cur )
    if commit and cur is not None:
        CON.commit() # type: ignore
        cur.close()
        return None
    else:
        return cur

def getOrdersByCustomerCode(code : str = "UCO%"):
    pass

def delOrdersCustomerCode(code : str = "UCO%"):
    pass

def delCustomerByUCO(code : str = "UCO%"):
    cur = doSql('delete from "CustomerAddress" where "Customer" in (select "Id" from "Customer" where "Code" LIKE ?)', (code, ) )
    cur = doSql('delete from "Customer" where "Code" LIKE ?', (code, ), cursor = cur )
    CON.commit() # type: ignore
    cur.close()

def delCustAddrById(id : int):
    cur = doSql('delete from "CustomerAddress" where "Id" = ? ', id )
    CON.commit() # type: ignore
    cur.close()

def deleteDummyCArex(unasId:int = 0, custId:int = -2):
    _caCode = MU.CUSTOMER_CODE_PREFIXES["patternAddr"] % ( MU.CUSTOMER_CODE_PREFIXES["address"],  unasId, 0)
    _caCode = _caCode[:-1] + '%'
    cur = doSql('delete from "CustomerAddress" where "Customer" = ? ' + ( '' if _caCode is None else ' and "Code" like ' + ("'%s'" % _caCode)), custId )
    CON.commit() # type: ignore
    cur.close()
    
def updateCustomerCode(symbolId, symbolCode):
    cur = doSql( 'update "Customer" set "Code" = ? where "Id" = ?', (symbolCode, symbolId ))
    CON.commit() # type: ignore
    cur.close()

def updateSymbolCode(symbolId, symbolCode, tableName, codeColumn = 'Code'):
    cur = doSql( 'update "%s" set "%s" = ? where "Id" = %i' % (tableName, codeColumn, symbolId), symbolCode)
    CON.commit() # type: ignore
    cur.close()

def updateSymbolCodeIfChanged(symbolId, symbolCode, tableName, codeColumn = 'Code'):
    cur = doSql( 'select "Code" from "Customer"  where "Id" = %i' % symbolId)
    symCode = cur.fetchone()
    if symCode is not None and symCode[0] != symbolCode:
        updateSymbolCode(symbolId, symbolCode, tableName, codeColumn)

def updateOrderStatus(symbolId, status:int = 1):
    cur = doSql( 'update "CustomerOrder" set "CustomerOrderStatus" = ? where "Id" = ?',  (status, symbolId ))
    CON.commit() # type: ignore
    cur.close()

def updateProductName(symbolId, prodName): # Name Varchar(100)
    cur = doSql( 'update "Product" set "Name" = ? where "Id" = ?', ( prodName[:100], symbolId ))
    CON.commit() # type: ignore
    cur.close()

# 
SELECT_ORDER_FROM_INVOICE = '''select FIRST 1 CO."VoucherNumber", CO."PrimeVoucherNumber" 
    from  "CustomerOrder" CO 
     JOIN "CustomerOrderDetail" COD on CO."Id" = COD."CustomerOrder" 
     JOIN "CustomerOrderFulfill" COF on COF."Target" = COD."Id" 
     JOIN "StockOutDetail" SOD ON SOD."Id" = COF."StockOutDetail"  
     JOIN "StockOut" SO on SO."Id" = SOD."StockOut" 
    where SO."VoucherNumber" = ?
'''

def getOrderIdByInvoice(szlaSzam):
    cur = doSql(SELECT_ORDER_FROM_INVOICE, szlaSzam)
    row = cur.fetchone()
    return row

def getProductSymbolId(sku):
    cur = doSql('select "Id" from "Product" where "Code" = ?', sku)
    row = cur.fetchone()
    return None if row is None else row[0]

def getProductNames(sku):
    cur = doSql('select "Name", "WebName"  from "Product" where "Code" = ?', sku)
    row = cur.fetchone()
    return (None, None) if row is None else (row[0], row[1])

def getCurrentDT():
    cur = doSql( "select current_timestamp from rdb$database" )
    row = cur.fetchone()
    return str(row[0])[0:19]

#def getOrdersByStatusCode(idList : List[int]) -> List:
def getOrdersOpened(ts : str = None) -> List: # type: ignore
    colsStr = '%s,%s,%s' % (
            '"Id","VoucherType","VoucherSequence","VoucherNumber","PrimeVoucherNumber","Customer","CustomerAddress"',
            '"VoucherDate","DeliveryFrom","DeliveryTo","CustomerOrderStatus","NetValue","GrossValue","VatValue"',
            '"RowVersion","RowCreate","RowModify"'
            )
    cols = colsStr.replace('"', '').split(',')
    cur = doSql('select %s from "CustomerOrder" where "Closed" = 0' % (
            colsStr, '' if ts is None else "\"RowVersion\" > '%s'" % MU.LastSetOrderDT if ts is None else ts ))
    resp = []
    for x in cur.fetchall():
        row: Dict = {}
        for colIdx in range(len(cols)):
            if cols[colIdx].startswith("Row") or cols[colIdx].startswith('Delivery') or cols[colIdx] == 'VoucherDate':
                row[ cols[colIdx] ] = str(x[colIdx])
            elif cols[colIdx].endswith('Value'):
                row[ cols[colIdx] ] = int(x[colIdx])
            else:
                row[ cols[colIdx] ] = x[colIdx] 
        resp.append(row)
    return resp
    
def getOrdersByStatusCode(idList : str) -> List:
    colsStr = '%s,%s,%s' % (
            '"Id","VoucherType","VoucherSequence","VoucherNumber","PrimeVoucherNumber","Customer","CustomerAddress"',
            '"VoucherDate","DeliveryFrom","DeliveryTo","CustomerOrderStatus","NetValue","GrossValue","VatValue"',
            '"RowVersion","RowCreate","RowModify"'
            )
    cols = colsStr.replace('"', '').split(',')
    if len(idList) < 1:
        return []
    cur = doSql('select %s from "CustomerOrder" where "CustomerOrderStatus" in (%s)' % ( colsStr, idList ))
    resp = []
    for x in cur.fetchall():
        row: Dict = {}
        for colIdx in range(len(cols)):
            if cols[colIdx].startswith("Row") or cols[colIdx].startswith('Delivery') or cols[colIdx] == 'VoucherDate':
                row[ cols[colIdx] ] = str(x[colIdx])
            elif cols[colIdx].endswith('Value'):
                row[ cols[colIdx] ] = int(x[colIdx])
            else:
                row[ cols[colIdx] ] = x[colIdx] 
        resp.append(row)
    return resp

def getPaymentMethodByCustomerId(custId:int):
    if custId < 1:
        return None

    sql = 'select PM."Name", PM."ToleranceDay" from "PaymentMethod" PM join "Customer" CU on PM."Id" = CU."PaymentMethod" and CU."Id" = ?'
    cur = doSql(sql,  (custId,) )
    row = cur.fetchone()
    return  ('Hiányzó fizetési mód', -99999) if row == None else row

def getPaymentMethodByCustomerCode(custCode:str):
    sql = 'select PM."Name", PM."ToleranceDay" from "PaymentMethod" PM join "Customer" CU on PM."Id" = CU."PaymentMethod" and CU."Code" like ?'
    cur = doSql(sql,  custCode )
    row = cur.fetchone()
    return None if row == None else row

def getOrderById(id:int):
    if id < 1:
        return None
    cur = doSql('select "Id", "Customer","PrimeVoucherNumber" from "CustomerOrder" where "Id" = ?', (id,) )
    row = cur.fetchone()
    return None if row == None else row
    
def getModTime( id, tableName = "Customer"):
    if id < 1:
        return None
    cur = doSql('select "RowModify" from "%s" where "Id" = ?' % tableName,(id ,))
    row = cur.fetchone()
    return None if row == None else row[0]

def createCustomerIfNotExists(id:int = -2, xmlCode:str = None, xmlEmail:str = None, xmlTaxno:str = None): # type: ignore
    cid = 0 if id is None else id
    cid = 0 if cid < 1 else id
    cur = doSql('select "Id" from "Customer" where "Id" = ? or "Code" = ?', (cid, 'xWqaS385qqQw' if xmlCode is None else xmlCode ))
    rex = cur.fetchone()
    if rex is None or len(rex) < 1:
        newCustomerId = insSql('Customer', ' "Code", "Name", "Email", "TaxNumber" ', ' ?, ?, ?, ? ', ( 
                            ('' if xmlCode is None else xmlCode, 'Missed from symbolDB',
                            '' if xmlEmail is None else xmlEmail,
                            '' if xmlTaxno is None else xmlTaxno  ))
                            )
        return newCustomerId
    else:
        return rex[0]


def insertDummyCustomer():
    cur = doSql('select "Id" from "Customer" where "Id" = -2')
    rex = cur.fetchone()
    if rex is None or len(rex) < 1:
        cur = doSql('insert into "Customer" ("Id", "Code", "Name") values(-2, ?, ? )', ("UCU-Dummy-rek", "Dummy rex"))
        CON.commit() # type: ignore

def testDbConnect():
    cur = doSql( 'select count(*) from "Customer"')
    row = cur.fetchone()
    return row[0]

########################################
# Kell ez ? 20260901
########################################
def getCustomerById(id:int):
    return getRow('select * from "Customer" where "Id" = ?', (id,))

def getCustomerNameById(id:int):
    return getField('select "Name" from "Customer" where "Id" = ?', (id,))
