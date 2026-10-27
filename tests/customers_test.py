import unittest
#from tests.mods.myDemoCalc import Calculations

from tests.mods.testUtils import unasApiWrapper, MU
from xmlclazz.unasCustomer import UnasCustomers

class CustomerTest(unittest.TestCase):

    #def test_sum(self):
    #    pass
        #calculation = Calculations(8, 2)
        #self.assertEqual(calculation.get_sum(), 10, 'The sum is wrong.')

    def getAllCustomer_test(self):
        # csak a szama erdekeljen?
        xmlReq = ''
        '''<?xml version="1.0" encoding="UTF-8" ?>
<Params>
    <StatusBase>1</StatusBase>
    <LimitNum>50</LimitNum>
    <LimitStart>20</LimitStart>
    <ContentType>full</ContentType>
</Params>'''
        resp = unasApiWrapper('getCustomer', '')
        custs = UnasCustomers.from_xml(MU.ET.fromstring(resp))
        self.assertEqual(len(custs.customers), 379, 'Customers count valtozott?')

#    def addCustomer_test(self):
#        # Crealok egy XML-t ra
#        pass
#    
#    def getCustomer_test(self):
#        # Az eppen felvittet - ossze lehet hasonlitani
#        pass
#
#    def modCustomer_test(self):
#        # Email - Tiltott, Lakcim - engedelyezett? Nev,Telszam
#        pass
#
#    def delCustomer_test(self):
#        pass
#
#    def groupCustomer_test(self):
#        # Default, R2, F5, EGYEDI(hibas), R3, default
#        pass

if __name__ == '__main__':
    unittest.main()