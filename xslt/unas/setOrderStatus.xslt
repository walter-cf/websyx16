<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            xmlns:date="http://exslt.org/dates-and-times" extension-element-prefixes="date"
    >
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="/">

        <xsl:for-each select="/CustomerOrderStatuses/CustomerOrder">
            <xsl:if test="not(SkipThisItem)">
            <Order> 
	            <Action>modify</Action>
                <Key><xsl:value-of select="substring-after(substring-after(PrimeVoucherNumber, '-'), '-')" /></Key>

                <Status><xsl:value-of  select="customerOrderStatus"/></Status>

                <StatusDetails>
                        Voucher:<xsl:value-of  select="VoucherNumber"/>
                        ststusz(kod):<xsl:value-of  select="CustomerOrderStatus"/>
                        Statusz(nev):<xsl:value-of  select="CustomerOrderStatusName"/>
                        symbolId:<xsl:value-of  select="Id"/>
                </StatusDetails>

                <!-- StatusDateMod><xsl:value-of  select="current-dateTime()"/></StatusDateMod -->
                <StatusDateMod><xsl:value-of select="date:date-time()"/></StatusDateMod>
                 
                <StatusEmail><xsl:value-of  select="sendOrderStatusEmail"/></StatusEmail>
        	</Order>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
 </xsl:stylesheet>