<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="Customers">
        <xsl:for-each select="Customer">

        <Customer>
            <Action>modify</Action>
			<xsl:if test="unasId">
				<Id><xsl:value-of select="unasId" /></Id>
			</xsl:if>
            <Email><xsl:value-of select="email" /></Email>
			<Params>
                <Param>
		            <!-- Id -->
                    <Name>symbolId</Name>
                    <Value><xsl:value-of select="id" /></Value>
                </Param>
                <Param>
		            <!-- Id -->
                    <Name>symbolCode</Name>
                    <Value><xsl:value-of select="code" /></Value>
                </Param>
            </Params>
        </Customer>

        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>