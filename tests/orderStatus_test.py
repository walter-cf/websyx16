import unittest

from tests.mods.testUtils import MU, unasSetOrderStatus, unasOrder_Direct, doUnasRequest, doUnasGetRequest, webControlCDN
from FdbUtils import getField, getRow
from xmlclazz.unasPostResponse import UnasResponse
from typing import List, Optional, Union

class OrderStatusTest(unittest.TestCase):

    def test_loadUnasCache(self):
        doUnasGetRequest(['x','unas','proxycontrol', 'ord', 'loadcache'], [])
        #print(resp)

    def test_Xml1(self):
        ordKey = '76172-100001'
        for ordStatus in MU.Conf("unas.order.statusNames") or []:
            xmlOrd = '<Order><Action>modify</Action><Key>%s</Key><Status><![CDATA[%s]]></Status><StatusEmail>%s</StatusEmail></Order>'''
            xmlResp = unasOrder_Direct(xmlOrd % ( f'{ordKey}', ordStatus[1], 'no' ))
            print (xmlResp)
            resp = UnasResponse.from_xmlstr_byTag(xmlResp, 'Order')
            self.assertEqual('ok', resp[0].status)

    def test_Xml2(self):
        ordKey = '76172-100001'
        for ordStatus in MU.Conf("unas.order.statusNames") or []:
            symbolId = getField('select "Id" from "CustomerOrder" where "PrimeVoucherNumber" = ?', (f'H24-{ordKey}', ))
            xmlResp = unasSetOrderStatus( ordKey,  ordStatus[0], symbolId)
            print (xmlResp)
            resp : List[UnasResponse] = UnasResponse.from_xmlstr_byTag(xmlResp, 'Order')
            self.assertEqual('ok', resp[0].status)

    def test_Xml3(self):
        ordKey = '76172-100001'
        invoiceStatus = '2'
        invoiceNumber = 'H24INV-1'
        invoiceURL = 'https://cdn.ledsound.hu/xx/222'
        #ordStatus = 'Megrendelés lezárva'
        ordStatus = next((x[1] for x in MU.Conf("unas.order.statusNames") or [] if x[0] == 'Closed'), 'Megrendelés lezárva' )
        xmlOrd = f'''<Order><Action>modify</Action><Key>{ordKey}</Key><Status><![CDATA[{ordStatus}]]></Status><Invoice>
                <Status>{invoiceStatus}</Status>
                <Number>{invoiceNumber}</Number>
                <Url>{invoiceURL}</Url>
                </Invoice></Order>'''
        xmlResp = unasOrder_Direct(xmlOrd)
        print (xmlResp)
        resp = UnasResponse.from_xmlstr_byTag(xmlResp, 'Order')
        self.assertEqual('ok', resp[0].status)

    def test_symbolCall(self):
        key1, status1, key2, status2, key3, status3 = ('76172-100001','Szedhető','76172-100002','Számlázható','76172-100003','Új rendelés')
        xml = xmlSymbolTest_1 % (key1, status1, key2, status2, key3, status3)
        resp = doUnasRequest('changedorderstatus', postData=xml)
        print(resp)
        self.assertEqual('OK', resp)

    def NOtest_proxyControlGetOrders(self):
        #resp = doUnasGetRequest(['x','unas','proxycontrol', 'ord', 'loadcache'], [])
        #print(resp)
        resp = doUnasGetRequest(['x','unas','proxycontrol', 'ord', 'getnew'], [])
        print(resp)
        resp = doUnasGetRequest(['x','unas','proxycontrol', 'ord', 'getnewjs'], [])
        print(resp)
        resp = doUnasGetRequest(['x','unas','proxycontrol', 'ord', 'getall'], [])
        print(resp)
        resp = doUnasGetRequest(['x','unas','proxycontrol', 'ord', 'getalljs'], [])
        print(resp)
    
    def test_symbolCall2(self):
        resp = doUnasGetRequest(['x','unas','proxycontrol', 'ord', 'loadcache'], [])
        print(resp)
        with open('tests/xml/symbol/changeOrderStatus1.xml') as xml:
            resp = doUnasRequest('changedorderstatus', postData=xml.read())
            print(resp)
            self.assertEqual('OK', resp)

    def test_setFeldolgozando(self):
        webstoreOrderKey = MU.Conf("unas.order.storekey")
        feldolgozasraVar = MU.Conf("unas.order.status.new")
        for ordkey in [1, 2, 3, 4, 5, 6, 7]:
            xmlOrd = '<Order><Action>modify</Action><Key>%s</Key><Status>%s</Status><StatusEmail>%s</StatusEmail></Order>'''
            xmlResp = unasOrder_Direct(xmlOrd % ( f'{webstoreOrderKey}-{100000 + ordkey}', feldolgozasraVar, 'no' ))
            print (xmlResp)
            resp = UnasResponse.from_xmlstr_byTag(xmlResp, 'Order')
            self.assertEqual('ok', resp[0].status)

    def test_fulfilled(self):
        webstoreOrderKey = MU.Conf("unas.order.storekey")
        teljesitve = MU.Conf("unas.order.status.closed")
        for ordkey in [1, 2, 3]:
            xmlOrd = '<Order><Action>modify</Action><Key>%s</Key><Status>%s</Status><StatusEmail>%s</StatusEmail></Order>'''
            xmlResp = unasOrder_Direct(xmlOrd % ( f'H24-{webstoreOrderKey}-{100000 + ordkey}', teljesitve, 'no' ))
            print (xmlResp)
            resp = UnasResponse.from_xmlstr_byTag(xmlResp, 'Order')
            self.assertEqual('ok', resp[0].status)

    def test_fulfilleSymbolXml(self):
        # orderFulfilled1
        confOrderRoot = MU.Conf("unas.order") or {}
        webstoreOrderKey = MU.Conf("storekey", confOrderRoot)
        ordkey = 1
        xml =  xmlFulfilledSymbolTest_1 % ( f'{MU.Conf("symbolOrderPrefix", confOrderRoot)}-{webstoreOrderKey}-{100000 + ordkey}')
        resp = doUnasRequest('fulfilled', xml)
        print(resp)
        self.assertEqual('OK', resp)

    def test_OrderInvoicePdfList(self):
        res = MU.FBU.getOrderInvoiceByDirectIds([2022, 2033])
        print(res)
        webstoreOrderKey = MU.Conf("unas.order.storekey")
        for ordkey in [1, 2, 3]:
            res = MU.FBU.getOrderInvoicePdfList( f'H24-{webstoreOrderKey}-{100000 + ordkey}' ) or []
            print(ordkey, res)

    def test_getInvoicepdfByControlSocket(self):
        pdfData, contentType = webControlCDN(['web6invoice', 'ea3b89e7-2aac-49f2-92c1-575f10c4aac1','y2R475'], None)
        print(contentType)
        # check hasPdfSignature? 
        self.assertEqual(b'PDF-1.4', pdfData[1:8])

    def test_X9(self):
        pass
    def test_XA(self):
        pass
    def test_XB(self):
        pass

