#
# https://jsontotable.org/xml-to-python
# 
from dataclasses import dataclass, field
from typing import List, Optional, Any
import xml.etree.ElementTree as ET

@dataclass
class Product:
    id: int = 0  # XML element: id
    code: str|None = None  # XML element: code
    webdisplay: int = 0  # XML element: webdisplay
    webname: str|None = None  # XML element: webname
    webdescription: str|None = None  # XML element: webdescription
    webmetadescription: str|None = None  # XML element: webmetadescription
    weburl: str|None = None  # XML element: weburl
    webkeywords: str|None = None  # XML element: webkeywords
    feedbackurl: str|None = None  # XML element: feedbackurl
    errorurl: str|None = None  # XML element: errorurl

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Product':
        instance = cls()
        id_elem = xml_element.find('id')
        if id_elem is not None:
            instance.id = int(id_elem.text or 0)
        code_elem = xml_element.find('code')
        if code_elem is not None:
            instance.code = code_elem.text
        webdisplay_elem = xml_element.find('webdisplay')
        if webdisplay_elem is not None:
            instance.webdisplay = int(webdisplay_elem.text or 0)
        webname_elem = xml_element.find('webname')
        if webname_elem is not None:
            instance.webname = webname_elem.text
        webdescription_elem = xml_element.find('webdescription')
        if webdescription_elem is not None:
            instance.webdescription = webdescription_elem.text
        webmetadescription_elem = xml_element.find('webmetadescription')
        if webmetadescription_elem is not None:
            instance.webmetadescription = webmetadescription_elem.text
        weburl_elem = xml_element.find('weburl')
        if weburl_elem is not None:
            instance.weburl = weburl_elem.text
        webkeywords_elem = xml_element.find('webkeywords')
        if webkeywords_elem is not None:
            instance.webkeywords = webkeywords_elem.text
        feedbackurl_elem = xml_element.find('feedbackurl')
        if feedbackurl_elem is not None:
            instance.feedbackurl = feedbackurl_elem.text
        errorurl_elem = xml_element.find('errorurl')
        if errorurl_elem is not None:
            instance.errorurl = errorurl_elem.text
        return instance

@dataclass
class Products:
    product: List[Product] = field(default_factory=list)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Products':
        instance = cls()
        product_elements = xml_element.findall('Product')
        instance.product = [Product.from_xml(elem) for elem in product_elements]
        return instance
