"""
The MIS Data On Demand Module contains
functions for exporting and parsing
Data On Demand CSV files
"""

import os
import json
import csv

from .lib import ffparser

LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )
DOD_MIS_SPEC_PATH = "%s/spec/mis_dod_spec.json" % LIB_ROOT

with open(DOD_MIS_SPEC_PATH) as dod_spec_file:
    DOD_MIS_SPEC = json.load(dod_spec_file)


def _dod_add_headers(report, data):

    dod_header = DOD_MIS_SPEC[report]

    return [dod_header] + data

def _dod_parse_file(report, dod_path, fill_empty=None, delim = '\t'):

    dod_rows = []
    with open(dod_path, newline='') as csvfile:

        dod_reader = csv.reader(csvfile,
                                delimiter=delim,
                                quotechar='"',
                                skipinitialspace=True)

        for row in dod_reader:
            dod_rows.append([elem.strip() if elem.strip() != '' else fill_empty for elem in row])

    return dod_rows

def _dod_parse_file_dict(report, dod_path, delim = '\t', fill_empty =None):

    dod_rows = []
    with open(dod_path, newline='') as csvfile:

        dod_reader = csv.DictReader(csvfile, delimiter=delim,
                                    fieldnames = DOD_MIS_SPEC[report])

        for row in dod_reader:
            dod_rows.append({k:(elem.strip() if elem.strip() != '' else fill_empty)  for k, elem in row.items()})

    return dod_rows

def sx_dod_parse(dod_file_path, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Enrollment data from DOD files

    :param str dod_file_path: path to sx dod file

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    if dict_read:
        dod_data = _dod_parse_file_dict('SX', dod_file_path, fill_empty = fill_empty)
        return dod_data

    dod_data = _dod_parse_file('SX', dod_file_path, fill_empty = fill_empty)

    if headers:
        dod_data = _dod_add_headers('SX', dod_data)

    return dod_data

def st_dod_parse(dod_file_path, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student data from DOD files

    :param str dod_file_path: path to st dod file

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    if dict_read:
        dod_data = _dod_parse_file_dict('ST', dod_file_path, fill_empty = fill_empty)
        return dod_data

    dod_data = _dod_parse_file('ST', dod_file_path, fill_empty = fill_empty)

    if headers:
        dod_data = _dod_add_headers('ST', dod_data)

    return dod_data

def xb_dod_parse(dod_file_path, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Section data from DOD files

    :param str dod_file_path: path to st dod file

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    if dict_read:
        dod_data = _dod_parse_file_dict('XB', dod_file_path, fill_empty = fill_empty)
        return dod_data

    dod_data = _dod_parse_file('XB', dod_file_path, fill_empty = fill_empty)

    if headers:
        dod_data = _dod_add_headers('XB', dod_data)

    return dod_data

def ccccoid_dod_parse(dod_file_path, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student Ref data from DOD files

    :param str dod_file_path: path to sx dod file

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    if dict_read:
        dod_data = _dod_parse_file_dict('CCCCOID', dod_file_path, fill_empty = fill_empty)
        return dod_data

    dod_data = _dod_parse_file('CCCCOID', dod_file_path, fill_empty = fill_empty)

    if headers:
        dod_data = _dod_add_headers('ID', dod_data)

    return dod_data
