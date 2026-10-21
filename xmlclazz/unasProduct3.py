from dataclasses import dataclass, field
from typing import List, Optional, Any
import xml.etree.ElementTree as ET

@dataclass
class AutomaticMeta:
    keywords: str|None = None  # XML element: Keywords
    description: str|None = None  # XML element: Description
    title: str|None = None  # XML element: Title

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'AutomaticMeta':
        instance = cls()
        keywords_elem = xml_element.find('Keywords')
        if keywords_elem is not None:
            instance.keywords = keywords_elem.text
        description_elem = xml_element.find('Description')
        if description_elem is not None:
            instance.description = description_elem.text
        title_elem = xml_element.find('Title')
        if title_elem is not None:
            instance.title = title_elem.text
        return instance
@dataclass
class Meta:
    keywords: str|None = None  # XML element: Keywords
    description: str|None = None  # XML element: Description
    title: str|None = None  # XML element: Title
    robots: str|None = None  # XML element: Robots

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Meta':
        instance = cls()
        keywords_elem = xml_element.find('Keywords')
        if keywords_elem is not None:
            instance.keywords = keywords_elem.text
        description_elem = xml_element.find('Description')
        if description_elem is not None:
            instance.description = description_elem.text
        robots_elem = xml_element.find('Title')
        if robots_elem is not None:
            instance.title = robots_elem.text
        robots_elem = xml_element.find('Title')
        if robots_elem is not None:
            instance.robots = robots_elem.text
        return instance
@dataclass
class PackageComponents:
    component: Component|None = None  # XML element: Component

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'PackageComponents':
        instance = cls()
        component_elem = xml_element.find('Component')
        if component_elem is not None:
            instance.component = Component.from_xml(component_elem)
        return instance
@dataclass
class Component:
    sku: str|None = None  # XML element: Sku
    qty: int|None = None  # XML element: Qty

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Component':
        instance = cls()
        sku_elem = xml_element.find('Sku')
        if sku_elem is not None:
            instance.sku = sku_elem.text
        qty_elem = xml_element.find('Qty')
        if qty_elem is not None:
            instance.qty = int(qty_elem.text or '0')
        return instance
@dataclass
class Types:
    type: str|None = None  # XML element: Type
    parent: str|None = None  # XML element: Parent
    display: int|None = None  # XML element: Display
    order: int|None = None  # XML element: Order

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Types':
        instance = cls()
        type_elem = xml_element.find('Type')
        if type_elem is not None:
            instance.type = type_elem.text
        parent_elem = xml_element.find('Parent')
        if parent_elem is not None:
            instance.parent = parent_elem.text
        display_elem = xml_element.find('Display')
        if display_elem is not None:
            instance.display = int(display_elem.text or '0')
        order_elem = xml_element.find('Order')
        if order_elem is not None:
            instance.order = int(order_elem.text or '0')
        return instance
@dataclass
class PlusServices:
    plus_service: PlusService|None = None  # XML element: PlusService

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'PlusServices':
        instance = cls()
        plus_service_elem = xml_element.find('PlusService')
        if plus_service_elem is not None:
            instance.plus_service = PlusService.from_xml(plus_service_elem)
        return instance
@dataclass
class PlusService:
    id: int|None = None  # XML element: Id
    name: str|None = None  # XML element: Name

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'PlusService':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or '0')
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        return instance
@dataclass
class OnlineContent:
    url: str|None = None  # XML element: Url
    limit: str|None = None  # XML element: Limit
    filename: str|None = None  # XML element: Filename

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'OnlineContent':
        instance = cls()
        url_elem = xml_element.find('Url')
        if url_elem is not None:
            instance.url = url_elem.text
        limit_elem = xml_element.find('Limit')
        if limit_elem is not None:
            instance.limit = limit_elem.text
        filename_elem = xml_element.find('Filename')
        if filename_elem is not None:
            instance.filename = filename_elem.text
        return instance
@dataclass
class Stocks:
    status: Status|None = None  # XML element: Status
    stock: Stock|None = None  # XML element: Stock

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Stocks':
        instance = cls()
        status_elem = xml_element.find('Status')
        if status_elem is not None:
            instance.status = Status.from_xml(status_elem)
        stock_elem = xml_element.find('Stock')
        if stock_elem is not None:
            instance.stock = Stock.from_xml(stock_elem)
        return instance
