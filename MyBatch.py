#!/usr/bin/python3

import json
import logging
import signal
import sys
import threading
from time import sleep
from typing import List

from lxml import etree as ET

import FdbUtils as FBU
import MySmtpClient as SM
import MyUtils as MU
import UnasConnectHelper as UCH
import UnasOrderCache as UOC
from MyServer import logrotate
from MySqlUtils import MySqlWrapper as mSqlWrapper
from MyUtilsTypes import (AlertMailType, MyProgramFlowWarningException,
                          ProxyErrCode, ProxyObjectType, UnasTransactionType)

MunchInstalled = False
try:
    from munch import DefaultMunch
    MunchInstalled = True
except Exception:
    MunchInstalled = False
    
global GBL_ErrorMessages
GBL_ErrorMessages = []

YAML_CONFIG_FILE = 'web6proxy.yaml'

ORDER_SETSTAUS_XML = '<Action>modify</Action><Key>%s</Key><Status>%s</Status><StatusEmail>%s</StatusEmail><Params><Param><Name>symbolId</Name><Value>%i</Value></Param></Params>'

ORDSTATCOLUMNS = [ "Id",  "VoucherNumber", "PrimeVoucherNumber", "CustomerOrderStatus", "Customer", "Closed", "Cancelled", "ClosedManually",  "RowVersion","RowModify" ]
Interrupted = False

def masterChallengeUnas(prc):
    raise MyProgramFlowWarningException("Not Usable Yet, under developed until... faszomTuggya ",1234321)

# Elavult notUsed! 
def quickStatusChange_NU( ):
    # get Orders
    orders = FBU.getModifiedOrders(ORDSTATCOLUMNS, 999962, 42)
    # foreach Orders
    for ord in orders:
        # set status if not Set? Visszaigazolva, , Megrendelés lezárva
        #status = None
        if 1 == ord[ ORDSTATCOLUMNS.index("Cancelled")]:
            #status = 'canceled'
            ordStatusStr =  "Megrendelés lezárva"
        elif 1 == ord[ ORDSTATCOLUMNS.index("Closed") ]:
            #status = 'closed'
            ordStatusStr = "Megrendelés lezárva"
        elif 1 == ord[ ORDSTATCOLUMNS.index("ClosedManually") ]:
            #status = 'manuallyClosed'
            ordStatusStr = "Megrendelés lezárva"
        else:
            st = ord[ ORDSTATCOLUMNS.index("CustomerOrderStatus") ]
            if st  == 2:
                ordStatusStr = "Visszaigazolva"
            elif st  == 3:
                ordStatusStr = "Készletezés alatt"
        #    ucc = next((x for x in  MU.UnasCustomerList.values() if x.unasId == unasId), None )
        if ordStatusStr is not None:
            # prc["statuses"]
            ordKey = ord[ ORDSTATCOLUMNS.index("PrimeVoucherNumber") ][ 1+len(MU.SYMBOLORDERIDPREFIX):]
            symbolId = int(ord[ORDSTATCOLUMNS.index("Id")]  )
            uoc = None if ordKey not in MU.UnasOrderList.keys() else MU.UnasOrderList[ordKey]
            if not uoc:
                ordXml = UCH.unasGetOrderBy("Key", ordKey)
                uoc = MU.putOrderXmlIntoCache(ordKey, ordXml)
            if uoc:
                if symbolId > 0  and symbolId != uoc.symbolId:
                    logging.error("Set statusnal UOC symbolId kulonbozott!!! Ori-UOC-id:{uoc.symbolId} symb:orderId:{symbolId}")
                    # uoc.symbolId = symbolId
                elif (ordStatusStr == uoc.orderStatus):
                    logging.debug("Skipping:%s", ordKey)
                else:
                    xmlResp = UCH.unasSetOrderStatus( ordKey,  ordStatusStr, symbolId)
                    logging.debug(f'SetOrder:[{ordKey}] set Status: {ordStatusStr}')
                    logging.debug(f'SetOrder response:{xmlResp}')
                    print(xmlResp)
                    # TODO meg kellene vizsgalni, hogy xml valos-e
                    if xmlResp.find('<Status>ok</Status>') > 0:
                        uoc.orderStatus = ordStatusStr
            else:
                logging.error("ordKEY missing Missing from UNAS Skipping:%s", ordKey)
            #
        # TODO into Cache and cache handling

def getOrdercacheFromProxy():
    # code, resp = UCH.callProxyControl('status/cache/orders')
    code, resp = UCH.callWebControl('qry/unascache/order')
    return [] if code > 200 else json.loads(resp)
    
