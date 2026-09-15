<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
   <xsl:output method="xml" encoding="utf8" />    
    <xsl:template match="SupplierOrders">
    <xsl:for-each select="SupplierOrder">
        <xsl:if test="not(SkipThisItem)">
            <Product>
                <Action>modify</Action>
                <Sku><xsl:value-of select="ProductCode" /></Sku>
                <!-- Quantity : <xsl:value-of select="Quantity" />  -->
                <Params>
                    <Param>
                        <Type>text</Type>
                        <xsl:if test="supplierParamId > 0">
                            <Id><xsl:value-of select="supplierParamId" /></Id>
                        </xsl:if>
                        <xsl:if test="supplierParamName">
                            <Name><xsl:value-of select="supplierParamName" /></Name>
                        </xsl:if>
                        <Value><xsl:value-of select="DeliveryDate" /></Value>
                    </Param>
                </Params>
            </Product>
        </xsl:if>
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
