#Import flask
import os
from flask import Flask

#Set up an instance of flask app and store it here
app = Flask(__name__)

#Test function with a route that will display sometext as a proof of concept, with / being default root
@app.route('/')
def hello():
    return 'Hello World ...again'

#Set up IP adress and port number so it knows how and where to run application
if __name__ == '__main__':
    #Set the host & port later used for Heroku; set debug
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)

