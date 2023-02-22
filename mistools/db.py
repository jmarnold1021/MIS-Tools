
"""
The DB Singleton Module contains
functions for reading/writing
data to the database...
"""

import pyodbc
import os
import json


LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )
CONFIGS_PATH = "%s/../configs/configs.json" % LIB_ROOT

DB_CONN_STR_TEMPLATE = r'Driver=SQL Server;Server=%s;Database=%s;Trusted_Connection=yes;'
DB_MAX_BATCH = 1000

class DB:

    def __init__(self, db_config_name):

        '''
        Create a connection to the DB

        :param str db_config_name: colleague/mis/ods see configs

        :return: Instance of DB a connection

        :rtype: None

        '''

        db_config_name = db_config_name.strip().upper() # adjust user input

        with open(CONFIGS_PATH) as configs:
            configs = json.load(configs)

        server_name = configs['DB'][db_config_name]['SERVER_NAME']
        db_name     = configs['DB'][db_config_name]['DB_NAME']

        conn_str    = DB_CONN_STR_TEMPLATE % \
                      (server_name, db_name)

        self.cnxn = pyodbc.connect(conn_str)

    def exec_query(self, sql, columns=False, dict_read=False):

        '''
        Executes an SQL query with this connection

        :param str sql: An sql query

        :param bool columns: Return the columns with the data.

        :param list dict_read: Return the data as a list of dicts.

        :return: 2D list of query results

        :rtype: list

        '''

        cursor = self.cnxn.cursor()
        cursor.execute(sql)
        # why make downstream care aabout pyodc rows?
        # row[0] has data, not sure of rest yet...
        data = [list(row) for row in cursor.fetchall()]

        if dict_read:
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, elem)) for elem in data]


        if columns:
            columns = [column[0] for column in cursor.description]
            return [columns] + data

        cursor.close()

        return data

    def insert_batch(self, resource, data, batch_size=DB_MAX_BATCH):

        '''
        Batch inserts the provided data to the provided resource

        :param str resource: db table/destination.

        :param list data: list of lists containt data elements to insert.

        :param int batch_size: How many rows to insert in a single batch

        :return: The total number of rows inserted.

        :rtype: int

        '''

        if batch_size > DB_MAX_BATCH:
            batch_size = DB_MAX_BATCH

        # get values from dict data rows
        if type(data[0]) == dict:
            data = [list(row.values()) for row in data]

        db_lines = [] # (..row[0]..), (..row[1]..), ...
        for row in data:
            #print(row)
            db_line = list(map(lambda x: x.replace( "'", "''"), row)) # add sql '' apostrophe in abbrevs
            # this list conversion looks arbitrary...
            db_line = list(map(lambda x: x.replace( x, "'" + x + "'"), db_line)) # create sql strings

            db_line = ','.join(db_line) # create sql batch insert line
            db_line = '(' + db_line + ')'

            db_lines.append(db_line)


        cursor = self.cnxn.cursor()

        db_insert = 'INSERT INTO ' + resource + ' VALUES '

        start  = 0
        end    = batch_size
        inc    = batch_size
        stop   = len(db_lines)
        row_count = 0
        while start <= stop:

            db_values = ','.join(db_lines[start:end])
            start += inc
            end   += inc
            query = db_insert + db_values
            cursor.execute( query )
            cursor.commit()
            if cursor.rowcount is not None:
                row_count += cursor.rowcount

        cursor.close()

        return row_count

    def close(self):

        '''
        Close this connection to the DB

        :return: Closes this DB connection

        :rtype: None

        '''

        self.cnxn.close()













