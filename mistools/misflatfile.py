"""
The MIS Flat File Module contains
functions for exporting and parsing
MIS flat files(.DAT)..
"""

import os
import pyodbc
import json
from datetime import datetime
from dateutil import parser # for string dates with no format...

# lib deps
from .lib import ffparser
from . import mislog

#### All ####

# Pull in the MIS DED specification
LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )
DED_MIS_SPEC_PATH = "%s/spec/mis_ded_spec.json" % LIB_ROOT

with open(DED_MIS_SPEC_PATH) as mis_spec_file:
    DED_MIS_SPEC = json.load(mis_spec_file)

# pull in configs
CONFIGS_PATH = "%s/../configs/configs.json" % LIB_ROOT # currently from lib root...
with open(CONFIGS_PATH) as configs:
    CONFIGS = json.load(configs)

misff_log  = mislog.mis_console_logger('misflatfile', CONFIGS['MIS_FLAT_FILE']['LOG_LEVEL'])

#### Export ####

# DB configs

CONNECTION_STRING = r'Driver=SQL Server;Server=%s;Database=%s;Trusted_Connection=yes;' % \
                    (CONFIGS['DB']['COLLEAGUE']['SERVER_NAME'],
                     CONFIGS['DB']['COLLEAGUE']['DB_NAME'])

# MIS FF EXPORT CONFIGS
MIS_FF_EXPORT_ROOT = CONFIGS['MIS_FLAT_FILE']['MIS_FF_EXPORT_ROOT']
TXT_FILE_LINE ="tx220%s%s%su22%s%sdat"
DAT_FILE_TEMPLATE = r'U22%s%s.DAT'

def _build_sql_g(report, gi03):

    schema = DED_MIS_SPEC[report]['SCHEMA']

    if 'GI03' not in schema:
        misff_log.critical('No GI03 Attribute Provided in Spec for report %s' % report)
        return "SELECT 'No GI03 Attribute Provided in Spec for report %s'" % report

    gi03_attr = schema['GI03']

    if 'MIS_SRC_TABLE' not in schema:
        misff_log.critical('No Source Table Provided in Spec for report %s' % report)
        return "SELECT 'No Source Table Provided in Spec for report %s'" % report

    table = schema['MIS_SRC_TABLE']

    flag_filter = ''
    if 'RPT_FLAG' in schema:
        rpt_flag = schema['RPT_FLAG']
        flag_filter = "      AND " + rpt_flag + " = 1"



    return "SELECT *" + \
           "\nFROM "  + table + \
           "\nWHERE " + gi03_attr + ' = ' + "'" + gi03 + "'" + \
           flag_filter

def _exec_query_g(sql):

    cnxn = pyodbc.connect(CONNECTION_STRING)
    cursor = cnxn.cursor()
    cursor.execute(sql)

    data = [row for row in cursor.fetchall()]
    if len(data) != 0:
        columns = [column[0] for column in cursor.description]

    cursor.close()
    cnxn.close()

    # why make downstream care aabout pyodc rows?
    return [dict(zip(columns, elem)) for elem in data]

