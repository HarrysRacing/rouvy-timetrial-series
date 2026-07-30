import requests

ROUVY_API_ME = "https://api.rouvy.com/me"

#RouvyAPIError class defined to inherit from python Exception class and enable easy RouvyAPIError identification  
class RouvyAPIError(Exception):
    pass  #do nothing and continue, so allows for basic inheritance nothing else

def get_rouvy_rider(access_token):


    try:
  
       profile_response = requests.get(ROUVY_API_ME,headers={"Authorization": f"Bearer {access_token}"} )

       # 200 Success returns: 
       #                "user": 
       #                    "userId",
       #                    "email",
       #                    "userName",
       #                    "timezoneIana",
       #                    "profilePhotoUrl",
       #                    "firstName",
       #                    "lastName",
       #                    "dateOfBirth",
       #                    "sex",
       #                    "nationalityIso3166",
       #                    "languageIso639",
       #                    "weightInKilograms",
       #                    "heightInMeters",
       #                    "team",
       #                    "ftp",
       #                    "maxHeartRate"
    
    except requests.RequestException as error:

       raise RouvyAPIError(
            "Unable to contact ROUVY API"
       ) from error

    if profile_response.status_code != 200:

       raise RouvyAPIError(
             f"ROUVY user request failed: HTTP {profile_response.status_code}"
       )
    

    try:

        return profile_response.json()

    except ValueError as error:

        raise RouvyAPIError(
            "ROUVY returned invalid JSON"
        ) from error

    
def get_access_token(riderId):

#1. Retrieve authorization record from db
#2. Check AccessTokenExpiresAt
#3. If still valid → return existing access token
#4. If near expiry → refresh it
#5. Store new token values and expiry
#6. Return valid access token

    return access_token  