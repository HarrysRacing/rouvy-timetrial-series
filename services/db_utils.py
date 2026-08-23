from pathlib import Path
from datetime import date, datetime, timedelta, timezone, UTC

from services.rouvy_oauth import exchange_token 
from services.rouvy_api import get_rouvy_race_start_list

import sqlite3

EXPIRY_MARGIN = 60

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "harrysracing.db"

class DatabaseError(Exception):
   pass

  

def get_access_token(riderId):
    
   try: 
      with sqlite3.connect(DB_PATH) as conn:
         cur = conn.cursor()

         # Retrieve authorization record from db
         query = ('SELECT Id, AccessToken, RefreshToken, ExpiresAt '
               'FROM OAuthKey '
               'WHERE RiderId = ?;'
               )
         cur.execute(query,(riderId))
         oauthInfo = cur.fetchall()       
         
         if not oauthInfo:
            raise DatabaseError  (f"No OAuthKey found for Rider {riderId}")            
         
         oauthId = oauthInfo[0][0]
         accessToken = oauthInfo[0][1]
         refreshToken = oauthInfo[0][2]
         expiresAtDb = oauthInfo[0][3]         
      
         expiresAt = datetime.fromisoformat(expiresAtDb.replace("Z", "+00:00")
)
         # Check Access Token ExpiresAt
         # If still valid → return existing access token      
         if expiresAt > datetime.now(timezone.utc):
            return accessToken # return Access Token 
         else:
            # exchange the Refresh token for a new Access Token  
            tokenData = exchange_token(refreshToken)         
      
            accessToken = tokenData["access_token"]
            refreshToken = tokenData.get("refresh_token", refreshToken)
            expiresIn = tokenData["expires_in"]

            expiresAt = datetime.now(UTC) + timedelta(seconds=tokenData["expires_in"] - EXPIRY_MARGIN)
            expires_at_db = expiresAt.isoformat().replace("+00:00", "Z")

            # Store new token values and expiry
            query = ('UPDATE OAuthKey  '
                     'SET AccessToken = ?, '
                     '    RefreshToken = ?, '
                     '    ExpiresAt = ? ' 
                     'WHERE Id = ?;'
                     )
        
            cur.execute(query,(accessToken, refreshToken, expires_at_db, oauthId))       
         
         # Return valid access token
         return accessToken 

   except sqlite3.Error as error:
      raise DatabaseError("Error obtaining OAuthKey for rider {riderId}") from error

def get_active_series():
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()
      query = 'SELECT Id, Name, date(StartDate), date(EndDate), CountingStages FROM Series WHERE StartDate <= datetime("now") AND EndDate > datetime("now");'
      cur.execute(query)
      seriesInfo = cur.fetchone()
   return seriesInfo

def get_admin():
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()
      query = 'SELECT Id FROM Rider WHERE UserName = (SELECT UserName FROM Administrator);'
      cur.execute(query)
      adminId = cur.fetchall()
   return adminId


def get_full_gc_info(series_id):
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()
      query = ('SELECT G.Position, R.UserName, R.Gender, N.Nationality, A.Label, G.CountingStages, G.Points '
               'FROM GC AS G, Rider AS R, AgeGroup AS A, Nationality AS N '
               'WHERE G.SeriesId = ? '
               'AND R.ID = G.RiderId '
               'AND A.ID = R.AgeGroupId '
               'AND R.Nationality = N.CountryCode '
               'ORDER BY G.Position, G.Points ASC;'             
               ) 
            
      cur.execute(query,(series_id,))
      gcInfo = cur.fetchall()   
   return gcInfo 

def get_participants_list():
    
   series_info = get_active_series()
   
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()    
    
      query = ('SELECT R.UserName, R.Gender, A.StartAge || "-" || A.EndAge, R.Nationality '
               'FROM Rider AS R, AgeGroup AS A, Participant AS P '
               'WHERE P.SeriesId = ? '
               'AND R.Id = P.RiderId '
               'AND A.Id = R.AgeGroupId '
               'ORDER BY R.UserName;'
               )

      cur.execute(query,(series_info[0][0],))
      results = cur.fetchall()
   return results

