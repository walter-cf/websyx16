from dataclasses import dataclass, field
from typing import List, Optional, Any
import xml.etree.ElementTree as ET

@dataclass
class CustomerOfferDetail:
    id: int | None = None  # XML element: Id
    product: int | None = None  # XML element: Product
    currency_name: str | None = None  # XML element: CurrencyName
    price_category_name: str | None = None  # XML element: PriceCategoryName
    base_price: float | None = None  # XML element: BasePrice
    base_price_date: str | None = None  # XML element: BasePriceDate
    sales_percent: float | None = None  # XML element: SalesPercent
    sales_price: float | None = None  # XML element: SalesPrice

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'CustomerOfferDetail':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or 0)
        product_elem = xml_element.find('Product')
        if product_elem is not None:
            instance.product = int(product_elem.text or 0)
        currency_name_elem = xml_element.find('CurrencyName')
        if currency_name_elem is not None:
            instance.currency_name = currency_name_elem.text
        price_category_name_elem = xml_element.find('PriceCategoryName')
        if price_category_name_elem is not None:
            instance.price_category_name = price_category_name_elem.text
        base_price_elem = xml_element.find('BasePrice')
        if base_price_elem is not None:
            instance.base_price = float(base_price_elem.text or '0.0')
        base_price_date_elem = xml_element.find('BasePriceDate')
        if base_price_date_elem is not None:
            instance.base_price_date = base_price_date_elem.text
        sales_percent_elem = xml_element.find('SalesPercent')
        if sales_percent_elem is not None:
            instance.sales_percent = float(sales_percent_elem.text or '0.0')
        sales_price_elem = xml_element.find('SalesPrice')
        if sales_price_elem is not None:
            instance.sales_price = float(sales_price_elem.text or '0.0')
        return instance

@dataclass
class CustomerOfferDetails:
    customer_offer_detail: List[CustomerOfferDetail] = field( default_factory=list)  # XML element: Order (arra

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'CustomerOfferDetails':
        instance = cls()
        customer_offer_detail_elements = xml_element.findall('CustomerOfferDetail')
        instance.customer_offer_detail = [CustomerOfferDetail.from_xml(elem) for elem in customer_offer_detail_elements]
        return instance

@dataclass
class CustomerOfferCustomer:
    id: int = -111  # XML element: Id
    customer: int = 0  # XML element: Customer
    forbid: int = 0  # XML element: Forbid

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'CustomerOfferCustomer':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or 0)
        customer_elem = xml_element.find('Customer')
        if customer_elem is not None:
            instance.customer = int(customer_elem.text or 0)
        forbid_elem = xml_element.find('Forbid')
        if forbid_elem is not None:
            instance.forbid = int(forbid_elem.text or 0)
        return instance

@dataclass
class CustomerOfferCustomers:
    customer_offer_customer: List[CustomerOfferCustomer] = field( default_factory=list)  # XML element: Order (arra

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'CustomerOfferCustomers':
        instance = cls()
        customer_offer_customer_elements = xml_element.findall('CustomerOfferCustomer')
        instance.customer_offer_customer = [CustomerOfferCustomer.from_xml(elem) for elem in customer_offer_customer_elements]
        return instance

@dataclass
class CustomerOffer:
    id: int | None = None  # XML element: Id
    voucher_number: str | None = None  # XML element: VoucherNumber
    name: str | None = None  # XML element: Name
    valid_from: str | None = None  # XML element: ValidFrom
    valid_to: str | None = None  # XML element: ValidTo
    customer_offer_customers: CustomerOfferCustomers | None | None = None
    customer_offer_details: CustomerOfferDetails | None =  None

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'CustomerOffer':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or 0)
        voucher_number_elem = xml_element.find('VoucherNumber')
        if voucher_number_elem is not None:
            instance.voucher_number = voucher_number_elem.text
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        valid_from_elem = xml_element.find('ValidFrom')
        if valid_from_elem is not None:
            instance.valid_from = valid_from_elem.text
        valid_to_elem = xml_element.find('ValidTo')
        if valid_to_elem is not None:
            instance.valid_to = valid_to_elem.text
        customer_offer_customers_elem = xml_element.find('CustomerOfferCustomers')
        if customer_offer_customers_elem is not None:
            instance.customer_offer_customers = CustomerOfferCustomers.from_xml(customer_offer_customers_elem)
        customer_offer_details_elem = xml_element.find('CustomerOfferDetails')
        if customer_offer_details_elem is not None:
            instance.customer_offer_details = CustomerOfferDetails.from_xml(customer_offer_details_elem)
        return instance

@dataclass
class CustomerOffers:
    customer_offers: List[CustomerOffer] | None | None = None  # XML element: CustomerOffer

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'CustomerOffers':
        instance = cls()
        customer_offer_elements = xml_element.findall('CustomerOffer')
        instance.customer_offers = [CustomerOffer.from_xml(elem) for elem in customer_offer_elements]
        return instance

