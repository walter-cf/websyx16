import unittest

import asyncio
from googletrans import Translator, constants
import MyUtils as MU

from pprint import pprint

class I18n_Text1(unittest.TestCase):

    def test_Egy1(self):
        # init the Google API translator
        translator = Translator()

        # translate a spanish text to english text (by default)
        translation = translator.translate("Hola Mundo", src='sp', dest='en')
        #print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
        tTxt = 'Szörnyű idő, szörnyű idő s a szörnyűség mindegyre nő'
        translation = translator.translate(tTxt, dest='ru')
        #print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
        print(f"{translation}")
        # self.assertEqual(calculation.get_sum(), 10, 'The sum is wrong.')

    def test_i2(self):
        async def translate_text():
            resp = []
            #async with Translator( service_urls=[ 'translate.google.com', 'translate.google.co.hu' ])  as translator:
            async with Translator()  as translator:
                result = await translator.translate('Hi Brooo!', src='ru', dest='hu')
                print(result)  # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
                print(result.text)  # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
            return resp
        
        result = asyncio.run(translate_text())
        print(result)

    def test_i3(self):
        async def translate_text():
            resp = []
            async with Translator(
                        service_urls=[
                            'translate.google.com',
                            'translate.google.co.kr'
                            ])  as translator:
                result = await translator.translate('안녕하세요.', src='ko')
                print(result)  # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
                print(result.text)  # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
                resp.append(result.text)
                result = await translator.translate('안녕하세요.', src='ko', dest='ja')
                print(result)  # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
                print(result.text)  # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
                resp.append(result.text)
                result = await translator.translate('veritas lux mea', src='la')
                print(result)  # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>
                print(result.text)  # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
                resp.append(result.text)
            return resp
        
        result = asyncio.run(translate_text())
        print(result)


if __name__ == '__main__':
    unittest.main()