@dataclass
class Stock:
    variants: Variants|None = None  # XML element: Variants
    qty: int|None = None  # XML element: Qty

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Stock':
        instance = cls()
        variants_elem = xml_element.find('Variants')
        if variants_elem is not None:
            instance.variants = Variants.from_xml(variants_elem)
        qty_elem = xml_element.find('Qty')
        if qty_elem is not None:
            instance.qty = int(qty_elem.text or '0')
        return instance
@dataclass
class SimilarProducts:
    similar_product: SimilarProduct|None = None  # XML element: SimilarProduct

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'SimilarProducts':
        instance = cls()
        similar_product_elem = xml_element.find('SimilarProduct')
        if similar_product_elem is not None:
            instance.similar_product = SimilarProduct.from_xml(similar_product_elem)
        return instance
@dataclass
class SimilarProduct:
    id: int|None = None  # XML element: Id
    sku: str|None = None  # XML element: Sku
    name: str|None = None  # XML element: Name

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'SimilarProduct':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or '0')
        sku_elem = xml_element.find('Sku')
        if sku_elem is not None:
            instance.sku = sku_elem.text
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        return instance
@dataclass
class AdditionalProducts:
    additional_product: AdditionalProduct|None = None  # XML element: AdditionalProduct

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'AdditionalProducts':
        instance = cls()
        additional_product_elem = xml_element.find('AdditionalProduct')
        if additional_product_elem is not None:
            instance.additional_product = AdditionalProduct.from_xml(additional_product_elem)
        return instance
@dataclass
class AdditionalProduct:
    id: int|None = None  # XML element: Id
    sku: str|None = None  # XML element: Sku
    name: str|None = None  # XML element: Name

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'AdditionalProduct':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text  or '0')
        sku_elem = xml_element.find('Sku')
        if sku_elem is not None:
            instance.sku = sku_elem.text
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        return instance
@dataclass
class QtyDiscount:
    step: Step|None = None  # XML element: Step

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'QtyDiscount':
        instance = cls()
        step_elem = xml_element.find('Step')
        if step_elem is not None:
            instance.step = Step.from_xml(step_elem)
        return instance
@dataclass
class Step:
    limit: Limit|None = None  # XML element: Limit
    discount: str|None = None  # XML element: Discount

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Step':
        instance = cls()
        limit_elem = xml_element.find('Limit')
        if limit_elem is not None:
            instance.limit = Limit.from_xml(limit_elem)
        discount_elem = xml_element.find('Discount')
        if discount_elem is not None:
            instance.discount = discount_elem.text
        return instance
@dataclass
class Limit:
    lower: int|None = None  # XML element: Lower
    upper: int|None = None  # XML element: Upper

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Limit':
        instance = cls()
        lower_elem = xml_element.find('Lower')
        if lower_elem is not None:
            instance.lower = int(lower_elem.text or '0')
        upper_elem = xml_element.find('Upper')
        if upper_elem is not None:
            instance.upper = int(upper_elem.text or '0')
        return instance
@dataclass
class AdditionalDatas:
    additional_data: AdditionalData|None = None  # XML element: AdditionalData

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'AdditionalDatas':
        instance = cls()
        additional_data_elem = xml_element.find('AdditionalData')
        if additional_data_elem is not None:
            instance.additional_data = AdditionalData.from_xml(additional_data_elem)
        return instance
@dataclass
class AdditionalData:
    id: int|None = None  # XML element: Id
    title: str|None = None  # XML element: Title
    content: str|None = None  # XML element: Content

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'AdditionalData':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or '0')
        title_elem = xml_element.find('Title')
        if title_elem is not None:
            instance.title = title_elem.text
        content_elem = xml_element.find('Content')
        if content_elem is not None:
            instance.content = content_elem.text
        return instance
@dataclass
class Params:
    param: Param|None = None  # XML element: Param

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Params':
        instance = cls()
        param_elem = xml_element.find('Param')
        if param_elem is not None:
            instance.param = Param.from_xml(param_elem)
        return instance
