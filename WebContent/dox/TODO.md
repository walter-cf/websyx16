# TODO

- Az UNAS limitek hivasspecifikusak is. Van orankent  
  - total packet count
  - egyszeres / tobbszoros  
  **setCustomer**
    ``` 
    Hívásonként egy megrendelés lekérdezése esetén:  
      PREMIUM 1000 hívás / óra  
      VIP 3000 hívás / óra  
    Hívásonként több megrendelés lekérdezése esetén:  
      PREMIUM 30 hívás / óra  
      VIP 90 hívás / óra
    ```  
    **setOrder**
    ```
    Maximum 100 megrendelést tartalmazó hívások esetén:  
      PREMIUM 1000 hívás / óra  
      VIP 3000 hívás / óra  
    Több, mint 100 megrendelést tartalmazó hívások esetén esetén:  
       PREMIUM 30 hívás / óra  
       VIP 90 hívás / óra  
    ```  
- Batch - handle service not available:  
Ha valamelyik eroforras nem elerheto (Sql, Net, Unas...), akkor a proxy folyamatosan ujraindul.  
Valamennyi ideig disabledbe kellene tennem es csak utana ujraprobalni:  
  disabledUntil = now() + 10 perc(yaml-bol) mondjuk  

- Batch code a proxyServer -be? Egyelore meg nem merem...  

- TODO sorokat kiszedni a code-bol  
A TODO sorok fele valoszinuleg ertelmetlen mar, ettol fuggetleneul, ha mart otthagytam a kodban, akkor legalabb egyszer ra kellene neznem  
  ```  
    GetProcessor.py:108:                else: #  TODO !!!!!  Ezzel vigyaznom kellene !!!!! UCO vs UCU nincs rendesen atgondolva!  
    GetProcessor.py:153:        # TODO Nincs atirva - elhanyagoltam, mert soha nem hasznaltam  
    GetProcessor.py:344:            houseNumber = None # TODO Hack !!   
    GetProcessor.py:366:        # TODO Ez HACK es nem tudom, mi a hatasa, megprobalom a houseNumbert None-nak tartani  
    GetProcessor.py:1339:                if idx > 5: # TODO Ez fingom sincs micsoda, vagy mit akartam  
    GetProcessor.py:1527:# # #                    # TODO ex itt igy nem jo meg, csak a felesleget kellene felvinni!!  
    MyBatch.py:86:                    # TODO meg kellene vizsgalni, hogy xml valos-e  
    MyBatch.py:92:        # TODO into Cache and cache handling  
    MyBatch.py:169:                        # TODO BVlokkosirttani  
    MyBatch.py:173:                        # TODO meg kellene vizsgalni, hogy xml valos-e  
    MyBatch.py:187:            # TODO into Cache and cache handling  
    MyBatch.py:343:  # TODO Tesztelni kelene a szervizeket, rendelkezesre allnak-e: Socket, WebControl, FDB, MySQL  
    MyBatch.py:352:    # MU.checkCacheState(force=True) # TODO Ezt at kell hozni a Proxy-bol  
    MyProxyControl.py:56:# TODO Ext meg azert at kell nezni, kell-e a binaris read egyaltalan?  
    MyProxyControl.py:103:        return resp or '[]', 'text/plain' # TODO Ki kellene elemezni a valaszt Jo/Rossz  
    MyServer.py:96:          # TODO a communacation errort itt kezelhetnem, esetleg - mert ujrakuldom az egeszet, megjelolve a feldolgozottakat  
    MyServer.py:176:      # TODO Ha idaig eljutott, akkor mar NAGY baj van! Ezert gondoltam, hog a a commErrCnt figyelembe veszem!  
    MyServer.py:332:  # TODO setXXX error 400 eseten ki kell elemzni a hibat es ha lehet, akkor ujra kuldeni a hibas tetel nelkul  
    MyServer.py:333:  # TODO a communacation errort itt kezelhetnem, esetleg - mert ujrakuldom az egeszet, megjelolve a feldolgozottakat  
    MyServer.py:338:      # TODO Ha idaig eljutott, akkor mar NAGY baj van! Ezert gondoltam, hog a a commErrCnt figyelembe veszem!  
    MyServer.py:566:  # TODO DB Connect TEST-eket kellene vegezni es ha nincs, akkor leallni vagy varni 5 percet 3x ujraprobalni es utana fatalExit  
    MySmtpClient.py:25:    # TODO a contextet ki kell egsziteni az objektum typpal es az objektumId vel  
    MySqlUtils.py:94:        objTyp = 'other' # TODO alertmailtypebol kepzem majd, ha lesz!  
    MyUtils.py:140:        ORDER_ITEM_FROMDB_FORCE    = cfg["unas"]["order"]["itemFromDbForce"] or False          # TODO Elavult, mar nem kell  
    MyUtils.py:141:        ORDER_ITEM_FROMDB_ON_MISSING = cfg["unas"]["order"]["itemFromDbOnMissing"] or False    # TODO Elavult, mar nem kell  
    MyUtils.py:245:                for addr in cust.find('Addresses'): # TODO Kikapcsolt cimkezelesnel nem kellen basztatni a cimeket - asszem  
    MyUtils.py:304:        # TODO: undeveloped part. Not ready Yet!  
    MyUtils.py:1579:    return getUnasContext().lastTS # TODO Logoljam a transaction Created Event-t?  
    MyUtils.py:1816:    return True if unasContext.masterClient is None else  unasContext.masterClient.ip != ip # TODO ez igy nem jo! Elobb biztosan tudnom kellene miert nics masterclienta   promoter miatt  
    MyUtils.py:1818:# TODO Not Ready Yet! Under development !!!  
    MyUtilsTypes.py:304:        self.lastAction  = None # TODO Valamiert ezt kikommenteztem egyszer. Nem szerepelt a structban, ha None volt?  
    PostProcessorUNAS.py:27:    # TODO MyUTils CONTSTANT kent kezelni felteteles ellenorzeskent  
    PostProcessorUNAS.py:141:                # TODO Ha tobb raktar lesz, akkor raktarankent kell nyilvantartanom a upc.stocks -ban  
    UnasConnectHelper.py:196:# TODO Ezekbe is kellene a hibakezeles  
  ```  

- Hibauzenetek:  
ProxyErrCode.UNKNOWN mindenhol - ertelmesebbre cserelni  
Errorcode B24 pl, doksit csinalni rola melyik-melyik
- python 3.13 venv  tovabbi futtasokhoz, aztan majd az uj gepnel figyelne rendes installra, most ossze van keveredve a 3.8, 3.12, 3.13 lib-ek.  
Katyvasz az egesz, csoda az hogy mukodik meg  

- ....

