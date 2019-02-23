# general imports
import os
from os.path import getmtime
import sys
import time
import logging
import datetime
from datetime import timedelta
import traceback
import simplejson as json
import requests
from rollbar import *
from settings import *
from log_handler import *
from web import *
app_log = setup_debug_log()

# True: Print debug statements to console
# False: Writes them to the log
# For a compiled windows service this must be False or the service will crash (no window to write to)
DEBUG = False

# True: For a Compiled Windows Service
# False: If using linux; any self-restarts will occur via by executing script name, not killing the process.
SERVICE_MODE = True

def debug_log(string):
    if DEBUG == True:
        print(string)
        app_log.info(string)
    else:
        app_log.info(string)

def restart_application(service_mode):
    if service_mode is True:
        sys.exit('Force-quitting app, so service manager restarts it.')
    else:
        os.execv(sys.executable, ['python'] + sys.argv)

def handle_network_failure():
    for i in range(FAILURE_RECOVERY_DELAY): # default is 4 hours
        online = check_network()
        debug_log("Internet Up?: %s" % online)
        if online:
            debug_log("Connection Resumed - Restarting service in 10 seconds")
            time.sleep(10)
            restart_application(SERVICE_MODE)
        else:
            debug_log("Internet connection test failed - Retrying every %s min until success" % str(RETRY_DELAY / 60))
            time.sleep(RETRY_DELAY)

def try_until_db_success(myargs):
    # useful wrapper if you wanna keep trying something until it succeeds. (database is sometimes offline for backups, etc)
    for i in range(FAILURE_RECOVERY_DELAY): # default is 4 hours
        query_result = some_data_query

        if my_success_condition:
            return query_result
        else:
            debug_log("DB Connection or data query failed. Retrying every %s mins until db success" % str(RETRY_DELAY / 60))
            time.sleep(RETRY_DELAY)            

def main():
    try:
        while(1):
            # put your service logic here 
            debug_log("Give me some purpose, I feel empty inside.")
            
            # Run any pending scheduled tasks
            # schedule.run_pending()

            debug_log("Sleeping for %d seconds" % SLEEP_DELAY)
            time.sleep(SLEEP_DELAY)
    except Exception as e:
        tb = traceback.format_exc()
        debug_log("GENERIC EXCEPTION: %s" % tb)

        if DEBUG == False:
            report_generic_exception(tb) # report to rollbar, but only in "production mode"

# setup any desired scheduled tasks before calling main loop
# schedule.every().day.at("00:00").do(my_method_name)
main()
