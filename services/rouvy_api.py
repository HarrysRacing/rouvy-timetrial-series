import requests

ROUVY_API_ME = "https://api.rouvy.com/me"
ROUVY_API_EVENT = "https://api.rouvy.com/events/"

#RouvyAPIError class defined to inherit from python Exception class and enable easy RouvyAPIError identification  
class RouvyAPIError(Exception):
    pass  #do nothing and continue, so allows for basic inheritance nothing else

def get_rouvy_race_info(access_token, event_id):

    try:
  
       #build ROUVY API EVent URL
       ROUVY_API_EVENT_URL = ROUVY_API_EVENT + event_id  
       
       print("Event ID:", event_id)
       print("URL:", ROUVY_API_EVENT_URL)

       
       event_response = requests.get(ROUVY_API_EVENT_URL,headers={"Authorization": f"Bearer {access_token}"} )

       print("HTTP:", event_response.status_code)

       # 200 Success returns (Key fields): 
       #     "event": 
       #             "eventId": "string",
       #             "type": "race",
       #             "status": "offline",
       #             "accessibility": "public",
       #             "title": "string",
       #             "startDateTimeUtc": "string",
       #             "capacity": 1,
       #             "route": {
       #                     "routeId": "string",
       #                     "name": "string",
       #                     "countryCodeISO": null,
       #                     "thumbnailUrl": null,
       #                     "distanceMeters": 1,
       #                     "ascendedMeters": 1,
       #                     "slope": {
       #                             "maxPercent": 1,
       #                             "avgPercent": 1  
   
    
    
    except requests.RequestException as error:

       raise RouvyAPIError(
            "Unable to contact ROUVY API"
       ) from error

    if event_response.status_code != 200:

       raise RouvyAPIError(
             f"ROUVY event request failed: HTTP {event_response.status_code}"
       )
    

    try:

        return event_response.json()

    except ValueError as error:

        raise RouvyAPIError(
            "ROUVY returned invalid JSON"
        ) from error


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

    
 