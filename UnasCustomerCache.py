import json
from typing import Any, List

from lxml.etree import _Element

import MyUtils as MU
from CustomerAddressHelper import CustomerAddress


def buildAzonData_NU(emil, taxNo):
    if emil is not None and str(emil).startswith('haffner'):
        print(emil, taxNo)
    _eml = '' if emil is None else '' if emil.text is None else emil.text.strip()
    _tax  = '' if taxNo is None else '' if taxNo.text is None else taxNo.text.strip()
    return _tax if len(_tax)>0 else _eml if len(_eml) > 0 else None

def buildCustAzonById_NU( id ):
    _id = '' if id is None else  str(id).strip()
    return None if len(_id) < 1 else  '#' + _id # type: ignore

class UnasCustomerCache:
    unasId: int
    symbolId: int
    code: str
    #custAzon: str
    customerGroup: str | None = None
    # priceCategory: str | None    
    specialCustomerCategory: str | None = None
    email: str
    taxNumber: str
    state: str
    lastmod: int
    authorized: bool
    unasAddrObj = List[CustomerAddress]
    unasAddrXml = List[_Element]

    def __init__(self, unasid:int=None, emil:str=None, taxNo:str=None, code:str=None, sid:int = 0 # type: ignore
                 , state:str = 'live', authed: bool = False
                 , cg:str = None, priceCat:str = None                            ): # type: ignore
        self.unasId = unasid
        self.symbolId = sid
        self.email = '' if emil is None else str(emil).strip()
        self.taxNumber = '' if taxNo is None else str(taxNo).strip()
        #self.custAzon = self.correctAzonData(self.email, self.taxNumber, unasid ) # type: ignore
        #self.custAzon = buildAzonData(emil, taxNo)
        #if self.custAzon is None:
        #    raise ValueError("Customer Identifier is missing")
        #if len(self.custAzon.strip()) < 1:
        #    raise ValueError("Customer Identifier is empty")
        self.code = code
        self.state = state
        self.lastmod = MU.UtcNow(1 + MU.GETCUSTOMER_INTERVAL * 2)
        self.unasAddrObj = []
        self.unasAddrXml = []
        self.authorized = authed
        # self.customerGroup = cg       FULL lekeresnel a CG-t megkapom, de a proceCat remenytelen, szal KI KELL Szedni!
        # self.priceCategory = priceCat
        
    def toStr(self):
        return '{ "unasId":%s, "symbolId":%s, "lastmod":(%i)[%s], "code":"%s", "email":"%s", "taxNumber":"%s", "state":"%s" }' % (
                    self.unasId, self.symbolId, self.lastmod, MU.tsToDateStr(self.lastmod), self.code
                    , self.email, self.taxNumber, self.state
                    # , self.customerGroup, self.priceCategory
                    )

    def fromXml(self, xml, symbolid:int=0):
        self.symbolId = symbolid if symbolid > 0 else next((x.Value for x in xml.find('Params').getchildren() if x.Name =='symbolId'), 0)  
        self.code = MU.mkCustomerCode(self)
        self.state = 'pending'
        self.lastmod = MU.UtcNow(1 + MU.GETCUSTOMER_INTERVAL * 2)
        self.unasAddrObj = xml.Addresses
        # self.unasAddrXml = []
        self.authorized = 'yes' == MU.nullSafeStru( xml, [ 'Authorize', 'Admin' ], '-' )
        # self.customerGroup = 'x'
        # self.priceCategory = 'x'

    VARIABLES = ["unasId","symbolId", "lastmod", "code", "email", "taxNumber", "state"]
    def toXml(self):
        #xxxvars = dir(self)
        xmlArr = []
        for varName in self.VARIABLES:
            varValue = getattr(self, varName, None)
            xmlArr.append( f"<{varName}>{varValue}</{varName}>" )
        return '<Customer>%s</Customer>' % " ".join(xmlArr)

    def correctAzonData_NU(self, emil:str, taxNo:str, unasid : int):
        _eml = '' if emil is None else emil.strip()
        _tax = '' if taxNo is None else taxNo.strip()
        _id  = None if unasid is None else str(unasid)
        return _tax if len(_tax)>0 else _eml if len(_eml) > 0 else buildCustAzonById_NU(_id)

class UnasCustomerCacheEncoder(json.JSONEncoder):
        def conver_element(self, element):
                foo = self.recursive_dict(element)
                return foo

        def recursive_dict(self, element):
            return element.tag, dict(map(self.recursive_dict, element)) or element.text
                
        def recursive_dict_with_attribs(self, element):
            if element.text == None and len(element.attrib):
                return element.tag, element.attrib
            return element.tag, dict(map(self.recursive_dict_with_attribs, element)) or element.text
                
        def default(self, o):
            return self.recursive_dict(o) if "<class 'lxml.etree._Element'>" == str(type(o)) else o.__dict__
