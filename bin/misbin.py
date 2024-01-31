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
from mistools    import misflatfile
from mistools    import misdod
from mistools    import misipeds
from mistools    import mislog
from mistools    import miscoci
from mistools    import misrpt
from mistools    import misnsc
from mistools    import misltusd
from mistools    import miscalgrant
from mistools    import miserrors
from mistools.db import DB


def _safe_prnt(data, itr=11): # place to print some specs and view data samples before uploading

    if not data or \
       type(data) != list or \
       len(data) == 0:

        print('_safe_prnt: No valid itr data')

    for i in range(0, itr):

        if i == 0:

            print('')
            print( 'Row Length is %d' % len(data[i]) )
            print('')

        print(data[i])

    print('')

@click.group(name='bin')
def bin():
    pass

@bin.command(name='mis_version', help='List the currently installed version of MIS-Tools.')
def mis_version():

    mis_log = mislog.mis_console_logger('mis_version', 'INFO')

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

@bin.command(name='mis_export', help='Export MIS Data to Flat Files from Colleague RPT Tables.')
@click.option('-r', '--report', type=str, help='The MIS report to export data from')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the report')
@click.option('-b', '--backup', is_flag=True, type=bool, help='Backup the prev dat file for this (gi03,report)')
@click.option('-s', '--sql-only', is_flag=True, type=bool, help='Print the SQL rather than create the export')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to ERROR, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def mis_export(report, gi03, backup, sql_only, log_level):

    mis_log = mislog.mis_console_logger('mis_export', log_level)

    EXPORT_FUNC = "misflatfile.%s_mis_export" % report.lower()

    if sql_only:

        mis_log.info("Generating %s Export Query for %s\n" % (report.upper(), gi03))
        sql = eval(EXPORT_FUNC)(gi03, sql_only = sql_only)
        print('-- Export SQL\n\n' + sql)
        print('')
        sys.exit(0)


    mis_log.info("Generating %s Export File for %s" % (report.upper(), gi03))
    if backup:
        mis_log.info("Backing %s Export File up for %s" % (report.upper(), gi03))
        eval(EXPORT_FUNC)(gi03, backup)
    else:
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


    if not report or report.lower() == 'cb':

        dod_data = misdod.cb_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...\n')
            misdod.ref_dod_update_db(dod_data, report='CB', gi03=gi03, full=full)


    if not report or report.lower() == 'xb':

        xb_data = misdod.xb_dod_parse(gi03=gi03)
        xf_data = misdod.xf_dod_parse(gi03=gi03)
        xe_data = misdod.xe_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(xb_data)
            _safe_prnt(xe_data)
            _safe_prnt(xf_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...XB\n')
            xb_data = misdod.ref_dod_update_db(dod_data, report='XB', gi03=gi03, full=full)
            mis_log.info('Starting DOD DB Update...XF\n')
            xf_data = misdod.ref_dod_update_db(dod_data, report='XF', gi03=gi03, full=full)
            mis_log.info('Starting DOD DB Update...XE\n')
            xe_data = misdod.ref_dod_update_db(dod_data, report='XE', gi03=gi03, full=full)


    if not report or report.lower() == 'sx':

        dod_data = misdod.sx_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...SX\n')
            misdod.ref_dod_update_db(dod_data, report='SX', gi03=gi03, full=full)


    if not report or report.lower() == 'eb':

        dod_data = misdod.eb_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...EB\n')
            misdod.ref_dod_update_db(dod_data, report='EB', gi03=gi03, full=full)


    if not report or report.lower() == 'st':

        dod_data = misdod.st_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...ST\n')
            misdod.ref_dod_update_db(dod_data, report='ST', gi03=gi03, full=full)


    if not report or report.lower() == 'ss':

        dod_data = misdod.ss_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...SS\n')
            misdod.ref_dod_update_db(dod_data, report='SS', gi03=gi03, full=full)


    if not report or report.lower() == 'sc':

        sc_data = misdod.sc_dod_parse(gi03=gi03)
        cw_data = misdod.cw_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(sc_data)
            _safe_prnt(cw_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...SC\n')
            misdod.ref_dod_update_db(sc_data, report='SC', gi03=gi03, full=full)
            mis_log.info('Starting DOD DB Update...CW\n')
            misdod.ref_dod_update_db(cw_data, report='CW', gi03=gi03, full=full)


    if not report or report.lower() == 'se':

        dod_data = misdod.se_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...SE\n')
            misdod.ref_dod_update_db(dod_data, report='SE', gi03=gi03, full=full)


    #if not report or report.lower() == 'sv':

    #    dod_data = misdod.sv_dod_parse(gi03=gi03)

    #    if safe:

    #        _safe_prnt(dod_data)

    #    else:

    #        print('')
    #        mis_log.info('Starting DOD DB Update...SV\n')
    #        misdod.ref_dod_update_db(dod_data, report='SV', gi03=gi03, full=full)


    if not report or report.lower() == 'sd':

        dod_data = misdod.sd_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...SD\n')
            misdod.ref_dod_update_db(dod_data, report='SD', gi03=gi03, full=full)


    if not report or report.lower() == 'sg':

        dod_data = misdod.sg_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...SG\n')
            misdod.ref_dod_update_db(dod_data, report='SG', gi03=gi03, full=full)


    #if not report or report.lower() == 'sy':

    #    dod_data = misdod.sy_dod_parse(gi03=gi03)

    #    if safe:

    #        _safe_prnt(dod_data)

    #    else:

    #        print('')
    #        mis_log.info('Starting DOD DB Update...SY\n')
    #        misdod.ref_dod_update_db(dod_data, report='SY', gi03=gi03, full=full)


    #if not report or report.lower() == 'sl':

    #    misdod.sl_dod_parse(gi03=gi03)

    #    if safe:

    #        _safe_prnt(dod_data)

    #    else:

    #        print('')
    #        mis_log.info('Starting DOD DB Update...SL\n')
    #        misdod.ref_dod_update_db(dod_data, report='SL', gi03=gi03, full=full)


    if not report or report.lower() == 'sf':

        sf_data = misdod.sf_dod_parse(gi03=gi03)
        fa_data = misdod.fa_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(sf_data)
            _safe_prnt(fa_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...SF\n')
            misdod.ref_dod_update_db(sf_data, report='SF', gi03=gi03, full=full)
            mis_log.info('Starting DOD DB Update...FA\n')
            misdod.ref_dod_update_db(fa_data, report='FA', gi03=gi03, full=full)


    #if not report or report.lower() == 'aa':
    #    misdod.aa_dod_parse(gi03=gi03)

    #    if safe:

    #        for i in range(0, 10):
    #            print(dod_data[i])

    #    else:

    #        print('')
    #        mis_log.info('Starting DOD DB Update...\n')
    #        misdod.ref_dod_update_db(dod_data, report='AA', gi03=gi03, full=full)


    if not report or report.lower() == 'sp':

        dod_data = misdod.sp_dod_parse(gi03=gi03)

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...SP\n')
            misdod.ref_dod_update_db(dod_data, report='SP', gi03=gi03, full=full)

    if not report or report.lower() == 'ej': # diff source could be combined w/ eb potentially but usually means diff

        dod_data = misdod.ej_dod_parse()

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...EJ\n')
            misdod.ref_dod_update_db(dod_data, report='EJ', gi03=gi03, full=full)


    if not report or report.lower() == 'stuid':

        dod_data = misdod.stuid_dod_parse()

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...STUID\n')
            misdod.ref_dod_update_db(dod_data, report='STUID', gi03=gi03, full=full)

    if not report or report.lower() == 'fr':

        dod_data = misdod.fr_dod_parse()

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...FR\n')
            misdod.ref_dod_update_db(dod_data, report='FR', gi03=gi03, full=full)


    if not report or report.lower() == 'sb':

        dod_data = misdod.sb_dod_parse()

        if safe:

            _safe_prnt(dod_data)

        else:

            print('')
            mis_log.info('Starting DOD DB Update...SB\n')
            misdod.ref_dod_update_db(dod_data, report='SB', gi03=gi03, full=full)


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

    if not report or report.lower() == 'ej':

        if sql_only:

            mis_log.info('Generating Schema for EJ RPT\n')
            script = misrpt.mis_ods_ej_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing EJ RPT Tables\n')
            script   = misrpt.mis_ods_ej_refresh_schema()
            num_rows = misrpt.mis_ods_ej_refresh_data()
            mis_log.info('Refreshed %d EJ RPT Rows\n' % num_rows)

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

    if not report or report.lower() == 'sf':

        if sql_only:

            mis_log.info('Generating Schema for SF RPT\n')
            script = misrpt.mis_ods_sf_refresh_schema(sql_only=True)
            print(script)
            script = misrpt.mis_ods_fa_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing SF RPT Tables\n')
            script = misrpt.mis_ods_sf_refresh_schema()
            num_rows = misrpt.mis_ods_sf_refresh_data()
            mis_log.info('Refreshed %d SF RPT Rows\n' % num_rows)

            mis_log.info('Refreshing FA RPT Tables\n')
            script = misrpt.mis_ods_fa_refresh_schema()
            num_rows = misrpt.mis_ods_fa_refresh_data()
            mis_log.info('Refreshed %d FA RPT Rows\n' % num_rows)

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

    if not report or report.lower() == 'sg':

        if sql_only:

            mis_log.info('Generating Schema for SG RPT\n')
            script = misrpt.mis_ods_sg_refresh_schema(sql_only=True)
            print(script)

        else:

            mis_log.info('Refreshing SG RPT Tables\n')
            script = misrpt.mis_ods_sg_refresh_schema()
            num_rows = misrpt.mis_ods_sg_refresh_data()
            mis_log.info('Refreshed %d SG RPT Rows\n' % num_rows)

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
@click.option('-h', '--ltusd', is_flag=True, help='Will only update LTUSD')
@click.option('-c', '--ltcc', is_flag=True, help='Will only update LTCC')
@click.option('-s', '--safe', is_flag=True, help='Do not take volatile actions db updates etc...print summary of refresh.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def nsc_st_refresh(ltusd, ltcc, safe, log_level):

    print('')

    mis_log = mislog.mis_console_logger('nsc_st_refresh', log_level)

    if ltusd or (not ltusd and not ltcc):

        ltusd_data = misnsc.mis_ltusd_st_results_parse()

        mis_log.info('Parsed %d rows from most recent LTUSD Student Tracker results\n' % len(ltusd_data))

        if safe:

            for i in range(0, 10):
                print(ltusd_data[i])

            print('')

        else:

            mis_log.info('Refreshing LTUSD Student Tracker Results Table\n')
            num_rows = misnsc.mis_ltusd_st_results_update_db(ltusd_data)
            mis_log.info('Refreshed %d Rows in Student Tracker Results\n' % num_rows)

    if ltcc or (not ltusd and not ltcc):

        ltcc_data = misnsc.mis_ltcc_st_results_parse()

        mis_log.info('Parsed %d rows from most recent LTCC Student Tracker results\n' % len(ltcc_data))

        if safe:

            for i in range(0, 10):
                print(ltcc_data[i])

            print('')

        else:

            mis_log.info('Refreshing LTCC Student Tracker Results Table\n')
            num_rows = misnsc.mis_ltcc_st_results_update_db(ltcc_data)
            mis_log.info('Refreshed %d Rows in LTCC Student Tracker Results\n' % num_rows)

    #mis_log.info("Exec Adam's Stored procedure...")
    #misnsc.mis_st_exec_adams_sp()

@bin.command(name='ltusd_grad_refresh', help='Refresh The LTUSD data from source files')
@click.option('-p', '--path',  type=str, help='Path to LTUSD Grad Data')
@click.option('-s', '--safe', is_flag=True, help='Do not take volatile Actions...db uploads etc. Print summary of future refresh.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def ltusd_grad_refresh(path, safe, log_level):

    mis_log = mislog.mis_console_logger('ltusd_grad_refresh', log_level)

    data = misltusd.mis_ltusd_grad_parse(path)

    if safe:

        for i in range(0, 10):
            print(data[i])
        sys.exit(0)

    mis_log.info('Appending LTUSD Grad Data Table\n')
    num_rows = misltusd.mis_ltusd_grads_update_db(data)
    mis_log.info('Refreshed %d Rows to LTUSD Grad Results\n' % num_rows)

@bin.command(name='coci_refresh', help='Refresh the COCI data from Curriculum Inventory')
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

@bin.command(name='cal_grant_enr', help='Get up to date cal-grant fall enrolment')
@click.option('-s', '--safe', is_flag=True, help='Do not take volatile Actions...db uploads etc. Print summary of future refresh.')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def cal_grant_enr(safe, log_level):

    miscalgrant.mis_cg_enr_generate(None) # not implemented for other terms yet. yet...

@bin.command(name='sb_savelist', help='Build the SB savelist')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the report')
@click.option('-l', '--log-level',  type=str, default='INFO', help='Set the logging level for the command defaults to INFO, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]')
def sb_savelist(gi03, log_level):


    mis_log = mislog.mis_console_logger('sb_savelist', log_level)
    data = miserrors.sb_build_savelist(gi03)
    #print(len(data))
    #print(data[0])
    sys.exit(0)


if __name__ == "__main__":
    bin()
