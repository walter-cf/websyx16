from dataclasses import dataclass, field
from typing import List, Optional, Union
import xml.etree.ElementTree as ET
from datetime import datetime

@dataclass
class Id:
    id: int = 0

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Id':
        """Create Id instance from XML element."""
        return cls(
            id=cls._parse_id(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Id instance to XML element."""
        element = ET.Element('Id')
        self._serialize_id(element)
        return element
    @staticmethod
    def _parse_id(element: ET.Element) -> int:
        """Parse Id from XML element."""
        if element is not None and element.text:
            return int(element.text)
        return 0
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            elem = ET.SubElement(parent, 'Id')
            elem.text = str(self.id)


@dataclass
class Name:
    name: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Name':
        """Create Name instance from XML element."""
        return cls(
            name=cls._parse_name(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Name instance to XML element."""
        element = ET.Element('Name')
        self._serialize_name(element)
        return element
    @staticmethod
    def _parse_name(element: ET.Element) -> str|None:
        """Parse Name from XML element."""
        #elem = element.find('Name')
        if element is not None and element.text:
            return element.text
        return None
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            elem = ET.SubElement(parent, 'Name')
            elem.text = str(self.name)



@dataclass
class Sku:
    sku: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Sku':
        """Create Name instance from XML element."""
        return cls(
            # sku=cls._parse_name(element)
            sku=cls._parse_name(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Name instance to XML element."""
        element = ET.Element('Name')
        self._serialize_name(element)
        return element
    @staticmethod
    def _parse_name(element: ET.Element) -> str|None:
        """Parse Name from XML element."""
        #elem = element.find('Sku')
        if element is not None and element.text:
            return element.text
        return None
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.sku is not None:
            elem = ET.SubElement(parent, 'Name')
            elem.text = str(self.sku)



@dataclass
class UnasProduct:
    id: Optional['Id'] = None
    sku: Optional['Sku'] = None
    name: Optional['Name'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'UnasProduct':
        """Create Product instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            sku=cls._parse_sku(element),
            name=cls._parse_name(element),
        )

    @staticmethod
    def _parse_id(element: ET.Element) -> Optional['Id']:
        """Parse Id from XML element."""
        child = element.find('Id')
        if child is not None:
            return Id.from_element(child)
        return None
    @staticmethod
    def _parse_sku(element: ET.Element) -> Optional['Sku']:
        """Parse Sku from XML element."""
        child = element.find('Sku')
        if child is not None:
            return Sku.from_element(child)
        return None
    @staticmethod
    def _parse_name(element: ET.Element) -> Optional['Name']:
        """Parse Sku from XML element."""
        child = element.find('Name')
        if child is not None:
            return Name.from_element(child)
        return None

    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_sku(self, parent: ET.Element) -> None:
        """Serialize sku to XML element."""
        if self.sku is not None:
            parent.append(self.sku.to_element())

    def to_element(self) -> ET.Element:
        """Convert Product instance to XML element."""
        element = ET.Element('Product')
        self._serialize_id(element)
        self._serialize_sku(element)
        self._serialize_name(element)
        return element



@dataclass
class UnasProducts:
    products: List['UnasProduct'] = field( default_factory=list)

    @classmethod
    def from_xml_string(cls, xml_string: str) -> List['UnasProduct']:
        """Parse XML string and create Products instance."""
        root = ET.fromstring(xml_string)
        prods = cls([])
        for prod in root.findall('Product'):
            prods.products.append(UnasProduct.from_element(prod))
        return prods.products
    
    @classmethod
    def from_element(cls, element: ET.Element) -> 'UnasProducts':
        """Create Products instance from XML element."""
        return cls(
            products=cls._parse_product(element)
        )
    
    def to_xml_string(self) -> str:
        """Convert Products instance to XML string."""
        root = self.to_element()
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    
    def to_element(self) -> ET.Element:
        """Convert Products instance to XML element."""
        element = ET.Element('Products')
        self._serialize_product(element)
        return element

    @staticmethod
    def _parse_product(element: ET.Element) -> List['UnasProduct']:
        """Parse Product from XML element."""
        prods = []
        for child in element.findall('Product'):
            prods.append( UnasProduct.from_element(child) )
        return prods
    def _serialize_product(self, parent: ET.Element) -> None:
        """Serialize product to XML element."""
        if self.products is not None:
            parent.append(self.to_element())


