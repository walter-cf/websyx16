import unittest
import requests

from UnasConnectHelper import unasCustomer_Direct
from PostProcessorUNAS import getErrorTextCustomer
#from xmlclazz.unasCustomer import UnasCustomers, UnasCustomer
from xmlclazz.symb.customers2 import Customers, Customer


class CustomerSymbol:

    def changeCustomerCategory(self, cat:str|None):
        pass

    def getCustomerById(self, unasId:int) -> Customer:
        cust:Customer = Customer()
        return cust

class CustomerOffersTestCases(unittest.TestCase):
    # cust Cats
    # from R5 -> R1, EGYEDI
    def changeCustomerCategory(self):
        for symbolCat in ('R5','R4','R3','R2','R1',None, 'EGYEDI', 'KamuValami'):
            CustomerSymbol.changeCustomerCategory(CustomerSymbol(), cat=symbolCat)

    def offerCreate(self):
        for symbolCat in ('R5','R4','R3','R2','R1',None, 'EGYEDI', 'KamuValami'):
            CustomerSymbol.changeCustomerCategory(CustomerSymbol(), cat=symbolCat)

    def offerCustomer(self):
        # customer.priceCat changed to EGYEDI
        for symbolCat in ('R5','R4','R3','R2','R1',None, 'EGYEDI', 'KamuValami'):
            CustomerSymbol.changeCustomerCategory(CustomerSymbol(), cat=symbolCat)

if __name__ == '__main__':
    unittest.main()