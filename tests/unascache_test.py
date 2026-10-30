import unittest
from tests.mods.testUtils import MU, doUnasGetRequest


class UnasCacheTest(unittest.TestCase):

    def test_load(self):
        MU.loadCacheStateDB()
        print(MU.UnasOrderList, MU.UnasProductList, MU.UnasCustomerList)

    def test_save(self):
        MU.saveCacheStateDB()
        print('resp')

    def test_refresh_customerCache(self):
        resp = MU.getUnasActiveCustomers()
        print(resp)
        MU.saveCacheStateDB(MU.MUT.ProxyObjectType.CUSTOMER)
        MU.loadCacheStateDB(MU.MUT.ProxyObjectType.CUSTOMER)

    def test_refresh_productCache(self):
        resp = MU.getUnasProductParted(25, contentType='full')
        print(resp)
        MU.saveCacheStateDB(MU.MUT.ProxyObjectType.CUSTOMER)
        MU.loadCacheStateDB(MU.MUT.ProxyObjectType.CUSTOMER)


    def test_refresh_orderCache(self):
        resp = doUnasGetRequest(['x','unas','proxycontrol', 'ord', 'loadcache'], [])
        print(resp)
        MU.saveCacheStateDB(MU.MUT.ProxyObjectType.ORDER)
        MU.loadCacheStateDB(MU.MUT.ProxyObjectType.ORDER)


if __name__ == '__main__':
    unittest.main()