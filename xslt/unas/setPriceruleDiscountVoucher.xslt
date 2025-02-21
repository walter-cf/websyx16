<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:variable name="XmlAction">$$$xmlAction$$$</xsl:variable>
    <xsl:template match="DiscountRules">
    <xsl:for-each select="CustomerVoucherDiscounts">
    </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
