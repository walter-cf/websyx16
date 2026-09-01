from dataclasses import dataclass, field
from typing import List, Optional, Any
import xml.etree.ElementTree as ET

@dataclass
class Customer:
    id: int = -1  # XML element: Id
    action: str|None = None  # XML element: Action
    status: str|None = None  # XML element: Status
    error: str|None = None  # XML element: Error text

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customer':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None and id_elem.text is not None:
            instance.id = int(id_elem.text)
        action_elem = xml_element.find('Action')
        if action_elem is not None:
            instance.action = action_elem.text
        status_elem = xml_element.find('Status')
        if status_elem is not None:
            instance.status = status_elem.text
        error_elem = xml_element.find('Error')
        if error_elem is not None:
            instance.error = error_elem.text
        return instance

@dataclass
class CustomerResponse:
    customer: List[Customer] = field( default_factory=list)

    def from_xmlStr(self, xmlStr) -> List[Customer]:
        groups : List[Customer] = []
        cgs = ET.fromstring(xmlStr)
        for group in cgs.findall("Customer"):
            groups.append(Customer.from_xml(group))
        return groups
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'CustomerResponse':
        instance = cls()
        customer_elements = xml_element.findall('Customer')
        instance.customer = [Customer.from_xml(elem) for elem in customer_elements]
        return instance
