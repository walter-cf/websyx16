from dataclasses import dataclass, field
from typing import List, Optional, Union
import xml.etree.ElementTree as ET
from datetime import datetime

@dataclass
class Contact:
    name   : str|None = None
    phone  : str|None = None
    mobile : str|None = None
    lang   : str|None = None


    @classmethod
    def from_xml_string(cls, xml_string: str) -> 'Contact':
        root = ET.fromstring(xml_string)
        return cls.from_element(root)
    @classmethod
    def from_element(cls, element: ET.Element) -> 'Contact':
        return cls(
            name          = cls._parse_stritem(element, 'Name'         ),
            phone         = cls._parse_stritem(element, 'Phone'        ),
            mobile        = cls._parse_stritem(element, 'Mobile'       ),
            lang          = cls._parse_stritem(element, 'Lang'         ),
        )
    def to_xml_string(self) -> str:
        """Convert Customer instance to XML string."""
        root = self.to_element()
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    def to_element(self) -> ET.Element:
        """Convert Invoice instance to XML element."""
        element = ET.Element('Contact')
        self._serialize_stritem(element, 'Name'    , self.name       )
        self._serialize_stritem(element, 'Phone'   , self.phone      )
        self._serialize_stritem(element, 'Mobile'  , self.mobile     )
        self._serialize_stritem(element, 'Lang'    , self.lang       )
        return element

    @staticmethod
    def _parse_stritem(element, itemName:str) -> str|None:
        elem = element.find(itemName)
        if elem is not None:
            return elem.text
        return None
    @staticmethod
    def _serialize_stritem(parent, itemName, itemValue) -> str|None:
        if itemValue is not None:
            elem = ET.SubElement(parent, itemName)
            elem.text = str(itemValue)

@dataclass
class Address:
    name: str|None = None
    zip:  str|None = None
    city:  str|None = None
    street:  str|None = None
    street_name:  str|None = None
    street_number:  str|None = None
    county:  str|None = None
    country:  str|None = None
    country_code:  str|None = None
    tax_number:  str|None = None
    eu_tax_number:  str|None = None
    tax_free:  str|None = None

    @classmethod
    def from_xml_string(cls, xml_string: str) -> 'Address':
        root = ET.fromstring(xml_string)
        return cls.from_element(root)
    @classmethod
    def from_element(cls, element: ET.Element) -> 'Address':
        return cls(
            name          = cls._parse_stritem(element, 'Name'           ),
            zip           = cls._parse_stritem(element, 'ZIP'            ),
            city          = cls._parse_stritem(element, 'City'           ),
            street        = cls._parse_stritem(element, 'Street'         ),
            street_name   = cls._parse_stritem(element, 'StreetName'     ),
            street_number = cls._parse_stritem(element, 'StreeNumber'    ),
            county        = cls._parse_stritem(element, 'County'         ),
            country       = cls._parse_stritem(element, 'Country'        ),
            country_code  = cls._parse_stritem(element, 'CountryCode'    ),
            tax_number    = cls._parse_stritem(element, 'TaxNumber'      ),
            eu_tax_number = cls._parse_stritem(element, 'EuTaxNumber'    ),
            tax_free      = cls._parse_stritem(element, 'TaxFree'        ),
        )
    def to_xml_string(self) -> str:
        """Convert Customer instance to XML string."""
        root = self.to_element()
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    def to_element(self) -> ET.Element:
        """Convert Invoice instance to XML element."""
        element = ET.Element('Address')
        self._serialize_stritem(element, 'Name'       , self.name            )
        self._serialize_stritem(element, 'ZIP'        , self.zip             )
        self._serialize_stritem(element, 'City'       , self.city            )
        self._serialize_stritem(element, 'Street'     , self.street          )
        self._serialize_stritem(element, 'StreetName' , self.street_name     )
        self._serialize_stritem(element, 'StreeNumber', self.street_number   )
        self._serialize_stritem(element, 'County'     , self.county          )
        self._serialize_stritem(element, 'Country'    , self.country         )
        self._serialize_stritem(element, 'CountryCode', self.country_code    )
        self._serialize_stritem(element, 'TaxNumber'  , self.tax_number      )
        self._serialize_stritem(element, 'EuTaxNumber', self.eu_tax_number   )
        self._serialize_stritem(element, 'TaxFree'    , self.tax_free        )
        return element

    @staticmethod
    def _parse_stritem(element, itemName:str) -> str|None:
        elem = element.find(itemName)
        if elem is not None:
            return elem.text
        return None
    
    @staticmethod
    def _serialize_stritem(parent, itemName, itemValue) -> str|None:
        if itemValue is not None:
            elem = ET.SubElement(parent, itemName)
            elem.text = str(itemValue)

