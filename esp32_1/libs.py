import time #библиотека для прерываний 
from machine import Pin #импортируем класс Пин
from onewire import OneWire #импортируем класс OneWire
from ds18b20 import DS18B20 #импортируем класс датчика ds18b20
from network import WLAN #импортируем класс подключения к сети вай-фай
from mqtt import MQTTClient #для реализации Mqtt клиента

class Temperature():
    #Класс для датчика температуры DS18B20
    
    def __init__(self, port):
        """Иницилизация класса"""
        self.port = port
        self.addr = []
        self.get_addr()
        
    def get_addr(self):
        """Функция получения адреса датчика"""
        self.dat = DS18B20(OneWire(Pin(self.port)))
        try_id = 1
        while len(self.addr)<1:
            print("Попытка номер {0} найти адрес датчика".format(try_id))
            self.addr = self.dat.scan()[0]
            time.sleep_ms(750)
            try_id += 1
        print("Соединения с датчиком установлено")

    def get_temp(self):
        self.dat.convert_temp()
        time.sleep_ms(750)
        self.temp = self.read_temp(rom)
        print("Текущая температура {0} градусов Цельсия".format(self.temp))
        return self.temp
    
class WiFi():
    #Класс для подлючения к сети вай-фай
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.connect()
        
    def connect(self):
    """Функция для подключения к вай-фай сети"""
        station = network.WLAN(network.STA_IF)

        if station.isconnected() == True:
            print("Соединение уже установлено")
            return

        station.active(True)
        station.connect(self.ssid, self.password)

        while station.isconnected() == False:
            pass

        print("Соединение установлено")
        print(station.ifconfig())
        
class ActiveBuzzer():
    #Класс для работы с звукоизвлекателем
    def __init__(self, port):
        self.port = port
        self.pin = Pin(port)
        
    def on(self):
        """Включить пищалку"""
        self.pin.value(1)
    
    def off(self):
        """Выключить пищалку"""
        self.pin.value(0)
        
    def beep(self, time_sleep_ms, count):
        for c in range(count):
            self.on()
            time.sleep_ms(time_sleep_ms)
            self.off()
            time.sleep_ms(time_sleep_ms)
            

class MQTT():
    #класс для управления данными отправляемыми по протоколу mqtt
    def __init__(self, client_id, server="io.adafruit.com", user="PashaSyr", password="Pavel12291993", port=1883):
        client = MQTTClient(client_id=client_id, server=server, user=user, password=password, port=port) 
        client.connect()
        
    def publish(self, topic, message):
        client.publish(str(topic), str(message))
        