<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
   <xsl:output method="xml" encoding="utf8" />    
    <xsl:template match="ProductPrices">
    <xsl:for-each select="ProductPrice">
        <xsl:variable name="ProductCode" select="productcode"/>
        <xsl:variable name="SymbolIdIsNull" select="symbolIdIsNull"/>
        <!-- 
        <xsl:variable name="RetValProduct" select="retValProduct"/>
        <! - - xsl:if test="$RetValProduct > 0 or $SymbolIdIsNull > 0" - - >
        -->
        <xsl:if test="product > 0"> <!-- symbolId -->
        <xsl:if test="not(SkipThisItem)">
            <Product>
                <Action>modify</Action>
                <Sku><xsl:value-of select="productcode" /></Sku>
                <xsl:for-each select="price">
                    <xsl:if test="retValValid > 1">
                        <Prices>
                            <Price>
                                <Type>normal</Type>
                                <Net><xsl:value-of select="value"/></Net>
                                <Gross><xsl:value-of select="calculatedGrossPrice"/></Gross>
                            </Price>
                        </Prices>
                    </xsl:if>
                </xsl:for-each>
                <xsl:if test="$SymbolIdIsNull > 0">
                    <Params>
                        <Param>
                            <Type>num</Type>
                            <Name>symbolId</Name>
                            <Value><xsl:value-of select="product" /></Value>
                        </Param>
                    </Params>
                </xsl:if>
            </Product>
        </xsl:if>
        </xsl:if>

    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
