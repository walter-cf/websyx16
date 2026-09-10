from dataclasses import dataclass, field
from typing import List, Optional, Any
import xml.etree.ElementTree as ET

@dataclass
class Discount:
    total: int | None = None  # XML element: Total
    direct: int| None  = None  # XML element: Direct

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Discount':
        instance = cls()
        total_elem = xml_element.find('Total')
        if total_elem is not None:
            instance.total = int(total_elem.text or 0)
        direct_elem = xml_element.find('Direct')
        if direct_elem is not None:
            instance.direct = int(direct_elem.text or 0)
        return instance

@dataclass
class Param:
    id: int|None = None  # XML element: Id
    name: str|None = None  # XML element: Name
    value: str|None = None  # XML element: Value

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Param':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or 0)
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        value_elem = xml_element.find('Value')
        if value_elem is not None:
            instance.value = value_elem.text
        return instance

@dataclass
class Params:
    param: List[Param] = field( default_factory=list)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Params':
        instance = cls()
        param_elements = xml_element.findall('Param')
        instance.param = [Param.from_xml(elem) for elem in param_elements]
        return instance


@dataclass
class Other:
    name: str|None = None  # XML element: Name
    z_i_p: int|None = None  # XML element: ZIP
    city: str|None = None  # XML element: City
    street: str|None = None  # XML element: Street
    county: str|None = None  # XML element: County
    country: str|None = None  # XML element: Country
    country_code: str|None = None  # XML element: CountryCode

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Other':
        instance = cls()
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        z_i_p_elem = xml_element.find('ZIP')
        if z_i_p_elem is not None:
            instance.z_i_p = int(z_i_p_elem.text or 0)
        city_elem = xml_element.find('City')
        if city_elem is not None:
            instance.city = city_elem.text
        street_elem = xml_element.find('Street')
        if street_elem is not None:
            instance.street = street_elem.text
        county_elem = xml_element.find('County')
        if county_elem is not None:
            instance.county = county_elem.text
        country_elem = xml_element.find('Country')
        if country_elem is not None:
            instance.country = country_elem.text
        country_code_elem = xml_element.find('CountryCode')
        if country_code_elem is not None:
            instance.country_code = country_code_elem.text
        return instance
@dataclass
class Shipping:
    name: str|None = None  # XML element: Name
    z_i_p: int|None = None  # XML element: ZIP
    city: str|None = None  # XML element: City
    street: str|None = None  # XML element: Street
    street_name: str|None = None  # XML element: StreetName
    street_type: str|None = None  # XML element: StreetType
    street_number: int|None = None  # XML element: StreetNumber
    county: str|None = None  # XML element: County
    country: str|None = None  # XML element: Country
    country_code: str|None = None  # XML element: CountryCode

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Shipping':
        instance = cls()
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        z_i_p_elem = xml_element.find('ZIP')
        if z_i_p_elem is not None:
            instance.z_i_p = int(z_i_p_elem.text or 0)
        city_elem = xml_element.find('City')
        if city_elem is not None:
            instance.city = city_elem.text
        street_elem = xml_element.find('Street')
        if street_elem is not None:
            instance.street = street_elem.text
        street_name_elem = xml_element.find('StreetName')
        if street_name_elem is not None:
            instance.street_name = street_name_elem.text
        street_type_elem = xml_element.find('StreetType')
        if street_type_elem is not None:
            instance.street_type = street_type_elem.text
        street_number_elem = xml_element.find('StreetNumber')
        if street_number_elem is not None:
            instance.street_number = int(street_number_elem.text or 0)
        county_elem = xml_element.find('County')
        if county_elem is not None:
            instance.county = county_elem.text
        country_elem = xml_element.find('Country')
        if country_elem is not None:
            instance.country = country_elem.text
        country_code_elem = xml_element.find('CountryCode')
        if country_code_elem is not None:
            instance.country_code = country_code_elem.text
        return instance
