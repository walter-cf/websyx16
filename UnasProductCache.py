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