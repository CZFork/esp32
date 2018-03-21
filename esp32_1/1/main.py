from libs import *
import time
import urequests
import machine


buz = ActiveBuzzer(17) #подключение пищалки
but = Button(15) #подключение кнопки
wifi = WiFi("WiFi-DOM.ru-6285", "Nastya26042015") #подключение вай фай
temp = Temperature(2) #подключение датчика температуры
mqtt = MQTT(client_id="1")


while True:
    try:
        n_t = temp.get_temp() #проверка температуры
        mqtt.pub('PashaSyr/feeds/temp', str(n_t)) #публикация температуры
        time.sleep(60)
    except Exception as err:
        try:
            req = urequests.post('https://api.telegram.org/bot399910911:AAEh2Wv3YWKe1XSOW0hXeBmaJfbp1O4VBlk/sendMessage?chat_id=24504089&text={0}'.format(err))
            machine.reset()
        except:
            machine.reset()
