import MyUtils as MU

class UnasProductCache:
    unasId: int
    symbolId: int
    sku: str
    vat: float
    state: str
    lastmod: int
    qty: float
    # egyelore nincs raktarkezeles: stock = ({  warehouse: qty })
    stocks: dict


    def __init__(self, unasid, sku, sid = 0, q = 0.0,  vat = 27.0, state = 'live', status = 2, sts = ({ -1, 0 })):
        self.unasId = unasid
        self.symbolId = sid
        self.sku = sku
        self.vat = vat
        self.state = state
        self.qty = q
        self.lastmod = MU.UtcNow(1 + MU.GETPRODUCT_INTERVAL * 2)
        self.stocks = sts