xmlFulfilledSymbolTest_1 = '''<FulfilledCustomerOrdersByInvoice xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <CustomerOrder>
    <Id>3633</Id>
    <VoucherNumber>REW2026/00430</VoucherNumber>
    <PrimeVoucherNumber>%s</PrimeVoucherNumber>
    <VoucherSequenceCode>B2B</VoucherSequenceCode>
  </CustomerOrder>
</FulfilledCustomerOrdersByInvoice>
'''

xmlSymbolTest_1 = '''<?xml version="1.0" encoding="UTF-8" ?>
<CustomerOrderStatuses>
    <CustomerOrder>
        <Id>9999991</Id>
        <VoucherNumber>REW2026/00002</VoucherNumber>
                <PrimeVoucherNumber>H24-%s</PrimeVoucherNumber>
                <VoucherSequenceCode>H24</VoucherSequenceCode>
                <CustomerOrderStatus>1</CustomerOrderStatus>
                <CustomerOrderStatusName>%s</CustomerOrderStatusName>
    </CustomerOrder>
    <CustomerOrder>
        <Id>9999992</Id>
        <VoucherNumber>REW2026/00002</VoucherNumber>
                <PrimeVoucherNumber>H24-%s</PrimeVoucherNumber>
                <VoucherSequenceCode>H24</VoucherSequenceCode>
                <CustomerOrderStatus>1</CustomerOrderStatus>
                <CustomerOrderStatusName>%s</CustomerOrderStatusName>
    </CustomerOrder>
    <CustomerOrder>
        <Id>9999992</Id>
        <VoucherNumber>REW2026/00003</VoucherNumber>
                <PrimeVoucherNumber>H24-%s</PrimeVoucherNumber>
                <VoucherSequenceCode>H24</VoucherSequenceCode>
                <CustomerOrderStatus>1</CustomerOrderStatus>
                <CustomerOrderStatusName>%s</CustomerOrderStatusName>
    </CustomerOrder>
</CustomerOrderStatuses>
'''

