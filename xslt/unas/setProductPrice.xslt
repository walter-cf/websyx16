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
                <Prices>
                <xsl:for-each select="price">
                    <!-- xsl:if test="retValValid > 1" -->
                    <xsl:if test="not(SkipThisItem)">
                        <xsl:if test="not(unasPriceSpecial)">
                        <Price>
                            <Type>normal</Type>
                            <Net><xsl:value-of select="value"/></Net>
                            <Gross><xsl:value-of select="calculatedGrossPrice"/></Gross>
                        </Price>
                        </xsl:if><!-- test="unasPriceSpecial == 0"  -->
                        <xsl:if test="unasPriceSpecial">
                        <Price>
                                <Type>special</Type>
                                <xsl:if test="groupName">
                                    <GroupName><xsl:value-of select="groupName"/></GroupName>
                                </xsl:if>
                                <Gross><xsl:value-of select="calculatedGrossPrice"/></Gross>
                                <Currency><xsl:value-of select="priceCurrency"/></Currency>
                                <xsl:if test="unasPriceCurrencyFilter">
                                    <CurrencyFilter><xsl:value-of select="unasPriceCurrencyFilter"/></CurrencyFilter>                                            
                                </xsl:if>
                                <!-- 
                                <Start><xsl:value-of select="offerStart"/></Start>
                                <End><xsl:value-of select="offerEnd"/></End>
                                -->
                        </Price>
                        </xsl:if><!-- test="unasPriceSpecial == 1"  -->
                        <xsl:if test="unasPriceArea">
                        <Price>
                                <Type>special</Type>
                                <xsl:if test="groupName">
                                    <GroupName><xsl:value-of select="groupName"/></GroupName>
                                </xsl:if>
                                <Gross><xsl:value-of select="calculatedGrossPrice"/></Gross>
                                <Currency><xsl:value-of select="priceCurrency"/></Currency>
                                <AreaName><xsl:value-of select="unasPriceArea"/></AreaName>
                                <CurrencyFilter><xsl:value-of select="unasPriceCurrencyFilter"/></CurrencyFilter>                                            
                        </Price>
                        </xsl:if><!-- test="unasPriceArea > 0""  -->
                    </xsl:if> <!-- test="not(SkipThisItem)"  -->
                </xsl:for-each>
                </Prices>
            </Product>
        </xsl:if>
        </xsl:if>
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
