
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="yes" />

    <xsl:template match="Customers">
        <xsl:variable name="SymbolCustomerID"><xsl:value-of select="Params/Param[contains('symbolId',Name)]/Value" /></xsl:variable>
        <Customers>
            <xsl:for-each select="Customer">
                <Customer>
                <unasId><xsl:value-of select="Id" /></unasId>
                <xsl:if test="$SymbolCustomerID != ''">
                    <sid><xsl:value-of select="$SymbolCustomerID" /></sid>
                </xsl:if>
                <email><xsl:value-of select="Email" /></email>
                <customeraddresses>
                    <customeraddress>
                        <CIM0><xsl:value-of select="Addresses/Invoice/Country" />(<xsl:if test="Addresses/Invoice/County != ''"><xsl:value-of select="Addresses/Invoice/County" /></xsl:if>) <xsl:value-of select="Addresses/Invoice/ZIP" />. <xsl:value-of select="Addresses/Invoice/City" /></CIM0>
                        <CIM1><xsl:value-of select="Addresses/Invoice/StreetName"  disable-output-escaping="yes" /><xsl:if test="Addresses/Invoice/StreetType"><xsl:text> </xsl:text></xsl:if><xsl:value-of  select="Addresses/Invoice/StreetType"  disable-output-escaping="yes" /><xsl:if test="Addresses/Invoice/StreetNumber"><xsl:text> </xsl:text></xsl:if><xsl:value-of select="Addresses/Invoice/StreetNumber" /></CIM1>
                        <CIM2><xsl:value-of select="Addresses/Invoice/Street" /></CIM2>
                    </customeraddress>
                    <xsl:for-each select="Addresses/Shipping">
                    <customeraddress>
                        <CIM0><xsl:value-of select="Country" />(<xsl:if test="County != ''"><xsl:value-of select="County" /></xsl:if>) <xsl:value-of select="ZIP" />. <xsl:value-of select="City" /></CIM0>
                        <CIM1><xsl:value-of select="StreetName" /><xsl:if test="StreetType"><xsl:text> </xsl:text></xsl:if><xsl:value-of select="StreetType" /><xsl:if test="StreetNumber"><xsl:text> </xsl:text></xsl:if><xsl:value-of select="StreetNumber" /></CIM1>
                        <CIM2><xsl:value-of select="Street" /></CIM2>
                    </customeraddress>
                    </xsl:for-each>
                    <!-- -->
                    <xsl:for-each select="Addresses/Other">
                    <xsl:if test="not(skipOtherAddress)">
                    <customeraddress>
                        <CIM0><xsl:value-of select="Country" />(<xsl:if test="County != ''"><xsl:value-of select="County" /></xsl:if>) <xsl:value-of select="ZIP" />. <xsl:value-of select="City" /></CIM0>
                        <CIM1><xsl:value-of select="StreetName" /><xsl:if test="StreetType"><xsl:text> </xsl:text></xsl:if><xsl:value-of select="StreetType" /><xsl:if test="StreetNumber"><xsl:text> </xsl:text></xsl:if><xsl:value-of select="StreetNumber" /></CIM1>
                        <CIM2><xsl:value-of select="Street" /></CIM2>
                    </customeraddress>
                    </xsl:if>
                    </xsl:for-each>
                </customeraddresses>
            </Customer>
        </xsl:for-each>
        </Customers>
    </xsl:template>
</xsl:stylesheet>