def _write_dat_file_g(report, rows, out_file, mode = 'w'):

    # data will need headers

    schema  = DED_MIS_SPEC[report]['SCHEMA']
    formats = DED_MIS_SPEC[report]['FORMAT_G']

    # if enum type pre sort...
    for attr, f in formats.items():
        if 'TYPE' in f and f['TYPE'] == 'ENUM' \
           and 'ORDER' in f:
               rows = sorted(rows, key=lambda k: [k[schema[skey]] for skey in f['ORDER']] ) # cray line here...sorts by variable keys


    ff_acc = []
    enum_inc = 0
    curr_enum = ''
    for row in rows:

        print(row)
        ff_line_acc = ''

        for attr, f in formats.items():
            print(attr)
            if 'TYPE' in f and f['TYPE'] == 'CONST' \
               and 'VALUE' in f:

                   ff_line_acc += f['VALUE']

            elif 'TYPE' in f and f['TYPE'] == 'STR' \
                 and 'START' in f and 'LENGTH' in f:

                tok = row[schema[attr]][formats[attr]['START']:formats[attr]['LENGTH'] + 1]
                if 'PADDING' in f and 'JUSTIFIED' in f:

                    pad = formats[attr]['PADDING'] * formats[attr]['LENGTH']

                    if f['JUSTIFIED'] == 'LEFT':

                        tok = (tok + pad)[:formats[attr]['LENGTH']]

                    elif f['JUSTIFIED'] == 'RIGHT':

                        tok = (pad + tok)[-(formats[attr]['LENGTH']):]

                ff_line_acc += tok

            elif 'TYPE' in f and f['TYPE'] == 'DATE' \
                 and 'FORMAT' in f:

                tok = row[schema[attr]]

                if type(tok) == str:
                    tok = parser.parse(tok)

                ff_line_acc += tok.strftime(formats[attr]['FORMAT'])

            elif 'TYPE' in f and f['TYPE'] == 'ENUM' \
                 and 'START' in f and 'OVER' in f:


                     if row[schema[f['OVER']]] == curr_enum:
                         enum_inc += 1
                         ff_line_acc += str(f['START'] + enum_inc)
                     else:
                         enum_inc = 0
                         ff_line_acc += str(f['START'])
                         curr_enum = row[schema[f['OVER']]]


            print(ff_line_acc)
        ff_acc.append(ff_line_acc)
        break

    print(ff_acc)


def _build_sql(report, gi03):

    attrs     = DED_MIS_SPEC[report]['FORMAT']
    gi03_attr = DED_MIS_SPEC[report]['FORMAT']['GI03']
    table     = DED_MIS_SPEC[report]['MIS_SRC_TABLE']

    # EB uses a different prefix CAHR not CAST...
    flag_filter = "\n      AND CAST_" + report + "_RPT_FLAG = 1"
    if report == 'EB':
        flag_filter = "\n      AND CAHR_" + report + "_RPT_FLAG = 1"

    return "SELECT "  + ' +\n       '.join(attrs.values()) + \
           "\nFROM "  + table + \
           "\nWHERE " + gi03_attr + ' = ' + "'" + gi03 + "'" + \
           flag_filter

def _exec_query(sql):

    cnxn = pyodbc.connect(CONNECTION_STRING)
    cursor = cnxn.cursor()
    cursor.execute(sql)
    data = [row[0] for row in cursor.fetchall()]
    cursor.close()
    cnxn.close()

    # why make downstream care aabout pyodc rows?
    return data

def _write_dat_file(rows, out_file, mode = 'w'):

    os.makedirs(os.path.dirname(out_file), exist_ok=True)

    with open(out_file, mode) as f:

        for idx, row in enumerate(rows):

            if row is None: # as the exports are done and normalized this will be unnecessary.
                # rows with null have a null value that was not converted
                # to the specs auto fill value, 430 is sb length aka long long man
                f.write( ('!' * 430) + '\n')
                misff_log.critical('Empty record found at line %d' , (idx + 1))
                continue
            f.write( row + '\n' )

    return len(rows) # return num rows for txt

def _build_txt_file(row_count, report, gi03, out_file):

    # builds a text file line
    def _build_txt_line(row_count, report, gi03):

        # 5041 => '    5041' with len 8
        row_count_str = ( (' ' * 8) + str(row_count) )[-8:]

        return TXT_FILE_LINE % (gi03,
                                report.lower(),
                                row_count_str,
                                gi03,
                                report.lower())

    new_rpt_line = [_build_txt_line(row_count, report, gi03)]

    if os.path.isfile(out_file):

        with open(out_file, 'r') as f:

            txt_lines = f.read().splitlines()

        rpt_txt_lines = txt_lines[:-1]

        idx = 0
        for line in rpt_txt_lines:

            if report.lower() == line[8:10]:

                if row_count == int(line[10:18]):

                    return # no update needed

                break

            idx += 1

        if idx < len(rpt_txt_lines):

            rpt_txt_lines[idx] = new_rpt_line[0]

        else:

            rpt_txt_lines += new_rpt_line
    else:

         rpt_txt_lines = new_rpt_line


    contact_info = CONFIGS['MIS_FLAT_FILE']['AUTHOR']['LAST_NAME'] + (' ' * 8) + \
                   CONFIGS['MIS_FLAT_FILE']['AUTHOR']['FIRST_NAME'] + (' ' * 7) + \
                   CONFIGS['MIS_FLAT_FILE']['AUTHOR']['PHONE_NUMBER']

    tx_txt_line = _build_txt_line(len(rpt_txt_lines) + 1, 'tx', gi03) + \
                  contact_info

    with open(out_file, 'w') as f:

        f.write('\n'.join(rpt_txt_lines))
        f.write( '\n' + tx_txt_line )


