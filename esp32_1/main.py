from libs import *
import time
buz = ActiveBuzzer(17) #подключение пищалки
wifi = WiFi("WiFi-DOM.ru-6285", "Nastya26042015") #подключение вай фай
buz.beep(50, 1) #после подключения вай-фай один звуковой сигнал
temp = Temperature(18) #подключение датчика температуры
buz.beep(50, 1) #после подключения датчика температуры один звуковой сигнал
mqtt = MQTT(client_id="1")
buz.beep(50, 1) #после подключения протокола mqtt один звуковой сигнал

buz.beep(150, 1) #после иницилизации писк


while True:
    n_t = temp.get_temp() #проверка температуры
    mqtt.publish('PashaSyr/∕Feeds∕/temp', str(n_t)) #публикация температуры
    time.sleep(60)
        
        