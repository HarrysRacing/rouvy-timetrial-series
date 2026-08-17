from pathlib import Path
from datetime import date, datetime, timedelta, timezone, UTC

from services.rouvy_oauth import exchange_token 

import sqlite3

EXPIRY_MARGIN = 60

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "harrysracing.db"

class DatabaseError(Exception):
   pass

def get_access_token(riderId):
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()

      # Retrieve authorization record from db
      query = ('SELECT Id, AccessToken, RefreshToken, ExpiresAt '
               'FROM OAuthKey '
               'WHERE RiderId = ?;'
               )
      cur.execute(query,(riderId))
      oauthInfo = cur.fetchall()       
               
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

def get_active_series():
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()
      query = 'SELECT Id, Name, date(StartDate), date(EndDate), CountingStages FROM Series WHERE StartDate <= datetime("now") AND EndDate > datetime("now");'
      cur.execute(query)
      results = cur.fetchall()
   return results

def get_full_gcinfo(series_id):
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
      results = cur.fetchall()   
   return results 

def get_participantslist():
    
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

def get_pointslist():
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()

      query = 'SELECT Position, Points FROM StagePoints;'
      cur.execute(query)
      results = cur.fetchall()
   return results    
    
def get_raceslist(stageId):
   with sqlite3.connect(DB_PATH) as conn:
      cur = conn.cursor()    
    
      query = ('SELECT Name, EventId, StartTime '
               'FROM Race '
               'WHERE StageId = ?;')

      cur.execute(query,(stageId))
      results = cur.fetchall()
   return results 
 
def get_stagesinfo():
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
    
def get_topten_gcinfo(series_id):
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
      results = cur.fetchall()
   return results
 
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
#           "timezoneIana",
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
                    'CurrentFTP = ?, '
                    'TimeZone = ? '
                    'WHERE Id = ?; ')
        
            cursor.execute(query,(rider["userName"],ageGroupId[0],rider["weightInKilograms"],rider["ftp"],rider["timezoneIana"],riderId_for_OARider[0]))
        
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
                        'CurrentFTP = ?, '
                        'TimeZone = ? '
                        'WHERE Id = ?; ')
        
               cursor.execute(query,(rider["userName"],ageGroupId[0],rider["weightInKilograms"],rider["ftp"],rider["timezoneIana"],riderId_for_Rider[0]))
 
            else:
               #no Rider record exists so must create a new one 
               query = ('INSERT INTO Rider (	'
                        'UserId, '
                        'UserName, '
                        'AgeGroupId, '
                        'Gender, ' 
                        'Nationality, '
                        'CurrentWeight, '
                        'CurrentFTP, '
                        'TimeZone)'
                        'VALUES (?,?,?,?,?,?,?,?) '
                        'RETURNING Id AS RiderId;')

               cursor.execute(query,(rider["userId"],rider["userName"],ageGroupId[0],rider["sex"],rider["nationalityIso3166"],rider["weightInKilograms"],rider["ftp"],rider["timezoneIana"]))
           
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

         print('stageFound ; ',stageFound)                  
         
         if stageFound[0] and not stageFound[1]:
            # update route data for Stage 
            print('Update Stage')
            
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
    
    
  