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
                    <id><xsl:value-of select="Id" /></id>
                -->
                <xsl:if test="symbolId"><xsl:if test="symbolId &gt; 0">
                    <sid><xsl:value-of select="symbolId" /></sid>
                    <code><xsl:value-of select="Sku" /></code>
                </xsl:if></xsl:if>

                <sid><xsl:value-of select="Id" /></sid>
                <name><xsl:value-of select="Name" /></name>

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
                <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/product/<xsl:value-of select="Id" />?symbolid=</feedbackurl>
                <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/product/<xsl:value-of select="Id" />?errormsg=</errorurl>
            </Product>
        </xsl:for-each>
        </ProductsDown>
    </xsl:template>
</xsl:stylesheet>
