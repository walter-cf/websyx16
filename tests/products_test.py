import unittest
from tests.mods.testUtils import unasApiWrapper, getProductBySku

xml = '''<Products>
<Product>
    <Action>modify</Action>
    <Sku>%s</Sku>
	<Prices>
        <Price>
            <Type>special</Type>
            <Gross>%s</Gross>
            <Currency>%s</Currency>
            <CurrencyFilter>%s</CurrencyFilter>
        </Price>
    </Prices>
</Product>
</Products>
'''

xml2 = '''<Products>
<Product>
    <Action>modify</Action>
    <Sku>%s</Sku>
	<Prices>
        <Price>
            <Type>special</Type>
            <Gross>%s</Gross>
            <Currency>%s</Currency>
            <CurrencyFilter>%s</CurrencyFilter>
            <AreaName>%s</AreaName>
        </Price>
    </Prices>
</Product>
</Products>
'''

class ProductTest(unittest.TestCase):
    PRODUCT_SKU = "PT-6445"

    def test_getProduct0(self):
        xmlParam = f'<Params><Sku>{self.PRODUCT_SKU}</Sku><ContentType>full</ContentType></Params>'
        resp = unasApiWrapper('getProduct', xmlParam)
        print(resp)

    def test_getProduct1(self):
        resp = getProductBySku(self.PRODUCT_SKU)
        print(resp)

    def test_getProductAll(self):
        xmlParam = f'<Params><State>live</State><ContentType>minimal</ContentType></Params>'
        resp = unasApiWrapper('getProduct', xmlParam)
        print(resp)

    
    def test_i18nPrices(self):
        # resp =  unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 96 * 127 / 127, 'HUF', 'HUF' ))
        # resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 16 * 127 / 118, 'USD', 'USD' ))
        # resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 26 * 127 / 118, 'EUR', 'EUR' ))
        # resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 36 * 127 / 118, 'RON', 'RON' ))
        # resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 46 * 127 / 117, 'EUR', 'EUR' ))
        # resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 56 * 127 / 123, 'PLN', 'PLN' ))
        # resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 66 * 127 / 121, 'CZK', 'CZK' ))
        # resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 76 * 127 / 117, 'BGN', 'BGN' ))
        # resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 86 * 127 / 122, 'MDL', 'MDL' ))
        resp =  unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 96                 , 'HUF', 'HUF' ))
        resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 16 * 1.076271186440, 'USD', 'USD' ))
        resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 26 * 1.076271186440, 'EUR', 'EUR' ))
        resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 36 * 1.076271186440, 'RON', 'RON' ))
        resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 46 * 1.076271186440, 'EUR', 'EUR' ))
        resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 56 * 1.076271186440, 'PLN', 'PLN' ))
        resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 66 * 1.076271186440, 'CZK', 'CZK' ))
        resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 76 * 1.076271186440, 'BGN', 'BGN' ))
        resp += unasApiWrapper('setProduct', xml % (self.PRODUCT_SKU, 86 * 1.076271186440, 'MDL', 'MDL' ))
        print(resp)

    def test_i18nPricesArea(self):
        resp =  unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 96 * 127 / 127, 'HUF', 'HUF', 'Budapest' ))
        resp += unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 16 * 127 / 118, 'USD', 'USD', 'Amerika'  ))
        resp += unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 26 * 127 / 118, 'EUR', 'EUR', 'Berlin'   ))
        resp += unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 36 * 127 / 118, 'RON', 'RON', 'Bukarest' ))
        resp += unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 46 * 127 / 117, 'EUR', 'EUR', 'Pozsony'  ))
        resp += unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 56 * 127 / 123, 'PLN', 'PLN', 'Varso'    ))
        resp += unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 66 * 127 / 121, 'CZK', 'CZK', 'Praga'    ))
        resp += unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 76 * 127 / 117, 'BGN', 'BGN', 'Szofia'   ))
        resp += unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 86 * 127 / 122, 'MDL', 'MDL', 'Kisinyov' ))
        print(resp)

    def NU_i18nPricesArea(self):
        resp = unasApiWrapper('setProduct', xml2 % (self.PRODUCT_SKU, 96 / 1.27, 96, 'HUF',  'Budapest' ))
        print(resp)


    def test_i18nPricesUniq(self):
        sku = self.PRODUCT_SKU
        xmlU = f'''<Products><Product><Action>add</Action><Sku>{sku}</Sku><Prices><Price><Type>special</Type>
                        <AreaName>Bukarest</AreaName>
                        <Gross>{999*127/118}</Gross>
                        <Currency>RON</Currency>
                        <CurrencyFilter>RON</CurrencyFilter>
                    </Price>
                </Prices>
            </Product>
            </Products>
            '''
        resp = unasApiWrapper('setProduct', xmlU)
        print(resp)

if __name__ == '__main__':
    unittest.main()