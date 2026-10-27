<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="/FulfilledCustomerOrdersByInvoice"> 
        <xsl:for-each select="CustomerOrder">
        <xsl:if test="not(SkipThisItem)">
            <Order> 
                <Action>modify</Action>
                <Key><xsl:value-of select="unasOrderKey" /></Key>
                <Status><xsl:value-of select="unasOrderStatus" /></Status>
                <StatusEmail>yes</StatusEmail>
                <Params>
                    <Param>
                        <Name>symbolId</Name>
                        <Value><xsl:value-of select="Id" /></Value>
                    </Param>
                </Params>
            <xsl:for-each select="Invoice">
                <Invoice>
                  <xsl:if test="invoiceStatus"><Status><xsl:value-of select="invoiceStatus" /></Status></xsl:if>
                  <xsl:if test="invoiceNumber"><Number><xsl:value-of select="invoiceNumber" /></Number></xsl:if>
                  <xsl:if test="invoicePdfUrl"><Url><xsl:value-of select="invoicePdfUrl" /></Url></xsl:if>
                </Invoice>
            </xsl:for-each> <!-- Invoice -->
            <xsl:if test="InvoiceStorno"><!-- Not costructed YET! -->
                <Storno>
                  <Number>number</Number>
                  <Url>url</Url>
                </Storno>
            </xsl:if> <!-- InvoiceStorno  NotUsed yet! -->
            </Order> 
        </xsl:if> <!-- Skip this item -->
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
