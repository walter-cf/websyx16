import unittest
import requests

from UnasConnectHelper import unasCustomer_Direct
from PostProcessorUNAS import getErrorTextCustomer

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

class Customers(unittest.TestCase):

    def test_addCustomer(self, xmlFn='customerAdd-1'):
        with open(f'tests/xml/unas/{xmlFn}.xml', 'r') as xf:
            content = ''.join(xf.readlines()).replace('\n','')
            resp = unasCustomer_Direct(xml=content)
            result = getErrorTextCustomer('customer', resp)
            self.assertIsNone(result)

    def test_changeCustomer(self, xmlFn='customerAdd-1'):
        with open(f'tests/xml/unas/{xmlFn}.xml', 'r') as xf:
            content = ''.join(xf.readlines()).replace('\n','')
            resp = unasCustomer_Direct(xml=content)
            result = getErrorTextCustomer('customer', resp)
            self.assertIsNone(result)

'''
class TestMath(unittest.TestCase):
    def test_addition(self):
        print('Hello world')
        self.assertEqual(2 + 2, 4)

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2) # type: ignore
'''

#if __name__ == '__main__':
#    unittest.main()