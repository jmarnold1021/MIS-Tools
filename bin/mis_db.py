# native deps
import os
import sys
import logging

# third-party
import click # cli dependancy

# local deps
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append("%s/../../MIS-Tools" % SCRIPT_DIR)

from mistools import misflatfile
from mistools import misdod
from mistools.db import DB

# create logger
# below has some good guidelines on when to use what levels...prob not that way yet...
# https://docs.python.org/3/howto/logging.html#logging-levels
def _get_mis_logger(level):

    # create logging comps
    logger    = logging.getLogger('mis_db')
    handler   = logging.StreamHandler() # log to console
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # sort of verbose atm

    # link everything
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    LOG_LEVELS = {

        "CRITICAL" : '50',
        "ERROR"    : '40',
        "WARNING"  : '30',
        "WARN"     : '30',
        "INFO"     : '20',
        "DEBUG"    : '10',
        "NOTSET"   : '0'
    }

    if level.upper() in list(LOG_LEVELS.keys()):
        logger.setLevel(int(LOG_LEVELS[level]))
        return logger

    logger.setLevel(20)
    return logger


@click.group(name='mis_db')
def mis_db():
    pass

@mis_db.command(name='update', help='Update MIS DB staging tables from submission Flat Files')
@click.option('-r', '--report', type=str, help='The MIS report to upload to the table')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the report')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
def update(report, gi03, safe, log_level):

    mis_log = _get_mis_logger(log_level)

    PARSE_FUNC = "misflatfile.%s_mis_parse" % report.lower()
    MIS_FF_PATH = '//ltcc-app/MIS/%s/U22%s%s.DAT' % (gi03,
                                                     gi03,
                                                     report.upper())

    try:
        if report.upper() in ['XB','XE','XF']: # uncombine XB -> XB/XF/XE

            PARSE_FUNC = "misflatfile.%s_mis_parse" % 'xb'
            MIS_FF_PATH = '//ltcc-app/MIS/%s/U22%s%s.DAT' % (gi03,
                                                             gi03,
                                                             'XB')
            data = eval(PARSE_FUNC)(MIS_FF_PATH)
            data = data[report.upper()] # XB/XF/XE
        else:
            data = eval(PARSE_FUNC)(MIS_FF_PATH)

    except FileNotFoundError as e:
        mis_log.error('No submission found for %s in term %s' % (report.upper(), gi03))
        sys.exit(1)

    if safe: # allows a quick print of top rows to verify POSITIONS DED spec...

        mis_log.info('Top row\n')
        for i in range(0,9):
            print(data[i])
            print('')
        mis_log.info("%s will update %d rows\n" % (report.upper(), len(data)))
        sys.exit(0)


    db = DB('mis') # start db con

    # super safe....
    rows = db.exec_query("SELECT COUNT(*) FROM %s_STAGING WHERE GI03 = '%s'" % (report.upper(), gi03))

    if rows[0][0] != 0: # basically top left of grid

        mis_log.warning("%s already updated for %s" % (report.upper(), gi03))
        db.close() # close db con
        sys.exit(1)

    # everything ok update with 'python update.py CW 222 0' -- at end says verified
    cnt = db.insert_batch('%s_STAGING' % report.upper(), data) # insert data
    mis_log.info('Inserted %d rows into %s_STAGING' % (cnt, report.upper()))

    db.close() # close db con

    sys.exit(0)

@mis_db.command(name='update_stuid', help='Update MIS DB CCCCO Ids table')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the ST report')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
def update_stuid(gi03, safe, log_level):

    mis_log = _get_mis_logger(log_level)

    db = DB('mis')

    # consinder making this a count query
    prev_id_data = db.exec_query('SELECT * FROM CCCOID2SB00')

    id_data = misdod.stuid_dod_parse(gi03, fill_empty = 'NA')

    if safe: # allows a quick print of top rows to verify POSITIONS DED spec...
        mis_log.info('Top rows CCCCOID\n')
        for i in range(0, 9):
            print(id_data[i])

        mis_log.info("CCCCO IDs will contain %d rows from a previous %d\n" % (len(id_data), len(prev_id_data)))
        db.close()
        sys.exit(0)


    #db.exec_query('TRUNCATE TABLE CCCOID2SB00')
    #mis_log.info('Cleared %d IDs' % len(prev_id_data))
    cnt = db.insert_batch( 'CCCOID2SB00', id_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, 'CCCOID2SB00'))

    db.close()

    sys.exit(0)

