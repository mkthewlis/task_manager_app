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

@app.route('/add_task')
def add_task():
    return render_template('addtask.html', categories=mongo.db.categories.find())

#Submitting a form using POST (the 'add task' button) so we have to specify HTTP method as default is GET
@app.route('/insert_task', methods=["POST"])
def insert_task():
    #Gets tasks collection from mongo, and inserts one request (as requests are the type of object sent across web) converted to dictionary
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    #Once done and sent, redirect to 'get_tasks' page above to view full selection
    return redirect(url_for('get_tasks'))

#Function reacts when edit btn clicked: need to retrieve task from db with its id
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    #Fetch the task that matches this task id, converted into a form that's readable by mongo
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    #The form will be filled in instead of being empty (as this is editing!)
    all_categories =  mongo.db.categories.find()
    return render_template('edittask.html', task=the_task,
                           categories=all_categories)


#Update the db after a task is edited
@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
        {
            'task_name':request.form.get('task_name'),
            'category_name':request.form.get('category_name'),
            'task_description': request.form.get('task_description'),
            'due_date': request.form.get('due_date'),
            'is_urgent': request.form.get('is_urgent')
        })
    return redirect(url_for('get_tasks'))

#Delete a task once it is completed
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    #Redirects to task list so users see task is gone
    return redirect(url_for('get_tasks'))



#Set up IP adress and port number so it knows how and where to run application
if __name__ == '__main__':
    #Set the host & port later used for Heroku; set debug
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)

