<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <Product>
            <Action>modify</Action>
            <Sku><xsl:value-of select="ProductCode" /></Sku>
            <xsl:if test="retValValid > 1">
                <Stocks>
                    <Status>
                        <Active>1</Active>
                        <Empty>0</Empty>
                        <Variant>0</Variant> <!-- ???? Mi a Variant-->
                    </Status>
                    <Stock>
                        <Qty><xsl:value-of select="CurrentQuantity"/></Qty>
                        <Comment>StrictQuantity:<xsl:value-of select="StrictAllocate"/></Comment>
                    </Stock>
                </Stocks>
            </xsl:if>
        </Product>
    </xsl:for-each>
</xsl:stylesheet>
