from dataclasses import dataclass, field
from typing import List, Optional, Union
import xml.etree.ElementTree as ET
from datetime import datetime

@dataclass
class State:
    state: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'State':
        """Create State instance from XML element."""
        return cls(
            state=cls._parse_state(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert State instance to XML element."""
        element = ET.Element('State')
        self._serialize_state(element)
        return element
    @staticmethod
    def _parse_state(element: ET.Element) -> str|None:
        """Parse State from XML element."""
        elem = element.find('State')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_state(self, parent: ET.Element) -> None:
        """Serialize state to XML element."""
        if self.state is not None:
            elem = ET.SubElement(parent, 'State')
            elem.text = str(self.state)


@dataclass
class Skunew:
    sku_new: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Skunew':
        """Create Skunew instance from XML element."""
        return cls(
            sku_new=cls._parse_sku_new(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Skunew instance to XML element."""
        element = ET.Element('SkuNew')
        self._serialize_sku_new(element)
        return element
    @staticmethod
    def _parse_sku_new(element: ET.Element) -> str|None:
        """Parse SkuNew from XML element."""
        elem = element.find('SkuNew')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_sku_new(self, parent: ET.Element) -> None:
        """Serialize sku_new to XML element."""
        if self.sku_new is not None:
            elem = ET.SubElement(parent, 'SkuNew')
            elem.text = str(self.sku_new)


@dataclass
class Action:
    action: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Action':
        """Create Action instance from XML element."""
        return cls(
            action=cls._parse_action(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Action instance to XML element."""
        element = ET.Element('Action')
        self._serialize_action(element)
        return element
    @staticmethod
    def _parse_action(element: ET.Element) -> str|None:
        """Parse Action from XML element."""
        elem = element.find('Action')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_action(self, parent: ET.Element) -> None:
        """Serialize action to XML element."""
        if self.action is not None:
            elem = ET.SubElement(parent, 'Action')
            elem.text = str(self.action)


@dataclass
class Time:
    time: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Time':
        """Create Time instance from XML element."""
        return cls(
            time=cls._parse_time(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Time instance to XML element."""
        element = ET.Element('Time')
        self._serialize_time(element)
        return element
    @staticmethod
    def _parse_time(element: ET.Element) -> float|None:
        """Parse Time from XML element."""
        elem = element.find('Time')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_time(self, parent: ET.Element) -> None:
        """Serialize time to XML element."""
        if self.time is not None:
            elem = ET.SubElement(parent, 'Time')
            elem.text = str(self.time)

@dataclass
class Skuold:
    sku_old: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Skuold':
        """Create Skuold instance from XML element."""
        return cls(
            sku_old=cls._parse_sku_old(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Skuold instance to XML element."""
        element = ET.Element('SkuOld')
        self._serialize_sku_old(element)
        return element
    @staticmethod
    def _parse_sku_old(element: ET.Element) -> str|None:
        """Parse SkuOld from XML element."""
        elem = element.find('SkuOld')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_sku_old(self, parent: ET.Element) -> None:
        """Serialize sku_old to XML element."""
        if self.sku_old is not None:
            elem = ET.SubElement(parent, 'SkuOld')
            elem.text = str(self.sku_old)


@dataclass
class Event:
    action: Optional['Action'] = None
    time: Optional['Time'] = None
    sku: Optional['Sku'] = None
    sku_old: Optional['Skuold'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Event':
        """Create Event instance from XML element."""
        return cls(
            action=cls._parse_action(element),
            time=cls._parse_time(element),
            sku=cls._parse_sku(element),
            sku_old=cls._parse_sku_old(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Event instance to XML element."""
        element = ET.Element('Event')
        self._serialize_action(element)
        self._serialize_time(element)
        self._serialize_sku(element)
        self._serialize_sku_old(element)
        return element
    @staticmethod
    def _parse_action(element: ET.Element) -> Optional['Action']:
        """Parse Action from XML element."""
        child = element.find('Action')
        if child is not None:
            return Action.from_element(child)
        return None
    @staticmethod
    def _parse_time(element: ET.Element) -> Optional['Time']:
        """Parse Time from XML element."""
        child = element.find('Time')
        if child is not None:
            return Time.from_element(child)
        return None
    @staticmethod
    def _parse_sku(element: ET.Element) -> Optional['Sku']:
        """Parse Sku from XML element."""
        child = element.find('Sku')
        if child is not None:
            return Sku.from_element(child)
        return None
    @staticmethod
    def _parse_sku_old(element: ET.Element) -> Optional['Skuold']:
        """Parse SkuOld from XML element."""
        child = element.find('SkuOld')
        if child is not None:
            return Skuold.from_element(child)
        return None
    def _serialize_action(self, parent: ET.Element) -> None:
        """Serialize action to XML element."""
        if self.action is not None:
            parent.append(self.action.to_element())
    def _serialize_time(self, parent: ET.Element) -> None:
        """Serialize time to XML element."""
        if self.time is not None:
            parent.append(self.time.to_element())
    def _serialize_sku(self, parent: ET.Element) -> None:
        """Serialize sku to XML element."""
        if self.sku is not None:
            parent.append(self.sku.to_element())
    def _serialize_sku_old(self, parent: ET.Element) -> None:
        """Serialize sku_old to XML element."""
        if self.sku_old is not None:
            parent.append(self.sku_old.to_element())


@dataclass
class History:
    event: Optional['Event'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'History':
        """Create History instance from XML element."""
        return cls(
            event=cls._parse_event(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert History instance to XML element."""
        element = ET.Element('History')
        self._serialize_event(element)
        return element
    @staticmethod
    def _parse_event(element: ET.Element) -> Optional['Event']:
        """Parse Event from XML element."""
        child = element.find('Event')
        if child is not None:
            return Event.from_element(child)
        return None
    def _serialize_event(self, parent: ET.Element) -> None:
        """Serialize event to XML element."""
        if self.event is not None:
            parent.append(self.event.to_element())

@dataclass
class Statuses:
    status: Optional['Status'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Statuses':
        """Create Statuses instance from XML element."""
        return cls(
            status=cls._parse_status(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Statuses instance to XML element."""
        element = ET.Element('Statuses')
        self._serialize_status(element)
        return element
    @staticmethod
    def _parse_status(element: ET.Element) -> Optional['Status']:
        """Parse Status from XML element."""
        child = element.find('Status')
        if child is not None:
            return Status.from_element(child)
        return None
    def _serialize_status(self, parent: ET.Element) -> None:
        """Serialize status to XML element."""
        if self.status is not None:
            parent.append(self.status.to_element())


@dataclass
class Nolist:
    no_list: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Nolist':
        """Create Nolist instance from XML element."""
        return cls(
            no_list=cls._parse_no_list(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Nolist instance to XML element."""
        element = ET.Element('NoList')
        self._serialize_no_list(element)
        return element
    @staticmethod
    def _parse_no_list(element: ET.Element) -> float|None:
        """Parse NoList from XML element."""
        elem = element.find('NoList')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_no_list(self, parent: ET.Element) -> None:
        """Serialize no_list to XML element."""
        if self.no_list is not None:
            elem = ET.SubElement(parent, 'NoList')
            elem.text = str(self.no_list)


@dataclass
class Inquire:
    inquire: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Inquire':
        """Create Inquire instance from XML element."""
        return cls(
            inquire=cls._parse_inquire(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Inquire instance to XML element."""
        element = ET.Element('Inquire')
        self._serialize_inquire(element)
        return element
    @staticmethod
    def _parse_inquire(element: ET.Element) -> float|None:
        """Parse Inquire from XML element."""
        elem = element.find('Inquire')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_inquire(self, parent: ET.Element) -> None:
        """Serialize inquire to XML element."""
        if self.inquire is not None:
            elem = ET.SubElement(parent, 'Inquire')
            elem.text = str(self.inquire)


@dataclass
class Custdiscountdisable:
    cust_discount_disable: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Custdiscountdisable':
        """Create Custdiscountdisable instance from XML element."""
        return cls(
            cust_discount_disable=cls._parse_cust_discount_disable(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Custdiscountdisable instance to XML element."""
        element = ET.Element('CustDiscountDisable')
        self._serialize_cust_discount_disable(element)
        return element
    @staticmethod
    def _parse_cust_discount_disable(element: ET.Element) -> float|None:
        """Parse CustDiscountDisable from XML element."""
        elem = element.find('CustDiscountDisable')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_cust_discount_disable(self, parent: ET.Element) -> None:
        """Serialize cust_discount_disable to XML element."""
        if self.cust_discount_disable is not None:
            elem = ET.SubElement(parent, 'CustDiscountDisable')
            elem.text = str(self.cust_discount_disable)


@dataclass
class Explicit:
    explicit: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Explicit':
        """Create Explicit instance from XML element."""
        return cls(
            explicit=cls._parse_explicit(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Explicit instance to XML element."""
        element = ET.Element('Explicit')
        self._serialize_explicit(element)
        return element
    @staticmethod
    def _parse_explicit(element: ET.Element) -> float|None:
        """Parse Explicit from XML element."""
        elem = element.find('Explicit')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_explicit(self, parent: ET.Element) -> None:
        """Serialize explicit to XML element."""
        if self.explicit is not None:
            elem = ET.SubElement(parent, 'Explicit')
            elem.text = str(self.explicit)


@dataclass
class Format:
    format: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Format':
        """Create Format instance from XML element."""
        return cls(
            format=cls._parse_format(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Format instance to XML element."""
        element = ET.Element('Format')
        self._serialize_format(element)
        return element
    @staticmethod
    def _parse_format(element: ET.Element) -> str|None:
        """Parse Format from XML element."""
        elem = element.find('Format')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_format(self, parent: ET.Element) -> None:
        """Serialize format to XML element."""
        if self.format is not None:
            elem = ET.SubElement(parent, 'Format')
            elem.text = str(self.format)


@dataclass
class Forbidden:
    format_list: List['Format'] = field(default_factory=list)

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Forbidden':
        """Create Forbidden instance from XML element."""
        return cls(
            format_list=cls._parse_format_list(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Forbidden instance to XML element."""
        element = ET.Element('Forbidden')
        self._serialize_format_list(element)
        return element
    @staticmethod
    def _parse_format_list(element: ET.Element) -> List['Format']:
        """Parse Format list from XML element."""
        children = element.findall('Format')
        return [Format.from_element(child) for child in children]
    def _serialize_format_list(self, parent: ET.Element) -> None:
        """Serialize format_list list to XML elements."""
        for item in self.format_list:
            parent.append(item.to_element())


@dataclass
class Export:
    status: Optional['Status'] = None
    forbidden: Optional['Forbidden'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Export':
        """Create Export instance from XML element."""
        return cls(
            status=cls._parse_status(element),
            forbidden=cls._parse_forbidden(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Export instance to XML element."""
        element = ET.Element('Export')
        self._serialize_status(element)
        self._serialize_forbidden(element)
        return element
    @staticmethod
    def _parse_status(element: ET.Element) -> Optional['Status']:
        """Parse Status from XML element."""
        child = element.find('Status')
        if child is not None:
            return Status.from_element(child)
        return None
    @staticmethod
    def _parse_forbidden(element: ET.Element) -> Optional['Forbidden']:
        """Parse Forbidden from XML element."""
        child = element.find('Forbidden')
        if child is not None:
            return Forbidden.from_element(child)
        return None
    def _serialize_status(self, parent: ET.Element) -> None:
        """Serialize status to XML element."""
        if self.status is not None:
            parent.append(self.status.to_element())
    def _serialize_forbidden(self, parent: ET.Element) -> None:
        """Serialize forbidden to XML element."""
        if self.forbidden is not None:
            parent.append(self.forbidden.to_element())


@dataclass
class Publicinterval:
    start: Optional['Start'] = None
    end: Optional['End'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Publicinterval':
        """Create Publicinterval instance from XML element."""
        return cls(
            start=cls._parse_start(element),
            end=cls._parse_end(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Publicinterval instance to XML element."""
        element = ET.Element('PublicInterval')
        self._serialize_start(element)
        self._serialize_end(element)
        return element
    @staticmethod
    def _parse_start(element: ET.Element) -> Optional['Start']:
        """Parse Start from XML element."""
        child = element.find('Start')
        if child is not None:
            return Start.from_element(child)
        return None
    @staticmethod
    def _parse_end(element: ET.Element) -> Optional['End']:
        """Parse End from XML element."""
        child = element.find('End')
        if child is not None:
            return End.from_element(child)
        return None
    def _serialize_start(self, parent: ET.Element) -> None:
        """Serialize start to XML element."""
        if self.start is not None:
            parent.append(self.start.to_element())
    def _serialize_end(self, parent: ET.Element) -> None:
        """Serialize end to XML element."""
        if self.end is not None:
            parent.append(self.end.to_element())

@dataclass
class Minimumqty:
    minimum_qty: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Minimumqty':
        """Create Minimumqty instance from XML element."""
        return cls(
            minimum_qty=cls._parse_minimum_qty(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Minimumqty instance to XML element."""
        element = ET.Element('MinimumQty')
        self._serialize_minimum_qty(element)
        return element
    @staticmethod
    def _parse_minimum_qty(element: ET.Element) -> float|None:
        """Parse MinimumQty from XML element."""
        elem = element.find('MinimumQty')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_minimum_qty(self, parent: ET.Element) -> None:
        """Serialize minimum_qty to XML element."""
        if self.minimum_qty is not None:
            elem = ET.SubElement(parent, 'MinimumQty')
            elem.text = str(self.minimum_qty)


@dataclass
class Maximumqty:
    maximum_qty: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Maximumqty':
        """Create Maximumqty instance from XML element."""
        return cls(
            maximum_qty=cls._parse_maximum_qty(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Maximumqty instance to XML element."""
        element = ET.Element('MaximumQty')
        self._serialize_maximum_qty(element)
        return element
    @staticmethod
    def _parse_maximum_qty(element: ET.Element) -> float|None:
        """Parse MaximumQty from XML element."""
        elem = element.find('MaximumQty')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_maximum_qty(self, parent: ET.Element) -> None:
        """Serialize maximum_qty to XML element."""
        if self.maximum_qty is not None:
            elem = ET.SubElement(parent, 'MaximumQty')
            elem.text = str(self.maximum_qty)


@dataclass
class Alertqty:
    alert_qty: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Alertqty':
        """Create Alertqty instance from XML element."""
        return cls(
            alert_qty=cls._parse_alert_qty(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Alertqty instance to XML element."""
        element = ET.Element('AlertQty')
        self._serialize_alert_qty(element)
        return element
    @staticmethod
    def _parse_alert_qty(element: ET.Element) -> float|None:
        """Parse AlertQty from XML element."""
        elem = element.find('AlertQty')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_alert_qty(self, parent: ET.Element) -> None:
        """Serialize alert_qty to XML element."""
        if self.alert_qty is not None:
            elem = ET.SubElement(parent, 'AlertQty')
            elem.text = str(self.alert_qty)


@dataclass
class Unitstep:
    unit_step: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Unitstep':
        """Create Unitstep instance from XML element."""
        return cls(
            unit_step=cls._parse_unit_step(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Unitstep instance to XML element."""
        element = ET.Element('UnitStep')
        self._serialize_unit_step(element)
        return element
    @staticmethod
    def _parse_unit_step(element: ET.Element) -> float|None:
        """Parse UnitStep from XML element."""
        elem = element.find('UnitStep')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_unit_step(self, parent: ET.Element) -> None:
        """Serialize unit_step to XML element."""
        if self.unit_step is not None:
            elem = ET.SubElement(parent, 'UnitStep')
            elem.text = str(self.unit_step)


@dataclass
class Unit:
    unit: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Unit':
        """Create Unit instance from XML element."""
        return cls(
            unit=cls._parse_unit(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Unit instance to XML element."""
        element = ET.Element('Unit')
        self._serialize_unit(element)
        return element
    @staticmethod
    def _parse_unit(element: ET.Element) -> str|None:
        """Parse Unit from XML element."""
        elem = element.find('Unit')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_unit(self, parent: ET.Element) -> None:
        """Serialize unit to XML element."""
        if self.unit is not None:
            elem = ET.SubElement(parent, 'Unit')
            elem.text = str(self.unit)


@dataclass
class Alterunit:
    qty: Optional['Qty'] = None
    unit: Optional['Unit'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Alterunit':
        """Create Alterunit instance from XML element."""
        return cls(
            qty=cls._parse_qty(element),
            unit=cls._parse_unit(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Alterunit instance to XML element."""
        element = ET.Element('AlterUnit')
        self._serialize_qty(element)
        self._serialize_unit(element)
        return element
    @staticmethod
    def _parse_qty(element: ET.Element) -> Optional['Qty']:
        """Parse Qty from XML element."""
        child = element.find('Qty')
        if child is not None:
            return Qty.from_element(child)
        return None
    @staticmethod
    def _parse_unit(element: ET.Element) -> Optional['Unit']:
        """Parse Unit from XML element."""
        child = element.find('Unit')
        if child is not None:
            return Unit.from_element(child)
        return None
    def _serialize_qty(self, parent: ET.Element) -> None:
        """Serialize qty to XML element."""
        if self.qty is not None:
            parent.append(self.qty.to_element())
    def _serialize_unit(self, parent: ET.Element) -> None:
        """Serialize unit to XML element."""
        if self.unit is not None:
            parent.append(self.unit.to_element())


@dataclass
class Weight:
    weight: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Weight':
        """Create Weight instance from XML element."""
        return cls(
            weight=cls._parse_weight(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Weight instance to XML element."""
        element = ET.Element('Weight')
        self._serialize_weight(element)
        return element
    @staticmethod
    def _parse_weight(element: ET.Element) -> float|None:
        """Parse Weight from XML element."""
        elem = element.find('Weight')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_weight(self, parent: ET.Element) -> None:
        """Serialize weight to XML element."""
        if self.weight is not None:
            elem = ET.SubElement(parent, 'Weight')
            elem.text = str(self.weight)


@dataclass
class Point:
    point: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Point':
        """Create Point instance from XML element."""
        return cls(
            point=cls._parse_point(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Point instance to XML element."""
        element = ET.Element('Point')
        self._serialize_point(element)
        return element
    @staticmethod
    def _parse_point(element: ET.Element) -> float|None:
        """Parse Point from XML element."""
        elem = element.find('Point')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_point(self, parent: ET.Element) -> None:
        """Serialize point to XML element."""
        if self.point is not None:
            elem = ET.SubElement(parent, 'Point')
            elem.text = str(self.point)


@dataclass
class Buyablewithpoint:
    buyable_with_point: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Buyablewithpoint':
        """Create Buyablewithpoint instance from XML element."""
        return cls(
            buyable_with_point=cls._parse_buyable_with_point(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Buyablewithpoint instance to XML element."""
        element = ET.Element('BuyableWithPoint')
        self._serialize_buyable_with_point(element)
        return element
    @staticmethod
    def _parse_buyable_with_point(element: ET.Element) -> str|None:
        """Parse BuyableWithPoint from XML element."""
        elem = element.find('BuyableWithPoint')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_buyable_with_point(self, parent: ET.Element) -> None:
        """Serialize buyable_with_point to XML element."""
        if self.buyable_with_point is not None:
            elem = ET.SubElement(parent, 'BuyableWithPoint')
            elem.text = str(self.buyable_with_point)


@dataclass
class Short:
    short: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Short':
        """Create Short instance from XML element."""
        return cls(
            short=cls._parse_short(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Short instance to XML element."""
        element = ET.Element('Short')
        self._serialize_short(element)
        return element
    @staticmethod
    def _parse_short(element: ET.Element) -> str|None:
        """Parse Short from XML element."""
        elem = element.find('Short')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_short(self, parent: ET.Element) -> None:
        """Serialize short to XML element."""
        if self.short is not None:
            elem = ET.SubElement(parent, 'Short')
            elem.text = str(self.short)


@dataclass
class Long:
    long: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Long':
        """Create Long instance from XML element."""
        return cls(
            long=cls._parse_long(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Long instance to XML element."""
        element = ET.Element('Long')
        self._serialize_long(element)
        return element
    @staticmethod
    def _parse_long(element: ET.Element) -> str|None:
        """Parse Long from XML element."""
        elem = element.find('Long')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_long(self, parent: ET.Element) -> None:
        """Serialize long to XML element."""
        if self.long is not None:
            elem = ET.SubElement(parent, 'Long')
            elem.text = str(self.long)


@dataclass
class Vat:
    vat: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Vat':
        """Create Vat instance from XML element."""
        return cls(
            vat=cls._parse_vat(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Vat instance to XML element."""
        element = ET.Element('Vat')
        self._serialize_vat(element)
        return element
    @staticmethod
    def _parse_vat(element: ET.Element) -> str|None:
        """Parse Vat from XML element."""
        elem = element.find('Vat')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_vat(self, parent: ET.Element) -> None:
        """Serialize vat to XML element."""
        if self.vat is not None:
            elem = ET.SubElement(parent, 'Vat')
            elem.text = str(self.vat)


@dataclass
class Start:
    start: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Start':
        """Create Start instance from XML element."""
        return cls(
            start=cls._parse_start(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Start instance to XML element."""
        element = ET.Element('Start')
        self._serialize_start(element)
        return element
    @staticmethod
    def _parse_start(element: ET.Element) -> str|None:
        """Parse Start from XML element."""
        elem = element.find('Start')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_start(self, parent: ET.Element) -> None:
        """Serialize start to XML element."""
        if self.start is not None:
            elem = ET.SubElement(parent, 'Start')
            elem.text = str(self.start)


@dataclass
class End:
    # No properties found
    pass

    @classmethod
    def from_element(cls, element: ET.Element) -> 'End':
        """Create End instance from XML element."""
        return cls()
    
    def to_element(self) -> ET.Element:
        """Convert End instance to XML element."""
        element = ET.Element('End')
        return element


@dataclass
class Groupname:
    group_name: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Groupname':
        """Create Groupname instance from XML element."""
        return cls(
            group_name=cls._parse_group_name(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Groupname instance to XML element."""
        element = ET.Element('GroupName')
        self._serialize_group_name(element)
        return element
    @staticmethod
    def _parse_group_name(element: ET.Element) -> str|None:
        """Parse GroupName from XML element."""
        elem = element.find('GroupName')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_group_name(self, parent: ET.Element) -> None:
        """Serialize group_name to XML element."""
        if self.group_name is not None:
            elem = ET.SubElement(parent, 'GroupName')
            elem.text = str(self.group_name)


@dataclass
class Areaname:
    area_name: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Areaname':
        """Create Areaname instance from XML element."""
        return cls(
            area_name=cls._parse_area_name(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Areaname instance to XML element."""
        element = ET.Element('AreaName')
        self._serialize_area_name(element)
        return element
    @staticmethod
    def _parse_area_name(element: ET.Element) -> str|None:
        """Parse AreaName from XML element."""
        elem = element.find('AreaName')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_area_name(self, parent: ET.Element) -> None:
        """Serialize area_name to XML element."""
        if self.area_name is not None:
            elem = ET.SubElement(parent, 'AreaName')
            elem.text = str(self.area_name)


@dataclass
class Salenet:
    sale_net: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Salenet':
        """Create Salenet instance from XML element."""
        return cls(
            sale_net=cls._parse_sale_net(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Salenet instance to XML element."""
        element = ET.Element('SaleNet')
        self._serialize_sale_net(element)
        return element
    @staticmethod
    def _parse_sale_net(element: ET.Element) -> float|None:
        """Parse SaleNet from XML element."""
        elem = element.find('SaleNet')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_sale_net(self, parent: ET.Element) -> None:
        """Serialize sale_net to XML element."""
        if self.sale_net is not None:
            elem = ET.SubElement(parent, 'SaleNet')
            elem.text = str(self.sale_net)


@dataclass
class Salegross:
    sale_gross: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Salegross':
        """Create Salegross instance from XML element."""
        return cls(
            sale_gross=cls._parse_sale_gross(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Salegross instance to XML element."""
        element = ET.Element('SaleGross')
        self._serialize_sale_gross(element)
        return element
    @staticmethod
    def _parse_sale_gross(element: ET.Element) -> float|None:
        """Parse SaleGross from XML element."""
        elem = element.find('SaleGross')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_sale_gross(self, parent: ET.Element) -> None:
        """Serialize sale_gross to XML element."""
        if self.sale_gross is not None:
            elem = ET.SubElement(parent, 'SaleGross')
            elem.text = str(self.sale_gross)


@dataclass
class Salestart:
    sale_start: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Salestart':
        """Create Salestart instance from XML element."""
        return cls(
            sale_start=cls._parse_sale_start(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Salestart instance to XML element."""
        element = ET.Element('SaleStart')
        self._serialize_sale_start(element)
        return element
    @staticmethod
    def _parse_sale_start(element: ET.Element) -> str|None:
        """Parse SaleStart from XML element."""
        elem = element.find('SaleStart')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_sale_start(self, parent: ET.Element) -> None:
        """Serialize sale_start to XML element."""
        if self.sale_start is not None:
            elem = ET.SubElement(parent, 'SaleStart')
            elem.text = str(self.sale_start)


@dataclass
class Saleend:
    sale_end: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Saleend':
        """Create Saleend instance from XML element."""
        return cls(
            sale_end=cls._parse_sale_end(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Saleend instance to XML element."""
        element = ET.Element('SaleEnd')
        self._serialize_sale_end(element)
        return element
    @staticmethod
    def _parse_sale_end(element: ET.Element) -> str|None:
        """Parse SaleEnd from XML element."""
        elem = element.find('SaleEnd')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_sale_end(self, parent: ET.Element) -> None:
        """Serialize sale_end to XML element."""
        if self.sale_end is not None:
            elem = ET.SubElement(parent, 'SaleEnd')
            elem.text = str(self.sale_end)


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
        """Convert Currencyfilter instance to XML element."""
        element = ET.Element('Currency')
        self._serialize_currency(element)
        return element
    @staticmethod
    def _parse_currency(element: ET.Element) -> str|None:
        """Parse CurrencyFilter from XML element."""
        elem = element.find('Currency')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_currency(self, parent: ET.Element) -> None:
        """Serialize currency_filter to XML element."""
        if self.currency is not None:
            elem = ET.SubElement(parent, 'CurrencyFilter')
            elem.text = str(self.currency)

@dataclass
class Currencyfilter:
    currency_filter: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Currencyfilter':
        """Create Currencyfilter instance from XML element."""
        return cls(
            currency_filter=cls._parse_currency_filter(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Currencyfilter instance to XML element."""
        element = ET.Element('CurrencyFilter')
        self._serialize_currency_filter(element)
        return element
    @staticmethod
    def _parse_currency_filter(element: ET.Element) -> str|None:
        """Parse CurrencyFilter from XML element."""
        elem = element.find('CurrencyFilter')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_currency_filter(self, parent: ET.Element) -> None:
        """Serialize currency_filter to XML element."""
        if self.currency_filter is not None:
            elem = ET.SubElement(parent, 'CurrencyFilter')
            elem.text = str(self.currency_filter)


@dataclass
class Net:
    net: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Net':
        """Create Net instance from XML element."""
        return cls(
            net=cls._parse_net(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Net instance to XML element."""
        element = ET.Element('Net')
        self._serialize_net(element)
        return element
    @staticmethod
    def _parse_net(element: ET.Element) -> float|None:
        """Parse Net from XML element."""
        elem = element.find('Net')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_net(self, parent: ET.Element) -> None:
        """Serialize net to XML element."""
        if self.net is not None:
            elem = ET.SubElement(parent, 'Net')
            elem.text = str(self.net)


@dataclass
class Gross:
    gross: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Gross':
        """Create Gross instance from XML element."""
        return cls(
            gross=cls._parse_gross(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Gross instance to XML element."""
        element = ET.Element('Gross')
        self._serialize_gross(element)
        return element
    @staticmethod
    def _parse_gross(element: ET.Element) -> float|None:
        """Parse Gross from XML element."""
        elem = element.find('Gross')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_gross(self, parent: ET.Element) -> None:
        """Serialize gross to XML element."""
        if self.gross is not None:
            elem = ET.SubElement(parent, 'Gross')
            elem.text = str(self.gross)


@dataclass
class Price:
    type: Optional['Type'] = None
    start: Optional['Start'] = None
    end: Optional['End'] = None
    group: Optional['Group'] = None
    group_name: Optional['Groupname'] = None
    area_name: Optional['Areaname'] = None
    sale_net: Optional['Salenet'] = None
    sale_gross: Optional['Salegross'] = None
    sale_start: Optional['Salestart'] = None
    sale_end: Optional['Saleend'] = None
    currency_filter: Optional['Currencyfilter'] = None
    net: Optional['Net'] = None
    gross: Optional['Gross'] = None
    currency: Optional['Currency'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Price':
        """Create Price instance from XML element."""
        return cls(
            type=cls._parse_type(element),
            start=cls._parse_start(element),
            end=cls._parse_end(element),
            group=cls._parse_group(element),
            group_name=cls._parse_group_name(element),
            area_name=cls._parse_area_name(element),
            sale_net=cls._parse_sale_net(element),
            sale_gross=cls._parse_sale_gross(element),
            sale_start=cls._parse_sale_start(element),
            sale_end=cls._parse_sale_end(element),
            currency_filter=cls._parse_currency_filter(element),
            net=cls._parse_net(element),
            gross=cls._parse_gross(element),
            currency=cls._parse_currency(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Price instance to XML element."""
        element = ET.Element('Price')
        self._serialize_type(element)
        self._serialize_start(element)
        self._serialize_end(element)
        self._serialize_group(element)
        self._serialize_group_name(element)
        self._serialize_area_name(element)
        self._serialize_sale_net(element)
        self._serialize_sale_gross(element)
        self._serialize_sale_start(element)
        self._serialize_sale_end(element)
        self._serialize_currency_filter(element)
        self._serialize_net(element)
        self._serialize_gross(element)
        self._serialize_currency(element)
        return element
    @staticmethod
    def _parse_type(element: ET.Element) -> Optional['Type']:
        """Parse Type from XML element."""
        child = element.find('Type')
        if child is not None:
            return Type.from_element(child)
        return None
    @staticmethod
    def _parse_start(element: ET.Element) -> Optional['Start']:
        """Parse Start from XML element."""
        child = element.find('Start')
        if child is not None:
            return Start.from_element(child)
        return None
    @staticmethod
    def _parse_end(element: ET.Element) -> Optional['End']:
        """Parse End from XML element."""
        child = element.find('End')
        if child is not None:
            return End.from_element(child)
        return None
    @staticmethod
    def _parse_group(element: ET.Element) -> Optional['Group']:
        """Parse Group from XML element."""
        child = element.find('Group')
        if child is not None:
            return Group.from_element(child)
        return None
    @staticmethod
    def _parse_group_name(element: ET.Element) -> Optional['Groupname']:
        """Parse GroupName from XML element."""
        child = element.find('GroupName')
        if child is not None:
            return Groupname.from_element(child)
        return None
    @staticmethod
    def _parse_area_name(element: ET.Element) -> Optional['Areaname']:
        """Parse AreaName from XML element."""
        child = element.find('AreaName')
        if child is not None:
            return Areaname.from_element(child)
        return None
    @staticmethod
    def _parse_sale_net(element: ET.Element) -> Optional['Salenet']:
        """Parse SaleNet from XML element."""
        child = element.find('SaleNet')
        if child is not None:
            return Salenet.from_element(child)
        return None
    @staticmethod
    def _parse_sale_gross(element: ET.Element) -> Optional['Salegross']:
        """Parse SaleGross from XML element."""
        child = element.find('SaleGross')
        if child is not None:
            return Salegross.from_element(child)
        return None
    @staticmethod
    def _parse_sale_start(element: ET.Element) -> Optional['Salestart']:
        """Parse SaleStart from XML element."""
        child = element.find('SaleStart')
        if child is not None:
            return Salestart.from_element(child)
        return None
    @staticmethod
    def _parse_sale_end(element: ET.Element) -> Optional['Saleend']:
        """Parse SaleEnd from XML element."""
        child = element.find('SaleEnd')
        if child is not None:
            return Saleend.from_element(child)
        return None
    @staticmethod
    def _parse_currency_filter(element: ET.Element) -> Optional['Currencyfilter']:
        """Parse CurrencyFilter from XML element."""
        child = element.find('CurrencyFilter')
        if child is not None:
            return Currencyfilter.from_element(child)
        return None
    @staticmethod
    def _parse_net(element: ET.Element) -> Optional['Net']:
        """Parse Net from XML element."""
        child = element.find('Net')
        if child is not None:
            return Net.from_element(child)
        return None
    @staticmethod
    def _parse_gross(element: ET.Element) -> Optional['Gross']:
        """Parse Gross from XML element."""
        child = element.find('Gross')
        if child is not None:
            return Gross.from_element(child)
        return None
    @staticmethod
    def _parse_currency(element: ET.Element) -> Optional['Currency']:
        """Parse Currency from XML element."""
        child = element.find('Currency')
        if child is not None:
            return Currency.from_element(child)
        return None
    def _serialize_type(self, parent: ET.Element) -> None:
        """Serialize type to XML element."""
        if self.type is not None:
            parent.append(self.type.to_element())
    def _serialize_start(self, parent: ET.Element) -> None:
        """Serialize start to XML element."""
        if self.start is not None:
            parent.append(self.start.to_element())
    def _serialize_end(self, parent: ET.Element) -> None:
        """Serialize end to XML element."""
        if self.end is not None:
            parent.append(self.end.to_element())
    def _serialize_group(self, parent: ET.Element) -> None:
        """Serialize group to XML element."""
        if self.group is not None:
            parent.append(self.group.to_element())
    def _serialize_group_name(self, parent: ET.Element) -> None:
        """Serialize group_name to XML element."""
        if self.group_name is not None:
            parent.append(self.group_name.to_element())
    def _serialize_area_name(self, parent: ET.Element) -> None:
        """Serialize area_name to XML element."""
        if self.area_name is not None:
            parent.append(self.area_name.to_element())
    def _serialize_sale_net(self, parent: ET.Element) -> None:
        """Serialize sale_net to XML element."""
        if self.sale_net is not None:
            parent.append(self.sale_net.to_element())
    def _serialize_sale_gross(self, parent: ET.Element) -> None:
        """Serialize sale_gross to XML element."""
        if self.sale_gross is not None:
            parent.append(self.sale_gross.to_element())
    def _serialize_sale_start(self, parent: ET.Element) -> None:
        """Serialize sale_start to XML element."""
        if self.sale_start is not None:
            parent.append(self.sale_start.to_element())
    def _serialize_sale_end(self, parent: ET.Element) -> None:
        """Serialize sale_end to XML element."""
        if self.sale_end is not None:
            parent.append(self.sale_end.to_element())
    def _serialize_currency_filter(self, parent: ET.Element) -> None:
        """Serialize currency_filter to XML element."""
        if self.currency_filter is not None:
            parent.append(self.currency_filter.to_element())
    def _serialize_net(self, parent: ET.Element) -> None:
        """Serialize net to XML element."""
        if self.net is not None:
            parent.append(self.net.to_element())
    def _serialize_gross(self, parent: ET.Element) -> None:
        """Serialize gross to XML element."""
        if self.gross is not None:
            parent.append(self.gross.to_element())
    def _serialize_currency(self, parent: ET.Element) -> None:
        """Serialize currency to XML element."""
        if self.currency is not None:
            parent.append(self.currency.to_element())


@dataclass
class Prices:
    vat: Optional['Vat'] = None
    price: Optional['Price'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Prices':
        """Create Prices instance from XML element."""
        return cls(
            vat=cls._parse_vat(element),
            price=cls._parse_price(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Prices instance to XML element."""
        element = ET.Element('Prices')
        self._serialize_vat(element)
        self._serialize_price(element)
        return element
    @staticmethod
    def _parse_vat(element: ET.Element) -> Optional['Vat']:
        """Parse Vat from XML element."""
        child = element.find('Vat')
        if child is not None:
            return Vat.from_element(child)
        return None
    @staticmethod
    def _parse_price(element: ET.Element) -> Optional['Price']:
        """Parse Price from XML element."""
        child = element.find('Price')
        if child is not None:
            return Price.from_element(child)
        return None
    def _serialize_vat(self, parent: ET.Element) -> None:
        """Serialize vat to XML element."""
        if self.vat is not None:
            parent.append(self.vat.to_element())
    def _serialize_price(self, parent: ET.Element) -> None:
        """Serialize price to XML element."""
        if self.price is not None:
            parent.append(self.price.to_element())



@dataclass
class Category:
    type: Optional['Type'] = None
    id: Optional['Id'] = None
    name: Optional['Name'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Category':
        """Create Category instance from XML element."""
        return cls(
            type=cls._parse_type(element),
            id=cls._parse_id(element),
            name=cls._parse_name(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Category instance to XML element."""
        element = ET.Element('Category')
        self._serialize_type(element)
        self._serialize_id(element)
        self._serialize_name(element)
        return element
    @staticmethod
    def _parse_type(element: ET.Element) -> Optional['Type']:
        """Parse Type from XML element."""
        child = element.find('Type')
        if child is not None:
            return Type.from_element(child)
        return None
    @staticmethod
    def _parse_id(element: ET.Element) -> Optional['Id']:
        """Parse Id from XML element."""
        child = element.find('Id')
        if child is not None:
            return Id.from_element(child)
        return None
    @staticmethod
    def _parse_name(element: ET.Element) -> Optional['Name']:
        """Parse Name from XML element."""
        child = element.find('Name')
        if child is not None:
            return Name.from_element(child)
        return None
    def _serialize_type(self, parent: ET.Element) -> None:
        """Serialize type to XML element."""
        if self.type is not None:
            parent.append(self.type.to_element())
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())


@dataclass
class Categories:
    category: Optional['Category'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Categories':
        """Create Categories instance from XML element."""
        return cls(
            category=cls._parse_category(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Categories instance to XML element."""
        element = ET.Element('Categories')
        self._serialize_category(element)
        return element
    @staticmethod
    def _parse_category(element: ET.Element) -> Optional['Category']:
        """Parse Category from XML element."""
        child = element.find('Category')
        if child is not None:
            return Category.from_element(child)
        return None
    def _serialize_category(self, parent: ET.Element) -> None:
        """Serialize category to XML element."""
        if self.category is not None:
            parent.append(self.category.to_element())


@dataclass
class Defaultfilename:
    default_filename: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Defaultfilename':
        """Create Defaultfilename instance from XML element."""
        return cls(
            default_filename=cls._parse_default_filename(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Defaultfilename instance to XML element."""
        element = ET.Element('DefaultFilename')
        self._serialize_default_filename(element)
        return element
    @staticmethod
    def _parse_default_filename(element: ET.Element) -> str|None:
        """Parse DefaultFilename from XML element."""
        elem = element.find('DefaultFilename')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_default_filename(self, parent: ET.Element) -> None:
        """Serialize default_filename to XML element."""
        if self.default_filename is not None:
            elem = ET.SubElement(parent, 'DefaultFilename')
            elem.text = str(self.default_filename)


@dataclass
class Defaultalt:
    default_alt: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Defaultalt':
        """Create Defaultalt instance from XML element."""
        return cls(
            default_alt=cls._parse_default_alt(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Defaultalt instance to XML element."""
        element = ET.Element('DefaultAlt')
        self._serialize_default_alt(element)
        return element
    @staticmethod
    def _parse_default_alt(element: ET.Element) -> str|None:
        """Parse DefaultAlt from XML element."""
        elem = element.find('DefaultAlt')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_default_alt(self, parent: ET.Element) -> None:
        """Serialize default_alt to XML element."""
        if self.default_alt is not None:
            elem = ET.SubElement(parent, 'DefaultAlt')
            elem.text = str(self.default_alt)


@dataclass
class Og:
    o_g: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Og':
        """Create Og instance from XML element."""
        return cls(
            o_g=cls._parse_o_g(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Og instance to XML element."""
        element = ET.Element('OG')
        self._serialize_o_g(element)
        return element
    @staticmethod
    def _parse_o_g(element: ET.Element) -> float|None:
        """Parse OG from XML element."""
        elem = element.find('OG')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_o_g(self, parent: ET.Element) -> None:
        """Serialize o_g to XML element."""
        if self.o_g is not None:
            elem = ET.SubElement(parent, 'OG')
            elem.text = str(self.o_g)


@dataclass
class Version:
    version: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Version':
        """Create Version instance from XML element."""
        return cls(
            version=cls._parse_version(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Version instance to XML element."""
        element = ET.Element('Version')
        self._serialize_version(element)
        return element
    @staticmethod
    def _parse_version(element: ET.Element) -> float|None:
        """Parse Version from XML element."""
        elem = element.find('Version')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_version(self, parent: ET.Element) -> None:
        """Serialize version to XML element."""
        if self.version is not None:
            elem = ET.SubElement(parent, 'Version')
            elem.text = str(self.version)


@dataclass
class Sefurl:
    sef_url: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Sefurl':
        """Create Sefurl instance from XML element."""
        return cls(
            sef_url=cls._parse_sef_url(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Sefurl instance to XML element."""
        element = ET.Element('SefUrl')
        self._serialize_sef_url(element)
        return element
    @staticmethod
    def _parse_sef_url(element: ET.Element) -> str|None:
        """Parse SefUrl from XML element."""
        elem = element.find('SefUrl')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_sef_url(self, parent: ET.Element) -> None:
        """Serialize sef_url to XML element."""
        if self.sef_url is not None:
            elem = ET.SubElement(parent, 'SefUrl')
            elem.text = str(self.sef_url)


@dataclass
class Alt:
    alt: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Alt':
        """Create Alt instance from XML element."""
        return cls(
            alt=cls._parse_alt(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Alt instance to XML element."""
        element = ET.Element('Alt')
        self._serialize_alt(element)
        return element
    @staticmethod
    def _parse_alt(element: ET.Element) -> str|None:
        """Parse Alt from XML element."""
        elem = element.find('Alt')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_alt(self, parent: ET.Element) -> None:
        """Serialize alt to XML element."""
        if self.alt is not None:
            elem = ET.SubElement(parent, 'Alt')
            elem.text = str(self.alt)


@dataclass
class Image:
    type: Optional['Type'] = None
    sef_url: Optional['Sefurl'] = None
    filename: Optional['Filename'] = None
    alt: Optional['Alt'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Image':
        """Create Image instance from XML element."""
        return cls(
            type=cls._parse_type(element),
            sef_url=cls._parse_sef_url(element),
            filename=cls._parse_filename(element),
            alt=cls._parse_alt(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Image instance to XML element."""
        element = ET.Element('Image')
        self._serialize_type(element)
        self._serialize_sef_url(element)
        self._serialize_filename(element)
        self._serialize_alt(element)
        return element
    @staticmethod
    def _parse_type(element: ET.Element) -> Optional['Type']:
        """Parse Type from XML element."""
        child = element.find('Type')
        if child is not None:
            return Type.from_element(child)
        return None
    @staticmethod
    def _parse_sef_url(element: ET.Element) -> Optional['Sefurl']:
        """Parse SefUrl from XML element."""
        child = element.find('SefUrl')
        if child is not None:
            return Sefurl.from_element(child)
        return None
    @staticmethod
    def _parse_filename(element: ET.Element) -> Optional['Filename']:
        """Parse Filename from XML element."""
        child = element.find('Filename')
        if child is not None:
            return Filename.from_element(child)
        return None
    @staticmethod
    def _parse_alt(element: ET.Element) -> Optional['Alt']:
        """Parse Alt from XML element."""
        child = element.find('Alt')
        if child is not None:
            return Alt.from_element(child)
        return None
    def _serialize_type(self, parent: ET.Element) -> None:
        """Serialize type to XML element."""
        if self.type is not None:
            parent.append(self.type.to_element())
    def _serialize_sef_url(self, parent: ET.Element) -> None:
        """Serialize sef_url to XML element."""
        if self.sef_url is not None:
            parent.append(self.sef_url.to_element())
    def _serialize_filename(self, parent: ET.Element) -> None:
        """Serialize filename to XML element."""
        if self.filename is not None:
            parent.append(self.filename.to_element())
    def _serialize_alt(self, parent: ET.Element) -> None:
        """Serialize alt to XML element."""
        if self.alt is not None:
            parent.append(self.alt.to_element())


@dataclass
class Images:
    default_filename: Optional['Defaultfilename'] = None
    default_alt: Optional['Defaultalt'] = None
    o_g: Optional['Og'] = None
    version: Optional['Version'] = None
    image: Optional['Image'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Images':
        """Create Images instance from XML element."""
        return cls(
            default_filename=cls._parse_default_filename(element),
            default_alt=cls._parse_default_alt(element),
            o_g=cls._parse_o_g(element),
            version=cls._parse_version(element),
            image=cls._parse_image(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Images instance to XML element."""
        element = ET.Element('Images')
        self._serialize_default_filename(element)
        self._serialize_default_alt(element)
        self._serialize_o_g(element)
        self._serialize_version(element)
        self._serialize_image(element)
        return element
    @staticmethod
    def _parse_default_filename(element: ET.Element) -> Optional['Defaultfilename']:
        """Parse DefaultFilename from XML element."""
        child = element.find('DefaultFilename')
        if child is not None:
            return Defaultfilename.from_element(child)
        return None
    @staticmethod
    def _parse_default_alt(element: ET.Element) -> Optional['Defaultalt']:
        """Parse DefaultAlt from XML element."""
        child = element.find('DefaultAlt')
        if child is not None:
            return Defaultalt.from_element(child)
        return None
    @staticmethod
    def _parse_o_g(element: ET.Element) -> Optional['Og']:
        """Parse OG from XML element."""
        child = element.find('OG')
        if child is not None:
            return Og.from_element(child)
        return None
    @staticmethod
    def _parse_version(element: ET.Element) -> Optional['Version']:
        """Parse Version from XML element."""
        child = element.find('Version')
        if child is not None:
            return Version.from_element(child)
        return None
    @staticmethod
    def _parse_image(element: ET.Element) -> Optional['Image']:
        """Parse Image from XML element."""
        child = element.find('Image')
        if child is not None:
            return Image.from_element(child)
        return None
    def _serialize_default_filename(self, parent: ET.Element) -> None:
        """Serialize default_filename to XML element."""
        if self.default_filename is not None:
            parent.append(self.default_filename.to_element())
    def _serialize_default_alt(self, parent: ET.Element) -> None:
        """Serialize default_alt to XML element."""
        if self.default_alt is not None:
            parent.append(self.default_alt.to_element())
    def _serialize_o_g(self, parent: ET.Element) -> None:
        """Serialize o_g to XML element."""
        if self.o_g is not None:
            parent.append(self.o_g.to_element())
    def _serialize_version(self, parent: ET.Element) -> None:
        """Serialize version to XML element."""
        if self.version is not None:
            parent.append(self.version.to_element())
    def _serialize_image(self, parent: ET.Element) -> None:
        """Serialize image to XML element."""
        if self.image is not None:
            parent.append(self.image.to_element())


@dataclass
class Values:
    value_list: List['Value'] = field(default_factory=list)

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Values':
        """Create Values instance from XML element."""
        return cls(
            value_list=cls._parse_value_list(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Values instance to XML element."""
        element = ET.Element('Values')
        self._serialize_value_list(element)
        return element
    @staticmethod
    def _parse_value_list(element: ET.Element) -> List['Value']:
        """Parse Value list from XML element."""
        children = element.findall('Value')
        return [Value.from_element(child) for child in children]
    def _serialize_value_list(self, parent: ET.Element) -> None:
        """Serialize value_list list to XML elements."""
        for item in self.value_list:
            parent.append(item.to_element())

@dataclass
class Data:
    id: Optional['Id'] = None
    name: Optional['Name'] = None
    value: Optional['Value'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Data':
        """Create Data instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            name=cls._parse_name(element),
            value=cls._parse_value(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Data instance to XML element."""
        element = ET.Element('Data')
        self._serialize_id(element)
        self._serialize_name(element)
        self._serialize_value(element)
        return element
    @staticmethod
    def _parse_id(element: ET.Element) -> Optional['Id']:
        """Parse Id from XML element."""
        child = element.find('Id')
        if child is not None:
            return Id.from_element(child)
        return None
    @staticmethod
    def _parse_name(element: ET.Element) -> Optional['Name']:
        """Parse Name from XML element."""
        child = element.find('Name')
        if child is not None:
            return Name.from_element(child)
        return None
    @staticmethod
    def _parse_value(element: ET.Element) -> Optional['Value']:
        """Parse Value from XML element."""
        child = element.find('Value')
        if child is not None:
            return Value.from_element(child)
        return None
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())
    def _serialize_value(self, parent: ET.Element) -> None:
        """Serialize value to XML element."""
        if self.value is not None:
            parent.append(self.value.to_element())


@dataclass
class Datas:
    data: Optional['Data'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Datas':
        """Create Datas instance from XML element."""
        return cls(
            data=cls._parse_data(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Datas instance to XML element."""
        element = ET.Element('Datas')
        self._serialize_data(element)
        return element
    @staticmethod
    def _parse_data(element: ET.Element) -> Optional['Data']:
        """Parse Data from XML element."""
        child = element.find('Data')
        if child is not None:
            return Data.from_element(child)
        return None
    def _serialize_data(self, parent: ET.Element) -> None:
        """Serialize data to XML element."""
        if self.data is not None:
            parent.append(self.data.to_element())



@dataclass
class Group:
    group: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Group':
        """Create Group instance from XML element."""
        return cls(
            group=cls._parse_group(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Group instance to XML element."""
        element = ET.Element('Group')
        self._serialize_group(element)
        return element
    @staticmethod
    def _parse_group(element: ET.Element) -> str|None:
        """Parse Group from XML element."""
        elem = element.find('Group')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_group(self, parent: ET.Element) -> None:
        """Serialize group to XML element."""
        if self.group is not None:
            elem = ET.SubElement(parent, 'Group')
            elem.text = str(self.group)


@dataclass
class Value:
    value: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Value':
        """Create Value instance from XML element."""
        return cls(
            value=cls._parse_value(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Value instance to XML element."""
        element = ET.Element('Value')
        self._serialize_value(element)
        return element
    @staticmethod
    def _parse_value(element: ET.Element) -> str|None:
        """Parse Value from XML element."""
        elem = element.find('Value')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_value(self, parent: ET.Element) -> None:
        """Serialize value to XML element."""
        if self.value is not None:
            elem = ET.SubElement(parent, 'Value')
            elem.text = str(self.value)


@dataclass
class Before:
    before: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Before':
        """Create Before instance from XML element."""
        return cls(
            before=cls._parse_before(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Before instance to XML element."""
        element = ET.Element('Before')
        self._serialize_before(element)
        return element
    @staticmethod
    def _parse_before(element: ET.Element) -> str|None:
        """Parse Before from XML element."""
        elem = element.find('Before')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_before(self, parent: ET.Element) -> None:
        """Serialize before to XML element."""
        if self.before is not None:
            elem = ET.SubElement(parent, 'Before')
            elem.text = str(self.before)


@dataclass
class After:
    after: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'After':
        """Create After instance from XML element."""
        return cls(
            after=cls._parse_after(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert After instance to XML element."""
        element = ET.Element('After')
        self._serialize_after(element)
        return element
    @staticmethod
    def _parse_after(element: ET.Element) -> str|None:
        """Parse After from XML element."""
        elem = element.find('After')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_after(self, parent: ET.Element) -> None:
        """Serialize after to XML element."""
        if self.after is not None:
            elem = ET.SubElement(parent, 'After')
            elem.text = str(self.after)


@dataclass
class Param:
    id: Optional['Id'] = None
    type: Optional['Type'] = None
    name: Optional['Name'] = None
    group: Optional['Group'] = None
    value: Optional['Value'] = None
    before: Optional['Before'] = None
    after: Optional['After'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Param':
        """Create Param instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            type=cls._parse_type(element),
            name=cls._parse_name(element),
            group=cls._parse_group(element),
            value=cls._parse_value(element),
            before=cls._parse_before(element),
            after=cls._parse_after(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Param instance to XML element."""
        element = ET.Element('Param')
        self._serialize_id(element)
        self._serialize_type(element)
        self._serialize_name(element)
        self._serialize_group(element)
        self._serialize_value(element)
        self._serialize_before(element)
        self._serialize_after(element)
        return element
    @staticmethod
    def _parse_id(element: ET.Element) -> Optional['Id']:
        """Parse Id from XML element."""
        child = element.find('Id')
        if child is not None:
            return Id.from_element(child)
        return None
    @staticmethod
    def _parse_type(element: ET.Element) -> Optional['Type']:
        """Parse Type from XML element."""
        child = element.find('Type')
        if child is not None:
            return Type.from_element(child)
        return None
    @staticmethod
    def _parse_name(element: ET.Element) -> Optional['Name']:
        """Parse Name from XML element."""
        child = element.find('Name')
        if child is not None:
            return Name.from_element(child)
        return None
    @staticmethod
    def _parse_group(element: ET.Element) -> Optional['Group']:
        """Parse Group from XML element."""
        child = element.find('Group')
        if child is not None:
            return Group.from_element(child)
        return None
    @staticmethod
    def _parse_value(element: ET.Element) -> Optional['Value']:
        """Parse Value from XML element."""
        child = element.find('Value')
        if child is not None:
            return Value.from_element(child)
        return None
    @staticmethod
    def _parse_before(element: ET.Element) -> Optional['Before']:
        """Parse Before from XML element."""
        child = element.find('Before')
        if child is not None:
            return Before.from_element(child)
        return None
    @staticmethod
    def _parse_after(element: ET.Element) -> Optional['After']:
        """Parse After from XML element."""
        child = element.find('After')
        if child is not None:
            return After.from_element(child)
        return None
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_type(self, parent: ET.Element) -> None:
        """Serialize type to XML element."""
        if self.type is not None:
            parent.append(self.type.to_element())
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())
    def _serialize_group(self, parent: ET.Element) -> None:
        """Serialize group to XML element."""
        if self.group is not None:
            parent.append(self.group.to_element())
    def _serialize_value(self, parent: ET.Element) -> None:
        """Serialize value to XML element."""
        if self.value is not None:
            parent.append(self.value.to_element())
    def _serialize_before(self, parent: ET.Element) -> None:
        """Serialize before to XML element."""
        if self.before is not None:
            parent.append(self.before.to_element())
    def _serialize_after(self, parent: ET.Element) -> None:
        """Serialize after to XML element."""
        if self.after is not None:
            parent.append(self.after.to_element())


@dataclass
class Params:
    param: Optional['Param'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Params':
        """Create Params instance from XML element."""
        return cls(
            param=cls._parse_param(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Params instance to XML element."""
        element = ET.Element('Params')
        self._serialize_param(element)
        return element
    @staticmethod
    def _parse_param(element: ET.Element) -> Optional['Param']:
        """Parse Param from XML element."""
        child = element.find('Param')
        if child is not None:
            return Param.from_element(child)
        return None
    def _serialize_param(self, parent: ET.Element) -> None:
        """Serialize param to XML element."""
        if self.param is not None:
            parent.append(self.param.to_element())



@dataclass
class Content:
    content: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Content':
        """Create Content instance from XML element."""
        return cls(
            content=cls._parse_content(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Content instance to XML element."""
        element = ET.Element('Content')
        self._serialize_content(element)
        return element
    @staticmethod
    def _parse_content(element: ET.Element) -> str|None:
        """Parse Content from XML element."""
        elem = element.find('Content')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_content(self, parent: ET.Element) -> None:
        """Serialize content to XML element."""
        if self.content is not None:
            elem = ET.SubElement(parent, 'Content')
            elem.text = str(self.content)


@dataclass
class Additionaldata:
    id: Optional['Id'] = None
    title: Optional['Title'] = None
    content: Optional['Content'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Additionaldata':
        """Create Additionaldata instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            title=cls._parse_title(element),
            content=cls._parse_content(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Additionaldata instance to XML element."""
        element = ET.Element('AdditionalData')
        self._serialize_id(element)
        self._serialize_title(element)
        self._serialize_content(element)
        return element
    @staticmethod
    def _parse_id(element: ET.Element) -> Optional['Id']:
        """Parse Id from XML element."""
        child = element.find('Id')
        if child is not None:
            return Id.from_element(child)
        return None
    @staticmethod
    def _parse_title(element: ET.Element) -> Optional['Title']:
        """Parse Title from XML element."""
        child = element.find('Title')
        if child is not None:
            return Title.from_element(child)
        return None
    @staticmethod
    def _parse_content(element: ET.Element) -> Optional['Content']:
        """Parse Content from XML element."""
        child = element.find('Content')
        if child is not None:
            return Content.from_element(child)
        return None
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_title(self, parent: ET.Element) -> None:
        """Serialize title to XML element."""
        if self.title is not None:
            parent.append(self.title.to_element())
    def _serialize_content(self, parent: ET.Element) -> None:
        """Serialize content to XML element."""
        if self.content is not None:
            parent.append(self.content.to_element())


@dataclass
class Additionaldatas:
    additional_data: Optional['Additionaldata'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Additionaldatas':
        """Create Additionaldatas instance from XML element."""
        return cls(
            additional_data=cls._parse_additional_data(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Additionaldatas instance to XML element."""
        element = ET.Element('AdditionalDatas')
        self._serialize_additional_data(element)
        return element
    @staticmethod
    def _parse_additional_data(element: ET.Element) -> Optional['Additionaldata']:
        """Parse AdditionalData from XML element."""
        child = element.find('AdditionalData')
        if child is not None:
            return Additionaldata.from_element(child)
        return None
    def _serialize_additional_data(self, parent: ET.Element) -> None:
        """Serialize additional_data to XML element."""
        if self.additional_data is not None:
            parent.append(self.additional_data.to_element())


@dataclass
class Lower:
    lower: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Lower':
        """Create Lower instance from XML element."""
        return cls(
            lower=cls._parse_lower(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Lower instance to XML element."""
        element = ET.Element('Lower')
        self._serialize_lower(element)
        return element
    @staticmethod
    def _parse_lower(element: ET.Element) -> float|None:
        """Parse Lower from XML element."""
        elem = element.find('Lower')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_lower(self, parent: ET.Element) -> None:
        """Serialize lower to XML element."""
        if self.lower is not None:
            elem = ET.SubElement(parent, 'Lower')
            elem.text = str(self.lower)


@dataclass
class Upper:
    upper: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Upper':
        """Create Upper instance from XML element."""
        return cls(
            upper=cls._parse_upper(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Upper instance to XML element."""
        element = ET.Element('Upper')
        self._serialize_upper(element)
        return element
    @staticmethod
    def _parse_upper(element: ET.Element) -> float|None:
        """Parse Upper from XML element."""
        elem = element.find('Upper')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_upper(self, parent: ET.Element) -> None:
        """Serialize upper to XML element."""
        if self.upper is not None:
            elem = ET.SubElement(parent, 'Upper')
            elem.text = str(self.upper)

@dataclass
class Discount:
    discount: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Discount':
        """Create Discount instance from XML element."""
        return cls(
            discount=cls._parse_discount(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Discount instance to XML element."""
        element = ET.Element('Discount')
        self._serialize_discount(element)
        return element
    @staticmethod
    def _parse_discount(element: ET.Element) -> str|None:
        """Parse Discount from XML element."""
        elem = element.find('Discount')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_discount(self, parent: ET.Element) -> None:
        """Serialize discount to XML element."""
        if self.discount is not None:
            elem = ET.SubElement(parent, 'Discount')
            elem.text = str(self.discount)


@dataclass
class Step:
    limit: Optional['Limit'] = None
    discount: Optional['Discount'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Step':
        """Create Step instance from XML element."""
        return cls(
            limit=cls._parse_limit(element),
            discount=cls._parse_discount(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Step instance to XML element."""
        element = ET.Element('Step')
        self._serialize_limit(element)
        self._serialize_discount(element)
        return element
    @staticmethod
    def _parse_limit(element: ET.Element) -> Optional['Limit']:
        """Parse Limit from XML element."""
        child = element.find('Limit')
        if child is not None:
            return Limit.from_element(child)
        return None
    @staticmethod
    def _parse_discount(element: ET.Element) -> Optional['Discount']:
        """Parse Discount from XML element."""
        child = element.find('Discount')
        if child is not None:
            return Discount.from_element(child)
        return None
    def _serialize_limit(self, parent: ET.Element) -> None:
        """Serialize limit to XML element."""
        if self.limit is not None:
            parent.append(self.limit.to_element())
    def _serialize_discount(self, parent: ET.Element) -> None:
        """Serialize discount to XML element."""
        if self.discount is not None:
            parent.append(self.discount.to_element())


@dataclass
class Qtydiscount:
    step: Optional['Step'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Qtydiscount':
        """Create Qtydiscount instance from XML element."""
        return cls(
            step=cls._parse_step(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Qtydiscount instance to XML element."""
        element = ET.Element('QtyDiscount')
        self._serialize_step(element)
        return element
    @staticmethod
    def _parse_step(element: ET.Element) -> Optional['Step']:
        """Parse Step from XML element."""
        child = element.find('Step')
        if child is not None:
            return Step.from_element(child)
        return None
    def _serialize_step(self, parent: ET.Element) -> None:
        """Serialize step to XML element."""
        if self.step is not None:
            parent.append(self.step.to_element())


@dataclass
class Additionalproduct:
    id: Optional['Id'] = None
    sku: Optional['Sku'] = None
    name: Optional['Name'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Additionalproduct':
        """Create Additionalproduct instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            sku=cls._parse_sku(element),
            name=cls._parse_name(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Additionalproduct instance to XML element."""
        element = ET.Element('AdditionalProduct')
        self._serialize_id(element)
        self._serialize_sku(element)
        self._serialize_name(element)
        return element
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
        """Parse Name from XML element."""
        child = element.find('Name')
        if child is not None:
            return Name.from_element(child)
        return None
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_sku(self, parent: ET.Element) -> None:
        """Serialize sku to XML element."""
        if self.sku is not None:
            parent.append(self.sku.to_element())
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())


@dataclass
class Additionalproducts:
    additional_product: Optional['Additionalproduct'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Additionalproducts':
        """Create Additionalproducts instance from XML element."""
        return cls(
            additional_product=cls._parse_additional_product(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Additionalproducts instance to XML element."""
        element = ET.Element('AdditionalProducts')
        self._serialize_additional_product(element)
        return element
    @staticmethod
    def _parse_additional_product(element: ET.Element) -> Optional['Additionalproduct']:
        """Parse AdditionalProduct from XML element."""
        child = element.find('AdditionalProduct')
        if child is not None:
            return Additionalproduct.from_element(child)
        return None
    def _serialize_additional_product(self, parent: ET.Element) -> None:
        """Serialize additional_product to XML element."""
        if self.additional_product is not None:
            parent.append(self.additional_product.to_element())

@dataclass
class Similarproduct:
    id: Optional['Id'] = None
    sku: Optional['Sku'] = None
    name: Optional['Name'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Similarproduct':
        """Create Similarproduct instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            sku=cls._parse_sku(element),
            name=cls._parse_name(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Similarproduct instance to XML element."""
        element = ET.Element('SimilarProduct')
        self._serialize_id(element)
        self._serialize_sku(element)
        self._serialize_name(element)
        return element
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
        """Parse Name from XML element."""
        child = element.find('Name')
        if child is not None:
            return Name.from_element(child)
        return None
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_sku(self, parent: ET.Element) -> None:
        """Serialize sku to XML element."""
        if self.sku is not None:
            parent.append(self.sku.to_element())
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())


@dataclass
class Similarproducts:
    similar_product: Optional['Similarproduct'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Similarproducts':
        """Create Similarproducts instance from XML element."""
        return cls(
            similar_product=cls._parse_similar_product(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Similarproducts instance to XML element."""
        element = ET.Element('SimilarProducts')
        self._serialize_similar_product(element)
        return element
    @staticmethod
    def _parse_similar_product(element: ET.Element) -> Optional['Similarproduct']:
        """Parse SimilarProduct from XML element."""
        child = element.find('SimilarProduct')
        if child is not None:
            return Similarproduct.from_element(child)
        return None
    def _serialize_similar_product(self, parent: ET.Element) -> None:
        """Serialize similar_product to XML element."""
        if self.similar_product is not None:
            parent.append(self.similar_product.to_element())


@dataclass
class Active:
    active: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Active':
        """Create Active instance from XML element."""
        return cls(
            active=cls._parse_active(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Active instance to XML element."""
        element = ET.Element('Active')
        self._serialize_active(element)
        return element
    @staticmethod
    def _parse_active(element: ET.Element) -> float|None:
        """Parse Active from XML element."""
        elem = element.find('Active')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_active(self, parent: ET.Element) -> None:
        """Serialize active to XML element."""
        if self.active is not None:
            elem = ET.SubElement(parent, 'Active')
            elem.text = str(self.active)


@dataclass
class Empty:
    empty: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Empty':
        """Create Empty instance from XML element."""
        return cls(
            empty=cls._parse_empty(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Empty instance to XML element."""
        element = ET.Element('Empty')
        self._serialize_empty(element)
        return element
    @staticmethod
    def _parse_empty(element: ET.Element) -> float|None:
        """Parse Empty from XML element."""
        elem = element.find('Empty')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_empty(self, parent: ET.Element) -> None:
        """Serialize empty to XML element."""
        if self.empty is not None:
            elem = ET.SubElement(parent, 'Empty')
            elem.text = str(self.empty)

@dataclass
class Status:
    active: Optional['Active'] = None
    empty: Optional['Empty'] = None
    variant: Optional['Variant'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Status':
        """Create Status instance from XML element."""
        return cls(
            active=cls._parse_active(element),
            empty=cls._parse_empty(element),
            variant=cls._parse_variant(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Status instance to XML element."""
        element = ET.Element('Status')
        self._serialize_active(element)
        self._serialize_empty(element)
        self._serialize_variant(element)
        return element
    @staticmethod
    def _parse_active(element: ET.Element) -> Optional['Active']:
        """Parse Active from XML element."""
        child = element.find('Active')
        if child is not None:
            return Active.from_element(child)
        return None
    @staticmethod
    def _parse_empty(element: ET.Element) -> Optional['Empty']:
        """Parse Empty from XML element."""
        child = element.find('Empty')
        if child is not None:
            return Empty.from_element(child)
        return None
    @staticmethod
    def _parse_variant(element: ET.Element) -> Optional['Variant']:
        """Parse Variant from XML element."""
        child = element.find('Variant')
        if child is not None:
            return Variant.from_element(child)
        return None
    def _serialize_active(self, parent: ET.Element) -> None:
        """Serialize active to XML element."""
        if self.active is not None:
            parent.append(self.active.to_element())
    def _serialize_empty(self, parent: ET.Element) -> None:
        """Serialize empty to XML element."""
        if self.empty is not None:
            parent.append(self.empty.to_element())
    def _serialize_variant(self, parent: ET.Element) -> None:
        """Serialize variant to XML element."""
        if self.variant is not None:
            parent.append(self.variant.to_element())


@dataclass
class Variant:
    variant: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Variant':
        """Create Variant instance from XML element."""
        return cls(
            variant=cls._parse_variant(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Variant instance to XML element."""
        element = ET.Element('Variant')
        self._serialize_variant(element)
        return element
    @staticmethod
    def _parse_variant(element: ET.Element) -> str|None:
        """Parse Variant from XML element."""
        elem = element.find('Variant')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_variant(self, parent: ET.Element) -> None:
        """Serialize variant to XML element."""
        if self.variant is not None:
            elem = ET.SubElement(parent, 'Variant')
            elem.text = str(self.variant)


@dataclass
class Variants:
    variant_list: List['Variant'] = field(default_factory=list)

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Variants':
        """Create Variants instance from XML element."""
        return cls(
            variant_list=cls._parse_variant_list(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Variants instance to XML element."""
        element = ET.Element('Variants')
        self._serialize_variant_list(element)
        return element
    @staticmethod
    def _parse_variant_list(element: ET.Element) -> List['Variant']:
        """Parse Variant list from XML element."""
        children = element.findall('Variant')
        return [Variant.from_element(child) for child in children]
    def _serialize_variant_list(self, parent: ET.Element) -> None:
        """Serialize variant_list list to XML elements."""
        for item in self.variant_list:
            parent.append(item.to_element())


@dataclass
class Stock:
    variants: Optional['Variants'] = None
    qty: Optional['Qty'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Stock':
        """Create Stock instance from XML element."""
        return cls(
            variants=cls._parse_variants(element),
            qty=cls._parse_qty(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Stock instance to XML element."""
        element = ET.Element('Stock')
        self._serialize_variants(element)
        self._serialize_qty(element)
        return element
    @staticmethod
    def _parse_variants(element: ET.Element) -> Optional['Variants']:
        """Parse Variants from XML element."""
        child = element.find('Variants')
        if child is not None:
            return Variants.from_element(child)
        return None
    @staticmethod
    def _parse_qty(element: ET.Element) -> Optional['Qty']:
        """Parse Qty from XML element."""
        child = element.find('Qty')
        if child is not None:
            return Qty.from_element(child)
        return None
    def _serialize_variants(self, parent: ET.Element) -> None:
        """Serialize variants to XML element."""
        if self.variants is not None:
            parent.append(self.variants.to_element())
    def _serialize_qty(self, parent: ET.Element) -> None:
        """Serialize qty to XML element."""
        if self.qty is not None:
            parent.append(self.qty.to_element())


@dataclass
class Stocks:
    status: Optional['Status'] = None
    stock: Optional['Stock'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Stocks':
        """Create Stocks instance from XML element."""
        return cls(
            status=cls._parse_status(element),
            stock=cls._parse_stock(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Stocks instance to XML element."""
        element = ET.Element('Stocks')
        self._serialize_status(element)
        self._serialize_stock(element)
        return element
    @staticmethod
    def _parse_status(element: ET.Element) -> Optional['Status']:
        """Parse Status from XML element."""
        child = element.find('Status')
        if child is not None:
            return Status.from_element(child)
        return None
    @staticmethod
    def _parse_stock(element: ET.Element) -> Optional['Stock']:
        """Parse Stock from XML element."""
        child = element.find('Stock')
        if child is not None:
            return Stock.from_element(child)
        return None
    def _serialize_status(self, parent: ET.Element) -> None:
        """Serialize status to XML element."""
        if self.status is not None:
            parent.append(self.status.to_element())
    def _serialize_stock(self, parent: ET.Element) -> None:
        """Serialize stock to XML element."""
        if self.stock is not None:
            parent.append(self.stock.to_element())


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
        element = ET.Element('Url')
        self._serialize_url(element)
        return element
    @staticmethod
    def _parse_url(element: ET.Element) -> str|None:
        """Parse Url from XML element."""
        elem = element.find('Url')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_url(self, parent: ET.Element) -> None:
        """Serialize url to XML element."""
        if self.url is not None:
            elem = ET.SubElement(parent, 'Url')
            elem.text = str(self.url)


@dataclass
class Limit:
    limit: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Limit':
        """Create Limit instance from XML element."""
        return cls(
            limit=cls._parse_limit(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Limit instance to XML element."""
        element = ET.Element('Limit')
        self._serialize_limit(element)
        return element
    @staticmethod
    def _parse_limit(element: ET.Element) -> str|None:
        """Parse Limit from XML element."""
        elem = element.find('Limit')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_limit(self, parent: ET.Element) -> None:
        """Serialize limit to XML element."""
        if self.limit is not None:
            elem = ET.SubElement(parent, 'Limit')
            elem.text = str(self.limit)


@dataclass
class Filename:
    filename: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Filename':
        """Create Filename instance from XML element."""
        return cls(
            filename=cls._parse_filename(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Filename instance to XML element."""
        element = ET.Element('Filename')
        self._serialize_filename(element)
        return element
    @staticmethod
    def _parse_filename(element: ET.Element) -> str|None:
        """Parse Filename from XML element."""
        elem = element.find('Filename')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_filename(self, parent: ET.Element) -> None:
        """Serialize filename to XML element."""
        if self.filename is not None:
            elem = ET.SubElement(parent, 'Filename')
            elem.text = str(self.filename)


@dataclass
class Onlinecontent:
    url: Optional['Url'] = None
    limit: Optional['Limit'] = None
    filename: Optional['Filename'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Onlinecontent':
        """Create Onlinecontent instance from XML element."""
        return cls(
            url=cls._parse_url(element),
            limit=cls._parse_limit(element),
            filename=cls._parse_filename(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Onlinecontent instance to XML element."""
        element = ET.Element('OnlineContent')
        self._serialize_url(element)
        self._serialize_limit(element)
        self._serialize_filename(element)
        return element
    @staticmethod
    def _parse_url(element: ET.Element) -> Optional['Url']:
        """Parse Url from XML element."""
        child = element.find('Url')
        if child is not None:
            return Url.from_element(child)
        return None
    @staticmethod
    def _parse_limit(element: ET.Element) -> Optional['Limit']:
        """Parse Limit from XML element."""
        child = element.find('Limit')
        if child is not None:
            return Limit.from_element(child)
        return None
    @staticmethod
    def _parse_filename(element: ET.Element) -> Optional['Filename']:
        """Parse Filename from XML element."""
        child = element.find('Filename')
        if child is not None:
            return Filename.from_element(child)
        return None
    def _serialize_url(self, parent: ET.Element) -> None:
        """Serialize url to XML element."""
        if self.url is not None:
            parent.append(self.url.to_element())
    def _serialize_limit(self, parent: ET.Element) -> None:
        """Serialize limit to XML element."""
        if self.limit is not None:
            parent.append(self.limit.to_element())
    def _serialize_filename(self, parent: ET.Element) -> None:
        """Serialize filename to XML element."""
        if self.filename is not None:
            parent.append(self.filename.to_element())


@dataclass
class Id:
    id: float|None = None

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
    def _parse_id(element: ET.Element) -> float|None:
        """Parse Id from XML element."""
        elem = element.find('Id')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
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
        elem = element.find('Name')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            elem = ET.SubElement(parent, 'Name')
            elem.text = str(self.name)


@dataclass
class Plusservice:
    id: Optional['Id'] = None
    name: Optional['Name'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Plusservice':
        """Create Plusservice instance from XML element."""
        return cls(
            id=cls._parse_id(element),
            name=cls._parse_name(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Plusservice instance to XML element."""
        element = ET.Element('PlusService')
        self._serialize_id(element)
        self._serialize_name(element)
        return element
    @staticmethod
    def _parse_id(element: ET.Element) -> Optional['Id']:
        """Parse Id from XML element."""
        child = element.find('Id')
        if child is not None:
            return Id.from_element(child)
        return None
    @staticmethod
    def _parse_name(element: ET.Element) -> Optional['Name']:
        """Parse Name from XML element."""
        child = element.find('Name')
        if child is not None:
            return Name.from_element(child)
        return None
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())


@dataclass
class Plusservices:
    plus_service: Optional['Plusservice'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Plusservices':
        """Create Plusservices instance from XML element."""
        return cls(
            plus_service=cls._parse_plus_service(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Plusservices instance to XML element."""
        element = ET.Element('PlusServices')
        self._serialize_plus_service(element)
        return element
    @staticmethod
    def _parse_plus_service(element: ET.Element) -> Optional['Plusservice']:
        """Parse PlusService from XML element."""
        child = element.find('PlusService')
        if child is not None:
            return Plusservice.from_element(child)
        return None
    def _serialize_plus_service(self, parent: ET.Element) -> None:
        """Serialize plus_service to XML element."""
        if self.plus_service is not None:
            parent.append(self.plus_service.to_element())


@dataclass
class Type:
    type: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Type':
        """Create Type instance from XML element."""
        return cls(
            type=cls._parse_type(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Type instance to XML element."""
        element = ET.Element('Type')
        self._serialize_type(element)
        return element
    @staticmethod
    def _parse_type(element: ET.Element) -> str|None:
        """Parse Type from XML element."""
        elem = element.find('Type')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_type(self, parent: ET.Element) -> None:
        """Serialize type to XML element."""
        if self.type is not None:
            elem = ET.SubElement(parent, 'Type')
            elem.text = str(self.type)


@dataclass
class Parent:
    parent: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Parent':
        """Create Parent instance from XML element."""
        return cls(
            parent=cls._parse_parent(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Parent instance to XML element."""
        element = ET.Element('Parent')
        self._serialize_parent(element)
        return element
    @staticmethod
    def _parse_parent(element: ET.Element) -> str|None:
        """Parse Parent from XML element."""
        elem = element.find('Parent')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_parent(self, parent: ET.Element) -> None:
        """Serialize parent to XML element."""
        if self.parent is not None:
            elem = ET.SubElement(parent, 'Parent')
            elem.text = str(self.parent)


@dataclass
class Display:
    display: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Display':
        """Create Display instance from XML element."""
        return cls(
            display=cls._parse_display(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Display instance to XML element."""
        element = ET.Element('Display')
        self._serialize_display(element)
        return element
    @staticmethod
    def _parse_display(element: ET.Element) -> float|None:
        """Parse Display from XML element."""
        elem = element.find('Display')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_display(self, parent: ET.Element) -> None:
        """Serialize display to XML element."""
        if self.display is not None:
            elem = ET.SubElement(parent, 'Display')
            elem.text = str(self.display)


@dataclass
class Order:
    order: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Order':
        """Create Order instance from XML element."""
        return cls(
            order=cls._parse_order(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Order instance to XML element."""
        element = ET.Element('Order')
        self._serialize_order(element)
        return element
    @staticmethod
    def _parse_order(element: ET.Element) -> float|None:
        """Parse Order from XML element."""
        elem = element.find('Order')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_order(self, parent: ET.Element) -> None:
        """Serialize order to XML element."""
        if self.order is not None:
            elem = ET.SubElement(parent, 'Order')
            elem.text = str(self.order)


@dataclass
class Types:
    type: Optional['Type'] = None
    parent: Optional['Parent'] = None
    display: Optional['Display'] = None
    order: Optional['Order'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Types':
        """Create Types instance from XML element."""
        return cls(
            type=cls._parse_type(element),
            parent=cls._parse_parent(element),
            display=cls._parse_display(element),
            order=cls._parse_order(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Types instance to XML element."""
        element = ET.Element('Types')
        self._serialize_type(element)
        self._serialize_parent(element)
        self._serialize_display(element)
        self._serialize_order(element)
        return element
    @staticmethod
    def _parse_type(element: ET.Element) -> Optional['Type']:
        """Parse Type from XML element."""
        child = element.find('Type')
        if child is not None:
            return Type.from_element(child)
        return None
    @staticmethod
    def _parse_parent(element: ET.Element) -> Optional['Parent']:
        """Parse Parent from XML element."""
        child = element.find('Parent')
        if child is not None:
            return Parent.from_element(child)
        return None
    @staticmethod
    def _parse_display(element: ET.Element) -> Optional['Display']:
        """Parse Display from XML element."""
        child = element.find('Display')
        if child is not None:
            return Display.from_element(child)
        return None
    @staticmethod
    def _parse_order(element: ET.Element) -> Optional['Order']:
        """Parse Order from XML element."""
        child = element.find('Order')
        if child is not None:
            return Order.from_element(child)
        return None
    def _serialize_type(self, parent: ET.Element) -> None:
        """Serialize type to XML element."""
        if self.type is not None:
            parent.append(self.type.to_element())
    def _serialize_parent(self, parent: ET.Element) -> None:
        """Serialize parent to XML element."""
        if self.parent is not None:
            parent.append(self.parent.to_element())
    def _serialize_display(self, parent: ET.Element) -> None:
        """Serialize display to XML element."""
        if self.display is not None:
            parent.append(self.display.to_element())
    def _serialize_order(self, parent: ET.Element) -> None:
        """Serialize order to XML element."""
        if self.order is not None:
            parent.append(self.order.to_element())


@dataclass
class Packageproduct:
    package_product: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Packageproduct':
        """Create Packageproduct instance from XML element."""
        return cls(
            package_product=cls._parse_package_product(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Packageproduct instance to XML element."""
        element = ET.Element('PackageProduct')
        self._serialize_package_product(element)
        return element
    @staticmethod
    def _parse_package_product(element: ET.Element) -> str|None:
        """Parse PackageProduct from XML element."""
        elem = element.find('PackageProduct')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_package_product(self, parent: ET.Element) -> None:
        """Serialize package_product to XML element."""
        if self.package_product is not None:
            elem = ET.SubElement(parent, 'PackageProduct')
            elem.text = str(self.package_product)


@dataclass
class Sku:
    sku: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Sku':
        """Create Sku instance from XML element."""
        return cls(
            sku=cls._parse_sku(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Sku instance to XML element."""
        element = ET.Element('Sku')
        self._serialize_sku(element)
        return element
    @staticmethod
    def _parse_sku(element: ET.Element) -> str|None:
        """Parse Sku from XML element."""
        elem = element.find('Sku')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_sku(self, parent: ET.Element) -> None:
        """Serialize sku to XML element."""
        if self.sku is not None:
            elem = ET.SubElement(parent, 'Sku')
            elem.text = str(self.sku)


@dataclass
class Qty:
    qty: float|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Qty':
        """Create Qty instance from XML element."""
        return cls(
            qty=cls._parse_qty(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Qty instance to XML element."""
        element = ET.Element('Qty')
        self._serialize_qty(element)
        return element
    @staticmethod
    def _parse_qty(element: ET.Element) -> float|None:
        """Parse Qty from XML element."""
        elem = element.find('Qty')
        if elem is not None and elem.text:
            return float(elem.text)
        return None
    def _serialize_qty(self, parent: ET.Element) -> None:
        """Serialize qty to XML element."""
        if self.qty is not None:
            elem = ET.SubElement(parent, 'Qty')
            elem.text = str(self.qty)


@dataclass
class Component:
    sku: Optional['Sku'] = None
    qty: Optional['Qty'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Component':
        """Create Component instance from XML element."""
        return cls(
            sku=cls._parse_sku(element),
            qty=cls._parse_qty(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Component instance to XML element."""
        element = ET.Element('Component')
        self._serialize_sku(element)
        self._serialize_qty(element)
        return element
    @staticmethod
    def _parse_sku(element: ET.Element) -> Optional['Sku']:
        """Parse Sku from XML element."""
        child = element.find('Sku')
        if child is not None:
            return Sku.from_element(child)
        return None
    @staticmethod
    def _parse_qty(element: ET.Element) -> Optional['Qty']:
        """Parse Qty from XML element."""
        child = element.find('Qty')
        if child is not None:
            return Qty.from_element(child)
        return None
    def _serialize_sku(self, parent: ET.Element) -> None:
        """Serialize sku to XML element."""
        if self.sku is not None:
            parent.append(self.sku.to_element())
    def _serialize_qty(self, parent: ET.Element) -> None:
        """Serialize qty to XML element."""
        if self.qty is not None:
            parent.append(self.qty.to_element())


@dataclass
class Packagecomponents:
    component: Optional['Component'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Packagecomponents':
        """Create Packagecomponents instance from XML element."""
        return cls(
            component=cls._parse_component(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Packagecomponents instance to XML element."""
        element = ET.Element('PackageComponents')
        self._serialize_component(element)
        return element
    @staticmethod
    def _parse_component(element: ET.Element) -> Optional['Component']:
        """Parse Component from XML element."""
        child = element.find('Component')
        if child is not None:
            return Component.from_element(child)
        return None
    def _serialize_component(self, parent: ET.Element) -> None:
        """Serialize component to XML element."""
        if self.component is not None:
            parent.append(self.component.to_element())

@dataclass
class Meta:
    keywords: Optional['Keywords'] = None
    description: Optional['Description'] = None
    title: Optional['Title'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Meta':
        """Create Meta instance from XML element."""
        return cls(
            keywords=cls._parse_keywords(element),
            description=cls._parse_description(element),
            title=cls._parse_title(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Meta instance to XML element."""
        element = ET.Element('Meta')
        self._serialize_keywords(element)
        self._serialize_description(element)
        self._serialize_title(element)
        return element
    @staticmethod
    def _parse_keywords(element: ET.Element) -> Optional['Keywords']:
        """Parse Keywords from XML element."""
        child = element.find('Keywords')
        if child is not None:
            return Keywords.from_element(child)
        return None
    @staticmethod
    def _parse_description(element: ET.Element) -> Optional['Description']:
        """Parse Description from XML element."""
        child = element.find('Description')
        if child is not None:
            return Description.from_element(child)
        return None
    @staticmethod
    def _parse_title(element: ET.Element) -> Optional['Title']:
        """Parse Title from XML element."""
        child = element.find('Title')
        if child is not None:
            return Title.from_element(child)
        return None
    def _serialize_keywords(self, parent: ET.Element) -> None:
        """Serialize keywords to XML element."""
        if self.keywords is not None:
            parent.append(self.keywords.to_element())
    def _serialize_description(self, parent: ET.Element) -> None:
        """Serialize description to XML element."""
        if self.description is not None:
            parent.append(self.description.to_element())
    def _serialize_title(self, parent: ET.Element) -> None:
        """Serialize title to XML element."""
        if self.title is not None:
            parent.append(self.title.to_element())


@dataclass
class Keywords:
    keywords: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Keywords':
        """Create Keywords instance from XML element."""
        return cls(
            keywords=cls._parse_keywords(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Keywords instance to XML element."""
        element = ET.Element('Keywords')
        self._serialize_keywords(element)
        return element
    @staticmethod
    def _parse_keywords(element: ET.Element) -> str|None:
        """Parse Keywords from XML element."""
        elem = element.find('Keywords')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_keywords(self, parent: ET.Element) -> None:
        """Serialize keywords to XML element."""
        if self.keywords is not None:
            elem = ET.SubElement(parent, 'Keywords')
            elem.text = str(self.keywords)


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
        element = ET.Element('Description')
        self._serialize_description(element)
        return element
    @staticmethod
    def _parse_description(element: ET.Element) -> str|None:
        """Parse Description from XML element."""
        elem = element.find('Description')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_description(self, parent: ET.Element) -> None:
        """Serialize description to XML element."""
        if self.description is not None:
            elem = ET.SubElement(parent, 'Description')
            elem.text = str(self.description)


@dataclass
class Title:
    title: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Title':
        """Create Title instance from XML element."""
        return cls(
            title=cls._parse_title(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Title instance to XML element."""
        element = ET.Element('Title')
        self._serialize_title(element)
        return element
    @staticmethod
    def _parse_title(element: ET.Element) -> str|None:
        """Parse Title from XML element."""
        elem = element.find('Title')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_title(self, parent: ET.Element) -> None:
        """Serialize title to XML element."""
        if self.title is not None:
            elem = ET.SubElement(parent, 'Title')
            elem.text = str(self.title)


@dataclass
class Automaticmeta:
    keywords: Optional['Keywords'] = None
    description: Optional['Description'] = None
    title: Optional['Title'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Automaticmeta':
        """Create Automaticmeta instance from XML element."""
        return cls(
            keywords=cls._parse_keywords(element),
            description=cls._parse_description(element),
            title=cls._parse_title(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Automaticmeta instance to XML element."""
        element = ET.Element('AutomaticMeta')
        self._serialize_keywords(element)
        self._serialize_description(element)
        self._serialize_title(element)
        return element
    @staticmethod
    def _parse_keywords(element: ET.Element) -> Optional['Keywords']:
        """Parse Keywords from XML element."""
        child = element.find('Keywords')
        if child is not None:
            return Keywords.from_element(child)
        return None
    @staticmethod
    def _parse_description(element: ET.Element) -> Optional['Description']:
        """Parse Description from XML element."""
        child = element.find('Description')
        if child is not None:
            return Description.from_element(child)
        return None
    @staticmethod
    def _parse_title(element: ET.Element) -> Optional['Title']:
        """Parse Title from XML element."""
        child = element.find('Title')
        if child is not None:
            return Title.from_element(child)
        return None
    def _serialize_keywords(self, parent: ET.Element) -> None:
        """Serialize keywords to XML element."""
        if self.keywords is not None:
            parent.append(self.keywords.to_element())
    def _serialize_description(self, parent: ET.Element) -> None:
        """Serialize description to XML element."""
        if self.description is not None:
            parent.append(self.description.to_element())
    def _serialize_title(self, parent: ET.Element) -> None:
        """Serialize title to XML element."""
        if self.title is not None:
            parent.append(self.title.to_element())


@dataclass
class UnasProduct:
    action: Optional['Action'] = None
    state: Optional['State'] = None
    id: Optional['Id'] = None
    sku: Optional['Sku'] = None
    sku_new: Optional['Skunew'] = None
    history: Optional['History'] = None
    statuses: Optional['Statuses'] = None
    no_list: Optional['Nolist'] = None
    inquire: Optional['Inquire'] = None
    cust_discount_disable: Optional['Custdiscountdisable'] = None
    explicit: Optional['Explicit'] = None
    export: Optional['Export'] = None
    public_interval: Optional['Publicinterval'] = None
    name: Optional['Name'] = None
    unit: Optional['Unit'] = None
    minimum_qty: Optional['Minimumqty'] = None
    maximum_qty: Optional['Maximumqty'] = None
    alert_qty: Optional['Alertqty'] = None
    unit_step: Optional['Unitstep'] = None
    alter_unit: Optional['Alterunit'] = None
    weight: Optional['Weight'] = None
    point: Optional['Point'] = None
    buyable_with_point: Optional['Buyablewithpoint'] = None
    description: Optional['Description'] = None
    prices: Optional['Prices'] = None
    categories: Optional['Categories'] = None
    url: Optional['Url'] = None
    sef_url: Optional['Sefurl'] = None
    images: Optional['Images'] = None
    variants: Optional['Variants'] = None
    datas: Optional['Datas'] = None
    params: Optional['Params'] = None
    additional_datas: Optional['Additionaldatas'] = None
    qty_discount: Optional['Qtydiscount'] = None
    additional_products: Optional['Additionalproducts'] = None
    similar_products: Optional['Similarproducts'] = None
    stocks: Optional['Stocks'] = None
    online_content: Optional['Onlinecontent'] = None
    plus_services: Optional['Plusservices'] = None
    types: Optional['Types'] = None
    package_product: Optional['Packageproduct'] = None
    package_components: Optional['Packagecomponents'] = None
    meta: Optional['Meta'] = None
    automatic_meta: Optional['Automaticmeta'] = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'UnasProduct':
        """Create Product instance from XML element."""
        return cls(
            action=cls._parse_action(element),
            state=cls._parse_state(element),
            id=cls._parse_id(element),
            sku=cls._parse_sku(element),
            sku_new=cls._parse_sku_new(element),
            history=cls._parse_history(element),
            statuses=cls._parse_statuses(element),
            no_list=cls._parse_no_list(element),
            inquire=cls._parse_inquire(element),
            cust_discount_disable=cls._parse_cust_discount_disable(element),
            explicit=cls._parse_explicit(element),
            export=cls._parse_export(element),
            public_interval=cls._parse_public_interval(element),
            name=cls._parse_name(element),
            unit=cls._parse_unit(element),
            minimum_qty=cls._parse_minimum_qty(element),
            maximum_qty=cls._parse_maximum_qty(element),
            alert_qty=cls._parse_alert_qty(element),
            unit_step=cls._parse_unit_step(element),
            alter_unit=cls._parse_alter_unit(element),
            weight=cls._parse_weight(element),
            point=cls._parse_point(element),
            buyable_with_point=cls._parse_buyable_with_point(element),
            description=cls._parse_description(element),
            prices=cls._parse_prices(element),
            categories=cls._parse_categories(element),
            url=cls._parse_url(element),
            sef_url=cls._parse_sef_url(element),
            images=cls._parse_images(element),
            variants=cls._parse_variants(element),
            datas=cls._parse_datas(element),
            params=cls._parse_params(element),
            additional_datas=cls._parse_additional_datas(element),
            qty_discount=cls._parse_qty_discount(element),
            additional_products=cls._parse_additional_products(element),
            similar_products=cls._parse_similar_products(element),
            stocks=cls._parse_stocks(element),
            online_content=cls._parse_online_content(element),
            plus_services=cls._parse_plus_services(element),
            types=cls._parse_types(element),
            package_product=cls._parse_package_product(element),
            package_components=cls._parse_package_components(element),
            meta=cls._parse_meta(element),
            automatic_meta=cls._parse_automatic_meta(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Product instance to XML element."""
        element = ET.Element('Product')
        self._serialize_action(element)
        self._serialize_state(element)
        self._serialize_id(element)
        self._serialize_sku(element)
        self._serialize_sku_new(element)
        self._serialize_history(element)
        self._serialize_statuses(element)
        self._serialize_no_list(element)
        self._serialize_inquire(element)
        self._serialize_cust_discount_disable(element)
        self._serialize_explicit(element)
        self._serialize_export(element)
        self._serialize_public_interval(element)
        self._serialize_name(element)
        self._serialize_unit(element)
        self._serialize_minimum_qty(element)
        self._serialize_maximum_qty(element)
        self._serialize_alert_qty(element)
        self._serialize_unit_step(element)
        self._serialize_alter_unit(element)
        self._serialize_weight(element)
        self._serialize_point(element)
        self._serialize_buyable_with_point(element)
        self._serialize_description(element)
        self._serialize_prices(element)
        self._serialize_categories(element)
        self._serialize_url(element)
        self._serialize_sef_url(element)
        self._serialize_images(element)
        self._serialize_variants(element)
        self._serialize_datas(element)
        self._serialize_params(element)
        self._serialize_additional_datas(element)
        self._serialize_qty_discount(element)
        self._serialize_additional_products(element)
        self._serialize_similar_products(element)
        self._serialize_stocks(element)
        self._serialize_online_content(element)
        self._serialize_plus_services(element)
        self._serialize_types(element)
        self._serialize_package_product(element)
        self._serialize_package_components(element)
        self._serialize_meta(element)
        self._serialize_automatic_meta(element)
        return element
    @staticmethod
    def _parse_action(element: ET.Element) -> Optional['Action']:
        """Parse Action from XML element."""
        child = element.find('Action')
        if child is not None:
            return Action.from_element(child)
        return None
    @staticmethod
    def _parse_state(element: ET.Element) -> Optional['State']:
        """Parse State from XML element."""
        child = element.find('State')
        if child is not None:
            return State.from_element(child)
        return None
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
    def _parse_sku_new(element: ET.Element) -> Optional['Skunew']:
        """Parse SkuNew from XML element."""
        child = element.find('SkuNew')
        if child is not None:
            return Skunew.from_element(child)
        return None
    @staticmethod
    def _parse_history(element: ET.Element) -> Optional['History']:
        """Parse History from XML element."""
        child = element.find('History')
        if child is not None:
            return History.from_element(child)
        return None
    @staticmethod
    def _parse_statuses(element: ET.Element) -> Optional['Statuses']:
        """Parse Statuses from XML element."""
        child = element.find('Statuses')
        if child is not None:
            return Statuses.from_element(child)
        return None
    @staticmethod
    def _parse_no_list(element: ET.Element) -> Optional['Nolist']:
        """Parse NoList from XML element."""
        child = element.find('NoList')
        if child is not None:
            return Nolist.from_element(child)
        return None
    @staticmethod
    def _parse_inquire(element: ET.Element) -> Optional['Inquire']:
        """Parse Inquire from XML element."""
        child = element.find('Inquire')
        if child is not None:
            return Inquire.from_element(child)
        return None
    @staticmethod
    def _parse_cust_discount_disable(element: ET.Element) -> Optional['Custdiscountdisable']:
        """Parse CustDiscountDisable from XML element."""
        child = element.find('CustDiscountDisable')
        if child is not None:
            return Custdiscountdisable.from_element(child)
        return None
    @staticmethod
    def _parse_explicit(element: ET.Element) -> Optional['Explicit']:
        """Parse Explicit from XML element."""
        child = element.find('Explicit')
        if child is not None:
            return Explicit.from_element(child)
        return None
    @staticmethod
    def _parse_export(element: ET.Element) -> Optional['Export']:
        """Parse Export from XML element."""
        child = element.find('Export')
        if child is not None:
            return Export.from_element(child)
        return None
    @staticmethod
    def _parse_public_interval(element: ET.Element) -> Optional['Publicinterval']:
        """Parse PublicInterval from XML element."""
        child = element.find('PublicInterval')
        if child is not None:
            return Publicinterval.from_element(child)
        return None
    @staticmethod
    def _parse_name(element: ET.Element) -> Optional['Name']:
        """Parse Name from XML element."""
        child = element.find('Name')
        if child is not None:
            return Name.from_element(child)
        return None
    @staticmethod
    def _parse_unit(element: ET.Element) -> Optional['Unit']:
        """Parse Unit from XML element."""
        child = element.find('Unit')
        if child is not None:
            return Unit.from_element(child)
        return None
    @staticmethod
    def _parse_minimum_qty(element: ET.Element) -> Optional['Minimumqty']:
        """Parse MinimumQty from XML element."""
        child = element.find('MinimumQty')
        if child is not None:
            return Minimumqty.from_element(child)
        return None
    @staticmethod
    def _parse_maximum_qty(element: ET.Element) -> Optional['Maximumqty']:
        """Parse MaximumQty from XML element."""
        child = element.find('MaximumQty')
        if child is not None:
            return Maximumqty.from_element(child)
        return None
    @staticmethod
    def _parse_alert_qty(element: ET.Element) -> Optional['Alertqty']:
        """Parse AlertQty from XML element."""
        child = element.find('AlertQty')
        if child is not None:
            return Alertqty.from_element(child)
        return None
    @staticmethod
    def _parse_unit_step(element: ET.Element) -> Optional['Unitstep']:
        """Parse UnitStep from XML element."""
        child = element.find('UnitStep')
        if child is not None:
            return Unitstep.from_element(child)
        return None
    @staticmethod
    def _parse_alter_unit(element: ET.Element) -> Optional['Alterunit']:
        """Parse AlterUnit from XML element."""
        child = element.find('AlterUnit')
        if child is not None:
            return Alterunit.from_element(child)
        return None
    @staticmethod
    def _parse_weight(element: ET.Element) -> Optional['Weight']:
        """Parse Weight from XML element."""
        child = element.find('Weight')
        if child is not None:
            return Weight.from_element(child)
        return None
    @staticmethod
    def _parse_point(element: ET.Element) -> Optional['Point']:
        """Parse Point from XML element."""
        child = element.find('Point')
        if child is not None:
            return Point.from_element(child)
        return None
    @staticmethod
    def _parse_buyable_with_point(element: ET.Element) -> Optional['Buyablewithpoint']:
        """Parse BuyableWithPoint from XML element."""
        child = element.find('BuyableWithPoint')
        if child is not None:
            return Buyablewithpoint.from_element(child)
        return None
    @staticmethod
    def _parse_description(element: ET.Element) -> Optional['Description']:
        """Parse Description from XML element."""
        child = element.find('Description')
        if child is not None:
            return Description.from_element(child)
        return None
    @staticmethod
    def _parse_prices(element: ET.Element) -> Optional['Prices']:
        """Parse Prices from XML element."""
        child = element.find('Prices')
        if child is not None:
            return Prices.from_element(child)
        return None
    @staticmethod
    def _parse_categories(element: ET.Element) -> Optional['Categories']:
        """Parse Categories from XML element."""
        child = element.find('Categories')
        if child is not None:
            return Categories.from_element(child)
        return None
    @staticmethod
    def _parse_url(element: ET.Element) -> Optional['Url']:
        """Parse Url from XML element."""
        child = element.find('Url')
        if child is not None:
            return Url.from_element(child)
        return None
    @staticmethod
    def _parse_sef_url(element: ET.Element) -> Optional['Sefurl']:
        """Parse SefUrl from XML element."""
        child = element.find('SefUrl')
        if child is not None:
            return Sefurl.from_element(child)
        return None
    @staticmethod
    def _parse_images(element: ET.Element) -> Optional['Images']:
        """Parse Images from XML element."""
        child = element.find('Images')
        if child is not None:
            return Images.from_element(child)
        return None
    @staticmethod
    def _parse_variants(element: ET.Element) -> Optional['Variants']:
        """Parse Variants from XML element."""
        child = element.find('Variants')
        if child is not None:
            return Variants.from_element(child)
        return None
    @staticmethod
    def _parse_datas(element: ET.Element) -> Optional['Datas']:
        """Parse Datas from XML element."""
        child = element.find('Datas')
        if child is not None:
            return Datas.from_element(child)
        return None
    @staticmethod
    def _parse_params(element: ET.Element) -> Optional['Params']:
        """Parse Params from XML element."""
        child = element.find('Params')
        if child is not None:
            return Params.from_element(child)
        return None
    @staticmethod
    def _parse_additional_datas(element: ET.Element) -> Optional['Additionaldatas']:
        """Parse AdditionalDatas from XML element."""
        child = element.find('AdditionalDatas')
        if child is not None:
            return Additionaldatas.from_element(child)
        return None
    @staticmethod
    def _parse_qty_discount(element: ET.Element) -> Optional['Qtydiscount']:
        """Parse QtyDiscount from XML element."""
        child = element.find('QtyDiscount')
        if child is not None:
            return Qtydiscount.from_element(child)
        return None
    @staticmethod
    def _parse_additional_products(element: ET.Element) -> Optional['Additionalproducts']:
        """Parse AdditionalProducts from XML element."""
        child = element.find('AdditionalProducts')
        if child is not None:
            return Additionalproducts.from_element(child)
        return None
    @staticmethod
    def _parse_similar_products(element: ET.Element) -> Optional['Similarproducts']:
        """Parse SimilarProducts from XML element."""
        child = element.find('SimilarProducts')
        if child is not None:
            return Similarproducts.from_element(child)
        return None
    @staticmethod
    def _parse_stocks(element: ET.Element) -> Optional['Stocks']:
        """Parse Stocks from XML element."""
        child = element.find('Stocks')
        if child is not None:
            return Stocks.from_element(child)
        return None
    @staticmethod
    def _parse_online_content(element: ET.Element) -> Optional['Onlinecontent']:
        """Parse OnlineContent from XML element."""
        child = element.find('OnlineContent')
        if child is not None:
            return Onlinecontent.from_element(child)
        return None
    @staticmethod
    def _parse_plus_services(element: ET.Element) -> Optional['Plusservices']:
        """Parse PlusServices from XML element."""
        child = element.find('PlusServices')
        if child is not None:
            return Plusservices.from_element(child)
        return None
    @staticmethod
    def _parse_types(element: ET.Element) -> Optional['Types']:
        """Parse Types from XML element."""
        child = element.find('Types')
        if child is not None:
            return Types.from_element(child)
        return None
    @staticmethod
    def _parse_package_product(element: ET.Element) -> Optional['Packageproduct']:
        """Parse PackageProduct from XML element."""
        child = element.find('PackageProduct')
        if child is not None:
            return Packageproduct.from_element(child)
        return None
    @staticmethod
    def _parse_package_components(element: ET.Element) -> Optional['Packagecomponents']:
        """Parse PackageComponents from XML element."""
        child = element.find('PackageComponents')
        if child is not None:
            return Packagecomponents.from_element(child)
        return None
    @staticmethod
    def _parse_meta(element: ET.Element) -> Optional['Meta']:
        """Parse Meta from XML element."""
        child = element.find('Meta')
        if child is not None:
            return Meta.from_element(child)
        return None
    @staticmethod
    def _parse_automatic_meta(element: ET.Element) -> Optional['Automaticmeta']:
        """Parse AutomaticMeta from XML element."""
        child = element.find('AutomaticMeta')
        if child is not None:
            return Automaticmeta.from_element(child)
        return None
    def _serialize_action(self, parent: ET.Element) -> None:
        """Serialize action to XML element."""
        if self.action is not None:
            parent.append(self.action.to_element())
    def _serialize_state(self, parent: ET.Element) -> None:
        """Serialize state to XML element."""
        if self.state is not None:
            parent.append(self.state.to_element())
    def _serialize_id(self, parent: ET.Element) -> None:
        """Serialize id to XML element."""
        if self.id is not None:
            parent.append(self.id.to_element())
    def _serialize_sku(self, parent: ET.Element) -> None:
        """Serialize sku to XML element."""
        if self.sku is not None:
            parent.append(self.sku.to_element())
    def _serialize_sku_new(self, parent: ET.Element) -> None:
        """Serialize sku_new to XML element."""
        if self.sku_new is not None:
            parent.append(self.sku_new.to_element())
    def _serialize_history(self, parent: ET.Element) -> None:
        """Serialize history to XML element."""
        if self.history is not None:
            parent.append(self.history.to_element())
    def _serialize_statuses(self, parent: ET.Element) -> None:
        """Serialize statuses to XML element."""
        if self.statuses is not None:
            parent.append(self.statuses.to_element())
    def _serialize_no_list(self, parent: ET.Element) -> None:
        """Serialize no_list to XML element."""
        if self.no_list is not None:
            parent.append(self.no_list.to_element())
    def _serialize_inquire(self, parent: ET.Element) -> None:
        """Serialize inquire to XML element."""
        if self.inquire is not None:
            parent.append(self.inquire.to_element())
    def _serialize_cust_discount_disable(self, parent: ET.Element) -> None:
        """Serialize cust_discount_disable to XML element."""
        if self.cust_discount_disable is not None:
            parent.append(self.cust_discount_disable.to_element())
    def _serialize_explicit(self, parent: ET.Element) -> None:
        """Serialize explicit to XML element."""
        if self.explicit is not None:
            parent.append(self.explicit.to_element())
    def _serialize_export(self, parent: ET.Element) -> None:
        """Serialize export to XML element."""
        if self.export is not None:
            parent.append(self.export.to_element())
    def _serialize_public_interval(self, parent: ET.Element) -> None:
        """Serialize public_interval to XML element."""
        if self.public_interval is not None:
            parent.append(self.public_interval.to_element())
    def _serialize_name(self, parent: ET.Element) -> None:
        """Serialize name to XML element."""
        if self.name is not None:
            parent.append(self.name.to_element())
    def _serialize_unit(self, parent: ET.Element) -> None:
        """Serialize unit to XML element."""
        if self.unit is not None:
            parent.append(self.unit.to_element())
    def _serialize_minimum_qty(self, parent: ET.Element) -> None:
        """Serialize minimum_qty to XML element."""
        if self.minimum_qty is not None:
            parent.append(self.minimum_qty.to_element())
    def _serialize_maximum_qty(self, parent: ET.Element) -> None:
        """Serialize maximum_qty to XML element."""
        if self.maximum_qty is not None:
            parent.append(self.maximum_qty.to_element())
    def _serialize_alert_qty(self, parent: ET.Element) -> None:
        """Serialize alert_qty to XML element."""
        if self.alert_qty is not None:
            parent.append(self.alert_qty.to_element())
    def _serialize_unit_step(self, parent: ET.Element) -> None:
        """Serialize unit_step to XML element."""
        if self.unit_step is not None:
            parent.append(self.unit_step.to_element())
    def _serialize_alter_unit(self, parent: ET.Element) -> None:
        """Serialize alter_unit to XML element."""
        if self.alter_unit is not None:
            parent.append(self.alter_unit.to_element())
    def _serialize_weight(self, parent: ET.Element) -> None:
        """Serialize weight to XML element."""
        if self.weight is not None:
            parent.append(self.weight.to_element())
    def _serialize_point(self, parent: ET.Element) -> None:
        """Serialize point to XML element."""
        if self.point is not None:
            parent.append(self.point.to_element())
    def _serialize_buyable_with_point(self, parent: ET.Element) -> None:
        """Serialize buyable_with_point to XML element."""
        if self.buyable_with_point is not None:
            parent.append(self.buyable_with_point.to_element())
    def _serialize_description(self, parent: ET.Element) -> None:
        """Serialize description to XML element."""
        if self.description is not None:
            parent.append(self.description.to_element())
    def _serialize_prices(self, parent: ET.Element) -> None:
        """Serialize prices to XML element."""
        if self.prices is not None:
            parent.append(self.prices.to_element())
    def _serialize_categories(self, parent: ET.Element) -> None:
        """Serialize categories to XML element."""
        if self.categories is not None:
            parent.append(self.categories.to_element())
    def _serialize_url(self, parent: ET.Element) -> None:
        """Serialize url to XML element."""
        if self.url is not None:
            parent.append(self.url.to_element())
    def _serialize_sef_url(self, parent: ET.Element) -> None:
        """Serialize sef_url to XML element."""
        if self.sef_url is not None:
            parent.append(self.sef_url.to_element())
    def _serialize_images(self, parent: ET.Element) -> None:
        """Serialize images to XML element."""
        if self.images is not None:
            parent.append(self.images.to_element())
    def _serialize_variants(self, parent: ET.Element) -> None:
        """Serialize variants to XML element."""
        if self.variants is not None:
            parent.append(self.variants.to_element())
    def _serialize_datas(self, parent: ET.Element) -> None:
        """Serialize datas to XML element."""
        if self.datas is not None:
            parent.append(self.datas.to_element())
    def _serialize_params(self, parent: ET.Element) -> None:
        """Serialize params to XML element."""
        if self.params is not None:
            parent.append(self.params.to_element())
    def _serialize_additional_datas(self, parent: ET.Element) -> None:
        """Serialize additional_datas to XML element."""
        if self.additional_datas is not None:
            parent.append(self.additional_datas.to_element())
    def _serialize_qty_discount(self, parent: ET.Element) -> None:
        """Serialize qty_discount to XML element."""
        if self.qty_discount is not None:
            parent.append(self.qty_discount.to_element())
    def _serialize_additional_products(self, parent: ET.Element) -> None:
        """Serialize additional_products to XML element."""
        if self.additional_products is not None:
            parent.append(self.additional_products.to_element())
    def _serialize_similar_products(self, parent: ET.Element) -> None:
        """Serialize similar_products to XML element."""
        if self.similar_products is not None:
            parent.append(self.similar_products.to_element())
    def _serialize_stocks(self, parent: ET.Element) -> None:
        """Serialize stocks to XML element."""
        if self.stocks is not None:
            parent.append(self.stocks.to_element())
    def _serialize_online_content(self, parent: ET.Element) -> None:
        """Serialize online_content to XML element."""
        if self.online_content is not None:
            parent.append(self.online_content.to_element())
    def _serialize_plus_services(self, parent: ET.Element) -> None:
        """Serialize plus_services to XML element."""
        if self.plus_services is not None:
            parent.append(self.plus_services.to_element())
    def _serialize_types(self, parent: ET.Element) -> None:
        """Serialize types to XML element."""
        if self.types is not None:
            parent.append(self.types.to_element())
    def _serialize_package_product(self, parent: ET.Element) -> None:
        """Serialize package_product to XML element."""
        if self.package_product is not None:
            parent.append(self.package_product.to_element())
    def _serialize_package_components(self, parent: ET.Element) -> None:
        """Serialize package_components to XML element."""
        if self.package_components is not None:
            parent.append(self.package_components.to_element())
    def _serialize_meta(self, parent: ET.Element) -> None:
        """Serialize meta to XML element."""
        if self.meta is not None:
            parent.append(self.meta.to_element())
    def _serialize_automatic_meta(self, parent: ET.Element) -> None:
        """Serialize automatic_meta to XML element."""
        if self.automatic_meta is not None:
            parent.append(self.automatic_meta.to_element())


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


