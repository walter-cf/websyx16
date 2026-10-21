import unittest

from deep_translator import GoogleTranslator as GT


class I18n_Text2(unittest.TestCase):

    def test_Egy1(self):

        proxies_example = {
                "https": "34.195.196.27:8080",
                "http": "34.195.196.27:8080"
            }
        translated = GT(source='auto', target='de', proxies=proxies_example).translate("keep it up, you are awesome")  # output -> Weiter so, du bist großartig
        print(translated)
        self.assertIsNotNone(translated)


if __name__ == '__main__':
    unittest.main()