@dataclass
class Addresses:
    invoice: Optional['Address'] = None
    shipping: Optional['Address'] = None

    @classmethod
    def from_xml_string(cls, xml_string: str) -> 'Addresses':
        root = ET.fromstring(xml_string)
        return cls.from_element(root)
    @classmethod
    def from_element(cls, element: ET.Element) -> 'Addresses':
        return cls(
            invoice=cls._parse_invoice(element),
            shipping=cls._parse_shipping(element),
        )

    def to_element(self) -> ET.Element:
        """Convert Customer instance to XML element."""
        element = ET.Element('Customer')
        self._serialize_invoice(element)
        self._serialize_shipping(element)
        return element

    @staticmethod
    def _parse_invoice(element: ET.Element) -> Optional[Address]:
        """Parse Id from XML element."""
        child = element.find('Id')
        if child is not None:
            return Address.from_element(child)
        return None
    @staticmethod
    def _parse_shipping(element: ET.Element) -> Optional[Address]:
        """Parse Email from XML element."""
        child = element.find('Email')
        if child is not None:
            return Address.from_element(child)
        return None

    def _serialize_invoice(self, parent: ET.Element) -> None:
        """Serialize authorize to XML element."""
        if self.invoice is not None:
            parent.append(self.invoice.to_element())
    def _serialize_shipping(self, parent: ET.Element) -> None:
        """Serialize authorize to XML element."""
        if self.shipping is not None:
            parent.append(self.shipping.to_element())

@dataclass
class Group:
    id: int|None
    name: str|None = None

    @classmethod
    def from_xml_string(cls, xml_string: str) -> 'Group':
        """Parse XML string and create Customer instance."""
        root = ET.fromstring(xml_string)
        return cls.from_element(root)

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Group':
        """Create Customer instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            name=cls._parse_name(element),
        )
    @staticmethod
    def _parse_id(element: ET.Element) -> int|None:
        """Parse Id from XML element."""
        child = element.find('Id')
        if child is not None:
            return int(str(child.text))
        return None
    @staticmethod
    def _parse_name(element: ET.Element) -> str|None:
        """Parse Email from XML element."""
        child = element.find('Name')
        if child is not None:
            return child.text
        return None
    
    # serialize Group
    def to_xml_string(self) -> str:
        """Convert Customer instance to XML string."""
        root = self.to_element()
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    def to_element(self) -> ET.Element:
        """Convert Customer instance to XML element."""
        element = ET.Element('Group')
        self._serialize_id(element)
        self._serialize_name(element)
        return element
    # serialize Simple Strings
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None and self.id > 0:
            elem = ET.SubElement(parent, 'Id')
            elem.text = str(self.id)
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize email to XML element."""
        if self.name is not None:
            elem = ET.SubElement(parent, 'Name')
            elem.text = str(self.name)
    
@dataclass
class Authorize:
    customer:str|None
    admin:str|None

    @classmethod
    def from_xml_string(cls, xml_string: str) -> 'Authorize':
        """Parse XML string and create Customer instance."""
        root = ET.fromstring(xml_string)
        return cls.from_element(root)
    @classmethod
    def from_element(cls, element: ET.Element) -> 'Authorize':
        """Create Customer instance from XML element."""
        return cls(
            customer=cls._parse_customer(element),
            admin=cls._parse_admin(element)
        )
    
    def to_xml_string(self) -> str:
        """Convert Customer instance to XML string."""
        root = self.to_element()
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    
    def to_element(self) -> ET.Element:
        """Convert Customer instance to XML element."""
        element = ET.Element('Customer')
        self._serialize_customer(element)
        self._serialize_admin(element)
        return element

    @staticmethod
    def _parse_customer(element: ET.Element) -> str|None:
        """Parse Email from XML element."""
        child = element.find('Customer')
        if child is not None:
            return child.text
        return None
    @staticmethod
    def _parse_admin(element: ET.Element) -> str|None:
        """Parse Email from XML element."""
        child = element.find('Admin')
        if child is not None:
            return child.text
        return None

    def _serialize_customer(self, parent: ET.Element) -> None:
        """Serialize email to XML element."""
        if self.customer is not None:
            elem = ET.SubElement(parent, 'Customer')
            elem.text = str(self.customer)
    def _serialize_admin(self, parent: ET.Element) -> None:
        """Serialize username to XML element."""
        if self.admin is not None:
            elem = ET.SubElement(parent, 'Admin')
            elem.text = str(self.admin)

