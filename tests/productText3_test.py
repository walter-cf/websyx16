from typing import Dict
import unittest
from translate import Translator
from mods.testUtils import unasProduct_Direct, MU
from I18nDeepL import ProductText, PROD


langs = ['ru','en','de','ro','cs','sk','sl','bg' ]

class I18n_Text3(unittest.TestCase):

    def test_Egy1(self):
        secret = '9183b874-d880-406f-904d-66fab48d20d6:fx'
        for lang in langs:
            trx = Translator(provider='deepl', from_lang='hu', to_lang=lang, secret_access_key=secret)
            translated = trx.translate("Hű de szép egy cicamica!")
            print(lang,translated)
            self.assertIsNotNone(translated)

    @staticmethod
    def createProduct_1() -> PROD.Product:
        p = PROD.Product()
        p.id = PROD.Id(-1)
        p.code = PROD.Code('PT-6381')
        p.name = 'Termék valódi neve'
        p.webdescription = PROD.Webdescription('Termék valódi WEB-neve')
        p.webkeywords = PROD.Webkeywords('Termék valódi kulcsszavai')
        p.webmetadescription = PROD.Webmetadescription('Termék valódi META leírása ')
        p.webname = PROD.Webname('Termék valódi WEB-en használt neve')
        p.weburl = PROD.Weburl('Termék valódi neveből képzett URL')
        return p

    @staticmethod
    def createProduct_2(sku:str) -> Dict[str, str]:
        return MU.FBU.getRow('select * from "Product" where "Code" = ?', (sku,))

    @classmethod
    def translate(cls, trx:Translator, txt:str, fromLang:str, toLang:str) -> PROD.Product:
        trx.to_lang = toLang
        translated = trx.translate(txt)
        print(toLang, translated)
        cls.assertIsNotNone(translated)
        return translated

    def test_unasLangsCapa(self):
        with open('tests/xml/unasSetProdText.xml') as fxml:
            xml = fxml.read()
            xmlReq = xml % ('PT-6381', 'de', 'Unbekannt produkt name, schade!', 'kurze deskription', 'Lange deskription')
            xmlReq += xml % ('PT-6381', 'ro', 'Unbekannt produkt name, schade!', 'kurze deskription', 'Lange deskription')
            xmlReq += xml % ('PT-6381', 'cz', 'Unbekannt produkt name, schade!', 'kurze deskription', 'Lange deskription')
            resp = unasProduct_Direct(xmlReq)
            print(resp)
            self.assertIsNotNone(resp)
            self.assertIn('<Status>ok</Status>', resp)

    def test_ProductText(self):
        prod  = self.createProduct_2()
        PT: ProductText = ProductText(symbolProduct=prod,fromLang='hu')
        trTxts = PT.translateToAllLangs()
        self.assertIsNotNone(trTxts)
        self.assertEqual(10, len(trTxts), 'Nincs meg mindegyik LANG?')

'''
    def test_ProductTextByProduct(self):
        self.assertIsNotNone(translated)

    def test_ProductTextByProductAllLang(self):
        self.assertIsNotNone(translated)
'''

if __name__ == '__main__':
    print('Ez akkor most begyutt ide is?')
    unittest.main()