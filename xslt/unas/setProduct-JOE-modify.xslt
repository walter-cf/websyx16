<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:for-each select="Products/Product">
    <xsl:if test="not(SkipThisItem)">
        <Product>
            <Action><xsl:value-of select="unasProductAction"/> </Action>
            <Sku><xsl:value-of select="code" /></Sku>
            <Name><xsl:value-of select="name" /></Name>
            <xsl:if test="not(unasProductAction = 'add')">
                <Prices>
                    <Vat><xsl:value-of select="vat"/></Vat>
                </Prices>

                <Statuses>
                    <Status>
                        <Type>base</Type>
                        <Value><xsl:value-of select="unasProductStatus"/></Value>
                    </Status>
                </Statuses>

                <Params>
                    <Param>
                        <Type>num</Type>
                        <Name>symbolId</Name>
                        <Value><xsl:value-of select="id" /></Value>
                    </Param>
                    <xsl:if test="barcode" >
                        <Param>
                            <Type>num</Type>
                            <Name>EAN</Name>
                            <Before>EAN : </Before>
                            <Value><xsl:value-of select="barcode" /></Value>
                        </Param>
                    </xsl:if>
                    <xsl:if test="manufacturer">
                        <Param>
                            <Type>string</Type>
                            <Name>Gyártó</Name>
                            <Value><xsl:value-of select="manufacturer" /></Value>
                        </Param>
                    </xsl:if>
                </Params>
            </xsl:if> <!-- action MODIFY  -->
            <Unit><xsl:value-of select="quantityunit" /></Unit>
            <xsl:if test="weight > 0"><Weight><xsl:value-of select="weight" /></Weight></xsl:if>
        </Product>
    </xsl:if> <!-- Webdisplay is 1? = not(SkipThisItem) -->
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
