
# native deps
import os
import sys
import logging
import glob
import json
from datetime import datetime
from datetime import timedelta

# third-party
import click # cli dependancy

# local deps
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PACKAGE_DIR = '%s/..' % SCRIPT_DIR
sys.path.append("%s/../../MIS-Tools" % SCRIPT_DIR)

from mistools    import misflatfile
from mistools    import misdod
from mistools    import mislog
from mistools    import miscoci
from mistools    import mis320
from mistools.db import DB

@click.group(name='bin_dev')
def bin_dev():
    pass

@bin_dev.command(name='dod_refresh_stuid', help='Refresh the DOD StuId Mappings')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to ERROR, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def dod_refresh_stuid(safe, log_level):

    mis_log = mislog.mis_console_logger('dod_refresh_stuid', log_level)
    dod_table = 'L56_DOD_STUID'

    db = DB('ods')

    # consinder making this a count query
    prev_id_data = db.exec_query('SELECT * FROM %s'  % dod_table)
    id_data = misdod.stuid_dod_parse()

    if safe: # allows a quick print of top rows to verify POSITIONS DED spec...
        mis_log.info('Top rows %s\n' % dod_table)
        for i in range(0, 9):
            print(id_data[i])

        mis_log.info("STU IDs will contain %d rows from a previous %d\n" % (len(id_data), len(prev_id_data)))
        db.close()
        sys.exit(0)

    db.truncate(dod_table)
    mis_log.info('Cleared %d stuid rows' % len(prev_id_data))

    cnt = db.insert_batch( dod_table, id_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, dod_table))

    db.close()

    sys.exit(0)

@bin_dev.command(name='dod_refresh_sb', help='Refresh the DOD StuId Mappings')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to ERROR, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def dod_refresh_sb(safe, log_level):

    mis_log = mislog.mis_console_logger('dod_refresh_sb', log_level)
    dod_table = 'L56_DOD_SB'
    db = DB('ods')

    # consinder making this a count query
    prev_sb_data = db.exec_query('SELECT * FROM %s'  % dod_table)
    sb_data = misdod.sb_dod_parse()

    if safe: # allows a quick print of top rows to verify POSITIONS DED spec...
        mis_log.info('Top rows %s\n' % dod_table)
        for i in range(0, 9):
            print(sb_data[i])

        mis_log.info("Student Basic will contain %d rows from a previous %d\n" % (len(sb_data), len(prev_sb_data)))
        db.close()
        sys.exit(0)

    db.truncate(dod_table)
    mis_log.info('Cleared %d Student Basic rows' % len(prev_sb_data))

    cnt = db.insert_batch( dod_table, sb_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, dod_table))

    db.close()

    sys.exit(0)

@bin_dev.command(name='dod_refresh_fr', help='Refresh the DOD StuId Mappings')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to ERROR, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def dod_refresh_fr(safe, log_level):

    mis_log = mislog.mis_console_logger('dod_refresh_fr', log_level)
    dod_table = 'L56_DOD_FR'

    db = DB('ods')

    # consinder making this a count query
    prev_fr_data = db.exec_query('SELECT * FROM %s'  % dod_table)
    fr_data = misdod.fr_dod_parse()

    if safe: # allows a quick print of top rows to verify POSITIONS DED spec...
        mis_log.info('Top rows %s\n' % dod_table)
        for i in range(0, 9):
            print(fr_data[i])

        mis_log.info("Firsts Ref will contain %d rows from a previous %d\n" % (len(fr_data), len(prev_fr_data)))
        db.close()
        sys.exit(0)

    db.truncate(dod_table)
    mis_log.info('Cleared %d Firsts Ref rows' % len(prev_fr_data))

    cnt = db.insert_batch( dod_table, fr_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, dod_table))

    db.close()

    sys.exit(0)


@bin_dev.command(name='dod_refresh_bac', help='Refresh/Add DOD data for the provided report/Gi03 pair')
@click.option('-r', '--report', type=str, help='The MIS report to export data from')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the ST report')
@click.option('--update', is_flag=True, help='Update the DOD data for the provided Gi03')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def dod_refresh(report, gi03, update, log_level):


    mis_log = mislog.mis_console_logger('dod_refresh', log_level)
    parse_func = "misdod.%s_dod_parse" % report.lower()
    dod_table  = 'L56_DOD_%s' % report.upper()


    dod_data = eval(parse_func)(gi03) # pull data

    db = DB('ods')

    # check what is there for provided gi03 only for feedback atm
    rows = db.exec_query("SELECT COUNT(*) FROM %s WHERE GI03 = '%s'" % (dod_table, gi03))

    if update: # remove this Gi03
        row_count = db.exec_query("DELETE FROM %s WHERE GI03 = '%s'" % (dod_table, gi03))
        mis_log.warning("Removed %d rows from %s" % ( row_count, dod_table))

    elif rows[0][0] != 0: # basically top left of grid

        mis_log.warning("%s already updated for %s use --update to refresh a provided Gi03" % (dod_table, gi03))
        db.close() # close db con
        sys.exit(1)

    cnt = db.insert_batch( dod_table, dod_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, dod_table))
    db.close()
    sys.exit(0)

@bin_dev.command(name='ipeds_hr', help='Refresh the DOD StuId Mappings')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
def ipeds_hr(safe, log_level):

    mis_log = _get_mis_logger(log_level)
    hr_table  = 'L56_DOD_IPEDS_HR'
    root = '//ltcc-app/MIS/Data_On_Demand/Accountability/Human_Resources/IPEDS_HUMANRESOR_221_*.txt'

    hr_files = []
    for hr_file in glob.iglob( root ):
        hr_files.append(hr_file)

    hr_data = misdod.hr_ipeds_parse(hr_files)
    print(hr_data[:9])

    db = DB('ods')
    db.truncate(hr_table)
    cnt = db.insert_batch( hr_table, hr_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, hr_table))
    db.close()
    sys.exit(0)


@bin_dev.command(name='test', help='Run Stuff')
def test():

    mis320.mis_320_summary_parse('C:/Users/admin_ja/LTCCD/MIS-Tools/tmp/320_Section_summary_P3.txt')



if __name__ == "__main__":
    bin_dev()
