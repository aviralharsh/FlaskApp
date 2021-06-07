from flask import Flask,render_template, request, redirect, make_response
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017") #host uri    
db = client.cloudcontrol    #Select the database

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/add_to_db", methods=["POST"])
def add_entry():
    appName = request.values.get('appName')
    healthCheck = request.values.get('healthCheck')
    versionPath = request.values.get('version')
    environment = request.values.get('selectEnv')

    addEntry = db[environment] #Select the collection name
    print(addEntry.find({"appName": appName}))

    entry = addEntry.find({"appName": appName}).count()

    #print(entry)

    if(entry >= 1):
        return render_template('index.html', value = "App Exists")
    else:
        entry = {"appName":appName, "healthCheck":healthCheck, "version":versionPath}
        addEntry.insert(entry)
        return render_template('index.html', value = "App Added")
        #return redirect("/")
    
@app.route("/fetch", methods=["GET"])
def display():
    return render_template('fetch.html')

@app.route("/fetch_db", methods=["POST"])
def search():
    environment = request.values.get('selectEnv')
    reqName = request.values.get('appName')
    
    fetchEntry = db[environment]

    if(reqName == '*'):
        getresults = fetchEntry.find()
        return render_template('fetch.html', results = getresults)
    else:
        countRes = fetchEntry.find({"appName": reqName}).count()    
        if(countRes >= 1 ):
            getresults = fetchEntry.find({"appName": reqName})
            return render_template('fetch.html', results = getresults)
        else:
            return render_template('fetch.html', value = "No Apps Found")

    

@app.route("/update", methods=["GET"])
def update():
    return render_template('update.html')


@app.route("/update_db", methods=["POST"])
def updateDB():
    environment = request.values.get("selectEnv")
    updateEnv = db[environment]
    appName = request.values.get("appName")
    healthCheck = request.values.get("healthCheck")
    version = request.values.get("version")

    checker = updateEnv.find({"appName": appName}).count()
    #print(checker)
    if(checker >= 1):
        updateEnv.update({"appName": appName}, {"$set":{"healthCheck": healthCheck, "version": version}})
        return render_template('update.html', value = "App Details Updated")
    else:
        return render_template('update.html', value = "No Apps Found")
    #print("*******") 

if __name__ == '__main__':
    app.run(debug=True)