def get_points_list():
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()

      query = 'SELECT Position, Points FROM StagePoints;'
      cur.execute(query)
      results = cur.fetchall()
   return results    
    
def get_races_list(stageId):
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()    
    
      query = ('SELECT Name, EventId, StartTime '
               'FROM Race '
               'WHERE StageId = ?;')

      cur.execute(query,(stageId,))
      results = cur.fetchall()
   return results 
 
def get_stages_info():
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor() 

      query = ('SELECT Name, RouteName, date(StartDate), date(EndDate), Country, Distance, Ascent, Id, RouteId '
               'FROM Stage '
               'WHERE SeriesId IN (SELECT Id '
               '                    FROM Series '
               '                    WHERE StartDate <= datetime("now") '
               '                    AND EndDate > datetime("now") '
               '                    );' 
               ) 
      cur.execute(query)
      results = cur.fetchall()
   return results   
    
def get_top_ten_gc_info(series_id):
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()    

      query = ('SELECT G.Position, R.UserName, R.Gender, N.Nationality, A.StartAge || "-" || A.EndAge, G.CountingStages, G.Points '
               'FROM GC AS G, Rider AS R, AgeGroup AS A, Nationality AS N '
               'WHERE G.SeriesId = ? '
               'AND R.ID = G.RiderId '
               'AND A.ID = R.AgeGroupId '
               'AND R.Nationality = N.CountryCode '
               'AND G.Position <= 10 '
               'ORDER BY G.Position, G.Points ASC;'             
               )            
      cur.execute(query,(series_id,))
      gcInfo = cur.fetchall()
   return gcInfo

def save_participant(riderId):
 
   series_info = get_active_series()
   
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()    
    
      query = ('SELECT * '
               'FROM Participant '
               'WHERE SeriesId = ? '
               'AND RiderId = ?;'
               )

      cur.execute(query,(series_info[0][0],riderId))
      participantExists = cur.fetchone()
 
      if not participantExists:
         
         query = ('INSERT INTO Participant '
                  '(SeriesId, RiderId) '
                  'VALUES (?,?);'
                  ) 
                  
         cursor.execute(query,(series_info[0][0],riderId))         
                  
   return   
 
def save_race_data(stageId, eventId, startTimeUTC, raceName):
   try:
    
      #use "with" clause to manage transaction commit or rollback depending on success
      with sqlite3.connect(DB_PATH) as conn:
         cursor = conn.cursor()    
         
         query = ('SELECT Id FROM Race '
                  'WHERE EventId = ?; '
                  )
                  
         cursor.execute(query,(eventId,))
         
         raceExists = cursor.fetchone()                    
         
         if not raceExists:
            
            query = ('INSERT INTO Race '
                     '(StageId, '
                     'EventId, '
                     'StartTime, '
                     'Name) '
                     'VALUES(?,?,?,?);'
                     )
             
            cursor.execute(query,(stageId,eventId,startTimeUTC,raceName))         
                     
      return 

   except sqlite3.Error as error:
      raise DatabaseError("Unable to save race data") from error

