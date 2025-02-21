<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="xml" indent="no" />
    <xsl:template match="CustomersUp">
        <xsl:for-each select="Customer">

        <xsl:variable name="TaxNumber" select="taxnumber"/>
        <xsl:variable name="EUTaxNumber" select="eutaxnumber"/>
        <xsl:variable name="CustomerName" select="name"/>
		<xsl:if test="not(SkipThisItem)">
        <Customer>
            <Action><xsl:value-of select="unasCustomerAction"/> </Action>
			<xsl:if test="unasCustomerId">
				<Id><xsl:value-of select="unasCustomerId" /></Id>
			</xsl:if>
            <Email><xsl:value-of select="email" /></Email>
			<Name><xsl:value-of select="$CustomerName" /></Name>
			<!-- Comment><xsl:value-of select="description" /></Comment -->
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
			<xsl:if test="contactname and contactname != ''">
			<Contact>
				<Name><xsl:value-of select="contactname" /></Name>
				<Phone>
					<xsl:choose>
					<xsl:when test="phone and phone != ''"><xsl:value-of select="phone" /></xsl:when>
					<xsl:otherwise>+3600000000</xsl:otherwise>
					</xsl:choose>
				</Phone>
				<Mobile>
					<xsl:choose>
					<xsl:when test="sms and sms != ''"><xsl:value-of select="sms" /></xsl:when>
					<xsl:otherwise>+3600000000</xsl:otherwise>
					</xsl:choose>
				</Mobile>
				<Lang>hu</Lang>
			</Contact>
			</xsl:if>
			<Addresses>
				<Invoice>
					<Name><xsl:value-of select="$CustomerName" /></Name> 
					<ZIP><xsl:value-of select="invoicezip" /></ZIP>
					<City><xsl:value-of select="invoicecity" /></City>
					<StreetName><xsl:value-of select="invoicestreet" /></StreetName>
					<StreetNumber><xsl:value-of select="invoicehousenumber" /></StreetNumber>
					<!-- 
					<Street><xsl:value-of select="invoicestreet" /> <xsl:value-of select="invoicehousenumber" /></Street>
					<xsl:if test="unasStreetName"><StreetName><xsl:value-of select="unasStreetName" /></StreetName> </xsl:if>
					<xsl:if test="unasStreetType"><StreetType><xsl:value-of select="unasStreetType" /></StreetType></xsl:if>
					-->
					<County><xsl:value-of select="invoiceregion" /></County>
					<Country><xsl:value-of select="invoicecountry" /></Country>
					<CountryCode>
						<xsl:choose>
						<xsl:when test="unasCountryCode" ><xsl:value-of select="unasCountryCode" /></xsl:when>
						<xsl:otherwise>hu</xsl:otherwise>
						</xsl:choose>
					</CountryCode>					
					<TaxNumber><xsl:value-of select="$TaxNumber" /></TaxNumber>
					<EUTaxNumber><xsl:value-of select="$EUTaxNumber" /></EUTaxNumber>
					<xsl:choose>
						<xsl:when test="iscompany = 1" ><CustomerType>company</CustomerType></xsl:when>
						<xsl:when test="iscompany = 9999" ><CustomerType>other_customer_without_tax_number</CustomerType></xsl:when>
						<xsl:otherwise><CustomerType>private</CustomerType></xsl:otherwise>
					</xsl:choose>
				</Invoice>
				<xsl:if test="not(HasMoreAddress)">
					<Shipping>
						<Comment>no-HasMoreAddress</Comment>
						<Name><xsl:value-of select="$CustomerName" /></Name> 
						<ZIP><xsl:value-of select="invoicezip" /></ZIP>
						<City><xsl:value-of select="invoicecity" /></City>
						<StreetName><xsl:value-of select="invoicestreet" /></StreetName>
						<StreetNumber><xsl:value-of select="invoicehousenumber" /></StreetNumber>
						<!-- 
						<Street><xsl:value-of select="invoicestreet" /> <xsl:value-of select="invoicehousenumber" /></Street>
						<xsl:if test="unasStreetName"><StreetName><xsl:value-of select="unasStreetName" /></StreetName> </xsl:if>
						<xsl:if test="unasStreetType"><StreetType><xsl:value-of select="unasStreetType" /></StreetType></xsl:if>
						-->
						<County><xsl:value-of select="invoiceregion" /></County>
						<Country><xsl:value-of select="invoicecountry" /></Country>
						<CountryCode>
							<xsl:choose>
							<xsl:when test="unasCountryCode" ><xsl:value-of select="unasCountryCode" /></xsl:when>
							<xsl:otherwise>hu</xsl:otherwise>
							</xsl:choose>
						</CountryCode>
					</Shipping>
				</xsl:if>
			    <xsl:for-each select="customeraddresses/customeraddress">
					<xsl:choose>
					<xsl:when test="LooperFirst=0 and deleted=0">
						<Shipping>
							<Comment>LooperFirst=0 and deleted=0</Comment>
						
							<Name><xsl:value-of select="name" /></Name> 
							<ZIP><xsl:value-of select="zip" /></ZIP>
							<City><xsl:value-of select="city" /></City>

							<StreetName><xsl:value-of select="street" /></StreetName>
							<StreetNumber><xsl:value-of select="housenumber" /></StreetNumber>
							<!-- 
							<Street><xsl:value-of select="street" /> <xsl:value-of select="housenumber" /></Street>
							<xsl:if test="unasStreetName"><StreetName><xsl:value-of select="unasStreetName" /></StreetName> </xsl:if>
							<xsl:if test="unasStreetType"><StreetType><xsl:value-of select="unasStreetType" /></StreetType></xsl:if>
							-->

							<County><xsl:value-of select="region" /></County>
							<Country><xsl:value-of select="country" /></Country>
							<CountryCode>
								<xsl:choose>
								<xsl:when test="unasCountryCode" ><xsl:value-of select="unasCountryCode" /></xsl:when>
								<xsl:otherwise>hu</xsl:otherwise>
								</xsl:choose>
							</CountryCode>
							<TaxNumber><xsl:value-of select="companytaxnumber" /></TaxNumber>
							<xsl:choose>
								<xsl:when test="iscompany = 1" ><CustomerType>company</CustomerType></xsl:when>
								<xsl:otherwise><CustomerType>private</CustomerType></xsl:otherwise>
							</xsl:choose>
						</Shipping>
					</xsl:when>
					<xsl:when test="deleted = 1"></xsl:when>
					<xsl:otherwise>
						<Other>
							<Comment>LooperFirst=<xsl:value-of select="LooperFirst" /></Comment>
							
							<Name><xsl:value-of select="name" /></Name> 
							<ZIP><xsl:value-of select="zip" /></ZIP>
							<City><xsl:value-of select="city" /></City>

							<Street><xsl:value-of select="street" /><xsl:if test="housenumber"> <xsl:value-of select="housenumber" /></xsl:if></Street>
							<!-- 
							<xsl:if test="unasStreetName"><StreetName><xsl:value-of select="unasStreetName" /></StreetName> </xsl:if>
							<xsl:if test="unasStreetType"><StreetType><xsl:value-of select="unasStreetType" /></StreetType></xsl:if>
							-->

							<County><xsl:value-of select="region" /></County>
							<Country><xsl:value-of select="country" /></Country>
							<CountryCode>
								<xsl:choose>
								<xsl:when test="unasCountryCode" ><xsl:value-of select="unasCountryCode" /></xsl:when>
								<xsl:otherwise>hu</xsl:otherwise>
								</xsl:choose>
							</CountryCode>
							<TaxNumber><xsl:value-of select="companytaxnumber" /></TaxNumber>
							<xsl:choose>
								<xsl:when test="iscompany > 0" ><CustomerType>private</CustomerType></xsl:when>
								<xsl:otherwise><CustomerType>company</CustomerType></xsl:otherwise>
							</xsl:choose>
						</Other>            
					</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
			</Addresses>
        </Customer>
		</xsl:if>

        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>