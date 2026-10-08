import unittest

from googletrans import Translator, constants
from pprint import pprint

class PepitaTest(unittest.TestCase):

    def test_1(self):
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


if __name__ == '__main__':
    unittest.main()