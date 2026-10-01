from dataclasses import dataclass, field
from typing import List, Optional, Any
import xml.etree.ElementTree as ET

@dataclass
class Customercontact:
    name: str|None = None  # XML element: name
    id: int = 0  # XML element: id
    responsibility: str|None = None  # XML element: responsibility
    phone: str|None = None  # XML element: phone
    fax: str|None = None  # XML element: fax
    sms: str|None = None  # XML element: sms
    email: str|None = None  # XML element: email
    url: str|None = None  # XML element: url
    skype: str|None = None  # XML element: skype
    facebookurl: str|None = None  # XML element: facebookurl
    msn: str|None = None  # XML element: msn
    description: str|None = None  # XML element: description
    deleted: int = 0  # XML element: deleted

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customercontact':
        instance = cls()
        name_elem = xml_element.find('name')
        if name_elem is not None:
            instance.name = name_elem.text
        id_elem = xml_element.find('id')
        if id_elem is not None:
            instance.id = int(id_elem.text or 0)
        responsibility_elem = xml_element.find('responsibility')
        if responsibility_elem is not None:
            instance.responsibility = responsibility_elem.text
        phone_elem = xml_element.find('phone')
        if phone_elem is not None:
            instance.phone = phone_elem.text
        fax_elem = xml_element.find('fax')
        if fax_elem is not None:
            instance.fax = fax_elem.text
        sms_elem = xml_element.find('sms')
        if sms_elem is not None:
            instance.sms = sms_elem.text
        email_elem = xml_element.find('email')
        if email_elem is not None:
            instance.email = email_elem.text
        url_elem = xml_element.find('url')
        if url_elem is not None:
            instance.url = url_elem.text
        skype_elem = xml_element.find('skype')
        if skype_elem is not None:
            instance.skype = skype_elem.text
        facebookurl_elem = xml_element.find('facebookurl')
        if facebookurl_elem is not None:
            instance.facebookurl = facebookurl_elem.text
        msn_elem = xml_element.find('msn')
        if msn_elem is not None:
            instance.msn = msn_elem.text
        description_elem = xml_element.find('description')
        if description_elem is not None:
            instance.description = description_elem.text
        deleted_elem = xml_element.find('deleted')
        if deleted_elem is not None:
            instance.deleted = int(deleted_elem.text or 0)
        return instance

@dataclass
class Customercontacts:
    customercontact: List[Customercontact] = field(default_factory=list)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customercontacts':
        instance = cls()
        customercontact_elements = xml_element.findall('customercontact')
        instance.customercontact = [Customercontact.from_xml(elem) for elem in customercontact_elements]
        return instance

@dataclass
class Customeraddress:
    preferred: int = 0  # XML element: preferred
    id: int = 0  # XML element: id
    code: str|None = None  # XML element: code
    name: str|None = None  # XML element: name
    country: str|None = None  # XML element: country
    region: str|None = None  # XML element: region
    zip: str|None = None  # XML element: zip
    city: str|None = None  # XML element: city
    street: str|None = None  # XML element: street
    housenumber: str|None = None  # XML element: housenumber
    contactname: str|None = None  # XML element: contactname
    phone: str|None = None  # XML element: phone
    fax: str|None = None  # XML element: fax
    email: str|None = None  # XML element: email
    iscompany: int = 0  # XML element: iscompany
    companytaxnumber: str|None = None  # XML element: companytaxnumber
    description: str|None = None  # XML element: description
    deleted: int = 0  # XML element: deleted

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customeraddress':
        instance = cls()
        preferred_elem = xml_element.find('preferred')
        if preferred_elem is not None:
            instance.preferred = int(preferred_elem.text or 0)
        id_elem = xml_element.find('id')
        if id_elem is not None:
            instance.id = int(id_elem.text or 0)
        code_elem = xml_element.find('code')
        if code_elem is not None:
            instance.code = code_elem.text
        name_elem = xml_element.find('name')
        if name_elem is not None:
            instance.name = name_elem.text
        country_elem = xml_element.find('country')
        if country_elem is not None:
            instance.country = country_elem.text
        region_elem = xml_element.find('region')
        if region_elem is not None:
            instance.region = region_elem.text
        zip_elem = xml_element.find('zip')
        if zip_elem is not None:
            instance.zip = zip_elem.text
        city_elem = xml_element.find('city')
        if city_elem is not None:
            instance.city = city_elem.text
        street_elem = xml_element.find('street')
        if street_elem is not None:
            instance.street = street_elem.text
        housenumber_elem = xml_element.find('housenumber')
        if housenumber_elem is not None:
            instance.housenumber = housenumber_elem.text
        contactname_elem = xml_element.find('contactname')
        if contactname_elem is not None:
            instance.contactname = contactname_elem.text
        phone_elem = xml_element.find('phone')
        if phone_elem is not None:
            instance.phone = phone_elem.text
        fax_elem = xml_element.find('fax')
        if fax_elem is not None:
            instance.fax = fax_elem.text
        email_elem = xml_element.find('email')
        if email_elem is not None:
            instance.email = email_elem.text
        iscompany_elem = xml_element.find('iscompany')
        if iscompany_elem is not None:
            instance.iscompany = int(iscompany_elem.text or 0)
        companytaxnumber_elem = xml_element.find('companytaxnumber')
        if companytaxnumber_elem is not None:
            instance.companytaxnumber = companytaxnumber_elem.text
        description_elem = xml_element.find('description')
        if description_elem is not None:
            instance.description = description_elem.text
        deleted_elem = xml_element.find('deleted')
        if deleted_elem is not None:
            instance.deleted = int(deleted_elem.text or 0)
        return instance
