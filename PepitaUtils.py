#!/opt/pepita-test/.venv/bin/python
import os,sys
import lxml.objectify as objectify
import lxml .etree as ET

import MyUtils as MU
from UnasConnectHelper import unasGetProdsLiveFull as getProds

#import  xmlclazz.pepitaTypes as PT

YAML_CONFIG_FILE = 'pepitaProxy.yaml'

xaa=''' ### gondoltam hatha XSD-vel jobb lenne
import urllib.request
##from xmlschema import XMLSchema, etree_tostring
def loadXsd(url:str):
    #url = "https://example.com/textfile.txt"
    response = urllib.request.urlopen(url)
    data = response.read()
    print(data)
    return data

def validateXml(xml:str):
    xmlDoc = ET.fromstring(xml.encode())
    # Load the XSD file
    xsd_file = getConf("pepitaXsdFile", "pepita")
    with open(xsd_file, 'rb') as schema_file:
        xmlschema_doc = ET.parse(schema_file)
        schema = ET.XMLSchema(xmlschema_doc)
        if schema.validate(xmlDoc):
            print("XML is valid.")
        else:
            print("XML is invalid.")
            print(schema.error_log)
'''
def xmlToProductList(xml:str):
    pppList = []
    xmlDoc = ET.fromstring(xml.encode())
    
    ppp = objectify.fromstring(xml.encode())
    for prodItem in ppp.findall("Product"):
        pppList.append(prodItem)
    return pppList

def getSymbolVat(p) -> float:
    # priceStr = FB.getPriceBySku(sku)
    return 0  if p  is None else  p.Vat.text.replace("%", "")


def getProdz(limitStart:int) -> list:
    prodXml = getProds("live", limitStart, MU.Conf("pepita.productLimitNum"))
    prodz = xmlToProductList(prodXml)
    return [] # prodz

#def findParamById( prms : list[PT.Param]) -> str:
def findParamById( prms : list, _id : int) -> str:
    for p in prms:
        if _id == p.Id:
            return p.Value
    return ""

#def createXmlFromUnas( prodList : list[PT.Product]) -> str:
def createXmlFromUnas( prodList : list) -> str:
    xml = ""
    for prod in prodList:
        xml += f'<Product>{createXml(prod)}</Product>'
    return xml # f'<Catalog xmlns="https://pepita.hu/feed/1.0">{xml}</Catalog>'

#def createXml( p : PT.Product  ) -> str:
def createXml( p ) -> str:
    return f'''
<Id>{p.Sku}</Id>
<LastMod>{p.LastModTime}</LastMod>
<StructuredId>{"Hianyzo-EAN" if p.find("Params") is None else findParamById(p.Params.findall("Param"), 555093)}</StructuredId>
<ProductNumber>{p.Sku}</ProductNumber>
<Descriptions>
    <Name><![CDATA[{p.Name}]]></Name>
    <Brand>{"-" if p.find("Params") is None else findParamById(p.Params.findall("Param"), 555069)}</Brand>
    <Description>
        <![CDATA[{"" if p.find("Description") is None or p.find("Description").find("Short") is None else p.Description.Short}]]>
    </Description>
</Descriptions>
<Categories>{"" if p.find("Categories") is None else getCategories(p.Categories.findall("Category"))}</Categories>
<Prices>
    <Currency>HUF</Currency>
    <Price>{MU.getSymbolPrice(p.Sku)}</Price>
    <VatPercent>{getSymbolVat(p.Prices)}</VatPercent>
</Prices>
<Photos>{ "" if p.find("Images") is None else getPhotos(p.Images.findall("Image"))}</Photos>
<Availability>
    <Available>{ "false" if p.find("Stocks") is None or p.Stocks.find("Status") is None or 1 != p.Stocks.Status.Active else "true"}</Available>
    <Quantity>{0 if p.find("Stocks") is None or p.Stocks.find("Stock") is None  else p.Stocks.Stock.Qty }</Quantity>
</Availability>
{ "" if p.find("Params") is None else getAttribs(p.Params.findall("Param"))}
'''

#def getAttribs(params : list[PT.Param]) -> str :
def getAttribs(params : list) -> str :
    xml = ""
    for prm in params:
        if prm.Id != 555093 and prm.Id != 555069 and "symbolId" != prm.Name:
            xml += f"""
    <Attribute>
        <AttributeName><![CDATA[{prm.Name}]]></AttributeName>
        <AttributeValue>{prm.Value}</AttributeValue>
    </Attribute>
    """
    return "" if len(xml) < 1 else "<Attributes>" + xml + "</Attributes>"

#def getPhotos(images : list [PT.Image]) -> str :
def getPhotos(images : list ) -> str : 
    xml = ""
    for img in images:
        xml += f'''
<Photo>
    <Url>{img.Url.Medium}</Url>
    <IsPrimary>{ "true" if img.Type == "base" else "false"}</IsPrimary>
</Photo>
'''
    return xml

def getCategories(categories : list ) -> str : 
    xml = ""
    for cat in categories:
        catzz = cat.Name.text.split("|")
        for c in catzz:
            xml += f'<Category><Name><![CDATA[{c}]]></Name></Category>'
    return xml


def createPepitaProductXml(limitNum:int, fn:str):
    # GET products from UNAS
    idx = 0
    if os.path.exists(fn):
        os.remove(fn)
    with open(fn, 'w') as f:
        f.write(MU.XMLTAG)
        f.write('<Catalog xmlns="https://pepita.hu/feed/1.0">')
        while True:
            products = getProdz(idx)
            pepitaXml = createXmlFromUnas(products)
            f.write(pepitaXml)
            #
            print(f"processed {idx} + {len(products)}")
            if len(products) < limitNum:
                break
            idx += limitNum
        #
        f.write('</Catalog>')
    MU.getLogger().logger.info(f"processed {idx + len(products)} product records")

def savePepitaOrders(queryParams, post_data) -> tuple[bool, str] :
    isError = False
    msg = ""
    
    with open(f"{MU.Conf("pepita.folder.save")}/{MU.getCurrTime()}.json.bin", "wb") as fp:
        fp.write( post_data )

    try:
        # check API key
        if len(queryParams) > 0 and len(queryParams['apikey'])==1:
            if MU.Conf("pepita.apikey") != queryParams['apikey'][0]:
                raise Exception(f"Bad API key: {queryParams['apikey']}")
        # JSON to PepitaOrderCache
        pcc = MU.putPepitaOrderIntoCache(post_data.decode())
        if MU.isLogLevelTrace():
            print(pcc)
    except Exception as eee:
        isError = True
        msg = f'"{eee}"'
    return isError, msg

def batchDoIt():
    limitNum = int(str(MU.Conf("pepita.productLimitNum") or '0'))
    fn = str(MU.Conf("pepita.resultPath") or 'PepitaUtils-batchDoIt')
    createPepitaProductXml(int(limitNum), fn or 'x')


#*********************************
#  TODO Tesztelni, hogy ugyanazt csinalja-e, mint a pepi2!!!
#*********************************
if __name__ == "__main__":
    configPath = YAML_CONFIG_FILE

    if (len(sys.argv)>1):
        configPath = sys.argv[1]
    config = MU.readYaml(configPath)
    limitNum = int(str(MU.Conf("pepita.productLimitNum", config) or '0')) # type: ignore
    fn = str(MU.Conf("pepita.resultPath", config) or 'PepitaUtils-batchDoIt') # type: ignore
    createPepitaProductXml(int(limitNum), fn or 'x')
