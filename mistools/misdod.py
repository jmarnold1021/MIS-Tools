"""
The MIS Data On Demand Module contains
functions for exporting and parsing
Data On Demand CSV files
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
from . import misutil

LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )
DOD_MIS_SPEC_PATH = "%s/spec/mis_dod_spec.json" % LIB_ROOT
DOD_SCFF_SPEC_PATH = "%s/spec/mis_scff_spec.json" % LIB_ROOT
DOD_SCHEMA_PATH = "%s/schema/" % LIB_ROOT
DOD_SCHEMA_TEMPLATE = DOD_SCHEMA_PATH + 'dbo.L56_DOD_%s.Table.sql'


# read in specs for different report/s
with open(DOD_MIS_SPEC_PATH) as dod_spec_file:
    DOD_MIS_SPEC = json.load(dod_spec_file)

with open(DOD_SCFF_SPEC_PATH) as dod_spec_file:
    DOD_SCFF_SPEC = json.load(dod_spec_file)

CONFIGS = misconfig.mis_load_config()
MIS_DOD_CONFIGS = CONFIGS['MIS_DOD']

# possible configs/future globals
MIS_DOD_SRC_DT_FRMT = '%m%d%Y'
MIS_DOD_ADJ_DT_FRMT = '%Y%m%d' # better for sql etc..

# set up global lib logger
dod_log  = mislog.mis_console_logger('misdod', MIS_DOD_CONFIGS['LOG_LEVEL'])


# this just ensurse that if the headers have been updated aka added elements...
# then old dod reports get None fills for those new columns...
def _dod_fill_missing(report, data):

    dod_header = DOD_MIS_SPEC[report]["HEADERS"]

    if len(dod_header) > len(data[0]):

        for i in range(0, len(data)):

            if type(data[i]) == dict:

                keys = list(data.keys())
                missing_keys = list(dod_header) - list(keys)
                missing_dict = dict.fromkeys(missing_keys)
                data.update(missing_dict)

            elif type(data[i]) == list:

                data[i] = data[i] + ( (len(dod_header) - len(data[i])) * [None] )

    return data


def _dod_adj_dates(report, data):


    if report       not in DOD_MIS_SPEC or \
       "HEADERS"    not in DOD_MIS_SPEC[report] or \
       "DATE_CONVS" not in DOD_MIS_SPEC[report]:
       return data # nothing to do

    # dod provides wonky date formate for sql so setting it
    # to the same as the submissions format
    dod_date_convs  = DOD_MIS_SPEC[report]["DATE_CONVS"]
    dod_headers     = DOD_MIS_SPEC[report]["HEADERS"]

    if type(data[0]) != dict:

        dod_date_idx = []
        for attr in dod_date_convs:
            dod_date_idx.append(dod_headers.index(attr))
        dod_date_convs = dod_date_idx

    for row in data:

        for i in dod_date_convs:
            row[i] = datetime.strptime(row[i], MIS_DOD_SRC_DT_FRMT).strftime(MIS_DOD_ADJ_DT_FRMT)
    return data

def _dod_add_headers(report, data):
    # adds headers from specs to 2d arrays as top array
    dod_header = DOD_MIS_SPEC[report]["HEADERS"]

    return [dod_header] + data

# needs has seperate option for adding header
def _dod_parse_file(dod_paths, fill_empty=None, delim = '\t'):

    if type(dod_paths) != list:
        dod_paths = [dod_paths]


    dod_rows = []
    for dod_path in dod_paths:

        with open(dod_path, encoding = 'utf8', newline='') as csvfile:

            dod_reader = csv.reader(csvfile,
                                    delimiter=delim,
                                    quotechar='"',
                                    skipinitialspace=True)

            for row in dod_reader:
                dod_rows.append([elem.strip() if elem.strip() != '' else fill_empty for elem in row])

    return dod_rows

# needs report for headers/keys
def _dod_parse_file_dict(report, dod_paths, delim = '\t', fill_empty =None):

    if type(dod_paths) != list:
        dod_paths = [dod_paths]

    headers = None
    if report in DOD_MIS_SPEC and \
       "HEADERS" in DOD_MIS_SPEC[report]: # otherwise should get them from top row...see api docs for csv.DictReader
        headers = DOD_MIS_SPEC[report]['HEADERS']

    dod_rows = []
    for dod_path in dod_paths:

        with open(dod_path, encoding = 'utf8', newline='') as csvfile:

            dod_reader = csv.DictReader(csvfile, delimiter=delim,
                                        fieldnames = headers )

            for row in dod_reader:
                dod_rows.append({k:(elem.strip() if elem.strip() != '' else fill_empty)  for k, elem in row.items()})

    return dod_rows


def sx_dod_parse( gi03 = None, dict_read = False, headers = False, fill_empty = None):

    '''
    Parse Enrollment data from DOD files.

    :param str gi03: Pull only data for this GI03

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data defautls to None

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['SX']['FILENAME'])


    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found SX DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('SX', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('SX', data)
    data = _dod_adj_dates('SX', data)

    dod_log.info('Parsed %d files and %d rows for SX' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('SX', data)

    return data



def ss_dod_parse( gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student Success data from DOD files.

    :param str gi03: Pull only data for this GI03

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data defautls to None

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['SS']['FILENAME'])


    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found SS DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('SS', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('SS', data)
    data = _dod_adj_dates('SS', data)

    dod_log.info('Parsed %d files and %d rows for SS' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('SS', data)

    return data

def st_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student data from DOD files

    :param str gi03: Pull only data for this GI03

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['ST']['FILENAME'])


    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found ST DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('ST', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('ST', data)
    data = _dod_adj_dates('ST', data)

    dod_log.info('Parsed %d files and %d rows for ST' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('ST', data)

    return data

def xb_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Section data from DOD files

    :param str gi03: Pull only data for this GI03

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['XB']['FILENAME'])


    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found XB DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('XB', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('XB', data)
    data = _dod_adj_dates('XB', data)

    dod_log.info('Parsed %d files and %d rows for XB' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('XB', data)

    return data

def xf_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Session data from DOD files

    :param str gi03: Pull only data for this GI03

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['XF']['FILENAME'])


    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found XF DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('XF', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('XF', data)
    data = _dod_adj_dates('XF', data)

    dod_log.info('Parsed %d files and %d rows for XF' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('XF', data)

    return data

def xe_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Session data from DOD files

    :param str gi03: Pull only data for this GI03

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['XE']['FILENAME'])


    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found XE DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('XE', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('XE', data)
    data = _dod_adj_dates('XE', data)

    dod_log.info('Parsed %d files and %d rows for XF' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('XE', data)

    return data

def cb_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Course data from DOD files

    :param str gi03: Gi03 of CB data to pull.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['CB']['FILENAME'])


    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found CB DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('CB', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('CB', data)
    data = _dod_adj_dates('CB', data)

    dod_log.info('Parsed %d files and %d rows for CB' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('CB', data)

    return data

def se_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse EOPS data from DOD files

    :param str gi03: Gi03 of EOPS data to pull.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['SE']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found SE DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('SE', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('SE', data)
    data = _dod_adj_dates('SE', data)

    dod_log.info('Parsed %d files and %d rows for SE' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('SE', data)

    return data

def eb_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Employee Demographic data from DOD files

    :param str gi03: Gi03 of EB data to pull.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['EB']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found EB DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('EB', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('EB', data)
    data = _dod_adj_dates('EB', data)

    dod_log.info('Parsed %d files and %d rows for EB' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('EB', data)

    return data

def ej_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Employee Assignment data from DOD files

    :param str gi03: Gi03 of EJ Data to Pull

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['EJ']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found EJ DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('EJ', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('EJ', data)
    data = _dod_adj_dates('EJ', data)

    dod_log.info('Parsed %d files and %d rows for EJ' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('EJ', data)

    return data

def sc_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student Cal-Works data from DOD files

    :param str gi03: Gi03 of Student Cal-Works data to pull.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, DOD_MIS_SPEC['SC']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, '/**/', recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found SC DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('SC', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('SC', data)
    data = _dod_adj_dates('SC', data)

    dod_log.info('Parsed %d files and %d rows for SC' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('SC', data)

    return data

def cw_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Cal-Works Work data from DOD files

    :param str gi03: Gi03 of Cal-Works Work data to pull

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['CW']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found CW DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('CW', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('CW', data)
    data = _dod_adj_dates('CW', data)

    dod_log.info('Parsed %d files and %d rows for CW' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('CW', data)

    return data

def sd_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student Disabilities data from DOD files

    :param str gi03: List of paths or path to a DOD SD Report.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['SD']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found SD DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('SD', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('SD', data)
    data = _dod_adj_dates('SD', data)

    dod_log.info('Parsed %d files and %d rows for SD' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('SD', data)

    return data

def sg_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student Groups data from DOD files

    :param str gi03: Gi03 of SG data to pull.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['SG']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found SG DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('SG', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('SG', data)
    data = _dod_adj_dates('SG', data)

    dod_log.info('Parsed %d files and %d rows for SG' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('SG', data)

    return data

def sf_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student Financial Aid data from DOD files

    :param str gi03: Gi03 of SF data to pull.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['SF']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found SF DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('SF', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('SF', data)
    data = _dod_adj_dates('SF', data)

    dod_log.info('Parsed %d files and %d rows for SF' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('SF', data)

    return data

def fa_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Financial Aid Award data from DOD files

    :param list gi03: Gi03 of FA data to pull.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['FA']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found FA DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('FA', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('FA', data)
    data = _dod_adj_dates('FA', data)

    dod_log.info('Parsed %d files and %d rows for FA' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('FA', data)

    return data

def sp_dod_parse(gi03=None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student Programs data from DOD files

    :param str gi03: Gi03 of sp data to pull

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['SP']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        if gi03 and gi03 not in os.path.basename(dod_file):
            continue

        dod_files.append(dod_file)
        dod_log.debug('Found SP DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('SP', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('SP', data)
    data = _dod_adj_dates('SP', data)

    dod_log.info('Parsed %d files and %d rows for SP' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('SP', data)

    return data

def sb_dod_parse(dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student Basic data from DOD files

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['SB']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        dod_files.append(dod_file)
        dod_log.debug('Found SB DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('SB', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('SB', data)
    data = _dod_adj_dates('SB', data)

    dod_log.info('Parsed %d files and %d rows for SB' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('SB', data)

    return data

def fr_dod_parse(dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Firsts Ref data from DOD files

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['FR']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        dod_files.append(dod_file)
        dod_log.debug('Found FR DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('FR', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('FR', data)
    data = _dod_adj_dates('FR', data)

    dod_log.info('Parsed %d files and %d rows for FR' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('FR', data)

    return data


def stuid_dod_parse(dict_read=False, headers=False, fill_empty=None):

    '''
    Parse Student Ref data from DOD files

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC['STUID']['FILENAME'])

    dod_files = []
    for dod_file in glob.iglob( root, recursive=True ):

        dod_files.append(dod_file)
        dod_log.debug('Found STUID DOD file - %s' % dod_file)

    if dict_read:

        data = _dod_parse_file_dict('STUID', dod_files, fill_empty = fill_empty)

    else:

        data = _dod_parse_file( dod_files, fill_empty = fill_empty)

    data = _dod_fill_missing('STUID', data)
    data = _dod_adj_dates('STUID', data)

    dod_log.info('Parsed %d files and %d rows for STUID' % (len(dod_files), len(data)))


    if not dict_read and headers: # could combine with parse similar to parse_dict
        data = _dod_add_headers('STUID', data)

    return data


def ref_dod_update_db(data, report = None, gi03 = None, full = None):

    '''
    Update any DOD data referential data in the Database

    :param object data: Data to upload, if dict key is used as report, if array report is required

    :param str report: Only parse files for the provided report/s

    :param str gi03: Only parse files for this gi03 in each provided report

    :param str full: Update table schema and upload provided Data

    :rtype: int

    '''

    if type(data) != dict:

        if report:

            data_tmp = data
            data = {}
            data[report] = data_tmp

        else:

            dod_log.critical('Data not in proper format.')
            return 0


    db = DB('ODS')

    total_rows = 0
    total_tables = 0
    for report in data:

        table = 'L56_DOD_%s' % report
        total_rows += len(data[report])
        total_tables += 1

        if total_rows == 0:
            continue

        if full:

            schema_path = DOD_SCHEMA_TEMPLATE % report
            dod_log.info('Updating schema for %s' % report)
            #db.exec_sql_file(schema_path, stmt_delim = 'GO\n')

        elif gi03:

            dod_log.info('Deleting %s from %s' % (gi03, report))
            #db.exec_query("DELETE FROM %s WHERE GI03 = '%s'" % (table, gi03))

        else:

            dod_log.info('Clearing %s' % report)
            #db.truncate(table)

        table = 'L56_DOD_%s' % report
        dod_log.info('Inserting %d rows into %s' % (len(data[report]), report))

        try:
            #db.insert_batch( table, data[report] )
            dod_log.info('Refresh Complete...%d rows inserted into %d tables' % (total_rows, total_tables))
        except Exception as e:
            dod_log.warning("Error occured during bacth insert %s data. Continuing upload..." % report)

    db.close()

    return total_rows

def ref_dod_parse(report = None, gi03 = None, dict_read=False, headers=False, fill_empty=None):

    '''
    Parse any DOD data referential data, :orangebold:`This function can litterally pull the entire DOD db into memory`

    :param str report: only parse files for the provided report

    :param str gi03: Only parse files for this gi03

    :param bool diff: Compare the new DOD Ref data with the current in the DB. (Requires report, gi03) args. Will still return the reported data with.

    :param bool dict_read: return data as a dict with headers for keys

    :param bool headers: include headers

    :param str fill_empty: filler string for missing data

    :rtype: list

    '''

    ref_files_root = MIS_DOD_CONFIGS['REF_FILES_ROOT']

    rep_list = [rep for rep in DOD_MIS_SPEC]
    if report:
      rep_list = [report.upper()]

    dod_data = {}
    for report in rep_list:

        dod_log.info('Started Parsing %s' % report)

        root = os.path.join(ref_files_root, '/**/', DOD_MIS_SPEC[report]['FILENAME'])
        dod_log.debug('Glob pattern - %s' % root)

        cnt = 0
        num_rows = 0
        dod_data[report] = []
        for dod_file in glob.iglob( root, recursive=True ):

            if gi03 and (gi03 not in os.path.basename(dod_file) or 'Non_Term' in dod_file) :
                continue

            dod_log.debug('Found DOD files - %s' % dod_file)
            cnt += 1

            if dict_read:

                data = _dod_parse_file_dict(report, dod_file, fill_empty = fill_empty)
                data = _dod_fill_missing(report, data)
                data = _dod_adj_dates(report, data)
                num_rows += len(data)
                dod_data[report] += data
                continue

            data = _dod_parse_file( dod_file, fill_empty = fill_empty)
            data = _dod_fill_missing(report, data)
            data = _dod_adj_dates(report, data)
            num_rows += len(data)
            dod_data[report] += data


        dod_log.info('Parsed %d files and %d rows for %s' % (cnt, num_rows, report))

        if report and gi03 and diff: # do a diff...before headers option is easier...

            _dod_diff(dod_data[report], report, gi03)

        if not dict_read and headers:

            dod_data[report] = _dod_add_headers(report, dod_data[report])


    return dod_data


def scff_dod_update_db(data, gi03 = None, full = None, safe = False):
    '''
    Update any DOD data referential data in the Database

    :param object data: Data to upload, if dict key is used as report, if array report is required

    :param str report: Only parse files for the provided report/s

    :param str gi03: Only parse files for this gi03 in each provided report

    :param str full: Update table schema and upload provided Data

    :rtype: int

    '''

    if safe:
        dod_log.info('Will clear and insert %d rows in SCFF' % len(data))
        return 0

    db = DB('ODS')

    table = 'L56_DOD_SCFF'

    if full:

        schema_path = DOD_SCHEMA_TEMPLATE % 'SCFF'
        dod_log.info('Updating schema for SCFF')
        db.exec_sql_file(schema_path, stmt_delim = 'GO\n')

    elif gi03:

        dod_log.info('Deleting %s from SCFF' % gi03)
        db.exec_query("DELETE FROM %s WHERE GI03 = '%s'" % (table, gi03))
    else:

        dod_log.info('Clearing %s' % report)
        db.truncate(table)

    dod_log.info('Inserting %d rows into SCFF' % len(data))
    cnt = db.insert_batch( table, data)


    db.close()

    return len(data)

def scff_dod_parse(gi03=None):

    '''
    Parse all DOD SCFF Pre-Allocation data

    :param str gi03: The GI03 of the reports to pull

    :rtype: list

    '''

    pa_path_root = MIS_DOD_CONFIGS['PRE_ALLOC_FILES_ROOT']

    scff_filenames = DOD_SCFF_SPEC['SCFF']['FILENAMES']
    scff_headers = DOD_SCFF_SPEC['SCFF']['HEADERS']

    scff_gi03_file_paths = {}
    for  filename in scff_filenames:

        glob_path =  pa_path_root + filename

        for file in glob.glob(glob_path):


            scff_gi03 = os.path.dirname(file)[-3:]
            if scff_gi03 not in scff_gi03_file_paths:
                scff_gi03_file_paths[scff_gi03] = []

            if gi03 and gi03 != scff_gi03:
                continue

            scff_gi03_file_paths[scff_gi03].append(file)


    scff_data = []
    for scff_gi03 in scff_gi03_file_paths:

        scff_file_paths = scff_gi03_file_paths[scff_gi03]
        scff_data_build = {}

        for scff_file in scff_file_paths:

            report = os.path.basename(scff_file).split('_')[0]
            data = _dod_parse_file_dict(None, scff_file, delim='|')

            dod_log.info('Parsing %d rows from %s for %s' % (len(data), report, scff_gi03))

            for row in data:

                if row['STUDENT_ID'] not in scff_data_build:

                    scff_data_build[row['STUDENT_ID']] = dict(zip(scff_headers, \
                                                        len(scff_headers) * [None]))

                    scff_data_build[row['STUDENT_ID']]['SB00'] = row['STUDENT_ID']
                    scff_data_build[row['STUDENT_ID']]['GI03'] = scff_gi03

                if len(row.keys()) == 2:

                    scff_data_build[row['STUDENT_ID']][report] = 'Y'

                else:

                    for key in row:

                        scff_data_build[row['STUDENT_ID']][report] = 'Y'

                        if row[key] == 'Y':

                            scff_data_build[row['STUDENT_ID']][report + '_' + key] = 'Y'

        scff_data += list(scff_data_build.values())

    return scff_data


