from dataclasses import dataclass, field
from typing import List, Optional, Any
import xml.etree.ElementTree as ET
#from lxml import objectify
import lxml.objectify as OBJ

@dataclass
class UnasResponse:
    id:     int = -1  # XML element: Id
    action: str|None = None  # XML element: Action
    status: str|None = None  # XML element: Status
    error:  str|None = None  # XML element: Error text
    group:  str|None = None  # XML element: Error text
    key:    str|None = None  # XML element: Error text
    name:   str|None = None  # XML element: Error text

    @staticmethod
    def to_stringElement(name:str, element:ET.Element) -> str|None:
        itm = element.find(name)
        if itm is not None:
            return itm.text
        return None

    @classmethod
    def from_xml_string(cls, xml:str) -> 'List[UnasResponse]':
        root = OBJ.fromstring(xml)
        #fromstring(xml)
        return [ cls.from_xml(R) for R in root.getchildren() ]

    @classmethod
    def from_xmlstr_byTag(cls, xml:str, tag:str) -> 'List[UnasResponse]':
        root = ET.fromstring(xml)
        return [ cls.from_xml(R) for R in root.findall(tag) ]

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'UnasResponse':
        instance = cls()
        instance.id     = int(instance.to_stringElement(  'Id', xml_element) or '-1')
        instance.action = instance.to_stringElement(  'Action', xml_element)
        instance.status = instance.to_stringElement(  'Status', xml_element)
        instance.error  = instance.to_stringElement(  'Error' , xml_element)
        instance.group  = instance.to_stringElement(  'Group' , xml_element)
        instance.key    = instance.to_stringElement(  'Key'   , xml_element)
        instance.name   = instance.to_stringElement(  'Name'  , xml_element)
        return instance