def save_rider_participant(riderList):
     
  try:
    
     #use "with" clause to manage transaction commit or rollback depending on success
     with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
    
        for rider in riderList["startlist"]:

           userId = rider["userId"]
           userName = rider["username"]
           gender = rider["gender"]
           age = rider["age"]
           ftp = rider["ftp"]
           weight = rider["weight"]
           country = rider["countryCode"]
        
 
           # Check if rider already exists in Rider? 
    
           query = ('SELECT Id FROM Rider WHERE UserId = ?;')
           cursor.execute(query,(userId,))
    
           riderId = cursor.fetchone()   
             
           query = ('SELECT Id FROM AgeGroup WHERE StartAge <= ? AND EndAge >= ?;')
           cursor.execute(query,(age,age))
             
           ageGroupId = cursor.fetchone() 
             
           if riderId:
        
              #if Rider record exists then refresh the fields that could have changed
              query = ('UPDATE Rider '
                       'SET UserName = ?, '
                       'AgeGroupId = ?, '
                       'CurrentWeight = ?, '
                       'CurrentFTP = ?, '
                       'Nationality = ? '
                       'WHERE Id = ?; ')
        
              cursor.execute(query,(userName,ageGroupId[0],weight,ftp,country,riderId[0]))
           
           else:
              #no Rider record exists so must create a new one 
              query = ('INSERT INTO Rider (	'
                       'UserId, '
                       'UserName, '
                       'AgeGroupId, '
                       'Gender, ' 
                       'Nationality, '
                       'CurrentWeight, '
                       'CurrentFTP) '
                       'VALUES (?,?,?,?,?,?,?) '
                       'RETURNING Id AS RiderId;')

              cursor.execute(query,(userId,userName,ageGroupId[0],gender,country,weight,ftp))
            
              riderId = cursor.fetchone()
           
           # create Participant record if it does not exist
           save_participant(riderId)
           
     return riderId
    
  except sqlite3.Error as error:
     raise DatabaseError("Unable to save rider") from error

 
def save_rider_auth(token_data,rider_profile):

# Token data: 
#   'access_token': {text-key}
#   'token_type': 'Bearer', 
#   'expires_in': 3600, 
#   'refresh_token' {text-key}

# Rider Profile:
#    "user": 
#           "userId",
#           "email", *** not used ***
#           "userName",
#           "timezoneIana", *** not used ***
#           "profilePhotoUrl", *** not used ***
#           "firstName", *** not used ***
#           "lastName", *** not used ***
#           "dateOfBirth",
#           "sex",
#           "nationalityIso3166",
#           "languageIso639",  *** not used ***
#           "weightInKilograms",
#           "heightInMeters",
#           "team", *** not used ***
#           "ftp",
#           "maxHeartRate"  *** not used ***


   expires_at = datetime.now(UTC) + timedelta(seconds=token_data["expires_in"] - EXPIRY_MARGIN)

   rider = rider_profile["user"]
    
   birthdate = datetime.strptime(rider["dateOfBirth"], '%Y-%m-%d')
   today = date.today()
   age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
 
   try:
    
      #use "with" clause to manage transaction commit or rollback depending on success
      with sqlite3.connect(DB_PATH) as conn:
         cursor = conn.cursor()
 
         # Check if OAuthKey contains a record for the RiderId ? 
    
         query = ('SELECT OA.RiderId FROM OAuthKey as OA, Rider as R WHERE OA.RiderId = R.Id AND R.UserId = ?;')
         cursor.execute(query,(rider["userId"],))
    
         riderId_for_OARider = cursor.fetchone()   
             
         query = ('SELECT Id FROM AgeGroup WHERE StartAge <= ? AND EndAge >= ?;')
         cursor.execute(query,(age,age))
             
         ageGroupId = cursor.fetchone() 
             
         if riderId_for_OARider:
        
            #if Rider record exists then refresh the fields that could have changed
            query = ('UPDATE Rider '
                    'SET UserName = ?, '
                    'AgeGroupId = ?, '
                    'CurrentWeight = ?, '
                    'CurrentFTP = ? '
                    'WHERE Id = ?; ')
        
            cursor.execute(query,(rider["userName"],ageGroupId[0],rider["weightInKilograms"],rider["ftp"],riderId_for_OARider[0]))
        
            # now update the OAuthKey with the new Token Data
            query = ('UPDATE OAuthKey '
                    'SET AccessToken = ?, '
                    'RefreshToken = ?, '
                    'ExpiresAt = ? '
                    'WHERE RiderId = ?; ')                       

            expires_at_db = expires_at.isoformat().replace("+00:00", "Z")

            cursor.execute(query,(token_data["access_token"],token_data["refresh_token"],expires_at_db,riderId_for_OARider[0]))
    
         else:
            #No record for User exists in both OAuthKey AND Rider tables - but there may still be a Rider record ?  
            #Check if Rider record for userId exists
            query = ('SELECT Id from Rider WHERE UserId = ?;')
            
            cursor.execute(query,(rider["userId"],))
            
            riderId_for_Rider = cursor.fetchone()
            
            if riderId_for_Rider:
               #if Rider record exists then refresh the fields that could have changed
               query = ('UPDATE Rider '
                        'SET UserName = ?, '
                        'AgeGroupId = ?, '
                        'CurrentWeight = ?, '
                        'CurrentFTP = ? '
                        'WHERE Id = ?; ')
        
               cursor.execute(query,(rider["userName"],ageGroupId[0],rider["weightInKilograms"],rider["ftp"],riderId_for_Rider[0]))
 
            else:
               #no Rider record exists so must create a new one 
               query = ('INSERT INTO Rider (	'
                        'UserId, '
                        'UserName, '
                        'AgeGroupId, '
                        'Gender, ' 
                        'Nationality, '
                        'CurrentWeight, '
                        'CurrentFTP)'
                        'VALUES (?,?,?,?,?,?,?,?) '
                        'RETURNING Id AS RiderId;')

               cursor.execute(query,(rider["userId"],rider["userName"],ageGroupId[0],rider["sex"],rider["nationalityIso3166"],rider["weightInKilograms"],rider["ftp"]))
           
               riderId_for_Rider = cursor.fetchone()
            
            # Either case we must create new OAuthKey record
            query = ('INSERT INTO OAuthKey ( '
                     'RiderId, '
                     'AccessToken, '
                     'RefreshToken, '
                     'ExpiresAt) '
                     'Values (?,?,?,?);')
    
            expires_at_db = expires_at.isoformat().replace("+00:00", "Z")
    
            cursor.execute(query,(riderId_for_Rider[0],token_data["access_token"],token_data["refresh_token"],expires_at_db))
            
      return
    
   except sqlite3.Error as error:
      raise DatabaseError("Unable to save rider") from error
    
