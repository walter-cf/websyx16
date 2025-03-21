#!/usr/bin/python3

import threading
import signal
from time import sleep
from typing import List
import json

import logging
import sys


import MyUtils as MU
import MySmtpClient as SM
import FdbUtils as FBU
import MySqlService as sqlSrv
from MySqlUtils import MySqlWrapper as mSqlWrapper

import GetProcessor as getProc
import PostProcessorUNAS as PPU
import PostProcessorEMAG as PPE
import UnasConnectHelper as UCH
import UnasOrderCache as UOC

global GBL_ErrorMessages
GBL_ErrorMessages = []

YAML_CONFIG_FILE = 'web6proxy.yaml'

ORDSTATCOLUMNS = [ "Id",  "VoucherNumber", "PrimeVoucherNumber", "CustomerOrderStatus", "Customer", "Closed", "Cancelled", "ClosedManually",  "RowVersion","RowModify" ]
Interrupted = False

# Elavult notUsed! 
def quickStatusChange( ):
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

def orderStatusUnas( prc ):
    # get Orders
    orders = FBU.getModifiedOrders(ORDSTATCOLUMNS, prc["orderStatusCheckInterval"], prc["checkVoucherSequence"])
    # foreach Orders
    for ord in orders:
        # set status if not Set?
        #status = None
        if 1 == ord[ ORDSTATCOLUMNS.index("Cancelled")]:
            #status = 'canceled'
            ordStatusStr = next(( x[1] for x in prc["statuses"] if x[0] == 'canceled'), "Megrendelés lezárva")
        elif 1 == ord[ ORDSTATCOLUMNS.index("Closed") ]:
            #status = 'closed'
            ordStatusStr = next(( x[1] for x in prc["statuses"] if x[0] == 'closed'), "Megrendelés lezárva")
        elif 1 == ord[ ORDSTATCOLUMNS.index("ClosedManually") ]:
            #status = 'manuallyClosed'
            ordStatusStr = next(( x[1] for x in prc["statuses"] if x[0] == 'manuallyClosed'), "Megrendelés lezárva")
        else:
            st = ord[ ORDSTATCOLUMNS.index("CustomerOrderStatus") ]
            ordStatusStr = next(( x[1] for x in prc["statuses"] if x[0] == st), None)
        #    ucc = next((x for x in  MU.UnasCustomerList.values() if x.unasId == unasId), None )
        if ordStatusStr is not None:
            #prc["statuses"]
            ordKey = ord[ ORDSTATCOLUMNS.index("PrimeVoucherNumber") ][ 1+len(MU.SYMBOLORDERIDPREFIX):]
            symbolId = int( ord[ORDSTATCOLUMNS.index("Id")]  )
            uoc = None if ordKey not in MU.UnasOrderList.keys() else MU.UnasOrderList[ordKey]
            if not uoc:
                ordXml = UCH.unasGetOrderBy("Key", ordKey)
                if ordXml is not None:
                    uoc = MU.putOrderXmlIntoCache(ordKey, ordXml)
                else:
                    uoc = UOC.UnasOrderCache(ordKey, -1, None, 0, 'Missing from UNAS')
                    MU.UnasOrderList[ordKey] = uoc 
                    _m = f""
                    SM.sendAlertMail('', 'Unasbol hianyzo rendeles')
            if uoc:
                if symbolId != uoc.symbolId:
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
            exec(f"x = {procName}(vals)")
            iterIdx = 0
            while not Interrupted and frequency > iterIdx:
                sleep(MU.BATCH_GRANULARITY)
                iterIdx = iterIdx + MU.BATCH_GRANULARITY
    print('Threads exiting', )

def processloop(threads):
    global Interrupted
    try:
        while not Interrupted:
            sleep(999999)
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
      
  logging.basicConfig(filename='syxBatch{0}.log'.format( '' if MU.serverPort == 3301 else '-'+str(MU.serverPort)),level=logLevel,format='%(asctime)s %(levelname)s %(name)s %(message)s')
  logger=logging.getLogger(__name__)

  if MU.isLogLevelWarn():
      print("Batch server started" )  #Server starts
      SM.sendAlertMail(f'batch-Server (re)started')
  #
  mSqlSrv = sqlSrv.MySqlService()
  #
  # Register the signal handlers
  signal.signal(signal.SIGTERM, service_shutdown)
  signal.signal(signal.SIGINT, service_shutdown)  
  #
  threads = []
  try:
    # MU.checkCacheState(force=True)
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
        SM.sendAlertMail("Batch Server stopped (normal)")
  except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    logging.error('Server Crashed x:', message)
    SM.sendAlertMail(message, "Batch Server aborted (CRASH)")

