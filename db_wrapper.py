"""
This script is overall resposible for creating the db handlers. This script reads all the DB details from dbconfig.ini files.

DB-wrapper is thread safe.
Added locking/semaphore concept on accessing the db handlers.
By default every process create one db handler connection(number of handlers to be created is configurable from config.ini file).
Connection Pool concept : We maintain the connection pool in our warpper itself.  Which contains all the handlers with the status, either it may be FREE or BUSY.
Every process/thread before executing the query, it will take the free handler from connection pool and acquire the lock on that, after successful execution of the query,
it will release the handler and this handler again go and sit in the pool with the status of FREE)
"""
__author__ = "Veerendra Patil"
__copyright__ = "Copyright 2017, The Lantern Project"
__credits__ = []
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Veerendra Patil"
__email__ = "Veerendra.Patil@ab-inbev.com"
__status__ = "Development"


import pyodbc
import _thread as thread
import string





class db_hndlr:
    """
    Over controller of creating the db handlers and executing the db queries.
    """
    __single = None
    dbHndlrList = []
    lock = thread.allocate_lock()

    def __init__(self, server, port, database, username,user_password,identifier):
        try:
            self.constr = "Driver={ODBC Driver 11 for SQL Server};Server=" + server + ";PORT=1433;Database=" + database + ";UID=" + username + ";PWD=" + user_password + ";charset='latin-1'"
            self.conn = pyodbc.connect(self.constr)
            self.cursor = self.conn.cursor()
            self.conn.autocommit = True
            self.id = identifier
            self.err = ''
            self.isFree = True

        except pyodbc.OperationalError as e:
            print("-- Database Error during connection setup => %s --", str(e))
            self.err = e

    def INIT():
        print("Calling INIT")
        db_hndlr.lock.acquire()
        try:
            if db_hndlr.__single == None:
                for i in range(1, dbConnPoolSize + 1):
                    dbHndlr_obj = db_hndlr(server, port, database, username,user_password,i)
                    if dbHndlr_obj.err == '':
                        db_hndlr.dbHndlrList.append(dbHndlr_obj)
                        print("====== Successfully created the database handlres, ready to use========")
                db_hndlr.__single = 'done'
        except Exception as e:
            print("Exception During Database Initialization=%s", str(e))
        db_hndlr.lock.release()

    INIT = staticmethod(INIT)

    def connect(self):
        self.conn = pyodbc.connect(self.constr)
        self.cursor = pyodbc.cursors()
        self.cursor.execute("SET AUTOCOMMIT=1")  # we will enable this after we review all logics

    def close(self):
        self.cursor.close()
        self.conn.close()


    def __execute(self,query,cmmd,params=None):
        stat = True
        results = []
        try:
            if cmmd == "SELECT":
                if params:
                    print("<<<< Executing Query -- %s with params -- %s and dbhndl id=%s", query, params,str(self.id))
                    cursor = self.conn.cursor().execute(query,params)
                    print(">>>> Executed Query -- %s with params -- %s and dbhndl id=%s", query, params,str(self.id))
                else:
                    print("<<<< Executing Query -- %s with dbhndl id=%s", query, str(self.id))
                    cursor = self.conn.cursor().execute(query)
                    print(">>>> Executed Query -- %s with dbhndl id=%s", query, str(self.id))

                columns = [column[0] for column in cursor.description]
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                self.conn.commit()
            elif cmmd == 'EXECUTE':

                if params:
                    print("<<<< Executing Query -- %s with params -- %s and dbhndl id=%s", query, params,str(self.id))
                    cursor = self.conn.cursor().execute(query,params)
                    print(">>>> Executed Query -- %s with params -- %s and dbhndl id=%s", query, params,str(self.id))
                else:
                    print("<<<< Executing Query -- %s with dbhndl id=%s", query, str(self.id))
                    cursor = self.conn.cursor().execute(query)
                    print(">>>> Executed Query -- %s with dbhndl id=%s", query, str(self.id))
                stat =  True
                result = ''

        except Exception as e:
            print("-- Error while executing the query and the error is => %s --", str(e))
            stat = False

        return stat, results

    def select(self, qstr,params=None):
        dbhndl_obj = None
        db_hndlr.lock.acquire()
        try:
            for tmp_obj in db_hndlr.dbHndlrList :
                if tmp_obj.isFree == True:
                    dbhndl_obj = tmp_obj
                    dbhndl_obj.isFree = False
                    print("Found idle dbhandle id = %s",str(dbhndl_obj.id))
                    break
        except Exception as e:
            print("Exception During Database selection=%s",str(e))
        db_hndlr.lock.release()
        if  dbhndl_obj == None:
            print("No dbhandle free....CANNOT PROCEED")
            return 'False',None
        try:
            stat, rowset = self.__execute(qstr, 'SELECT',params)
        except Exception as e:
            print("Excecption caught :%s",str(e))
        dbhndl_obj.isFree = True
        return stat,rowset

    def execute(self, qstr,params=None):

        dbhndl_obj = None
        db_hndlr.lock.acquire()
        try:
            for tmp_obj in db_hndlr.dbHndlrList:
                if tmp_obj.isFree == True:
                    dbhndl_obj = tmp_obj
                    dbhndl_obj.isFree = False
                    print("Found idle dbhandle id = %s", str(dbhndl_obj.id))
                    break
        except Exception as e:
            print("Exception During Database selection=%s", str(e))
        db_hndlr.lock.release()
        if dbhndl_obj == None:
            print("No dbhandle free....CANNOT PROCEED")
            return 'False', None
        try:
            stat, rowset = self.__execute(qstr, 'EXECUTE', params)
        except Exception as e:
            print("Excecption caught :%s", str(e))
        dbhndl_obj.isFree = True
        return stat, rowset

print("====== Now Its Time To Create databse handler========")
print("--- Loading DataBase module ---")
#--- Reading the DB settings from dbconfig.ini file

server = 'azrdwhlantern.database.windows.net'
port = 1433
database = 'azrdwhlantern'
username = 'Sovan'
user_password = 'xtM%T-qfdk3#@cXN'
db=db_hndlr(server,port,database,username,user_password,1)
dbConnPoolSize = 1
db.INIT()
#--- created the db handlers