@mis_db.command(name='update_xbd', help='Update MIS DB XBD staging table from DOD files')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the ST report')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take volatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
def update_xbd(gi03, safe, log_level):

    mis_log = _get_mis_logger(log_level)

    try:
        xbd_data = misdod.xb_dod_parse(gi03, fill_empty='NA', dict_read=True)
    except FileNotFoundError as e:
        mis_log.error('No Data On Demand referential data found for XBD found for term %s' % gi03)
        sys.exit(1)

    xbd_rows = []

    for row in xbd_data:
        xbd_row = []

        xbd_row.append(row['GI03'])

        xbd_row.append(row['CB01'])

        xbd_row.append(row['XB00'])

        xbd_row.append(row['CB00'])

        xbd_row.append(row['XBD1'])

        xbd_row.append(row['XBD3'])

        if float(row['XBD4']).is_integer() == True:
            xbd_row.append(str(int(float(row['XBD4'])))) # xbd2
        else:
            xbd_row.append(str(round(float(row['XBD4']), 2))) # xbd2

        xbd_row.append(row['XBD5'])

        xbd_rows.append(xbd_row)

    if safe: # allows a quick print of top row to verify POSITIONS DED spec...

        mis_log.info('Top rows\n')
        for i in range(0, 9):
            print(xbd_rows[i])

        mis_log.info("XBD will update %d rows\n" % len(xbd_rows))
        sys.exit(0)

    db = DB('mis')
    rows = db.exec_query("SELECT COUNT(*) FROM XBD_STAGING WHERE GI03 = '%s'" % gi03)
    if rows[0][0] != 0: # basically top left of grid

        mis_log.warning("XBD already updated for %s" %  gi03)
        db.close() # close db con
        sys.exit(1)


    cnt = db.insert_batch('XBD_STAGING', xbd_rows)
    mis_log.info('Inserted %d rows into XBD_STAGING' % cnt)

    db.close()
    sys.exit(0)

@mis_db.command(name='update_std', help='Update MIS DB ST staging table from DOD files')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the ST report')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
def update_std(gi03, safe, log_level):

    mis_log = _get_mis_logger(log_level)

    db = DB('mis')
    id_data = db.exec_query('SELECT * FROM CCCOID2SB00', dict_read=True)

    id_map = {}
    for row in id_data:
        id_map[row['CCCOID']] = row['SB00']

    try:
        std_data = misdod.st_dod_parse(gi03, fill_empty='NA', dict_read=True)
    except FileNotFoundError as e:
        mis_log.error('No Data On Demand referential data found for STD found for term %s' % gi03)
        sys.exit(1)

    std_rows = []
    bad_cccco_ids = [] # bad stuff
    for row in std_data:

        std_row = []

        cccco_id = row['CCCCO_Assigned']
        if cccco_id not in id_map:
            bad_cccco_ids.append([row['CCCCO_Assigned'], row['SB31'], row['SB32']]) # ids's from data files not found in ref
            continue

        std_row.append(id_map[cccco_id]) # sb00
        std_row.append(cccco_id)         # ccco_id

        std_row.append(row['GI03']) # Gi03

        std_row.append(row['STD1']) # std1

        if float(row['STD2']).is_integer() == True:
            std_row.append(str(int(float(row['STD2'])))) # std2
        else:
            std_row.append(str(round(float(row['STD2']), 2))) # std2

        std_row.append(row['STD3']) # std3

        std_row.append(row['STD4']) # std4

        if float(row['STD5']).is_integer() == True:
            std_row.append(str(int(float(row['STD5'])))) # std5
        else:
            std_row.append(str(round(float(row['STD5']), 2))) # std5

        std_row.append(row['STD6']) # std6

        std_row.append(row['STD7']) # std7

        if float(row['STD8']).is_integer() == True:
            std_row.append(str(int(float(row['STD8'])))) # std8
        else:
            std_row.append(str(round(float(row['STD8']), 2))) # std8

        std_row.append(row['STD10']) # std10


        std_rows.append(std_row)

    if safe: # allows a quick print of top row to verify POSITIONS DED spec...

        mis_log.info('Top rows\n')
        for i in range(0, 9):
            print(std_rows[i])

        mis_log.info("STD will update %d rows\n" % len(std_rows))
        mis_log.info("%d Unmatched IDS\n" % len(bad_cccco_ids))
        print(bad_cccco_ids[:10])
        db.close() # close db con
        sys.exit(0)

    rows = db.exec_query("SELECT COUNT(*) FROM ST_STAGING WHERE GI03 = '%s'" % gi03)
    if rows[0][0] != 0: # basically top left of grid

        mis_log.warning("ST already updated for %s" %  gi03)
        db.close() # close db con
        sys.exit(1)

    cnt = db.insert_batch('ST_STAGING', std_rows)

    mis_log.info('Inserted %d rows into %s' % (cnt, 'ST_STAGING'))

    db.close()
    sys.exit(0)

