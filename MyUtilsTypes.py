from typing import Dict
from enum import IntEnum

class UnasTransactionType(IntEnum):
    CREATENEW   = 0
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

class UnasContext:
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
    lastLogin:int
    lastAction: str
    commBlocked: int
    lastBlockMailSent: int
    lastAlertMailSent: Dict[UnasTransactionType, int]
    statEntryMySqlId: int
    
    def __init__(self):
        self.authcnt     = 0
        self.getcnt      = 0
        self.setcnt     = 0
        self.commCnt     = 0
        self.commOkCnt   = 0
        self.commErrCnt  = 0 
        self.loginErrCnt = 0 
        self.lastMod     = 0
        self.lastTS      = 0
        self.lastLogin   = 0
        self.lastAction  = None
        self.commCntTotal      = 0
        self.commOkCntTotal    = 0
        self.commErrCntTotal   = 0
        self.commBlocked       = 0
        self.lastBlockMailSent = 0
        self.lastAlertMailSent = dict({})
        self.statEntryMySqlId  = 0
        
    def clearCounters(self):
        self.commErrCnt = 0
        self.commBlocked = 0
        self.loginErrCnt = 0

