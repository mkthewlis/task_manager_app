#Imports to reflect what we have installed
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

#Keeps eny.py private by being listed on gitignore file
from os import path
if path.exists("env.py"):
    import env

#Set up an instance of flask app and store it here
app = Flask(__name__)

#MongoDB name and the url linking to that DB
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

#Instance of pymongo - constructor method
mongo = PyMongo(app)

#Test function with a route that will display sometext as a proof of concept, with / being default root
@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())

#Set up IP adress and port number so it knows how and where to run application
if __name__ == '__main__':
    #Set the host & port later used for Heroku; set debug
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)