# MIS Export Interface
def sx_mis_export(gi03, sql_only = False):

    '''
    Export Enrollemnt Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    # build sql from spec
    sql = _build_sql('SX', gi03)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SX', gi03, out_file)

    return sql


def sy_mis_export(gi03, sql_only = False):

    '''
    Export Student Prior Learning to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    # build sql from spec
    sql = _build_sql('SY', gi03)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SY')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SY', gi03, out_file)

    return sql


def ss_mis_export(gi03, sql_only = False):

    '''
    Export Student Success Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    # build sql from spec
    sql = _build_sql('SS', gi03)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SS')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SS', gi03, out_file)

    return sql



def sd_mis_export(gi03, sql_only = False):

    '''
    Export Student Disablility Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    # build sql from spec
    sql = _build_sql('SD', gi03)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SD')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SD', gi03, out_file)

    return sql



def sc_mis_export(gi03, sql_only = False):

    '''
    Export Student Calworks/Calworks Work Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    SC_SQL_DELIM = '\n--\n'
    sql_list = []

    # build sql from spec
    sc_sql = _build_sql('SC', gi03)
    sql_list.append(sc_sql)

    # build sql from spec
    cw_sql = _build_sql('CW', gi03)
    sql_list.append(cw_sql)

    if sql_only:
        return SC_SQL_DELIM.join(sql_list)

    # SC export
    rows = _exec_query(sc_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SC')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SC', gi03, out_file)

    # CW export
    rows = _exec_query(cw_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'CW')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'CW', gi03, out_file)

    return SC_SQL_DELIM.join(sql_list)


def sb_mis_export(gi03, sql_only = False):

    '''
    Export Student Basic Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    # build sql from spec
    sql = _build_sql('SB', gi03)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SB')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SB', gi03, out_file)

    return sql


def sg_mis_export(gi03, sql_only = False):

    '''
    Export Student Groups Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    # build sql from spec
    sql = _build_sql('SG', gi03)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SG')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SG', gi03, out_file)

    return sql


def cb_mis_export(gi03, sql_only = False):

    '''
    Export Course Basic Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''


    # build sql from spec
    sql = _build_sql('CB', gi03)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'CB')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'CB', gi03, out_file)

    return sql


def sv_mis_export(gi03, sql_only = False):


    '''
    Export Student VTEA Data to a Flat File(:redbold:`Has not been Implemented`)

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: :redbold:`empty string`

    :rtype: str

    '''
    return ''
    # build sql from spec
    #sql = _build_sql('SV', gi03)

    #if sql_only:
    #    return sql

    #rows = _exec_query(sql)

    #dat_file = DAT_FILE_TEMPLATE % (gi03, 'SV')
    #out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    #row_count = _write_dat_file(rows, out_file)

    #txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    #out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    #_build_txt_file(row_count, 'SV', gi03, out_file)

    #return sql


