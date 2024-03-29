import json

from flask import Flask, request, Response, g, jsonify
from flask.ext.restful import Resource, Api, abort
#from flask.ext.cors import CORS
from werkzeug.exceptions import NotFound, UnsupportedMediaType

from utils import RegexConverter
import database

DEFAULT_DB_PATH = 'db/sensor_data.db'

COLLECTIONJSNO = "application/vnd.collection+json"

#Define thee app and Api
app = Flask(__name__)
app.debug = True
app.config.update({'DATABASE':database.SensorDatabase()})

#cors = CORS(app, resources={r"/foo": {"origins": "*"}})

#Start the RESTful Api
api = Api(app)

def create_error_response(status_code, title, message, resource_type=None):
    response = jsonify(title=title, message=message, resource_type=resource_type)
    response.status_code = status_code
    return response

@app.errorhandler(404)
def resource_not_found(error):
    return create_error_response(404, "Resource not found", "This resource url does not exit")

@app.errorhandler(500)
def unknown_error(error):
    return create_error_response(500, "Error", "The system has failed. Please, contact the administrator")

@app.before_request
def set_database():
    '''Stores an instance of the database API before each request in the flask
    variable accessible only from the application context'''
    g.db = app.config['DATABASE']

#Defining resources

class Temperature_And_Humidity(Resource):
    '''
    Resource Messages implementation
    '''
    #get the values from the database

    def get(self):
        values_db = g.db.get_values(1)

        #Create the envelope
        envelope = {}
        collection = {}
        envelope["collection"] = collection
        collection['version'] = "1.0"
        collection['href'] = api.url_for(Temperature_And_Humidity)


        #Create the items
        items = []
        for values in values_db:
            print values
            _timestamp = values['timestamp']
            _temperature = values['temp_in']
            _humidity = values['hum']
            _url = api.url_for(Temperature_And_Humidity, timestamp=_timestamp, temperature=_temperature, humidity = _humidity)

            _values = {}
            _values['href'] = _url
            _values['data'] = []
            value1 = {'name':'timestamp', 'value':_timestamp}
            value2 = {'name':'temperature', 'value':_temperature}
            value3 = {'name':'humidity', 'value':_humidity}

            _values['data'].append(value1)
            _values['data'].append(value2)
            _values['data'].append(value3)

            items.append(_values)


        collection['items'] = items
        return envelope

class history_data(Resource):
    '''
    Historical data for graph etc...
    '''

    def get(self):
        #Extract history data from database
        values_db = g.db.get_history_values()

        #Create the envelope
        envelope = {}
        collection = {}
        envelope["collection"] = collection
        collection['version'] = "1.0"
        collection['template'] = {
          "data" : [
                {"prompt" : "timestamp", "name" : "timestamp", "value" : "", "required":True},
                {"prompt" : "temperature", "name" : "temperature", "value" : "", "required":True},
                {"prompt" : "humidity", "name" : "humidity", "value" : "", "required":True}
        ]}
        #Create the items
        items = []
        for data in values_db:
            _timestamp = data['timestamp']
            _temperature = data['temp_in']
            _humidity = data['hum']
            #_url = api.url_for(History, timestamp=_timestamp)
            history_data = {}
            #task['href'] = _url
            history_data['data'] = []
            value0 = {'name':'timestamp', 'value':_timestamp}
            value1 = {'name':'temperature', 'value':_temperature}
            value2 = {'name':'humidity', 'value':_humidity}
            history_data['data'].append(value0)
            history_data['data'].append(value1)
            history_data['data'].append(value2)
            #task['links'] = [{"href" : api.url_for(Comments, taskid=_task), "rel" : "Comments", "prompt" : "Comments for this task"},
            #                 {"href" : api.url_for(Assignees, taskid=_task), "rel" : "Assignees", "prompt" : "Assignees for this task"}]
            items.append(data)
        collection['items'] = items

        return envelope


app.url_map.converters['regex'] = RegexConverter

#Define the routes
api.add_resource(Temperature_And_Humidity, '/api/',
                 endpoint='values')
api.add_resource(history_data, '/api/history/', endpoint ='history')



@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

#Start the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