@dataclass
class Param:
    id: int|None = None  # XML element: Id
    type: str|None = None  # XML element: Type
    name: str|None = None  # XML element: Name
    group: str|None = None  # XML element: Group
    value: str|None = None  # XML element: Value
    before: str|None = None  # XML element: Before
    after: str|None = None  # XML element: After

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Param':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text  or '0')
        type_elem = xml_element.find('Type')
        if type_elem is not None:
            instance.type = type_elem.text
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        group_elem = xml_element.find('Group')
        if group_elem is not None:
            instance.group = group_elem.text
        value_elem = xml_element.find('Value')
        if value_elem is not None:
            instance.value = value_elem.text
        before_elem = xml_element.find('Before')
        if before_elem is not None:
            instance.before = before_elem.text
        after_elem = xml_element.find('After')
        if after_elem is not None:
            instance.after = after_elem.text
        return instance
@dataclass
class Datas:
    data: Data|None = None  # XML element: Data

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Datas':
        instance = cls()
        data_elem = xml_element.find('Data')
        if data_elem is not None:
            instance.data = Data.from_xml(data_elem)
        return instance
@dataclass
class Data:
    id: int|None = None  # XML element: Id
    name: str|None = None  # XML element: Name
    value: str|None = None  # XML element: Value

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Data':
        instance = cls()
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or '0')
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        value_elem = xml_element.find('Value')
        if value_elem is not None:
            instance.value = value_elem.text
        return instance
@dataclass
class Value:
    name: str|None = None  # XML element: Name

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Value':
        instance = cls()
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        return instance
@dataclass
class Variants:
    variant: Variant|None = None  # XML element: Variant

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Variants':
        instance = cls()
        variant_elem = xml_element.find('Variant')
        if variant_elem is not None:
            instance.variant = Variant.from_xml(variant_elem)
        return instance
@dataclass
class Values:
    value: List[Value] =  field( default_factory=list)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Values':
        instance = cls()
        value_elements = xml_element.findall('Value')
        instance.value = [Value.from_xml(elem) for elem in value_elements]
        return instance

@dataclass
class Variant:
    name: str|None = None  # XML element: Name
    values: Value|None = None  # XML element: Values

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Variant':
        instance = cls()
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        values_elem = xml_element.find('Values')
        if values_elem is not None:
            instance.values = Value.from_xml(values_elem)
        return instance
@dataclass
class Images:
    default_filename: str|None = None  # XML element: DefaultFilename
    default_alt: str|None = None  # XML element: DefaultAlt
    o_g: int|None = None  # XML element: OG
    version: int|None = None  # XML element: Version
    image: Image|None = None  # XML element: Image

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Images':
        instance = cls()
        default_filename_elem = xml_element.find('DefaultFilename')
        if default_filename_elem is not None:
            instance.default_filename = default_filename_elem.text
        default_alt_elem = xml_element.find('DefaultAlt')
        if default_alt_elem is not None:
            instance.default_alt = default_alt_elem.text
        o_g_elem = xml_element.find('OG')
        if o_g_elem is not None:
            instance.o_g = int(o_g_elem.text or '0')
        version_elem = xml_element.find('Version')
        if version_elem is not None:
            instance.version = int(version_elem.text or '0')
        image_elem = xml_element.find('Image')
        if image_elem is not None:
            instance.image = Image.from_xml(image_elem)
        return instance
@dataclass
class Image:
    type: str|None = None  # XML element: Type
    sef_url: str|None = None  # XML element: SefUrl
    filename: str|None = None  # XML element: Filename
    alt: str|None = None  # XML element: Alt

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Image':
        instance = cls()
        type_elem = xml_element.find('Type')
        if type_elem is not None:
            instance.type = type_elem.text
        sef_url_elem = xml_element.find('SefUrl')
        if sef_url_elem is not None:
            instance.sef_url = sef_url_elem.text
        filename_elem = xml_element.find('Filename')
        if filename_elem is not None:
            instance.filename = filename_elem.text
        alt_elem = xml_element.find('Alt')
        if alt_elem is not None:
            instance.alt = alt_elem.text
        return instance
