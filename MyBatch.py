#!/usr/bin/python3

from threading import Thread
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
            prc["statuses"]
            ordKey = ord[ ORDSTATCOLUMNS.index("PrimeVoucherNumber") ][ 1+len(MU.SYMBOLORDERIDPREFIX):]
            symbolId = int(ORDSTATCOLUMNS.index("Id")  )
            uoc = None if ordKey not in MU.UnasOrderList.keys() else MU.UnasOrderList[ordKey]
            if not uoc:
                ordXml = UCH.unasGetOrderBy("Key", ordKey)
                uoc = MU.putOrderXmlIntoCache(ordKey, ordXml)
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
    batchProcesses: List[BatchContext] = []
    
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

def startProcess(bpCtx:BatchContext):
    pass

def stopProcess( t:Thread):
    
    t.join()

def stopProcesses(threads):
    logging.warning("Stop processes:%i" % len(threads))
    for t in threads:
        stopProcess(t)
    
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
      
  logging.basicConfig(filename='syxBatch.log',level=logLevel,format='%(asctime)s %(levelname)s %(name)s %(message)s')
  logger=logging.getLogger(__name__)

  if MU.isLogLevelWarn():
      print("Batch server started" )  #Server starts
      SM.sendAlertMail(f'batch-Server (re)started')
  #
  mSqlSrv = sqlSrv.MySqlService()
  #
  threads = List[Thread]
  try:
      MU.checkCacheState(force=True)
      # get Processes
      for proc in MU.BATCH_PROCESSES:
          # run process
          bp = MyBatch()
          xxx_myMyslConnection = bp.mSql.getConn()
          thread = Thread( target = startProcess, name = proc.name, args = (proc, ))
          thread.start()
          
  except KeyboardInterrupt:
      logging.info('Server closing...')
      stopProcesses(threads)
      logging.info('Server closed')
      
  #fb_Conn = FBU.getFbConn()
  #FBU.dbClose
  
  if MU.isLogLevelWarn():
        print("Server stopped.")
        SM.sendAlertMail("Server stopped")
