'''
Driver wrapper for mysql-connector-python
'''
import time
import mysql.connector
from mysql.connector import Error

class DriverMySQL():
    '''
    Driver wrapper for mysql-connector-python
    Provides a uniform interface to SQL user code
    '''
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, connectionInfo):
        '''
        Constructor
        :param connectionInfo: dictionary having the items needed to connect to MySQL server:
                {'host', 'user', 'passwd', 'database', 'port' : 3306, 'use_pure' : False }
        '''
        self.host = connectionInfo['host']
        self.user = connectionInfo['user']
        self.passwd = connectionInfo['passwd']
        self.database = connectionInfo['database']        
        self.port = connectionInfo.get('port', 3306)
        self.use_pure = connectionInfo.get('use_pure', False)
        self.cursor = None
        self.connect()          
        
    def connect(self) -> bool:
        '''
        Connect to the database.
        
        use_pure=True will prevent BLOBs being returned as Unicode strings
          (which either fails when decoding or when comparing to bytes.)
        https://stackoverflow.com/questions/52759667/properly-getting-blobs-from-mysql-database-with-mysql-connector-in-python
        :return True/False
        '''
        self.connection = None
        try:
            self.connection = mysql.connector.connect(host=self.host, 
                                                      port=self.port, 
                                                      user=self.user, 
                                                      passwd=self.passwd, 
                                                      database=self.database,
                                                      use_pure=self.use_pure)
            return True
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
            return False

    def disconnect(self) -> bool:
        '''
        Disconnect from the database.
        :return True/False
        '''
        try:
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None
            return True
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
            return False
        
    def is_connected(self) -> bool:
        return self.connection is not None
        
    def execute(self, 
            query: str, 
            params: str | None = None, 
            commit: bool = False,
            reconnect: bool = True,
            fail_after: float = 86400
        ) -> bool:
        '''
        Execute an SQL query.
        :param query: str
        :param params: tuple or dictionary params are bound to the variables in the operation. 
                       Specify variables using %s or %(name)s parameter style (that is, using format or pyformat style).
        :param commit: If True, commit INSERT/UPDATE/DELETE queries immediately.
        :param reconnect: If True and the connection seems to have gone away, reconnect and retry the query.
        :param fail_after: Give up reconnecting after this many seconds
        :return True/False
        '''
        done = False
        delay = 0
        fail_at = time.time() + fail_after
        while not done:
            if not self.is_connected():
                self.connect()
            if not self.is_connected():
                time.sleep(delay)
                delay += 1
            else:
                try:
                    self.cursor = self.connection.cursor(buffered = True)
                    self.cursor.execute(query, params)
                    if commit:
                        self.connection.commit()
                    done = True
                except mysql.connector.Error as e:
                    print(f"MySQL error: {e}")
                    if not reconnect:
                        return False
                    else:
                        if time.time() > fail_at:                            
                            return False
                        time.sleep(delay)
                        delay += 1
                        try:
                            self.connection.reconnect()
                        except:
                            pass
        return True
    
    def commit(self) -> bool:
        '''
        Commit any previously executed but not yet committed INSERT/UPDATE/DELETE queries.
        :return True/False
        '''
        try:
            self.connection.commit()
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            return True
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
            return False
        
    def rollback(self) -> bool:
        '''
        Rollback any previously executed but not yet committed INSERT/UPDATE/DELETE queries.
        :return True/False
        '''
        try:
            self.connection.rollback()
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            return True
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
            return False

    def fetchone(self) -> tuple[any] | None:
        '''
        Fetch one row from the last SELECT query.
        :return tuple or None
        '''
        try:
            row = self.cursor.fetchone()
            return row
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
            return None    

    def fetchmany(self, max_rows) -> list[tuple[any]] | None:
        '''
        Fetch multiple rows from the last SELECT query.
        :param max_rows: max number of rows to fetch
        :return list of tuple or None
        '''
        try:
            result = self.cursor.fetchmany(max_rows)
            return result
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
            return None
        
    def fetchall(self) -> list[tuple[any]] | None:
        '''
        Fetch all rows from the last SELECT query.
        :return list of tuple or None
        '''
        try:
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
            return None
