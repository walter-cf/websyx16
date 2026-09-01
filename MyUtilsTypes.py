import json
import typing
from enum import IntEnum
from typing import Dict

import MyUtils as MU


class ProxyErrCode(IntEnum):
    UNKNOWN = 0
    INFO = 1
    KET = 2
    HAA = 3
    E04 = 4
    E05 = 5
    E06 = 6
    E07 = 7
    E08 = 8
    E09 = 9
    E10 = 10
    E11 = 11
    E12 = 12
    E13 = 13
    E14 = 14
    E15 = 15
    E16 = 16
    E17 = 17
    E18 = 18
    E19 = 19
    E20 = 20
    E21 = 21
    E22 = 22
    E23 = 23
    B24 = 24
    B25 = 25
    B26 = 26
    B27 = 27
    B28 = 28  # UnasAuth Login result HTML page - Api not available
    B29 = 29
    B30 = 30
    B31 = 31
    B32 = 32
    B33 = 33
    B34 = 34
    B35 = 35
    B36 = 36
    B37 = 37
    B38 = 38
    B39 = 39
    E40 = 40
    E41 = 41
    E42 = 42 # masterChallengeUnas -> Nout USED !!!
    F50 = 50 # PepitaCache missed item

class UnasTransactionType(IntEnum):
    CREATENEW   = 0
    STARTPROXY  = 1
    STARTBATCH  = 2
    LOGIN = 5
    ORDERS = 11
    ORDERBY = 12
    PRODUCTS = 13
    PRODBY = 14
    UNASPROD = 15
    INQUIRERS = 16
    CUSTOMERS = 17
    CUSTOMERORDER = 18
    UNASCUST = 19
    CUSTOMERBY = 20
    STORAGE = 21
    LOGGER = 22
    INITCACHE = 23
    PROXYCONTROLS = 24
    TESTGET = 25
    TESTJOE = 26
    ORDERSTATUS = 27
    LOGROTATE = 28
    XMLROTATE = 29
    #
    # Post
    PRODUCT = 41
    INVENTORY = 42
    PRICE = 43
    DOC = 44
    PIC = 45
    CAT = 46
    CUSTOMER = 47
    PRICERULE = 48
    BILLED = 49
    BLKUPLOAD = 50
    RETURNOK = 51
    SYNCLOG = 52
    PROXYCONTROL = 53
    TESTPOST = 54
    OFFER = 55
    PEPITA_ORDER = 56
    #
    UNAS_COMM_ERROR = 60
    UNAS_LOGIN_ERROR = 61
    #
    UNKNOWN_MAX = 99

class LogLvl(IntEnum):
    ERROR   = 1
    WARNING = 2
    INFO    = 3
    DEBUG   = 4
    TRACE   = 5

    @classmethod
    def getLevelFromStr(cls, lvl:str):
        ch = lvl[0].upper()
        if ch == 'T':
            return LogLvl.TRACE
        if ch == 'W':
            return LogLvl.WARNING
        if ch == 'E':
            return LogLvl.ERROR
        if ch == 'D':
            return LogLvl.DEBUG
        return LogLvl.INFO

class ProxyObjectType(IntEnum):
    ALL         = 0 # ??? Mittomen? - Mailernek esetleg ...
    CUSTOMER    = 1
    UNASCUSTOMER= 21
    PRODUCT     = 2
    UNASPRODUCT = 22
    ORDER       = 3
    UNASORDER   = 23
    PRICE       = 4
    INVENTORY   = 5
    INFOTYPE    = 6 # ??? Mittomen? - Mailernek esetleg ...
    UNKNOWN     = 97 # Ez se tudom, mire kellhet - Mailernek esetleg ...
    UNTYPED     = 98 # Ez se tudom, mire kellhet - Mailernek esetleg ...

    @classmethod
    def getTypeFromStr(cls, lvl:str):
        ch = lvl[0].upper()
        if ch == 'P' and 'O' == lvl[2].upper():
            return ProxyObjectType.PRODUCT
        if ch == 'P' and 'I' == lvl[2].upper():
            return ProxyObjectType.PRICE
        if ch == 'O':
            return ProxyObjectType.ORDER
        if ch == 'I':
            return ProxyObjectType.INVENTORY
        if ch == 'C':
            return ProxyObjectType.CUSTOMER
        return ProxyObjectType.ALL

