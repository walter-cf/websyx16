import json

# import mysql as mySQL
import mysql.connector

import MyUtils as MU
from MyUtilsTypes import AlertMailType, AlertMailTypeEncoder


class MySqlWrapper():
    MyDB = None
    RowCount = 0
    
    def __init__(self):
        # self.MyDB = self.connect()
        self.RowCount = 0
    
    def rowCount(self) -> int:
        return self.RowCount
    
    def getConn(self, force=False):
        if force or self.MyDB is None:
            self.MyDB = self.connect()
        return self.MyDB
    
    def close(self):
        self.getConn().close() # type: ignore
    
    def commit(self):
        if self.MyDB:
            self.MyDB.commit()

    def rollback(self):
        if self.MyDB:
            self.MyDB.rollback()
    
    def connect(self):
        self.MyDB = mysql.connector.connect(
                host     = MU.MYSQL_HOST,
                user     = MU.MYSQL_USER,
                password = MU.MYSQL_PASSWORD,
                database = MU.MYSQL_DB,
                auth_plugin='mysql_native_password'
        )
        return self.MyDB
    
    def getCursor(self):
        try:
            if self.MyDB is None:
                self.MyDB = self.getConn(True)
            return self.MyDB.cursor(buffered=True, dictionary=True)
        except mysql.connector.errors.OperationalError:
            self.MyDB = self.getConn(True)
            return self.MyDB.cursor(buffered=True, dictionary=True)

    def doSql(self, sql, params = () ):
        crsr = self.getCursor()
        crsr.execute(sql, params)
        result = crsr.fetchall()
        self.RowCount = crsr.rowcount
        return result
    
    def getRow(self, sql, param = ()):
        crsr = self.getCursor()
        crsr.execute(sql, param)
        resultRow = crsr.fetchone()
        return resultRow
    
    def doSqlList(self):
        pass
    
    def execSql(self, sql:str, params, commit = False):
        crsr = self.getCursor()
        if params is None:
            crsr.execute(sql)
        elif "<class 'tuple'>" == str(type (params)):
            crsr.execute(sql, params)
        elif "<class 'list'>" == str(type (params)):
            crsr.execute(sql, params)
        else:
            crsr.execute(sql, [params])
        if commit:
            self.commit()
        return crsr.lastrowid # type: ignore
    
    def insSqlTest(self, commit = False) -> int:
        sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
        val = ("John", "Highway 21")
        crsr = self.getCursor()
        crsr.execute(sql, val)
        if commit:
            self.commit()
        return self.getCursor().lastrowid() # type: ignore
    
    def handleError_NU(self, msgStr, action, uts, ):
        pass # write error
    
    def writeError(self, shortTxt, errTxt,  typ:AlertMailType, trId:int=0, ):
        errSql = "INSERT INTO errors (objTyp, shorttext, errortext, alerttype, transactionId, created) values( %s,%s,%s,%s,%s, now())"
        objTyp = 'other' # TODO alertmailtypebol kepzem majd, ha lesz!
        self.execSql(errSql, ( objTyp, shortTxt, errTxt, json.dumps(typ,cls=AlertMailTypeEncoder), trId ), commit=True)

    def getLastErrors(self, cnt:int = 10, startFrom:int=0):
        startFromString = '' if startFrom==0 else '%d,' % startFrom
        sql = f"select * from errors order by created desc  LIMIT {startFromString} {cnt}"
        return  self.doSql(sql )

"""
def dbClose(con = None):
    global CON
    con = CON if con is None else con
    if con is not None and not con._Connection__get_closed(): # type: ignore
        con.rollback()
        con.close()
    CON = None

def Connect(dbFileName, dbRoot, fbUser, fbPass, fbHost):
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

def doSql( sql, param = None ):
    cur = getFbCursor()
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
        raise WalueError(err)
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

def execSql(sql:str,  param = None ):
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
    CON.commit()  # type: ignore /// a getCursor beallitotta, ha nulla volt a con!!! LOGIKATLAN es CSUNYA!!!


def prepStatement(sql, cur):
    return cur.prep(sql)
"""
