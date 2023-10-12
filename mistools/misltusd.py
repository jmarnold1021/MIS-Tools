"""
The MIS LTUSD Module contains
functions for working with the
Data we are provided by LTUSD.
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
MIS_LTUSD_CONFIGS = CONFIGS['MIS_LTUSD']
ltusd_log  = mislog.mis_console_logger('misnsc', MIS_LTUSD_CONFIGS['LOG_LEVEL'])

def _ltusd_parse_file_dict(ltusd_path, fill_empty=None):

    rows = []

    with open(ltusd_path, encoding = 'utf8', newline='') as csvfile:

        nsc_reader = csv.DictReader(csvfile, quotechar='"')

        for row in nsc_reader:
            rows.append({k:(elem.strip() if elem.strip() != '' else fill_empty)  for k, elem in row.items()})

    return rows

def mis_ltusd_grad_parse(ltusd_grad_path):

    '''
    Parse LTUSD Graduate Results

    :param str ltusd_grad_path: The new LTUSD Grads

    :rtype: list

    '''

    ltusd_log.info("Parsing newest results from %s" % ltusd_grad_path)
    rows = _ltusd_parse_file_dict(ltusd_grad_path)

    return rows

def mis_ltusd_grads_update_db(data):

    '''
    Appends LTUSD Graduate Results

    :param list data: The new LTUSD Grads data

    :rtype: int

    '''

    db = DB('ODS')
    num_rows = db.insert_batch('L56_LtusdGraduates', data)
    db.close()
    return num_rows
