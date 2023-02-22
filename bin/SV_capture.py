'''
Script to capture SV Data very hack
'''
import os
import pandas as pd
import pyodbc
import json
#import numpy as np

# XL56_VATEA contains one record per student

BIN = os.path.dirname( os.path.realpath(__file__) )
CONNECTION_STRING_TEMPLATE = r'Driver=SQL Server;Server=%s;Database=%s;Trusted_Connection=yes;'
LOG_FILE = BIN + '/../mistools/logs/SV_capture_logs'
LOGS = []

# DB configs
CONFIGS_PATH = "%s/../configs/configs.json" % BIN

def main():

    # load db configs
    with open(CONFIGS_PATH) as configs:
        CONFIGS = json.load(configs)

    server_name = CONFIGS['DB']['COLLEAGUE']['SERVER_NAME']
    db_name     = CONFIGS['DB']['COLLEAGUE']['DB_NAME']

    # create db connection obj
    cnxn = pyodbc.connect(CONNECTION_STRING_TEMPLATE % \
                           ( server_name, db_name ))

    # load response source data
    vatea_resp = pd.read_excel("//ltcc-app/MIS/MIS_Source_Data/SV/Confidential Student Survey.xlsx")

    # create a username column from emails in response dataframe to join on for ids
    vatea_resp['OEE_USERNAME'] = vatea_resp['Email'].apply(lambda email: email.split('@')[0])


    # get ids from usernames off emails with this table and join to response
    org_entity_env = pd.read_sql('SELECT OEE_USERNAME, OEE_RESOURCE FROM ORG_ENTITY_ENV', cnxn)
    vatea_resp = pd.merge(vatea_resp, org_entity_env, on = 'OEE_USERNAME', how = 'inner')


    # vatea_resp has everything needed now.
    # convert to match the table in db...
    # No -> None
    # Panda Null -> None
    # Yes -> Y
    xl56_vatea_update = pd.DataFrame(columns=['XVATEA_ID',
                                              'XVATEA_SINGLE_PARENT',
                                              'XVATEA_DISPLACED_HOMEMAKER',
                                              'XVATEA_HOUSEHOLD_SIZE',
                                              'XVATEA_HOUSEHOLD_INCOME_CODE',
                                              'XVATEA_MIGRANT_WORKER',
                                              'XVATEA_DATE_COLLECTED',
                                              'XVATEA_CW_TANF_AFDC',
                                              'XVATEA_CW_TANF_AFDC_SOURCE',
                                              'XVATEA_OTHER_ECON_DISADVANT',
                                              'XVATEA_OTHER_ECON_DIS_SOURCE',
                                              'XVATEA_SSI',
                                              'XVATEA_SSI_SOURCE',
                                              'XVATEA_GA',
                                              'XVATEA_GA_SOURCE'])

    xl56_vatea_update['XVATEA_ID'] = vatea_resp['OEE_RESOURCE'] # student id

    # these columns have long question names so use iloc each row converts the question answer to the exsiting value in XL56_VATEA
    xl56_vatea_update['XVATEA_SINGLE_PARENT'] = vatea_resp.iloc[:,5]\
                                                .apply(lambda ans: None if (pd.isnull(ans) or ans == 'No') else 'Y')

    xl56_vatea_update['XVATEA_DISPLACED_HOMEMAKER'] = vatea_resp.iloc[:,6]\
                                                      .apply(lambda ans: None if (pd.isnull(ans) or ans == 'No') else 'Y')

    xl56_vatea_update['XVATEA_HOUSEHOLD_SIZE'] = vatea_resp.iloc[:,12]\
                                                .apply(lambda ans: None if (pd.isna(ans)) else str(int(ans)))

    xl56_vatea_update['XVATEA_HOUSEHOLD_INCOME_CODE'] = vatea_resp.iloc[:,13]\
                                                        .apply(lambda ans: None if (pd.isnull(ans)) else ans[0])

    xl56_vatea_update['XVATEA_MIGRANT_WORKER'] = vatea_resp.iloc[:,11]\
                                                 .apply(lambda ans: None if (pd.isnull(ans) or ans == 'No') else 'Y')

    #xl56_vatea_update['XVATEA_DATE_COLLECTED'] = vatea_resp['Completion time']\
    #                                             .dt.strptime('%Y-%m-%d 00:00:00:000') # another way but returns a string not datetime internal dt obj has no strptime...
    xl56_vatea_update['XVATEA_DATE_COLLECTED'] = pd.to_datetime(vatea_resp['Completion time'], format = '%Y-%m-%d 00:00:00:000')


    xl56_vatea_update['XVATEA_CW_TANF_AFDC'] = vatea_resp.iloc[:,7]\
                                               .apply(lambda ans: None if (pd.isnull(ans) or ans == 'No') else 'Y')
    xl56_vatea_update['XVATEA_CW_TANF_AFDC_SOURCE'] = 'S'


    xl56_vatea_update['XVATEA_OTHER_ECON_DISADVANT'] = vatea_resp.iloc[:,10]\
                                                       .apply(lambda ans: None if (pd.isnull(ans) or ans == 'No') else 'Y')
    xl56_vatea_update['XVATEA_OTHER_ECON_DIS_SOURCE'] = 'S'


    xl56_vatea_update['XVATEA_SSI'] = vatea_resp.iloc[:,8]\
                                      .apply(lambda ans: None if (pd.isnull(ans) or ans == 'No') else 'Y')
    xl56_vatea_update['XVATEA_SSI_SOURCE'] = 'S'


    xl56_vatea_update['XVATEA_GA'] = vatea_resp.iloc[:,9]\
                                    .apply(lambda ans: None if (pd.isnull(ans) or ans == 'No') else 'Y')
    xl56_vatea_update['XVATEA_GA_SOURCE'] = 'S'

    # SQL Templates
    insert_sql = 'INSERT INTO XL56_VATEA_TMP VALUES (' + ','.join(('?' * len(list(xl56_vatea_update.columns)))) + ')'

    update_sql = 'UPDATE XL56_VATEA_TMP SET ' + ', '.join(list(map(lambda x: x + ' = ?', list(xl56_vatea_update.columns)[1:]))) + \
                 ' WHERE ' + list(xl56_vatea_update.columns)[0] + ' = ?  AND ' + list(xl56_vatea_update.columns)[6] +' < ?'

    # execute sql for each row in the vatea resp info
    # check if we have any for id
    # otherwise update if collection date is newer
    cursor = cnxn.cursor()
    for index, row in xl56_vatea_update.iterrows():

        try:
            cursor.execute(insert_sql, list(row))
            cnxn.commit() # insert

            if cursor.rowcount == 1:
                LOGS.append("'%s', VATEA Data Inserted successfully" % row[0])

        except pyodbc.IntegrityError as pyodbc_err:

            if pyodbc_err.args[0] == '23000': # primary key exception

                cursor.execute(update_sql, list(row[1:]) + [row[0]] + [row[6]]) # id and date on end for where, list() needs iterable so single elements use [] ...
                cnxn.commit() # update

                if cursor.rowcount == 1:
                    LOGS.append("'%s', VATEA Updated Successfully" % row[0])
                else:
                    LOGS.append("'%s', VATEA not updated check date!!!!!!!!!" % row[0])
            else:

                LOGS.append("'%s', Unknown pyodbc.IntegrityError see below" % row[0])
                LOGS.append(repr(e)) # execution will not stop for exception

        except Exception as e:

            LOGS.append("'%s', Unknown Error see below" % row[0])
            LOGS.append(repr(e)) # execution will not stop for exception

    cursor.close()
    cnxn.close()

    with open(LOG_FILE, 'w') as f:
        f.write('\n'.join(LOGS))




if __name__ == "__main__":
    main()
