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

# internal modules...
from mistools    import misipeds
from mistools    import mislog
from mistools    import miserrors
from mistools.db import DB


@click.group(name='bin')
def bin():
    pass

@bin.command(name='ipeds_version', help='List the currently installed version of MIS-Tools.')
def ipeds_version():

    mis_log = mislog.mis_console_logger('ipeds_version', 'INFO')

    local_version = None
    version       = None

    try: # nice for dev...an checking version upates happen

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

@bin.command(name='ipeds_sfa', help='Refresh the DOD Ipeds Student Financial Aid data')
@click.option('-y', '--latter-year',  type=int, help='The later survey year')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take volatile Actions...db uploads etc. Print top rows of data.')
@click.option('-d', '--diff', is_flag=True, type=bool, help='Look for differeces between new EF data and current in DB')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def ipeds_sfa(latter_year, safe, diff, log_level):

    mis_log = mislog.mis_console_logger('ipeds_sfa', log_level)

    sfa_table  = 'L56_DOD_IPEDS_SFA'
    sfa_data = misipeds.sfa_ipeds_parse(latter_year=latter_year)

    if safe:

        for i in range(0, 10):
            print(ef_data[i])

        sys.exit(0)

    if latter_year and diff: # only diff individual years atm

        mis_log.info('Diffing DB vs Parsed Files')
        misipeds.sfa_ipeds_diff(sfa_data, latter_year, sfa_table)
        sys.exit(0)

    db = DB('ods')

    if not latter_year:
        db.truncate(sfa_table)
    else:
        db.exec_query('DELETE FROM %s WHERE LATTER_YEAR = %d' % (sfa_table, latter_year) )

    cnt = db.insert_batch( sfa_table, sfa_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, sfa_table))
    db.close()
    sys.exit(0)

@bin.command(name='ipeds_ef', help='Refresh the DOD Ipeds EF data')
@click.option('-y', '--latter-year',  type=int, help='The later survey year')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take volatile Actions...db uploads etc. Print top rows of data.')
@click.option('-d', '--diff', is_flag=True, type=bool, help='Look for differeces between new EF data and current in DB')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def ipeds_ef(latter_year, safe, diff, log_level):

    mis_log = mislog.mis_console_logger('ipeds_ef', log_level)

    ef_table  = 'L56_DOD_IPEDS_EF'
    ef_data = misipeds.ef_ipeds_parse(latter_year=latter_year)

    if safe:

        for i in range(0, 10):
            print(ef_data[i])

        sys.exit(0)

    if latter_year and diff: # only diff individual years atm

        mis_log.info('Diffing DB vs Parsed Files')
        misipeds.ef_ipeds_diff(ef_data, latter_year, ef_table)
        sys.exit(0)

    db = DB('ods')

    if not latter_year:
        db.truncate(ef_table)
    else:
        db.exec_query('DELETE FROM %s WHERE LATTER_YEAR = %d' % (ef_table, latter_year) )

    cnt = db.insert_batch( ef_table, ef_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, ef_table))
    db.close()
    sys.exit(0)

@bin.command(name='ipeds_e12', help='Refresh the DOD Ipeds 12 month data')
@click.option('-y', '--latter-year',  type=int, help='The latter survey year')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take volatile Actions...db uploads etc. Print top rows of data.')
@click.option('-d', '--diff', is_flag=True, type=bool, help='Look for differeces between new E12 data and current in DB')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def ipeds_e12(latter_year, safe, diff, log_level):

    mis_log = mislog.mis_console_logger('ipeds_e12', log_level)

    e12_table  = 'L56_DOD_IPEDS_E12'
    e12_data = misipeds.e12_ipeds_parse(latter_year=latter_year)

    if safe:

        for i in range(0, 10):
            print(e12_data[i])

        sys.exit(0)

    if latter_year and diff: # only diff individual years atm

        misipeds.e12_ipeds_diff(e12_data, latter_year, e12_table)
        sys.exit(0)

    db = DB('ods')

    if not latter_year:
        db.truncate(e12_table)
    else:
        db.exec_query('DELETE FROM %s WHERE LATTER_YEAR = %d' % (e12_table, latter_year) )

    mis_log.info('Diffing DB vs Parsed Files')
    cnt = db.insert_batch( e12_table, e12_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, e12_table))
    db.close()
    sys.exit(0)

@bin.command(name='ipeds_soc', help='Refresh the DOD Ipeds Soc Map')
@click.option('-f', '--file',  type=str, help='Path to the SOC map CSV.')
@click.option('-s', '--safe', is_flag=True, type=bool, help='Do not take volatile Actions...db uploads etc. Print top rows of data.')
@click.option('-d', '--diff', is_flag=True, type=bool, help='Look for differeces between new SOC data and current in DB')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def ipeds_soc(file, safe, diff, log_level):

    mis_log = mislog.mis_console_logger('ipeds_soc', log_level)

    soc_table  = 'L56_DOD_IPEDS_SOC_MAP'
    soc_data = misipeds.hr_ipeds_soc_map_parse(file)

    if safe:

        for i in range(0, 10):
            print(soc_data[i])

        sys.exit(0)



    db = DB('ods')

    db.truncate(soc_table)

    mis_log.info('Diffing DB vs Parsed Files')
    cnt = db.insert_batch( soc_table, soc_data )
    mis_log.info('Inserted %d rows into %s' % (cnt, soc_table))
    db.close()
    sys.exit(0)

if __name__ == "__main__":
    bin()