class MyProgramFlowErrorException(Exception):
    def __init__(self, msg="Signal for exception already catched", code:ProxyErrCode=ProxyErrCode.UNKNOWN ):
        self.responseCode = code
        self.responseMessage = msg[ msg.index('>'):].replace('\r\n','') if msg.startswith('<?xml ') else msg
        super().__init__(self.responseMessage)

    def __str__(self):
        return f'{self.responseCode} -> {self.responseMessage}'

class MyWarningBreakException(Exception):
    def __init__(self, msg="Continuable program break", code:ProxyErrCode=ProxyErrCode.UNKNOWN ):
        self.responseCode = code
        self.responseMessage = msg
        self.message = msg
        super().__init__(msg)

    def __str__(self):
        return f'{self.responseCode} -> {self.responseMessage}'

class MyProgramFlowWarningException(MyWarningBreakException):
    def __init__(self, msg="Signal for exception already catched", code:ProxyErrCode=ProxyErrCode.UNKNOWN ):
        self.responseCode = code
        self.responseMessage = msg[39:].replace('\r\n','') if msg.startswith('<?xml ') else msg
        super().__init__(self.responseMessage)

    def __str__(self):
        return f'{self.responseCode} -> {self.responseMessage}'

class UnasCommErrException(Exception):
    def __init__(self, code, text):
        self.responseMessage = text
        self.responseCode = code
        super().__init__("Unhandled communication error")

    def __str__(self):
        return f'{self.responseCode} -> {self.responseMessage}'

class UnasCommIpDisabledException(Exception):
    def __init__(self, client=(None, 0), msg:typing.Optional[str]=None):
        ip, port = client 
        self.ip = ip or MU.getUnasContext().lastIpAddress
        self.message = msg or f'Client IP:{self.ip} is disabled'
        super().__init__(self.message)

class ControlProcessSocketExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

class ControlProcessWebExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

class AlertMailType():
    type: UnasTransactionType
    sent: int
    objId: int
    objTyp: ProxyObjectType
    errCode: ProxyErrCode
    trId : int
    def __init__(self, typ: UnasTransactionType, oid: int = 0, otyp: ProxyObjectType = ProxyObjectType.UNTYPED, code: ProxyErrCode = ProxyErrCode.UNKNOWN, ts:int=0):
        self.sent = 0
        self.type   = typ 
        self.objId  = oid
        self.objTyp = otyp
        self.errCode= code
        self.trId = ts if ts > 0 else MU.getTS()

    def toJson(self):
        return '{ %s }' % f'"type" : "{self.type.name}","objId" : "{self.objId}","objTyp" : "{self.objTyp.name}","errCode" : "{self.errCode.name}", \
            "trId" : "{self.trId}","trTime" : "{MU.getTimeStringTS(self.trId)}","trAction" : "{MU.getActionTypeNameFromTS(self.trId)}"'

class AlertMailTypeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AlertMailType):
            return {
                "type"     : o.type.name,
                "objId"    : str(o.objId), ## joe@20250623 
                "objTyp"   : o.objTyp.name,
                "errCode"  : o.errCode.name,
                "trId"     : o.trId,
                "trTime"   : MU.getTimeStringTS(o.trId),
                "trAction" : MU.getActionTypeNameFromTS(o.trId)
            }
        return super().default(o)    


class ProxyClient:
    ip :  str
    lastTS:int
    lastActive:int
    isMaster: bool
    prio: int
    def __init__(self, ip:str, ts:int = 0, act=0, master= False, priority=-1):
        self.ip = ip
        self.lastTS = ts if ts > 0 else MU.getTS()
        self.lastActive = act if act > 0 else MU.getCurrTime()
        self.isMaster = master
        self.prio = priority