@dataclass
class Customer:
    id: int  = 0
    email: str|None = None
    username: str|None = None
    contact: Optional['Contact'] = None
    addresses: Optional['Addresses'] = None
    group: Optional['Group'] = None
    authorize: Optional['Authorize'] = None
#    dates: Optional['Dates'] = None
#    discount: Optional['Discount'] = None
#    points_account: Optional['Pointsaccount'] = None
#    newsletter: Optional['Newsletter'] = None
#    others: Optional['Others'] = None

    @classmethod
    def from_xml_string(cls, xml_string: str) -> 'Customer':
        """Parse XML string and create Customer instance."""
        root = ET.fromstring(xml_string)
        return cls.from_element(root)
    @classmethod
    def from_element(cls, element: ET.Element) -> 'Customer':
        """Create Customer instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            email=cls._parse_email(element),
            username=cls._parse_username(element),
            contact=cls._parse_contact(element),
            addresses=cls._parse_addresses(element),
            group=cls._parse_group(element),
            authorize=cls._parse_authorize(element),
        )
    
    def to_xml_string(self) -> str:
        """Convert Customer instance to XML string."""
        root = self.to_element()
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    
    def to_element(self) -> ET.Element:
        """Convert Customer instance to XML element."""
        element = ET.Element('Customer')
        self._serialize_id(element)
        self._serialize_email(element)
        self._serialize_username(element)
        self._serialize_contact(element)
        self._serialize_addresses(element)
        self._serialize_group(element)
        self._serialize_authorize(element)
        #
        #self._serialize_dates(element)
        #self._serialize_discount(element)
        #self._serialize_points_account(element)
        #self._serialize_newsletter(element)
        #self._serialize_others(element)
        return element

    def to_element_groupName(self, grpName):
        self.group = Group(None, grpName)

    @staticmethod
    def _parse_id(element: ET.Element) -> int:
        """Parse Id from XML element."""
        child = element.find('Id')
        if child is not None:
            return int(child.text or '0')
        return 0
    @staticmethod
    def _parse_email(element: ET.Element) -> str|None:
        """Parse Email from XML element."""
        child = element.find('Email')
        if child is not None:
            return child.text
        return None
    @staticmethod
    def _parse_username(element: ET.Element) -> str|None:
        """Parse Username from XML element."""
        child = element.find('Username')
        if child is not None:
            return child.text
        return None
    @staticmethod
    def _parse_contact(element: ET.Element) -> Optional['Contact']:
        """Parse Contact from XML element."""
        child = element.find('Contact')
        if child is not None:
            return Contact.from_element(child)
        return None
    @staticmethod
    def _parse_addresses(element: ET.Element) -> Optional['Addresses']:
        """Parse Addresses from XML element."""
        child = element.find('Addresses')
        if child is not None:
            return Addresses.from_element(child)
        return None
    @staticmethod
    def _parse_group(element: ET.Element) -> Optional['Group']:
        """Parse Group from XML element."""
        child = element.find('Group')
        if child is not None:
            return Group.from_element(child)
        return None
    @staticmethod
    def _parse_authorize(element: ET.Element) -> Optional['Authorize']:
        """Parse Authorize from XML element."""
        child = element.find('Authorize')
        if child is not None:
            return Authorize.from_element(child)
        return None

    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None and self.id > 0:
            elem = ET.SubElement(parent, 'Id')
            elem.text = str(self.id)

    def _serialize_email(self, parent: ET.Element) -> None:
        """Serialize email to XML element."""
        if self.email is not None:
            elem = ET.SubElement(parent, 'Email')
            elem.text = str(self.email)
    def _serialize_username(self, parent: ET.Element) -> None:
        """Serialize username to XML element."""
        if self.username is not None:
            elem = ET.SubElement(parent, 'Username')
            elem.text = str(self.email)
    def _serialize_contact(self, parent: ET.Element) -> None:
        """Serialize contact to XML element."""
        if self.contact is not None:
            parent.append(self.contact.to_element())
    def _serialize_addresses(self, parent: ET.Element) -> None:
        """Serialize addresses to XML element."""
        if self.addresses is not None:
            parent.append(self.addresses.to_element())
    def _serialize_group(self, parent: ET.Element) -> None:
        """Serialize group to XML element."""
        if self.group is not None:
            parent.append(self.group.to_element())
    def _serialize_authorize(self, parent: ET.Element) -> None:
        """Serialize authorize to XML element."""
        if self.authorize is not None:
            parent.append(self.authorize.to_element())

@dataclass
class Customers:
    customers: List[Customer] = field( default_factory=list)
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customers':
        instance = cls()
        elements = xml_element.findall('Customer')
        instance.customers = [Customer.from_element(elem) for elem in elements]
        return instance
