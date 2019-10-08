import collections
from datetime import datetime
import pymysql #PyMySQL-0.9.3
from typing import *
import sys

from SimpleBenchmarkToConsole import *
import Config as Config

class DatabaseConnector:

    maxBatchSize = 50


    def __init__(self):
        self.host = Config.db['host']
        self.port = Config.db['port']
        self.db = Config.db['db']
        self.user = Config.db['user']
        self.password = Config.db['password']

    def ExecuteMultipleRaw(self, sql: str):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db)
        cur = conn.cursor()

        r = cur.execute(sql)
        records = [x[0] for x in cur.fetchall()]


        return records

    def ExecuteRawSingle(self, sql: str):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db)
        cur = conn.cursor()

        r = cur.execute(sql)
        record = cur.fetchone()
        
        return record[0] if len(record) > 0 else None


    @SimpleBenchmarkToConsole
    def WriteToDatabase(self, objects: List[str], table: str, keys: Dict, propertiesAgainst: List[str] = [], shouldUpdateDelegate = None):
        
        if len(objects) == 0:
            return

        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db)
        cur = conn.cursor()
        print('table --> ' + table)
        batchSize = 0

        inserted = 0
        updated = 0
        skipped = 0
        failed = 0

        paramsHolder = ['%s' for i in range(len(keys))]
        keysHolder = ['`{0}`'.format(key) for key in keys]
        insertQuery = f"INSERT INTO `{table}` ({', '.join(keysHolder)}) VALUES ({', '.join(paramsHolder)})"


        for o in objects:
            temp = [getattr(o, key) for key in keys]
            checkQuery = ""
            executeInsertQuery = True
        
            if len(propertiesAgainst) > 0:
                selectCols = ['`{0}`'.format(key) for key in propertiesAgainst]
                whereClauseList = [f"`{p}` = '{getattr(o, p)}'" for p in propertiesAgainst]
                checkQuery = f"SELECT {', '.join(selectCols)} FROM {table} WHERE {' AND '.join(whereClauseList)}" 

            try:
                cur = conn.cursor()
                if len(propertiesAgainst) > 0:
                    r = cur.execute(checkQuery)
                    records = cur.fetchall()
                    if len(records) > 0: 
                        executeInsertQuery = False

                if table == 'CommitteeMembers':
                    if o.MemberId == '48690'  and o.CommitteeId  == '40' and o.From == '2016-11-16':
                        uuu = 999
                if executeInsertQuery:
                    r = cur.execute(insertQuery, temp)
                    inserted += 1

                elif shouldUpdateDelegate is not None and shouldUpdateDelegate(o):
                    setParams = ','.join([f'`{v}`=%s' for k,v in keys.items()])
                    updateQuery = f"UPDATE `{table}` SET {setParams} WHERE {' AND '.join(whereClauseList)}"
                    r = cur.execute(updateQuery, temp)
                    updated += 1
                else:
                    skipped += 1

                cur.close()
            except pymysql.IntegrityError as e:
                failed += 1
            except Exception as e:
                print(e)
                failed += 1

            batchSize += 1
            if batchSize >= self.maxBatchSize:
                conn.commit()
                batchSize = 0

        if batchSize > 0:
            conn.commit()

        print(f".")
        print(f"--- Inserted - {inserted} --- Updated - {updated} --- Skipped - {skipped} --- Failed - {failed}")


        conn.commit()
        cur.close()
        conn.close()

        # SELECT * FROM `CommitteeMembers` WHERE CommitteeId = 40 AND MemberId = 48690 and `From` = '2016-11-16'


#ALLOW - table name in query
#DISALLOW - DROP, --, /*, */, TRUNCATE, DELETE, UPDATE