@dataclass
class Categories:
    category: Category|None = None  # XML element: Category

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Categories':
        instance = cls()
        category_elem = xml_element.find('Category')
        if category_elem is not None:
            instance.category = Category.from_xml(category_elem)
        return instance
@dataclass
class Category:
    type: str|None = None  # XML element: Type
    id: int|None = None  # XML element: Id
    name: str|None = None  # XML element: Name

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Category':
        instance = cls()
        type_elem = xml_element.find('Type')
        if type_elem is not None:
            instance.type = type_elem.text
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text  or '0')
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        return instance
@dataclass
class Prices:
    vat: str|None = None  # XML element: Vat
    price: Price|None = None  # XML element: Price

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Prices':
        instance = cls()
        vat_elem = xml_element.find('Vat')
        if vat_elem is not None:
            instance.vat = vat_elem.text
        price_elem = xml_element.find('Price')
        if price_elem is not None:
            instance.price = Price.from_xml(price_elem)
        return instance
@dataclass
class Price:
    type: str|None = None  # XML element: Type
    start: str|None = None  # XML element: Start
    end: str|None = None  # XML element: End
    group: int|None = None  # XML element: Group
    group_name: str|None = None  # XML element: GroupName
    area_name: str|None = None  # XML element: AreaName
    sale_net: float|None = None  # XML element: SaleNet
    sale_gross: float|None = None  # XML element: SaleGross
    sale_start: str|None = None  # XML element: SaleStart
    sale_end: str|None = None  # XML element: SaleEnd
    currency_filter: str|None = None  # XML element: CurrencyFilter
    net: float|None = None  # XML element: Net
    gross: float|None = None  # XML element: Gross
    currency: str|None = None  # XML element: Currency

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Price':
        instance = cls()
        type_elem = xml_element.find('Type')
        if type_elem is not None:
            instance.type = type_elem.text
        start_elem = xml_element.find('Start')
        if start_elem is not None:
            instance.start = start_elem.text
        end_elem = xml_element.find('End')
        if end_elem is not None:
            instance.end = end_elem.text
        group_elem = xml_element.find('Group')
        if group_elem is not None:
            instance.group = int(group_elem.text or '0')
        group_name_elem = xml_element.find('GroupName')
        if group_name_elem is not None:
            instance.group_name = group_name_elem.text
        area_name_elem = xml_element.find('AreaName')
        if area_name_elem is not None:
            instance.area_name = area_name_elem.text
        sale_net_elem = xml_element.find('SaleNet')
        if sale_net_elem is not None:
            instance.sale_net = float(sale_net_elem.text or '0')
        sale_gross_elem = xml_element.find('SaleGross')
        if sale_gross_elem is not None:
            instance.sale_gross = float(sale_gross_elem.text or '0')
        sale_start_elem = xml_element.find('SaleStart')
        if sale_start_elem is not None:
            instance.sale_start = sale_start_elem.text
        sale_end_elem = xml_element.find('SaleEnd')
        if sale_end_elem is not None:
            instance.sale_end = sale_end_elem.text
        currency_filter_elem = xml_element.find('CurrencyFilter')
        if currency_filter_elem is not None:
            instance.currency_filter = currency_filter_elem.text
        net_elem = xml_element.find('Net')
        if net_elem is not None:
            instance.net = float(net_elem.text or '0')
        gross_elem = xml_element.find('Gross')
        if gross_elem is not None:
            instance.gross = float(gross_elem.text or '0')
        currency_elem = xml_element.find('Currency')
        if currency_elem is not None:
            instance.currency = currency_elem.text
        return instance
@dataclass
class Description:
    short: str|None = None  # XML element: Short
    long: str|None = None  # XML element: Long

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Description':
        instance = cls()
        short_elem = xml_element.find('Short')
        if short_elem is not None:
            instance.short = short_elem.text
        long_elem = xml_element.find('Long')
        if long_elem is not None:
            instance.long = long_elem.text
        return instance
