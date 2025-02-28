<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="Products">
        <xsl:variable name="FeedbackUrl"><xsl:value-of select="unasFeedbackURL" /></xsl:variable>
        <ProductsDown>
        <xsl:for-each select="Product">
            <Product>
                <!--
                    <sid>9999100<xsl:value-of select="Id" /></sid>
                    <NumExA><xsl:value-of select="Id" /></NumExA>
                    <UnasId><xsl:value-of select="Id" /></UnasId>
                -->
                <xsl:if test="symbolId"><xsl:if test="symbolId &gt; 0">
                    <id><xsl:value-of select="symbolId" /></id>
                </xsl:if></xsl:if>
                <name><xsl:value-of select="Name" /></name>
                <code><xsl:value-of select="Sku" /></code>

                <!--
                *** Kiirtva, Peti szerint nem kell @2024.03.01
                <webdisplay>1</webdisplay>
                <webname><xsl:value-of select="Description/Short" /></webname>
                <webdescription><xsl:text disable-output-escaping="yes">&lt;![CDATA[</xsl:text><xsl:value-of select="Description/Long" disable-output-escaping="yes"/><xsl:text  disable-output-escaping="yes">]]&gt;</xsl:text></webdescription>
                <webmetadescription><xsl:value-of select="Meta/Description" /></webmetadescription>
                <weburl><xsl:value-of select="Url" /></weburl>
                <webkeywords><xsl:value-of select="AutomaticMeta/Keywords" /></webkeywords>
                    
                -->
                <!-- Web SID-->
                <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/product?id=<xsl:value-of select="Id" /><xsl:text>&amp;</xsl:text>prodname=<xsl:value-of select="Name" /><xsl:text>&amp;</xsl:text>symbolid=</feedbackurl>
                <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/product?id=<xsl:value-of select="Id" /><xsl:text>&amp;</xsl:text>errormsg=</errorurl>
            </Product>
        </xsl:for-each>
        </ProductsDown>
    </xsl:template>
</xsl:stylesheet>