@mis_db.command(name='update_sxd', help='Update MIS DB SXD staging table from DOD files')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the ST report')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
def update_sxd(gi03, safe, log_level):

    mis_log = _get_mis_logger(log_level)

    db = DB('mis')
    id_data = db.exec_query('SELECT * FROM CCCOID2SB00', dict_read=True)

    id_map = {}
    for row in id_data:
        id_map[row['CCCOID']] = row['SB00']

    try:
        sxd_data = misdod.sx_dod_parse(gi03, fill_empty='NA', dict_read=True)
    except FileNotFoundError as e:
        mis_log.error('No Data On Demand referential data found for SXD found for term %s' % gi03)

    sxd_rows = []
    bad_cccco_ids = [] # bad stuff

    for row in sxd_data:
        sxd_row = []

        cccco_id = row['CCCCO_Assigned']
        if cccco_id not in id_map:
            bad_cccco_ids.append(cccco_id) # ids's from data files not found in ref
            continue

        sxd_row.append(id_map[cccco_id]) # sb00
        sxd_row.append(cccco_id)         # ccco_id
        sxd_row.append(row['GI03'])     # Gi03

        sxd_row.append(row['SXD1'])     # sxd1
        sxd_row.append(row['SXD2'])     # sxd2

        if float(row['SXD3']).is_integer() == True:
            sxd_row.append(str(int(float(row['SXD3'])))) # sxd3
        else:
            sxd_row.append(str(round(float(row['SXD3']), 2))) # sxd3

        if float(row['SXD4']).is_integer() == True:
            sxd_row.append(str(int(float(row['SXD4'])))) # sxd4
        else:
            sxd_row.append(str(round(float(row['SXD4']), 1))) # sxd4

        sxd_row.append(row['XB00']) # xb00
        sxd_row.append(row['CB01']) # cb01
        sxd_row.append(row['CB00']) # cb00

        sxd_rows.append(sxd_row)

    if safe: # allows a quick print of top row to verify POSITIONS DED spec...

        mis_log.info('Top rows\n')
        for i in range(0, 9):
            print(sxd_rows[i])

        mis_log.info("SXD will update %d rows\n" % len(sxd_rows))
        mis_log.info("%d Unmatched IDS\n" % len(bad_cccco_ids))
        print(bad_cccco_ids[:10])
        db.close() # close db con
        sys.exit(0)

    rows = db.exec_query("SELECT COUNT(*) FROM SXD_STAGING WHERE GI03 = '%s'" % gi03)
    if rows[0][0] != 0: # basically top left of grid

        mis_log.warning("SXD already updated for %s" %  gi03)
        db.close() # close db con
        sys.exit(1)

    cnt = db.insert_batch('SXD_STAGING', sxd_rows)
    mis_log.info('Inserted %d rows into %s' % (cnt, 'SXD_STAGING'))

    db.close()
    sys.exit(0)

@mis_db.command(name='update_sps', help='Run MIS DB Stored Procedure Updates')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take vaolatile Actions...db uploads etc. Print top rows of data.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command, Choices [CRITICAL, ERROR, WARN INFO, DEBUG]')
def update_sps( safe, log_level):

    mis_log = _get_mis_logger(log_level)

    if safe:

        mis_log.info('WIll update the follwoing Stored Procedures')
        print('\nSX_REPORT_MAINTENANCE')
        print('Refresh_PELL_UPTAKE')
        #print('UPDATE_PELL_PROM_AWARDS_FLAG')
        print('')
        sys.exit(0)

    db = DB('mis')

    print('')

    mis_log.info('Starting SX_REPORT_MAINTENANCE Stored Procedure')
    db.exec_sp('SX_REPORT_MAINTENANCE')
    mis_log.info('Finished SX_REPORT_MAINTENANCE Stored Procedure')

    print('')

    mis_log.info('Starting Refresh_PELL_UPTAKE Stored Procedure')
    db.exec_sp('Refresh_PELL_UPTAKE')
    mis_log.info('Finished Refresh_PELL_UPTAKE Stored Procedure')

    print('')

    #mis_log.info('Starting UPDATE_PELL_PROM_AWARDS_FLAG Stored Procedure')
    #db.exec_sp('UPDATE_PELL_PROM_AWARDS_FLAG')
    #mis_log.info('Finished UPDATE_PELL_PROM_AWARDS_FLAG Stored Procedure')

    #print('')

    db.close()
    sys.exit(0)


if __name__ == "__main__":
    mis_db()
