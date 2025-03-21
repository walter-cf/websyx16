<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="/">
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
                    <!--  Jelen pillanatban NotUsed!
                    <xsl:if test="customstariffnumber">
                        <Param>
                            <Type>string</Type>
                            <Name>VTSZ</Name>
                            <Value><xsl:value-of select="customstariffnumber" /></Value>
                        </Param>
                    </xsl:if>
                    -->
                    <xsl:if test="unasExtendedAttributes = 1">
                        <xsl:if test="productcategory">
                            <Param>
                                <Type>string</Type>
                                <Name>TargetCategory</Name>
                                <Value><xsl:value-of select="productcategory" /></Value>
                            </Param>
                        </xsl:if>
                        <xsl:if test="Attributes">
                            <Param>
                                <Type>string</Type>
                                <Name>Attributes</Name>
                                <Value><xsl:value-of select="Attributes" /></Value>
                            </Param>
                        </xsl:if>
                        <xsl:if test="guaranteemonths">
                            <Param>
                                <Type>string</Type>
                                <Name>GuaranteeMonths</Name> 
                                <Value><xsl:value-of select="guaranteemonths" /></Value>
                            </Param>
                        </xsl:if>
                    </xsl:if>             <!--  unasExtendedAttributes -->
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

            </xsl:if>  <!-- action ADD -->
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
                    <!--  Jelen pillanatban NotUsed!
                    <xsl:if test="customstariffnumber">
                        <Param>
                            <Type>num</Type>
                            <Name>VTSZ</Name>
                            <Value><xsl:value-of select="customstariffnumber" /></Value>
                        </Param>
                    </xsl:if>
                     -->
                </Params>
            </xsl:if> <!-- action MODIFY  -->
            <!--  Felteteles ADD ended -->
            <Unit><xsl:value-of select="quantityunit" /></Unit>
            <xsl:if test="weight > 0"><Weight><xsl:value-of select="weight" /></Weight></xsl:if>
            <Description>
                <Short><xsl:value-of select="webname" /></Short>
                <Long><xsl:value-of select="webdescription" /></Long>
            </Description>
            <!-- -->
            <xsl:if test="pictureX">
                <Images><Image>
                    <Type>base</Type>
                    <Import>
                    <Encoded><xsl:value-of select="picture" /></Encoded>
                    </Import>
                </Image></Images>
            </xsl:if>
            <xsl:if test="not(webmetadescription ='')">
                <Meta><Keywords>LedSound Haffner24</Keywords><Description><xsl:value-of select="webmetadescription" /></Description></Meta>
            </xsl:if>
        </Product>
    </xsl:if> <!-- Webdisplay is 1? = not(SkipThisItem) -->
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
