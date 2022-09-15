"""
The MIS Export Library contains
functions for exporting MIS data
to flat files(.DAT) or Generating
the SQL query that performs the export.
"""

import json
import os
import pyodbc


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


CONFIGS_PATH = "%s/../configs/configs.json" % LIB_ROOT
with open(CONFIGS_PATH) as configs:
    CONFIGS = json.load(configs)

CONNECTION_STRING = r'Driver=SQL Server;Server=%s;Database=%s;Trusted_Connection=yes;' % \
                    (CONFIGS['DB']['COLLEAGUE']['SERVER_NAME'],
                     CONFIGS['DB']['COLLEAGUE']['DB_NAME'])

TXT_FILE_LINE ="tx220%s%s%su22%s%sdat"

DAT_FILE_TEMPLATE = r'U22%s%s.DAT'


def _build_sql(gi03, attrs, gi03_attr, table):

    return "SELECT "  + ' +\n       '.join(attrs.values()) + \
           "\nFROM "  + table + \
           "\nWHERE " + gi03_attr + ' = ' + "'" + gi03 + "'"


def _exec_query(sql):

    cnxn = pyodbc.connect(CONNECTION_STRING)
    cursor = cnxn.cursor()
    cursor.execute(sql)

    # why make downstream care aabout pyodc rows?
    return [row[0] for row in cursor.fetchall()]

def _write_dat_file(rows, out_file, mode = 'w'):

    with open(out_file, mode) as f:

        for row in rows:

            if row is None:
                # rows with null have a null value that was not converted
                # to the specs auto fill value, 430 is sb length aka long long man
                f.write( ('!' * 430) + '\n')
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


    contact_info = CONFIGS['MIS']['AUTHOR']['LAST_NAME'] + (' ' * 8) + \
                   CONFIGS['MIS']['AUTHOR']['FIRST_NAME'] + (' ' * 7) + \
                   CONFIGS['MIS']['AUTHOR']['PHONE_NUMBER']

    tx_txt_line = _build_txt_line(len(rpt_txt_lines) + 1, 'tx', gi03) + \
                  contact_info

    with open(out_file, 'w') as f:

        f.write('\n'.join(rpt_txt_lines))
        f.write( '\n' + tx_txt_line )


# MIS Export Interface
def sx_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Enrollemnt Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['SX']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['SX']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['SX']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SX')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'SX', gi03, out_file)

    return sql


def sy_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Student Prior Learning to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['SY']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['SY']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['SY']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SY')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'SY', gi03, out_file)

    return sql


def ss_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Student Success Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['SS']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['SS']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['SS']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SS')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'SS', gi03, out_file)

    return sql



def sd_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Student Disablility Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['SD']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['SD']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['SD']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SD')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'SD', gi03, out_file)

    return sql



def sc_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Student Calworks Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['SC']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['SC']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['SC']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SC')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'SC', gi03, out_file)

    return sql


def cw_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Calworks Positions Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['CW']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['CW']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['CW']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'CW')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'CW', gi03, out_file)

    return sql


def sb_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Student Basic Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['SB']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['SB']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['SB']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SB')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'SB', gi03, out_file)

    return sql


def sg_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Student Groups Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['SG']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['SG']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['SG']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SG')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'SG', gi03, out_file)

    return sql


def cb_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Course Basic Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['CB']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['CB']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['CB']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'CB')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'CB', gi03, out_file)

    return sql


def sv_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Student VTEA Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['SV']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['SV']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['SV']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SV')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'SV', gi03, out_file)

    return sql


def eb_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Employee Demographic Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['EB']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['EB']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['EB']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'EB')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'EB', gi03, out_file)

    return sql


