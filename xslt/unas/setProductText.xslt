<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="/">
    <xsl:for-each select="Products/Product">
        <xsl:for-each select="lLang">
            <xsl:if test="not(SkipThisItem)">
                <Product>
                    <Action>modify</Action>
                    <Sku><xsl:value-of select="Sku" /></Sku>
                    <Lang><xsl:value-of select="Lang" /></Lang>
                    <Name><xsl:value-of select="Name" /></Name>
                    <!--  Felteteles ADD - - >
                    <xsl:if test="lDescription">
                    </xsl:if>
                    <xsl:if test="lMeta">
                    </xsl:if>
                    <! - - + Unit, AlterUnit, ManufacturerUrl, SefUrl, Images[names], Variants[names], Datas.Data, AdditionalDatas.AdditionalData, Params - - >
                    <xsl:if test="lData">
                    </xsl:if>
                    <xsl:if test="lAltData">
                    </xsl:if>
                    <xsl:if test="lParams">
                    </xsl:if>
                    -->
                </Product>
            </xsl:if> <!-- Webdisplay is 1? = not(SkipThisItem) -->
        </xsl:for-each> <!-- s e l e c t= "lLang" -->
    </xsl:for-each> <!-- s e l e c t= "Products/Product" -->
    </xsl:template>
</xsl:stylesheet>
