import MyUtils as MU
from CustomerAddressHelper import CustomerAddress
import MyUtils as MU
from typing import Any, List
from lxml.etree import _Element

def buildAzonData(emil, taxNo):
    _eml = '' if emil is None else '' if emil.text is None else emil.text.strip()
    _tax  = '' if taxNo is None else '' if taxNo.text is None else taxNo.text.strip()
    return _tax if len(_tax)>0 else _eml if len(_eml) > 0 else None

def buildCustAzonById( id ):
    _id = '' if id is None else  str(id).strip()
    return None if len(_id) < 1 else  '#' + _id # type: ignore

class UnasCustomerCache:
    unasId: int
    symbolId: int
    code: str
    custAzon: str
    email: str
    taxNumber: str
    state: str
    lastmod: int
    unasAddrObj = List[CustomerAddress]
    unasAddrXml = List[_Element]

    def __init__(self, unasid:int=None, emil:str=None, taxNo:str=None, code:str=None, sid:int = 0, state:str = 'live'): # type: ignore
        self.unasId = unasid
        self.symbolId = sid
        self.email = '' if emil is None else str(emil).strip()
        self.taxNumber = '' if taxNo is None else str(taxNo).strip()
        self.custAzon = self.correctAzonData(self.email, self.taxNumber, unasid ) # type: ignore
        #self.custAzon = buildAzonData(emil, taxNo)
        if self.custAzon is None:
            raise ValueError("Customer Identifier is missing")
        if len(self.custAzon.strip()) < 1:
            raise ValueError("Customer Identifier is empty")
        self.code = code
        self.state = state
        self.lastmod = MU.UtcNow(1 + MU.GETCUSTOMER_INTERVAL * 2)
        self.unasAddrObj = []
        self.unasAddrXml = []

    def toStr(self):
        return '{ "unasId":%s, "symbolId":%s, "lastmod":(%i)[%s], "code":"%s", "custAzon":"%s", "email":"%s", "taxNumber":"%s", "state":"%s" }' % (
                            self.unasId, self.symbolId, self.lastmod, MU.tsToDateStr(self.lastmod), self.code, self.custAzon, self.email, self.taxNumber, self.state)

    VARIABLES = ["unasId","symbolId", "lastmod", "code", "custAzon", "email", "taxNumber", "state"]
    def toXml(self):
        #xxxvars = dir(self)
        xmlArr = []
        for varName in self.VARIABLES:
            varValue = getattr(self, varName, None)
            xmlArr.append( f"<{varName}>{varValue}</{varName}>" )
        return '<Customer>%s</Customer>' % " ".join(xmlArr)

    def correctAzonData(self, emil:str, taxNo:str, unasid : int):
        _eml = '' if emil is None else emil.strip()
        _tax = '' if taxNo is None else taxNo.strip()
        _id  = None if unasid is None else str(unasid)
        return _tax if len(_tax)>0 else _eml if len(_eml) > 0 else buildCustAzonById(_id)
    