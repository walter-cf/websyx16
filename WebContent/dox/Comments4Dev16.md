```
update "Product" set "Name" = trim("Name") || ' (joe)' where "Id" in (3404,2812,4079,3257,226,4105,168,4009,1414,3446,3917,1635,3478,3205,3302,1828,2187,731,2923,2331,3247,3676,628,35);

update "Product" set "Name" = replace("Name", ' (joe)','') where "Name like '% (joe)' and "Id" not in (3727, 3676, 3567, 3504, 3482, 3478, 3446, 3205, 3151, 2812, 2605, 2492, 2432, 2384, 2187, 1999, 1849, 1836, 1828, 1813, 1773, 1635, 1571, 1523, 1267, 1226, 1163, 924, 731, 628, 575, 489, 425, 168, 35)

select "Id", trim("Name") from "Product" where "Name" like '%joe%' ;

select "Id", char_length("Name") from "Product" where "Id" in (3404,2812,4079,3257,226,4105,168,4009,1414,2753,3446,3917,2256,1635,3478,3205,3302,1828,2187,731,2923,2331,3247,1043,3676,628,35) order by 2;
```

**A cel, h barmelyik vevonek/CG-nek lehessen barmilyen kedvezmenyt adni**

> feltetelezem: PG = CG | EGYEDI  (PriceGroup / CostumerGroup)  
    van CG EGYEDI? Es az mit jelentsen?

--------------

**Harom fuggetlen folyamat:**  
  - F1. Customer CG/PG set => setCustomer  
  - F2. Product specialprice (Rx) => setProduct (specialPrice [Rx] )  
  - F3. Vevoi Akcio => Offer => setProduct (specialPrice [uniqueName] )  

_________________________________

  > **Q?**
Ha EGYEB-bol megy vissza Rx-be, akkor, mi van - most nem csinalok semmit  
**A** Es ez igy jo is lesz, ha az UNASban is atmegy a setCustomer miatt CG-be
  > **Q?**
CustomerCat es PriceCat is van es raadasul kulonbozik, akkor a CustomerCat nyer MOST  
PEDIG Csak a PriceCat kellene, hogy szamitson, nicht war?

  > Vasarlo csoportot NEM lehet az UNASban modositani (nem 1-1 a symbol-Unas osszerendeles)  
  > Vevoi Akciokat nem tudom OK-zni  
  > Unas termek specialPrice nem torolheto  

## CustomersUp

### CustomerGroup/PriceCategory variants

1.  CG: Normal / PG Normal
	   Nothing to do
2. CG: Normal / PG Rx
	   Nothing to do? or UnasCG set symbPriceCat? ??? Nem egyertelmu!!! 
3. CG: Rx / Rx PG automatikusan Rx
	   UnasCG set symbCG
    CG: Rx / PG valami mas NEM Rx ez NEM EGYEDI
	   Unas CG => Rx
4. CG: Normal / PG EGYEDI
	   UnasCG set EGYEDI-UCO-<CustomerUnasId> ??
	   ??? de ez nem jo semmire, szal nem ertek valamit, biztosan
5. CG: Rx / PG EGYEDI
	   UnasCG set EGYEDI-UCO-<CustomerUnasId>
	   for Products in Rx (Form Firebird DB OR ProductCache) amiben most nincsenek benne az arak!!! 
	       make ProductSpecailPrice with CG=EGYEDI-UCO-<CustomerUnasId>, Prod=Prod, Price:ProdPrice-Rx
6. CG: Rx / Ry
	   Nothing to do  ??? Elvileg ez is Spec arak az Ry-ra EGYEDI-UCO-xxx tehat same as Rx+Ry+Egyedi-UCO-xxx
	                  MOST CG = EGYEDI es Csinalok Rx-re es Ry-ra egyedi arakat a termeknek DE EZ HULYESEG!!!???
		  ha CG - PG , akkor a CG elintezi, tehat noting to do, de ha kulonbozik??? Akkor:
		      PG -> EGYEDI PP
			  CG -< EGYEDI PP
		> !!! NEM TESZTELT !!!
		>>!!!! Azert eztnem igazan talaltam ki jol!! es nincs is teljesen tesztelve!!!!
7. None/None Missing data - AMI NEM LEHET
**Test cases**
	- TC-1 normal/Normal  = None
	- TC-2 N  / R8 Direkt nem letezik az UNASban a csoport => L:trehozza es beallitja ra
	- TC-3 Rx / Rx  =\> Rx
	- TC-4 N  / E   =\> None
	- TC-5 Rx / E   =\> Egyedi-UCO-xxx
                  	\+ customer_offer_details alapon hozza letre a special Rx PriceOffereket Rx-re 
					de mi van, ha mar letezik az ajanlat, csak mondjuk mas datummal?
					Egyaltalan mi kulonbozteti meg az egyik ajanlatot a masiktol?
					symb-CustOffer: symbolId de a special-ProdPricenak nincs azonositoja
	- TC-6 Missing all


