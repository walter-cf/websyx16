from enum import Enum
from typing import List, Optional, Any
from dataclasses import dataclass
import json


axa="""
        @dataclass
        class User:
            user_name: str
            email: str
            tags: List[str]

        # Example JSON data
        json_data = '{"user_name": "john_doe", "email": "john@example.com", "tags": ["python", "developer"]}'

        # Deserialize JSON to User object
        data = json.loads(json_data)
        user = User(**data)
"""

@dataclass
class PepitaCustomer:
    last_name: str
    first_name: str
    phone: str
    email: str
    billing_name: str
    billing_country: str
    billing_city: str
    billing_street: str
    billing_street_address: str
    billing_house_number: str
    billing_postal_code: str
    shipping_country: str
    shipping_city: str
    shipping_street: str
    shipping_street_address: str
    shipping_house_number: str
    shipping_postal_code: str
    tax_number: str| None = None

@dataclass
class PepitaProducts:
    id: str
    sku: str
    currency: str
    quantity: int
    price: int
    vat: int

#@dataclass
class PaymentModeEnum(Enum):
    cod = "cod" # Utanvet
    transfer = "transfer" # Atutalas
    creditcard = "creditcard" # card

class DeliveryModeEnum(Enum):
    shipping ='shipping'
    gls      = 'gls'
    gls_parcellocker = 'gls_parcellocker'
    gls_xxl  = 'gls_xxl'
    mpl      ='mpl'

@dataclass
class PepitaOrder:
    origin: str
    id: int
    date: str
    payment_mode: PaymentModeEnum  # cod: utánvét- transfer: átutalás - creditcard: bankkártya ENUM
    customer_message: str
    courier_message: str
    status: str
    payment_status: str
    total_shipping_price: int
    total_shipping_price_currency: str
    voucher: str
    delivery_mod: DeliveryModeEnum
    customer: PepitaCustomer
    products: List[PepitaProducts]
    package_label: str|None = None
    tsId : int = 0
    symbolId: int = 0

def from_json(jsonStr: str) -> 'PepitaOrder':
    data = json.loads(jsonStr)
    return PepitaOrder(**data)

def from_jsonFile(fp) -> 'PepitaOrder':
    data = json.load(fp)
    return PepitaOrder(**data)

def toJson(po : PepitaOrder) -> str:
    return json.dumps(po)

def toSymbolOrderXml(po : PepitaOrder) -> str:
    pepitaPrefixOrderId = 'B2C'
    symbolVouchersequenceCode = 'B2C'
    axa = f"""
            <customerorder>
                <date>{po.date}</date>
                <orderid>{pepitaPrefixOrderId}-{po.id}</orderid>
                <currency>{po.total_shipping_price_currency}</currency>
                <vouchersequencecode>{symbolVouchersequenceCode}</vouchersequencecode>

                    <customercode><xsl:value-of select="CustSymbolCode"/></customercode><!-- Symbol vevő CODE ha van (Customer.Code) -->
                    <customeremail><xsl:value-of select="Email"/></customeremail><!-- Vevő email címe (Customer.Email)  Beállítás alapján vevő azonosításra használható.-->
                    <xsl:for-each select="Addresses">
                        <xsl:for-each select="Invoice">
                            <country><xsl:value-of select="Country"/></country><!-- Számlázási ország (Customer.InvoiceCountry) -->
                            <xsl:if test="County != ''"><region><xsl:value-of select="County"/></region></xsl:if><!-- Számlázási megye (Customer.InvoiceRegion) -->
                            <zip><xsl:value-of select="ZIP"/></zip><!-- Számlázási irányítószám (Customer.InvoiceZip) -->
                            <city><xsl:value-of select="City"/></city><!-- Számlázási város (Customer.InvoiceCity) -->
                            <street><xsl:value-of select="Street"/></street><!-- Számlázási utca (Customer.InvoiceStreet) -->
                        </xsl:for-each>
                        <xsl:for-each select="Shipping">
                            <transportname><xsl:value-of select="Name"/></transportname><!-- Telephely megnevezése (CustomerAddress.Name) -->
                            <transportcountry><xsl:value-of select="Country"/></transportcountry><!-- Telephely ország (CustomerAddress.Country) -->
                            <xsl:if test="County != ''"><transportregion><xsl:value-of select="County"/></transportregion></xsl:if> <!-- Telephely megye (CustomerAddress.Region) -->
                            <transportzip><xsl:value-of select="ZIP"/></transportzip><!-- Telephely irányítószám (CustomerAddress.Zip) -->
                            <transportcity><xsl:value-of select="City"/></transportcity><!-- Telephely város (CustomerAddress.City) -->
                            <transportstreet><xsl:value-of select="Street"/></transportstreet><!-- Telephely utca (CustomerAddress.Street) -->
                            <transportcontactname><xsl:value-of select="Name"/></transportcontactname><!-- Telephely kapcsolattartó (CustomerAddress.ContactName) -->
                        </xsl:for-each>
                    </xsl:for-each>
                </xsl:for-each>
                <transportmode><xsl:value-of select="Shipping/Name"/></transportmode><!-- szállítási mód (TransportMode.Name) -->
                <paymentmethod><xsl:value-of select="paymentMethodName"/></paymentmethod><!-- fizetési mód (PaymentMethod.Name) -->
                <paymentmethodtolerance><xsl:value-of select="paymentMethodTolerance"/></paymentmethodtolerance><!-- fizetési mód (PaymentMethod.ToleranceDay) -->
                <comment><xsl:value-of select="Comments/Comment/Text"/></comment><!-- Rendelés megjegyzése (CustomerOrder.Comment) -->
                <xsl:for-each select="Items/Item">
                <xsl:if test="not(Sku='shipping-cost')">
                    <detail>
                        <productcode><xsl:value-of select="Sku"/></productcode>
                        <quantity><xsl:value-of select="Quantity"/></quantity>
                        <unipricenet><xsl:value-of select="PriceNet" /></unipricenet>
                        <grossvalue><xsl:value-of select="computedPriceGross" /></grossvalue>
                    </detail>
                </xsl:if>
                </xsl:for-each>
                <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/order?id=<xsl:value-of select="Id" /><xsl:text>&amp;</xsl:text>orderkey=<xsl:value-of select="Key" /><xsl:text>&amp;</xsl:text>ipaddr=<xsl:value-of select="Others/Ip" />&amp;symbolid=</feedbackurl>
                <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/order?id=<xsl:value-of select="Id" /><xsl:text>&amp;</xsl:text>orderkey=<xsl:value-of select="Key" />&amp;errormsg=</errorurl>
            </customerorder>
    """
    
    return "xxxx"
