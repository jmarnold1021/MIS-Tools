import json
import os

LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )
DED_MIS_SPEC_PATH = "%s/spec/mis_spec.json" % LIB_ROOT

with open(DED_MIS_SPEC_PATH) as mis_spec_file:
    DED_MIS_SPEC = json.load(mis_spec_file)

def mis_get_spec(indent=4, prnt = False):
    '''
    Retrieve/Print the MIS Specification JSON, mainly used for documenting
    the spec. :orangebold:`Could potentially replace the file source in other tools`

    :param int indent: JSON indentation, defaults to 4

    :param bool prnt: print the spec to STDOUT, defaults to False

    :return: The MIS spec in JSON format.

    :rtype: str

    '''
    if prnt: # get prnt bruh

        print(json.dumps(DED_MIS_SPEC, indent=indent))

    return json.dumps(DED_MIS_SPEC, indent=indent)

