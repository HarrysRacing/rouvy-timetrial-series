# import the Flask library
from flask import Flask, render_template

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
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")
    
@app.route("/guide")
def guide():
    return render_template("guide.html")
    
@app.route("/about")
def about():
    return render_template("about.html")   

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")  

@app.route("/terms")
def terms():
    return render_template("terms.html")    

# Start with flask web app, with debug as True,
# only if this is the starting page
if __name__ == "__main__":
    app.run(debug=True)