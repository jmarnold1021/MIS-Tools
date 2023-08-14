
"""
The DB Class holds a db connection object,
and provides functions for Inserting, Deleting, and
Querying data using the provided connection.
"""

import pyodbc
import os
import json
from decimal import Decimal
from datetime import datetime

from . import mislog
from . import misconfig

LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )

# possible globals/configs
DB_CONN_STR_TEMPLATE = r'Driver=SQL Server;Server=%s;Database=%s;Trusted_Connection=yes;'
DB_MAX_BATCH = 1000

# global lib logger...
CONFIGS = misconfig.mis_load_config()
DB_CONFIGS = CONFIGS['DB']
db_log  = mislog.mis_console_logger('db_log', DB_CONFIGS['LOG_LEVEL'])

class DB:

    def __init__(self, db_config_name):

        '''
        Create a connection to the DB

        :param str db_config_name: colleague/mis/ods see configs

        :return: Instance of DB a connection

        :rtype: Object

        '''
        if db_config_name is None:

            db_log.critical('No DB name provided')
            return

        db_config_name = db_config_name.strip().upper() # adjust user input

        self.name = db_config_name # for logging instance stuff

        if db_config_name not in DB_CONFIGS or \
           'SERVER_NAME'  not in DB_CONFIGS[db_config_name] or \
           'DB_NAME'      not in DB_CONFIGS[db_config_name]:

            db_log.critical('No DB configs found for %s' % db_config_name)
            return

        server_name = DB_CONFIGS[db_config_name]['SERVER_NAME']
        db_name     = DB_CONFIGS[db_config_name]['DB_NAME']

        conn_str    = DB_CONN_STR_TEMPLATE % \
                      (server_name, db_name)

        self.cnxn   = pyodbc.connect(conn_str)

    # enter and exit interface provide ability to work with context managers and are not explicitly used...
    def __enter__(self):

        db_log.debug('Opening Context Manager Connection for %s' % self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        db_log.debug('Calling Exit and Closing Connection for %s after context manager' % self.name)
        self.close()

    def get_attrs(self, table):

        '''
        Return the DB attrs for a provided table.

        :param str table_name

        :return: list of attrs

        :rtype: list

        '''

        query = 'SELECT TOP(1)* FROM %s' % table
        cursor = self.cnxn.cursor()
        cursor.execute( query )
        columns = [column[0] for column in cursor.description]

        return columns

    def truncate(self, table):

        '''
        Truncates the provided table.

        :param str table: An sql table to truncate

        :return: Nothing atm...

        :rtype: None

        '''
        query = 'TRUNCATE TABLE %s' % table
        cursor = self.cnxn.cursor()
        cursor.execute( query )
        cursor.commit()
        cursor.close()

    def exec_sp(self, sp_name):

        '''
        Executes the provided stored procedure

        :param str sp_name: The name of a Stored Procedure in this DB

        :return: Nothing atm...

        :rtype: None

        '''

        # can extend...https://stackoverflow.com/questions/28635671/using-sql-server-stored-procedures-from-python-pyodbc/42009222#42009222
        sp = 'EXEC  %s' % sp_name
        cursor = self.cnxn.cursor()
        cursor.execute( sp )
        cursor.commit()
        cursor.close()

    def exec_sql_file(self, sql_file_path, stmt_delim = ';'):

        '''
        Executes an SQL script with this connection

        :param str sql_file_path: The path to an SQL file.

        :param str stmt_delim: Statement deliminator in the script

        :return: Nothing atm...

        :rtype: None

        '''

        try:

            with open(sql_file_path, 'r') as sql_lines:
                sql_script = sql_lines.readlines()

            sql_script = ''.join(sql_script) # return to buffer

        except Exception as e: # not the best way to do this should check for valid types/paths first
            sql_script = sql_file_path

        for stmt in sql_script.split(stmt_delim):

            if len(stmt) == 0:
                continue

            with self.cnxn.cursor() as cur:
                cur.execute(stmt)
                cur.commit()


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
        if 'DELETE'   == sql[:6].upper() or \
           'UPDATE'   == sql[:6].upper() or \
           'INSERT'   == sql[:6].upper() or \
           'TRUNCATE' == sql[:8].upper() or \
           'ALTER'    == sql[:5].upper():

            cursor.commit()
            row_count = cursor.rowcount
            cursor.close()
            return row_count

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

    def insert_batch(self, resource, data, dt_format = '%Y%m%d', batch_size=DB_MAX_BATCH):

        '''
        Batch inserts the provided data to the provided resource

        :param str resource: db table/destination.

        :param list data: list of lists containt data elements to insert.

        :param int dt_format: Specify the format of Datetime's for downstream

        :param int batch_size: How many rows to insert in a single batch

        :return: The total number of rows inserted.

        :rtype: int

        '''

        if batch_size > DB_MAX_BATCH:
            batch_size = DB_MAX_BATCH


        if len(data) == 0:
            return 0

        # get values from dict data rows
        if type(data[0]) == dict:

            data = [list(row.values()) for row in data]

        db_lines = [] # (..row[0]..), (..row[1]..), ...
        for row in data:

            # all these maps and lambda's need to go.....

            # strings
            db_line = map(lambda x: x.replace( "'", "''") if type(x) == str else x, row) # add sql '' apostrophe in abbrevs

            db_line = map(lambda x: "'" + x + "'"  if type(x) == str else x, db_line)
            # None
            db_line = map(lambda x: 'NULL'  if x is None else x, db_line)

            # better below
            db_line = list(db_line)

            # bools/ints/dates oh my!!!
            for idx in range(0, len(db_line)):

                if type(db_line[idx]) == int or type(db_line[idx]) == Decimal:
                    db_line[idx] = str(db_line[idx])

                if type(db_line[idx]) == bool:
                   if not db_line[idx]:
                       db_line[idx] = '0'
                   else:
                       db_line[idx] = '1'

                if type(db_line[idx]) == datetime:
                        db_line[idx] = db_line[idx].strftime(dt_format)


            #print(list(db_line))
            db_line = ','.join(db_line) # create sql batch insert line
            db_line = '(' + db_line + ')'


            #print(db_line)

            db_lines.append(db_line)

        cursor = self.cnxn.cursor()

        db_insert = 'INSERT INTO %s VALUES' % resource

        start  = 0
        end    = batch_size
        inc    = batch_size
        stop   = len(db_lines)
        row_count = 0
        while start <= stop:

            db_values = ','.join(db_lines[start:end])
            query = db_insert + db_values
            cursor.execute( query )
            cursor.commit()
            if cursor.rowcount is not None:
                row_count += cursor.rowcount

            start += inc
            end   += inc
            #print('[DB][DEBUG]', str(start) + ':' +   str(end))

        cursor.close()

        return row_count

    def close(self):

        '''
        Close this connection to the DB

        :return: Closes this DB connection

        :rtype: None

        '''

        self.cnxn.close()

