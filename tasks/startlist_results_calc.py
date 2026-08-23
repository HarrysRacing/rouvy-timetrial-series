import sqlite3

from datetime import datetime, timezone
from services.db_utils import get_active_series, update_start_list

# ***
# This script should be scheduled to run every 30 mins
# 1. Check if any Series is active - if not sleep.
# -  For an active Series [ there will only be one active Series at any time ]
# 2.    For all races that are scheduled get the startlist data (via API) and populate the Rider table 
# -     The Startlist data from ROUVY can be used to populate the Rider and Participant tables 
# 3.    For all races that are completed ie passed Starttime,  
#           get the results (via API) and populate the StageResult (results data) and GC tables (includes calculating positions and points)
# ***

try:
   activeSeries = get_active_series()

   if activeSeries:

    # For the active Series, create or update the Startlist data (Rider and Participant tables)
    update_start_list()

    # calculate the results for completed races and populate stageResults
    update_stage_results()


except sqlite3.Error as error:
    print('Error occurred -', error)


        
  
