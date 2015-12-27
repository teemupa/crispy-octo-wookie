import Adafruit_DHT

DHT_TYPE    = Adafruit_DHT.AM2302
AM2302_PIN  = 4

def get_temp_and_hum():
    '''
    Read temperature and humidity values from the AM2302 sensor
    IN: -
    OUT:    if success, return values
            else, return None
    '''
    humidity, temperature = Adafruit_DHT.read(DHT_TYPE, AM2302_PIN)
    if temperature is not None and humidity is not None:
        values = {'temperature':temperature, 'humidity':humidity}
        return values

    else:
        return None