def xb_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Section/Session/Assignment Data to a Flat File(.DAT)
           :greenbold:`UNION ALL maintains the order of the union.`

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql query used to perform the export, In order XB/XF/XE,

    :rtype: str

    '''

    XB_SQL_UNION = '\nUNION ALL\n'
    sql_list = []

    # XB
    attrs     = DED_MIS_SPEC['XB']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['XB']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['XB']['CAL_GOLD_TABLE']

    # build sql from spec
    xb_sql = _build_sql(gi03, attrs, gi03_attr, table)
    sql_list.append(xb_sql)

    # XF
    attrs     = DED_MIS_SPEC['XF']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['XF']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['XF']['CAL_GOLD_TABLE']

    # build sql from spec
    xf_sql = _build_sql(gi03, attrs, gi03_attr, table)
    sql_list.append(xf_sql)

    # XE
    attrs     = DED_MIS_SPEC['XE']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['XE']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['XE']['CAL_GOLD_TABLE']

    # build sql from spec
    xe_sql = _build_sql(gi03, attrs, gi03_attr, table)
    sql_list.append(xe_sql)

    if sql_only:
        return XB_SQL_UNION.join(sql_list)

    # XB
    rows = _exec_query(xb_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'XB')
    out_file = os.path.join(out_file_path, dat_file)

    xb_row_count = _write_dat_file(rows, out_file)


    # XF
    rows = _exec_query(xf_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'XB')
    out_file = os.path.join(out_file_path, dat_file)

    xf_row_count = _write_dat_file(rows, out_file, mode = 'a') # append


    # XE
    rows = _exec_query(xe_sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'XB')
    out_file = os.path.join(out_file_path, dat_file)

    xe_row_count = _write_dat_file(rows, out_file, mode = 'a') # append


    row_count = xb_row_count + xf_row_count + xe_row_count

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'XB', gi03, out_file)

    return XB_SQL_UNION.join(sql_list)

def se_mis_export(gi03, out_file_path, sql_only = False):
    '''
    Export Student EOPS Data(:redbold:`Has not been Implemented`)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: :redbold:`empty string`

    :rtype: string

    '''

    return ''

def sp_mis_export(gi03, out_file_path, sql_only = False):

    '''
    Export Student Programs Data to a Flat File(.DAT)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: The sql used to perform the export

    :rtype: str

    '''

    attrs     = DED_MIS_SPEC['SP']['CAL_GOLD_ATTRS']
    gi03_attr = DED_MIS_SPEC['SP']['CAL_GOLD_ATTRS']['GI03']
    table     = DED_MIS_SPEC['SP']['CAL_GOLD_TABLE']

    # build sql from spec
    sql = _build_sql(gi03, attrs, gi03_attr, table)

    if sql_only:
        return sql

    rows = _exec_query(sql)

    dat_file = DAT_FILE_TEMPLATE % (gi03, 'SP')
    out_file = os.path.join(out_file_path, dat_file)

    row_count = _write_dat_file(rows, out_file)

    txt_file = DAT_FILE_TEMPLATE % (gi03, 'TX')
    out_file = os.path.join(out_file_path, txt_file)

    _build_txt_file(row_count, 'SP', gi03, out_file)

    return sql

def aa_mis_export(gi03, out_file_path, sql_only = False):
    '''
    Export Adult Edcation Assement Data(:redbold:`Has not been Implemented`)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: :redbold:`empty string`

    :rtype: string

    '''

    return ''

def sl_mis_export(gi03, out_file_path, sql_only = False):
    '''
    Export Student Placement Data(:redbold:`Has not been Implemented`)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: :redbold:`empty string`

    :rtype: string

    '''

    return ''

def sf_mis_export(gi03, out_file_path, sql_only = False):
    '''
    Export Student Financial Aid Data(:redbold:`Has not been Implemented`)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: :redbold:`empty string`

    :rtype: string

    '''

    return ''

def fa_mis_export(gi03, out_file_path, sql_only = False):
    '''
    Export Student Financial Aid Award Data(:redbold:`Has not been Implemented`)

    :param str gi03: Term to export data from

    :param str out_file_path: Path where .DAT file should be written

    :param bool sql_only: Only return the generated sql, defaults to False

    :return: :redbold:`empty string`

    :rtype: string

    '''

    return ''
