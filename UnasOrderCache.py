import MyUtils as MU
from  typing import Any, TypedDict

class UnasOrderCache:
    orderKey    : str
    unasId      : int
    symbolId    : int
    code        : str
    custId      : int
    unasCustId  : int
    orderStatus : str
    acknowledged: bool
    lastmod     : int
    ordXml      : Any
    
    def __init__(self, ordKey:str, sid:int = 0, ordcode:str = None, custid:int = 0, status:str = None, lastmod:int = 0): # type: ignore
        self.orderKey = ordKey
        self.symbolId = sid
        self.code = ordcode
        self.custId = custid
        self.orderStatus = status
        self.lastmod = lastmod
        self.unasId = 0
        self.unasCustId = 0
        self.acknowledged = False

        
    def initFromXml(self, oo):
        self.ordXml = oo
        self.code =  self.findItem(["xx","xx","xx"])
        #self.custId =  self.toInt(self.findItem(["xx","xx","xx"]))
        self.orderStatus =  self.findItem(["Status"])
        self.lastmod = MU.dateStrToTs( self.findItem(["DateMod"]))
        self.unasCustId = self.toInt( self.findItem(["Customer","Id"]))
        self.unasId = self.toInt(self.findItem(["Id"]))
        #
        if oo.find("Params") is not None:
            for p in oo.find("Params"):
                if "symbolId" == p.find("Name"):
                    self.symbolId =  self.toInt(p.find("Value"))
                if "symbolCustomerId" == p.find("Name"):
                    self.custId =  self.toInt(p.find("Value"))
        
    def toInt(self, s):
        if s is None:
            return 0
        if not isinstance(s, str):
            s = str(s)
        return 0 if 'None' == s else int(s)
    
    def findItem(self, args) -> str:
        tag = self.ordXml
        for k in args:
            if tag is not None:
                tag = tag.find(k)
        return None if tag is None else tag.text # type: ignore
        
    def __getitem__(self, index):
        # if isinstance(index, int):
        #     return self.items[index]
        # elif isinstance(index, str):
        #     return self.items.index(index)
        if isinstance(index, str):
            return self[index]
        else:
            raise TypeError("Invalid Argument Type")

    def __setitem__(self, index, val):
        # if isinstance(index, int):
        #     return self.items[index]
        # elif isinstance(index, str):
        #     return self.items.index(index)
        # else:
        #     raise TypeError("Invalid Argument Type")
        if isinstance(index, str):
            self[index] = val
        else:
            raise TypeError("Invalid Argument Type")

    def toStr(self):
         return '{ "key":%s, "symbolId":%i, "lastmod":(%i)[%s], "code":"%s", "custId":%i, "status":"%s" , "ack":%i  }' % (
                             self.orderKey, self.symbolId, self.lastmod, MU.tsToDateStr(self.lastmod), self.code,
                             self.custId, self.orderStatus, 1 if self.acknowledged else 0)
