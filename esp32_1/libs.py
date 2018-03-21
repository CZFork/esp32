import time #библиотека для прерываний 
from machine import Pin, PWM #импортируем класс Пин и ШИМ
from onewire import OneWire #импортируем класс OneWire
from ds18b20 import DS18B20 #импортируем класс датчика ds18b20
from network import WLAN #импортируем класс подключения к сети вай-фай
from mqtt import MQTTClient #для реализации Mqtt клиента
import traceback #трассировка ошибки - необходима для работы модуля логгирования
import urequests #для http запросов - необходима для отправки данных в телеграмм

class Logfile():
    filename = "log.txt"
    
    def __init__(self):
        self.file = open(Logfile.filename, "a")
        
    def log_mes(self, text):
        mes = str(time.strftime("%Y-%m-%d %H:%M:%S"))+" "+ str("[INFO]") +" "+ str(text) + "\n"
        self.file.write(mes)
        self.post_message(mes)
    
    def log_err(self, err):
        trace = traceback.format_exc()
        mes = str(time.strftime("%Y-%m-%d %H:%M:%S"))+" "+ str("[ERROR]") +" "+ str(err) + "\n"
        self.file.write(mes)
        self.post_message(mes)
        
        trace_split = trace.split('\n')
        for trace in trace_split:
            if trace!='':
                mes = str(time.strftime("%Y-%m-%d %H:%M:%S"))+" "+ str("[TRACEBACK]") +" "+ str(trace) + "\n"
                self.file.write(mes)
                self.post_message(mes)
    
    def end(self):
        self.file.close()
        
    def post_message(self, message):
        try:
            URL = 'https://api.telegram.org/bot' 
            TOKEN = '399910911:AAEh2Wv3YWKe1XSOW0hXeBmaJfbp1O4VBlk'
            data = {'offset': 1, 'limit': 0, 'timeout': 0}
            message_data = {
                    'chat_id': 24504089, 
                    'text': message,
                    'parse_mode': 'HTML'
                }

            request = urequests.post(URL+TOKEN +'/sendMessage', data=message_data) 
            
        except Exception as err:
            self.log_err(err)


class Temperature(Logfile):
    #Класс для датчика температуры DS18B20
    
    def __init__(self, port):
        """Иницилизация класса"""
        self.port = port
        self.addr = []
        self.get_addr()
        
    def get_addr(self):
        """Функция получения адреса датчика"""
        try:
            self.dat = DS18B20(OneWire(Pin(self.port, Pin.IN)))
            try_id = 1
            while len(self.addr)<1:
                self.log_mes("Попытка номер {0} найти адрес датчика".format(try_id))
                self.addr = self.dat.scan()[0]
                time.sleep_ms(750)
                try_id += 1
            self.log_mes("Соединения с датчиком установлено")
        
        except Exception as err:
            self.log_err(err)
            

    def get_temp(self):
        try:   
            self.dat.convert_temp()
            time.sleep_ms(750)
            self.temp = self.dat.read_temp(self.addr)
            self.log_mes("Текущая температура {0} градусов Цельсия".format(self.temp))
            return self.temp
       
        except Exception as err:
            self.log_err(err)
    
    
class WiFi(Logfile):
    #Класс для подлючения к сети вай-фай
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.connect()
        
    def connect(self):
        try:
            """Функция для подключения к вай-фай сети"""
            station = network.WLAN(network.STA_IF)

            if station.isconnected() == True:
                self.log_mes("Соединение уже установлено")
                return

            station.active(True)
            station.connect(self.ssid, self.password)

            while station.isconnected() == False:
                pass

            self.log_mes("Соединение установлено")
            self.log_mes(station.ifconfig())
        
        except Exception as err:
            self.log_err(err)
        
        
class ActiveBuzzer(Logfile):
    #Класс для работы с звукоизвлекателем
    def __init__(self, port):
        self.port = port
        self.pin = Pin(port, Pin.OUT)
        
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
            
    def sub_cb(self, topic, msg):
        #Для MQTT подписка
        if msg == b"Включить":
            self.on()
        elif msg == b"Выключить":
            self.off()
            

class MQTT(Logfile):
    #класс для управления данными отправляемыми по протоколу mqtt
    def __init__(self, client_id, server="io.adafruit.com", user="PashaSyr", password="e9666ef66a0149679734021420f5680b", port=1883):
        try:
            client = MQTTClient(client_id=client_id, server=server, user=user, password=password, port=port) 
            client.connect()
            self.client = client
        
        except Exception as err:
            self.log_err(err)
        
    def pub(self, topic, message):
        try:
            self.client.publish(str(topic), str(message))
        except Exception as err:
            self.log_err(err)
    
    def set_call(self, callback):
        try:
            self.client.set_callback(callback)
        except Exception as err:
            self.log_err(err)
    
    def sub(self, topic):
        try:
            self.client.subscribe(str(topic))
        except Exception as err:
            self.log_err(err)
        
        
class Button(Logfile):
    #Класс для управление кнопкой
    
    def __init__(self, port):
        self.port = port
        self.pin = Pin(port, Pin.IN, Pin.PULL_UP)
        self.mode = 0
        
            
    def but_pressed(self):
        self.mode = self.pin.value()
        return self.mode
        

class RGBLed:
    #Класс для управления светодиодом
    def __init__(self, pin_r, pin_g, pin_b):
        self.pin_r = PWM(Pin(pin_r))
        self.pin_g = PWM(Pin(pin_g))
        self.pin_b = PWM(Pin(pin_b))
        self.set(0, 0, 0)

    def set(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.duty()

    def duty(self):
        self.pin_r.duty(self.duty_translate(self.r))
        self.pin_g.duty(self.duty_translate(self.g))
        self.pin_b.duty(self.duty_translate(self.b))

    def duty_translate(self, n):
        """translate values from 0-255 to 0-1023"""
        return int((float(n) / 255) * 1023)
        