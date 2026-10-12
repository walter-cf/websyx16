from typing import List, Dict, Optional
from MyUtils import Conf as MuConf
from translate import Translator
import xmlclazz.symb.products2 as PROD

class ProductText():
    prod: PROD.Product
    LANGS:List
    trx:Translator
    
    def __init__(self, symbolProduct:PROD.Product, fromLang='hu'):
        self.prod = symbolProduct
        secret = MuConf("secrets.deepl")
        self.trx = Translator(provider='deepl', from_lang=fromLang, secret_access_key=secret)
        self.LANGS:List = MuConf("unas.web.langs") or []

    def translateToAllLangs(self, txt:str) -> Dict[str, str]:
        translated: Dict = {}
        for lang in MuConf("unas.web.langs"):
            translated[lang] = self.translateFromHu(txt, lang)
        return translated

    
    def translateFromHu(self, txt:str, lang:str) -> str:
        self.trx.to_lang = lang
        return self.trx.translate(txt)
