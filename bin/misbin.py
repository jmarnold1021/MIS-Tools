# native deps
import os
import sys
import logging
import glob
import json
from datetime import datetime
from datetime import timedelta

# build deps
import pkg_resources  # part of setuptools...

# third-party
import click          # cli dependancy...

# local deps
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append("%s/../../MIS-Tools" % SCRIPT_DIR)

from mistools    import misflatfile
from mistools    import misdod
from mistools    import mislog
from mistools    import miscoci
from mistools    import misrpt
from mistools    import misnsc
from mistools.db import DB

@click.group(name='bin')
def bin():
    pass

@bin.command(name='mis_version', help='List the currently installed version of MIS-Tools.')
def mis_version():

    mis_log = mislog.mis_console_logger('mis_version', 'INFO')

    local_version = None
    version       = None

    try: # nice for dev...an checking version upateds happen

        with open('%s/../version.json' % SCRIPT_DIR) as version_file:
            local_version = json.load(version_file)['version']

    except FileNotFoundError as e:

        pass #... no local version don't really need to show this...


    try:

        version = pkg_resources.require("mistools")[0].version # pulls version from package insalled package

    except pkg_resources.DistributionNotFound as e:

        if not local_version and not version: # I don't believe there should ever not be one of these around.

            mis_log.critical("No version info found fix this!!!!!")
            sys.exit(1)


    print('')
    if version == local_version or not local_version:

        print("Version: %s" % version)
        print('')
        sys.exit(0)


    print("Local Version: %s" % local_version)
    print("Installed Version: %s" % version)
    print('')

    sys.exit(0)

@bin.command(name='mis_export', help='Export MIS Data to Flat Files from Colleague RPT Tables.')
@click.option('-r', '--report', type=str, help='The MIS report to export data from')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the report')
@click.option('-s', '--sql-only', is_flag=True, type=bool, help='Print the SQL rather than create the export')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to ERROR, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def mis_export(report, gi03, sql_only, log_level):

    mis_log = mislog.mis_console_logger('mis_export', log_level)

    EXPORT_FUNC = "misflatfile.%s_mis_export" % report.lower()

    if sql_only:

        mis_log.info("Generating %s Export Query for %s\n" % (report.upper(), gi03))
        sql = eval(EXPORT_FUNC)(gi03, sql_only = sql_only)
        print('Export SQL\n' + sql)
        sys.exit(0)


    mis_log.info("Generating %s Export File for %s" % (report.upper(), gi03))
    eval(EXPORT_FUNC)(gi03)
    sys.exit(0)