@dataclass
class AlterUnit:
    qty: int|None = None  # XML element: Qty
    unit: str|None = None  # XML element: Unit

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'AlterUnit':
        instance = cls()
        qty_elem = xml_element.find('Qty')
        if qty_elem is not None:
            instance.qty = int(qty_elem.text or '0')
        unit_elem = xml_element.find('Unit')
        if unit_elem is not None:
            instance.unit = unit_elem.text
        return instance
@dataclass
class PublicInterval:
    start: str|None = None  # XML element: Start
    end: str|None = None  # XML element: End

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'PublicInterval':
        instance = cls()
        start_elem = xml_element.find('Start')
        if start_elem is not None:
            instance.start = start_elem.text
        end_elem = xml_element.find('End')
        if end_elem is not None:
            instance.end = end_elem.text
        return instance
@dataclass
class Export:
    status: int|None = None  # XML element: Status
    forbidden: Forbidden|None = None  # XML element: Forbidden

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Export':
        instance = cls()
        status_elem = xml_element.find('Status')
        if status_elem is not None:
            instance.status = int(status_elem.text or '0')
        forbidden_elem = xml_element.find('Forbidden')
        if forbidden_elem is not None:
            instance.forbidden = Forbidden.from_xml(forbidden_elem)
        return instance
@dataclass
class Forbidden:
    format: List[str] = field( default_factory=list)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Forbidden':
        instance = cls()
        format_elements = xml_element.findall('Format')
        instance.format = [elem.text or '' for elem in format_elements or []]
        return instance
@dataclass
class Statuses:
    status: Status|None = None  # XML element: Status

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Statuses':
        instance = cls()
        status_elem = xml_element.find('Status')
        if status_elem is not None:
            instance.status = Status.from_xml(status_elem)
        return instance
@dataclass
class Status:
    type: str|None = None  # XML element: Type
    id: int|None = None  # XML element: Id
    name: str|None = None  # XML element: Name
    value: int|None = None  # XML element: Value

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Status':
        instance = cls()
        type_elem = xml_element.find('Type')
        if type_elem is not None:
            instance.type = type_elem.text
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or '0')
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        value_elem = xml_element.find('Value')
        if value_elem is not None:
            instance.value = int(value_elem.text or '0')
        return instance
@dataclass
class History:
    event: Event|None = None  # XML element: Event

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'History':
        instance = cls()
        event_elem = xml_element.find('Event')
        if event_elem is not None:
            instance.event = Event.from_xml(event_elem)
        return instance
@dataclass
class Event:
    action: str|None = None  # XML element: Action
    time: int|None = None  # XML element: Time
    sku: str|None = None  # XML element: Sku
    sku_old: str|None = None  # XML element: SkuOld

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Event':
        instance = cls()
        action_elem = xml_element.find('Action')
        if action_elem is not None:
            instance.action = action_elem.text
        time_elem = xml_element.find('Time')
        if time_elem is not None:
            instance.time = int(time_elem.text or 0)
        sku_elem = xml_element.find('Sku')
        if sku_elem is not None:
            instance.sku = sku_elem.text
        sku_old_elem = xml_element.find('SkuOld')
        if sku_old_elem is not None:
            instance.sku_old = sku_old_elem.text
        return instance

