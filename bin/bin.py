import click # cli dependancy
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append("%s/../../MIS-Tools" % SCRIPT_DIR)

from mistools import misflatfile
from mistools import misdod
from mistools.db import DB

@click.group(name='bin')
def bin():
    pass

@bin.command(name='mis_export', help='Update MIS DB staging tables from submission Flat Files')
@click.option('-r', '--report', type=str, help='The MIS report to upload to the table')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the report')
@click.option('-s', '--sql-only', is_flag=True, type=bool, help='Print the SQL rather than create the export')
def mis_export(report, gi03, sql_only):

    EXPORT_FUNC = "misflatfile.%s_mis_export" % report.lower()
    EXPORT_PATH = '//ltcc-app/MIS/%s/' % gi03

    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)

    print(sql_only)

    print("Generating %s Export Query for %s" % (report.upper(), gi03))
    print(eval(EXPORT_FUNC)(gi03, EXPORT_PATH, sql_only))


@bin.command(name='update_mis_db', help='Update MIS DB staging tables from submission Flat Files')
@click.option('-r', '--report', type=str, help='The MIS report to upload to the table')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the report')
@click.option('--debug', is_flag=True, type=bool, help='Enable debug mode')
def update_mis_db(report, gi03, debug):

    PARSE_FUNC = "misflatfile.%s_mis_parse" % report.lower()
    MIS_FF_PATH = '//ltcc-app/MIS/%s/U22%s%s.DAT' % (gi03,
                                                     gi03,
                                                     report.upper())

    try:
        if report.upper() in ['XB','XE','XF']:

            PARSE_FUNC = "misflatfile.%s_mis_parse" % 'xb'
            MIS_FF_PATH = '//ltcc-app/MIS/%s/U22%s%s.DAT' % (gi03,
                                                             gi03,
                                                             'XB')

            data = eval(PARSE_FUNC)(MIS_FF_PATH)
            data = data[report.upper()]
        else:
            data = eval(PARSE_FUNC)(MIS_FF_PATH)

    except FileNotFoundError as e:
        print('No submission found for %s in term %s' % (report.upper(), gi03))
        sys.exit(1)

    if debug: # allows a quick print of top rows to verify POSITIONS DED spec...

        print('\nTop row\n')
        for i in range(0,9):
            print(data[i])
        print("\n%s will update %d rows\n" % (report.upper(), len(data)))
        sys.exit(0)


    db = DB('mis') # start db con

    # super safe....
    rows = db.exec_query("SELECT COUNT(*) FROM %s_STAGING WHERE GI03 = '%s'" % (report.upper(), gi03))

    if rows[0][0] != 0: # basically top left of grid

        print("%s already updated for %s" % (report.upper(), gi03))
        db.close() # close db con
        sys.exit(1)


    # everything ok update with 'python update.py CW 222 0' -- at end says verified
    cnt = db.insert_batch('%s_STAGING' % report.upper(), data) # insert data
    print('Inserted %d rows into %s_STAGING' % (cnt, report.upper()))

    db.close() # close db con

    sys.exit(0)

@bin.command(name='update_mis_db_ccccoid', help='Update MIS DB CCCCO Ids table')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the Stu Ref file to upload')
@click.option('--debug', is_flag=True, type=bool, help='Enable debug mode')
def update_mis_db_ccccoid(gi03, debug):

    id_data = misdod.ccccoid_dod_parse("//ltcc-app/MIS/Data_On_Demand/Referential/Non-Term/NonTerm/%s-StuIDRef.txt" % gi03, fill_empty='NA')

    if debug: # allows a quick print of top rows to verify POSITIONS DED spec...

        print('\nTop row\n')
        for i in range(0,9):
            print(id_data[i])
        print("\n Will upload %d CCCCOIDS\n" % len(id_data))
        sys.exit(0)

    db = DB('mis')
    db.exec_query('TRUNCATE TABLE CCCOID2SB00')
    cnt = db.insert_batch( 'CCCOID2SB00', id_data)
    print('Inserted %d rows into %s' % (cnt, 'CCCOID2SB00'))

    db.close()

    sys.exit(0)

