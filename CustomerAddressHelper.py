from typing  import Any, List, Dict, Union
import MyUtils as MU
import FdbUtils as FBU
# from datetime import datetime as DT


#
# Constants 
#
CAstate_unasOnly = "unasOnly"
CAstate_symbolOnly = "symbolOnly"
CAstate_dummy = "dummy"
CAstate_duplicate = "duplicate"
CAstate_assigned = "assigned"
CAstate_check = "check"
CAstate_X = "x"
CAtype_shipping = "shipping"
CAtype_dummy    = "dummy"
CAtype_other    = "other"
CAtype_invoice  = "invoice"


class CustomerAddress:
    Id                    : int
    Customer              : int
    Preferred             : int
    Code                  : str
    Name                  : str
    DisplayCountry        : int
    Country               : str
    Region                : str
    Township              : str
    Zip                   : str
    City                  : str
    Street                : str
    HouseNumber           : str
    ContactName           : str
    Phone                 : str
    Fax                   : str
    Sms                   : str
    Email                 : str
    IsPerson              : int
    IsCompany             : int
    CompanyType           : int
    EUMembership          : int
    CompanyTaxNumber      : str
    CompanyEUTaxNumber    : str
    CompanyGroupTaxNumber : str
    CompanyTradeRegNumber : str
    Agent                 : int
    AgentStrict           : int
    PaymentMethod         : int
    TransportMode         : int
    DeliveryCDay          : int
    DeliveryInfo          : str
    ParcelInfo            : int
    GLN                   : str 
    Comment               : str 
    VoucherComment        : str
    Deleted               : int
    RowVersion            : str
    RowCreate             : str
    RowModify             : str    
    #
    state : str # new , dele, paired
    idx   : int
    
    def presetCode(self, unasid:int, idx:int):
            self.Code     = MU.CUSTOMER_CODE_PREFIXES["patternAddr"] % (MU.CUSTOMER_CODE_PREFIXES["address"], unasid, idx)
            if MU.isLogLevelDebug:
                print(self.Code)

    def __init__(self, id:int = 0, unasid:int = 0, country: str = None, region: str = None, zip: str = None, city: str = None, # type: ignore
                 street: str = None, house: str = None, name: str = None, contact:str = None, idx:int = 0, preferred:int = 0, deleted:int = 0 ): # type: ignore
        self.Id           = id
        self.Preferred    = preferred
        if unasid > 0 and idx > 0:
            self.presetCode(unasid, idx)
        self.Name         = name
        self.Country      = country
        self.Region       = region
        self.Zip          = zip
        self.City         = city
        self.Street       = street
        self.HouseNumber  = house
        self.ContactName  = contact
        self.Deleted      = deleted
        #
        self.state = ''
        self.idx = idx

    def initAddr_w_HouseNumber(self, tag, state=CAstate_unasOnly, deleted:int=0):
        self.Name         = tag.Name
        self.Country      = tag.Country
        self.Region       = tag.County
        self.Zip          = tag.ZIP
        self.City         = tag.City
        self.Street       = str(tag.Street if not tag.find('StreetName') else tag.StreetName) + str( '' if not tag.find('StreetType') else (' ' + tag.StreetType ))
        self.HouseNumber  = None if not tag.find('StreetNumber') else tag.StreetNumber # type: ignore
        # self.ContactName  = tag.find('Name')
        self.Deleted      = deleted
        self.state        = state
        
    def initAddr(self, tag, state=CAstate_unasOnly, deleted:int=0):
        self.Name         = tag.Name
        self.Country      = tag.Country
        self.Region       = tag.County
        self.Zip          = tag.ZIP
        self.City         = tag.City
        self.Street       = tag.Street
        self.HouseNumber  = None
        # self.ContactName  = tag.find('Name')
        self.Deleted      = deleted
        self.state        = state

