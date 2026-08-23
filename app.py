# import the Flask library
from flask import Flask, render_template, redirect, request, logging

#import datetime functions
from datetime import datetime

#import function to retrieve active series data
from services.db_utils import get_points_list, get_participants_list, get_races_list, get_active_series, get_stages_info, get_top_ten_gc_info, save_rider_auth, DatabaseError
from services.rouvy_oauth import get_oauth_url, get_token, RouvyOAuthError
from services.rouvy_api import get_rouvy_rider,  RouvyAPIError

# app is a standard construct in Flask and where app.py is called from a python session "__name__" will be set by python to "__main__"
# hence further down the app.run will be triggered in debug mode
# if app.py were to be called as part of, or from, a module "__name__" would equate to the module name and app.run would not trigger
# Further to this __name__ equates not only to the calling module name, but also the full path, held in teh metadata by python. 
# So Flask therefore knows the location of the calling module and uses this to locate the relevant folders, such as templates, static etc...
app = Flask(__name__)

# app.route() is a standard flask decorator function that works as:
# when the root "/" URL is entered in the browser, app.route("/") matches this and calls the home() function that returns/renders index.html 
# which flask will look for in the standard templates folder
#note the "home" function could in this case be named anything you choose

@app.route("/about")
def about():
    return render_template("about.html") 

@app.route("/authorize")
def authorize():
    auth_url = get_oauth_url()
    return redirect(auth_url)

@app.route("/auth/callback")
def callback():
    
    try:
    
       code = request.args.get("code")

       if not code:
          app.logger.warning("No authorization code returned by ROUVY")
          return render_template("registration_error.html") 
           
       # Exchange the Auth Code for the Token data
       token_data = get_token(code)

       #Get the Rouvy Rider Profile via Rouvy API
       rouvy_rider_profile = get_rouvy_rider(token_data["access_token"])

       #Store authorization and Rider Profile in the database
       save_rider_auth(token_data,rouvy_rider_profile)
   
       return render_template("registration_success.html")
   
    except (RouvyOAuthError, RouvyAPIError, DatabaseError) as error:

       # Log the technical error
       app.logger.exception("ROUVY registration failed.")

       return render_template("registration_error.html")

@app.route("/guide")
def guide():
    return render_template("guide.html")

@app.route("/")
def home():
    series_info = get_active_series()
    
    #stages_info : Name, RouteName, StartDate, EndDate, Country, Distance, Ascent, Id, RouteId
    stages_info = get_stages_info()
    
    gc_info = get_top_ten_gc_info(series_info[0][0])
       
    # Parse the ISO 8601 date
    start_dt = datetime.fromisoformat(series_info[0][2])
    end_dt = datetime.fromisoformat(series_info[0][3])
    
    # Format to dd-mmm-yyyy
    start_dt_fmt = start_dt.strftime('%d-%b-%Y')
    end_dt_fmt = end_dt.strftime('%d-%b-%Y')
    
    stage_list = []
    
    for row in stages_info:
         
         # Parse the ISO 8601 date
         stageS_dt = datetime.fromisoformat(row[2])
         stageE_dt = datetime.fromisoformat(row[3])
    
         li = list(row)
         
         # Format to dd-mmm-yyyy
         li[2] = stageS_dt.strftime('%d-%b-%Y')
         li[3] = stageE_dt.strftime('%d-%b-%Y')
         
         today = datetime.now().date()
         
         #mark stage as "complete" or "active"
         stage_end = stageE_dt.date()
         status = "complete" if stage_end < today else "active"

         li.append(status)
         
         row = tuple(li)
         
         stage_list.append(row)         
    
    return render_template("index.html", name=series_info[0][1], start_date=start_dt_fmt,end_date=end_dt_fmt,
                            counting_stages=series_info[0][4], stage_tbl=stage_list, gc_tbl=gc_info)
    
# there are no links to this from the webpage, so just here to address a manual entry in browser with index url
@app.route("/index")
def index():
    return render_template("index.html", name="Fred")
    
@app.route("/participants")
def participants():
    series_info = get_active_series()
    
    participants_list = get_participants_list()
    
    return render_template("participants.html", name=series_info[0][1], participants_tbl=participants_list)
    
@app.route("/points")
def points():
    series_info = get_active_series()
    
    points_list = get_points_list()
    
    return render_template("points.html", name=series_info[0][1], points_tbl=points_list)  

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")  

@app.route("/register")
def register():
    return render_template("register.html") 

@app.route("/rouvy_races")
def rouvy_races():

    # stageId and stageName passed in as commandline arguments in index.html, when calling rouvy_races.html
    stageId = request.args.get("stageId")
    stageName = request.args.get("stageName")

    series_info = get_active_series()
    
    races_info = get_races_list(stageId)
    
    races_list = []
    
    for row in races_info:
         
         # Parse the ISO 8601 date
         start_dt = datetime.fromisoformat(row[2])

        # date = start_dt.strftime("%d-%b-%Y")
        # time = start_dt.strftime("%H:%M")     
        # day = start_dt.strftime("%A")
    
         li = list(row)
         
         # Format to dd-mmm-yyyy
         li[2] = start_dt

         #li.append(date)
         #li.append(time)
         
         row = tuple(li)
         
         races_list.append(row)
   
    return render_template("rouvy_races.html", series_name=series_info[0][1], stage_name=stageName, races_tbl=races_list)

@app.route("/terms")
def terms():
    return render_template("terms.html")  


# Start with flask web app, with debug as True,
# only if this is the starting page
#The __name__ is a built-in special variable that evaluates the name of the current module. 
#If the source file is executed as the main program, the interpreter sets the __name__ variable to have a value “__main__”. 
#If this file is being imported from another module, __name__ will be set to the module’s name
if __name__ == "__main__":
    app.run(debug=True,port=3000)