@bin.command(name='dod_refresh', help='Refresh all DOD data from source files')
@click.option('-r', '--report', type=str, help='Only refresh the provided Report')
@click.option('-g', '--gi03', type=str, help='Only refresh the provided Report')
@click.option('-f', '--full', is_flag=True, help='Refresh Schema also Will Ignore --gi03')
@click.option('-s', '--safe', is_flag=True, help='Do not take vaolatile Actions...db uploads etc. Print summary of future refresh.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def dod_refresh(report, gi03, full, safe, log_level):

    mis_log = mislog.mis_console_logger('dod_refresh', log_level)

    print('')
    mis_log.info('Starting Refresh...\n')
    mis_log.info('Starting Parse...\n')

    dod_data = misdod.ref_dod_parse(report=report, gi03=gi03)

    if safe:

        for rpt in dod_data:

            rpt_len = len(dod_data[rpt])

            if rpt_len == 0:
                continue

            itr = 10
            if rpt_len < 10:
                itr = rpt_len

            for i in range(0, itr):
                print(dod_data[rpt][i])

        print('')
        sys.exit(0)

    print('')
    mis_log.info('Starting DOD DB Update...\n')
    misdod.ref_dod_update_db(dod_data, report=report, gi03=gi03, full=full)
    print('')

    sys.exit(0)

@bin.command(name='scff_refresh', help='Refresh The SCFF data from source files')
@click.option('-g', '--gi03', type=str, help='Only refresh the provided Report')
@click.option('-f', '--full', is_flag=True, help='Refresh Schema also Will Ignore --gi03')
@click.option('-s', '--safe', is_flag=True, help='Do not take vaolatile Actions...db uploads etc. Print summary of future refresh.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def scff_refresh(gi03, safe, full, log_level):

    mis_log = mislog.mis_console_logger('scff_refresh', log_level)

    scff_data = misdod.scff_dod_parse(gi03=gi03)

    mis_log.info('Clearing and Inserting %d rows for SCFF %s' % (len(scff_data),gi03))

    print('')
    mis_log.info('Starting DOD DB Update...\n')
    misdod.scff_dod_update_db(scff_data, gi03=gi03, full=full, safe=safe)
    print('')

    sys.exit(0)

@bin.command(name='ods_rpt_refresh', help='Refresh The ODS RPT data from source files')
@click.option('-r', '--report', type=str, help='Only refresh the provided Report')
@click.option('-s', '--sql-only', is_flag=True, help='Will only output the Schemas')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def ods_rpt_refresh(report, sql_only, log_level):

    mis_log = mislog.mis_console_logger('ods_rpt_refresh', log_level)
    print('')
    if not report or report.lower() == 'cb':

        if sql_only:
            mis_log.info('Generating Schema for CB RPT\n')
            script = misrpt.mis_ods_cb_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing CB RPT Tables\n')
            script   = misrpt.mis_ods_cb_refresh_schema()
            num_rows = misrpt.mis_ods_cb_refresh_data()
            mis_log.info('Refreshed %d CB RPT rows\n' % num_rows)

    if not report or report.lower() == 'xb':

        if sql_only:

            mis_log.info('Generating Schema for XB RPT\n')
            script = misrpt.mis_ods_xb_refresh_schema(sql_only=True)
            print(script)
            script = misrpt.mis_ods_xf_refresh_schema(sql_only=True)
            print(script)
            script = misrpt.mis_ods_xe_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing XB RPT Tables\n')
            script   = misrpt.mis_ods_xb_refresh_schema()
            num_rows = misrpt.mis_ods_xb_refresh_data()
            mis_log.info('Refreshed %d XB RPT rows\n' % num_rows)
            script   = misrpt.mis_ods_xf_refresh_schema()
            num_rows = misrpt.mis_ods_xf_refresh_data()
            mis_log.info('Refreshed %d XF RPT rows\n' % num_rows)
            script   = misrpt.mis_ods_xe_refresh_schema()
            num_rows = misrpt.mis_ods_xe_refresh_data()
            mis_log.info('Refreshed %d XE RPT rows\n' % num_rows)

    if not report or report.lower() == 'sx':

        if sql_only:

            mis_log.info('Generating Schema for SX RPT\n')
            script  = misrpt.mis_ods_sx_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing SX RPT Tables\n')
            script   = misrpt.mis_ods_sx_refresh_schema()
            num_rows = misrpt.mis_ods_sx_refresh_data()
            mis_log.info('Refreshed %d SX RPT rows\n' % num_rows)


    if not report or report.lower() == 'eb':

        if sql_only:

            mis_log.info('Generating Schema for EB RPT\n')
            script = misrpt.mis_ods_eb_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing EB RPT Tables\n')
            script   = misrpt.mis_ods_eb_refresh_schema()
            num_rows = misrpt.mis_ods_eb_refresh_data()
            mis_log.info('Refreshed %d EB RPT Rows\n' % num_rows)

    if not report or report.lower() == 'sb':

        if sql_only:

            mis_log.info('Generating Schema for SB RPT\n')
            script = misrpt.mis_ods_sb_refresh_schema(sql_only = True)
            print(script)

        else:

            mis_log.info('Refreshing SB RPT Tables\n')
            script = misrpt.mis_ods_sb_refresh_schema()
            num_rows = misrpt.mis_ods_sb_refresh_data()
            mis_log.info('Refreshed %d SB RPT Rows\n' % num_rows)

    if not report or report.lower() == 'ss':

        if sql_only:

            mis_log.info('Generating Schema for SS RPT\n')
            script = misrpt.mis_ods_ss_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing SS RPT Tables\n')
            script = misrpt.mis_ods_ss_refresh_schema()
            num_rows = misrpt.mis_ods_ss_refresh_data()
            mis_log.info('Refreshed %d SS RPT Rows\n' % num_rows)

    if not report or report.lower() == 'sc':

        if sql_only:

            mis_log.info('Generating Schema for SC RPT\n')
            script = misrpt.mis_ods_sc_refresh_schema(sql_only=True)
            print(script)
            script = misrpt.mis_ods_cw_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing SC RPT Tables\n')
            script = misrpt.mis_ods_sc_refresh_schema()
            num_rows = misrpt.mis_ods_sc_refresh_data()
            mis_log.info('Refreshed %d SC RPT Rows\n' % num_rows)

            mis_log.info('Refreshing CW RPT Tables\n')
            script = misrpt.mis_ods_cw_refresh_schema()
            num_rows = misrpt.mis_ods_cw_refresh_data()
            mis_log.info('Refreshed %d CW RPT Rows\n' % num_rows)

    if not report or report.lower() == 'sd':

        if sql_only:

            mis_log.info('Generating Schema for SD RPT\n')
            script = misrpt.mis_ods_sd_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing SD RPT Tables\n')
            script = misrpt.mis_ods_sd_refresh_schema()
            num_rows = misrpt.mis_ods_sd_refresh_data()
            mis_log.info('Refreshed %d SD RPT Rows\n' % num_rows)

    if not report or report.lower() == 'sy':

        if sql_only:

            mis_log.info('Generating Schema for SY RPT\n')
            script = misrpt.mis_ods_sy_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing SY RPT Tables\n')
            script = misrpt.mis_ods_sy_refresh_schema()
            num_rows = misrpt.mis_ods_sy_refresh_data()
            mis_log.info('Refreshed %d SY RPT Rows\n' % num_rows)

    if not report or report.lower() == 'sp':

        if sql_only:

            mis_log.info('Generating Schema for SP RPT\n')
            script = misrpt.mis_ods_sp_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing SP RPT Tables\n')
            script = misrpt.mis_ods_sp_refresh_schema()
            num_rows = misrpt.mis_ods_sp_refresh_data()
            mis_log.info('Refreshed %d SP RPT Rows\n' % num_rows)

    sys.exit(0)

@bin.command(name='nsc_st_refresh', help='Refresh The Student Tracker Data from result')
@click.option('-s', '--safe', is_flag=True, help='Will only output the Schemas')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def nsc_st_refresh(safe,log_level):

    mis_log = mislog.mis_console_logger('nsc_st_refresh', log_level)

    data = misnsc.mis_st_results_parse()

    mis_log.info('Parsed %d rows from most recent Student Tracker results\n' % len(data))
    if safe:
        for i in range(0, 10):
            print(data[i])
        sys.exit(0)

    mis_log.info('Refreshing Student Tracker Results Table\n')
    num_rows = misnsc.mis_st_results_update_db(data)
    mis_log.info('Refreshed %d Rows in Student Tracker Results\n' % num_rows)

@bin.command(name='coci_refresh', help='Refresh The COCI data from Curriculum Inventory')
@click.option('-c', '--courses', is_flag=True, help='Only consider COCI Courses in Refresh Operations')
@click.option('-p', '--programs', is_flag=True, help='Only consider COCI programs in Refresh Operations')
@click.option('-s', '--safe', is_flag=True, help='Do not take volatile Actions...db uploads etc. Print summary of future refresh.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def coci_refresh(courses, programs, safe, log_level):

    print('')

    mis_log = mislog.mis_console_logger('coci_refresh', log_level)

    if courses or (not programs and not courses):

        coci_course_data = miscoci.mis_coci_courses_parse()
        mis_log.info('Parsed %d course records from COCI' % len(coci_course_data) )

        if safe:

            mis_log.info('Will clear and update %d course rows from Curriculum Inventory(COCI)' % len(coci_course_data) )
            print('')

            for i in range(0,9):
                print(coci_course_data[i])

            print('')

        else:

            num_rows = miscoci.mis_coci_courses_update_db(coci_course_data)

            print('')
            mis_log.info('Updated %d rows for COCI Courses' % num_rows )
            print('')

    if programs or (not programs and not courses):

        coci_prog_data = miscoci.mis_coci_programs_parse()
        mis_log.info('Parsed %d Program records from COCI' % len(coci_prog_data) )

        if safe:

            mis_log.info('Will clear and update %d program rows from Curriculum Inventory(COCI)' % len(coci_prog_data) )
            print('')

            for i in range(0,9):
                print(coci_prog_data[i])

            print('')
        else:

            num_rows = miscoci.mis_coci_programs_update_db(coci_prog_data)

            print('')
            mis_log.info('Updated %d rows for COCI Programs' % num_rows )
            print('')

    sys.exit(0)


#@bin.command(name='ipeds_ef', help='Refresh the DOD Ipeds Fall HR data')
#@click.option('-y', '--later-year',  type=int, help='The later survey year')
#@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
#@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
#def ipeds_hr(later_year, safe, log_level):
#
#    mis_log = mislog.mis_console_logger('ipeds_fa_enr', log_level)
#
#    fa_enr_table  = 'L56_DOD_IPEDS_EF'
#    fa_enr_data = misdod.ef_ipeds_parse(later_year)
#    db = DB('ods')
#    #db.truncate(fa_enr_table)
#    cnt = db.insert_batch( fa_enr_table, fa_enr_data )
#    mis_log.info('Inserted %d rows into %s' % (cnt, fa_enr_table))
#    db.close()
#    sys.exit(0)
#
#@bin.command(name='ipeds_enr_12', help='Refresh the DOD Ipeds Fall HR data')
#@click.option('-y', '--later-year',  type=int, help='The later survey year')
#@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
#@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
#def ipeds_hr(later_year, safe, log_level):
#
#    mis_log = mislog.mis_console_logger('ipeds_enr_12', log_level)
#
#    enr_12_table  = 'L56_DOD_IPEDS_ENR_12'
#    enr_12_data = misdod.enr_12_ipeds_parse(later_year)
#
#    db = DB('ods')
#    #db.truncate(enr_12_table)
#    cnt = db.insert_batch( enr_12_table, enr_12_data )
#    mis_log.info('Inserted %d rows into %s' % (cnt, enr_12_table))
#    db.close()
#    sys.exit(0)

if __name__ == "__main__":
    bin()
