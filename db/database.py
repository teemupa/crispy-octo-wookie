import sqlite3


DB_PATH     = '/home/pi/projects/rtdsd15/db/sensor_data.db'
DB_SCHEMA   = 'db/schema.sql'
KEYS_ON     = 'PRAGMA foreign_keys = ON'

class SensorDatabase(object):
    '''API to access the sensor value database.'''

    def __init__(self):
        super(SensorDatabase, self).__init__()

    def create_tables(self):
        '''
        Create database tables from schema
        '''
        con = sqlite3.connect(DB_PATH)
        with open (DB_SCHEMA) as f:
            sql = f.read()
            cur = con.cursor()
            cur.executescript(sql)


    def add_values(self, temp_in, hum):
        '''
        Insert sensor data values in to the
        '''
        if type(temp_in) is not float  or type(hum) is not float:
            #print("Error: Value not type of float.")
            return False
        stmnt = 'INSERT INTO SENSOR_DATA (temp_in, hum) VALUES(?,?)'
        con = sqlite3.connect(DB_PATH)
        with con:
            cur = con.cursor()
            cur.execute(KEYS_ON)
            pvalue = (temp_in, hum)
            try:
                cur.execute(stmnt, pvalue)
            except sqlite3.OperationalError:
                return False

            if cur.rowcount < 1:
                return False
            return True


    def get_values(self, limit):
        '''Get values from database'''
        stmnt = 'SELECT timestamp, temp_in, hum FROM SENSOR_DATA ORDER BY ID DESC LIMIT ?'
        con = sqlite3.connect(DB_PATH)
        with con:
            cur = con.cursor()
            cur.execute(KEYS_ON)
            pvalue = (limit,)
            rows = []
            try:
                cur.execute(stmnt, pvalue)
                rows = cur.fetchall()
            except sqlite3.IntegrityError:
                return False
            values = []
            for row in rows:
                value_row = dict(timestamp=row[0], temp_in=row[1], hum=row[2])
                values.append(value_row)
            return values

    def get_history_values(self):
        '''Get all history values'''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'SELECT TOP 24 timestamp, temp_in, hum FROM SENSOR_DATA ORDER BY timestamp desc'
        con = sqlite3.connect(DB_PATH)
        con.text_factory = str #To avoid UTF-8 encoding problem
        with con:
            cur = con.cursor()
            cur.execute(KEYS_ON)
            cur.execute(stmnt)
            rows = cur.fetchall()
            if rows is None:
                return False
            history_data = []
            for row in rows:
                data = dict(timestamp=row[0], temp_in=row[1], hum=row[2])
                history_data.append(task)
            return history_data
