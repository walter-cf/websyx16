from dataclasses import dataclass
from typing import List, Optional, Any
import xml.etree.ElementTree as ET

@dataclass
class TransportMode:
    transport_mode_name: str = None  # XML element: TransportModeName
    discount_percent: int = None  # XML element: DiscountPercent

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'TransportMode':
        instance = cls()
        transport_mode_name_elem = xml_element.find('TransportModeName')
        if transport_mode_name_elem is not None:
            instance.transport_mode_name = transport_mode_name_elem.text
        discount_percent_elem = xml_element.find('DiscountPercent')
        if discount_percent_elem is not None:
            instance.discount_percent = discount_percent_elem.text
        return instance
@dataclass
class TransportModes:
    transport_mode: List[TransportMode] = None  # XML element: TransportMode (array)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'TransportModes':
        instance = cls()
        transport_mode_elements = xml_element.findall('TransportMode')
        instance.transport_mode = [TransportMode.from_xml(elem) for elem in transport_mode_elements]
        return instance

@dataclass
class ProductCustomerDiscount:
    product: int = None  # XML element: Product
    product_code: str = None  # XML element: ProductCode
    product_name: str = None  # XML element: ProductName
    customer: int = None  # XML element: Customer
    customer_code: str = None  # XML element: CustomerCode
    customer_name: str = None  # XML element: CustomerName
    discount_percent: int = None  # XML element: DiscountPercent

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'ProductCustomerDiscount':
        instance = cls()
        product_elem = xml_element.find('Product')
        if product_elem is not None:
            instance.product = product_elem.text
        product_code_elem = xml_element.find('ProductCode')
        if product_code_elem is not None:
            instance.product_code = product_code_elem.text
        product_name_elem = xml_element.find('ProductName')
        if product_name_elem is not None:
            instance.product_name = product_name_elem.text
        customer_elem = xml_element.find('Customer')
        if customer_elem is not None:
            instance.customer = customer_elem.text
        customer_code_elem = xml_element.find('CustomerCode')
        if customer_code_elem is not None:
            instance.customer_code = customer_code_elem.text
        customer_name_elem = xml_element.find('CustomerName')
        if customer_name_elem is not None:
            instance.customer_name = customer_name_elem.text
        discount_percent_elem = xml_element.find('DiscountPercent')
        if discount_percent_elem is not None:
            instance.discount_percent = discount_percent_elem.text
        return instance
@dataclass
class ProductCustomerDiscounts:
    product_customer_discount: List[ProductCustomerDiscount] = None  # XML element: ProductCustomerDiscount (array)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'ProductCustomerDiscounts':
        instance = cls()
        product_customer_discount_elements = xml_element.findall('ProductCustomerDiscount')
        instance.product_customer_discount = [ProductCustomerDiscount.from_xml(elem) for elem in product_customer_discount_elements]
        return instance

@dataclass
class ProductCategoryDiscount:
    product_category: str = None  # XML element: ProductCategory
    customer: int = None  # XML element: Customer
    customer_code: str = None  # XML element: CustomerCode
    customer_name: str = None  # XML element: CustomerName
    discount_percent: int = None  # XML element: DiscountPercent
    inherit: int = None  # XML element: Inherit

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'ProductCategoryDiscount':
        instance = cls()
        product_category_elem = xml_element.find('ProductCategory')
        if product_category_elem is not None:
            instance.product_category = product_category_elem.text
        customer_elem = xml_element.find('Customer')
        if customer_elem is not None:
            instance.customer = customer_elem.text
        customer_code_elem = xml_element.find('CustomerCode')
        if customer_code_elem is not None:
            instance.customer_code = customer_code_elem.text
        customer_name_elem = xml_element.find('CustomerName')
        if customer_name_elem is not None:
            instance.customer_name = customer_name_elem.text
        discount_percent_elem = xml_element.find('DiscountPercent')
        if discount_percent_elem is not None:
            instance.discount_percent = discount_percent_elem.text
        inherit_elem = xml_element.find('Inherit')
        if inherit_elem is not None:
            instance.inherit = inherit_elem.text
        return instance
@dataclass
class ProductCategoryDiscounts:
    product_category_discount: List[ProductCategoryDiscount] = None  # XML element: ProductCategoryDiscount (array)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'ProductCategoryDiscounts':
        instance = cls()
        product_category_discount_elements = xml_element.findall('ProductCategoryDiscount')
        instance.product_category_discount = [ProductCategoryDiscount.from_xml(elem) for elem in product_category_discount_elements]
        return instance

@dataclass
class PaymentMethod:
    payment_method_name: str = None  # XML element: PaymentMethodName
    discount_percent: int = None  # XML element: DiscountPercent

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'PaymentMethod':
        instance = cls()
        payment_method_name_elem = xml_element.find('PaymentMethodName')
        if payment_method_name_elem is not None:
            instance.payment_method_name = payment_method_name_elem.text
        discount_percent_elem = xml_element.find('DiscountPercent')
        if discount_percent_elem is not None:
            instance.discount_percent = discount_percent_elem.text
        return instance

@dataclass
class PaymentMethods:
    payment_method: List[PaymentMethod] = None  # XML element: PaymentMethod (array)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'PaymentMethods':
        instance = cls()
        payment_method_elements = xml_element.findall('PaymentMethod')
        instance.payment_method = [PaymentMethod.from_xml(elem) for elem in payment_method_elements]
        return instance

@dataclass
class DiscountRules:
    customer_voucher_discounts: str|None = None  # XML element: CustomerVoucherDiscounts
    payment_methods: PaymentMethods|None = None  # XML element: PaymentMethods
    product_category_discounts: ProductCategoryDiscounts|None = None  # XML element: ProductCategoryDiscounts
    product_customer_discounts: ProductCustomerDiscounts|None = None  # XML element: ProductCustomerDiscounts
    transport_modes: TransportModes|None = None  # XML element: TransportModes

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'DiscountRules':
        instance = cls()
        customer_voucher_discounts_elem = xml_element.find('CustomerVoucherDiscounts')
        if customer_voucher_discounts_elem is not None:
            instance.customer_voucher_discounts = customer_voucher_discounts_elem.text
        payment_methods_elem = xml_element.find('PaymentMethods')
        if payment_methods_elem is not None:
            instance.payment_methods = PaymentMethods.from_xml(payment_methods_elem)
        product_category_discounts_elem = xml_element.find('ProductCategoryDiscounts')
        if product_category_discounts_elem is not None:
            instance.product_category_discounts = ProductCategoryDiscounts.from_xml(product_category_discounts_elem)
        product_customer_discounts_elem = xml_element.find('ProductCustomerDiscounts')
        if product_customer_discounts_elem is not None:
            instance.product_customer_discounts = ProductCustomerDiscounts.from_xml(product_customer_discounts_elem)
        transport_modes_elem = xml_element.find('TransportModes')
        if transport_modes_elem is not None:
            instance.transport_modes = TransportModes.from_xml(transport_modes_elem)
        return instance