class UnasContext:
    processName: str
    authcnt:int
    getcnt:int
    setcnt:int
    commCnt:int
    commOkCnt:int
    commErrCnt:int 
    commCntTotal:int
    commOkCntTotal:int
    commErrCntTotal:int 
    loginErrCnt:int 
    lastMod: int
    lastTS:int
    # saved context
    lastGetCustomer  : int
    lastGetOrder : int
    lastSetCustomer : int
    lastSetProduct : int
    lastUnasOrderStatus : int
    # saved context
    lastLogin:int
    lastAction: typing.Optional[str]=None
    lastIpAddress: typing.Optional[str]=None
    commBlocked: int
    lastBlockMailSent: int
    lastYarnMailSent: int
    lastAlertMailSent: typing.List[AlertMailType]
    statEntryMySqlId: int
    #
    masterClient : typing.Optional[ ProxyClient]=None
    clientList: typing.Dict[str, ProxyClient ]
    
    def __init__(self, procName = 'Proxy'):
        self.processName = procName
        self.getcnt      = 0
        self.setcnt      = 0
        self.commCnt     = 0
        self.commOkCnt   = 0
        self.commErrCnt  = 0 
        self.loginErrCnt = 0 
        self.lastMod     = 0
        self.lastTS      = 0
        self.lastLogin   = 0
        self.lastAction  = None # TODO Valamiert ezt kikommenteztem egyszer. Nem szerepelt a structban, ha None volt?
        self.lastIpAddress  = None
        self.commCntTotal      = 0
        self.commOkCntTotal    = 0
        self.commErrCntTotal   = 0
        self.commBlocked       = 0
        self.lastBlockMailSent = 0
        self.lastAlertMailSent = []
        self.lastYarnMailSent  = 0
        self.statEntryMySqlId  = 0
        self.lastGetCustomer     = 0
        self.lastGetOrder        = 0
        self.lastSetCustomer     = 0
        self.lastSetProduct      = 0
        self.lastUnasOrderStatus = 0
        self.masterClient        = None
        self.clientList          = {}
        

    def toJson(self):
        jsStr = f'''
        "processName"      : "{self.processName}",
        "getcnt"           :  {self.getcnt},
        "setcnt"           :  {self.setcnt},
        "commCnt"          :  {self.commCnt},
        "commOkCnt"        :  {self.commOkCnt},
        "commErrCnt"       :  {self.commErrCnt},
        "loginErrCnt"      :  {self.loginErrCnt},
        "lastMod"          : "{self.tsToS(self.lastMod)}",
        "lastTS"           :  {self.lastTS},
        "lastTStime"       : "{self.tsToS(MU.getTimeFromTS(self.lastTS))}",
        "lastTStype"       : "{MU.getActionTypeNameFromTS(self.lastTS)}",
        "lastLogin"        : "{self.tsToS(self.lastLogin)}",
        "lastAction"       : "{self.lastAction}",
        "lastIpAddress"    : "{self.lastIpAddress}",
        "commCntTotal"     :  {self.commCntTotal},
        "commOkCntTotal"   :  {self.commOkCntTotal},
        "commErrCntTotal"  :  {self.commErrCntTotal},
        "commBlocked"      :  {self.commBlocked},
        "lastBlockMailSent": "{self.tsToS(self.lastBlockMailSent)}",
        "lastAlertMailSent": "{self.lastAlertMailSent}",
        "lastYarnMailSent" : "{self.tsToS(self.lastYarnMailSent)}",
        "statEntryMySqlId" :  {self.statEntryMySqlId},
        "lastGetCustomer"  : "{self.tsToS(self.lastGetCustomer)}",
        "lastGetOrder"     : "{self.tsToS(self.lastGetOrder)}",
        "lastSetCustomer"  : "{self.tsToS(self.lastSetCustomer)}",
        "lastSetProduct"   : "{self.tsToS(self.lastSetProduct)}",
        "lastUnasOrderStatus": "{self.tsToS(self.lastUnasOrderStatus)}"
        '''
        return '{%s}' % jsStr

    def tsToS(self, ts) -> str:
        if ts > 100:
            return f"{MU.tsToDateStr(ts)} ({ts})"
        return ''
    
    def clearCounters(self):
        self.commErrCnt = 0
        self.commBlocked = 0
        self.loginErrCnt = 0

