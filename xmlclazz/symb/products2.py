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
        element = ET.Element('id')
        self._serialize_id(element)
        return element
    @staticmethod
    def _parse_id(element: ET.Element) -> int:
        """Parse id from XML element."""
        elem = element.find('id')
        if elem is not None and elem.text:
            return int(elem.text or 0)
        return 0
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            elem = ET.SubElement(parent, 'id')
            elem.text = str(self.id)


@dataclass
class Code:
    code: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Code':
        """Create Code instance from XML element."""
        return cls(
            code=cls._parse_code(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Code instance to XML element."""
        element = ET.Element('code')
        self._serialize_code(element)
        return element
    @staticmethod
    def _parse_code(element: ET.Element) -> str|None:
        """Parse code from XML element."""
        elem = element.find('code')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_code(self, parent: ET.Element) -> None:
        """Serialize code to XML element."""
        if self.code is not None:
            elem = ET.SubElement(parent, 'code')
            elem.text = str(self.code)


@dataclass
class Webdisplay:
    webdisplay: int = 0

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Webdisplay':
        """Create Webdisplay instance from XML element."""
        return cls(
            webdisplay=cls._parse_webdisplay(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Webdisplay instance to XML element."""
        element = ET.Element('webdisplay')
        self._serialize_webdisplay(element)
        return element
    @staticmethod
    def _parse_webdisplay(element: ET.Element) -> int:
        """Parse webdisplay from XML element."""
        elem = element.find('webdisplay')
        if elem is not None and elem.text:
            return int(elem.text or 0)
        return 0
    def _serialize_webdisplay(self, parent: ET.Element) -> None:
        """Serialize webdisplay to XML element."""
        if self.webdisplay is not None:
            elem = ET.SubElement(parent, 'webdisplay')
            elem.text = str(self.webdisplay)


@dataclass
class Webname:
    webname: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Webname':
        """Create Webname instance from XML element."""
        return cls(
            webname=cls._parse_webname(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Webname instance to XML element."""
        element = ET.Element('webname')
        self._serialize_webname(element)
        return element
    @staticmethod
    def _parse_webname(element: ET.Element) -> str|None:
        """Parse webname from XML element."""
        elem = element.find('webname')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_webname(self, parent: ET.Element) -> None:
        """Serialize webname to XML element."""
        if self.webname is not None:
            elem = ET.SubElement(parent, 'webname')
            elem.text = str(self.webname)


@dataclass
class Webdescription:
    webdescription: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Webdescription':
        """Create Webdescription instance from XML element."""
        return cls(
            webdescription=cls._parse_webdescription(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Webdescription instance to XML element."""
        element = ET.Element('webdescription')
        self._serialize_webdescription(element)
        return element
    @staticmethod
    def _parse_webdescription(element: ET.Element) -> str|None:
        """Parse webdescription from XML element."""
        elem = element.find('webdescription')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_webdescription(self, parent: ET.Element) -> None:
        """Serialize webdescription to XML element."""
        if self.webdescription is not None:
            elem = ET.SubElement(parent, 'webdescription')
            elem.text = str(self.webdescription)


@dataclass
class Webmetadescription:
    webmetadescription: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Webmetadescription':
        """Create Webmetadescription instance from XML element."""
        return cls(
            webmetadescription=cls._parse_webmetadescription(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Webmetadescription instance to XML element."""
        element = ET.Element('webmetadescription')
        self._serialize_webmetadescription(element)
        return element
    @staticmethod
    def _parse_webmetadescription(element: ET.Element) -> str|None:
        """Parse webmetadescription from XML element."""
        elem = element.find('webmetadescription')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_webmetadescription(self, parent: ET.Element) -> None:
        """Serialize webmetadescription to XML element."""
        if self.webmetadescription is not None:
            elem = ET.SubElement(parent, 'webmetadescription')
            elem.text = str(self.webmetadescription)


@dataclass
class Weburl:
    weburl: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Weburl':
        """Create Weburl instance from XML element."""
        return cls(
            weburl=cls._parse_weburl(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Weburl instance to XML element."""
        element = ET.Element('weburl')
        self._serialize_weburl(element)
        return element
    @staticmethod
    def _parse_weburl(element: ET.Element) -> str|None:
        """Parse weburl from XML element."""
        elem = element.find('weburl')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_weburl(self, parent: ET.Element) -> None:
        """Serialize weburl to XML element."""
        if self.weburl is not None:
            elem = ET.SubElement(parent, 'weburl')
            elem.text = str(self.weburl)


@dataclass
class Webkeywords:
    webkeywords: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Webkeywords':
        """Create Webkeywords instance from XML element."""
        return cls(
            webkeywords=cls._parse_webkeywords(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Webkeywords instance to XML element."""
        element = ET.Element('webkeywords')
        self._serialize_webkeywords(element)
        return element
    @staticmethod
    def _parse_webkeywords(element: ET.Element) -> str|None:
        """Parse webkeywords from XML element."""
        elem = element.find('webkeywords')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_webkeywords(self, parent: ET.Element) -> None:
        """Serialize webkeywords to XML element."""
        if self.webkeywords is not None:
            elem = ET.SubElement(parent, 'webkeywords')
            elem.text = str(self.webkeywords)


@dataclass
class Feedbackurl:
    feedbackurl: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Feedbackurl':
        """Create Feedbackurl instance from XML element."""
        return cls(
            feedbackurl=cls._parse_feedbackurl(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Feedbackurl instance to XML element."""
        element = ET.Element('feedbackurl')
        self._serialize_feedbackurl(element)
        return element
    @staticmethod
    def _parse_feedbackurl(element: ET.Element) -> str|None:
        """Parse feedbackurl from XML element."""
        elem = element.find('feedbackurl')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_feedbackurl(self, parent: ET.Element) -> None:
        """Serialize feedbackurl to XML element."""
        if self.feedbackurl is not None:
            elem = ET.SubElement(parent, 'feedbackurl')
            elem.text = str(self.feedbackurl)


@dataclass
class Errorurl:
    errorurl: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Errorurl':
        """Create Errorurl instance from XML element."""
        return cls(
            errorurl=cls._parse_errorurl(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Errorurl instance to XML element."""
        element = ET.Element('errorurl')
        self._serialize_errorurl(element)
        return element
    @staticmethod
    def _parse_errorurl(element: ET.Element) -> str|None:
        """Parse errorurl from XML element."""
        elem = element.find('errorurl')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_errorurl(self, parent: ET.Element) -> None:
        """Serialize errorurl to XML element."""
        if self.errorurl is not None:
            elem = ET.SubElement(parent, 'errorurl')
            elem.text = str(self.errorurl)


@dataclass
class Product:
    id: Optional['Id'] = None
    code: Optional['Code'] = None
    webdisplay: Optional['Webdisplay'] = None
    webname: Optional['Webname'] = None
    webdescription: Optional['Webdescription'] = None
    webmetadescription: Optional['Webmetadescription'] = None
    weburl: Optional['Weburl'] = None
    webkeywords: Optional['Webkeywords'] = None
    feedbackurl: Optional['Feedbackurl'] = None
    errorurl: Optional['Errorurl'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Product':
        """Create Product instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            code=cls._parse_code(element),
            webdisplay=cls._parse_webdisplay(element),
            webname=cls._parse_webname(element),
            webdescription=cls._parse_webdescription(element),
            webmetadescription=cls._parse_webmetadescription(element),
            weburl=cls._parse_weburl(element),
            webkeywords=cls._parse_webkeywords(element),
            feedbackurl=cls._parse_feedbackurl(element),
            errorurl=cls._parse_errorurl(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Product instance to XML element."""
        element = ET.Element('Product')
        self._serialize_id(element)
        self._serialize_code(element)
        self._serialize_webdisplay(element)
        self._serialize_webname(element)
        self._serialize_webdescription(element)
        self._serialize_webmetadescription(element)
        self._serialize_weburl(element)
        self._serialize_webkeywords(element)
        self._serialize_feedbackurl(element)
        self._serialize_errorurl(element)
        return element
    @staticmethod
    def _parse_id(element: ET.Element) -> Optional['Id']:
        """Parse id from XML element."""
        child = element.find('id')
        if child is not None:
            return Id.from_element(child)
        return None
    @staticmethod
    def _parse_code(element: ET.Element) -> Optional['Code']:
        """Parse code from XML element."""
        child = element.find('code')
        if child is not None:
            return Code.from_element(child)
        return None
    @staticmethod
    def _parse_webdisplay(element: ET.Element) -> Optional['Webdisplay']:
        """Parse webdisplay from XML element."""
        child = element.find('webdisplay')
        if child is not None:
            return Webdisplay.from_element(child)
        return None
    @staticmethod
    def _parse_webname(element: ET.Element) -> Optional['Webname']:
        """Parse webname from XML element."""
        child = element.find('webname')
        if child is not None:
            return Webname.from_element(child)
        return None
    @staticmethod
    def _parse_webdescription(element: ET.Element) -> Optional['Webdescription']:
        """Parse webdescription from XML element."""
        child = element.find('webdescription')
        if child is not None:
            return Webdescription.from_element(child)
        return None
    @staticmethod
    def _parse_webmetadescription(element: ET.Element) -> Optional['Webmetadescription']:
        """Parse webmetadescription from XML element."""
        child = element.find('webmetadescription')
        if child is not None:
            return Webmetadescription.from_element(child)
        return None
    @staticmethod
    def _parse_weburl(element: ET.Element) -> Optional['Weburl']:
        """Parse weburl from XML element."""
        child = element.find('weburl')
        if child is not None:
            return Weburl.from_element(child)
        return None
    @staticmethod
    def _parse_webkeywords(element: ET.Element) -> Optional['Webkeywords']:
        """Parse webkeywords from XML element."""
        child = element.find('webkeywords')
        if child is not None:
            return Webkeywords.from_element(child)
        return None
    @staticmethod
    def _parse_feedbackurl(element: ET.Element) -> Optional['Feedbackurl']:
        """Parse feedbackurl from XML element."""
        child = element.find('feedbackurl')
        if child is not None:
            return Feedbackurl.from_element(child)
        return None
    @staticmethod
    def _parse_errorurl(element: ET.Element) -> Optional['Errorurl']:
        """Parse errorurl from XML element."""
        child = element.find('errorurl')
        if child is not None:
            return Errorurl.from_element(child)
        return None
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_code(self, parent: ET.Element) -> None:
        """Serialize code to XML element."""
        if self.code is not None:
            parent.append(self.code.to_element())
    def _serialize_webdisplay(self, parent: ET.Element) -> None:
        """Serialize webdisplay to XML element."""
        if self.webdisplay is not None:
            parent.append(self.webdisplay.to_element())
    def _serialize_webname(self, parent: ET.Element) -> None:
        """Serialize webname to XML element."""
        if self.webname is not None:
            parent.append(self.webname.to_element())
    def _serialize_webdescription(self, parent: ET.Element) -> None:
        """Serialize webdescription to XML element."""
        if self.webdescription is not None:
            parent.append(self.webdescription.to_element())
    def _serialize_webmetadescription(self, parent: ET.Element) -> None:
        """Serialize webmetadescription to XML element."""
        if self.webmetadescription is not None:
            parent.append(self.webmetadescription.to_element())
    def _serialize_weburl(self, parent: ET.Element) -> None:
        """Serialize weburl to XML element."""
        if self.weburl is not None:
            parent.append(self.weburl.to_element())
    def _serialize_webkeywords(self, parent: ET.Element) -> None:
        """Serialize webkeywords to XML element."""
        if self.webkeywords is not None:
            parent.append(self.webkeywords.to_element())
    def _serialize_feedbackurl(self, parent: ET.Element) -> None:
        """Serialize feedbackurl to XML element."""
        if self.feedbackurl is not None:
            parent.append(self.feedbackurl.to_element())
    def _serialize_errorurl(self, parent: ET.Element) -> None:
        """Serialize errorurl to XML element."""
        if self.errorurl is not None:
            parent.append(self.errorurl.to_element())


@dataclass
class Productsdown:
    product_list: List['Product'] = field(default_factory=list)

    @classmethod
    def from_xml_string(cls, xml_string: str) -> 'Productsdown':
        """Parse XML string and create Productsdown instance."""
        root = ET.fromstring(xml_string)
        return cls.from_element(root)
    
    @classmethod
    def from_element(cls, element: ET.Element) -> 'Productsdown':
        """Create Productsdown instance from XML element."""
        return cls(
            product_list=cls._parse_product_list(element)
        )
    
    def to_xml_string(self) -> str:
        """Convert Productsdown instance to XML string."""
        root = self.to_element()
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    
    def to_element(self) -> ET.Element:
        """Convert Productsdown instance to XML element."""
        element = ET.Element('ProductsDown')
        self._serialize_product_list(element)
        return element
    @staticmethod
    def _parse_product_list(element: ET.Element) -> List['Product']:
        """Parse Product list from XML element."""
        children = element.findall('Product')
        return [Product.from_element(child) for child in children]
    def _serialize_product_list(self, parent: ET.Element) -> None:
        """Serialize product_list list to XML elements."""
        for item in self.product_list:
            parent.append(item.to_element())
