import time # библиотека для прерываний
from machine import Pin, PWM # импортируем класс Пин и ШИМ
from onewire import OneWire # импортируем класс OneWire
from ds18x20 import DS18X20 # импортируем класс датчика ds18b20
import network # импортируем класс подключения к сети вай-фай
from mqtt import MQTTClient # для реализации Mqtt клиента


class Temperature:
    # Класс для датчика температуры DS18X20
    
    def __init__(self, port):
        """Иницилизация класса"""
        self.port = port
        self.addr = []
        self.get_addr()
        self.dat = ''
        self.temp = 0.0
        
    def get_addr(self):
        """Функция получения адреса датчика"""
        self.dat = DS18X20(OneWire(Pin(self.port, Pin.IN)))
        try_id = 1
        while len(self.addr) < 1:
            try:
                time.sleep(2)
                self.addr = self.dat.scan()[0]
                time.sleep_ms(2750)
                try_id += 1
            except:
                time.sleep_ms(750)
                try_id += 1
            finally:
                print("Попытка соединения с датчиком {0}".format(try_id))

    def get_temp(self):
            self.dat.convert_temp()
            time.sleep_ms(750)
            self.temp = self.dat.read_temp(self.addr)
         
            return self.temp


class WiFi:
    # Класс для подлючения к сети вай-фай
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.connect()
        
    def connect(self):
            """Функция для подключения к вай-фай сети"""
            station = network.WLAN(network.STA_IF)

            if station.isconnected() is True:
                print("Соединение установлено")
                return

            station.active(True)
            station.connect(self.ssid, self.password)

            while station.isconnected() is False:
                pass


class ActiveBuzzer:
    # Класс для работы с звукоизвлекателем
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
        # Для MQTT подписка
        if msg == b"On":
            self.on()
        elif msg == b"Off":
            self.off()


class MQTT:
    # класс для управления данными отправляемыми по протоколу mqtt
    def __init__(self, client_id, server="io.adafruit.com", user="PashaSyr",
                 password="e9666ef66a0149679734021420f5680b", port=1883):
            self.client = MQTTClient(client_id, server=server, user=user, password=password, port=port)
        
    def pub(self, topic, message):
        self.client.connect()
        self.client.publish(str(topic), str(message))
        self.client.disconnect()

    def sub(self, topic):
        self.client.connect()
        self.client.subscribe(topic)
        result = self.client.check_msg()
        time.sleep(1)
        self.client.disconnect()
        return result
        
        
class Button:
    # Класс для управление кнопкой
    def __init__(self, port):
        self.port = port
        self.pin = Pin(port, Pin.IN, Pin.PULL_UP)
        self.mode = 0

    def but_pressed(self):
        self.mode = self.pin.value()
        return self.mode
        

class RGBLed:
    # Класс для управления светодиодом
    def __init__(self, pin_r, pin_g, pin_b):
        self.pin_r = PWM(Pin(pin_r))
        self.pin_g = PWM(Pin(pin_g))
        self.pin_b = PWM(Pin(pin_b))
        self.r = 0
        self.g = 0
        self.b = 0
        self.set_rgb(0, 0, 0)

    def set_rgb(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.duty()

    def duty(self):
        self.pin_r.duty(self.duty_translate(self.r))
        self.pin_g.duty(self.duty_translate(self.g))
        self.pin_b.duty(self.duty_translate(self.b))

    @staticmethod
    def duty_translate(n):
        """translate values from 0-255 to 0-1023"""
        return int((float(n) / 255) * 1023)