@dataclass
class Invoice:
    name: str|None = None  # XML element: Name
    z_i_p: int|None = None  # XML element: ZIP
    city: str|None = None  # XML element: City
    street: str|None = None  # XML element: Street
    street_name: str|None = None  # XML element: StreetName
    street_type: str|None = None  # XML element: StreetType
    street_number: int|None = None  # XML element: StreetNumber
    county: str|None = None  # XML element: County
    country: str|None = None  # XML element: Country
    country_code: str|None = None  # XML element: CountryCode
    tax_number: str|None = None  # XML element: TaxNumber
    e_u_tax_number: str|None = None  # XML element: EUTaxNumber
    customer_type: str|None = None  # XML element: CustomerType

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Invoice':
        instance = cls()
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        z_i_p_elem = xml_element.find('ZIP')
        if z_i_p_elem is not None:
            instance.z_i_p = int(z_i_p_elem.text or 0)
        city_elem = xml_element.find('City')
        if city_elem is not None:
            instance.city = city_elem.text
        street_elem = xml_element.find('Street')
        if street_elem is not None:
            instance.street = street_elem.text
        street_name_elem = xml_element.find('StreetName')
        if street_name_elem is not None:
            instance.street_name = street_name_elem.text
        street_type_elem = xml_element.find('StreetType')
        if street_type_elem is not None:
            instance.street_type = street_type_elem.text
        street_number_elem = xml_element.find('StreetNumber')
        if street_number_elem is not None:
            instance.street_number = int(street_number_elem.text or 0 )
        county_elem = xml_element.find('County')
        if county_elem is not None:
            instance.county = county_elem.text
        country_elem = xml_element.find('Country')
        if country_elem is not None:
            instance.country = country_elem.text
        country_code_elem = xml_element.find('CountryCode')
        if country_code_elem is not None:
            instance.country_code = country_code_elem.text
        tax_number_elem = xml_element.find('TaxNumber')
        if tax_number_elem is not None:
            instance.tax_number = tax_number_elem.text
        e_u_tax_number_elem = xml_element.find('EUTaxNumber')
        if e_u_tax_number_elem is not None:
            instance.e_u_tax_number = e_u_tax_number_elem.text
        customer_type_elem = xml_element.find('CustomerType')
        if customer_type_elem is not None:
            instance.customer_type = customer_type_elem.text
        return instance
@dataclass
class Contact:
    name: str|None = None  # XML element: Name
    phone: int|None = None  # XML element: Phone
    mobile: int|None = None  # XML element: Mobile
    lang: str|None = None  # XML element: Lang

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Contact':
        instance = cls()
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        phone_elem = xml_element.find('Phone')
        if phone_elem is not None:
            instance.phone = int(phone_elem.text or 0 )
        mobile_elem = xml_element.find('Mobile')
        if mobile_elem is not None:
            instance.mobile = int(mobile_elem.text or 0 )
        lang_elem = xml_element.find('Lang')
        if lang_elem is not None:
            instance.lang = lang_elem.text
        return instance

@dataclass
class Addresses:
    invoice: Invoice|None = None  # XML element: Invoice
    shipping: Shipping|None = None  # XML element: Shipping
    other: Other|None = None  # XML element: Other

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Addresses':
        instance = cls()
        invoice_elem = xml_element.find('Invoice')
        if invoice_elem is not None:
            instance.invoice = Invoice.from_xml(invoice_elem)
        shipping_elem = xml_element.find('Shipping')
        if shipping_elem is not None:
            instance.shipping = Shipping.from_xml(shipping_elem)
        other_elem = xml_element.find('Other')
        if other_elem is not None:
            instance.other = Other.from_xml(other_elem)
        return instance

@dataclass
class UnasCustomer:
    action: str|None = None  # XML element: Action
    email: str|None = None  # XML element: Email
    password_crypted: str|None = None  # XML element: PasswordCrypted
    contact: Contact|None = None  # XML element: Contact
    addresses: Addresses|None = None  # XML element: Addresses
    params: Params|None = None  # XML element: Params
    discount: Discount|None = None  # XML element: Discount
    group: str|None = None  # XML element: Discount

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'UnasCustomer':
        instance = cls()
        action_elem = xml_element.find('Action')
        if action_elem is not None:
            instance.action = action_elem.text
        email_elem = xml_element.find('Email')
        if email_elem is not None:
            instance.email = email_elem.text
        password_crypted_elem = xml_element.find('PasswordCrypted')
        if password_crypted_elem is not None:
            instance.password_crypted = password_crypted_elem.text
        contact_elem = xml_element.find('Contact')
        if contact_elem is not None:
            instance.contact = Contact.from_xml(contact_elem)
        addresses_elem = xml_element.find('Addresses')
        if addresses_elem is not None:
            instance.addresses = Addresses.from_xml(addresses_elem)
        params_elem = xml_element.find('Params')
        if params_elem is not None:
            instance.params = Params.from_xml(params_elem)
        discount_elem = xml_element.find('Discount')
        if discount_elem is not None:
            instance.discount = Discount.from_xml(discount_elem)
        group_elem = xml_element.find('Group')
        if group_elem is not None:
            instance.group = group_elem.text
        return instance


@dataclass
class UnasCustomers:
    customers: List[UnasCustomer] = field( default_factory=list)
    @classmethod
    def from_xmlStr(cls, xmlStr: str) -> List[UnasCustomer]:
        xmlBytes = bytes(xmlStr, 'utf-8')
        xmlItem = ET.fromstring(xmlBytes)
        instance = cls.from_xml(xmlItem)
        return instance.customers
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'UnasCustomers':
        instance = cls()
        customers_elements = xml_element.findall('Customer')
        instance.customers = [UnasCustomer.from_xml(elem) for elem in customers_elements]
        return instance
    