#
# SQL consts
#
sqlCreate ="""CREATE TABLE "CustomerAddress" (
  "Id" BIGINT NOT NULL,
  "Customer" BIGINT NOT NULL,
  "Preferred" SMALLINT DEFAULT 0 NOT NULL,
  "Code" VARCHAR(40) COLLATE UNICODE_CI,
  "Name" VARCHAR(100) NOT NULL COLLATE UNICODE_CI,
  "DisplayCountry" SMALLINT DEFAULT 0 NOT NULL,
  "Country" VARCHAR(100) COLLATE UNICODE_CI,
  "Region" VARCHAR(100) COLLATE UNICODE_CI,
  "Township" VARCHAR(100) COLLATE UNICODE_CI,
  "Zip" VARCHAR(10) COLLATE UNICODE_CI,
  "City" VARCHAR(100) COLLATE UNICODE_CI,
  "Street" VARCHAR(100) COLLATE UNICODE_CI,
  "HouseNumber" VARCHAR(20) COLLATE UNICODE_CI,
  "ContactName" VARCHAR(100) COLLATE UNICODE_CI,
  "Phone" VARCHAR(20) COLLATE UNICODE_CI,
  "Fax" VARCHAR(20) COLLATE UNICODE_CI,
  "Sms" VARCHAR(20) COLLATE UNICODE_CI,
  "Email" VARCHAR(100) COLLATE UNICODE_CI,
  "IsPerson" SMALLINT DEFAULT 0 NOT NULL,
  "IsCompany" SMALLINT DEFAULT 0 NOT NULL,
  "CompanyType" INTEGER DEFAULT 0 NOT NULL,
  "EUMembership" INTEGER,
  "CompanyTaxNumber" VARCHAR(20) COLLATE UNICODE_CI,
  "CompanyEUTaxNumber" VARCHAR(20) COLLATE UNICODE_CI,
  "CompanyGroupTaxNumber" VARCHAR(20) COLLATE UNICODE_CI,
  "CompanyTradeRegNumber" VARCHAR(20) COLLATE UNICODE_CI,
  "Agent" BIGINT,
  "AgentStrict" SMALLINT DEFAULT 0 NOT NULL,
  "PaymentMethod" BIGINT,
  "TransportMode" BIGINT,
  "DeliveryCDay" INTEGER,
  "DeliveryInfo" BLOB SUB_TYPE TEXT SEGMENT SIZE 80,
  "ParcelInfo" BIGINT,
  GLN VARCHAR(40) COLLATE UNICODE_CI,
  "Comment" BLOB SUB_TYPE TEXT SEGMENT SIZE 80,
  "VoucherComment" BLOB SUB_TYPE TEXT SEGMENT SIZE 80,
  "Deleted" SMALLINT DEFAULT 0 NOT NULL,
  "RowVersion" TIMESTAMP DEFAULT CURRENT_TIMESTAMP  NOT NULL,
  "RowCreate" TIMESTAMP,
  "RowModify" TIMESTAMP,
  CONSTRAINT "PK_CustomerAddress"
  PRIMARY KEY (Id)
    USING ASCENDING INDEX "PK_CustomerAddress"
)
"""