def orderStatusUnasProxy( prc ):
    skippingStatus = next(( x[1] for x in prc["statuses"] if x[0] == 'manuallyClosed'), prc["defaultClosedStatus"])
    # get Orders
    orders = FBU.getModifiedOrders(ORDSTATCOLUMNS, prc["orderStatusCheckInterval"], prc["checkVoucherSequence"])
    # orderStatusXmlArray = []
    # foreach Orders
    for ord in orders:
        # set status if not Set?
        #status = None
        symbolId = int( ord[ORDSTATCOLUMNS.index("Id")]  )
        ordKey  = ord[ ORDSTATCOLUMNS.index("PrimeVoucherNumber") ][ 1+len(MU.SYMBOLORDERIDPREFIX):]
        ordCode = ord[ ORDSTATCOLUMNS.index("VoucherNumber") ]
        badOrder = MU.UnasBadOrderList.get( symbolId )

        if badOrder is None or badOrder.badCounter < 4: 
            if 1 == ord[ ORDSTATCOLUMNS.index("Cancelled")]:
                #status = 'canceled'
                ordStatusStr = next(( x[1] for x in prc["statuses"] if x[0] == 'canceled'), prc["defaultClosedStatus"])
            elif 1 == ord[ ORDSTATCOLUMNS.index("Closed") ]:
                #status = 'closed'
                ordStatusStr = next(( x[1] for x in prc["statuses"] if x[0] == 'closed'), prc["defaultClosedStatus"])
            elif 1 == ord[ ORDSTATCOLUMNS.index("ClosedManually") ]:
                #status = 'manuallyClosed'
                ordStatusStr = next(( x[1] for x in prc["statuses"] if x[0] == 'manuallyClosed'), prc["defaultClosedStatus"])
            else:
                st = ord[ ORDSTATCOLUMNS.index("CustomerOrderStatus") ]
                ordStatusStr = next(( x[1] for x in prc["statuses"] if x[0] == st), None)
            #    ucc = next((x for x in  MU.UnasCustomerList.values() if x.unasId == unasId), None )
            if ordStatusStr is not None:
                #prc["statuses"]
                uoc = None if ordKey not in MU.UnasOrderList.keys() else MU.UnasOrderList.get(ordKey)
                if not uoc:
                    _xml = UCH.unasGetOrderBy("Key", ordKey)
                    #getOrders....
                    _ords = ET.fromstring(  _xml.replace(MU.XMLTAG, '').replace('\r\n', '') )
                    if _ords is not None and len(_ords.getchildren()) > 0:
                        uoc = MU.putOrderXmlObjectIntoCache(ordKey, _ords)
                    elif  ordStatusStr == skippingStatus: # UNAS bol hianyzik, Statusza manuallyClosed: KIZAROM a folyamatbol
                        tmpOrder = UOC.UnasOrderCache(ordKey, sid=symbolId, ordcode=ordCode, status=skippingStatus)
                        tmpOrder.badCounter = 11 # Azonnal kizarom!
                        MU.UnasBadOrderList[symbolId] = tmpOrder
                        _m = f"Symbol Rendeles: {ordKey} / {ordCode} (Id:{symbolId}) - UNAS bol hianyzik, Statusza manuallyClosed: Azonnal KIZAROM a folyamatbol"
                        _m += "\r\n\r\n A web6Proxy ujrainditaskor visszakerul a folyamatba - ezt kesobb kezelem majd, elteszem a ``Rosszak listajat``"
                        SM.sendProxyMail(_m, AlertMailType(UnasTransactionType.ORDERSTATUS, oid=symbolId, otyp=ProxyObjectType.ORDER), 'Lekezeletlen rendeles! Unasbol hianyzik: %s' % ordKey)
                    else:
                        if badOrder is None:
                            tmpOrder = UOC.UnasOrderCache(ordKey, sid=symbolId, ordcode=ordCode, status=ordStatusStr)
                            tmpOrder.badCounter = 1 + tmpOrder.badCounter
                            MU.UnasBadOrderList[symbolId] = tmpOrder
                        badOrder.badCounter = 1 + badOrder.badCounter
                        _m = f"Symbol Rendeles: {ordKey} / {ordCode} (Id:{symbolId}) adatai valtoztak, de az UNAS-ban nem talalhato"
                        if badOrder.badCounter >= 4:
                            _m += "\r\nTobbszoros (3) probalkozasbol nem sikerult megtalalni a rendelest - KIZAROM a feldolgozasbol!"
                        else:
                            _m += f"\r\nTobbszoros: {badOrder.badCounter}. probalkozas"
                        #
                        SM.sendProxyMail(_m, AlertMailType(UnasTransactionType.ORDERSTATUS, oid=symbolId, otyp=ProxyObjectType.ORDER),'Lekezeletlen rendeles! Unasbol hianyzik: %s' % ordKey)
                #
                if uoc:
                    if symbolId != uoc.symbolId:
                        if ordStatusStr != skippingStatus:
                            MU.UnasBadOrderList[symbolId] = uoc
                            _msg = f"Set statusnal UOC symbolId kulonbozott!!! Ori-UOC-id:{uoc.symbolId} symb:orderId:{symbolId}"
                            MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.B24), level = logging.ERROR, eDescr=sys.exc_info())
                            uoc.badCounter = 1 + uoc.badCounter

                    elif (ordStatusStr == uoc.orderStatus):
                        logging.debug(f"Skipping:{ordKey}({symbolId}) BizSz:{ord[ORDSTATCOLUMNS.index('VoucherNumber')]} Customer:{uoc.code}({uoc.symbolCustId})")
                    else:
                        # TODO BVlokkosirttani
                        # orderStatusXmlArray.append(f"<Order>{ORDER_SETSTAUS_XML % (ordKey, MU.ORDER_STATUS_SENDMAIL, ordStatusStr, symbolId)}</Order>")
                        xmlResp = UCH.unasSetOrderStatus( ordKey,  ordStatusStr, symbolId)
                        logging.debug(f'SetOrder:[{ordKey}] set Status: {ordStatusStr}')
                        # TODO meg kellene vizsgalni, hogy xml valos-e
                        if xmlResp.find('<Status>ok</Status>') > 0:
                            uoc.orderStatus = ordStatusStr
                        else:
                            _msg = f"ORDERSTATUS process error - UNAS reply:\r\n{xmlResp}"
                            _msg = f"A status feldolgozasbol kizartam:  {ordKey} ({symbolId}) / {ordStatusStr} )"
                            MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.B25), level = logging.ERROR, eDescr=sys.exc_info())
                            MU.UnasBadOrderList[symbolId] = uoc
                            uoc.badCounter = 11
                elif  ordStatusStr == skippingStatus:
                    pass
                else:
                    logging.error("ordKEY missing from UNAS Skipping:%s", ordKey)
                #
            # TODO into Cache and cache handling
            ## if len(orderStatusXmlArray) > 0:
            ##     xmlResp = UCH.unasOrder_Direct(orderStatusXmlArray.join('\n'))
            ##     logging.debug(f'SetOrder response:{xmlResp}')
            ##     print(xmlResp)
        #
        elif badOrder:
            logging.debug("BadList hit:%s" % badOrder)

