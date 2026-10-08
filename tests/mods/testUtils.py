import MyUtils as MU
#import lxml.etree as ET
from GetProcessor import doUnasGetRequest
from PostProcessorUNAS import doUnasRequest
from xmlclazz.unasCustomer import UnasCustomer
from xmlclazz.customerResponse import CustomerResponse
from UnasConnectHelper import unasCustomer_Direct, unasFreeXml, unasProduct_Direct, getProds as getProductBy

def getCustomerById(unasId:int) -> CustomerResponse:
    resp = doUnasGetRequest(['x','customerby','customerby','Id',f'{unasId}'],[])
    return CustomerResponse.from_xml(MU.ET.fromstring(resp))

def setCustomerCategoryById(cat :str, unasId:int) -> CustomerResponse:
    with open('tests/xml/symbol/chgDemoCustomerCategory.xml', 'mode', encoding='utf-8') as fil:
        demoXml = fil.read()
        resp = doUnasRequest('customer', demoXml % (unasId, cat))
        return CustomerResponse.from_xml(MU.ET.fromstring(resp))

def createDemoCustomer() -> CustomerResponse:
    with open('tests/xml/symbol/createDemoCustomer.xml', 'r', encoding='utf-8') as fil:
        demoXml = fil.read()
        resp = doUnasRequest('customer', demoXml)
        return CustomerResponse.from_xml(MU.ET.fromstring(resp))

def getProductBySku(sku:str) -> str:
    resp = getProductBy('Sku', sku)
    return resp

def unasApiWrapper(action:str, xml:str) -> str:
    resp = unasFreeXml(action, xml)
    return resp

def unasApiSetProdict(xml:str) -> str:
    resp = unasProduct_Direct(xml)
    return resp

class MyServerConnector():
    serverPort = 3346
    serverHost = '192.168.10.6'

    def GET(self, path:str, qry:str|None=None) -> str:
        queryStr = '' if qry is None else f'?{qry}'
        API_URL = f"http://{self.serverHost}:{self.serverPort}/{path}{queryStr}"
        response = requests.get('API_URL')
        return response.text

    def POST(self, path:str, postData:str, qry:str|None=None) -> str:
        queryStr = '' if qry is None else f'?{qry}'
        API_URL = f"http://{self.serverHost}:{self.serverPort}/{path}{queryStr}"
        response = requests.post(API_URL, data=postData)
        return response.text    

