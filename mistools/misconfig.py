import os
import json
import sys

from . import mislog

LIB_ROOT = os.path.dirname( os.path.realpath(__file__) )

configs_log  = mislog.mis_console_logger('configs', 'INFO')

CONFIG_FILENAME = 'configs.json'

def mis_load_config():


    # I am not super familiar with windows but I think this should be pretty standard
    # https://stackoverflow.com/questions/446209/possible-values-from-sys-platformhttps://stackoverflow.com/questions/446209/possible-values-from-sys-platform
    # a rough list of systems...
    if sys.platform.startswith('win32'): # WINDOWS
        configs_path = os.environ['USERPROFILE'] + '/Documents/MIS-Tools/%s' % CONFIG_FILENAME

    try:

        with open(configs_path) as configs_file:
            configs = json.load(configs_file)

        return configs

    except Exception as e:

        configs_log.critical('No config found at %s' % configs_path)
        print(e)

