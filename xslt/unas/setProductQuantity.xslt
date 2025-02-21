<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="/ProductQuantities">
    <xsl:for-each select="ProductQuantity">
        <xsl:variable name="SymbolIdIsNull" select="symbolIdIsNull"/>
        <xsl:if test="not(SkipThisItem)">
        <xsl:if test="retValValid > 0 or $SymbolIdIsNull > 0">
            <Product>
                <Action>modify</Action>
                <Sku><xsl:value-of select="ProductCode" /></Sku>
                <!--
                <ProductQuantities xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <ProductQuantity>
                        <Warehouse>-1</Warehouse>
                        <WarehouseName>LED Sound Kft. (Központi raktár)</WarehouseName>
                        <WarehouseSite>0</WarehouseSite>
                        <Product>1</Product>
                        <ProductCode>LSSPK20BK</ProductCode>
                        <Quantity>0</Quantity>
                        <StrictAllocate>0</StrictAllocate>
                    </ProductQuantity>
                </ProductQuantities>
                -->
                <!--
                        <Stocks>
                            <Status>
                                <Active>1</Active>
                                <Empty>1</Empty>
                                <Variant>1</Variant>
                            </Status>
                            <Stock>
                                <Variants>
                                    <Variant><![CDATA[Kék]]></Variant>
                                    <Variant><![CDATA[S]]></Variant>
                                </Variants>
                                <Qty>10</Qty>
                            </Stock>
                            <Stock>
                                <Variants>
                                    <Variant><![CDATA[Piros]]></Variant>
                                    <Variant><![CDATA[M]]></Variant>
                                </Variants>
                                <Qty>20</Qty>
                            </Stock>
                        </Stocks>
                -->
                <xsl:if test="retValValid > 1">
                    <Stocks>
                        <Status>
                            <Active>1</Active>
                            <Empty>1</Empty>
                            <Variant>0</Variant> <!-- ???? Mi a Variant-->
                        </Status>
                        <Stock>
                            <Qty><xsl:value-of select="CurrentQuantity"/></Qty>
                            <Comment>StrictQuantity:<xsl:value-of select="StrictAllocate"/></Comment>
                        </Stock>
                    </Stocks>
                </xsl:if>

                <xsl:if test="$SymbolIdIsNull > 0">
                    <Params>
                        <Param>
                            <Type>num</Type>
                            <Name>symbolId</Name>
                            <Value><xsl:value-of select="Product" /></Value>
                        </Param>
                    </Params>
                </xsl:if>
            </Product>
        </xsl:if>
        </xsl:if> <!-- Skip this item -->
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
