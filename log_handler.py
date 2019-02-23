import time
import re
import os
import stat
import logging
from logging.handlers import RotatingFileHandler

def setup_debug_log():
    log_formatter = logging.Formatter('%(asctime)s -- %(message)s')
    debug_log_file = 'debug.log'
    # 20MB allocated for the main debug log file, one for the current, and one backup.
    handler = RotatingFileHandler(debug_log_file, mode='a', maxBytes=10*1024*1024,
                                         backupCount=1, encoding=None, delay=0)
    handler.setFormatter(log_formatter)
    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)
    app_log.addHandler(handler)
    return app_log