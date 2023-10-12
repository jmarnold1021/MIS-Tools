"""
The MIS RPT Module contains
functions generating sql that
helps update and analyze MIS RPT
tables
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
#
CONFIGS = misconfig.mis_load_config()
MIS_RPT_CONFIGS = CONFIGS['MIS_RPT']


## set up global lib logger
rpt_log  = mislog.mis_console_logger('misrpt', MIS_RPT_CONFIGS['LOG_LEVEL'])

RPT_SCHEMA_PATH = "%s/schema/" % LIB_ROOT
RPT_SCHEMA_FILENAME = 'dbo.%s_%s_RPT.Table.sql'

RPT_ADJ_DT_FRMT = "%Y-%m-%d"

def _fetch_upstream_data(prefix, report):

    db = DB(MIS_RPT_CONFIGS['SRC_DB_NAME'])
    sql = """
          SELECT *
          FROM %s_%s_RPT
          WHERE %s_%s_RPT_FLAG = 1
          """ % (prefix, report, prefix, report)

    data = db.exec_query(sql)
    db.close()

    return data

def _read_rpt_sql_schema(prefix, report):

    rpt_schema_path = (RPT_SCHEMA_PATH + RPT_SCHEMA_FILENAME) % (prefix, report)
    with open(rpt_schema_path) as rpt_schema_file:
        schema_lines = rpt_schema_file.readlines()

    return schema_lines

def _update_table_name(prefix, report, schema_lines):

    src_name = '[dbo].[%s_%s_RPT]' % (prefix, report)
    dst_name = '[dbo].[L56_%s_%s_RPT]' % (prefix, report)

    ods_lines = []
    for line in schema_lines:

        if src_name in line:

            ods_line = line.replace(src_name, dst_name)
            ods_lines.append(ods_line)
            continue

        ods_lines.append(line)

    return ''.join(ods_lines)

def _refresh_schema(sql_script):

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    db.exec_sql_file(sql_script, stmt_delim = 'GO\n')
    db.close()

def mis_ods_cb_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for CB in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "CB"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script   = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)

    return ods_script

def mis_ods_cb_refresh_data(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for CB in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "CB"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data)
    db.close()

    return num_rows

def mis_ods_xb_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for XB in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "XB"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_xb_refresh_data(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for XB in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "XB"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data)
    db.close()

    return num_rows

def mis_ods_xf_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for XF in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "XF"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_xf_refresh_data(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for XF in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "XF"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data)
    db.close()

    return num_rows

def mis_ods_xe_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for XE in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "XE"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_xe_refresh_data(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for XE in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "XE"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data)
    db.close()

    return num_rows

def mis_ods_sx_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for SX in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "SX"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_sx_refresh_data():

    '''
    Builds/Executes the SQL Sccript for SX in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "SX"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data)
    db.close()

    return num_rows

def mis_ods_eb_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for EB in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAHR"
    report = "EB"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_eb_refresh_data():

    '''
    Builds/Executes the SQL Sccript for EB in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAHR"
    report    = "EB"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data, dt_format = RPT_ADJ_DT_FRMT)
    db.close()

    return num_rows

def mis_rpt_ods_ej_refresh(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for EJ in the LTCC_MIS(:redbold:1Has not been Implemented`)

    :param bool sql_only: Only return the Script

    :return: :redbold:`empty string`

    :rtype: str

    '''

    #prefix = "CAHR"
    #report = "EJ"

    #schema_lines = _read_rpt_sql_schema(prefix, report)
    #ods_script = _update_table_name(prefix, report, schema_lines)

    #if sql_only:
    #    return ods_script

    #_refresh_schema(ods_script)
    #return ods_script
    return ''

def mis_ods_sb_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for SB in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "SB"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_sb_refresh_data():

    '''
    Builds/Executes the SQL Sccript for SB in the LTCC_MIS

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "SB"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data, dt_format = RPT_ADJ_DT_FRMT)
    db.close()

    return num_rows

def mis_ods_ss_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for SS in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "SS"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_ss_refresh_data():

    '''
    Builds/Executes the SQL Sccript for SB in the LTCC_MIS

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "SS"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data, dt_format = RPT_ADJ_DT_FRMT)
    db.close()

    return num_rows

def mis_ods_sc_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for SC in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "SC"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_sc_refresh_data():

    '''
    Builds/Executes the SQL Sccript for SB in the LTCC_MIS

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "SC"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data, dt_format = RPT_ADJ_DT_FRMT)
    db.close()

    return num_rows

def mis_ods_cw_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for CW in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "CW"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_cw_refresh_data():

    '''
    Builds/Executes the SQL Sccript for SB in the LTCC_MIS

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "CW"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data, dt_format = RPT_ADJ_DT_FRMT)
    db.close()

    return num_rows

def mis_ods_sd_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for SD in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "SD"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_sd_refresh_data():

    '''
    Builds/Executes the SQL Sccript for SB in the LTCC_MIS

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "SD"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data, dt_format = RPT_ADJ_DT_FRMT)
    db.close()

    return num_rows

def mis_ods_sy_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for SY in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "SY"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_sy_refresh_data():

    '''
    Builds/Executes the SQL Sccript for SB in the LTCC_MIS

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "SY"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data, dt_format = RPT_ADJ_DT_FRMT)
    db.close()

    return num_rows

def mis_ods_sg_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for SG in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "SG"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_sg_refresh_data():

    '''
    Builds/Executes the SQL Sccript for SP in the LTCC_MIS

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "SG"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data, dt_format = RPT_ADJ_DT_FRMT)
    db.close()

    return num_rows

def mis_ods_sp_refresh_schema(sql_only = False):

    '''
    Builds/Executes the SQL Sccript for SP in the LTCC_MIS

    :param bool sql_only: Only return the Script

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix = "CAST"
    report = "SP"

    schema_lines = _read_rpt_sql_schema(prefix, report)
    ods_script = _update_table_name(prefix, report, schema_lines)

    if sql_only:
        return ods_script

    _refresh_schema(ods_script)
    return ods_script

def mis_ods_sp_refresh_data():

    '''
    Builds/Executes the SQL Sccript for SP in the LTCC_MIS

    :return: The sql script used to maintain the schema

    :rtype: str

    '''

    prefix    = "CAST"
    report    = "SP"
    dst_table = 'L56_%s_%s_RPT' % (prefix, report)

    data = _fetch_upstream_data(prefix, report)

    db = DB(MIS_RPT_CONFIGS['DST_DB_NAME'])
    num_rows = db.insert_batch(dst_table, data, dt_format = RPT_ADJ_DT_FRMT)
    db.close()

    return num_rows

