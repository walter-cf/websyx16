from typing import List, Dict, Optional, Any, cast as Cast
from MyUtils import Conf as MuConf
from translate import Translator
import xmlclazz.symb.products2 as PROD

def translateWith(trx:Translator, txt:str) -> str:
    return trx.translate(txt)

def createTranslator(toLang:str, fromLang:str='hu') -> Translator:
    secret = MuConf("secrets.deepl")
    return Translator(provider='deepl', to_lang=toLang, from_lang=fromLang, secret_access_key=secret)

class ProductText():
    prod: PROD.Product|None
    #LANGS:List
    trx:Translator
    
    def __init__(self, symbolProduct:PROD.Product|None=None, fromLang='hu', toLang='en'):
        self.prod = symbolProduct
        secret = MuConf("secrets.deepl")
        self.trx = Translator(provider='deepl', to_lang=toLang, from_lang=fromLang, secret_access_key=secret)
        #self.LANGS = Cast(List, MuConf("unas.web.langs"))

    def translateToAllLangs(self, txt:str) -> Dict[str, str]:
        translated: Dict = {}
        for lang in MuConf("unas.web.langs") or []:
            translated[lang] = self.translateFromHu(txt, lang)
        return translated

    def translateFromHu(self, txt:str, lang:str) -> str:
        self.trx.to_lang = lang
        return self.trx.translate(txt)

    def translateText(self, txt:str) -> str:
        return self.trx.translate(txt)