@bin.command(name='update_mis_db_xbd', help='Update MIS DB XBD staging table from DOD files')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the XBD report')
@click.option('--debug', is_flag=True, type=bool, help='Enable debug mode')
def update_mis_db_xbd(gi03, debug):

    DOD_XBD_PATH_TEMPLATE = "//ltcc-app/MIS/Data_On_Demand/Referential/Quarterly/%s/XB%s.txt"

    try:
        xbd_data = misdod.xb_dod_parse(DOD_XBD_PATH_TEMPLATE % (gi03, gi03), fill_empty='NA', dict_read=True)
    except FileNotFoundError as e:
        print('No Data On Demand referential data found for XBD found for term %s' % gi03)
        sys.exit(0)

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

    if debug: # allows a quick print of top row to verify POSITIONS DED spec...

        print('\nTop row\n')
        for i in range(0, 9):
            print(xbd_rows[i])

        print("\nXBD will update %d rows\n" % len(xbd_data))
        sys.exit(0)

    db = DB('mis')
    rows = db.exec_query("SELECT COUNT(*) FROM XBD_STAGING WHERE GI03 = '%s'" % gi03)

    if rows[0][0] != 0: # basically top left of grid

        print("XBD already updated for %s" %  gi03)
        db.close() # close db con
        sys.exit(1)

    cnt = db.insert_batch('XBD_STAGING', xbd_rows)

    print('Inserted %d rows into XBD_STAGING' % cnt)

    db.close()
    sys.exit(0)

@bin.command(name='update_mis_db_std', help='Update MIS DB ST staging table from DOD files')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the ST report')
@click.option('--debug', is_flag=True, type=bool, help='Enable debug mode')
def update_mis_db_std(gi03, debug):

    DOD_STD_PATH_TEMPLATE = "//ltcc-app/MIS/Data_On_Demand/Referential/Quarterly/%s/ST%s.txt"

    db = DB('mis')
    id_data = db.exec_query('SELECT * FROM CCCOID2SB00', dict_read=True)

    id_map = {}
    for row in id_data:
        id_map[row['CCCOID']] = row['SB00']

    std_data = misdod.sx_dod_parse(DOD_STD_PATH_TEMPLATE % (gi03, gi03), fill_empty='NA', dict_read=True)

    std_rows = []
    bad_cccco_ids = [] # bad stuff

    for row in std_data:

        std_row = []

        cccco_id = row['CCCC0_Assigned']
        if cccco_id not in id_map:
            bad_cccco_ids.append(cccco_id) # ids's from data files not found in ref
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

    if debug: # allows a quick print of top row to verify POSITIONS DED spec...

        print('\nTop row\n')
        for i in range(0, 9):
            print(std_rows[i])

        print("\nSTD will update %d rows\n" % len(std_rows))
        print("\nUnmatched IDS\n")
        print(bad_cccco_ids)
        sys.exit(0)

    #cnt = db.insert_batch('ST_STAGING', std_rows)

    #print('Inserted %d rows into %s' % (cnt, 'ST_STAGING'))

    db.close()
    sys.exit(0)

@bin.command(name='update_mis_db_sxd', help='Update MIS DB SXD staging table from DOD files')
@click.option('-g', '--gi03', type=str, help='The GI03 term for the SXD report')
@click.option('--debug', is_flag=True, type=bool, help='Enable debug mode')
def update_mis_db_sxd(gi03, debug):

    DOD_SX_PATH_TEMPLATE = "//ltcc-app/MIS/Data_On_Demand/Referential/Quarterly/%s/SX%s.txt"

    db = DB('mis')
    id_data = db.exec_query('SELECT * FROM CCCOID2SB00', dict_read=True)

    id_map = {}
    for row in id_data:
        id_map[row['CCCOID']] = row['SB00']

    sxd_data = misdod.sx_dod_parse(DOD_ST_PATH_TEMPLATE % (gi03, gi03), fill_empty='NA', dict_read=True)

    sxd_rows = []
    bad_cccco_ids = [] # bad stuff

    for row in sxd_data:
        sxd_row = []

        cccco_id = row['CCCC0_Assigned']
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
            sxd_line.append(str(int(float(row['SXD4'])))) # sxd4
        else:
            sxd_line.append(str(round(float(row['SXD4']), 1))) # sxd4

        sxd_row.append(row['XB00']) # xb00
        sxd_row.append(row['CB01']) # cb01
        sxd_row.append(row['CB00']) # cb00

        sxd_rows.append(sxd_row)

    if debug: # allows a quick print of top row to verify POSITIONS DED spec...

        print('\nTop row\n')
        for i in range(0, 9):
            print(sxd_rows[i])

        print("\nSXD will update %d rows\n" % len(sxd_rows))
        print("\nUnmatched IDS\n")
        print(bad_cccco_ids)
        sys.exit(0)

    #cnt = db.insert_batch('SXD_STAGING', sxd_rows)
    #print('Inserted %d rows into %s' % (cnt, 'SXD_STAGING'))

    db.close()
    sys.exit(0)

if __name__ == "__main__":
    bin()