def orderStatusUnas( prc ):
    UCH.callGET('batch/orderStatusUnas')
    
def saveUnasProxyContext( prc ):
    UCH.callProxyControl('saveProxyContext')

def refreshUnasCache( prc ):
    if MU.WEB_CONTROL_ENABLED:
        UCH.callUnasGET('initcache')
    MU.checkCacheState(typ=ProxyObjectType.ORDER)


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

class BatchContext():
    startDelay: int = 0
    frequency : int = 600
    name      : str = 'Default processName'
    method    : str = 'nullProcess()'
    active    : int  = 0
    lastRun   : int  = 0
    
    
    def __init__(self):
        self.mSql = mSqlWrapper()

class MyBatch():
    mSql : mSqlWrapper
    batchProcesses: List[BatchContext] = []  # Nem hasznalom, pedig lehetne, de nincs szikronaizalva a YAML-lal

    def __init__(self):
        self.mSql = mSqlWrapper()
    
    def doSql(self, arrPath):
        R = []
        if 'getTests0' == arrPath[0]:
            resp = self.mSql.doSql()
            for r in resp:
                R.append(json.dumps(r))
        else:
            print(arrPath)
        return R
    
    def rollback(self):
        self.mSql.commit()


def startProcess1(prc):
    logger.info('Process1 Started at:%s' , MU.tsToDateSql(MU.getCurrTime()))
    print('Process1 Started at:%s' , MU.tsToDateSql(MU.getCurrTime()))
    print(prc)

def startProcess2(prc):
    logger.info(' Process22222 Started at:%s' , MU.tsToDateSql(MU.getCurrTime()))
    print(' Process22222 Started at:%s' , MU.tsToDateSql(MU.getCurrTime()))
    print(prc)
    
def startProcess3(prc):
    logger.info(' Process3 3 Harom Started at:%s' , MU.tsToDateSql(MU.getCurrTime()))
    print(' Process3 3 Harom Started at:%s' , MU.tsToDateSql(MU.getCurrTime()))
    print(prc)

