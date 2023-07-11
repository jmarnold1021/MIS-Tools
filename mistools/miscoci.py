
"""
Tools for Retrieving COCI Data from https://coci2.ccctechcenter.org/

"""

# native deps
import os
import json
import csv
import glob
from datetime import datetime
import requests # I forget if this is third party

# lib deps
from . import mislog
from .db import DB


LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )

# DB configs
CONFIGS_PATH = "%s/../configs/configs.json" % LIB_ROOT
with open(CONFIGS_PATH) as configs:
    CONFIGS = json.load(configs)

MIS_COCI_CONFIGS = CONFIGS['MIS_COCI']

# set up global lib logger
coci_log  = mislog.mis_console_logger('miscoci', MIS_COCI_CONFIGS['LOG_LEVEL'])

MIS_COCI_COURSES_URL = "https://coci2.ccctechcenter.org/courses/excel?college_filter[]=LAKE TAHOE"
MIS_COCI_PROGRAMS_URL = "https://coci2.ccctechcenter.org/programs/excel?college_filter[]=LAKE TAHOE"

MIS_COCI_SRC_DT_FRMT = '%Y-%m-%d'
MIS_COCI_ADJ_DT_FRMT = '%Y%m%d' # better for sql etc..
MIS_COCI_DEFAULT_DATE = '1908-08-08' # this is the default that DOD provides...so ccccco default...

def mis_coci_courses_parse():

    '''
    Parse Course data from Curriculum Inventory(COCI)

    :return: The 2d array of coci data

    :rtype: list

    '''

    r = requests.get(MIS_COCI_COURSES_URL)

    if r.status_code != 200:
        coci_log.critical('Error fetching COCI Course Data: code %d' % r.status_code)
        return

    x = csv.reader(r.text.split('\n')[1:]) # no header usually malformed...
    data = []

    for row in x:

        if len(row) == 0:
            continue

        row_adj = [None if elem == '' else elem for elem in row]
        row_adj[25] = datetime.strptime(row_adj[25], MIS_COCI_SRC_DT_FRMT).strftime(MIS_COCI_ADJ_DT_FRMT)

        data.append(row_adj)

    return data

def mis_coci_courses_update_db(data):

    db = DB('ODS')
    db.truncate('L56_COCI_COURSES')
    num_rows = db.insert_batch('L56_COCI_COURSES', data)
    db.close()
    return num_rows

def mis_coci_programs_parse():

    '''
    Parse Program data from Curriculum Inventory(COCI)

    :return: The 2d array of coci data

    :rtype: list

    '''

    r = requests.get(MIS_COCI_PROGRAMS_URL)

    if r.status_code != 200:
        coci_log.critical('Error fetching COCI Course Data: code %d' % r.status_code)
        return

    x = csv.reader(r.text.split('\n')[1:]) # no header usually malformed...
    data = []

    for row in x:

        if len(row) == 0:
            continue

        row_adj = [None if elem == '' else elem for elem in row]

        if row_adj[8] is None:
            row_adj[8] = MIS_COCI_DEFAULT_DATE

        row_adj[8] = datetime.strptime(row_adj[8], MIS_COCI_SRC_DT_FRMT).strftime(MIS_COCI_ADJ_DT_FRMT)

        data.append(row_adj)

    return data

def mis_coci_programs_update_db(data):

    db = DB('ODS')
    db.truncate('L56_COCI_PROGRAMS')
    num_rows = db.insert_batch('L56_COCI_PROGRAMS', data)
    db.close()
    return num_rows