> Csak "felfele" tud valtozni? Normal-R 1..5 , EGYEDI sorrendben?  
Vagy AZ AMI BE VAN ALLITVA es kesz?
					

## ProductPrice:
>ha van R1,R2..R9 pricecategoryName-mel ar adat, akkor azt SPECIAL arkent felviszem. A ProductPrice.validFrom lesz az UNAS.StartDate az EndDate pedig legyen mondjuk 2038.01.19
PG == EGYEDI Exception, nincs lekezelve, mert - szerintem  - ilyen nincs is  
Warning BaseCategory most 18 - nem elegge dinamikus - azt hiszem (Ez nekem szolo megj.)
Nem tudok mar felvitt ProductPrice-t torolni!
	  
  **Test cases = Prod: BS285509**
	
1. PP-1 normal
2. PP-2 Rx ::  Ha nincs normal ar, az baj! Bar, ha egyszer a tetel felkerult, akkor biztosan van,
               	torolni meg egyebkent sem tudom, szal: les(z)arhato
3. PP-3 Rx, Ry, Rz
4. PP-4 normal, Rx, Ry, Rz

* **Q**
*ha mar felvittem, nem tudom, hogyan lehet torolni egy ar tetelt, ha esetleg megsem akarom. OK, levehetem az EndDate-t mara vagy tegnapra, de akkor tudnom kell, milyen arteteli vannak a termeknek az Unasban. Le kell kerdeznem vagy CACHE-ben tarthatom(en erre szavazok, ha mar ugyis van CACHE ebben a verzioban


## CustomerOffer:

	* **Sztem ez adja magat es keszen volt ket hete is**
**Test cases**  
1. CO-1 Normal
2. CO-2 R4
3. CO-3 EGYEDI # Ettol kezdve a Customer EGYEDI-UCO-xxx csoportba KELL tartozzon, legalabbis az offer vegeig!?


* **Q** Altalaban az uj setCustomer felulirja a regit - Jo ez igy? biztosan nem. CACHE vezerelt legyen?

## DiscountRules/ProductCategoryDiscount
## DiscountRules/CustomerCategoryDiscount
  > Logikailag - nekem - ugyanaz mindketto:
	lekerem a hivatkozott Cust es Prod recordokat es mindbol kell Cust/Prod special prodPrice-t csinalni
  > Gondolom Egyedi CustomerOfferkent fel lehet vinni,
      csak vigyaznom kell, hogy a customer nem a symbolban tartott CG-be tartozik, szal CACHE???

**Test cases**  
1. DRPC-1 
2. DRCC-1 
3. DRPC-2
4. DRCC-2 

-----------------------------------------------------
```
logging 
python forms??
threading

unasConnector =- login es sendRequest
unasComm =- requestors

mySql
fbSql
```
```
symbolComm
--------------------------------
PT-6445
BS285509
HF342714
ST111165
ST310454
ST126084
ST129412
ST364747
================================
demo 2 CG:R1   Price R2
demo3 NO csoport
demo4 R2
demo5 R1
demo6 EGYEDI + R1
demo7 R1 + OFFER - Proba-11(PT-6445)
```
```
CREATE TABLE `costumer_offers` (
  `id` bigint NOT NULL ,
   `voucher_number` varchar(255) COLLATE utf8mb4_hungarian_ci NOT NULL,
   `name` varchar(255) COLLATE utf8mb4_hungarian_ci NOT NULL,
   `valid_from` date,
   `valid_to` date,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci

CREATE TABLE `consumer_offer_details` (
  `id` bigint NOT NULL ,
  `customer` bigint NOT NULL ,
  `forbid` boolean default 0,
  `offer_id` bigint NOT NULL ,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (offer_id) REFERENCES costumer_offers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci

CREATE TABLE `consumer_offer_costumers` (
  `id` bigint NOT NULL ,
  `product` bigint NOT NULL ,
   `currency_name` varchar(255) ,
   `price_category_name` varchar(255),
   `base_price` DOUBLE ,
   `base_price_date` date,
   `sales_percent` DOUBLE,
   `sales_price` DOUBLE,
   offer_id bigint,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (offer_id) REFERENCES costumer_offers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci

================

update "Product" set "Name" = trim("Name") || ' (unas)' where character_length("Name") < 91 and "Id" in (2605,1646,489,3661,3504,1849,1813,387,425,2303,3727,3933,3151,4095,1836,2944,137,251,1521,3482,3116,1163,1267,2384,1999,3567,4147,575,1773,2492,3047,2483,1226,3519,2334,3409,2432,924,4132,159,3372,3408,3924,1571)


(*
Source - https://stackoverflow.com/a/12070498
Posted by Andrej Kirejeu, modified by community. See post 'Timeline' for change history
Retrieved 2026-07-09, License - CC BY-SA 3.0*)

SELECT
  TRIM(rf.rdb$field_name) name,  IIF(rdb$field_source LIKE 'RDB$%',
  DECODE(f.rdb$field_type, 
    8,  'INTEGER', 
    12, 'DATE', 
    37, 'VARCHAR', 
    14, 'CHAR', 
    7,  'SMALLINT'),
  TRIM(rdb$field_source)) nemtommi,
  IIF((rdb$field_source LIKE 'RDB$%') AND (f.rdb$field_type IN (37, 14)),
    '(' || f.rdb$field_length || ')',
    '') ftommi,
  IIF((f.rdb$null_flag = 1) OR (rf.rdb$null_flag = 1), 
    ' NOT NULL', '') xxxx
FROM
  rdb$relation_fields rf JOIN rdb$fields f
    ON f.rdb$field_name = rf.rdb$field_source
WHERE
  rf.rdb$relation_name = 'Product'

(*
Source - https://stackoverflow.com/a/12074601
Posted by Ondrej Kelle
Retrieved 2026-07-09, License - CC BY-SA 3.0
*)

SELECT
  RF.RDB$FIELD_NAME FIELD_NAME,
  CASE F.RDB$FIELD_TYPE
    WHEN 7 THEN
      CASE F.RDB$FIELD_SUB_TYPE
        WHEN 0 THEN 'SMALLINT'
        WHEN 1 THEN 'NUMERIC(' || F.RDB$FIELD_PRECISION || ', ' || (-F.RDB$FIELD_SCALE) || ')'
        WHEN 2 THEN 'DECIMAL'
      END
    WHEN 8 THEN
      CASE F.RDB$FIELD_SUB_TYPE
        WHEN 0 THEN 'INTEGER'
        WHEN 1 THEN 'NUMERIC('  || F.RDB$FIELD_PRECISION || ', ' || (-F.RDB$FIELD_SCALE) || ')'
        WHEN 2 THEN 'DECIMAL'
      END
    WHEN 9 THEN 'QUAD'
    WHEN 10 THEN 'FLOAT'
    WHEN 12 THEN 'DATE'
    WHEN 13 THEN 'TIME'
    WHEN 14 THEN 'CHAR(' || (TRUNC(F.RDB$FIELD_LENGTH / CH.RDB$BYTES_PER_CHARACTER)) || ') '
    WHEN 16 THEN
      CASE F.RDB$FIELD_SUB_TYPE
        WHEN 0 THEN 'BIGINT'
        WHEN 1 THEN 'NUMERIC(' || F.RDB$FIELD_PRECISION || ', ' || (-F.RDB$FIELD_SCALE) || ')'
        WHEN 2 THEN 'DECIMAL'
      END
    WHEN 27 THEN 'DOUBLE'
    WHEN 35 THEN 'TIMESTAMP'
    WHEN 37 THEN 'VARCHAR(' || (TRUNC(F.RDB$FIELD_LENGTH / CH.RDB$BYTES_PER_CHARACTER)) || ')'
    WHEN 40 THEN 'CSTRING' || (TRUNC(F.RDB$FIELD_LENGTH / CH.RDB$BYTES_PER_CHARACTER)) || ')'
    WHEN 45 THEN 'BLOB_ID'
    WHEN 261 THEN 'BLOB SUB_TYPE ' || F.RDB$FIELD_SUB_TYPE
    ELSE 'RDB$FIELD_TYPE: ' || F.RDB$FIELD_TYPE || '?'
  END FIELD_TYPE,
  IIF(COALESCE(RF.RDB$NULL_FLAG, 0) = 0, NULL, 'NOT NULL') FIELD_NULL,
  CH.RDB$CHARACTER_SET_NAME FIELD_CHARSET,
  DCO.RDB$COLLATION_NAME FIELD_COLLATION,
  COALESCE(RF.RDB$DEFAULT_SOURCE, F.RDB$DEFAULT_SOURCE) FIELD_DEFAULT,
  F.RDB$VALIDATION_SOURCE FIELD_CHECK,
  RF.RDB$DESCRIPTION FIELD_DESCRIPTION
FROM RDB$RELATION_FIELDS RF
JOIN RDB$FIELDS F ON (F.RDB$FIELD_NAME = RF.RDB$FIELD_SOURCE)
LEFT OUTER JOIN RDB$CHARACTER_SETS CH ON (CH.RDB$CHARACTER_SET_ID = F.RDB$CHARACTER_SET_ID)
LEFT OUTER JOIN RDB$COLLATIONS DCO ON ((DCO.RDB$COLLATION_ID = F.RDB$COLLATION_ID) AND (DCO.RDB$CHARACTER_SET_ID = F.RDB$CHARACTER_SET_ID))
WHERE (RF.RDB$RELATION_NAME = 'Product') AND (COALESCE(RF.RDB$SYSTEM_FLAG, 0) = 0)
ORDER BY RF.RDB$FIELD_POSITION;
```