from libs import *
import _thread
import time

buz = ActiveBuzzer(17) #подключение пищалки
but = Button(2) #подключение кнопки
wifi = WiFi("WiFi-DOM.ru-6285", "Nastya26042015") #подключение вай фай
buz.beep(50, 1) #после подключения вай-фай один звуковой сигнал
temp = Temperature(18) #подключение датчика температуры
buz.beep(50, 1) #после подключения датчика температуры один звуковой сигнал
mqtt = MQTT(client_id="1")
mqtt.set_call(buz.sub_cb)
mqtt.sub("PashaSyr/Feeds/beep")
buz.beep(50, 1) #после подключения протокола mqtt один звуковой сигнал

buz.beep(150, 1) #после иницилизации писк

n_t = 0 #глобальная переменная для температуры

def get_and_push_temp():
    global n_t
    while True:
        n_t = temp.get_temp() #проверка температуры
        mqtt.pub('PashaSyr/∕Feeds∕/temp', str(n_t)) #публикация температуры
        mqtt.client.wait_msg()
        time.sleep(60)

def change_buz(buz, but):
    global n_t
    while True:
        if n_t<=17:
            buz.on()
            while True:
                if but.but_pressed==True:
                    buz.off()
                    time.sleep(600)
                    break
                elif n_t>17:
                    buz.off()
                    break
        else:       
            buz.off()

_thread.start_new_thread(change_buz, (buz, but)) 
_thread.start_new_thread(get_and_push_temp, ())  
   