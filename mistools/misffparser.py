'''
The MIS Flat File Parser contains
functions for converting flat files into
2D arrays which can easily be translated
to pandas dataframes for db requests
'''

import json
import os

from .lib import ffparser

# Pull in the MIS DED specification
LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )
DED_MIS_SPEC_PATH = "%s/spec/mis_spec.json" % LIB_ROOT


with open(DED_MIS_SPEC_PATH) as mis_spec_file:
    DED_MIS_SPEC = json.load(mis_spec_file)


# adjust postions spec from 1 cnt to 0 cnt
for report in DED_MIS_SPEC:

    spec = DED_MIS_SPEC[report]['POSITION']

    for key in spec:

        spec[key][0] = spec[key][0] - 1
        spec[key][1] = spec[key][1] - 1



# MIS specific parse options
FF_OPTIONS = {
    "fill_empty"  : "NA" # this could vary highly
}


def _mis_add_headers(report, data):

    mis_spec = DED_MIS_SPEC[report]['POSITION']

    return [list(mis_spec.keys())] + data


def _mis_parse_files(report, mis_file_path):

    mis_spec = DED_MIS_SPEC[report]['POSITION']

    mis_data = ffparser.parse_files(mis_spec.values(), \
                                    mis_file_path, \
                                    FF_OPTIONS)

    return mis_data


def _mis_parse_lines(report, mis_ff_lines):

    mis_spec = DED_MIS_SPEC[report]['POSITION']

    mis_data = ffparser.parse_lines(mis_spec.values(), \
                                    mis_ff_lines, \
                                    FF_OPTIONS)

    return mis_data


def _xb_mis_split_ff(xb_file_path):

    # split file objs
    xb_ff_data = {

        "XB": [],
        "XF": [],
        "XE": []
    }

    if not isinstance(xb_file_path, list):
        xb_file_path = [xb_file_path]

    for path in xb_file_path:

        # validate paths!!!!!
        with open( path ) as file:

            line = file.readline()

            while line:

                if line[0:2] == "XB":
                    xb_ff_data['XB'].append(line)

                if line[0:2] == "XF":
                    xb_ff_data['XF'].append(line)

                if line[0:2] == "XE":
                    xb_ff_data['XE'].append(line)

                line = file.readline()

    return xb_ff_data


# MIS FF Parse Interface

def sb_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student Basic data from DAT files

    :param str mis_file_path: path to sb dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SB', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SB', mis_data)

    return mis_data


def cb_mis_parse(mis_file_path, headers = False):
    '''
    Parse Course data from DAT files

    :param str mis_file_path: path to cb dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('CB', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('CB', mis_data)

    return mis_data


def xb_mis_parse(xb_mis_file_path, headers = False):
    '''
    Parse Section/Session/Assignment data from DAT files

    :param str xb_mis_file_path: path to xb dat file

    :param bool headers: include headers

    :rtype: list

    '''

    xb_mis_data = _xb_mis_split_ff(xb_mis_file_path)

    xb_mis_data['XB'] = _mis_parse_lines('XB', xb_mis_data['XB'])
    xb_mis_data['XF'] = _mis_parse_lines('XF', xb_mis_data['XF'])
    xb_mis_data['XE'] = _mis_parse_lines('XE', xb_mis_data['XE'])

    if headers:
        xb_mis_data['XB'] = _mis_add_headers('XB', xb_mis_data['XB'])
        xb_mis_data['XF'] = _mis_add_headers('XE', xb_mis_data['XF'])
        xb_mis_data['XE'] = _mis_add_headers('XF', xb_mis_data['XE'])


    return xb_mis_data


def sc_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student Calworks data from DAT files

    :param str mis_file_path: path to sc dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SC', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SC', mis_data)

    return mis_data


def sx_mis_parse(mis_file_path, headers = False):
    '''
    Parse Enrollment data from DAT files

    :param str mis_file_path: path to sx dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SX', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SX', mis_data)

    return mis_data

def sy_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student SY data from DAT files

    :param str mis_file_path: path to sy dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SY', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SY', mis_data)

    return mis_data


def ss_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student Success data from DAT files

    :param str mis_file_path: path to ss dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SS', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SS', mis_data)

    return mis_data

def sd_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student Disability data from DAT files

    :param str mis_file_path: path to sd dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SD', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SD', mis_data)

    return mis_data

def sv_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student VTEA data from DAT files

    :param str mis_file_path: path to sv dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SV', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SV', mis_data)

    return mis_data

def se_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student EOPS data from DAT files

    :param str mis_file_path: path to se dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SE', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SE', mis_data)

    return mis_data

def eb_mis_parse(mis_file_path, headers = False):
    '''
    Parse Employee Demographic data from DAT files

    :param str mis_file_path: path to eb dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('EB', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('EB', mis_data)

    return mis_data


# ANNUAL
def sp_mis_parse(mis_file_path, headers = False):

    '''
    Parse Student SP data from DAT files

    :param str mis_file_path: path to sp dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SP', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SP', mis_data)

    return mis_data


def sf_mis_parse(mis_file_path, headers = False):

    '''
    Parse Student SF data from DAT files

    :param str mis_file_path: path to sf dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SF', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SF', mis_data)

    return mis_data


def fa_mis_parse(mis_file_path, headers = False):

    '''
    Parse Student FA data from DAT files

    :param str mis_file_path: path to fa dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('FA', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('FA', mis_data)

    return mis_data

