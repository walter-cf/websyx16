import MyUtils as MU
from MySqlUtils import MySqlWrapper as mSqlWrapper

# import mysql as mySQL
import mysql.connector
import json


class MySqlService():
    mSql : mSqlWrapper
    
    def __init__(self):
        self.mSql = mSqlWrapper()
        
    def getWrapper(self) -> mSqlWrapper:
        return self.mSql
    
    def doSql(self, arrPath):
        R = []
        if 'getTests0' == arrPath[0]:
            resp = self.mSql.doSql()
            for r in resp:
                R.append(json.dumps(r))
        else:
            print(arrPath)
        return R
    
    def close(self):
        self.mSql.close()
    
