import unittest
import requests

from UnasConnectHelper import unasCustomer_Direct
from PostProcessorUNAS import getErrorTextCustomer

class CustomerSymbol:

    def changeCustomerCategory(self, cat:str|None):
        pass

class CustomerOffersTestCases(unittest.TestCase):
    # cust Cats
    # from R5 -> R1, EGYEDI
    def changeCustomerCategory(self):
        for symbolCat in ('R5','R4','R3','R2','R1',None, 'EGYEDI', 'KamuValami'):
            CustomerSymbol.changeCustomerCategory(CustomerSymbol(), cat=symbolCat)

if __name__ == '__main__':
    unittest.main()