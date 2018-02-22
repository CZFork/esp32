#Файл служит для автоматического выполнения скриптов на плате
from machine import ADC, Pin, PWM
import network
from temperature import Temperature
from ConnectWifFi import WiFi
from pwm import Pwm


#Константы
ssid = "WiFiDomRu-6285"
password =  "Nastya26042015"
pin_temp = 0
pin_led = 12

#Подключение к вай-фай
wifi = WiFi(ssid, password)
wifi.connect()

#получить температуру
temp = Temperature(pin_temp) #0 - пин
temp.get_temp()

#Управление ШИМ (мигание светодиода)
led = Pwm(pin_led, 1000, 512)