@dataclass
class UnasProduct:
    action: str|None = None  # XML element: Action
    state: str|None = None  # XML element: State
    id: int|None = None  # XML element: Id
    sku: str|None = None  # XML element: Sku
    sku_new: str|None = None  # XML element: SkuNew
    history: History|None = None  # XML element: History
    statuses: Statuses|None = None  # XML element: Statuses
    no_list: int|None = None  # XML element: NoList
    inquire: int|None = None  # XML element: Inquire
    cust_discount_disable: int|None = None  # XML element: CustDiscountDisable
    explicit: int|None = None  # XML element: Explicit
    export: Export|None = None  # XML element: Export
    public_interval: PublicInterval|None = None  # XML element: PublicInterval
    name: str|None = None  # XML element: Name
    unit: str|None = None  # XML element: Unit
    minimum_qty: int|None = None  # XML element: MinimumQty
    maximum_qty: int|None = None  # XML element: MaximumQty
    alert_qty: int|None = None  # XML element: AlertQty
    unit_step: int|None = None  # XML element: UnitStep
    alter_unit: AlterUnit|None = None  # XML element: AlterUnit
    weight: float|None = None  # XML element: Weight
    point: int|None = None  # XML element: Point
    buyable_with_point: str|None = None  # XML element: BuyableWithPoint
    description: Description|None = None  # XML element: Description
    prices: Prices|None = None  # XML element: Prices
    categories: Categories|None = None  # XML element: Categories
    url: str|None = None  # XML element: Url
    sef_url: str|None = None  # XML element: SefUrl
    images: Images|None = None  # XML element: Images
    variants: Variants|None = None  # XML element: Variants
    datas: Datas|None = None  # XML element: Datas
    params: Params|None = None  # XML element: Params
    additional_datas: AdditionalDatas|None = None  # XML element: AdditionalDatas
    qty_discount: QtyDiscount|None = None  # XML element: QtyDiscount
    additional_products: AdditionalProducts|None = None  # XML element: AdditionalProducts
    similar_products: SimilarProducts|None = None  # XML element: SimilarProducts
    stocks: Stocks|None = None  # XML element: Stocks
    online_content: OnlineContent|None = None  # XML element: OnlineContent
    plus_services: PlusServices|None = None  # XML element: PlusServices
    types: Types|None = None  # XML element: Types
    package_product: str|None = None  # XML element: PackageProduct
    package_components: PackageComponents|None = None  # XML element: PackageComponents
    meta: Meta|None = None  # XML element: Meta
    automatic_meta: AutomaticMeta|None = None  # XML element: AutomaticMeta

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'UnasProduct':
        instance = cls()
        action_elem = xml_element.find('Action')
        if action_elem is not None:
            instance.action = action_elem.text
        state_elem = xml_element.find('State')
        if state_elem is not None:
            instance.state = state_elem.text
        id_elem = xml_element.find('Id')
        if id_elem is not None:
            instance.id = int(id_elem.text or '0')
        sku_elem = xml_element.find('Sku')
        if sku_elem is not None:
            instance.sku = sku_elem.text
        sku_new_elem = xml_element.find('SkuNew')
        if sku_new_elem is not None:
            instance.sku_new = sku_new_elem.text
        history_elem = xml_element.find('History')
        if history_elem is not None:
            instance.history = History.from_xml(history_elem)
        statuses_elem = xml_element.find('Statuses')
        if statuses_elem is not None:
            instance.statuses = Statuses.from_xml(statuses_elem)
        no_list_elem = xml_element.find('NoList')
        if no_list_elem is not None:
            instance.no_list = int(no_list_elem.text or '0')
        inquire_elem = xml_element.find('Inquire')
        if inquire_elem is not None:
            instance.inquire = int(inquire_elem.text or '0')
        cust_discount_disable_elem = xml_element.find('CustDiscountDisable')
        if cust_discount_disable_elem is not None:
            instance.cust_discount_disable = int(cust_discount_disable_elem.text or '0')
        explicit_elem = xml_element.find('Explicit')
        if explicit_elem is not None:
            instance.explicit = int(explicit_elem.text or '0')
        export_elem = xml_element.find('Export')
        if export_elem is not None:
            instance.export = Export.from_xml(export_elem)
        public_interval_elem = xml_element.find('PublicInterval')
        if public_interval_elem is not None:
            instance.public_interval = PublicInterval.from_xml(public_interval_elem)
        name_elem = xml_element.find('Name')
        if name_elem is not None:
            instance.name = name_elem.text
        unit_elem = xml_element.find('Unit')
        if unit_elem is not None:
            instance.unit = unit_elem.text
        minimum_qty_elem = xml_element.find('MinimumQty')
        if minimum_qty_elem is not None:
            instance.minimum_qty = int(minimum_qty_elem.text or '0')
        maximum_qty_elem = xml_element.find('MaximumQty')
        if maximum_qty_elem is not None:
            instance.maximum_qty = int(maximum_qty_elem.text or '0')
        alert_qty_elem = xml_element.find('AlertQty')
        if alert_qty_elem is not None:
            instance.alert_qty = int(alert_qty_elem.text or '0')
        unit_step_elem = xml_element.find('UnitStep')
        if unit_step_elem is not None:
            instance.unit_step = int(unit_step_elem.text or '0')
        alter_unit_elem = xml_element.find('AlterUnit')
        if alter_unit_elem is not None:
            instance.alter_unit = AlterUnit.from_xml(alter_unit_elem)
        weight_elem = xml_element.find('Weight')
        if weight_elem is not None:
            instance.weight = float(weight_elem.text or '0')
        point_elem = xml_element.find('Point')
        if point_elem is not None:
            instance.point = int(point_elem.text or '0')
        buyable_with_point_elem = xml_element.find('BuyableWithPoint')
        if buyable_with_point_elem is not None:
            instance.buyable_with_point = buyable_with_point_elem.text
        description_elem = xml_element.find('Description')
        if description_elem is not None:
            instance.description = Description.from_xml(description_elem)
        prices_elem = xml_element.find('Prices')
        if prices_elem is not None:
            instance.prices = Prices.from_xml(prices_elem)
        categories_elem = xml_element.find('Categories')
        if categories_elem is not None:
            instance.categories = Categories.from_xml(categories_elem)
        url_elem = xml_element.find('Url')
        if url_elem is not None:
            instance.url = url_elem.text
        sef_url_elem = xml_element.find('SefUrl')
        if sef_url_elem is not None:
            instance.sef_url = sef_url_elem.text
        images_elem = xml_element.find('Images')
        if images_elem is not None:
            instance.images = Images.from_xml(images_elem)
        variants_elem = xml_element.find('Variants')
        if variants_elem is not None:
            instance.variants = Variants.from_xml(variants_elem)
        datas_elem = xml_element.find('Datas')
        if datas_elem is not None:
            instance.datas = Datas.from_xml(datas_elem)
        params_elem = xml_element.find('Params')
        if params_elem is not None:
            instance.params = Params.from_xml(params_elem)
        additional_datas_elem = xml_element.find('AdditionalDatas')
        if additional_datas_elem is not None:
            instance.additional_datas = AdditionalDatas.from_xml(additional_datas_elem)
        qty_discount_elem = xml_element.find('QtyDiscount')
        if qty_discount_elem is not None:
            instance.qty_discount = QtyDiscount.from_xml(qty_discount_elem)
        additional_products_elem = xml_element.find('AdditionalProducts')
        if additional_products_elem is not None:
            instance.additional_products = AdditionalProducts.from_xml(additional_products_elem)
        similar_products_elem = xml_element.find('SimilarProducts')
        if similar_products_elem is not None:
            instance.similar_products = SimilarProducts.from_xml(similar_products_elem)
        stocks_elem = xml_element.find('Stocks')
        if stocks_elem is not None:
            instance.stocks = Stocks.from_xml(stocks_elem)
        online_content_elem = xml_element.find('OnlineContent')
        if online_content_elem is not None:
            instance.online_content = OnlineContent.from_xml(online_content_elem)
        plus_services_elem = xml_element.find('PlusServices')
        if plus_services_elem is not None:
            instance.plus_services = PlusServices.from_xml(plus_services_elem)
        types_elem = xml_element.find('Types')
        if types_elem is not None:
            instance.types = Types.from_xml(types_elem)
        package_product_elem = xml_element.find('PackageProduct')
        if package_product_elem is not None:
            instance.package_product = package_product_elem.text
        package_components_elem = xml_element.find('PackageComponents')
        if package_components_elem is not None:
            instance.package_components = PackageComponents.from_xml(package_components_elem)
        meta_elem = xml_element.find('Meta')
        if meta_elem is not None:
            instance.meta = Meta.from_xml(meta_elem)
        automatic_meta_elem = xml_element.find('AutomaticMeta')
        if automatic_meta_elem is not None:
            instance.automatic_meta = AutomaticMeta.from_xml(automatic_meta_elem)
        return instance

@dataclass
class UnasProducts:
    products: List[UnasProduct] = field( default_factory=list)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'UnasProducts':
        instance = cls()
        for prod in xml_element.findall('Product'):
            instance.products.append(UnasProduct.from_xml(prod))
        return instance