def startProcess(**kwargs):
    global Interrupted
    print(kwargs)
    for key , vals in kwargs.items():
        startDelay = vals["startDelay"]
        sleep(  startDelay if startDelay > 0 else 0)
        frequency = vals["frequency"]
        procName = vals["method"]
        while not Interrupted:
            logger.info(' Process:%s Started at:%s' , procName, MU.tsToDateSql(MU.getCurrTime()))
            try:
                exec(f"x = {procName}(vals)")
            except Exception as e:
                if isinstance(e, KeyboardInterrupt):
                    Interrupted = True
                elif isinstance(e, ServiceExit):
                    Interrupted = True
                else:
                    _msg = f"Batch exception ({procName}) : {str(e) if not hasattr(e, 'message') else e.message}"
                    MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.B26), eDescr=sys.exc_info())
            iterIdx = 0
            while not Interrupted and frequency > iterIdx:
                sleep(MU.BATCH_GRANULARITY)
                iterIdx = iterIdx + MU.BATCH_GRANULARITY
    print('Threads exiting', )

def processloop(threads):
    global Interrupted
    try:
        try:
            while not Interrupted:
                sleep(999999)
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                Interrupted = True
            elif isinstance(e, ServiceExit):
                Interrupted = True
            else:
                _msg = f"Batch exception : {str(e) if not hasattr(e, 'message') else e.message}"
                MU.errorHandler(_msg, AlertMailType(UnasTransactionType.UNKNOWN_MAX, code=ProxyErrCode.B27), eDescr=sys.exc_info())
    except (KeyboardInterrupt, ServiceExit) as ex:
      logging.info('Batch Server interrupted - closing...(%s)', ex)
    #
    Interrupted = True
    # and wait
    for t in threads:
        t.join()
    logging.info('Server closed')
    
    
def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit
 
if __name__ == "__main__":
  configPath = YAML_CONFIG_FILE
  if (len(sys.argv)>1):
    configPath = sys.argv[1]
  MU.readYaml(configPath)

  GBL_ErrorMessages = []
  if MU.LOGLEVEL[0].upper() == 'I':
      logLevel = logging.INFO
  elif MU.LOGLEVEL[0].upper() == 'W':
      logLevel = logging.WARNING
  elif MU.LOGLEVEL[0].upper() == 'E':
      logLevel = logging.ERROR
  else:
      logLevel = logging.DEBUG
      
  logFileName='syxBatch{0}.log'.format( '' if MU.serverPort == 3301 else '-'+str(MU.serverPort))
  logrotate(logFileName)
  logging.basicConfig(filename=logFileName,level=logLevel,format='%(asctime)s %(levelname)s %(name)s %(message)s')
  logger=logging.getLogger(__name__)

  MU.getUnasContext().processName = 'Batch'
  if MU.isLogLevelWarn():
      print("Batch server started" )  #Server starts
      SM.sendProxyMail(f'batch-Server (re)started', AlertMailType(UnasTransactionType.STARTBATCH), 'starting')
  #
  # TODO Tesztelni kelene a szervizeket, rendelkezesre allnak-e: Socket, WebControl, FDB, MySQL
  # mSqlSrv = sqlSrv.MySqlService()
  #
  # Register the signal handlers
  signal.signal(signal.SIGTERM, service_shutdown)
  signal.signal(signal.SIGINT, service_shutdown)  
  #
  threads = []
  try:
    # MU.checkCacheState(force=True) # TODO Ezt at kell hozni a Proxy-bol
    if MunchInstalled:
        try:
            print(MU.UnasOrderList)
            for f in getOrdercacheFromProxy():
                f['ordXml'] = None
                MU.UnasOrderList[f['orderKey']] =  DefaultMunch.fromDict(f)
        except Exception as e:
            logging.error('getOrdercacheFromProxy Failed: %s', str(e) if not hasattr(e,'message') else e.message)
    # get Processes
    # ??? bp = MyBatch()
    # ??? myMyslConnection = bp.mSql.getConn()
    for batchItem in MU.BATCH_PROCESSES:
        for procName, procArgs in batchItem.items():
            logger.info('Thread :%s created', procName)
            # run process
            thread = threading.Thread( target = startProcess, name = procName, kwargs = { procName: procArgs } )
            threads.append(thread)
            thread.start()
    # Wait for all threads to finish.
  except (KeyboardInterrupt, ServiceExit) as ex:
    Interrupted = True
    logging.info('Server closing...(%s)', ex)
    logging.info('Server closed')

  #fb_Conn = FBU.getFbConn()
  #FBU.dbClose
  try:
    processloop(threads)
    if MU.isLogLevelWarn():
        print("Server stopped normally.")
        SM.sendProxyMail("Batch Server stopped (normal)", AlertMailType(UnasTransactionType.STARTBATCH), 'web6batch stopped')
  except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    logging.error('Server Crashed x:', message)
    SM.sendProxyMail(message, AlertMailType(UnasTransactionType.STARTBATCH), "Batch Server aborted (CRASH)")