def eb_mis_export(gi03, sql_only = False):

    '''
    Export Employee Demographic Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    # build sql from spec
    sql = _build_sql('EB', gi03)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'EB')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'EB', gi03, out_file)

    return sql


def xb_mis_export(gi03, sql_only = False):

    '''
    Export Section/Session/Assignment Data to a Flat File(.DAT)
           :greenbold:`UNION ALL maintains the order of the union.`

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql query used to perform the export, In order XB/XF/XE,

    :rtype: str

    '''

    XB_SQL_UNION = '\nUNION ALL\n'
    sql_list = []

    # XB
    xb_sql = _build_sql('XB', gi03)
    sql_list.append(xb_sql)

    # XF
    xf_sql = _build_sql('XF', gi03)
    sql_list.append(xf_sql)

    # XE
    xe_sql = _build_sql('XE', gi03)
    sql_list.append(xe_sql)

    if sql_only:
        return XB_SQL_UNION.join(sql_list)

    # XB
    rows = _exec_query(xb_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'XB')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    xb_row_count = _write_dat_file(rows, out_file)


    # XF
    rows = _exec_query(xf_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'XB')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    xf_row_count = _write_dat_file(rows, out_file, mode = 'a') # append


    # XE
    rows = _exec_query(xe_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'XB')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    xe_row_count = _write_dat_file(rows, out_file, mode = 'a') # append

    # get combined row count...
    row_count = xb_row_count + xf_row_count + xe_row_count

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'XB', gi03, out_file)

    return XB_SQL_UNION.join(sql_list)

def se_mis_export(gi03, sql_only = False):
    '''
    Export Student EOPS Data(:redbold:`Has not been Implemented`)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: :redbold:`empty string`

    :rtype: string

    '''

    return ''

def sp_mis_export(gi03, sql_only = False):

    '''
    Export Student Programs Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    # build sql from spec
    sql = _build_sql('SP', gi03)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SP')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SP', gi03, out_file)

    return sql

def sp_mis_export_g(gi03):


    # build sql from spec
    sql = _build_sql_g('SP', gi03)

    rows = _exec_query_g(sql)

    #print(rows[0])

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SP')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file_g('SP', rows, out_file)
    return
    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SP', gi03, out_file)

    return sql

def sf_mis_export(gi03, sql_only = False):
    '''
    Export Student Financial Aid Data

    :param str gi03: Term to export data from

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    SF_SQL_DELIM = '\n--\n'
    sql_list = []

    sf_sql = _build_sql('SF', gi03)
    sql_list.append(sf_sql)

    fa_sql = _build_sql('FA', gi03)
    sql_list.append(fa_sql)

    if sql_only:
        return SF_SQL_DELIM.join(sql_list)

    rows = _exec_query(sf_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SF')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'SF', gi03, out_file)

    rows = _exec_query(fa_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'FA')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(MIS_FF_EXPORT_ROOT, gi03, txt_file)

    _build_txt_file(row_count, 'FA', gi03, out_file)

    return SF_SQL_DELIM.join(sql_list)


def aa_mis_export(gi03, sql_only = False):
    '''
    Export Adult Edcation Assement Data(:redbold:`Has not been Implemented`)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: :redbold:`empty string`

    :rtype: str

    '''

    return ''

def sl_mis_export(gi03, sql_only = False):
    '''
    Export Student Placement Data(:redbold:`Has not been Implemented`)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: :redbold:`empty string`

    :rtype: str

    '''

    return ''



#### Parse ####

# adjust postions spec from 1 cnt to 0 cnt
for report in DED_MIS_SPEC:

    spec = DED_MIS_SPEC[report]['POSITION']

    for key in spec:

        if type(spec[key]) == str:
            continue

        spec[key][0] = spec[key][0] - 1
        spec[key][1] = spec[key][1] - 1


# MIS specific parse options
FF_OPTIONS = {
    "fill_empty"  : None # this could vary highly so kept in db standard aka null see constants in DED spec of deleted elements this would set the fill value for all elements in the report.
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
        xb_mis_data['XF'] = _mis_add_headers('XF', xb_mis_data['XF'])
        xb_mis_data['XE'] = _mis_add_headers('XE', xb_mis_data['XE'])

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

def cw_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student Calworks Work data from DAT files

    :param str mis_file_path: path to cw dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('CW', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('CW', mis_data)

    return mis_data

def sg_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student Groups data from DAT files

    :param str mis_file_path: path to sg dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('SG', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('SG', mis_data)

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

def cc_mis_parse(mis_file_path, headers = False):
    '''
    Parse Student Calendar data from DAT files

    :param str mis_file_path: path to se dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('CC', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('CC', mis_data)

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

def ej_mis_parse(mis_file_path, headers = False):
    '''
    Parse Employee Assignment data from DAT files

    :param str mis_file_path: path to ej dat file

    :param bool headers: include headers

    :rtype: list

    '''

    mis_data = _mis_parse_files('EJ', mis_file_path)

    if headers:
        mis_data = _mis_add_headers('EJ', mis_data)

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


