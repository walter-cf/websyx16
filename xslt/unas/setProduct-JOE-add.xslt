<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:for-each select="Products/Product">
    <xsl:if test="not(SkipThisItem)">
        <Product>
            <Action><xsl:value-of select="unasProductAction"/> </Action>
            <Sku><xsl:value-of select="code" /></Sku>
            <Name><xsl:value-of select="name" /></Name>
            <!--  Felteteles ADD -->
            <xsl:if test="unasProductAction = 'add'">
                <Prices>
                    <Vat><xsl:value-of select="vat"/></Vat>
                    <Price>
                        <Type>normal</Type>
                        <Net>
                            <xsl:if test="netprices"><xsl:value-of select="netprices"/></xsl:if>
                            <xsl:if test="not(netprices)">1000000</xsl:if>
                        </Net>
                        <Gross>
                            <xsl:if test="grossprices &gt; 0"><xsl:value-of select="grossprices"/></xsl:if>
                            <xsl:if test="not(netprices)">1270000</xsl:if>
                        </Gross>
                    </Price>
                </Prices>
                <Params>
                    <Param>
                        <Type>num</Type>
                        <Name>symbolId</Name>
                        <Value><xsl:value-of select="id" /></Value>
                    </Param>
                    <xsl:if test="barcode" >
                        <Param>
                            <Type>string</Type>
                            <Name>EAN</Name>
                            <Value><xsl:value-of select="barcode" /></Value>
                        </Param>
                    </xsl:if>
                    <xsl:if test="manufacturer">
                        <Param>
                            <Type>string</Type>
                            <Name>Gyarto</Name>
                            <Value><xsl:value-of select="manufacturer" /></Value>
                        </Param>
                    </xsl:if>
                </Params>

                <Statuses>
                    <Status>
                        <Type>base</Type>
                        <Value><xsl:value-of select="unasProductStatus"/></Value>
                    </Status>
                </Statuses>
                <!-- -->
                <xsl:if test="unasActionWebCategory">
                    <Categories>
                        <Category>
                            <Id><xsl:value-of select="unasActionWebCategory" /></Id>
                            <xsl:if test="unasActionWebCategoryName">
                                <Name><xsl:value-of select="unasActionWebCategoryName" /></Name>
                            </xsl:if>
                            <Type>base</Type>
                        </Category>
                    </Categories>
                </xsl:if>

            <Unit><xsl:value-of select="quantityunit" /></Unit>
            <xsl:if test="weight > 0"><Weight><xsl:value-of select="weight" /></Weight></xsl:if>
        </Product>
    </xsl:if> <!-- Webdisplay is 1? = not(SkipThisItem) -->
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
