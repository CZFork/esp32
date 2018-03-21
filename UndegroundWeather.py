# coding: utf-8

from WunderWeather import weather
from Adafruit_IO import *
import time

def get_temp_street():
    extractor = weather.Extract("0acd2cbb929b017c")
    [location,current] = extractor.features("RU/Tyumen",(('geolookup',''),('now','')))
    temp = current.temp_c
    aio = Client('e9666ef66a0149679734021420f5680b')
    aio.send('temp_on_street', temp)
    
while True:
    get_temp_street()
    time.sleep(60)