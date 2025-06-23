## web6Proxy - valtozaslista joe @ 2025.05.31

### - 2025.06.23
Issue: 0002: getOrder - Duplicate customer 0 errorhandlling failed
```
Context:: client:192.168.10.4, action:getOrder -+- TS:1750546863011, tsTime:2025.06.22 01:01:03, tsType:ORDERS

Object of type IntElement is not JSON serializable

Exception:<class 'TypeError'> / Object of type IntElement is not JSON serializable
Traceback (most recent call last):
  File "/opt/websyx/GetProcessor.py", line 106, in transformGetRequestObject
    MU.putCustomerIntoCache(ucc)   # MU.UnasCustomerList[ucc.custAzon] = ucc
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "/opt/websyx/MyUtils.py", line 549, in putCustomerIntoCache
    raise MUT.MyProgramFlowErrorException( _m, MUT.ProxyErrCode.E40 )
MyUtilsTypes.MyProgramFlowErrorException: 40 -> [putCustomerIntoCache]:Duplicate item:{ "unasId":None, "symbolId":None, "lastmod":(1750545662)[2025.06.22 00:41:02], "code":"UCU-269184499",
+"email":"rendeles@lovemobile.hu", "taxNumber":"12676981-2-41", "state":"nonRegged" } :*-*: { "unasId":None, "symbolId":None, "lastmod":(1750545662)[2025.06.22 00:41:02], "code":"UCU-269192964",
+"email":"procurement@irodaszerellato.hu", "taxNumber":"12372137-2-41", "state":"nonRegged" }
```
MyUtilTypes:239 -> simans str -re konvertaltam !!! HACK !!! Kesobb megnezem

### - 2025.06.17
 - Issue-0001: setCustomer Failed!  TrId:1750148875047(first) - 1750151038047(last)
   getCustomerFrom Cache - bad code - changeId: 6bf46c9d2b1e6610b25ad3a4e40376aa9758c613

### - 2025.05.31
- log/xmlfiles rotate & archive /  add batch-func
- xmlfiles - ProductPrice.UNAS - save: missed (3dbd207710ae96827f1955d4a2764b3549dbd8a7)
- DOX:webSocks: add new api entry (d51df661e67778aab914e0f950a6a8eacd570e13)
- Remove unused Py files (27d3c02da933537a2d778b523324a233c3e8d78b)

### - 2025.04.10
- *Dokumentaciot keszitek, amig van hozza ize... (index README, CHANGELOG,TODO)

- *Issue : Rendeles teteladatok nem kerultek rogzitesre a symbolban*

### - 2025.04.09
- web6proxy.yaml config aktualizaltam.  
A config fajl tartalma le volt maradva a dev (-3311.yaml) filehoz kepest . Ez okozta, tobbek kozott a Batch szerviz elhalasat (hianyzott par config-key-value pair)

- *Issue : Email:25.04.09 11:04:49::FATAL - unhandled error (14)! TS:1744189487011*  
A hibauzenet le volt nyelve, de nem okozott gondott - (prgHiba)Javitva
*FATAL - unhandled error (15)! TS:1744189487011* kovetkezmenye az elozonek(symbol is szol, hogy sikertelen volt a feedback)