class CustomerAddressHelper:
    customerid: int
    unasid: int
    symbAddresses: List[CustomerAddress]
    unasAddresses: List[CustomerAddress]
    unasAddrTag: Any
    
    def __init__(self, errors, cid: int, uid: int=0 , tag = None):
        self.customerid = cid
        self.unasid = uid
        self.symbAddresses = self.loadSymbolAddresses(errors)
        self.unasAddresses = []
        self.unasAddrTag = tag

    def compareCA( self, a : CustomerAddress, b : CustomerAddress ) -> bool:
        #E = a.Customer == b.Customer
        #
        E =       self.strCmp(a.Name        , b.Name        )
        E = E and self.strCmp(a.Country     , b.Country     )
        E = E and self.strCmp(a.Region      , b.Region      )
        E = E and self.strCmp(a.Zip         , b.Zip         )
        E = E and self.strCmp(a.City        , b.City        )
        E = E and self.strCmp(a.Street      , b.Street      )
        E = E and self.strCmp(a.HouseNumber , b.HouseNumber )
        return E

    def getSymbolCAmaxIndx(self):
        #self.symbAddresses = self.loadSymbolAddresses()
        max = 0
        for cc in self.symbAddresses:
            xx = '' if cc.Code is None else cc.Code.split('-')
            if len(xx) == 3:
                ii = self.toInt(xx[2])
                if ii > max:
                    max = ii
        return max

    def getSymbolCAactiveCnt(self):
        max = 0
        for cc in self.symbAddresses:
            if cc.Deleted == 0:
                max = max + 1
        return max
    
    def strCmp( self, a : str, b : str ) -> bool:
        aa = '' if a is None else str(a)
        bb = '' if b is None else str(b)
        if aa.upper() == '<NULL>' :
            aa = ''
        if bb.upper() == '<NULL>' :
            bb = ''
        if len(aa.strip()) == 0 and len(bb.strip()) == 0:
            return True
        return aa == bb

    def toInt(self, s:str) -> int:
        return 0 if s is None else int(s)
    
    def loadSymbolAddresses(self, errors) -> List[CustomerAddress]:
        self.symbAddresses = []
        cols = FBU.colListCA
        if (self.customerid) > 0:
            rex = FBU.getCustomerAddressesById(self.customerid)
            for r in rex:
                ca = CustomerAddress(
                    id          = self.toInt(r[  cols.index("Id") ]),
                    preferred   = self.toInt(r[  cols.index("Preferred") ]),
                    country     = r[  cols.index("Country") ],
                    region      = r[  cols.index("Region") ],
                    zip         = r[  cols.index("Zip") ],
                    city        = r[  cols.index("City") ],
                    street      = r[  cols.index("Street") ],
                    house       = r[  cols.index("HouseNumber") ],
                    name        = r[  cols.index("Name") ],
                    #contact=
                    #idx=
                    deleted     = r[  cols.index("Deleted") ],
                )
                ca.Code = r[  cols.index("Code") ]
                ca.idx = 0 if ca.Code is None else self.toInt(ca.Code.split('-')[2]) # Ezt azert meg kellene nezni!
                ca.state = CAstate_symbolOnly
                self.symbAddresses.append(ca)
        return self.symbAddresses

    def rebuildCAlist(self, customerId:int):
        for ss in self.symbAddresses:
            if ss.state == CAstate_symbolOnly:
                FBU.setDeletedAddrById(ss.Id)
        for uu in self.unasAddresses:
            if uu.state == CAstate_unasOnly:
                uu.Id = FBU.addCustAddr(custSymbolId= -2 if self.customerid < 1 else self.customerid,
                        unasId=self.unasid , addressIdx=uu.idx,
                        name=uu.Name, city=uu.City, zip=uu.Zip, region=uu.Region, country=uu.Country,
                        street=uu.Street, house=uu.HouseNumber )

    def analyzeCAlist( self ):
        self.analyzeCA(self.unasAddresses, self.symbAddresses )
        
    def analyzeCA( self, al : List[CustomerAddress], bl : List[CustomerAddress]):
        for uu in al:
            for ss in bl:
                if self.compareCA(uu, ss):
                    uu.state = 'paired'
                    ss.state = 'paired'

    def identfyCA( self, uca : CustomerAddress) -> CustomerAddress:
        for ss in self.symbAddresses:
            if self.compareCA(uca, ss):
                ss.state =  'paired'
                return ss
        return None # type: ignore

    def pairingCA( self, bl : List[CustomerAddress]):
        pass

    def buildSqlInsert( self, a : CustomerAddress ) -> str:
        return 'insert into "CustomerAddress"'

    def buildSqlUpdate( self, a : CustomerAddress ) -> str:
        return 'insert into "CustomerAddress"'

    def buildSqlDelete( self, a : CustomerAddress ) -> str:
        return 'insert into "CustomerAddress"'

    def symbXmlBuilder( self, a : CustomerAddress ) -> str:
        return 'x'
    
    def unasXmlBuilder( self, a : CustomerAddress ) -> str:
        return 'x'
