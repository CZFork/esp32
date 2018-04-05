# coding: utf-8

import requests
from Adafruit_IO import *
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

broker = '127.0.0.1'
state_topic = 'home-assistant/temp/temp_on_street'
client = mqtt.Client("ha-client")
client.connect(broker)
client.loop_start()


def get_temp_street():
    url = 'http://narodmon.ru/api/sensorsOnDevice?id=1405&uuid=841199ada28c8747a112ad7c8d90a202&api_key=fGUwrZDQQaFan&lang=ru'
    res=requests.get(url)
    data = res.json()
    temp = data['sensors'][0]['value'] #температура
    pleassure = data['sensors'][1]['value'] #давление
    lux = data['sensors'][2]['value'] #освещенность
    url = 'http://narodmon.ru/api/sensorsOnDevice?id=2401&uuid=841199ada28c8747a112ad7c8d90a202&api_key=fGUwrZDQQaFan&lang=ru'
    res=requests.get(url)
    data = res.json()
    relative_humidity = data['sensors'][2]['value']
    aio = Client('e9666ef66a0149679734021420f5680b')
    aio.send('pleassure', pleassure)
    aio.send('relative_humidity', relative_humidity)
    aio.send('temp_on_street', temp)
    aio.send('lux', lux)
    return temp

def main():
    while True:
        try:
            temp = get_temp_street()
            client.publish(state_topic, temp)
            time.sleep(300)
        except Exception as er:
            print(er)
            time.sleep(30)

if __name__=="__main__":
    main()