
"""
The MIS Data On Demand IPEDS Module contains
functions for exporting and parsing
Data On Demand IPEDS CSV files
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
DOD_IPEDS_SPEC_PATH = "%s/spec/mis_ipeds_spec.json" % LIB_ROOT
with open(DOD_IPEDS_SPEC_PATH) as dod_spec_file:
    DOD_IPEDS_SPEC = json.load(dod_spec_file)

CONFIGS = misconfig.mis_load_config()
MIS_IPEDS_CONFIGS = CONFIGS['MIS_IPEDS']

# set up global lib logger
ipeds_log  = mislog.mis_console_logger('misipeds', MIS_IPEDS_CONFIGS['LOG_LEVEL'])

def _ipeds_adj_year(data):

   for row in data:

       sy = row['SURVEY_YEAR'].split('-')
       del row['SURVEY_YEAR']
       row['YEAR'] = sy[0]
       row['LATTER_YEAR'] = sy[0][0:2] + sy[1]

   return data

# needs report for headers/keys
def _ipeds_parse_file_dict(ipeds_paths, delim = ',', fill_empty =None):

    if type(ipeds_paths) != list:
        ipeds_paths = [ipeds_paths]

    ipeds_rows = []
    for ipeds_path in ipeds_paths:

        with open(ipeds_path, encoding = 'utf8', newline='') as csvfile:

            ipeds_reader = csv.DictReader(csvfile, delimiter=delim,
                                          fieldnames = None )

            for row in ipeds_reader:
                ipeds_rows.append({k:(elem.strip() if elem.strip() != '' else fill_empty)  for k, elem in row.items()})

    return ipeds_rows

def hr_ipeds_parse(ipeds_file_path, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse IPEDS grads rates from IPEDS DOD files

    :param int trail_year: The trailing year of the Grad file being parsed.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ipeds_data = _dod_parse_file_dict( None, ipeds_file_path,  delim = ',')


    return ipeds_data

def ef_ipeds_parse(later_year, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse IPEDS Fall Enrollment Rates DOD files

    :param int trail_year: The trailing year of the Grad file being parsed.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_IPEDS_CONFIGS['ACC_FILES_ROOT']

    root = os.path.join(ref_files_root, DOD_IPEDS_SPEC['EF']['FILENAME'])
    for dod_file in glob.iglob( root, recursive=True ):
        if str(later_year)[-2:] in os.path.basename(dod_file) and \
           str(later_year-1) in os.path.basename(dod_file):

           dod_data = _dod_parse_file_dict(None, dod_file,  delim = ',')
           dod_data = _dod_ipeds_adj_year(dod_data)

           return dod_data

def e12_ipeds_parse(latter_year=None):

    '''
    Parse IPEDS 12 Month Rates DOD files

    :param int latter_year: The latter year of the Grad file being parsed.

    :rtype: list

    '''
    # This can be configured...
    ipeds_files_root = MIS_IPEDS_CONFIGS['ACC_FILES_ROOT']

    # the file names are specified by dod so you would have to rename them in fs
    # and spec or just keep them as is ;)..............2 moves or 0.............
    root = os.path.join(ipeds_files_root, DOD_IPEDS_SPEC['E12']['FILENAME'])
    ipeds_data = []
    for ipeds_file in glob.iglob( root, recursive=True ):

        if latter_year and \
           str(latter_year)[-2:] in os.path.basename(ipeds_file) and \
           str(latter_year-1) in os.path.basename(ipeds_file):

             data = _ipeds_parse_file_dict(ipeds_file)
             data = _ipeds_adj_year(data)
             ipeds_data += data

             return ipeds_data # one year

        data = _ipeds_parse_file_dict(ipeds_file)
        data = _ipeds_adj_year(data)
        ipeds_data += data

    return ipeds_data # all years


def grads_ipeds_parse(later_year, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse IPEDS grads rates from IPEDS DOD files

    :param int trail_year: The trailing year of the Grad file being parsed.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''
    grad_rates_file_name = 'IPEDS_GRADRATES _221_%s-%s.txt' % \
                           (str(later_year - 1), str(later_year)[-2:])
    dod_file_path = MIS_IPEDS_CONFIGS['ACC_IPEDS_PATH_TEMPLATE'] % \
                    ('Graduation_Rates', grad_rates_file_name)

    dod_data = _dod_parse_file(dod_file_path,  delim = ',')


    return dod_data

def grads_200_ipeds_parse(later_year, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse IPEDS grads 200 rates from IPEDS DOD files

    :param int trail_year: The trailing year of the Grad file being parsed.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    grad_rates_file_name = 'IPEDS_GRDRATE200_221_%s-%s.txt' % \
                           (str(later_year - 1), str(later_year)[-2:])
    dod_file_path = MIS_IPEDS_CONFIGS['ACC_IPEDS_PATH_TEMPLATE'] % \
                    ('Graduation_Rates', grad_rates_file_name)

    dod_data = _dod_parse_file( dod_file_path,  delim = ',')


    return dod_data

