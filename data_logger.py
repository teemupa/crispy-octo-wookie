#!/usr/bin/python
import Adafruit_DHT
import db.database as db

DHT_TYPE = Adafruit_DHT.AM2302
AM2302_PIN = 4

sensor_db = db.SensorDatabase()

humidity, temperature = Adafruit_DHT.read(DHT_TYPE, AM2302_PIN)

#If the values is valid, write to to DB
if temperature is not None and humidity is not None:
    values = {'temperature':temperature, 'humidity':humidity}
    sensor_db.add_values(temperature, humidity)

#else:
#    print "Bad values"
