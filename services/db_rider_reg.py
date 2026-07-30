from pathlib import Path
from datetime import date, datetime, timedelta, UTC
import sqlite3

class DatabaseError(Exception):
   pass
  
def save_rider_auth(token_data,rider_profile):

# save_rider_auth could be called for a re-registration where the refresh_token expired. So must code accordingly.

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

   db_path = Path(__file__).resolve().parent.parent / "database" / "harrysracing.db"

   EXPIRY_MARGIN = 60

   expires_at = datetime.now(UTC) + timedelta(seconds=token_data["expires_in"] - EXPIRY_MARGIN)

   rider = rider_profile["user"]
    
   birthdate = datetime.strptime(rider["dateOfBirth"], '%Y-%m-%d')
   today = date.today()
   age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
 
   try:
    
      #use "with" clause to manage transaction commit or rollback depending on success
      with sqlite3.connect(db_path) as conn:
         cursor = conn.cursor()
 
         # Check if OAuthKey contains a record for the RiderId ? 
    
         query = ('SELECT OA.RiderId FROM OAuthKey as OA, Rider as R WHERE OA.RiderId = R.Id AND R.UserId = ?;')
         cursor.execute(query,(rider["userId"],))
    
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
                    'TimeZone = ? '
                    'WHERE RiderId = ?; ')
        
            cursor.execute(query,(rider["userName"],ageGroupId[0],rider["weightInKilograms"],rider["ftp"],rider["timezoneIana"],riderId[0]))
        
            # now update the OAuthKey with the new Token Data
            query = ('UPDATE OAuthKey '
                    'SET AccessToken = ?, '
                    'RefreshToken = ?, '
                    'ExpiresAt = ? '
                    'WHERE RiderId - ?; ')                       

            cursor.execute(query,(token_data["access_token"],token_data["refresh_token"],expires_at,riderId[0]))
    
         else:
            # There is a 1 to 1 mandatory relationship Rider to OAuthKey, so they either both exist or not
            # so if we have to INSERT one we have to INSERT the other.
               
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
           
            riderId = cursor.fetchone()
            
            query = ('INSERT INTO OAuthKey ( '
                    'RiderId, '
                    'AccessToken, '
                    'RefreshToken, '
                    'ExpiresAt) '
                    'Values (?,?,?,?);')
    
            cursor.execute(query,(riderId[0],token_data["access_token"],token_data["refresh_token"],expires_at))
            
      return
    
   except sqlite3.Error as error:
      raise DatabaseError("Unable to save rider") from error
    