xmlOrdSample = '''
<Orders> 
    <Order> 
        <Action>add</Action>  		
        <Date>2022.03.12 10:00:00</Date>		
        <Lang>hu</Lang> 
        <Customer>
            <Id>100000</Id> 
            <Email>unas@unas.hu</Email> 
            <Username></Username> 
            <Contact> 
                <Name><![CDATA[Kis János]]></Name> 
                <Phone><![CDATA[+3699111111]]></Phone> 
                <Mobile><![CDATA[+36301111111]]></Mobile> 
            </Contact>
            <Addresses> 
                <Invoice> 
                    <Name><![CDATA[Teszt János]]></Name> 
                    <ZIP>1111</ZIP> 
                    <City><![CDATA[Teszt Város]]></City> 
                    <Street><![CDATA[Tej út 2.]]></Street> 
                    <StreetName><![CDATA[Tej]]></StreetName> 
                    <StreetType><![CDATA[út]]></StreetType> 
                    <StreetNumber><![CDATA[2]]></StreetNumber> 
                    <County><![CDATA[]]></County> 
                    <Country>Magyarország</Country> 
                    <CountryCode>hu</CountryCode> 
                    <TaxNumber><![CDATA[12345678-9-00]]></TaxNumber> 
                    <EUTaxNumber><![CDATA[HU0123456789]]></EUTaxNumber> 
                    <CustomerType><![CDATA[private]]></CustomerType> 
                </Invoice>
                <Shipping> 
                    <Name><![CDATA[Teszt János]]></Name> 
                    <ZIP>2222</ZIP> 
                    <City><![CDATA[Teszt Város]]></City> 
                    <Street><![CDATA[Tej út 10.]]></Street> 
                    <StreetName><![CDATA[Tej]]></StreetName> 
                    <StreetType><![CDATA[út]]></StreetType> 
                    <StreetNumber><![CDATA[10]]></StreetNumber> 
                    <County><![CDATA[]]></County> 
                    <Country>Magyarország</Country> 
                    <CountryCode>hu</CountryCode> 
                    <DeliveryPointID>157547</DeliveryPointID> 
                    <DeliveryPointGroup>gls_api_dropoffpoints</DeliveryPointGroup> 
                    <DeliveryPointSubGroup>csomagautomata</DeliveryPointSubGroup> 
                    <RecipientName>Teszt János</RecipientName> 
                </Shipping>
            </Addresses>			
            <Comment><![CDATA[Megjegyzés]]></Comment> 		
        </Customer>
        <Currency>HUF</Currency> 		
        <Payment> 
            <Id>100</Id> 
            <Name><![CDATA[Utalás]]></Name> 
            <Type>transfer</Type>			
        </Payment>
        <Shipping> 
            <Id>200</Id> 
            <Name><![CDATA[Futárszolgálat]]></Name> 
            <PackageNumber><![CDATA[PUDO123456789]]></PackageNumber>			
        </Shipping>
        <Invoice> 
            <Status>1</Status> 
            <StatusText><![CDATA[Számlázható]]></StatusText> 			
        </Invoice>
        <Params> 
            <Param> 
                <Id>1000</Id> 
                <Name><![CDATA[Kérdés1]]></Name> 
                <Value><![CDATA[Válasz1]]></Value> 
            </Param>
            <Param> 
                <Id>2000</Id>
                <Name><![CDATA[Kérdés2]]></Name>
                <Value><![CDATA[Válasz2]]></Value>
            </Param>
        </Params>		
        <Coupon><![CDATA[f6zhr48jd]]></Coupon> 
        <Weight>10.5</Weight>		
        <Comments> 
            <Comment>
                <Type>customer</Type> 
                <Text><![CDATA[A vásárló megjegyzése]]></Text> 
            </Comment>
        </Comments>
        <SumPriceGross>12700</SumPriceGross> 
        <Items> 
            <Item> 
                <Id>1000</Id> 
                <Sku>Cikkszam1</Sku> 
                <Name><![CDATA[Termék név 1]]></Name> 
                <Unit>db</Unit> 
                <Quantity>10</Quantity> 
                <PriceNet>1000</PriceNet> 
                <PriceGross>1270</PriceGross> 
                <Vat>27%</Vat> 
                <Status><![CDATA[Holnap érkezik]]></Status>				
            </Item>			
        </Items>
    </Order>	
</Orders>'''

if __name__ == '__main__':
    unittest.main()