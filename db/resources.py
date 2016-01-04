import json

from flask import Flask, request, Response, g, jsonify
from flask.ext.restful import Resource, Api, abort
from werkzeug.exceptions import NotFound, UnsupportedMediaType

from utils import RegexConverter
import database

DEFAULT_DB_PATH = 'db/sensor_data.db'

COLLECTIONJSNO = "application/vnd.collection+json"

#Define thee app and Api
app = Flask(__name__)
app.debug = True
app.config.update({'DATABASE':database.ProjectDatabase(DEFAULT_DB_PATH)})

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

class Temperature&Humidity(resource):
    '''
    Resource Messages implementation
    '''
    #get the values from the database
    def get(self):
        values_db = g.db.get_values()

    #Create the envelope
    envelope = {}
    collection = {}
    envelope["collection"] = collection
    collection['version'] = "1.0"
    collection['href'] = api.url_for(Temperature&Humidity)


    #Create the items
    items = []
    for values in values_db:
        print values
        _timestamp = values['timestamp']
        _temperature = values['temperature']
        _humidity = values['humidity']
        _url = api.url_for(Temperature&Humidity, timestamp=_timestamp, temperature=_temperature, humidity = _humidity)

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



app.url_map.converters['regex'] = RegexConverter

#Define the routes
api.add_resource(Temperature&Humidity, '/project/api/tasks/',
                 endpoint='values')


#Start the application
if __name__ == '__main__':
    app.run(debug=True)
