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


CONFIGS = misconfig.mis_load_config()
MIS_CG_CONFIGS = CONFIGS['MIS_CALGRANT']


def mis_cg_enr_generate(fall_term):

    sql = """

        SELECT DISTINCT(REPLACE(p.SSN,'-','')) AS SSN

        FROM STUDENT_ACAD_CRED sac
             INNER JOIN STC_STATUSES ss ON sac.STUDENT_ACAD_CRED_ID = ss.STUDENT_ACAD_CRED_ID
                                           AND POS = 1
             INNER JOIN PERSON p ON p.ID = sac.STC_PERSON_ID

        WHERE sac.STC_TERM = '2023FA'
              AND ss.STC_STATUS in ('A', 'NR')
              AND  p.SSN IS NOT NULL
              AND LEFT(p.SSN,3) <> '000'
              AND LEFT(p.SSN,1) <> '9'
              AND LEN(p.SSN) = 11

    """

    db = DB(MIS_CG_CONFIGS['SRC_DB_NAME'])

    data = db.exec_query(sql)

    today = datetime.today().strftime("%m%d%y")
    filename = '012907-ENR'

    with open(MIS_CG_CONFIGS['DST_FF_PATH'] + '/' + filename, 'w') as file:

        for line in data:

            file.write(line[0])
            file.write('\n')



