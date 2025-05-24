import json
import typing

from lxml import etree as ET

import MyUtils as MU


class UnasOrderCache:
    orderKey    : str
    unasId      : int
    symbolId    : int
    code        : typing.Optional[str]
    symbolCustId: int
    unasCustId  : int
    orderStatus : str
    acknowledged: bool
    lastmod     : int
    badCounter  : int
    ordXml      : typing.Any
    
    def __init__(self, ordKey:str, sid:int = 0, ordcode:str = None, symbCustid:int = 0, status:str = None, lastmod:int = 0): # type: ignore
        self.orderKey = ordKey
        self.symbolId = sid
        self.code = ordcode
        self.symbolCustId = symbCustid
        self.orderStatus = status
        self.lastmod = lastmod
        self.unasId = 0
        self.unasCustId = 0
        self.acknowledged = False
        self.badCounter = 0

    def fromMunch(self, mObj):
        self.orderKey     = mObj.orderKey
        self.symbolId     = mObj.symbolId
        self.code         = mObj.code
        self.symbolCustId = mObj.symbolCustId
        self.orderStatus  = mObj.orderStatus
        self.lastmod      = mObj.lastmod
        self.unasId       = mObj.unasId
        self.unasCustId   = mObj.unasCustId
        self.acknowledged = mObj.acknowledged
        self.badCounter   = mObj.badCounter
        self.ordXml       = None

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def getParamValeByName(self, obj, name):
        if len(obj.findall('Params')) > 0:
            for prm in obj.find('Params').getchildren():
                if name == prm.Name:
                    return prm.Value
        return None

    def getParamValueByNameObj(self, obj, name):
        if len(obj.findall('Params')) > 0:
            for prm in obj.find('Params').getchildren():
                if name == prm.find('Name').text:
                    return prm.find('Value').text
        return None
    
    def initFromXmlObj(self, oo):
        self.ordXml = oo
        cust = oo.find('Customer')
        _val = self.getParamValueByNameObj(cust, 'symbolCode')
        self.code = None if _val is None else str(_val)
        _val = self.getParamValueByNameObj(cust, 'symbolId')
        self.symbolCustId =  0 if _val is None else int(str(_val))
        self.orderStatus =  self.findItem(["Status"])
        self.lastmod = MU.dateStrToTs( self.findItem(["DateMod"]))
        self.unasCustId = self.toInt( self.findItem(["Customer","Id"]))
        self.unasId = self.toInt(self.findItem(["Id"]))
        #
        if oo.find("Params") is not None:
            for p in oo.find("Params").getchildren():
                if "symbolId" == p.find("Name").text:
                    self.symbolId = self.toInt(p.find("Value").text)

    def initFromXml(self, oo):
        self.ordXml = oo
        _val = self.getParamValeByName(oo.Customer, 'symbolCode')
        self.code = None if _val is None else str(_val)
        _val = self.getParamValeByName(oo.Customer, 'symbolId')
        self.symbolCustId =  0 if _val is None else int(str(_val))
        self.orderStatus =  self.findItem(["Status"])
        self.lastmod = MU.dateStrToTs( self.findItem(["DateMod"]))
        self.unasCustId = self.toInt( self.findItem(["Customer","Id"]))
        self.unasId = self.toInt(self.findItem(["Id"]))
        #
        if oo.find("Params") is not None:
            for p in oo.find("Params").getchildren():
                if "symbolId" == p.find("Name"):
                    self.symbolId =  self.toInt(p.find("Value"))
                if "symbolCustomerId" == p.find("Name"):              #  notUsed, pedig jo lenne!
                    self.symbolCustId =  self.toInt(p.find("Value"))
        
    def toInt(self, s):
        if s is None:
            return 0
        if not isinstance(s, str):
            s = str(s)
        if len(s) == 0:
            return 0
        return 0 if 'None' == s else int(s)
    
    def findItem(self, args) -> str:
        tag = self.ordXml
        for k in args:
            if tag is not None:
                tag = tag.find(k)
        return None if tag is None else tag.text # type: ignore

    def findItemObj(self, args) -> str:
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
         return '{ "key":%s, "symbolId":%i, "lastmod":(%i)[%s], "code":"%s", "symbolCustId":%i, "status":"%s" , "ack":%i m badCnt:%d }' % (
                             self.orderKey, self.symbolId, self.lastmod, MU.tsToDateStr(self.lastmod), self.code,
                             self.symbolCustId, self.orderStatus, 1 if self.acknowledged else 0, self.badCounter)

    def  __str__(self):
        return self.toStr()
        
class UnasOrderCacheEncoder(json.JSONEncoder):
    
        def recursive_dict(self, element):
            return element.tag, dict(map(self.recursive_dict, element)) or element.text
                
        def recursive_dict_with_attribs(self, element):
            if element.text == None and len(element.attrib):
                return element.tag, element.attrib
            return element.tag, dict(map(self.recursive_dict_with_attribs, element)) or element.text
                
        def default(self, o):
            if "<class 'lxml.etree._Element'>" == str(type(o)):
                return self.recursive_dict(o)
            elif "<class 'set'>" == str(type(o)):
                return str(o)
            else:
                return o.__dict__
