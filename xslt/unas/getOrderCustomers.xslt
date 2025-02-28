<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="text" indent="no"  encoding="utf-8"/>
    <xsl:template match="Orders">
        <xsl:variable name="FeedbackUrl"><xsl:value-of select="unasFeedbackURL" /></xsl:variable>
        <xsl:for-each select="Order">
        <xsl:variable name="TmpOrderID"><xsl:value-of select="Id" /></xsl:variable>
        <xsl:for-each select="Customer">
        <xsl:if test="not(SkipThisItem)">
            <Customer>
                <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/customer/unregistered?id=<xsl:value-of select="$TmpOrderID" />?symbolid=</feedbackurl>
                <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/customer/unregistered?id=<xsl:value-of select="$TmpOrderID" />?errormsg=</errorurl>
                <!-- ezek nincsenek meg az UNASban?
                    <id>UNAS-C-<xsl:value-of select="Id" /></id>                - - web-es ID
                    <sid>4357</sid>                                             - - symbol ID
                    <code>WEB<xsl:value-of select="Id" /></code>                - - Vevő kódja (Customer.Code)
                    <code>UNAS0<xsl:value-of select="Id" /></code>
                 nem tehetem bele , mert rakeres a g. symbol   
                    <code>UCU<xsl:value-of select="$TmpOrderID" /></code>
                -->
                <name><xsl:value-of select="Addresses/Invoice/Name" /></name>
                <country><xsl:value-of select="Addresses/Invoice/Country" /></country>
                <region><xsl:value-of select="Addresses/Invoice/County" /></region>
                <zip><xsl:value-of select="Addresses/Invoice/ZIP" /></zip>
                <city><xsl:value-of select="Addresses/Invoice/City" /></city>
                <street><xsl:value-of select="Addresses/Invoice/Street" /></street>
                <!-- @20240916 - Ezt most  kiveszem cimek javitasa miatt
                <housenumber><xsl:value-of select="Addresses/Invoice/StreetNumber" /></housenumber>
                 -->
                <taxnumber><xsl:value-of select="Addresses/Invoice/TaxNumber" /></taxnumber>
                <webusername><xsl:value-of select="Username" /></webusername>
                <email><xsl:value-of select="Email" /></email>
                <contactname><xsl:value-of select="Contact/Name" /></contactname>
                <phone><xsl:value-of select="Contact/Phone" /></phone>
                <sms><xsl:value-of select="Contact/Mobile" /></sms>
                <xsl:if test="Discount/Total > 0">
                    <!-- <discountpercent><xsl:value-of select="100 * Discount/Direct div Discount/Total" /></discountpercent> -->
                    <discountpercent><xsl:value-of select="Discount/Direct" /></discountpercent>
                </xsl:if>
                <iscompany>
                    <xsl:choose>
                        <xsl:when test="Addresses/Invoice/CustomerType='company'" >1</xsl:when>
                        <xsl:otherwise>0</xsl:otherwise>
                    </xsl:choose>
                </iscompany>
                <xsl:if test="not(SkipAddressShipping)">
                    <customeraddresses>
                    <customeraddress>
                        <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/custshipaddr/unregistered?id=<xsl:value-of select="$TmpOrderID" />?symbolid=</feedbackurl>
                        <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/custshipaddr/unregistered?id=<xsl:value-of select="$TmpOrderID" />?errormsg=</errorurl>
                        <preferred>0</preferred>
                        <name><xsl:value-of        select="Contact/Name" /></name>
                        <contactname><xsl:value-of select="Contact/Name" /></contactname>
                        <email><xsl:value-of       select="Email" /></email>
                        <phone><xsl:value-of select="Contact/Phone" /></phone>
                        <country><xsl:value-of select="Addresses/Shipping/Country" /></country>
                        <region><xsl:value-of select="Addresses/Shipping/County" /></region>
                        <zip><xsl:value-of select="Addresses/Shipping/ZIP" /></zip>
                        <city><xsl:value-of select="Addresses/Shipping/City" /></city>
                        <street><xsl:value-of select="Addresses/Shipping/Street" /></street>
                        <companytaxnumber><xsl:value-of select="Addresses/Shipping/TaxNumber" /></companytaxnumber>
                        <iscompany>
                            <xsl:choose>
                                <xsl:when test="Addresses/Shipping/CustomerType='company'" >1</xsl:when>
                                <xsl:otherwise>0</xsl:otherwise>
                            </xsl:choose>
                        </iscompany>
                        <description>UNAS Customer Shipping Address info</description>
                        <deleted>0</deleted><!--  -->
                    </customeraddress>
                    </customeraddresses>
                </xsl:if>
            </Customer>
        </xsl:if>
        </xsl:for-each>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>