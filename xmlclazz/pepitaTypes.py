class Param:
    Id:  int
    Name: str
    Value: str

class Image:
    Type: str
    Url: str

class Status:
    Active: bool
    
class Stock:
    status: Status
    Qty: int

class Description:
    Short : str
    
class Product:
    Id : int
    Sku : str
    Name: str
    Params : list[ Param ]
    Images : list[ Image ]
    Stocks : list[ Stock ]
    descr  : Description
    LastModTime: str