def save_stage_route_data(routeId, routeName, country, distance, ascent, maxSlope, raceStartUTC):
   try:
    
      #use "with" clause to manage transaction commit or rollback depending on success
      with sqlite3.connect(DB_PATH) as conn:
         cursor = conn.cursor()    
         
         query = ('SELECT Id, RouteName FROM Stage '
                  'WHERE StartDate <= ? '
                  'AND EndDate >= ? '
                  'AND RouteId = ?;'
                  )
                  
         cursor.execute(query,(raceStartUTC,raceStartUTC,routeId))
         
         stageFound = cursor.fetchone()                     
         
         if stageFound[0] and not stageFound[1]:
            # update route data for Stage 
            
            query = ('UPDATE Stage '
                     'SET RouteName = ?, '            
                     'Country = ?, '
                     'Distance = ?, '
                     'Ascent = ?, '
                     'MaxSlope = ? '
                     'WHERE Id = ?;'
                     )
             
            cursor.execute(query,(routeName,country,distance,ascent,maxSlope,stageFound[0]))         
         elif not stageFound[0]:
              print('No Stage found for this race.')
                           
      return stageFound[0]

   except sqlite3.Error as error:
      raise DatabaseError("Unable to save stage route data") from error

def update_stage_results():

   RESULTCHECKDELTA = 7 # One week period for calculating race results, after this race results are assumed final

   try:
    
      #use "with" clause to manage transaction commit or rollback depending on success
      with sqlite3.connect(DB_PATH) as conn:
         cursor = conn.cursor() 

         # get Admin RiderId
         adminRider = get_admin()
         
         #get Access Token
         accessToken = get_access_token(adminRider[0])
         
         #get list of stages for current Series  - SELECT Name, RouteName, date(StartDate), date(EndDate), Country, Distance, Ascent, Id, RouteId 
         stagesInfo = get_stages_info()
         
         for stage in stagesInfo:
         
            stageDistance = (stage[5]*1000) #Distance in metres
            stageId = stage[7]
         
            # get the list of scheduled races for the Series
            schedRaces = get_races_list(stageId)
         
            #For each scheduled race get the startlist
            for race in schedRaces:
         
               startTime = race[2]
         
               # if race StartTime is in the past check for results, but only for races no more than RESULTCHECKDELTA days old.         
               if (startTime <= datetime.now(UTC)) and startTime > (datetime.now(UTC) - timedelta(days=RESULTCHECKDELTA)):
         
                  eventId = race[1]
         
                  # get the startlist data
                  raceResult = get_rouvy_race_result(access_token, eventId)

                  # if a result is found for the race, then...
                  if raceResult:

                     # Need to save race result against each rider in StageResult table 
                     for rider in raceResults["activities"]:
                     
                        #Fields in raceResults JSON we care about
                        # "activities": 
                        #    "userId": "string",
                        #    "routeId": null,
                        #    "distanceMeters": 1, -- should equal distance of race otherwise rider did not finish
                        #    "eventId": null,
                        #    "eventFinishTimeSeconds": null,
                        #    "aggregates": {
                        #       "powerWatts": {
                        #          "avg": 1

                        userId = rider["userId"]
                        routeId = rider["routeId"]
                        distance = rider["distanceMeters"]
                        eventId = rider["eventId"]
                        finishTimeNew = rider["eventFinishTimeSeconds"]
                        avgPower = rider["aggregates"]["powerWatts"]["avg"]

                        #get Rider data for userId
                        query = ('SELECT Id, CurrentWeight '
                                 'FROM Rider '
                                  'WHERE UserId = ?;'
                                 )      
                                 
                        cursor.execute(query,(userId,))

                        riderInfo = cursor.fetchone()

                        riderId = riderInfo[0][0]
                        riderWeight = riderInfo[0][1]                        
 
                        # did this rider complete the race ?
                        if distance >= stageDistance:
                            #yes the Rider completed the race - check if the Rider already has a result
                            
                            query = ('SELECT FinishTime '
                                     'FROM StageResult '
                                     'WHERE RiderId = ? '
                                     'AND StageId = ?;'
                                     )
                                     
                            cursor.execute(query,(stageId,riderId))
                            
                            finishTimeOld = cursor.fetchone()
                            
                            if finishTimeOld and (finishTimeOld > finishTimeNew):
                               # if the Rider has a stageResult but it is slower than the new result 
                               # then save the new result
                                
                               nowTime = datetime.now(UTC).isoformat().replace("+00:00", "Z")
                                
                               query = ('UPDATE StageResult '
                                        'SET Weight = ?, '
                                        '    AvgPower = ?, '
                                        '    FinishTime = ?, '
                                        '    RaceId = (SELECT Id FROM Race WHERE StageId = ? AND EventId = ?)'
                                        '    LastCalc = ? '                                       
                                        'WHERE StageId = ? '
                                        'AND RiderId = ?; '
                                        )
                                         
                               cursor.execute(query,(riderWeight,avgPower,finishTimeNew,nowTime,stageId,riderId))                                               
                                
                            else: # no record in StageResult for Stage/Rider so create one
                            
                               query = ('INSERT INTO StageResult '
                                        '(StageId, RiderId, Weight, AvgPower, FinishTime, RaceId, LastCalc) '
                                        'VALUES(?,?,?,?,?,(SELECT Id FROM Race WHERE StageId = ? AND EventId = ?),?);'
                                        )

   except sqlite3.Error as error:
      raise DatabaseError("Unable to update database with startlist data") from error   

    
def update_start_list():

   try:
    
      #use "with" clause to manage transaction commit or rollback depending on success
      with sqlite3.connect(DB_PATH) as conn:
         cursor = conn.cursor() 

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
               

   except sqlite3.Error as error:
      raise DatabaseError("Unable to update database with startlist data") from error   
  