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

@bin.command(name='dod_refresh_all', help='Refresh all DOD data from source files')
@click.option('-s', '--safe', is_flag=True, help='Do not take vaolatile Actions...db uploads etc. Print summary of future refresh.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def dod_refresh_all(safe, log_level):

    mis_log = mislog.mis_console_logger('dod_refresh_all', log_level)

    print('')
    mis_log.info('Starting Refresh...\n')

    mis_log.info('Starting Parse...\n')
    dod_data = misdod.ref_dod_parse()

    print('')
    mis_log.info('Starting Batch upload...\n')

    db = DB('ods')
    total_rows = 0
    total_tables = 0
    for report in dod_data:

        dod_table = 'L56_DOD_%s' % report
        total_rows += len(dod_data[report])
        total_tables += 1
        if safe:
            mis_log.info('Will clear and insert %d rows to %s' % (len(dod_data[report]), dod_table))
            continue

        mis_log.info('Clearing %s' % dod_table)
        db.truncate(dod_table)
        mis_log.info('Starting to insert %d rows for %s' % (len(dod_data[report]), dod_table))
        cnt = db.insert_batch( dod_table, dod_data[report] )
        mis_log.info('Inserted %d rows into %s' % (cnt, dod_table))

    print('')
    mis_log.info('Refresh Complete...%d rows inserted into %d tables' % (total_rows, total_tables))
    print('')

    db.close()
    sys.exit(0)

@bin.command(name='dod_refresh_stuid', help='Refresh the DOD StuId Mappings')
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

@bin.command(name='dod_refresh_sb', help='Refresh the DOD StuId Mappings')
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

@bin.command(name='dod_refresh_fr', help='Refresh the DOD StuId Mappings')
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


@bin.command(name='dod_refresh', help='Refresh the DOD StuId Mappings')
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

    # check what is there for provided gi03
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

####### DEV #########

@bin.command(name='ipeds_hr', help='Refresh the DOD StuId Mappings')
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


@bin.command(name='test', help='Refresh the DOD StuId Mappings')
def test():

    test_log = mislog.mis_console_logger('test', 'DEBUG')
    data = misflatfile.cc_mis_parse('//ltcc-app/MIS/230/U22230CC.dat', headers = True)

    print(data[0])
    start_date = datetime.fromisoformat('2022-07-01')
    print(start_date)
    for row in data[1:]:
        if row[9] == 'H':
            td = timedelta(days = (int(row[3]) - 1))
            print(start_date + td)


if __name__ == "__main__":
    bin()
