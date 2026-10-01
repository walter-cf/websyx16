from dataclasses import dataclass, field
from typing import List, Optional, Union
import xml.etree.ElementTree as ET
from datetime import datetime


@dataclass
class Customerstatus:
    customerstatus: int = 0

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Customerstatus':
        """Create Customerstatus instance from XML element."""
        return cls(
            customerstatus=cls._parse_customerstatus(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Customerstatus instance to XML element."""
        element = ET.Element('customerstatus')
        self._serialize_customerstatus(element)
        return element
    @staticmethod
    def _parse_customerstatus(element: ET.Element) -> int:
        """Parse customerstatus from XML element."""
        elem = element.find('customerstatus')
        if elem is not None and elem.text:
            return int(elem.text)
        return 0
    def _serialize_customerstatus(self, parent: ET.Element) -> None:
        """Serialize customerstatus to XML element."""
        if self.customerstatus is not None:
            elem = ET.SubElement(parent, 'customerstatus')
            elem.text = str(self.customerstatus)


@dataclass
class Supplierstatus:
    supplierstatus: int = 0

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Supplierstatus':
        """Create Supplierstatus instance from XML element."""
        return cls(
            supplierstatus=cls._parse_supplierstatus(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Supplierstatus instance to XML element."""
        element = ET.Element('supplierstatus')
        self._serialize_supplierstatus(element)
        return element
    @staticmethod
    def _parse_supplierstatus(element: ET.Element) -> int:
        """Parse supplierstatus from XML element."""
        elem = element.find('supplierstatus')
        if elem is not None and elem.text:
            return int(elem.text)
        return 0
    def _serialize_supplierstatus(self, parent: ET.Element) -> None:
        """Serialize supplierstatus to XML element."""
        if self.supplierstatus is not None:
            elem = ET.SubElement(parent, 'supplierstatus')
            elem.text = str(self.supplierstatus)


@dataclass
class Searchname:
    searchname: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Searchname':
        """Create Searchname instance from XML element."""
        return cls(
            searchname=cls._parse_searchname(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Searchname instance to XML element."""
        element = ET.Element('searchname')
        self._serialize_searchname(element)
        return element
    @staticmethod
    def _parse_searchname(element: ET.Element) -> str|None:
        """Parse searchname from XML element."""
        elem = element.find('searchname')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_searchname(self, parent: ET.Element) -> None:
        """Serialize searchname to XML element."""
        if self.searchname is not None:
            elem = ET.SubElement(parent, 'searchname')
            elem.text = str(self.searchname)


@dataclass
class Customercategory:
    customercategory: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Customercategory':
        """Create Customercategory instance from XML element."""
        return cls(
            customercategory=cls._parse_customercategory(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Customercategory instance to XML element."""
        element = ET.Element('customercategory')
        self._serialize_customercategory(element)
        return element
    @staticmethod
    def _parse_customercategory(element: ET.Element) -> str|None:
        """Parse customercategory from XML element."""
        elem = element.find('customercategory')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_customercategory(self, parent: ET.Element) -> None:
        """Serialize customercategory to XML element."""
        if self.customercategory is not None:
            elem = ET.SubElement(parent, 'customercategory')
            elem.text = str(self.customercategory)


@dataclass
class Suppliercategory:
    suppliercategory: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Suppliercategory':
        """Create Suppliercategory instance from XML element."""
        return cls(
            suppliercategory=cls._parse_suppliercategory(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Suppliercategory instance to XML element."""
        element = ET.Element('suppliercategory')
        self._serialize_suppliercategory(element)
        return element
    @staticmethod
    def _parse_suppliercategory(element: ET.Element) -> str|None:
        """Parse suppliercategory from XML element."""
        elem = element.find('suppliercategory')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_suppliercategory(self, parent: ET.Element) -> None:
        """Serialize suppliercategory to XML element."""
        if self.suppliercategory is not None:
            elem = ET.SubElement(parent, 'suppliercategory')
            elem.text = str(self.suppliercategory)


@dataclass
class Currency:
    currency: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Currency':
        """Create Currency instance from XML element."""
        return cls(
            currency=cls._parse_currency(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Currency instance to XML element."""
        element = ET.Element('currency')
        self._serialize_currency(element)
        return element
    @staticmethod
    def _parse_currency(element: ET.Element) -> str|None:
        """Parse currency from XML element."""
        elem = element.find('currency')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_currency(self, parent: ET.Element) -> None:
        """Serialize currency to XML element."""
        if self.currency is not None:
            elem = ET.SubElement(parent, 'currency')
            elem.text = str(self.currency)


@dataclass
class Invoicecountry:
    invoicecountry: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Invoicecountry':
        """Create Invoicecountry instance from XML element."""
        return cls(
            invoicecountry=cls._parse_invoicecountry(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Invoicecountry instance to XML element."""
        element = ET.Element('invoicecountry')
        self._serialize_invoicecountry(element)
        return element
    @staticmethod
    def _parse_invoicecountry(element: ET.Element) -> str|None:
        """Parse invoicecountry from XML element."""
        elem = element.find('invoicecountry')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_invoicecountry(self, parent: ET.Element) -> None:
        """Serialize invoicecountry to XML element."""
        if self.invoicecountry is not None:
            elem = ET.SubElement(parent, 'invoicecountry')
            elem.text = str(self.invoicecountry)


@dataclass
class Invoiceregion:
    invoiceregion: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Invoiceregion':
        """Create Invoiceregion instance from XML element."""
        return cls(
            invoiceregion=cls._parse_invoiceregion(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Invoiceregion instance to XML element."""
        element = ET.Element('invoiceregion')
        self._serialize_invoiceregion(element)
        return element
    @staticmethod
    def _parse_invoiceregion(element: ET.Element) -> str|None:
        """Parse invoiceregion from XML element."""
        elem = element.find('invoiceregion')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_invoiceregion(self, parent: ET.Element) -> None:
        """Serialize invoiceregion to XML element."""
        if self.invoiceregion is not None:
            elem = ET.SubElement(parent, 'invoiceregion')
            elem.text = str(self.invoiceregion)


@dataclass
class Invoicezip:
    invoicezip: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Invoicezip':
        """Create Invoicezip instance from XML element."""
        return cls(
            invoicezip=cls._parse_invoicezip(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Invoicezip instance to XML element."""
        element = ET.Element('invoicezip')
        self._serialize_invoicezip(element)
        return element
    @staticmethod
    def _parse_invoicezip(element: ET.Element) -> str|None:
        """Parse invoicezip from XML element."""
        elem = element.find('invoicezip')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_invoicezip(self, parent: ET.Element) -> None:
        """Serialize invoicezip to XML element."""
        if self.invoicezip is not None:
            elem = ET.SubElement(parent, 'invoicezip')
            elem.text = str(self.invoicezip)


@dataclass
class Invoicecity:
    invoicecity: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Invoicecity':
        """Create Invoicecity instance from XML element."""
        return cls(
            invoicecity=cls._parse_invoicecity(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Invoicecity instance to XML element."""
        element = ET.Element('invoicecity')
        self._serialize_invoicecity(element)
        return element
    @staticmethod
    def _parse_invoicecity(element: ET.Element) -> str|None:
        """Parse invoicecity from XML element."""
        elem = element.find('invoicecity')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_invoicecity(self, parent: ET.Element) -> None:
        """Serialize invoicecity to XML element."""
        if self.invoicecity is not None:
            elem = ET.SubElement(parent, 'invoicecity')
            elem.text = str(self.invoicecity)


@dataclass
class Invoicestreet:
    invoicestreet: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Invoicestreet':
        """Create Invoicestreet instance from XML element."""
        return cls(
            invoicestreet=cls._parse_invoicestreet(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Invoicestreet instance to XML element."""
        element = ET.Element('invoicestreet')
        self._serialize_invoicestreet(element)
        return element
    @staticmethod
    def _parse_invoicestreet(element: ET.Element) -> str|None:
        """Parse invoicestreet from XML element."""
        elem = element.find('invoicestreet')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_invoicestreet(self, parent: ET.Element) -> None:
        """Serialize invoicestreet to XML element."""
        if self.invoicestreet is not None:
            elem = ET.SubElement(parent, 'invoicestreet')
            elem.text = str(self.invoicestreet)


@dataclass
class Invoicehousenumber:
    invoicehousenumber: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Invoicehousenumber':
        """Create Invoicehousenumber instance from XML element."""
        return cls(
            invoicehousenumber=cls._parse_invoicehousenumber(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Invoicehousenumber instance to XML element."""
        element = ET.Element('invoicehousenumber')
        self._serialize_invoicehousenumber(element)
        return element
    @staticmethod
    def _parse_invoicehousenumber(element: ET.Element) -> str|None:
        """Parse invoicehousenumber from XML element."""
        elem = element.find('invoicehousenumber')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_invoicehousenumber(self, parent: ET.Element) -> None:
        """Serialize invoicehousenumber to XML element."""
        if self.invoicehousenumber is not None:
            elem = ET.SubElement(parent, 'invoicehousenumber')
            elem.text = str(self.invoicehousenumber)


@dataclass
class Mailcountry:
    mailcountry: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Mailcountry':
        """Create Mailcountry instance from XML element."""
        return cls(
            mailcountry=cls._parse_mailcountry(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Mailcountry instance to XML element."""
        element = ET.Element('mailcountry')
        self._serialize_mailcountry(element)
        return element
    @staticmethod
    def _parse_mailcountry(element: ET.Element) -> str|None:
        """Parse mailcountry from XML element."""
        elem = element.find('mailcountry')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_mailcountry(self, parent: ET.Element) -> None:
        """Serialize mailcountry to XML element."""
        if self.mailcountry is not None:
            elem = ET.SubElement(parent, 'mailcountry')
            elem.text = str(self.mailcountry)


@dataclass
class Mailregion:
    mailregion: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Mailregion':
        """Create Mailregion instance from XML element."""
        return cls(
            mailregion=cls._parse_mailregion(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Mailregion instance to XML element."""
        element = ET.Element('mailregion')
        self._serialize_mailregion(element)
        return element
    @staticmethod
    def _parse_mailregion(element: ET.Element) -> str|None:
        """Parse mailregion from XML element."""
        elem = element.find('mailregion')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_mailregion(self, parent: ET.Element) -> None:
        """Serialize mailregion to XML element."""
        if self.mailregion is not None:
            elem = ET.SubElement(parent, 'mailregion')
            elem.text = str(self.mailregion)


@dataclass
class Mailname:
    mailname: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Mailname':
        """Create Mailname instance from XML element."""
        return cls(
            mailname=cls._parse_mailname(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Mailname instance to XML element."""
        element = ET.Element('mailname')
        self._serialize_mailname(element)
        return element
    @staticmethod
    def _parse_mailname(element: ET.Element) -> str|None:
        """Parse mailname from XML element."""
        elem = element.find('mailname')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_mailname(self, parent: ET.Element) -> None:
        """Serialize mailname to XML element."""
        if self.mailname is not None:
            elem = ET.SubElement(parent, 'mailname')
            elem.text = str(self.mailname)


@dataclass
class Mailzip:
    mailzip: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Mailzip':
        """Create Mailzip instance from XML element."""
        return cls(
            mailzip=cls._parse_mailzip(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Mailzip instance to XML element."""
        element = ET.Element('mailzip')
        self._serialize_mailzip(element)
        return element
    @staticmethod
    def _parse_mailzip(element: ET.Element) -> str|None:
        """Parse mailzip from XML element."""
        elem = element.find('mailzip')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_mailzip(self, parent: ET.Element) -> None:
        """Serialize mailzip to XML element."""
        if self.mailzip is not None:
            elem = ET.SubElement(parent, 'mailzip')
            elem.text = str(self.mailzip)


@dataclass
class Mailcity:
    mailcity: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Mailcity':
        """Create Mailcity instance from XML element."""
        return cls(
            mailcity=cls._parse_mailcity(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Mailcity instance to XML element."""
        element = ET.Element('mailcity')
        self._serialize_mailcity(element)
        return element
    @staticmethod
    def _parse_mailcity(element: ET.Element) -> str|None:
        """Parse mailcity from XML element."""
        elem = element.find('mailcity')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_mailcity(self, parent: ET.Element) -> None:
        """Serialize mailcity to XML element."""
        if self.mailcity is not None:
            elem = ET.SubElement(parent, 'mailcity')
            elem.text = str(self.mailcity)


@dataclass
class Mailstreet:
    mailstreet: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Mailstreet':
        """Create Mailstreet instance from XML element."""
        return cls(
            mailstreet=cls._parse_mailstreet(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Mailstreet instance to XML element."""
        element = ET.Element('mailstreet')
        self._serialize_mailstreet(element)
        return element
    @staticmethod
    def _parse_mailstreet(element: ET.Element) -> str|None:
        """Parse mailstreet from XML element."""
        elem = element.find('mailstreet')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_mailstreet(self, parent: ET.Element) -> None:
        """Serialize mailstreet to XML element."""
        if self.mailstreet is not None:
            elem = ET.SubElement(parent, 'mailstreet')
            elem.text = str(self.mailstreet)


@dataclass
class Mailhousenumber:
    mailhousenumber: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Mailhousenumber':
        """Create Mailhousenumber instance from XML element."""
        return cls(
            mailhousenumber=cls._parse_mailhousenumber(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Mailhousenumber instance to XML element."""
        element = ET.Element('mailhousenumber')
        self._serialize_mailhousenumber(element)
        return element
    @staticmethod
    def _parse_mailhousenumber(element: ET.Element) -> str|None:
        """Parse mailhousenumber from XML element."""
        elem = element.find('mailhousenumber')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_mailhousenumber(self, parent: ET.Element) -> None:
        """Serialize mailhousenumber to XML element."""
        if self.mailhousenumber is not None:
            elem = ET.SubElement(parent, 'mailhousenumber')
            elem.text = str(self.mailhousenumber)


@dataclass
class Paymentmethod:
    paymentmethod: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Paymentmethod':
        """Create Paymentmethod instance from XML element."""
        return cls(
            paymentmethod=cls._parse_paymentmethod(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Paymentmethod instance to XML element."""
        element = ET.Element('paymentmethod')
        self._serialize_paymentmethod(element)
        return element
    @staticmethod
    def _parse_paymentmethod(element: ET.Element) -> str|None:
        """Parse paymentmethod from XML element."""
        elem = element.find('paymentmethod')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_paymentmethod(self, parent: ET.Element) -> None:
        """Serialize paymentmethod to XML element."""
        if self.paymentmethod is not None:
            elem = ET.SubElement(parent, 'paymentmethod')
            elem.text = str(self.paymentmethod)


@dataclass
class Paymentmethodtoleranceday:
    paymentmethodtoleranceday: int = 0

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Paymentmethodtoleranceday':
        """Create Paymentmethodtoleranceday instance from XML element."""
        return cls(
            paymentmethodtoleranceday=cls._parse_paymentmethodtoleranceday(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Paymentmethodtoleranceday instance to XML element."""
        element = ET.Element('paymentmethodtoleranceday')
        self._serialize_paymentmethodtoleranceday(element)
        return element
    @staticmethod
    def _parse_paymentmethodtoleranceday(element: ET.Element) -> int:
        """Parse paymentmethodtoleranceday from XML element."""
        elem = element.find('paymentmethodtoleranceday')
        if elem is not None and elem.text:
            return int(elem.text)
        return 0
    def _serialize_paymentmethodtoleranceday(self, parent: ET.Element) -> None:
        """Serialize paymentmethodtoleranceday to XML element."""
        if self.paymentmethodtoleranceday is not None:
            elem = ET.SubElement(parent, 'paymentmethodtoleranceday')
            elem.text = str(self.paymentmethodtoleranceday)


@dataclass
class Pricecategory:
    pricecategory: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Pricecategory':
        """Create Pricecategory instance from XML element."""
        return cls(
            pricecategory=cls._parse_pricecategory(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Pricecategory instance to XML element."""
        element = ET.Element('pricecategory')
        self._serialize_pricecategory(element)
        return element
    @staticmethod
    def _parse_pricecategory(element: ET.Element) -> str|None:
        """Parse pricecategory from XML element."""
        elem = element.find('pricecategory')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_pricecategory(self, parent: ET.Element) -> None:
        """Serialize pricecategory to XML element."""
        if self.pricecategory is not None:
            elem = ET.SubElement(parent, 'pricecategory')
            elem.text = str(self.pricecategory)


@dataclass
class Pricecategoryname:
    pricecategoryname: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Pricecategoryname':
        """Create Pricecategoryname instance from XML element."""
        return cls(
            pricecategoryname=cls._parse_pricecategoryname(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Pricecategoryname instance to XML element."""
        element = ET.Element('pricecategoryname')
        self._serialize_pricecategoryname(element)
        return element
    @staticmethod
    def _parse_pricecategoryname(element: ET.Element) -> str|None:
        """Parse pricecategoryname from XML element."""
        elem = element.find('pricecategoryname')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_pricecategoryname(self, parent: ET.Element) -> None:
        """Serialize pricecategoryname to XML element."""
        if self.pricecategoryname is not None:
            elem = ET.SubElement(parent, 'pricecategoryname')
            elem.text = str(self.pricecategoryname)


@dataclass
class Discountpercent:
    discountpercent: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Discountpercent':
        """Create Discountpercent instance from XML element."""
        return cls(
            discountpercent=cls._parse_discountpercent(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Discountpercent instance to XML element."""
        element = ET.Element('discountpercent')
        self._serialize_discountpercent(element)
        return element
    @staticmethod
    def _parse_discountpercent(element: ET.Element) -> float|None:
        """Parse discountpercent from XML element."""
        elem = element.find('discountpercent')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_discountpercent(self, parent: ET.Element) -> None:
        """Serialize discountpercent to XML element."""
        if self.discountpercent is not None:
            elem = ET.SubElement(parent, 'discountpercent')
            elem.text = str(self.discountpercent)


@dataclass
class Transportmode:
    transportmode: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Transportmode':
        """Create Transportmode instance from XML element."""
        return cls(
            transportmode=cls._parse_transportmode(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Transportmode instance to XML element."""
        element = ET.Element('transportmode')
        self._serialize_transportmode(element)
        return element
    @staticmethod
    def _parse_transportmode(element: ET.Element) -> str|None:
        """Parse transportmode from XML element."""
        elem = element.find('transportmode')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_transportmode(self, parent: ET.Element) -> None:
        """Serialize transportmode to XML element."""
        if self.transportmode is not None:
            elem = ET.SubElement(parent, 'transportmode')
            elem.text = str(self.transportmode)


@dataclass
class Taxnumber:
    taxnumber: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Taxnumber':
        """Create Taxnumber instance from XML element."""
        return cls(
            taxnumber=cls._parse_taxnumber(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Taxnumber instance to XML element."""
        element = ET.Element('taxnumber')
        self._serialize_taxnumber(element)
        return element
    @staticmethod
    def _parse_taxnumber(element: ET.Element) -> str|None:
        """Parse taxnumber from XML element."""
        elem = element.find('taxnumber')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_taxnumber(self, parent: ET.Element) -> None:
        """Serialize taxnumber to XML element."""
        if self.taxnumber is not None:
            elem = ET.SubElement(parent, 'taxnumber')
            elem.text = str(self.taxnumber)


@dataclass
class Eutaxnumber:
    eutaxnumber: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Eutaxnumber':
        """Create Eutaxnumber instance from XML element."""
        return cls(
            eutaxnumber=cls._parse_eutaxnumber(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Eutaxnumber instance to XML element."""
        element = ET.Element('eutaxnumber')
        self._serialize_eutaxnumber(element)
        return element
    @staticmethod
    def _parse_eutaxnumber(element: ET.Element) -> str|None:
        """Parse eutaxnumber from XML element."""
        elem = element.find('eutaxnumber')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_eutaxnumber(self, parent: ET.Element) -> None:
        """Serialize eutaxnumber to XML element."""
        if self.eutaxnumber is not None:
            elem = ET.SubElement(parent, 'eutaxnumber')
            elem.text = str(self.eutaxnumber)


@dataclass
class Bankaccount:
    bankaccount: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Bankaccount':
        """Create Bankaccount instance from XML element."""
        return cls(
            bankaccount=cls._parse_bankaccount(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Bankaccount instance to XML element."""
        element = ET.Element('bankaccount')
        self._serialize_bankaccount(element)
        return element
    @staticmethod
    def _parse_bankaccount(element: ET.Element) -> str|None:
        """Parse bankaccount from XML element."""
        elem = element.find('bankaccount')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_bankaccount(self, parent: ET.Element) -> None:
        """Serialize bankaccount to XML element."""
        if self.bankaccount is not None:
            elem = ET.SubElement(parent, 'bankaccount')
            elem.text = str(self.bankaccount)


@dataclass
class Bankaccountiban:
    bankaccountiban: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Bankaccountiban':
        """Create Bankaccountiban instance from XML element."""
        return cls(
            bankaccountiban=cls._parse_bankaccountiban(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Bankaccountiban instance to XML element."""
        element = ET.Element('bankaccountiban')
        self._serialize_bankaccountiban(element)
        return element
    @staticmethod
    def _parse_bankaccountiban(element: ET.Element) -> str|None:
        """Parse bankaccountiban from XML element."""
        elem = element.find('bankaccountiban')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_bankaccountiban(self, parent: ET.Element) -> None:
        """Serialize bankaccountiban to XML element."""
        if self.bankaccountiban is not None:
            elem = ET.SubElement(parent, 'bankaccountiban')
            elem.text = str(self.bankaccountiban)


@dataclass
class Bankname:
    bankname: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Bankname':
        """Create Bankname instance from XML element."""
        return cls(
            bankname=cls._parse_bankname(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Bankname instance to XML element."""
        element = ET.Element('bankname')
        self._serialize_bankname(element)
        return element
    @staticmethod
    def _parse_bankname(element: ET.Element) -> str|None:
        """Parse bankname from XML element."""
        elem = element.find('bankname')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_bankname(self, parent: ET.Element) -> None:
        """Serialize bankname to XML element."""
        if self.bankname is not None:
            elem = ET.SubElement(parent, 'bankname')
            elem.text = str(self.bankname)


@dataclass
class Bankswiftcode:
    bankswiftcode: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Bankswiftcode':
        """Create Bankswiftcode instance from XML element."""
        return cls(
            bankswiftcode=cls._parse_bankswiftcode(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Bankswiftcode instance to XML element."""
        element = ET.Element('bankswiftcode')
        self._serialize_bankswiftcode(element)
        return element
    @staticmethod
    def _parse_bankswiftcode(element: ET.Element) -> str|None:
        """Parse bankswiftcode from XML element."""
        elem = element.find('bankswiftcode')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_bankswiftcode(self, parent: ET.Element) -> None:
        """Serialize bankswiftcode to XML element."""
        if self.bankswiftcode is not None:
            elem = ET.SubElement(parent, 'bankswiftcode')
            elem.text = str(self.bankswiftcode)

@dataclass
class Webusername:
    webusername: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Webusername':
        """Create Webusername instance from XML element."""
        return cls(
            webusername=cls._parse_webusername(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Webusername instance to XML element."""
        element = ET.Element('webusername')
        self._serialize_webusername(element)
        return element
    @staticmethod
    def _parse_webusername(element: ET.Element) -> str|None:
        """Parse webusername from XML element."""
        elem = element.find('webusername')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_webusername(self, parent: ET.Element) -> None:
        """Serialize webusername to XML element."""
        if self.webusername is not None:
            elem = ET.SubElement(parent, 'webusername')
            elem.text = str(self.webusername)


@dataclass
class Webpassword:
    webpassword: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Webpassword':
        """Create Webpassword instance from XML element."""
        return cls(
            webpassword=cls._parse_webpassword(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Webpassword instance to XML element."""
        element = ET.Element('webpassword')
        self._serialize_webpassword(element)
        return element
    @staticmethod
    def _parse_webpassword(element: ET.Element) -> str|None:
        """Parse webpassword from XML element."""
        elem = element.find('webpassword')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_webpassword(self, parent: ET.Element) -> None:
        """Serialize webpassword to XML element."""
        if self.webpassword is not None:
            elem = ET.SubElement(parent, 'webpassword')
            elem.text = str(self.webpassword)


@dataclass
class Eumembership:
    eumembership: int = 0

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Eumembership':
        """Create Eumembership instance from XML element."""
        return cls(
            eumembership=cls._parse_eumembership(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Eumembership instance to XML element."""
        element = ET.Element('eumembership')
        self._serialize_eumembership(element)
        return element
    @staticmethod
    def _parse_eumembership(element: ET.Element) -> int:
        """Parse eumembership from XML element."""
        elem = element.find('eumembership')
        if elem is not None and elem.text:
            return int(elem.text)
        return 0
    def _serialize_eumembership(self, parent: ET.Element) -> None:
        """Serialize eumembership to XML element."""
        if self.eumembership is not None:
            elem = ET.SubElement(parent, 'eumembership')
            elem.text = str(self.eumembership)


@dataclass
class Strexa:
    strexa: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Strexa':
        """Create Strexa instance from XML element."""
        return cls(
            strexa=cls._parse_strexa(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Strexa instance to XML element."""
        element = ET.Element('strexa')
        self._serialize_strexa(element)
        return element
    @staticmethod
    def _parse_strexa(element: ET.Element) -> str|None:
        """Parse strexa from XML element."""
        elem = element.find('strexa')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_strexa(self, parent: ET.Element) -> None:
        """Serialize strexa to XML element."""
        if self.strexa is not None:
            elem = ET.SubElement(parent, 'strexa')
            elem.text = str(self.strexa)


@dataclass
class Strexb:
    strexb: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Strexb':
        """Create Strexb instance from XML element."""
        return cls(
            strexb=cls._parse_strexb(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Strexb instance to XML element."""
        element = ET.Element('strexb')
        self._serialize_strexb(element)
        return element
    @staticmethod
    def _parse_strexb(element: ET.Element) -> str|None:
        """Parse strexb from XML element."""
        elem = element.find('strexb')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_strexb(self, parent: ET.Element) -> None:
        """Serialize strexb to XML element."""
        if self.strexb is not None:
            elem = ET.SubElement(parent, 'strexb')
            elem.text = str(self.strexb)


@dataclass
class Strexc:
    strexc: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Strexc':
        """Create Strexc instance from XML element."""
        return cls(
            strexc=cls._parse_strexc(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Strexc instance to XML element."""
        element = ET.Element('strexc')
        self._serialize_strexc(element)
        return element
    @staticmethod
    def _parse_strexc(element: ET.Element) -> str|None:
        """Parse strexc from XML element."""
        elem = element.find('strexc')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_strexc(self, parent: ET.Element) -> None:
        """Serialize strexc to XML element."""
        if self.strexc is not None:
            elem = ET.SubElement(parent, 'strexc')
            elem.text = str(self.strexc)


@dataclass
class Strexd:
    strexd: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Strexd':
        """Create Strexd instance from XML element."""
        return cls(
            strexd=cls._parse_strexd(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Strexd instance to XML element."""
        element = ET.Element('strexd')
        self._serialize_strexd(element)
        return element
    @staticmethod
    def _parse_strexd(element: ET.Element) -> str|None:
        """Parse strexd from XML element."""
        elem = element.find('strexd')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_strexd(self, parent: ET.Element) -> None:
        """Serialize strexd to XML element."""
        if self.strexd is not None:
            elem = ET.SubElement(parent, 'strexd')
            elem.text = str(self.strexd)


@dataclass
class Dateexa:
    dateexa: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Dateexa':
        """Create Dateexa instance from XML element."""
        return cls(
            dateexa=cls._parse_dateexa(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Dateexa instance to XML element."""
        element = ET.Element('dateexa')
        self._serialize_dateexa(element)
        return element
    @staticmethod
    def _parse_dateexa(element: ET.Element) -> str|None:
        """Parse dateexa from XML element."""
        elem = element.find('dateexa')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_dateexa(self, parent: ET.Element) -> None:
        """Serialize dateexa to XML element."""
        if self.dateexa is not None:
            elem = ET.SubElement(parent, 'dateexa')
            elem.text = str(self.dateexa)


@dataclass
class Dateexb:
    dateexb: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Dateexb':
        """Create Dateexb instance from XML element."""
        return cls(
            dateexb=cls._parse_dateexb(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Dateexb instance to XML element."""
        element = ET.Element('dateexb')
        self._serialize_dateexb(element)
        return element
    @staticmethod
    def _parse_dateexb(element: ET.Element) -> str|None:
        """Parse dateexb from XML element."""
        elem = element.find('dateexb')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_dateexb(self, parent: ET.Element) -> None:
        """Serialize dateexb to XML element."""
        if self.dateexb is not None:
            elem = ET.SubElement(parent, 'dateexb')
            elem.text = str(self.dateexb)


@dataclass
class Numexa:
    numexa: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Numexa':
        """Create Numexa instance from XML element."""
        return cls(
            numexa=cls._parse_numexa(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Numexa instance to XML element."""
        element = ET.Element('numexa')
        self._serialize_numexa(element)
        return element
    @staticmethod
    def _parse_numexa(element: ET.Element) -> float|None:
        """Parse numexa from XML element."""
        elem = element.find('numexa')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_numexa(self, parent: ET.Element) -> None:
        """Serialize numexa to XML element."""
        if self.numexa is not None:
            elem = ET.SubElement(parent, 'numexa')
            elem.text = str(self.numexa)


@dataclass
class Numexb:
    numexb: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Numexb':
        """Create Numexb instance from XML element."""
        return cls(
            numexb=cls._parse_numexb(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Numexb instance to XML element."""
        element = ET.Element('numexb')
        self._serialize_numexb(element)
        return element
    @staticmethod
    def _parse_numexb(element: ET.Element) -> float|None:
        """Parse numexb from XML element."""
        elem = element.find('numexb')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_numexb(self, parent: ET.Element) -> None:
        """Serialize numexb to XML element."""
        if self.numexb is not None:
            elem = ET.SubElement(parent, 'numexb')
            elem.text = str(self.numexb)


@dataclass
class Numexc:
    numexc: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Numexc':
        """Create Numexc instance from XML element."""
        return cls(
            numexc=cls._parse_numexc(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Numexc instance to XML element."""
        element = ET.Element('numexc')
        self._serialize_numexc(element)
        return element
    @staticmethod
    def _parse_numexc(element: ET.Element) -> float|None:
        """Parse numexc from XML element."""
        elem = element.find('numexc')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_numexc(self, parent: ET.Element) -> None:
        """Serialize numexc to XML element."""
        if self.numexc is not None:
            elem = ET.SubElement(parent, 'numexc')
            elem.text = str(self.numexc)


@dataclass
class Boolexa:
    boolexa: bool = False

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Boolexa':
        """Create Boolexa instance from XML element."""
        return cls(
            boolexa=cls._parse_boolexa(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Boolexa instance to XML element."""
        element = ET.Element('boolexa')
        self._serialize_boolexa(element)
        return element
    @staticmethod
    def _parse_boolexa(element: ET.Element) -> bool:
        """Parse boolexa from XML element."""
        elem = element.find('boolexa')
        if elem is not None and elem.text:
            return bool(elem.text)
        return False
    def _serialize_boolexa(self, parent: ET.Element) -> None:
        """Serialize boolexa to XML element."""
        if self.boolexa is not None:
            elem = ET.SubElement(parent, 'boolexa')
            elem.text = str(self.boolexa)


@dataclass
class Boolexb:
    boolexb:  bool = False

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Boolexb':
        """Create Boolexb instance from XML element."""
        return cls(
            boolexb=cls._parse_boolexb(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Boolexb instance to XML element."""
        element = ET.Element('boolexb')
        self._serialize_boolexb(element)
        return element
    @staticmethod
    def _parse_boolexb(element: ET.Element) -> bool:
        """Parse boolexb from XML element."""
        elem = element.find('boolexb')
        if elem is not None and elem.text:
            return bool(elem.text)
        return False
    def _serialize_boolexb(self, parent: ET.Element) -> None:
        """Serialize boolexb to XML element."""
        if self.boolexb is not None:
            elem = ET.SubElement(parent, 'boolexb')
            elem.text = str(self.boolexb)


@dataclass
class Lookupexa:
    lookupexa: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Lookupexa':
        """Create Lookupexa instance from XML element."""
        return cls(
            lookupexa=cls._parse_lookupexa(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Lookupexa instance to XML element."""
        element = ET.Element('lookupexa')
        self._serialize_lookupexa(element)
        return element
    @staticmethod
    def _parse_lookupexa(element: ET.Element) -> str|None:
        """Parse lookupexa from XML element."""
        elem = element.find('lookupexa')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_lookupexa(self, parent: ET.Element) -> None:
        """Serialize lookupexa to XML element."""
        if self.lookupexa is not None:
            elem = ET.SubElement(parent, 'lookupexa')
            elem.text = str(self.lookupexa)


@dataclass
class Lookupexb:
    lookupexb: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Lookupexb':
        """Create Lookupexb instance from XML element."""
        return cls(
            lookupexb=cls._parse_lookupexb(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Lookupexb instance to XML element."""
        element = ET.Element('lookupexb')
        self._serialize_lookupexb(element)
        return element
    @staticmethod
    def _parse_lookupexb(element: ET.Element) -> str|None:
        """Parse lookupexb from XML element."""
        elem = element.find('lookupexb')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_lookupexb(self, parent: ET.Element) -> None:
        """Serialize lookupexb to XML element."""
        if self.lookupexb is not None:
            elem = ET.SubElement(parent, 'lookupexb')
            elem.text = str(self.lookupexb)


@dataclass
class Lookupexc:
    lookupexc: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Lookupexc':
        """Create Lookupexc instance from XML element."""
        return cls(
            lookupexc=cls._parse_lookupexc(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Lookupexc instance to XML element."""
        element = ET.Element('lookupexc')
        self._serialize_lookupexc(element)
        return element
    @staticmethod
    def _parse_lookupexc(element: ET.Element) -> str|None:
        """Parse lookupexc from XML element."""
        elem = element.find('lookupexc')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_lookupexc(self, parent: ET.Element) -> None:
        """Serialize lookupexc to XML element."""
        if self.lookupexc is not None:
            elem = ET.SubElement(parent, 'lookupexc')
            elem.text = str(self.lookupexc)


@dataclass
class Lookupexd:
    lookupexd: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Lookupexd':
        """Create Lookupexd instance from XML element."""
        return cls(
            lookupexd=cls._parse_lookupexd(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Lookupexd instance to XML element."""
        element = ET.Element('lookupexd')
        self._serialize_lookupexd(element)
        return element
    @staticmethod
    def _parse_lookupexd(element: ET.Element) -> str|None:
        """Parse lookupexd from XML element."""
        elem = element.find('lookupexd')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_lookupexd(self, parent: ET.Element) -> None:
        """Serialize lookupexd to XML element."""
        if self.lookupexd is not None:
            elem = ET.SubElement(parent, 'lookupexd')
            elem.text = str(self.lookupexd)


@dataclass
class Preferred:
    preferred: int = 0

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Preferred':
        """Create Preferred instance from XML element."""
        return cls(
            preferred=cls._parse_preferred(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Preferred instance to XML element."""
        element = ET.Element('preferred')
        self._serialize_preferred(element)
        return element
    @staticmethod
    def _parse_preferred(element: ET.Element) -> int:
        """Parse preferred from XML element."""
        elem = element.find('preferred')
        if elem is not None and elem.text:
            return int(elem.text or 0)
        return 0
    def _serialize_preferred(self, parent: ET.Element) -> None:
        """Serialize preferred to XML element."""
        if self.preferred is not None:
            elem = ET.SubElement(parent, 'preferred')
            elem.text = str(self.preferred)

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
class Country:
    country: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Country':
        """Create Country instance from XML element."""
        return cls(
            country=cls._parse_country(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Country instance to XML element."""
        element = ET.Element('country')
        self._serialize_country(element)
        return element
    @staticmethod
    def _parse_country(element: ET.Element) -> str|None:
        """Parse country from XML element."""
        elem = element.find('country')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_country(self, parent: ET.Element) -> None:
        """Serialize country to XML element."""
        if self.country is not None:
            elem = ET.SubElement(parent, 'country')
            elem.text = str(self.country)


@dataclass
class Region:
    region: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Region':
        """Create Region instance from XML element."""
        return cls(
            region=cls._parse_region(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Region instance to XML element."""
        element = ET.Element('region')
        self._serialize_region(element)
        return element
    @staticmethod
    def _parse_region(element: ET.Element) -> str|None:
        """Parse region from XML element."""
        elem = element.find('region')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_region(self, parent: ET.Element) -> None:
        """Serialize region to XML element."""
        if self.region is not None:
            elem = ET.SubElement(parent, 'region')
            elem.text = str(self.region)


@dataclass
class Zip:
    zip: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Zip':
        """Create Zip instance from XML element."""
        return cls(
            zip=cls._parse_zip(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Zip instance to XML element."""
        element = ET.Element('zip')
        self._serialize_zip(element)
        return element
    @staticmethod
    def _parse_zip(element: ET.Element) -> str|None:
        """Parse zip from XML element."""
        elem = element.find('zip')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_zip(self, parent: ET.Element) -> None:
        """Serialize zip to XML element."""
        if self.zip is not None:
            elem = ET.SubElement(parent, 'zip')
            elem.text = str(self.zip)


@dataclass
class City:
    city: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'City':
        """Create City instance from XML element."""
        return cls(
            city=cls._parse_city(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert City instance to XML element."""
        element = ET.Element('city')
        self._serialize_city(element)
        return element
    @staticmethod
    def _parse_city(element: ET.Element) -> str|None:
        """Parse city from XML element."""
        elem = element.find('city')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_city(self, parent: ET.Element) -> None:
        """Serialize city to XML element."""
        if self.city is not None:
            elem = ET.SubElement(parent, 'city')
            elem.text = str(self.city)


@dataclass
class Street:
    street: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Street':
        """Create Street instance from XML element."""
        return cls(
            street=cls._parse_street(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Street instance to XML element."""
        element = ET.Element('street')
        self._serialize_street(element)
        return element
    @staticmethod
    def _parse_street(element: ET.Element) -> str|None:
        """Parse street from XML element."""
        elem = element.find('street')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_street(self, parent: ET.Element) -> None:
        """Serialize street to XML element."""
        if self.street is not None:
            elem = ET.SubElement(parent, 'street')
            elem.text = str(self.street)


@dataclass
class Housenumber:
    housenumber: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Housenumber':
        """Create Housenumber instance from XML element."""
        return cls(
            housenumber=cls._parse_housenumber(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Housenumber instance to XML element."""
        element = ET.Element('housenumber')
        self._serialize_housenumber(element)
        return element
    @staticmethod
    def _parse_housenumber(element: ET.Element) -> str|None:
        """Parse housenumber from XML element."""
        elem = element.find('housenumber')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_housenumber(self, parent: ET.Element) -> None:
        """Serialize housenumber to XML element."""
        if self.housenumber is not None:
            elem = ET.SubElement(parent, 'housenumber')
            elem.text = str(self.housenumber)


@dataclass
class Contactname:
    contactname: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Contactname':
        """Create Contactname instance from XML element."""
        return cls(
            contactname=cls._parse_contactname(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Contactname instance to XML element."""
        element = ET.Element('contactname')
        self._serialize_contactname(element)
        return element
    @staticmethod
    def _parse_contactname(element: ET.Element) -> str|None:
        """Parse contactname from XML element."""
        elem = element.find('contactname')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_contactname(self, parent: ET.Element) -> None:
        """Serialize contactname to XML element."""
        if self.contactname is not None:
            elem = ET.SubElement(parent, 'contactname')
            elem.text = str(self.contactname)


@dataclass
class Iscompany:
    iscompany: int = 0

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Iscompany':
        """Create Iscompany instance from XML element."""
        return cls(
            iscompany=cls._parse_iscompany(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Iscompany instance to XML element."""
        element = ET.Element('iscompany')
        self._serialize_iscompany(element)
        return element
    @staticmethod
    def _parse_iscompany(element: ET.Element) -> int:
        """Parse iscompany from XML element."""
        elem = element.find('iscompany')
        if elem is not None and elem.text:
            return int(elem.text or 0)
        return 0
    def _serialize_iscompany(self, parent: ET.Element) -> None:
        """Serialize iscompany to XML element."""
        if self.iscompany is not None:
            elem = ET.SubElement(parent, 'iscompany')
            elem.text = str(self.iscompany)


@dataclass
class Companytaxnumber:
    companytaxnumber: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Companytaxnumber':
        """Create Companytaxnumber instance from XML element."""
        return cls(
            companytaxnumber=cls._parse_companytaxnumber(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Companytaxnumber instance to XML element."""
        element = ET.Element('companytaxnumber')
        self._serialize_companytaxnumber(element)
        return element
    @staticmethod
    def _parse_companytaxnumber(element: ET.Element) -> str|None:
        """Parse companytaxnumber from XML element."""
        elem = element.find('companytaxnumber')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_companytaxnumber(self, parent: ET.Element) -> None:
        """Serialize companytaxnumber to XML element."""
        if self.companytaxnumber is not None:
            elem = ET.SubElement(parent, 'companytaxnumber')
            elem.text = str(self.companytaxnumber)


@dataclass
class Customeraddress:
    preferred: Optional['Preferred'] = None
    id: Optional['Id'] = None
    code: Optional['Code'] = None
    name: Optional['Name'] = None
    country: Optional['Country'] = None
    region: Optional['Region'] = None
    zip: Optional['Zip'] = None
    city: Optional['City'] = None
    street: Optional['Street'] = None
    housenumber: Optional['Housenumber'] = None
    contactname: Optional['Contactname'] = None
    phone: Optional['Phone'] = None
    fax: Optional['Fax'] = None
    email: Optional['Email'] = None
    iscompany: Optional['Iscompany'] = None
    companytaxnumber: Optional['Companytaxnumber'] = None
    description: Optional['Description'] = None
    deleted: Optional['Deleted'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Customeraddress':
        """Create Customeraddress instance from XML element."""
        return cls(
            preferred=cls._parse_preferred(element),
            id=cls._parse_id(element),
            code=cls._parse_code(element),
            name=cls._parse_name(element),
            country=cls._parse_country(element),
            region=cls._parse_region(element),
            zip=cls._parse_zip(element),
            city=cls._parse_city(element),
            street=cls._parse_street(element),
            housenumber=cls._parse_housenumber(element),
            contactname=cls._parse_contactname(element),
            phone=cls._parse_phone(element),
            fax=cls._parse_fax(element),
            email=cls._parse_email(element),
            iscompany=cls._parse_iscompany(element),
            companytaxnumber=cls._parse_companytaxnumber(element),
            description=cls._parse_description(element),
            deleted=cls._parse_deleted(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Customeraddress instance to XML element."""
        element = ET.Element('customeraddress')
        self._serialize_preferred(element)
        self._serialize_id(element)
        self._serialize_code(element)
        self._serialize_name(element)
        self._serialize_country(element)
        self._serialize_region(element)
        self._serialize_zip(element)
        self._serialize_city(element)
        self._serialize_street(element)
        self._serialize_housenumber(element)
        self._serialize_contactname(element)
        self._serialize_phone(element)
        self._serialize_fax(element)
        self._serialize_email(element)
        self._serialize_iscompany(element)
        self._serialize_companytaxnumber(element)
        self._serialize_description(element)
        self._serialize_deleted(element)
        return element
    @staticmethod
    def _parse_preferred(element: ET.Element) -> Optional['Preferred']:
        """Parse preferred from XML element."""
        child = element.find('preferred')
        if child is not None:
            return Preferred.from_element(child)
        return None
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
    def _parse_name(element: ET.Element) -> Optional['Name']:
        """Parse name from XML element."""
        child = element.find('name')
        if child is not None:
            return Name.from_element(child)
        return None
    @staticmethod
    def _parse_country(element: ET.Element) -> Optional['Country']:
        """Parse country from XML element."""
        child = element.find('country')
        if child is not None:
            return Country.from_element(child)
        return None
    @staticmethod
    def _parse_region(element: ET.Element) -> Optional['Region']:
        """Parse region from XML element."""
        child = element.find('region')
        if child is not None:
            return Region.from_element(child)
        return None
    @staticmethod
    def _parse_zip(element: ET.Element) -> Optional['Zip']:
        """Parse zip from XML element."""
        child = element.find('zip')
        if child is not None:
            return Zip.from_element(child)
        return None
    @staticmethod
    def _parse_city(element: ET.Element) -> Optional['City']:
        """Parse city from XML element."""
        child = element.find('city')
        if child is not None:
            return City.from_element(child)
        return None
    @staticmethod
    def _parse_street(element: ET.Element) -> Optional['Street']:
        """Parse street from XML element."""
        child = element.find('street')
        if child is not None:
            return Street.from_element(child)
        return None
    @staticmethod
    def _parse_housenumber(element: ET.Element) -> Optional['Housenumber']:
        """Parse housenumber from XML element."""
        child = element.find('housenumber')
        if child is not None:
            return Housenumber.from_element(child)
        return None
    @staticmethod
    def _parse_contactname(element: ET.Element) -> Optional['Contactname']:
        """Parse contactname from XML element."""
        child = element.find('contactname')
        if child is not None:
            return Contactname.from_element(child)
        return None
    @staticmethod
    def _parse_phone(element: ET.Element) -> Optional['Phone']:
        """Parse phone from XML element."""
        child = element.find('phone')
        if child is not None:
            return Phone.from_element(child)
        return None
    @staticmethod
    def _parse_fax(element: ET.Element) -> Optional['Fax']:
        """Parse fax from XML element."""
        child = element.find('fax')
        if child is not None:
            return Fax.from_element(child)
        return None
    @staticmethod
    def _parse_email(element: ET.Element) -> Optional['Email']:
        """Parse email from XML element."""
        child = element.find('email')
        if child is not None:
            return Email.from_element(child)
        return None
    @staticmethod
    def _parse_iscompany(element: ET.Element) -> Optional['Iscompany']:
        """Parse iscompany from XML element."""
        child = element.find('iscompany')
        if child is not None:
            return Iscompany.from_element(child)
        return None
    @staticmethod
    def _parse_companytaxnumber(element: ET.Element) -> Optional['Companytaxnumber']:
        """Parse companytaxnumber from XML element."""
        child = element.find('companytaxnumber')
        if child is not None:
            return Companytaxnumber.from_element(child)
        return None
    @staticmethod
    def _parse_description(element: ET.Element) -> Optional['Description']:
        """Parse description from XML element."""
        child = element.find('description')
        if child is not None:
            return Description.from_element(child)
        return None
    @staticmethod
    def _parse_deleted(element: ET.Element) -> Optional['Deleted']:
        """Parse deleted from XML element."""
        child = element.find('deleted')
        if child is not None:
            return Deleted.from_element(child)
        return None
    def _serialize_preferred(self, parent: ET.Element) -> None:
        """Serialize preferred to XML element."""
        if self.preferred is not None:
            parent.append(self.preferred.to_element())
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_code(self, parent: ET.Element) -> None:
        """Serialize code to XML element."""
        if self.code is not None:
            parent.append(self.code.to_element())
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())
    def _serialize_country(self, parent: ET.Element) -> None:
        """Serialize country to XML element."""
        if self.country is not None:
            parent.append(self.country.to_element())
    def _serialize_region(self, parent: ET.Element) -> None:
        """Serialize region to XML element."""
        if self.region is not None:
            parent.append(self.region.to_element())
    def _serialize_zip(self, parent: ET.Element) -> None:
        """Serialize zip to XML element."""
        if self.zip is not None:
            parent.append(self.zip.to_element())
    def _serialize_city(self, parent: ET.Element) -> None:
        """Serialize city to XML element."""
        if self.city is not None:
            parent.append(self.city.to_element())
    def _serialize_street(self, parent: ET.Element) -> None:
        """Serialize street to XML element."""
        if self.street is not None:
            parent.append(self.street.to_element())
    def _serialize_housenumber(self, parent: ET.Element) -> None:
        """Serialize housenumber to XML element."""
        if self.housenumber is not None:
            parent.append(self.housenumber.to_element())
    def _serialize_contactname(self, parent: ET.Element) -> None:
        """Serialize contactname to XML element."""
        if self.contactname is not None:
            parent.append(self.contactname.to_element())
    def _serialize_phone(self, parent: ET.Element) -> None:
        """Serialize phone to XML element."""
        if self.phone is not None:
            parent.append(self.phone.to_element())
    def _serialize_fax(self, parent: ET.Element) -> None:
        """Serialize fax to XML element."""
        if self.fax is not None:
            parent.append(self.fax.to_element())
    def _serialize_email(self, parent: ET.Element) -> None:
        """Serialize email to XML element."""
        if self.email is not None:
            parent.append(self.email.to_element())
    def _serialize_iscompany(self, parent: ET.Element) -> None:
        """Serialize iscompany to XML element."""
        if self.iscompany is not None:
            parent.append(self.iscompany.to_element())
    def _serialize_companytaxnumber(self, parent: ET.Element) -> None:
        """Serialize companytaxnumber to XML element."""
        if self.companytaxnumber is not None:
            parent.append(self.companytaxnumber.to_element())
    def _serialize_description(self, parent: ET.Element) -> None:
        """Serialize description to XML element."""
        if self.description is not None:
            parent.append(self.description.to_element())
    def _serialize_deleted(self, parent: ET.Element) -> None:
        """Serialize deleted to XML element."""
        if self.deleted is not None:
            parent.append(self.deleted.to_element())


@dataclass
class Customeraddresses:
    customeraddress_list: List['Customeraddress'] = field(default_factory=list)

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Customeraddresses':
        """Create Customeraddresses instance from XML element."""
        return cls(
            customeraddress_list=cls._parse_customeraddress_list(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Customeraddresses instance to XML element."""
        element = ET.Element('customeraddresses')
        self._serialize_customeraddress_list(element)
        return element
    @staticmethod
    def _parse_customeraddress_list(element: ET.Element) -> List['Customeraddress']:
        """Parse customeraddress list from XML element."""
        children = element.findall('customeraddress')
        return [Customeraddress.from_element(child) for child in children]
    def _serialize_customeraddress_list(self, parent: ET.Element) -> None:
        """Serialize customeraddress_list list to XML elements."""
        for item in self.customeraddress_list:
            parent.append(item.to_element())


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
        element = ET.Element('name')
        self._serialize_name(element)
        return element
    @staticmethod
    def _parse_name(element: ET.Element) -> str|None:
        """Parse name from XML element."""
        elem = element.find('name')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            elem = ET.SubElement(parent, 'name')
            elem.text = str(self.name)


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
            return int(elem.text)
        return 0
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            elem = ET.SubElement(parent, 'id')
            elem.text = str(self.id)


@dataclass
class Responsibility:
    # No properties found
    pass

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Responsibility':
        """Create Responsibility instance from XML element."""
        return cls()
    
    def to_element(self) -> ET.Element:
        """Convert Responsibility instance to XML element."""
        element = ET.Element('responsibility')
        return element


@dataclass
class Phone:
    phone: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Phone':
        """Create Phone instance from XML element."""
        return cls(
            phone=cls._parse_phone(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Phone instance to XML element."""
        element = ET.Element('phone')
        self._serialize_phone(element)
        return element
    @staticmethod
    def _parse_phone(element: ET.Element) -> str|None:
        """Parse phone from XML element."""
        elem = element.find('phone')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_phone(self, parent: ET.Element) -> None:
        """Serialize phone to XML element."""
        if self.phone is not None:
            elem = ET.SubElement(parent, 'phone')
            elem.text = str(self.phone)


@dataclass
class Fax:
    fax: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Fax':
        """Create Fax instance from XML element."""
        return cls(
            fax=cls._parse_fax(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Fax instance to XML element."""
        element = ET.Element('fax')
        self._serialize_fax(element)
        return element
    @staticmethod
    def _parse_fax(element: ET.Element) -> str|None:
        """Parse fax from XML element."""
        elem = element.find('fax')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_fax(self, parent: ET.Element) -> None:
        """Serialize fax to XML element."""
        if self.fax is not None:
            elem = ET.SubElement(parent, 'fax')
            elem.text = str(self.fax)


@dataclass
class Sms:
    sms: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Sms':
        """Create Sms instance from XML element."""
        return cls(
            sms=cls._parse_sms(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Sms instance to XML element."""
        element = ET.Element('sms')
        self._serialize_sms(element)
        return element
    @staticmethod
    def _parse_sms(element: ET.Element) -> str|None:
        """Parse sms from XML element."""
        elem = element.find('sms')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_sms(self, parent: ET.Element) -> None:
        """Serialize sms to XML element."""
        if self.sms is not None:
            elem = ET.SubElement(parent, 'sms')
            elem.text = str(self.sms)


@dataclass
class Email:
    email: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Email':
        """Create Email instance from XML element."""
        return cls(
            email=cls._parse_email(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Email instance to XML element."""
        element = ET.Element('email')
        self._serialize_email(element)
        return element
    @staticmethod
    def _parse_email(element: ET.Element) -> str|None:
        """Parse email from XML element."""
        elem = element.find('email')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_email(self, parent: ET.Element) -> None:
        """Serialize email to XML element."""
        if self.email is not None:
            elem = ET.SubElement(parent, 'email')
            elem.text = str(self.email)


@dataclass
class Url:
    url: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Url':
        """Create Url instance from XML element."""
        return cls(
            url=cls._parse_url(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Url instance to XML element."""
        element = ET.Element('url')
        self._serialize_url(element)
        return element
    @staticmethod
    def _parse_url(element: ET.Element) -> str|None:
        """Parse url from XML element."""
        elem = element.find('url')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_url(self, parent: ET.Element) -> None:
        """Serialize url to XML element."""
        if self.url is not None:
            elem = ET.SubElement(parent, 'url')
            elem.text = str(self.url)


@dataclass
class Skype:
    skype: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Skype':
        """Create Skype instance from XML element."""
        return cls(
            skype=cls._parse_skype(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Skype instance to XML element."""
        element = ET.Element('skype')
        self._serialize_skype(element)
        return element
    @staticmethod
    def _parse_skype(element: ET.Element) -> str|None:
        """Parse skype from XML element."""
        elem = element.find('skype')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_skype(self, parent: ET.Element) -> None:
        """Serialize skype to XML element."""
        if self.skype is not None:
            elem = ET.SubElement(parent, 'skype')
            elem.text = str(self.skype)


@dataclass
class Facebookurl:
    facebookurl: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Facebookurl':
        """Create Facebookurl instance from XML element."""
        return cls(
            facebookurl=cls._parse_facebookurl(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Facebookurl instance to XML element."""
        element = ET.Element('facebookurl')
        self._serialize_facebookurl(element)
        return element
    @staticmethod
    def _parse_facebookurl(element: ET.Element) -> str|None:
        """Parse facebookurl from XML element."""
        elem = element.find('facebookurl')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_facebookurl(self, parent: ET.Element) -> None:
        """Serialize facebookurl to XML element."""
        if self.facebookurl is not None:
            elem = ET.SubElement(parent, 'facebookurl')
            elem.text = str(self.facebookurl)


@dataclass
class Msn:
    msn: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Msn':
        """Create Msn instance from XML element."""
        return cls(
            msn=cls._parse_msn(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Msn instance to XML element."""
        element = ET.Element('msn')
        self._serialize_msn(element)
        return element
    @staticmethod
    def _parse_msn(element: ET.Element) -> str|None:
        """Parse msn from XML element."""
        elem = element.find('msn')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_msn(self, parent: ET.Element) -> None:
        """Serialize msn to XML element."""
        if self.msn is not None:
            elem = ET.SubElement(parent, 'msn')
            elem.text = str(self.msn)


@dataclass
class Description:
    description: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Description':
        """Create Description instance from XML element."""
        return cls(
            description=cls._parse_description(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Description instance to XML element."""
        element = ET.Element('description')
        self._serialize_description(element)
        return element
    @staticmethod
    def _parse_description(element: ET.Element) -> str|None:
        """Parse description from XML element."""
        elem = element.find('description')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_description(self, parent: ET.Element) -> None:
        """Serialize description to XML element."""
        if self.description is not None:
            elem = ET.SubElement(parent, 'description')
            elem.text = str(self.description)


@dataclass
class Deleted:
    deleted: int = 0

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Deleted':
        """Create Deleted instance from XML element."""
        return cls(
            deleted=cls._parse_deleted(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Deleted instance to XML element."""
        element = ET.Element('deleted')
        self._serialize_deleted(element)
        return element
    @staticmethod
    def _parse_deleted(element: ET.Element) -> int:
        """Parse deleted from XML element."""
        elem = element.find('deleted')
        if elem is not None and elem.text:
            return int(elem.text)
        return 0
    def _serialize_deleted(self, parent: ET.Element) -> None:
        """Serialize deleted to XML element."""
        if self.deleted is not None:
            elem = ET.SubElement(parent, 'deleted')
            elem.text = str(self.deleted)


@dataclass
class Customercontact:
    name: Optional['Name'] = None
    id: Optional['Id'] = None
    responsibility: Optional['Responsibility'] = None
    phone: Optional['Phone'] = None
    fax: Optional['Fax'] = None
    sms: Optional['Sms'] = None
    email: Optional['Email'] = None
    url: Optional['Url'] = None
    skype: Optional['Skype'] = None
    facebookurl: Optional['Facebookurl'] = None
    msn: Optional['Msn'] = None
    description: Optional['Description'] = None
    deleted: Optional['Deleted'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Customercontact':
        """Create Customercontact instance from XML element."""
        return cls(
            name=cls._parse_name(element),
            id=cls._parse_id(element),
            responsibility=cls._parse_responsibility(element),
            phone=cls._parse_phone(element),
            fax=cls._parse_fax(element),
            sms=cls._parse_sms(element),
            email=cls._parse_email(element),
            url=cls._parse_url(element),
            skype=cls._parse_skype(element),
            facebookurl=cls._parse_facebookurl(element),
            msn=cls._parse_msn(element),
            description=cls._parse_description(element),
            deleted=cls._parse_deleted(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Customercontact instance to XML element."""
        element = ET.Element('customercontact')
        self._serialize_name(element)
        self._serialize_id(element)
        self._serialize_responsibility(element)
        self._serialize_phone(element)
        self._serialize_fax(element)
        self._serialize_sms(element)
        self._serialize_email(element)
        self._serialize_url(element)
        self._serialize_skype(element)
        self._serialize_facebookurl(element)
        self._serialize_msn(element)
        self._serialize_description(element)
        self._serialize_deleted(element)
        return element
    @staticmethod
    def _parse_name(element: ET.Element) -> Optional['Name']:
        """Parse name from XML element."""
        child = element.find('name')
        if child is not None:
            return Name.from_element(child)
        return None
    @staticmethod
    def _parse_id(element: ET.Element) -> Optional['Id']:
        """Parse id from XML element."""
        child = element.find('id')
        if child is not None:
            return Id.from_element(child)
        return None
    @staticmethod
    def _parse_responsibility(element: ET.Element) -> Optional['Responsibility']:
        """Parse responsibility from XML element."""
        child = element.find('responsibility')
        if child is not None:
            return Responsibility.from_element(child)
        return None
    @staticmethod
    def _parse_phone(element: ET.Element) -> Optional['Phone']:
        """Parse phone from XML element."""
        child = element.find('phone')
        if child is not None:
            return Phone.from_element(child)
        return None
    @staticmethod
    def _parse_fax(element: ET.Element) -> Optional['Fax']:
        """Parse fax from XML element."""
        child = element.find('fax')
        if child is not None:
            return Fax.from_element(child)
        return None
    @staticmethod
    def _parse_sms(element: ET.Element) -> Optional['Sms']:
        """Parse sms from XML element."""
        child = element.find('sms')
        if child is not None:
            return Sms.from_element(child)
        return None
    @staticmethod
    def _parse_email(element: ET.Element) -> Optional['Email']:
        """Parse email from XML element."""
        child = element.find('email')
        if child is not None:
            return Email.from_element(child)
        return None
    @staticmethod
    def _parse_url(element: ET.Element) -> Optional['Url']:
        """Parse url from XML element."""
        child = element.find('url')
        if child is not None:
            return Url.from_element(child)
        return None
    @staticmethod
    def _parse_skype(element: ET.Element) -> Optional['Skype']:
        """Parse skype from XML element."""
        child = element.find('skype')
        if child is not None:
            return Skype.from_element(child)
        return None
    @staticmethod
    def _parse_facebookurl(element: ET.Element) -> Optional['Facebookurl']:
        """Parse facebookurl from XML element."""
        child = element.find('facebookurl')
        if child is not None:
            return Facebookurl.from_element(child)
        return None
    @staticmethod
    def _parse_msn(element: ET.Element) -> Optional['Msn']:
        """Parse msn from XML element."""
        child = element.find('msn')
        if child is not None:
            return Msn.from_element(child)
        return None
    @staticmethod
    def _parse_description(element: ET.Element) -> Optional['Description']:
        """Parse description from XML element."""
        child = element.find('description')
        if child is not None:
            return Description.from_element(child)
        return None
    @staticmethod
    def _parse_deleted(element: ET.Element) -> Optional['Deleted']:
        """Parse deleted from XML element."""
        child = element.find('deleted')
        if child is not None:
            return Deleted.from_element(child)
        return None
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_responsibility(self, parent: ET.Element) -> None:
        """Serialize responsibility to XML element."""
        if self.responsibility is not None:
            parent.append(self.responsibility.to_element())
    def _serialize_phone(self, parent: ET.Element) -> None:
        """Serialize phone to XML element."""
        if self.phone is not None:
            parent.append(self.phone.to_element())
    def _serialize_fax(self, parent: ET.Element) -> None:
        """Serialize fax to XML element."""
        if self.fax is not None:
            parent.append(self.fax.to_element())
    def _serialize_sms(self, parent: ET.Element) -> None:
        """Serialize sms to XML element."""
        if self.sms is not None:
            parent.append(self.sms.to_element())
    def _serialize_email(self, parent: ET.Element) -> None:
        """Serialize email to XML element."""
        if self.email is not None:
            parent.append(self.email.to_element())
    def _serialize_url(self, parent: ET.Element) -> None:
        """Serialize url to XML element."""
        if self.url is not None:
            parent.append(self.url.to_element())
    def _serialize_skype(self, parent: ET.Element) -> None:
        """Serialize skype to XML element."""
        if self.skype is not None:
            parent.append(self.skype.to_element())
    def _serialize_facebookurl(self, parent: ET.Element) -> None:
        """Serialize facebookurl to XML element."""
        if self.facebookurl is not None:
            parent.append(self.facebookurl.to_element())
    def _serialize_msn(self, parent: ET.Element) -> None:
        """Serialize msn to XML element."""
        if self.msn is not None:
            parent.append(self.msn.to_element())
    def _serialize_description(self, parent: ET.Element) -> None:
        """Serialize description to XML element."""
        if self.description is not None:
            parent.append(self.description.to_element())
    def _serialize_deleted(self, parent: ET.Element) -> None:
        """Serialize deleted to XML element."""
        if self.deleted is not None:
            parent.append(self.deleted.to_element())


@dataclass
class Customercontacts:
    customercontact_list: List['Customercontact'] = field(default_factory=list)

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Customercontacts':
        """Create Customercontacts instance from XML element."""
        return cls(
            customercontact_list=cls._parse_customercontact_list(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Customercontacts instance to XML element."""
        element = ET.Element('customercontacts')
        self._serialize_customercontact_list(element)
        return element
    @staticmethod
    def _parse_customercontact_list(element: ET.Element) -> List['Customercontact']:
        """Parse customercontact list from XML element."""
        children = element.findall('customercontact')
        return [Customercontact.from_element(child) for child in children]
    def _serialize_customercontact_list(self, parent: ET.Element) -> None:
        """Serialize customercontact_list list to XML elements."""
        for item in self.customercontact_list:
            parent.append(item.to_element())


@dataclass
class Customer:
    id: Optional['Id'] = None
    code: Optional['Code'] = None
    customerstatus: Optional['Customerstatus'] = None
    supplierstatus: Optional['Supplierstatus'] = None
    name: Optional['Name'] = None
    searchname: Optional['Searchname'] = None
    customercategory: Optional['Customercategory'] = None
    suppliercategory: Optional['Suppliercategory'] = None
    currency: Optional['Currency'] = None
    invoicecountry: Optional['Invoicecountry'] = None
    invoiceregion: Optional['Invoiceregion'] = None
    invoicezip: Optional['Invoicezip'] = None
    invoicecity: Optional['Invoicecity'] = None
    invoicestreet: Optional['Invoicestreet'] = None
    invoicehousenumber: Optional['Invoicehousenumber'] = None
    mailcountry: Optional['Mailcountry'] = None
    mailregion: Optional['Mailregion'] = None
    mailname: Optional['Mailname'] = None
    mailzip: Optional['Mailzip'] = None
    mailcity: Optional['Mailcity'] = None
    mailstreet: Optional['Mailstreet'] = None
    mailhousenumber: Optional['Mailhousenumber'] = None
    paymentmethod: Optional['Paymentmethod'] = None
    paymentmethodtoleranceday: Optional['Paymentmethodtoleranceday'] = None
    pricecategory: Optional['Pricecategory'] = None
    pricecategoryname: Optional['Pricecategoryname'] = None
    discountpercent: Optional['Discountpercent'] = None
    transportmode: Optional['Transportmode'] = None
    taxnumber: Optional['Taxnumber'] = None
    eutaxnumber: Optional['Eutaxnumber'] = None
    bankaccount: Optional['Bankaccount'] = None
    bankaccountiban: Optional['Bankaccountiban'] = None
    bankname: Optional['Bankname'] = None
    bankswiftcode: Optional['Bankswiftcode'] = None
    contactname: Optional['Contactname'] = None
    phone: Optional['Phone'] = None
    fax: Optional['Fax'] = None
    sms: Optional['Sms'] = None
    email: Optional['Email'] = None
    webusername: Optional['Webusername'] = None
    webpassword: Optional['Webpassword'] = None
    iscompany: Optional['Iscompany'] = None
    eumembership: Optional['Eumembership'] = None
    description: Optional['Description'] = None
    deleted: Optional['Deleted'] = None
    strexa: Optional['Strexa'] = None
    strexb: Optional['Strexb'] = None
    strexc: Optional['Strexc'] = None
    strexd: Optional['Strexd'] = None
    dateexa: Optional['Dateexa'] = None
    dateexb: Optional['Dateexb'] = None
    numexa: Optional['Numexa'] = None
    numexb: Optional['Numexb'] = None
    numexc: Optional['Numexc'] = None
    boolexa: Optional['Boolexa'] = None
    boolexb: Optional['Boolexb'] = None
    lookupexa: Optional['Lookupexa'] = None
    lookupexb: Optional['Lookupexb'] = None
    lookupexc: Optional['Lookupexc'] = None
    lookupexd: Optional['Lookupexd'] = None
    customeraddresses: Optional['Customeraddresses'] = None
    customercontacts: Optional['Customercontacts'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Customer':
        """Create Customer instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            code=cls._parse_code(element),
            customerstatus=cls._parse_customerstatus(element),
            supplierstatus=cls._parse_supplierstatus(element),
            name=cls._parse_name(element),
            searchname=cls._parse_searchname(element),
            customercategory=cls._parse_customercategory(element),
            suppliercategory=cls._parse_suppliercategory(element),
            currency=cls._parse_currency(element),
            invoicecountry=cls._parse_invoicecountry(element),
            invoiceregion=cls._parse_invoiceregion(element),
            invoicezip=cls._parse_invoicezip(element),
            invoicecity=cls._parse_invoicecity(element),
            invoicestreet=cls._parse_invoicestreet(element),
            invoicehousenumber=cls._parse_invoicehousenumber(element),
            mailcountry=cls._parse_mailcountry(element),
            mailregion=cls._parse_mailregion(element),
            mailname=cls._parse_mailname(element),
            mailzip=cls._parse_mailzip(element),
            mailcity=cls._parse_mailcity(element),
            mailstreet=cls._parse_mailstreet(element),
            mailhousenumber=cls._parse_mailhousenumber(element),
            paymentmethod=cls._parse_paymentmethod(element),
            paymentmethodtoleranceday=cls._parse_paymentmethodtoleranceday(element),
            pricecategory=cls._parse_pricecategory(element),
            pricecategoryname=cls._parse_pricecategoryname(element),
            discountpercent=cls._parse_discountpercent(element),
            transportmode=cls._parse_transportmode(element),
            taxnumber=cls._parse_taxnumber(element),
            eutaxnumber=cls._parse_eutaxnumber(element),
            bankaccount=cls._parse_bankaccount(element),
            bankaccountiban=cls._parse_bankaccountiban(element),
            bankname=cls._parse_bankname(element),
            bankswiftcode=cls._parse_bankswiftcode(element),
            contactname=cls._parse_contactname(element),
            phone=cls._parse_phone(element),
            fax=cls._parse_fax(element),
            sms=cls._parse_sms(element),
            email=cls._parse_email(element),
            webusername=cls._parse_webusername(element),
            webpassword=cls._parse_webpassword(element),
            iscompany=cls._parse_iscompany(element),
            eumembership=cls._parse_eumembership(element),
            description=cls._parse_description(element),
            deleted=cls._parse_deleted(element),
            strexa=cls._parse_strexa(element),
            strexb=cls._parse_strexb(element),
            strexc=cls._parse_strexc(element),
            strexd=cls._parse_strexd(element),
            dateexa=cls._parse_dateexa(element),
            dateexb=cls._parse_dateexb(element),
            numexa=cls._parse_numexa(element),
            numexb=cls._parse_numexb(element),
            numexc=cls._parse_numexc(element),
            boolexa=cls._parse_boolexa(element),
            boolexb=cls._parse_boolexb(element),
            lookupexa=cls._parse_lookupexa(element),
            lookupexb=cls._parse_lookupexb(element),
            lookupexc=cls._parse_lookupexc(element),
            lookupexd=cls._parse_lookupexd(element),
            customeraddresses=cls._parse_customeraddresses(element),
            customercontacts=cls._parse_customercontacts(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Customer instance to XML element."""
        element = ET.Element('Customer')
        self._serialize_id(element)
        self._serialize_code(element)
        self._serialize_customerstatus(element)
        self._serialize_supplierstatus(element)
        self._serialize_name(element)
        self._serialize_searchname(element)
        self._serialize_customercategory(element)
        self._serialize_suppliercategory(element)
        self._serialize_currency(element)
        self._serialize_invoicecountry(element)
        self._serialize_invoiceregion(element)
        self._serialize_invoicezip(element)
        self._serialize_invoicecity(element)
        self._serialize_invoicestreet(element)
        self._serialize_invoicehousenumber(element)
        self._serialize_mailcountry(element)
        self._serialize_mailregion(element)
        self._serialize_mailname(element)
        self._serialize_mailzip(element)
        self._serialize_mailcity(element)
        self._serialize_mailstreet(element)
        self._serialize_mailhousenumber(element)
        self._serialize_paymentmethod(element)
        self._serialize_paymentmethodtoleranceday(element)
        self._serialize_pricecategory(element)
        self._serialize_pricecategoryname(element)
        self._serialize_discountpercent(element)
        self._serialize_transportmode(element)
        self._serialize_taxnumber(element)
        self._serialize_eutaxnumber(element)
        self._serialize_bankaccount(element)
        self._serialize_bankaccountiban(element)
        self._serialize_bankname(element)
        self._serialize_bankswiftcode(element)
        self._serialize_contactname(element)
        self._serialize_phone(element)
        self._serialize_fax(element)
        self._serialize_sms(element)
        self._serialize_email(element)
        self._serialize_webusername(element)
        self._serialize_webpassword(element)
        self._serialize_iscompany(element)
        self._serialize_eumembership(element)
        self._serialize_description(element)
        self._serialize_deleted(element)
        self._serialize_strexa(element)
        self._serialize_strexb(element)
        self._serialize_strexc(element)
        self._serialize_strexd(element)
        self._serialize_dateexa(element)
        self._serialize_dateexb(element)
        self._serialize_numexa(element)
        self._serialize_numexb(element)
        self._serialize_numexc(element)
        self._serialize_boolexa(element)
        self._serialize_boolexb(element)
        self._serialize_lookupexa(element)
        self._serialize_lookupexb(element)
        self._serialize_lookupexc(element)
        self._serialize_lookupexd(element)
        self._serialize_customeraddresses(element)
        self._serialize_customercontacts(element)
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
    def _parse_customerstatus(element: ET.Element) -> Optional['Customerstatus']:
        """Parse customerstatus from XML element."""
        child = element.find('customerstatus')
        if child is not None:
            return Customerstatus.from_element(child)
        return None
    @staticmethod
    def _parse_supplierstatus(element: ET.Element) -> Optional['Supplierstatus']:
        """Parse supplierstatus from XML element."""
        child = element.find('supplierstatus')
        if child is not None:
            return Supplierstatus.from_element(child)
        return None
    @staticmethod
    def _parse_name(element: ET.Element) -> Optional['Name']:
        """Parse name from XML element."""
        child = element.find('name')
        if child is not None:
            return Name.from_element(child)
        return None
    @staticmethod
    def _parse_searchname(element: ET.Element) -> Optional['Searchname']:
        """Parse searchname from XML element."""
        child = element.find('searchname')
        if child is not None:
            return Searchname.from_element(child)
        return None
    @staticmethod
    def _parse_customercategory(element: ET.Element) -> Optional['Customercategory']:
        """Parse customercategory from XML element."""
        child = element.find('customercategory')
        if child is not None:
            return Customercategory.from_element(child)
        return None
    @staticmethod
    def _parse_suppliercategory(element: ET.Element) -> Optional['Suppliercategory']:
        """Parse suppliercategory from XML element."""
        child = element.find('suppliercategory')
        if child is not None:
            return Suppliercategory.from_element(child)
        return None
    @staticmethod
    def _parse_currency(element: ET.Element) -> Optional['Currency']:
        """Parse currency from XML element."""
        child = element.find('currency')
        if child is not None:
            return Currency.from_element(child)
        return None
    @staticmethod
    def _parse_invoicecountry(element: ET.Element) -> Optional['Invoicecountry']:
        """Parse invoicecountry from XML element."""
        child = element.find('invoicecountry')
        if child is not None:
            return Invoicecountry.from_element(child)
        return None
    @staticmethod
    def _parse_invoiceregion(element: ET.Element) -> Optional['Invoiceregion']:
        """Parse invoiceregion from XML element."""
        child = element.find('invoiceregion')
        if child is not None:
            return Invoiceregion.from_element(child)
        return None
    @staticmethod
    def _parse_invoicezip(element: ET.Element) -> Optional['Invoicezip']:
        """Parse invoicezip from XML element."""
        child = element.find('invoicezip')
        if child is not None:
            return Invoicezip.from_element(child)
        return None
    @staticmethod
    def _parse_invoicecity(element: ET.Element) -> Optional['Invoicecity']:
        """Parse invoicecity from XML element."""
        child = element.find('invoicecity')
        if child is not None:
            return Invoicecity.from_element(child)
        return None
    @staticmethod
    def _parse_invoicestreet(element: ET.Element) -> Optional['Invoicestreet']:
        """Parse invoicestreet from XML element."""
        child = element.find('invoicestreet')
        if child is not None:
            return Invoicestreet.from_element(child)
        return None
    @staticmethod
    def _parse_invoicehousenumber(element: ET.Element) -> Optional['Invoicehousenumber']:
        """Parse invoicehousenumber from XML element."""
        child = element.find('invoicehousenumber')
        if child is not None:
            return Invoicehousenumber.from_element(child)
        return None
    @staticmethod
    def _parse_mailcountry(element: ET.Element) -> Optional['Mailcountry']:
        """Parse mailcountry from XML element."""
        child = element.find('mailcountry')
        if child is not None:
            return Mailcountry.from_element(child)
        return None
    @staticmethod
    def _parse_mailregion(element: ET.Element) -> Optional['Mailregion']:
        """Parse mailregion from XML element."""
        child = element.find('mailregion')
        if child is not None:
            return Mailregion.from_element(child)
        return None
    @staticmethod
    def _parse_mailname(element: ET.Element) -> Optional['Mailname']:
        """Parse mailname from XML element."""
        child = element.find('mailname')
        if child is not None:
            return Mailname.from_element(child)
        return None
    @staticmethod
    def _parse_mailzip(element: ET.Element) -> Optional['Mailzip']:
        """Parse mailzip from XML element."""
        child = element.find('mailzip')
        if child is not None:
            return Mailzip.from_element(child)
        return None
    @staticmethod
    def _parse_mailcity(element: ET.Element) -> Optional['Mailcity']:
        """Parse mailcity from XML element."""
        child = element.find('mailcity')
        if child is not None:
            return Mailcity.from_element(child)
        return None
    @staticmethod
    def _parse_mailstreet(element: ET.Element) -> Optional['Mailstreet']:
        """Parse mailstreet from XML element."""
        child = element.find('mailstreet')
        if child is not None:
            return Mailstreet.from_element(child)
        return None
    @staticmethod
    def _parse_mailhousenumber(element: ET.Element) -> Optional['Mailhousenumber']:
        """Parse mailhousenumber from XML element."""
        child = element.find('mailhousenumber')
        if child is not None:
            return Mailhousenumber.from_element(child)
        return None
    @staticmethod
    def _parse_paymentmethod(element: ET.Element) -> Optional['Paymentmethod']:
        """Parse paymentmethod from XML element."""
        child = element.find('paymentmethod')
        if child is not None:
            return Paymentmethod.from_element(child)
        return None
    @staticmethod
    def _parse_paymentmethodtoleranceday(element: ET.Element) -> Optional['Paymentmethodtoleranceday']:
        """Parse paymentmethodtoleranceday from XML element."""
        child = element.find('paymentmethodtoleranceday')
        if child is not None:
            return Paymentmethodtoleranceday.from_element(child)
        return None
    @staticmethod
    def _parse_pricecategory(element: ET.Element) -> Optional['Pricecategory']:
        """Parse pricecategory from XML element."""
        child = element.find('pricecategory')
        if child is not None:
            return Pricecategory.from_element(child)
        return None
    @staticmethod
    def _parse_pricecategoryname(element: ET.Element) -> Optional['Pricecategoryname']:
        """Parse pricecategoryname from XML element."""
        child = element.find('pricecategoryname')
        if child is not None:
            return Pricecategoryname.from_element(child)
        return None
    @staticmethod
    def _parse_discountpercent(element: ET.Element) -> Optional['Discountpercent']:
        """Parse discountpercent from XML element."""
        child = element.find('discountpercent')
        if child is not None:
            return Discountpercent.from_element(child)
        return None
    @staticmethod
    def _parse_transportmode(element: ET.Element) -> Optional['Transportmode']:
        """Parse transportmode from XML element."""
        child = element.find('transportmode')
        if child is not None:
            return Transportmode.from_element(child)
        return None
    @staticmethod
    def _parse_taxnumber(element: ET.Element) -> Optional['Taxnumber']:
        """Parse taxnumber from XML element."""
        child = element.find('taxnumber')
        if child is not None:
            return Taxnumber.from_element(child)
        return None
    @staticmethod
    def _parse_eutaxnumber(element: ET.Element) -> Optional['Eutaxnumber']:
        """Parse eutaxnumber from XML element."""
        child = element.find('eutaxnumber')
        if child is not None:
            return Eutaxnumber.from_element(child)
        return None
    @staticmethod
    def _parse_bankaccount(element: ET.Element) -> Optional['Bankaccount']:
        """Parse bankaccount from XML element."""
        child = element.find('bankaccount')
        if child is not None:
            return Bankaccount.from_element(child)
        return None
    @staticmethod
    def _parse_bankaccountiban(element: ET.Element) -> Optional['Bankaccountiban']:
        """Parse bankaccountiban from XML element."""
        child = element.find('bankaccountiban')
        if child is not None:
            return Bankaccountiban.from_element(child)
        return None
    @staticmethod
    def _parse_bankname(element: ET.Element) -> Optional['Bankname']:
        """Parse bankname from XML element."""
        child = element.find('bankname')
        if child is not None:
            return Bankname.from_element(child)
        return None
    @staticmethod
    def _parse_bankswiftcode(element: ET.Element) -> Optional['Bankswiftcode']:
        """Parse bankswiftcode from XML element."""
        child = element.find('bankswiftcode')
        if child is not None:
            return Bankswiftcode.from_element(child)
        return None
    @staticmethod
    def _parse_contactname(element: ET.Element) -> Optional['Contactname']:
        """Parse contactname from XML element."""
        child = element.find('contactname')
        if child is not None:
            return Contactname.from_element(child)
        return None
    @staticmethod
    def _parse_phone(element: ET.Element) -> Optional['Phone']:
        """Parse phone from XML element."""
        child = element.find('phone')
        if child is not None:
            return Phone.from_element(child)
        return None
    @staticmethod
    def _parse_fax(element: ET.Element) -> Optional['Fax']:
        """Parse fax from XML element."""
        child = element.find('fax')
        if child is not None:
            return Fax.from_element(child)
        return None
    @staticmethod
    def _parse_sms(element: ET.Element) -> Optional['Sms']:
        """Parse sms from XML element."""
        child = element.find('sms')
        if child is not None:
            return Sms.from_element(child)
        return None
    @staticmethod
    def _parse_email(element: ET.Element) -> Optional['Email']:
        """Parse email from XML element."""
        child = element.find('email')
        if child is not None:
            return Email.from_element(child)
        return None
    @staticmethod
    def _parse_webusername(element: ET.Element) -> Optional['Webusername']:
        """Parse webusername from XML element."""
        child = element.find('webusername')
        if child is not None:
            return Webusername.from_element(child)
        return None
    @staticmethod
    def _parse_webpassword(element: ET.Element) -> Optional['Webpassword']:
        """Parse webpassword from XML element."""
        child = element.find('webpassword')
        if child is not None:
            return Webpassword.from_element(child)
        return None
    @staticmethod
    def _parse_iscompany(element: ET.Element) -> Optional['Iscompany']:
        """Parse iscompany from XML element."""
        child = element.find('iscompany')
        if child is not None:
            return Iscompany.from_element(child)
        return None
    @staticmethod
    def _parse_eumembership(element: ET.Element) -> Optional['Eumembership']:
        """Parse eumembership from XML element."""
        child = element.find('eumembership')
        if child is not None:
            return Eumembership.from_element(child)
        return None
    @staticmethod
    def _parse_description(element: ET.Element) -> Optional['Description']:
        """Parse description from XML element."""
        child = element.find('description')
        if child is not None:
            return Description.from_element(child)
        return None
    @staticmethod
    def _parse_deleted(element: ET.Element) -> Optional['Deleted']:
        """Parse deleted from XML element."""
        child = element.find('deleted')
        if child is not None:
            return Deleted.from_element(child)
        return None
    @staticmethod
    def _parse_strexa(element: ET.Element) -> Optional['Strexa']:
        """Parse strexa from XML element."""
        child = element.find('strexa')
        if child is not None:
            return Strexa.from_element(child)
        return None
    @staticmethod
    def _parse_strexb(element: ET.Element) -> Optional['Strexb']:
        """Parse strexb from XML element."""
        child = element.find('strexb')
        if child is not None:
            return Strexb.from_element(child)
        return None
    @staticmethod
    def _parse_strexc(element: ET.Element) -> Optional['Strexc']:
        """Parse strexc from XML element."""
        child = element.find('strexc')
        if child is not None:
            return Strexc.from_element(child)
        return None
    @staticmethod
    def _parse_strexd(element: ET.Element) -> Optional['Strexd']:
        """Parse strexd from XML element."""
        child = element.find('strexd')
        if child is not None:
            return Strexd.from_element(child)
        return None
    @staticmethod
    def _parse_dateexa(element: ET.Element) -> Optional['Dateexa']:
        """Parse dateexa from XML element."""
        child = element.find('dateexa')
        if child is not None:
            return Dateexa.from_element(child)
        return None
    @staticmethod
    def _parse_dateexb(element: ET.Element) -> Optional['Dateexb']:
        """Parse dateexb from XML element."""
        child = element.find('dateexb')
        if child is not None:
            return Dateexb.from_element(child)
        return None
    @staticmethod
    def _parse_numexa(element: ET.Element) -> Optional['Numexa']:
        """Parse numexa from XML element."""
        child = element.find('numexa')
        if child is not None:
            return Numexa.from_element(child)
        return None
    @staticmethod
    def _parse_numexb(element: ET.Element) -> Optional['Numexb']:
        """Parse numexb from XML element."""
        child = element.find('numexb')
        if child is not None:
            return Numexb.from_element(child)
        return None
    @staticmethod
    def _parse_numexc(element: ET.Element) -> Optional['Numexc']:
        """Parse numexc from XML element."""
        child = element.find('numexc')
        if child is not None:
            return Numexc.from_element(child)
        return None
    @staticmethod
    def _parse_boolexa(element: ET.Element) -> Optional['Boolexa']:
        """Parse boolexa from XML element."""
        child = element.find('boolexa')
        if child is not None:
            return Boolexa.from_element(child)
        return None
    @staticmethod
    def _parse_boolexb(element: ET.Element) -> Optional['Boolexb']:
        """Parse boolexb from XML element."""
        child = element.find('boolexb')
        if child is not None:
            return Boolexb.from_element(child)
        return None
    @staticmethod
    def _parse_lookupexa(element: ET.Element) -> Optional['Lookupexa']:
        """Parse lookupexa from XML element."""
        child = element.find('lookupexa')
        if child is not None:
            return Lookupexa.from_element(child)
        return None
    @staticmethod
    def _parse_lookupexb(element: ET.Element) -> Optional['Lookupexb']:
        """Parse lookupexb from XML element."""
        child = element.find('lookupexb')
        if child is not None:
            return Lookupexb.from_element(child)
        return None
    @staticmethod
    def _parse_lookupexc(element: ET.Element) -> Optional['Lookupexc']:
        """Parse lookupexc from XML element."""
        child = element.find('lookupexc')
        if child is not None:
            return Lookupexc.from_element(child)
        return None
    @staticmethod
    def _parse_lookupexd(element: ET.Element) -> Optional['Lookupexd']:
        """Parse lookupexd from XML element."""
        child = element.find('lookupexd')
        if child is not None:
            return Lookupexd.from_element(child)
        return None
    @staticmethod
    def _parse_customeraddresses(element: ET.Element) -> Optional['Customeraddresses']:
        """Parse customeraddresses from XML element."""
        child = element.find('customeraddresses')
        if child is not None:
            return Customeraddresses.from_element(child)
        return None
    @staticmethod
    def _parse_customercontacts(element: ET.Element) -> Optional['Customercontacts']:
        """Parse customercontacts from XML element."""
        child = element.find('customercontacts')
        if child is not None:
            return Customercontacts.from_element(child)
        return None
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_code(self, parent: ET.Element) -> None:
        """Serialize code to XML element."""
        if self.code is not None:
            parent.append(self.code.to_element())
    def _serialize_customerstatus(self, parent: ET.Element) -> None:
        """Serialize customerstatus to XML element."""
        if self.customerstatus is not None:
            parent.append(self.customerstatus.to_element())
    def _serialize_supplierstatus(self, parent: ET.Element) -> None:
        """Serialize supplierstatus to XML element."""
        if self.supplierstatus is not None:
            parent.append(self.supplierstatus.to_element())
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())
    def _serialize_searchname(self, parent: ET.Element) -> None:
        """Serialize searchname to XML element."""
        if self.searchname is not None:
            parent.append(self.searchname.to_element())
    def _serialize_customercategory(self, parent: ET.Element) -> None:
        """Serialize customercategory to XML element."""
        if self.customercategory is not None:
            parent.append(self.customercategory.to_element())
    def _serialize_suppliercategory(self, parent: ET.Element) -> None:
        """Serialize suppliercategory to XML element."""
        if self.suppliercategory is not None:
            parent.append(self.suppliercategory.to_element())
    def _serialize_currency(self, parent: ET.Element) -> None:
        """Serialize currency to XML element."""
        if self.currency is not None:
            parent.append(self.currency.to_element())
    def _serialize_invoicecountry(self, parent: ET.Element) -> None:
        """Serialize invoicecountry to XML element."""
        if self.invoicecountry is not None:
            parent.append(self.invoicecountry.to_element())
    def _serialize_invoiceregion(self, parent: ET.Element) -> None:
        """Serialize invoiceregion to XML element."""
        if self.invoiceregion is not None:
            parent.append(self.invoiceregion.to_element())
    def _serialize_invoicezip(self, parent: ET.Element) -> None:
        """Serialize invoicezip to XML element."""
        if self.invoicezip is not None:
            parent.append(self.invoicezip.to_element())
    def _serialize_invoicecity(self, parent: ET.Element) -> None:
        """Serialize invoicecity to XML element."""
        if self.invoicecity is not None:
            parent.append(self.invoicecity.to_element())
    def _serialize_invoicestreet(self, parent: ET.Element) -> None:
        """Serialize invoicestreet to XML element."""
        if self.invoicestreet is not None:
            parent.append(self.invoicestreet.to_element())
    def _serialize_invoicehousenumber(self, parent: ET.Element) -> None:
        """Serialize invoicehousenumber to XML element."""
        if self.invoicehousenumber is not None:
            parent.append(self.invoicehousenumber.to_element())
    def _serialize_mailcountry(self, parent: ET.Element) -> None:
        """Serialize mailcountry to XML element."""
        if self.mailcountry is not None:
            parent.append(self.mailcountry.to_element())
    def _serialize_mailregion(self, parent: ET.Element) -> None:
        """Serialize mailregion to XML element."""
        if self.mailregion is not None:
            parent.append(self.mailregion.to_element())
    def _serialize_mailname(self, parent: ET.Element) -> None:
        """Serialize mailname to XML element."""
        if self.mailname is not None:
            parent.append(self.mailname.to_element())
    def _serialize_mailzip(self, parent: ET.Element) -> None:
        """Serialize mailzip to XML element."""
        if self.mailzip is not None:
            parent.append(self.mailzip.to_element())
    def _serialize_mailcity(self, parent: ET.Element) -> None:
        """Serialize mailcity to XML element."""
        if self.mailcity is not None:
            parent.append(self.mailcity.to_element())
    def _serialize_mailstreet(self, parent: ET.Element) -> None:
        """Serialize mailstreet to XML element."""
        if self.mailstreet is not None:
            parent.append(self.mailstreet.to_element())
    def _serialize_mailhousenumber(self, parent: ET.Element) -> None:
        """Serialize mailhousenumber to XML element."""
        if self.mailhousenumber is not None:
            parent.append(self.mailhousenumber.to_element())
    def _serialize_paymentmethod(self, parent: ET.Element) -> None:
        """Serialize paymentmethod to XML element."""
        if self.paymentmethod is not None:
            parent.append(self.paymentmethod.to_element())
    def _serialize_paymentmethodtoleranceday(self, parent: ET.Element) -> None:
        """Serialize paymentmethodtoleranceday to XML element."""
        if self.paymentmethodtoleranceday is not None:
            parent.append(self.paymentmethodtoleranceday.to_element())
    def _serialize_pricecategory(self, parent: ET.Element) -> None:
        """Serialize pricecategory to XML element."""
        if self.pricecategory is not None:
            parent.append(self.pricecategory.to_element())
    def _serialize_pricecategoryname(self, parent: ET.Element) -> None:
        """Serialize pricecategoryname to XML element."""
        if self.pricecategoryname is not None:
            parent.append(self.pricecategoryname.to_element())
    def _serialize_discountpercent(self, parent: ET.Element) -> None:
        """Serialize discountpercent to XML element."""
        if self.discountpercent is not None:
            parent.append(self.discountpercent.to_element())
    def _serialize_transportmode(self, parent: ET.Element) -> None:
        """Serialize transportmode to XML element."""
        if self.transportmode is not None:
            parent.append(self.transportmode.to_element())
    def _serialize_taxnumber(self, parent: ET.Element) -> None:
        """Serialize taxnumber to XML element."""
        if self.taxnumber is not None:
            parent.append(self.taxnumber.to_element())
    def _serialize_eutaxnumber(self, parent: ET.Element) -> None:
        """Serialize eutaxnumber to XML element."""
        if self.eutaxnumber is not None:
            parent.append(self.eutaxnumber.to_element())
    def _serialize_bankaccount(self, parent: ET.Element) -> None:
        """Serialize bankaccount to XML element."""
        if self.bankaccount is not None:
            parent.append(self.bankaccount.to_element())
    def _serialize_bankaccountiban(self, parent: ET.Element) -> None:
        """Serialize bankaccountiban to XML element."""
        if self.bankaccountiban is not None:
            parent.append(self.bankaccountiban.to_element())
    def _serialize_bankname(self, parent: ET.Element) -> None:
        """Serialize bankname to XML element."""
        if self.bankname is not None:
            parent.append(self.bankname.to_element())
    def _serialize_bankswiftcode(self, parent: ET.Element) -> None:
        """Serialize bankswiftcode to XML element."""
        if self.bankswiftcode is not None:
            parent.append(self.bankswiftcode.to_element())
    def _serialize_contactname(self, parent: ET.Element) -> None:
        """Serialize contactname to XML element."""
        if self.contactname is not None:
            parent.append(self.contactname.to_element())
    def _serialize_phone(self, parent: ET.Element) -> None:
        """Serialize phone to XML element."""
        if self.phone is not None:
            parent.append(self.phone.to_element())
    def _serialize_fax(self, parent: ET.Element) -> None:
        """Serialize fax to XML element."""
        if self.fax is not None:
            parent.append(self.fax.to_element())
    def _serialize_sms(self, parent: ET.Element) -> None:
        """Serialize sms to XML element."""
        if self.sms is not None:
            parent.append(self.sms.to_element())
    def _serialize_email(self, parent: ET.Element) -> None:
        """Serialize email to XML element."""
        if self.email is not None:
            parent.append(self.email.to_element())
    def _serialize_webusername(self, parent: ET.Element) -> None:
        """Serialize webusername to XML element."""
        if self.webusername is not None:
            parent.append(self.webusername.to_element())
    def _serialize_webpassword(self, parent: ET.Element) -> None:
        """Serialize webpassword to XML element."""
        if self.webpassword is not None:
            parent.append(self.webpassword.to_element())
    def _serialize_iscompany(self, parent: ET.Element) -> None:
        """Serialize iscompany to XML element."""
        if self.iscompany is not None:
            parent.append(self.iscompany.to_element())
    def _serialize_eumembership(self, parent: ET.Element) -> None:
        """Serialize eumembership to XML element."""
        if self.eumembership is not None:
            parent.append(self.eumembership.to_element())
    def _serialize_description(self, parent: ET.Element) -> None:
        """Serialize description to XML element."""
        if self.description is not None:
            parent.append(self.description.to_element())
    def _serialize_deleted(self, parent: ET.Element) -> None:
        """Serialize deleted to XML element."""
        if self.deleted is not None:
            parent.append(self.deleted.to_element())
    def _serialize_strexa(self, parent: ET.Element) -> None:
        """Serialize strexa to XML element."""
        if self.strexa is not None:
            parent.append(self.strexa.to_element())
    def _serialize_strexb(self, parent: ET.Element) -> None:
        """Serialize strexb to XML element."""
        if self.strexb is not None:
            parent.append(self.strexb.to_element())
    def _serialize_strexc(self, parent: ET.Element) -> None:
        """Serialize strexc to XML element."""
        if self.strexc is not None:
            parent.append(self.strexc.to_element())
    def _serialize_strexd(self, parent: ET.Element) -> None:
        """Serialize strexd to XML element."""
        if self.strexd is not None:
            parent.append(self.strexd.to_element())
    def _serialize_dateexa(self, parent: ET.Element) -> None:
        """Serialize dateexa to XML element."""
        if self.dateexa is not None:
            parent.append(self.dateexa.to_element())
    def _serialize_dateexb(self, parent: ET.Element) -> None:
        """Serialize dateexb to XML element."""
        if self.dateexb is not None:
            parent.append(self.dateexb.to_element())
    def _serialize_numexa(self, parent: ET.Element) -> None:
        """Serialize numexa to XML element."""
        if self.numexa is not None:
            parent.append(self.numexa.to_element())
    def _serialize_numexb(self, parent: ET.Element) -> None:
        """Serialize numexb to XML element."""
        if self.numexb is not None:
            parent.append(self.numexb.to_element())
    def _serialize_numexc(self, parent: ET.Element) -> None:
        """Serialize numexc to XML element."""
        if self.numexc is not None:
            parent.append(self.numexc.to_element())
    def _serialize_boolexa(self, parent: ET.Element) -> None:
        """Serialize boolexa to XML element."""
        if self.boolexa is not None:
            parent.append(self.boolexa.to_element())
    def _serialize_boolexb(self, parent: ET.Element) -> None:
        """Serialize boolexb to XML element."""
        if self.boolexb is not None:
            parent.append(self.boolexb.to_element())
    def _serialize_lookupexa(self, parent: ET.Element) -> None:
        """Serialize lookupexa to XML element."""
        if self.lookupexa is not None:
            parent.append(self.lookupexa.to_element())
    def _serialize_lookupexb(self, parent: ET.Element) -> None:
        """Serialize lookupexb to XML element."""
        if self.lookupexb is not None:
            parent.append(self.lookupexb.to_element())
    def _serialize_lookupexc(self, parent: ET.Element) -> None:
        """Serialize lookupexc to XML element."""
        if self.lookupexc is not None:
            parent.append(self.lookupexc.to_element())
    def _serialize_lookupexd(self, parent: ET.Element) -> None:
        """Serialize lookupexd to XML element."""
        if self.lookupexd is not None:
            parent.append(self.lookupexd.to_element())
    def _serialize_customeraddresses(self, parent: ET.Element) -> None:
        """Serialize customeraddresses to XML element."""
        if self.customeraddresses is not None:
            parent.append(self.customeraddresses.to_element())
    def _serialize_customercontacts(self, parent: ET.Element) -> None:
        """Serialize customercontacts to XML element."""
        if self.customercontacts is not None:
            parent.append(self.customercontacts.to_element())


@dataclass
class Customersup:
    customer_list: List['Customer'] = field(default_factory=list)

    @classmethod
    def from_xml_string(cls, xml_string: str) -> 'Customersup':
        """Parse XML string and create Customersup instance."""
        root = ET.fromstring(xml_string)
        return cls.from_element(root)
    
    @classmethod
    def from_element(cls, element: ET.Element) -> 'Customersup':
        """Create Customersup instance from XML element."""
        return cls(
            customer_list=cls._parse_customer_list(element)
        )
    
    def to_xml_string(self) -> str:
        """Convert Customersup instance to XML string."""
        root = self.to_element()
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    
    def to_element(self) -> ET.Element:
        """Convert Customersup instance to XML element."""
        element = ET.Element('CustomersUp')
        self._serialize_customer_list(element)
        return element
    @staticmethod
    def _parse_customer_list(element: ET.Element) -> List['Customer']:
        """Parse Customer list from XML element."""
        children = element.findall('Customer')
        return [Customer.from_element(child) for child in children]
    def _serialize_customer_list(self, parent: ET.Element) -> None:
        """Serialize customer_list list to XML elements."""
        for item in self.customer_list:
            parent.append(item.to_element())
