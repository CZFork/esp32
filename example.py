# coding: utf-8
from WunderWeather import weather
from Adafruit_IO import *
import time
from datetime import datetime

def get_temp():
    extractor = weather.Extract("0acd2cbb929b017c")
    [location,current] = extractor.features("RU/Tyumen",(('geolookup',''),('now','')))
    temp = float(current.temp_c)
    print(temp)
    return temp


#Иницилизация клиента
aio = Client('e9666ef66a0149679734021420f5680b')
break_time = int(aio.receive('break_time').value) #стандартное время без включания будильника
target_temp = int(aio.receive('target_temp').value) #пороговая температура для включения будильника


while 1:
    temp = get_temp() #проверяем температуру
    aio.send('temp_on_street', temp)
    if temp <= target_temp and break_time == 0: #если температура меньше целевой и время без будильника истекло
        break_time = int(aio.receive('break_time').value) #устанавливаем время без включения будильника
        print("Beep on")
        aio.send('beep', "Включить") #запускаем пищалку
        print("It's so cold! Temp = {0}, Stop_beep = {1}".format(temp, break_time))
        get_temp_time = 110 #переменная для проверки температуры при включенном будильнике 
        while True: #бесконечный цикл
            if get_temp_time == 0: #если время проверки температуры истекло
                temp = get_temp() #проверяем температуру
                aio.send('temp_on_street', temp) #отправляем температуру на сервер
                get_temp_time = 110 #устанавливаем время в начальное состояние
                if temp >  target_temp: #если температура за это время повысилась выше целевой, 
                    print("Beep off") #выключаем будильник
                    aio.send('beep', "Выключить") #отправляем данные на сервер
                    break
            else: #если время проверки не истекло
                data = aio.receive('beep') #получаем данные о состоянии будильника
                if data.value == "Выключить": #если он выключен
                    print("Beep off") #выключаем будильник
                    break
                else:    #если будильник не выключили
                    get_temp_time -= 1  #отнимаем один из времени проверки 
                    time.sleep(0.5) #засыпаем на полсекунды
    elif temp <= target_temp and break_time>0: #если температура меньше или равна целевой а время без включения не истекло
        break_time -= 1 #уменьшаем время без будильника на 1
    time.sleep(58.5)