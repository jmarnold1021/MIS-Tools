"""
The MIS Errors Module contains
functions generating sql from
mis error reports
"""

# native deps
import os
import json
import csv
import glob
from datetime import datetime

# lib deps
from . import mislog
from .db import DB
from . import misconfig

CONFIGS = misconfig.mis_load_config()
MIS_ERRORS_CONFIGS = CONFIGS['MIS_ERRORS']

err_log  = mislog.mis_console_logger('miserrors', MIS_ERRORS_CONFIGS['LOG_LEVEL'])

def _errors_parse_file_dict(err_path, headers=False, fill_empty=None, delim = ','):


    rows = []

    with open(err_path, encoding = 'utf8', newline='') as csvfile:

        err_reader = csv.DictReader(csvfile,
                                delimiter=delim,
                                quotechar='"',
                                skipinitialspace=True)

        for row in err_reader:

            rows.append({k:(elem.strip() if elem.strip() != '' else fill_empty)  for k, elem in row.items()})

    return rows

def sb_build_savelist(gi03):

    '''
    Build the SB Savelist from the final SB referential errors.

    :param str gi03: A single or list of DOD file paths to parse.

    :rtype: list

    '''

    query = """

        SELECT DISTINCT p.ID
        FROM PERSON p
        WHERE REPLACE(p.SSN, '-', '') IN %s
              OR
              ('D' + p.ID) IN %s
    """

    # should prob have some spec for the file name...but keeping here for now...
    SPEC = 'SB_savelist_errors.csv'
    error_files_root = MIS_ERRORS_CONFIGS['MIS_ERRORS_ROOT']
    root = os.path.join(error_files_root, 'SB', gi03, '**')

    err_data = []
    for sb_file in glob.iglob( root, recursive=True ):

        if os.path.basename(sb_file) == SPEC:

            err_data = _errors_parse_file_dict(sb_file)
            break

    sb00s = []
    for row in err_data:

        # going blist for now
        if row['File Type'].upper not in ['CB','XB','TX','SG','EB','SB']:

            curr_id = row['Data Dictionary Element Value']

            # not getting leading zeros in parse and trying to program at 430pm :(
            if curr_id is not None and \
                len(curr_id) != 9 and \
                curr_id[0] != 'D':
                curr_id = curr_id.rjust(9, '0')

            if curr_id is not None and \
               curr_id not in sb00s:
                sb00s.append(curr_id)

    print(len(sb00s))
    sb00s_filter = "('" + "','".join(sb00s) + "')"
    query = query % (sb00s_filter, sb00s_filter)

    db = DB(MIS_ERRORS_CONFIGS['SRC_DB_NAME'])
    #print(query)
    data = db.exec_query(query)
    return data
