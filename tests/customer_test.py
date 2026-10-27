import unittest
#from tests.mods.myDemoCalc import Calculations

from tests.mods.testUtils import unasApiWrapper, createDemoCustomer, MU
# from xmlclazz.customerResponse import CustomerResponse
from xmlclazz.unasCustomer2 import Customers as UnasCustomers, Customer as UnasCustomer, Contact as UnasCustomerContact

class CustomTest(unittest.TestCase):

    def test_getAllCustomer(self):
        # csak a szama erdekeljen?
        xmlReq = ''
        '''<?xml version="1.0" encoding="UTF-8" ?>
<Params>
    <StatusBase>1</StatusBase>
    <LimitNum>50</LimitNum>
    <LimitStart>20</LimitStart>
    <ContentType>full</ContentType>
</Params>'''
        resp = unasApiWrapper('getCustomer', '<Params />')
        custs = UnasCustomers.from_xml(MU.ET.fromstring(resp.replace(MU.XMLTAG, '')))
        self.assertEqual(len(custs.customers), 9, 'Customers count valtozott?')

    def test_addCustomer(self):
        # Crealok egy XML-t ra
        resp = createDemoCustomer()
        self.assertEqual('OK', resp)
    
    def test_getCustomer(self):
        resp = unasApiWrapper('getCustomer', '<Params><Email>unittest@ledsound.hu</Email></Params>')
        custs = UnasCustomers.from_xml(MU.ET.fromstring(resp.replace(MU.XMLTAG, '')))
        cust = custs.customers[0]
        self.assertGreater(cust.id, 0)
        self.assertEqual('unittest@ledsound.hu', cust.email)

    def test_modCustomer(self):
        resp = unasApiWrapper('getCustomer', '<Params><Email>unittest@ledsound.hu</Email></Params>')
        custs = UnasCustomers.from_xml(MU.ET.fromstring(resp.replace(MU.XMLTAG, '')))
        cust = custs.customers[0]
        if cust.contact is None:
            cust.contact = UnasCustomerContact(None, 'Test Contact Modified Name') 
        else:
            cust.contact.name = 'Test Contact Modified Name'
        #
        xml = UnasCustomer.to_xml_string(cust)
        resp = MU.UCH.unasCustomer_Direct(xml.replace(MU.XMLTAG, ''))
        #unasApiWrapper('setCustomer', f'{MU.XMLTAG}<Customers>{xml}</Customers>')
        print(resp)

    def test_delCustomer(self):
        pass

    def test_groupCustomer(self):
        # Default, R2, F5, EGYEDI(hibas), R3, default
        pass

if __name__ == '__main__':
    unittest.main()