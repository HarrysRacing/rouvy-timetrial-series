
import traceback

from datetime import datetime, timezone
from services.db_utils import get_active_series, get_access_token, get_admin, get_stages_info, get_races_list, save_rider_participant, update_stage_results, calc_stage_points, calc_gc
from services.rouvy_api import get_rouvy_race_start_list

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
    
     # get Admin RiderId
     adminRider = get_admin()
         
     #get Access Token
     accessToken = get_access_token(adminRider[0])
         
     #get list of stages for current Series  - SELECT Name, RouteName, date(StartDate), date(EndDate), Country, Distance, Ascent, Id, RouteId 
     stagesInfo = get_stages_info()
         
     for stage in stagesInfo:
         
        # get the list of scheduled races for the Series
        schedRaces = get_races_list(stage[7])
         
        #For each scheduled race get the startlist
        for race in schedRaces:
            
           eventId = race[1]
         
           # get the startlist data
           startList = get_rouvy_race_start_list(accessToken,eventId)

           #  "startlist": 
           #      "userId": "string",
           #      "username": "string",
           #      "gender": "male",
           #      "age": null,
           #      "ftp": null,
           #      "weight": null,
           #xxxx  "firstName": null,
           #xxxx  "lastName": null,
           #xxxx  "avatarUrl": null,
           #      "countryCode": null,
           #xxxx  "team": null

           # Need to save rider info, where rider does not exist OR update age, username, weight, FTP, country 
           riderId = save_rider_participant(startList)
                 
     # calculate the results for completed races and populate stageResults
     update_stage_results()
     
     #calculate positions and points and update SearchResults and GC tables
     # (re)Calculate Position and Points in StageResult table for all StageIds
     calc_stage_points()
     
     #calculate and update GC table
     calc_gc()
                       

except Exception as e:
    print('Error occurred -', e)
    traceback.print_exc()


        
  
