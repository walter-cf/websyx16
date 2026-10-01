from dataclasses import dataclass, field
from typing import List, Optional, Any
import xml.etree.ElementTree as ET

@dataclass
class Feedbackurl:
    feedbackurl: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Feedbackurl':
        """Create Feedbackurl instance from XML element."""
        return cls(
            feedbackurl=cls._parse_feedbackurl(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Feedbackurl instance to XML element."""
        element = ET.Element('feedbackurl')
        self._serialize_feedbackurl(element)
        return element
    @staticmethod
    def _parse_feedbackurl(element: ET.Element) -> str|None:
        """Parse feedbackurl from XML element."""
        elem = element.find('feedbackurl')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_feedbackurl(self, parent: ET.Element) -> None:
        """Serialize feedbackurl to XML element."""
        if self.feedbackurl is not None:
            elem = ET.SubElement(parent, 'feedbackurl')
            elem.text = str(self.feedbackurl)


@dataclass
class Errorurl:
    errorurl: str|None = None

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Errorurl':
        """Create Errorurl instance from XML element."""
        return cls(
            errorurl=cls._parse_errorurl(element)
        )
    
    def to_element(self) -> ET.Element:
        """Convert Errorurl instance to XML element."""
        element = ET.Element('errorurl')
        self._serialize_errorurl(element)
        return element
    @staticmethod
    def _parse_errorurl(element: ET.Element) -> str|None:
        """Parse errorurl from XML element."""
        elem = element.find('errorurl')
        if elem is not None and elem.text:
            return elem.text
        return None
    def _serialize_errorurl(self, parent: ET.Element) -> None:
        """Serialize errorurl to XML element."""
        if self.errorurl is not None:
            elem = ET.SubElement(parent, 'errorurl')
            elem.text = str(self.errorurl)


@dataclass
class Customercontact:
    feedbackurl: str | None = None  # XML element: feedbackurl
    name: str  = ''  # XML element: name
    sid: int = 0  # XML element: sid
    responsibility: str | None = None  # XML element: responsibility
    phone: str | None = None  # XML element: phone
    fax: str | None = None  # XML element: fax
    sms: str | None = None  # XML element: sms
    email: str | None = None  # XML element: email
    url: str | None = None  # XML element: url
    skype: str | None = None  # XML element: skype
    facebookurl: str | None = None  # XML element: facebookurl
    msn: str | None = None  # XML element: msn
    description: str | None = None  # XML element: description
    deleted: int = 0  # XML element: deleted

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customercontact':
        instance = cls()
        feedbackurl_elem = xml_element.find('feedbackurl')
        if feedbackurl_elem is not None:
            instance.feedbackurl = feedbackurl_elem.text
        name_elem = xml_element.find('name')
        if name_elem is not None:
            instance.name = name_elem.text or ''
        sid_elem = xml_element.find('sid')
        if sid_elem is not None:
            instance.sid = int(sid_elem.text or 0)
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
            instance.deleted = int(deleted_elem.text or '0')
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
    feedbackurl: str | None = None  # XML element: feedbackurl
    preferred: int = 0  # XML element: preferred
    id: int = 0  # XML element: id
    sid: int = 0
    code: str | None = None  # XML element: code
    name: str  = ''  # XML element: name
    country: str | None = None  # XML element: country
    region: str | None = None  # XML element: region
    zip: str | None = None  # XML element: zip
    city: str | None = None  # XML element: city
    street: str | None = None  # XML element: street
    housenumber: str | None = None  # XML element: housenumber
    contactname: str | None = None  # XML element: contactname
    phone: str | None = None  # XML element: phone
    fax: str | None = None  # XML element: fax
    email: str | None = None  # XML element: email
    iscompany: int = 0  # XML element: iscompany
    companytaxnumber: str | None = None  # XML element: companytaxnumber
    companygrouptaxnumber: str | None = None  # XML element: companygrouptaxnumber
    companyeutaxnumber: str | None = None  # XML element: companyeutaxnumber
    description: str | None = None  # XML element: description
    deleted: int = 0  # XML element: deleted

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customeraddress':
        instance = cls()
        feedbackurl_elem = xml_element.find('feedbackurl')
        if feedbackurl_elem is not None:
            instance.feedbackurl = feedbackurl_elem.text
        preferred_elem = xml_element.find('preferred')
        if preferred_elem is not None:
            instance.preferred = int(preferred_elem.text or '0')
        id_elem = xml_element.find('id')
        if id_elem is not None:
            instance.id = int(id_elem.text or '0')
        sid_elem = xml_element.find('sid')
        if sid_elem is not None:
            instance.sid = int(sid_elem.text or '0')
        code_elem = xml_element.find('code')
        if code_elem is not None:
            instance.code = code_elem.text
        name_elem = xml_element.find('name')
        if name_elem is not None:
            instance.name = name_elem.text or ''
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
            instance.iscompany = int(iscompany_elem.text or '0')
        companytaxnumber_elem = xml_element.find('companytaxnumber')
        if companytaxnumber_elem is not None:
            instance.companytaxnumber = companytaxnumber_elem.text
        companygrouptaxnumber_elem = xml_element.find('companygrouptaxnumber')
        if companygrouptaxnumber_elem is not None:
            instance.companygrouptaxnumber = companygrouptaxnumber_elem.text
        companyeutaxnumber_elem = xml_element.find('companyeutaxnumber')
        if companyeutaxnumber_elem is not None:
            instance.companyeutaxnumber = companyeutaxnumber_elem.text
        description_elem = xml_element.find('description')
        if description_elem is not None:
            instance.description = description_elem.text
        deleted_elem = xml_element.find('deleted')
        if deleted_elem is not None:
            instance.deleted = int(deleted_elem.text or '0')
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
    feedbackurl: str | None = None  # XML element: feedbackurl
    errorurl: str | None = None  # XML element: errorurl
    id: int = 0  # XML element: id
    sid: int = 0  # XML element: sid
    code: str | None = None  # XML element: code
    name: str | None = None  # XML element: name
    firstname: str | None = None  # XML element: firstname
    lastname: str | None = None  # XML element: lastname
    country: str | None = None  # XML element: country
    region: str | None = None  # XML element: region
    zip: str| None = None  # XML element: zip
    city: str | None = None  # XML element: city
    street: str | None = None  # XML element: street
    housenumber: str| None = None  # XML element: housenumber
    mailcountry: str | None = None  # XML element: mailcountry
    mailregion: str | None = None  # XML element: mailregion
    mailzip: str| None = None  # XML element: mailzip
    mailcity: str | None = None  # XML element: mailcity
    mailstreet: str | None = None  # XML element: mailstreet
    mailhousenumber: str| None = None  # XML element: mailhousenumber
    taxnumber: str | None = None  # XML element: taxnumber
    grouptaxnumber: str | None = None  # XML element: grouptaxnumber
    eutaxnumber: str | None = None  # XML element: eutaxnumber
    bankaccount: str | None = None  # XML element: bankaccount
    bankname: str | None = None  # XML element: bankname
    bankswiftcode: str | None = None  # XML element: bankswiftcode
    contactname: str | None = None  # XML element: contactname
    email: str | None = None  # XML element: email
    phone: str | None = None  # XML element: phone
    sms: str | None = None  # XML element: sms
    fax: str | None = None  # XML element: fax
    iscompany: int| None = None  # XML element: iscompany
    eumembership: int = 0  # XML element: eumembership
    description: str | None = None  # XML element: description
    customercategory: str | None = None  # XML element: customercategory
    pricecategoryname: str | None = None  # XML element: pricecategoryname
    discountpercent: float = 0  # XML element: discountpercent
    webusername: str | None = None  # XML element: webusername
    webpassword: str | None = None  # XML element: webpassword
    '''
    strexa: str | None = None  # XML element: strexa
    strexb: str | None = None  # XML element: strexb
    strexc: str | None = None  # XML element: strexc
    strexd: str | None = None  # XML element: strexd
    dateexa: str | None = None  # XML element: dateexa
    dateexb: str | None = None  # XML element: dateexb
    dateexc: str | None = None  # XML element: dateexc
    dateexd: str | None = None  # XML element: dateexd
    numexa: int| None = None  # XML element: numexa
    numexb: int| None = None  # XML element: numexb
    numexc: int| None = None  # XML element: numexc
    numexd: int| None = None  # XML element: numexd
    boolexa: int| None = None  # XML element: boolexa
    boolexb: int| None = None  # XML element: boolexb
    boolexc: int| None = None  # XML element: boolexc
    boolexd: int| None = None  # XML element: boolexd
    lookupexa: str | None = None  # XML element: lookupexa
    lookupexb: str | None = None  # XML element: lookupexb
    lookupexc: str | None = None  # XML element: lookupexc
    lookupexd: str | None = None  # XML element: lookupexd
    '''
    customeraddresses: Customeraddresses  | None = None
    customercontacts:  Customercontacts   | None = None

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> 'Customer':
        instance = cls()
        feedbackurl_elem = xml_element.find('feedbackurl')
        if feedbackurl_elem is not None:
            instance.feedbackurl = feedbackurl_elem.text
        errorurl_elem = xml_element.find('errorurl')
        if errorurl_elem is not None:
            instance.errorurl = errorurl_elem.text
        id_elem = xml_element.find('id')
        if id_elem is not None:
            instance.id = int(id_elem.text or 0)
        sid_elem = xml_element.find('sid')
        if sid_elem is not None:
            instance.sid = int(sid_elem.text or 0)
        code_elem = xml_element.find('code')
        if code_elem is not None:
            instance.code = code_elem.text
        name_elem = xml_element.find('name')
        if name_elem is not None:
            instance.name = name_elem.text
        firstname_elem = xml_element.find('firstname')
        if firstname_elem is not None:
            instance.firstname = firstname_elem.text
        lastname_elem = xml_element.find('lastname')
        if lastname_elem is not None:
            instance.lastname = lastname_elem.text
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
        mailcountry_elem = xml_element.find('mailcountry')
        if mailcountry_elem is not None:
            instance.mailcountry = mailcountry_elem.text
        mailregion_elem = xml_element.find('mailregion')
        if mailregion_elem is not None:
            instance.mailregion = mailregion_elem.text
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
        taxnumber_elem = xml_element.find('taxnumber')
        if taxnumber_elem is not None:
            instance.taxnumber = taxnumber_elem.text
        grouptaxnumber_elem = xml_element.find('grouptaxnumber')
        if grouptaxnumber_elem is not None:
            instance.grouptaxnumber = grouptaxnumber_elem.text
        eutaxnumber_elem = xml_element.find('eutaxnumber')
        if eutaxnumber_elem is not None:
            instance.eutaxnumber = eutaxnumber_elem.text
        bankaccount_elem = xml_element.find('bankaccount')
        if bankaccount_elem is not None:
            instance.bankaccount = bankaccount_elem.text
        bankname_elem = xml_element.find('bankname')
        if bankname_elem is not None:
            instance.bankname = bankname_elem.text
        bankswiftcode_elem = xml_element.find('bankswiftcode')
        if bankswiftcode_elem is not None:
            instance.bankswiftcode = bankswiftcode_elem.text
        contactname_elem = xml_element.find('contactname')
        if contactname_elem is not None:
            instance.contactname = contactname_elem.text
        email_elem = xml_element.find('email')
        if email_elem is not None:
            instance.email = email_elem.text
        phone_elem = xml_element.find('phone')
        if phone_elem is not None:
            instance.phone = phone_elem.text
        sms_elem = xml_element.find('sms')
        if sms_elem is not None:
            instance.sms = sms_elem.text
        fax_elem = xml_element.find('fax')
        if fax_elem is not None:
            instance.fax = fax_elem.text
        iscompany_elem = xml_element.find('iscompany')
        if iscompany_elem is not None:
            instance.iscompany = int(iscompany_elem.text or 0)
        eumembership_elem = xml_element.find('eumembership')
        if eumembership_elem is not None:
            instance.eumembership = int(eumembership_elem.text or 0)
        description_elem = xml_element.find('description')
        if description_elem is not None:
            instance.description = description_elem.text
        customercategory_elem = xml_element.find('customercategory')
        if customercategory_elem is not None:
            instance.customercategory = customercategory_elem.text
        pricecategoryname_elem = xml_element.find('pricecategoryname')
        if pricecategoryname_elem is not None:
            instance.pricecategoryname = pricecategoryname_elem.text
        discountpercent_elem = xml_element.find('discountpercent')
        if discountpercent_elem is not None:
            instance.discountpercent = float(discountpercent_elem.text or 0)
        webusername_elem = xml_element.find('webusername')
        if webusername_elem is not None:
            instance.webusername = webusername_elem.text
        webpassword_elem = xml_element.find('webpassword')
        if webpassword_elem is not None:
            instance.webpassword = webpassword_elem.text
            '''
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
        dateexc_elem = xml_element.find('dateexc')
        if dateexc_elem is not None:
            instance.dateexc = dateexc_elem.text
        dateexd_elem = xml_element.find('dateexd')
        if dateexd_elem is not None:
            instance.dateexd = dateexd_elem.text
        numexa_elem = xml_element.find('numexa')
        if numexa_elem is not None:
            instance.numexa = numexa_elem.text
        numexb_elem = xml_element.find('numexb')
        if numexb_elem is not None:
            instance.numexb = numexb_elem.text
        numexc_elem = xml_element.find('numexc')
        if numexc_elem is not None:
            instance.numexc = numexc_elem.text
        numexd_elem = xml_element.find('numexd')
        if numexd_elem is not None:
            instance.numexd = numexd_elem.text
        boolexa_elem = xml_element.find('boolexa') or False)
        if boolexa_elem is not None:
            instance.boolexa = boolexa_elem.text or False)
        boolexb_elem = xml_element.find('boolexb')
        if boolexb_elem is not None:
            instance.boolexb = boolexb_elem.text or False)
        boolexc_elem = xml_element.find('boolexc')
        if boolexc_elem is not None:
            instance.boolexc = bool(boolexc_elem.text or False)
        boolexd_elem = xml_element.find('boolexd')
        if boolexd_elem is not None:
            instance.boolexd = boolexd_elem.text or False)
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
            '''
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
