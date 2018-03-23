# coding: utf-8

from WunderWeather import weather
from Adafruit_IO import *
import time

def get_temp_street():
    extractor = weather.Extract("0acd2cbb929b017c")
    [location,current] = extractor.features("RU/Tyumen",(('geolookup',''),('now','')))
    temp = current.temp_c
    pleassure = round(float(current.data['pressure_mb'])*(760/1013.25),1)
    relative_humidity = int(current.data['relative_humidity'].replace("%",''))
    aio = Client('e9666ef66a0149679734021420f5680b')
    aio.send('pleassure', pleassure)
    aio.send('relative_humidity', relative_humidity)
    aio.send('temp_on_street', temp)
    
while True:
    get_temp_street()
    time.sleep(60)