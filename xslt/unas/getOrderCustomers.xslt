<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="text" indent="no"  encoding="utf-8"/>
    <xsl:variable name="FeedbackUrl"><xsl:value-of select="unasFeedbackURL" /></xsl:variable>
    <xsl:template match="/Orders">
        <xsl:for-each select="Order">
        <xsl:variable name="TmpOrderID"><xsl:value-of select="Id" /></xsl:variable>
        <xsl:for-each select="Customer">
        <xsl:if test="not(Id)">
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
                <customeraddresses>
                    <xsl:for-each select="Addresses/Invoice">
                    <customeraddress>
                        <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/custinvaddr/unregistered?id=<xsl:value-of select="$TmpOrderID" />?symbolid=</feedbackurl>
                        <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/custinvaddr/unregistered?id=<xsl:value-of select="$TmpOrderID" />?errormsg=</errorurl>
                        <preferred>1</preferred>
                        <!--
                            <id>9<xsl:value-of select="/Customers/Customer/Id" /></id>
                            <sid>UNAS-CINV-<xsl:value-of select="Id" /></sid>
                            <code>UNAS-INV-<xsl:value-of select="Id" /></code>
                        -->
                        <phone><xsl:value-of select="../../Contact/Phone" /></phone>
                        <email><xsl:value-of select="../../Email" /></email>
                        <contactname><xsl:value-of select="../../Contact/Name" /></contactname>
                        <name><xsl:value-of select="../../Contact/Name" /></name>
                        <country><xsl:value-of select="Country" /></country>
                        <region><xsl:value-of select="County" /></region>
                        <zip><xsl:value-of select="ZIP" /></zip>
                        <city><xsl:value-of select="City" /></city>
                        <street><xsl:value-of select="Street" /></street>
                        <companytaxnumber><xsl:value-of select="TaxNumber" /></companytaxnumber>
                        <iscompany>
                            <xsl:choose>
                                <xsl:when test="CustomerType='company'" >1</xsl:when>
                                <xsl:otherwise>0</xsl:otherwise>
                            </xsl:choose>
                        </iscompany>
                        <description>UNAS nem tart kulon telephely adatot, ez az Invoice Address</description>
                        <deleted>0</deleted><!-- Not Used By UNAS, asszem -->
                    </customeraddress>
                    </xsl:for-each>
                    <xsl:for-each select="Addresses/Shipping">
                    <customeraddress>
                        <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/custshipaddr/unregistered?id=<xsl:value-of select="$TmpOrderID" />?symbolid=</feedbackurl>
                        <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/custshipaddr/unregistered?id=<xsl:value-of select="$TmpOrderID" />?errormsg=</errorurl>
                        <preferred>0</preferred>
                        <name><xsl:value-of        select="../../Contact/Name" /></name>
                        <contactname><xsl:value-of select="../../Contact/Name" /></contactname>
                        <email><xsl:value-of       select="../../Email" /></email>
                        <phone><xsl:value-of select="../../Contact/Phone" /></phone>
                        <country><xsl:value-of select="Country" /></country>
                        <region><xsl:value-of select="County" /></region>
                        <zip><xsl:value-of select="ZIP" /></zip>
                        <city><xsl:value-of select="City" /></city>
                        <street><xsl:value-of select="Street" /></street>
                        <companytaxnumber><xsl:value-of select="TaxNumber" /></companytaxnumber>
                        <iscompany>
                            <xsl:choose>
                                <xsl:when test="CustomerType='company'" >1</xsl:when>
                                <xsl:otherwise>0</xsl:otherwise>
                            </xsl:choose>
                        </iscompany>
                        <description>UNAS Customer Shipping Address info</description>
                        <deleted>0</deleted><!--  -->
                    </customeraddress>
                    </xsl:for-each>
                </customeraddresses>
            </Customer>
        </xsl:if>
        </xsl:for-each>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>