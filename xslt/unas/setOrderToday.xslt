<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="/">
        <customerorders>
        <xsl:for-each select="Orders/Order">
	        <customerorder>
                <date><xsl:value-of select="Date" /></date>
                <orderid>UNAS-0-<xsl:value-of select="Id" /></orderid>


                <customer><xsl:value-of select="Customer/Addresses/Invoice/Name"/></customer>
                <customerid><xsl:value-of select="Customer/Username"/></customerid>
                <customercode>Nem-tudom</customercode>
                <customeremail><xsl:value-of select="Customer/Email"/></customeremail>

                <country><xsl:value-of select="Customer/Addresses/Invoice/Email"/></country>
                <region><xsl:value-of select="Customer/Addresses/Invoice/Email"/></region>
                <zip><xsl:value-of select="Customer/Addresses/Invoice/ZIP"/></zip>
                <city><xsl:value-of select="Customer/Addresses/Invoice/City"/></city>
                <street><xsl:value-of select="Customer/Addresses/Invoice/StreetName"/></street>
                <housenumber><xsl:value-of select="Customer/Addresses/Invoice/StreetNumber"/></housenumber>


                <xsl:for-each select="Items/Item">
                    <detail>
                        <productid><xsl:value-of select="Id"/></productid>
                        <productname><xsl:value-of select="Name"/></productname>
                        <quantity><xsl:value-of select="Quantity"/></quantity>
                        <vat><xsl:value-of select="Vat" /></vat>
                        <netvalue><xsl:value-of select="PriceNet" /></netvalue>
                        <grossvalue><xsl:value-of select="PriceGross" /></grossvalue>
                    </detail>
                </xsl:for-each>
	        </customerorder>
        </xsl:for-each>
        </customerorders>
    </xsl:template>
 </xsl:stylesheet>