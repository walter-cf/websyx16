
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="yes" />

    <xsl:template match="Customers">
        <xsl:variable name="FeedbackUrl"><xsl:value-of select="unasFeedbackURL" /></xsl:variable>
        <Customers>
            <xsl:if test="UnregisteredCustomers">
                <xsl:value-of select="UnregisteredCustomers" disable-output-escaping="yes" />
            </xsl:if>
            
            <xsl:for-each select="Customer">
            <xsl:if test="not(SkipThisCustomerItem)">
            <Customer>
                <xsl:variable name="UnasCustomerID"><xsl:value-of select="Id" /></xsl:variable>
                <xsl:variable name="SymbolCustomerID"><xsl:value-of select="Params/Param[contains('symbolId',Name)]/Value" /></xsl:variable>
                
                <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/customer?id=<xsl:value-of select="Id" /><xsl:text>&amp;</xsl:text>ipaddr=<xsl:value-of select="Others/Ip" />&amp;symbolid=</feedbackurl>
                <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/customer?id=<xsl:value-of select="Id" />&amp;errormsg=</errorurl>

                <id><xsl:value-of select="$UnasCustomerID" /></id>
                <xsl:if test="$SymbolCustomerID != ''">
                    <sid><xsl:value-of select="$SymbolCustomerID" /></sid>
                </xsl:if>
                <contactname><xsl:value-of select="Contact/Name" /></contactname>
                <name><xsl:value-of select="Addresses/Invoice/Name" /></name> <!-- VAGY inkabb sima Name??? -->
                <country><xsl:value-of select="Addresses/Invoice/Country" /></country>
                <xsl:if test="Addresses/Invoice/County != ''"><region><xsl:value-of select="Addresses/Invoice/County" /></region></xsl:if>
                <zip><xsl:value-of select="Addresses/Invoice/ZIP" /></zip>
                <city><xsl:value-of select="Addresses/Invoice/City" /></city>
                <street><xsl:value-of select="Addresses/Invoice/Street" /></street>
                <!-- @20240615 - Ugy dontottem, mostantol NINCS HouseNumber !!!
                    <street><xsl:value-of  select="Addresses/Invoice/StreetName"  disable-output-escaping="yes" /><xsl:if test="Addresses/Invoice/StreetType"><xsl:text> </xsl:text></xsl:if><xsl:value-of select="Addresses/Invoice/StreetType" /></street>
                    <housenumber><xsl:value-of select="Addresses/Invoice/StreetNumber" /></housenumber>
                -->
                <customercategory><xsl:value-of select="unasCustomerCategory" /></customercategory>
                <taxnumber><xsl:value-of select="Addresses/Invoice/TaxNumber" /></taxnumber>
                <email><xsl:value-of select="Email" /></email>
                <phone><xsl:value-of select="Contact/Phone" /></phone>
                <sms><xsl:value-of select="Contact/Mobile" /></sms>
                <iscompany>
                    <xsl:choose>
                        <xsl:when test="not(Addresses/Invoice/TaxNumber='')" >1</xsl:when>
                        <xsl:otherwise>0</xsl:otherwise>
                    </xsl:choose>
                </iscompany>
                <description><xsl:value-of select="Comment" /></description>
                <discountpercent><xsl:value-of select="Discount/Direct" /></discountpercent>
                <webusername><xsl:value-of select="Username" /></webusername>
                <xsl:if test="handleCustomerAddresses">
                    <customeraddresses>
                        <xsl:for-each select="Addresses/Shipping">
                        <customeraddress>
                            <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/custshipaddr?id=<xsl:value-of select="$UnasCustomerID" /><xsl:text>&amp;</xsl:text>idx=<xsl:value-of select="otherAddressIndex" /><xsl:text>&amp;</xsl:text>symbolid=</feedbackurl>
                            <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/custshipaddr?id=<xsl:value-of select="$UnasCustomerID" /><xsl:text>&amp;</xsl:text>idx=<xsl:value-of select="otherAddressIndex" /><xsl:text>&amp;</xsl:text>errormsg=</errorurl>
                            <preferred><xsl:value-of select="unasFirstAddresItem" /></preferred>
                            <code><xsl:value-of select="customerAddressCode" /></code>
                            <name><xsl:value-of select="Name" /></name>
                            <country><xsl:value-of select="Country" /></country>
                            <xsl:if test="County != ''"><region><xsl:value-of select="County" /></region></xsl:if>
                            <zip><xsl:value-of select="ZIP" /></zip>
                            <city><xsl:value-of select="City" /></city>
                            <street><xsl:value-of select="Street" /></street>
                                <!-- @20240615 - Ugy dontottem, mostantol NINCS HouseNumber !!!
                                    <street><xsl:if test="StreetType"><xsl:text> </xsl:text></xsl:if><xsl:value-of select="StreetType" /></street>
                                    <housenumber><xsl:value-of select="StreetNumber" /></housenumber>
                                -->
                            <contactname><xsl:value-of select="/Customers/Customer/Contact/Name" /></contactname>
                            <companytaxnumber><xsl:value-of select="TaxNumber" /></companytaxnumber>
                            <phone><xsl:value-of select="/Customers/Customer/Contact/Phone" /></phone>
                            <iscompany>
                                <xsl:choose>
                                    <xsl:when test="not(TaxNumber = '')" >1</xsl:when>
                                    <xsl:otherwise>0</xsl:otherwise>
                                </xsl:choose>
                            </iscompany>
                            <description>UNAS Customer Shipping Address</description>
                            <deleted>0</deleted><!--  -->
                        </customeraddress>
                        </xsl:for-each>
                        <!-- -->
                        <xsl:for-each select="Addresses/Other">
                        <xsl:if test="not(skipOtherAddress)">
                        <customeraddress>
                            <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/custothaddr?id=<xsl:value-of select="$UnasCustomerID" /><xsl:text>&amp;</xsl:text>idx=<xsl:value-of select="otherAddressIndex" /><xsl:text>&amp;</xsl:text>symbolid=</feedbackurl>
                            <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/custothaddr?id=<xsl:value-of select="$UnasCustomerID" /><xsl:text>&amp;</xsl:text>idx=<xsl:value-of select="otherAddressIndex" /><xsl:text>&amp;</xsl:text>errormsg=</errorurl>

                            <preferred>0</preferred>

                            <code><xsl:value-of select="customerAddressCode" /></code>

                            <name><xsl:value-of select="Name" /></name>
                            <country><xsl:value-of select="Country" /></country>
                            <xsl:if test="County != ''"><region><xsl:value-of select="County" /></region></xsl:if>
                            <zip><xsl:value-of select="ZIP" /></zip>
                            <city><xsl:value-of select="City" /></city>
                            <street><xsl:value-of select="Street" /></street>
                        <!-- @20240615 - Ugy dontottem, mostantol NINCS HouseNumber !!!
                            <street><xsl:if test="StreetType"><xsl:text> </xsl:text></xsl:if><xsl:value-of select="StreetType" /></street>
                            <housenumber><xsl:value-of select="StreetNumber" /></housenumber>
                        -->
                            <xsl:if test="TaxNumber"></xsl:if>
                            <xsl:choose>
                                    <xsl:when test="not(TaxNumber) and not(TaxNumber = '')" >
                                        <companytaxnumber><xsl:value-of select="TaxNumber" /></companytaxnumber>
                                        <iscompany>1</iscompany>
                                    </xsl:when>
                                    <xsl:otherwise><iscompany>0</iscompany></xsl:otherwise>
                            </xsl:choose>

                            <description>UNAS Customer Other Address info - idx:<xsl:value-of select="otherAddressIndex" /></description>
                            <deleted>0</deleted>
                        </customeraddress>
                        </xsl:if>
                        </xsl:for-each>
                    </customeraddresses>
                </xsl:if>
                <!-- Nem tom mit irjak bele
                <customercontacts>
                    <customercontact></customercontact>
                    <customercontact></customercontact>
                </customercontacts>
                -->
            </Customer>
            </xsl:if>
            </xsl:for-each>
        </Customers>
    </xsl:template>
</xsl:stylesheet>