<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="/FulfilledCustomerOrdersByInvoice"> 
        <xsl:for-each select="CustomerOrder">
        <xsl:if test="not(SkipThisItem)">
            <Order> 
                <Action>modify</Action>
                <Key><xsl:value-of select="PrimeVoucherNumber" /></Key>
                <Status><xsl:value-of select="unasOrderStatus" /></Status>
                <StatusEmail>yes</StatusEmail>
                <Params>
                    <Param>
                        <Name>symbolId</Name>
                        <Value><xsl:value-of select="Id" /></Value>
                    </Param>
                </Params>
            </Order> 
        </xsl:if> <!-- Skip this item -->
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
