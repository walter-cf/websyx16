from dataclasses import dataclass, field
from typing import List, Optional, Any
import xml.etree.ElementTree as ET

@dataclass
class Product:
    id: int | None = None  # XML element: Id
    sku: str | None = None  # XML element: SKU / cikkszam
    action: str | None = None  # XML element: Action
    status: str | None = None  # XML element: Status
    error: str | None = None  # XML element: Status

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Product':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = 0 if id_elem.text is None else int(id_elem.text)
        action_elem = xml_element.find('Action')
        if action_elem is not None:
            instance.action = action_elem.text
        sku_elem = xml_element.find('Sku')
        if sku_elem is not None:
            instance.sku = sku_elem.text
        status_elem = xml_element.find('Status')
        if status_elem is not None:
            instance.status = status_elem.text
        error_elem = xml_element.find('Error')
        if error_elem is not None:
            instance.error = error_elem.text
        return instance

@dataclass
class ProductResponse:
    products: List[Product] = field( default_factory=list)

    def from_xmlStr(self, xmlStr) -> List[Product]:
        prods : List[Product] = []
        cgs = ET.fromstring(xmlStr)
        for prod in cgs.findall("Product"):
            prods.append(Product.from_xml(prod))
        return prods
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'ProductResponse':
        instance = cls()
        product_elements = xml_element.findall('Product')
        instance.products = [Product.from_xml(elem) for elem in product_elements]
        return instance
