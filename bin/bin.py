# native deps
import os
import sys
import logging
import glob
from datetime import datetime
from datetime import timedelta

# third-party
import click # cli dependancy

# local deps
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append("%s/../../MIS-Tools" % SCRIPT_DIR)

from mistools    import misflatfile
from mistools    import misdod
from mistools    import mislog
from mistools.db import DB

@click.group(name='bin')
def bin():
    pass

@bin.command(name='mis_export', help='Export MIS Data to Flat Files from Colleague RPT Tables')
@click.option('-r', '--report', type=str, help='The MIS report to export data from')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the report')
@click.option('-s', '--sql-only', is_flag=True, type=bool, help='Print the SQL rather than create the export')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to ERROR, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def mis_export(report, gi03, sql_only, log_level):

    mis_log = mislog.mis_console_logger('mis_export', log_level)

    EXPORT_FUNC = "misflatfile.%s_mis_export" % report.lower()

    if sql_only:
        sql = eval(EXPORT_FUNC)(gi03, sql_only = sql_only)
        mis_log.info('Export SQL\n' + sql)
        mis_log.info("Generating %s Export Query for %s\n" % (report.upper(), gi03))
        sys.exit(0)


    mis_log.info("Generating %s Export Query for %s" % (report.upper(), gi03))
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
    print('')
    mis_log.info('Starting DOD DB Update...\n')
    misdod.ref_dod_update_db(dod_data, report=report, gi03=gi03, full=full, safe=safe)
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


@bin.command(name='ipeds_ef', help='Refresh the DOD Ipeds Fall HR data')
@click.option('-y', '--later-year',  type=int, help='The later survey year')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
def ipeds_hr(later_year, safe, log_level):

    mis_log = mislog.mis_console_logger('ipeds_fa_enr', log_level)

    fa_enr_table  = 'L56_DOD_IPEDS_EF'
    fa_enr_data = misdod.ef_ipeds_parse(later_year)
    db = DB('ods')
    #db.truncate(fa_enr_table)
    cnt = db.insert_batch( fa_enr_table, fa_enr_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, fa_enr_table))
    db.close()
    sys.exit(0)

@bin.command(name='ipeds_enr_12', help='Refresh the DOD Ipeds Fall HR data')
@click.option('-y', '--later-year',  type=int, help='The later survey year')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
def ipeds_hr(later_year, safe, log_level):

    mis_log = mislog.mis_console_logger('ipeds_enr_12', log_level)

    enr_12_table  = 'L56_DOD_IPEDS_ENR_12'
    enr_12_data = misdod.enr_12_ipeds_parse(later_year)

    db = DB('ods')
    #db.truncate(enr_12_table)
    cnt = db.insert_batch( enr_12_table, enr_12_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, enr_12_table))
    db.close()
    sys.exit(0)

if __name__ == "__main__":
    bin()