@dataclass
class Customeraddresses:
    customeraddress: List[Customeraddress] = field(default_factory=list)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customeraddresses':
        instance = cls()
        customeraddress_elements = xml_element.findall('customeraddress')
        instance.customeraddress = [Customeraddress.from_xml(elem) for elem in customeraddress_elements]
        return instance

@dataclass
class Customer:
    id: int = 0  # XML element: id
    code: str|None = None  # XML element: code
    customerstatus: int = 0  # XML element: customerstatus
    supplierstatus: int = 0  # XML element: supplierstatus
    name: str|None = None  # XML element: name
    searchname: str|None = None  # XML element: searchname
    customercategory: str|None = None  # XML element: customercategory
    suppliercategory: str|None = None  # XML element: suppliercategory
    currency: str|None = None  # XML element: currency
    invoicecountry: str|None = None  # XML element: invoicecountry
    invoiceregion: str|None = None  # XML element: invoiceregion
    invoicezip: str|None = None  # XML element: invoicezip
    invoicecity: str|None = None  # XML element: invoicecity
    invoicestreet: str|None = None  # XML element: invoicestreet
    invoicehousenumber: str|None = None  # XML element: invoicehousenumber
    mailcountry: str|None = None  # XML element: mailcountry
    mailregion: str|None = None  # XML element: mailregion
    mailname: str|None = None  # XML element: mailname
    mailzip: str|None = None  # XML element: mailzip
    mailcity: str|None = None  # XML element: mailcity
    mailstreet: str|None = None  # XML element: mailstreet
    mailhousenumber: str|None = None  # XML element: mailhousenumber
    paymentmethod: str|None = None  # XML element: paymentmethod
    paymentmethodtoleranceday: int = 0  # XML element: paymentmethodtoleranceday
    pricecategory: str|None = None  # XML element: pricecategory
    pricecategoryname: str|None = None  # XML element: pricecategoryname
    discountpercent: float|None = None  # XML element: discountpercent
    transportmode: str|None = None  # XML element: transportmode
    taxnumber: str|None = None  # XML element: taxnumber
    eutaxnumber: str|None = None  # XML element: eutaxnumber
    bankaccount: str|None = None  # XML element: bankaccount
    bankaccountiban: str|None = None  # XML element: bankaccountiban
    bankname: str|None = None  # XML element: bankname
    bankswiftcode: str|None = None  # XML element: bankswiftcode
    contactname: str|None = None  # XML element: contactname
    phone: str|None = None  # XML element: phone
    fax: str|None = None  # XML element: fax
    sms: str|None = None  # XML element: sms
    email: str|None = None  # XML element: email
    webusername: str|None = None  # XML element: webusername
    webpassword: str|None = None  # XML element: webpassword
    iscompany: int = 0  # XML element: iscompany
    eumembership: int = 0  # XML element: eumembership
    description: str|None = None  # XML element: description
    deleted: int = 0  # XML element: deleted
    strexa: str|None = None  # XML element: strexa
    strexb: str|None = None  # XML element: strexb
    strexc: str|None = None  # XML element: strexc
    strexd: str|None = None  # XML element: strexd
    dateexa: str|None = None  # XML element: dateexa
    dateexb: str|None = None  # XML element: dateexb
    numexa: int = 0  # XML element: numexa
    numexb: int = 0  # XML element: numexb
    numexc: int = 0  # XML element: numexc
    boolexa: int = 0  # XML element: boolexa
    boolexb: int = 0  # XML element: boolexb
    lookupexa: str|None = None  # XML element: lookupexa
    lookupexb: str|None = None  # XML element: lookupexb
    lookupexc: str|None = None  # XML element: lookupexc
    lookupexd: str|None = None  # XML element: lookupexd
    customeraddresses: Customeraddresses|None = None
    customercontacts: Customercontacts|None = None

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customer':
        instance = cls()
        id_elem = xml_element.find('id')
        if id_elem is not None:
            instance.id = int(id_elem.text or 0)
        code_elem = xml_element.find('code')
        if code_elem is not None:
            instance.code = code_elem.text
        customerstatus_elem = xml_element.find('customerstatus')
        if customerstatus_elem is not None:
            instance.customerstatus = int(customerstatus_elem.text or 0)
        supplierstatus_elem = xml_element.find('supplierstatus')
        if supplierstatus_elem is not None:
            instance.supplierstatus = int(supplierstatus_elem.text or 0)
        name_elem = xml_element.find('name')
        if name_elem is not None:
            instance.name = name_elem.text
        searchname_elem = xml_element.find('searchname')
        if searchname_elem is not None:
            instance.searchname = searchname_elem.text
        customercategory_elem = xml_element.find('customercategory')
        if customercategory_elem is not None:
            instance.customercategory = customercategory_elem.text
        suppliercategory_elem = xml_element.find('suppliercategory')
        if suppliercategory_elem is not None:
            instance.suppliercategory = suppliercategory_elem.text
        currency_elem = xml_element.find('currency')
        if currency_elem is not None:
            instance.currency = currency_elem.text
        invoicecountry_elem = xml_element.find('invoicecountry')
        if invoicecountry_elem is not None:
            instance.invoicecountry = invoicecountry_elem.text
        invoiceregion_elem = xml_element.find('invoiceregion')
        if invoiceregion_elem is not None:
            instance.invoiceregion = invoiceregion_elem.text
        invoicezip_elem = xml_element.find('invoicezip')
        if invoicezip_elem is not None:
            instance.invoicezip = invoicezip_elem.text
        invoicecity_elem = xml_element.find('invoicecity')
        if invoicecity_elem is not None:
            instance.invoicecity = invoicecity_elem.text
        invoicestreet_elem = xml_element.find('invoicestreet')
        if invoicestreet_elem is not None:
            instance.invoicestreet = invoicestreet_elem.text
        invoicehousenumber_elem = xml_element.find('invoicehousenumber')
        if invoicehousenumber_elem is not None:
            instance.invoicehousenumber = invoicehousenumber_elem.text
        mailcountry_elem = xml_element.find('mailcountry')
        if mailcountry_elem is not None:
            instance.mailcountry = mailcountry_elem.text
        mailregion_elem = xml_element.find('mailregion')
        if mailregion_elem is not None:
            instance.mailregion = mailregion_elem.text
        mailname_elem = xml_element.find('mailname')
        if mailname_elem is not None:
            instance.mailname = mailname_elem.text
        mailzip_elem = xml_element.find('mailzip')
        if mailzip_elem is not None:
            instance.mailzip = mailzip_elem.text
        mailcity_elem = xml_element.find('mailcity')
        if mailcity_elem is not None:
            instance.mailcity = mailcity_elem.text
        mailstreet_elem = xml_element.find('mailstreet')
        if mailstreet_elem is not None:
            instance.mailstreet = mailstreet_elem.text
        mailhousenumber_elem = xml_element.find('mailhousenumber')
        if mailhousenumber_elem is not None:
            instance.mailhousenumber = mailhousenumber_elem.text
        paymentmethod_elem = xml_element.find('paymentmethod')
        if paymentmethod_elem is not None:
            instance.paymentmethod = paymentmethod_elem.text
        paymentmethodtoleranceday_elem = xml_element.find('paymentmethodtoleranceday')
        if paymentmethodtoleranceday_elem is not None:
            instance.paymentmethodtoleranceday = int(paymentmethodtoleranceday_elem.text or 0)
        pricecategory_elem = xml_element.find('pricecategory')
        if pricecategory_elem is not None:
            instance.pricecategory = pricecategory_elem.text
        pricecategoryname_elem = xml_element.find('pricecategoryname')
        if pricecategoryname_elem is not None:
            instance.pricecategoryname = pricecategoryname_elem.text
        discountpercent_elem = xml_element.find('discountpercent')
        if discountpercent_elem is not None:
            instance.discountpercent = float(discountpercent_elem.text or 0)
        transportmode_elem = xml_element.find('transportmode')
        if transportmode_elem is not None:
            instance.transportmode = transportmode_elem.text
        taxnumber_elem = xml_element.find('taxnumber')
        if taxnumber_elem is not None:
            instance.taxnumber = taxnumber_elem.text
        eutaxnumber_elem = xml_element.find('eutaxnumber')
        if eutaxnumber_elem is not None:
            instance.eutaxnumber = eutaxnumber_elem.text
        bankaccount_elem = xml_element.find('bankaccount')
        if bankaccount_elem is not None:
            instance.bankaccount = bankaccount_elem.text
        bankaccountiban_elem = xml_element.find('bankaccountiban')
        if bankaccountiban_elem is not None:
            instance.bankaccountiban = bankaccountiban_elem.text
        bankname_elem = xml_element.find('bankname')
        if bankname_elem is not None:
            instance.bankname = bankname_elem.text
        bankswiftcode_elem = xml_element.find('bankswiftcode')
        if bankswiftcode_elem is not None:
            instance.bankswiftcode = bankswiftcode_elem.text
        contactname_elem = xml_element.find('contactname')
        if contactname_elem is not None:
            instance.contactname = contactname_elem.text
        phone_elem = xml_element.find('phone')
        if phone_elem is not None:
            instance.phone = phone_elem.text
        fax_elem = xml_element.find('fax')
        if fax_elem is not None:
            instance.fax = fax_elem.text
        sms_elem = xml_element.find('sms')
        if sms_elem is not None:
            instance.sms = sms_elem.text
        email_elem = xml_element.find('email')
        if email_elem is not None:
            instance.email = email_elem.text
        webusername_elem = xml_element.find('webusername')
        if webusername_elem is not None:
            instance.webusername = webusername_elem.text
        webpassword_elem = xml_element.find('webpassword')
        if webpassword_elem is not None:
            instance.webpassword = webpassword_elem.text
        iscompany_elem = xml_element.find('iscompany')
        if iscompany_elem is not None:
            instance.iscompany = int(iscompany_elem.text or 0)
        eumembership_elem = xml_element.find('eumembership')
        if eumembership_elem is not None:
            instance.eumembership = int(eumembership_elem.text or 0)
        description_elem = xml_element.find('description')
        if description_elem is not None:
            instance.description = description_elem.text
        deleted_elem = xml_element.find('deleted')
        if deleted_elem is not None:
            instance.deleted = int(deleted_elem.text or 0)
        strexa_elem = xml_element.find('strexa')
        if strexa_elem is not None:
            instance.strexa = strexa_elem.text
        strexb_elem = xml_element.find('strexb')
        if strexb_elem is not None:
            instance.strexb = strexb_elem.text
        strexc_elem = xml_element.find('strexc')
        if strexc_elem is not None:
            instance.strexc = strexc_elem.text
        strexd_elem = xml_element.find('strexd')
        if strexd_elem is not None:
            instance.strexd = strexd_elem.text
        dateexa_elem = xml_element.find('dateexa')
        if dateexa_elem is not None:
            instance.dateexa = dateexa_elem.text
        dateexb_elem = xml_element.find('dateexb')
        if dateexb_elem is not None:
            instance.dateexb = dateexb_elem.text
        numexa_elem = xml_element.find('numexa')
        if numexa_elem is not None:
            instance.numexa = int(numexa_elem.text or 0)
        numexb_elem = xml_element.find('numexb')
        if numexb_elem is not None:
            instance.numexb = int(numexb_elem.text or 0)
        numexc_elem = xml_element.find('numexc')
        if numexc_elem is not None:
            instance.numexc = int(numexc_elem.text or 0)
        boolexa_elem = xml_element.find('boolexa')
        if boolexa_elem is not None:
            instance.boolexa = bool(boolexa_elem.text or False)
        boolexb_elem = xml_element.find('boolexb')
        if boolexb_elem is not None:
            instance.boolexb = bool(boolexb_elem.text or False)
        lookupexa_elem = xml_element.find('lookupexa')
        if lookupexa_elem is not None:
            instance.lookupexa = lookupexa_elem.text
        lookupexb_elem = xml_element.find('lookupexb')
        if lookupexb_elem is not None:
            instance.lookupexb = lookupexb_elem.text
        lookupexc_elem = xml_element.find('lookupexc')
        if lookupexc_elem is not None:
            instance.lookupexc = lookupexc_elem.text
        lookupexd_elem = xml_element.find('lookupexd')
        if lookupexd_elem is not None:
            instance.lookupexd = lookupexd_elem.text
        customeraddresses_elem = xml_element.find('customeraddresses')
        if customeraddresses_elem is not None:
            instance.customeraddresses = Customeraddresses.from_xml(customeraddresses_elem)
        customercontacts_elem = xml_element.find('customercontacts')
        if customercontacts_elem is not None:
            instance.customercontacts = Customercontacts.from_xml(customercontacts_elem)
        return instance

@dataclass
class Customers:
    customer: List[Customer] = field(default_factory=list)

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customers':
        instance = cls()
        customer_elements = xml_element.findall('Customer')
        instance.customer = [Customer.from_xml(elem) for elem in customer_elements]
        return instance
