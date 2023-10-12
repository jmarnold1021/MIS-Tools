"""
The MIS NSC Module contains
functions with the National
Student Clearinghouse Data
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


LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )
MIS_NSC_SPEC_PATH = "%s/spec/mis_nsc_spec.json" % LIB_ROOT

with open(MIS_NSC_SPEC_PATH) as mis_spec_file:
    MIS_NSC_SPEC = json.load(mis_spec_file)


# set up global lib logger

CONFIGS = misconfig.mis_load_config()
MIS_NSC_CONFIGS = CONFIGS['MIS_NSC']

nsc_log  = mislog.mis_console_logger('misnsc', MIS_NSC_CONFIGS['LOG_LEVEL'])

NSC_ST_FILENAME="*DETLRPT_*_import_file.csv" # this is a specification...

def _nsc_parse_file(nsc_path, headers=False):


    rows = []

    with open(nsc_path, encoding = 'utf8', newline='') as csvfile:

        nsc_reader = csv.reader(csvfile,
                                quotechar='"',
                                skipinitialspace=True)

        for row in nsc_reader:
            rows.append(row)

    return rows

def _nsc_parse_file_dict(nsc_path, fill_empty=None):

    rows = []

    with open(nsc_path, encoding = 'utf8', newline='') as csvfile:

        nsc_reader = csv.DictReader(csvfile, quotechar='"')

        for row in nsc_reader:
            rows.append({k:(elem.strip() if elem.strip() != '' else fill_empty)  for k, elem in row.items()})

    return rows

def mis_ltcc_st_results_parse():

    '''
    Parse NSC LTCC Student Tracker Results

    :param str term: term to parse results for

    :rtype: list

    '''

    archive = MIS_NSC_CONFIGS["STUDENT_TRACKER_LTCC"] + '/**/'

    root = os.path.join(archive, NSC_ST_FILENAME)

    # get newest results file from ltcc archive.
    new_results = None
    newest_ctime = 0
    for res_file in glob.iglob( root, recursive=True ):

        if os.stat(res_file).st_ctime > newest_ctime:
            new_results = res_file
            newest_ctime = os.stat(res_file).st_ctime

    nsc_log.info("Parsing newest results from %s" % new_results)
    rows = _nsc_parse_file_dict(new_results)

    return rows

def mis_ltcc_st_results_update_db(data):


    db = DB('ODS')
    db.truncate('L56_NscDetailFileStage')
    num_rows = db.insert_batch('L56_NscDetailFileStage', data)
    db.close()

    return num_rows

def mis_ltusd_st_results_parse():

    '''
    Parse NSC LTUSD Student Tracker Results

    :param str term: term to parse results for

    :rtype: list

    '''

    archive = MIS_NSC_CONFIGS["STUDENT_TRACKER_LTUSD"] + '/**/'

    root = os.path.join(archive, NSC_ST_FILENAME)

    # get newest results file from ltusd archive.
    new_results = None
    newest_ctime = 0
    for res_file in glob.iglob( root, recursive=True ):

        if os.stat(res_file).st_ctime > newest_ctime:
            new_results = res_file
            newest_ctime = os.stat(res_file).st_ctime

    nsc_log.info("Parsing newest results from %s" % new_results)
    rows = _nsc_parse_file_dict(new_results)

    return rows

def mis_ltusd_st_results_update_db(data):


    db = DB('ODS')
    db.truncate('L56_LtusdNscDetailFileStage')
    num_rows = db.insert_batch('L56_LtusdNscDetailFileStage', data)
    db.close()

    return num_rows


def mis_st_exec_adams_sp():


    db = DB('ODS')
    db.exec_sp('dbo.L56_IMPORT_STUDENT_TRACKER')
    db.close()
    return num_rows
