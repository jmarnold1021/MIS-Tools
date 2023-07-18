import os
import pyodbc
import json
import re
from datetime import datetime
from dateutil import parser # for string dates with no format...

# lib deps
from .lib import ffparser
from . import mislog

LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )
MIS_320_SPEC_PATH = "%s/spec/mis_320_spec.json" % LIB_ROOT

CONFIGS_PATH = "%s/../configs/configs.json" % LIB_ROOT # currently from lib root...
with open(CONFIGS_PATH) as configs:
    CONFIGS = json.load(configs)

with open(MIS_320_SPEC_PATH) as mis_spec_file:
    MIS_320_SPEC = json.load(mis_spec_file)

mis320_log  = mislog.mis_console_logger('mis320', CONFIGS['MIS_320']['LOG_LEVEL'])


# the text version atm.
def mis_320_summary_parse(summary_file):

    '''
    Parse the provided 320 Summary file after Conversion to Flat File using PDFMiner.

    :param str summary_file: summary file to parse

    :rtype: list

    '''


    MIS_320_SUMMARY_SPEC = MIS_320_SPEC['320_SUMMARY']

    k0_regexp = None
    k0_spec   = None

    k1_regexp = None
    k1_spec   = None

    k2_regexp = None
    k2_spec   = None

    h0_regexp = None
    h0_spec   = None

    d0_regexp = None
    d0_spec = None

    for line_spec in MIS_320_SUMMARY_SPEC:

        if line_spec == "K0":
            k0_regexp = re.compile(MIS_320_SUMMARY_SPEC[line_spec]['LINE_ID'])
            k0_spec   = MIS_320_SUMMARY_SPEC[line_spec]['SPEC']

        if line_spec == "K1":
            k1_regexp = re.compile(MIS_320_SUMMARY_SPEC[line_spec]['LINE_ID'])
            k1_spec   = MIS_320_SUMMARY_SPEC[line_spec]['SPEC']

        if line_spec == "K2":
            k2_regexp = re.compile(MIS_320_SUMMARY_SPEC[line_spec]['LINE_ID'])
            k2_spec   = MIS_320_SUMMARY_SPEC[line_spec]['SPEC']

        if line_spec == "H0":
            h0_regexp = re.compile(MIS_320_SUMMARY_SPEC[line_spec]['LINE_ID'])
            h0_spec   = MIS_320_SUMMARY_SPEC[line_spec]['SPEC']

        if line_spec == "D0":

            d0_regexp = re.compile(MIS_320_SUMMARY_SPEC[line_spec]['LINE_ID'])
            d0_spec   = MIS_320_SUMMARY_SPEC[line_spec]['SPEC']


    f = open(summary_file)
    data = f.readlines()
    f.close()

    data_a = []
    for line in data:

        if '320 SECTION SUMMARY REPORT' in line:

            idx = 1
            continue

        if idx == 1:

            idx -= 1 # remove line after 320...
            continue

        data_a.append(line)

    # parse the txt file...
    data = data_a

    data_f = []
    data_b = []
    header = []
    header_done = False

    data_k = []
    for line in data:


        if k0_regexp.search(line):

            data_k = [] #reset data_k any time we see a k0 line
            k0_data = ffparser.parse_lines(k0_spec, line, None)
            for tok in k0_data[0]:

                tok_comp = tok.split(':', 1) # first occurance
                if len(data_f) == 0:

                    header.append(tok_comp[0])

                data_k.append('"' +tok_comp[1]+'"')

        if k1_regexp.search(line):

            k1_data = ffparser.parse_lines(k1_spec, line, None)
            for tok in k1_data[0]:

                tok_comp = tok.split(':', 1) # first occurance
                if len(data_f) == 0:
                    header.append(tok_comp[0])


                print(tok_comp[1])
                data_k.append('"' +tok_comp[1]+'"')


        if k2_regexp.search(line):

            k2_data = ffparser.parse_lines(k2_spec, line, None)
            for row in data_b:
                row.append(k2_data[0][0])
            data_f += data_b
            data_b = []

        if h0_regexp.search(line):


            h0_data = ffparser.parse_lines(h0_spec, line, None)

            if len(data_f) == 0:

                header += h0_data[0]
                header.append('Term')
                data_f.append(header)


        if d0_regexp.search(line):
            d0_data = ffparser.parse_lines(d0_spec, line, None)
            for row in d0_data:
                row_adj = map(lambda x: '"' + x.replace(',','') + '"', row)
                data_b.append(data_k + list(row_adj))


    ##text=List of strings to be written to file
    with open('320_Summary.csv','w') as file:
        for row in data_f:
            s = ','.join(row)
            file.write(s)
            file.write('\n')



