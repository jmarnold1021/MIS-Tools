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


LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )
#DOD_MIS_SPEC_PATH = "%s/spec/mis_dod_spec.json" % LIB_ROOT
#DOD_IPEDS_SPEC_PATH = "%s/spec/mis_ipeds_spec.json" % LIB_ROOT
#DOD_SCFF_SPEC_PATH = "%s/spec/mis_scff_spec.json" % LIB_ROOT
#DOD_SCHEMA_PATH = "%s/schema/" % LIB_ROOT
#DOD_SCHEMA_TEMPLATE = DOD_SCHEMA_PATH + 'dbo.L56_DOD_%s.Table.sql'
#
#
## read in specs for different report/s
#with open(DOD_MIS_SPEC_PATH) as dod_spec_file:
#    DOD_MIS_SPEC = json.load(dod_spec_file)
#
#with open(DOD_IPEDS_SPEC_PATH) as dod_spec_file:
#    DOD_IPEDS_SPEC = json.load(dod_spec_file)
#
#with open(DOD_SCFF_SPEC_PATH) as dod_spec_file:
#    DOD_SCFF_SPEC = json.load(dod_spec_file)
#
## DB configs
CONFIGS_PATH = "%s/../configs/configs.json" % LIB_ROOT
with open(CONFIGS_PATH) as configs:
    CONFIGS = json.load(configs)
#
MIS_RPT_CONFIGS = CONFIGS['MIS_RPT']
#
#
## set up global lib logger
rpt_log  = mislog.mis_console_logger('misdod', MIS_RPT_CONFIGS['LOG_LEVEL'])

def mis_rpt_cb_refresh():

   pass

