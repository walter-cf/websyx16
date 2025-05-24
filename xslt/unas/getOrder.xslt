<!-- 
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*" />
    <xsl:output method="text" indent="no" />
    <xsl:template match="/Orders">
        <xsl:variable name="FeedbackUrl"><xsl:value-of select="unasFeedbackURL" /></xsl:variable>
        <customerorders>
        <xsl:for-each select="Order">
        <xsl:if test="not(SkipThisOrderItem)" >
            <customerorder>
                <date><xsl:value-of select="Date" /></date>
                <!-- <expirationdays>10</expirationdays>< ! - - Lejárat napok száma (üresen is hagyható) -->
                <orderid><xsl:value-of select="prefixOrderId" /><xsl:value-of select="Key" /></orderid>
                <currency><xsl:value-of select="Currency"/></currency><!-- Pénznem (Currency.Name) -->
                <!-- <currencyrate>1</currencyrate> -->
                <vouchersequencecode><xsl:value-of select="symbolVouchersequenceCode" /></vouchersequencecode>
                <xsl:for-each select="Customer">
                    <!-- nem hasznalhatom, mert atirtam a 'WEB<unasId>' kodot, szal muszaj nekem tudnom  a perfect kodot
                      <customer><xsl:value-of select="Id"/></customer><! - - Web-es vevőid, ami a vevő a weben jött létre és már lejött korábban - - >
                      <customercode>WEB00000234</customercode>< ! - - Symbol vevő CODE ha van (Customer.Code) - - >
                      <! - - <customerid>234</customerid>< ! - - Symbol vevő ID ha a vevő a symbolból került feltöltésre (CustomerOrder.Customer) - - >
                    -->
                    <customercode><xsl:value-of select="CustSymbolCode"/></customercode><!-- Symbol vevő CODE ha van (Customer.Code) -->
                    <customeremail><xsl:value-of select="Email"/></customeremail><!-- Vevő email címe (Customer.Email)  Beállítás alapján vevő azonosításra használható.-->
                    <xsl:for-each select="Addresses">
                        <xsl:for-each select="Invoice">
                            <country><xsl:value-of select="Country"/></country><!-- Számlázási ország (Customer.InvoiceCountry) -->
                            <xsl:if test="County != ''"><region><xsl:value-of select="County"/></region></xsl:if><!-- Számlázási megye (Customer.InvoiceRegion) -->
                            <zip><xsl:value-of select="ZIP"/></zip><!-- Számlázási irányítószám (Customer.InvoiceZip) -->
                            <city><xsl:value-of select="City"/></city><!-- Számlázási város (Customer.InvoiceCity) -->
                            <street><xsl:value-of select="Street"/></street><!-- Számlázási utca (Customer.InvoiceStreet) -->
                            <!-- 
                                <street><xsl:value-of select="StreetName"/></street>< ! - - Számlázási utca (Customer.InvoiceStreet) - - >
                                <housenumber><xsl:value-of select="StreetNumber"/></housenumber>< ! - - Számlázási házszám (Customer.InvoiceHouseNumber) - - >
                            -->
                        </xsl:for-each>
                        <xsl:for-each select="Shipping">
                            <!-- <transportid>43575</transportid> --> <!-- Telephely Symbol belső azonosító (CustomerAddress.Id) -->
                            <!-- <transportcontactname>NEM TUDOM!!!</transportcontactname> --> <!-- Telephely kapcsolattartó (CustomerAddress.ContactName) -->
                            <transportname><xsl:value-of select="Name"/></transportname><!-- Telephely megnevezése (CustomerAddress.Name) -->
                            <transportcountry><xsl:value-of select="Country"/></transportcountry><!-- Telephely ország (CustomerAddress.Country) -->
                            <xsl:if test="County != ''"><transportregion><xsl:value-of select="County"/></transportregion></xsl:if> <!-- Telephely megye (CustomerAddress.Region) -->
                            <transportzip><xsl:value-of select="ZIP"/></transportzip><!-- Telephely irányítószám (CustomerAddress.Zip) -->
                            <transportcity><xsl:value-of select="City"/></transportcity><!-- Telephely város (CustomerAddress.City) -->
			    <transportstreet><xsl:value-of select="Street"/></transportstreet><!-- Telephely utca (CustomerAddress.Street) -->
			    <transportcontactname><xsl:value-of select="Name"/></transportcontactname><!-- Telephely kapcsolattartó (CustomerAddress.ContactName) -->
                            <!-- 
                            <transportstreet><xsl:value-of select="StreetName"/></transportstreet>< ! - - Telephely utca (CustomerAddress.Street) - - >
                            <transporthousenumber><xsl:value-of select="StreetNumber"/></transporthousenumber><! - - Telephely házszám (CustomerAddress.HouseNumber) - - >
                            -->
                        </xsl:for-each>
                    </xsl:for-each>
            
                </xsl:for-each>
                <transportmode><xsl:value-of select="Shipping/Name"/></transportmode><!-- szállítási mód (TransportMode.Name) -->
                <paymentmethod><xsl:value-of select="paymentMethodName"/></paymentmethod><!-- fizetési mód (PaymentMethod.Name) -->
                <paymentmethodtolerance><xsl:value-of select="paymentMethodTolerance"/></paymentmethodtolerance><!-- fizetési mód (PaymentMethod.ToleranceDay) -->
                <comment><xsl:value-of select="Comments/Comment/Text"/></comment><!-- Rendelés megjegyzése (CustomerOrder.Comment) -->
                <!--
                    <transporttargetid>589830</transporttargetid><! - - Postapont száma
                    <transportdate>2010-07-20</transportdate><! - - szállítási dátum (CustomerOrder.DeliveryDate) - - >
                    <paymentmethodtolerance>8</paymentmethodtolerance><! - - átutalás esetén a napon száma (PaymentMethod.ToleranceDay) - - >
                    <warehouse>Központi</warehouse>< ! - - raktár (CustomerOrder.Warehouse) - - >
                    <notifyphone>1</notifyphone>< ! - - telefonos értesítés (1=igaz, 0=hamis) - - > (CustomerOrder.NotifyPhone) - - >
                    <notifysms>0</notifysms>< ! - - sms értesítés (1=igaz, 0=hamis) - - > (CustomerOrder.NotifySms) - - > 
                    <notifyemail>1</notifyemail>< ! - - email értesítés (1=igaz, 0=hamis) - - > (CustomerOrder.NotifyEmail) - - >
                    <splitforbid>1</splitforbid>< ! - - egyben kiszolgálandó (1=igaz, 0=hamis) - - > (CustomerOrder.SplitForbid) - - >
                    <banktrid>ABC123</banktrid>< ! - - banki tranzakciós azonosító (CustomerOrder.BankTRID) - - >
                    <closedmanually>0</closedmanually><! - -  Rendelés kézzel lezárt (1=igaz, 0=hamis) - - > (CustomerOrder.ClosedManually) - - >
                -->
                <!--
                    <productid>1</productid><! - - ID (Product.Id) - - >
                    <productcode>B123</productcode>< ! - - Termékkód (Product.Code) - - >
                    <productname>Termék II.</productname><! - - termlk neve, ha más jelenjen meg a számlán (Product.Name) - - >
                    <quantity>4</quantity><! - - Mennyiség (CustomerOrderDetail.Quantity) - - >
                    <vat>27</vat><! - - Áfa százalék
                    <vatname>KBAET</vatname><! - - Áfa kulcs megnevezése, az iseuvat mező kivezetésre került
                    <unipricenet>60.00000</unipricenet><! - -  (CustomerOrderDetail.VirtualUnitPrice) - - >
                    <uniprice>1900.00000</uniprice><! - -  (CustomerOrderDetail.VirtualUnitPrice) - - >
                    <netvalue>710</netvalue><! - - Web-en látott nettó összár, amitől nem tudunk eltérni (CustomerOrderDetail.NetValue) - - >
                    <grossvalue>75700</grossvalue><! - - web-en látott összár, amitől nem tudunk eltérni (CustomerOrderDetail.GrossValue) - - >
                    <discountpercent>10</discountpercent><! - - kedvezmény %-os értéke (CustomerOrderDetail.DiscountPercent) - - >
                    <mustmanufacturing>0</mustmanufacturing><! - - kiszolgálás gyártással (1=igaz, 0=hamis) - - > (CustomerOrderDetail.MustManufacturing) - - >
                    <allocate>1</allocate><! - - készlet foglalás (1=igaz, 0=hamis) - - > (CustomerOrderDetail.AllocateWarehouse) - - >
                    <detailstatus>Beérkezés alatt</detailstatus>< ! - - tétel állapot (CustomerOrderDetailStatus.Name) - - >
                    <comment>Tétel megjegyzése</comment><! - - Megjegyzés (CustomerOrderDetail.Comment) - - >
                -->
                <xsl:for-each select="Items/Item">
                <xsl:if test="not(Sku='shipping-cost')">
                    <detail>
                        <productcode><xsl:value-of select="Sku"/></productcode>
                        <quantity><xsl:value-of select="Quantity"/></quantity>
                        <unipricenet><xsl:value-of select="PriceNet" /></unipricenet>
                        <grossvalue><xsl:value-of select="computedPriceGross" /></grossvalue>

                        <!-- 
                        <vat><xsl:value-of select="substring-before(Vat, '%')" /></vat>
                        <productname><xsl:value-of select="Name"/></productname>
                        <uniprice><xsl:value-of select="PriceGross" /></uniprice>

                        <netvalue><xsl:value-of select="PriceNet" /></netvalue>
                        -->

                    </detail>
                </xsl:if>
                </xsl:for-each>
                <feedbackurl><xsl:value-of select="$FeedbackUrl"/>/oke/order?id=<xsl:value-of select="Id" /><xsl:text>&amp;</xsl:text>orderkey=<xsl:value-of select="Key" /><xsl:text>&amp;</xsl:text>ipaddr=<xsl:value-of select="Others/Ip" />&amp;symbolid=</feedbackurl>
                <errorurl><xsl:value-of select="$FeedbackUrl"/>/err/order?id=<xsl:value-of select="Id" /><xsl:text>&amp;</xsl:text>orderkey=<xsl:value-of select="Key" />&amp;errormsg=</errorurl>
            </customerorder>
        </xsl:if>
        </xsl:for-each>
        </customerorders>
    </xsl:template>
</xsl:stylesheet>
