import json

import MyUtils as MU


class UnasProductCache:
    unasId: int
    symbolId: int
    sku: str
    vat: float
    state: str
    status: int
    lastmod: int
    qty: float
    # egyelore nincs raktarkezeles: stock = ({  warehouse: qty })
    stocks: dict

    ProductStatus_INACTIVE = 0
    ProductStatus_ACTIVE = 1
    ProductStatus_NEW = 2
    ProductStatus_NOTAVAILABLE = 3
    
    ProductState_LIVE    = 'live'
    ProductState_DELETED = 'deleted'
    ProductState_PENDING = 'pending'

    def __init__(self, unasid, sku, sid = 0, q = 0.0,  vat = 27.0, state = ProductState_LIVE, status = ProductStatus_NEW, sts = ({ -1, 0 })):
        self.unasId = unasid
        self.symbolId = sid
        self.sku = sku
        self.vat = vat
        self.state = state
        self.status = status
        self.qty = q
        self.lastmod = MU.UtcNow(1 + MU.GETPRODUCT_INTERVAL * 2)
        self.stocks = sts

class UnasProductCacheEncoder(json.JSONEncoder):
    
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
