import unittest
#from tests.mods.myDemoCalc import Calculations

class PriceTest(unittest.TestCase):

    def test_sum(self):
        pass
        #calculation = Calculations(8, 2)
        #self.assertEqual(calculation.get_sum(), 10, 'The sum is wrong.')

    def addCustomer_test(self):
        # Crealok egy XML-t ra
        pass

    def modCustomer_test(self):
        # Email - Tiltott, Lakcim - engedelyezett? Nev,Telszam
        pass

    def delCustomer_test(self):
        pass

    def groupCustomer_test(self):
        # Default, R2, F5, EGYEDI(hibas), R3, default
        pass

if __name__ == '__main__':
    unittest.main()