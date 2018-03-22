from libs import *
import time
import urequests
import machine

def cb(topic, msg):
    print(topic, msg)
    return topic, msg

buz = ActiveBuzzer(17) #подключение пищалки
but = Button(15) #подключение кнопки
wifi = WiFi("WiFi-DOM.ru-6285", "Nastya26042015") #подключение вай фай
temp = Temperature(2) #подключение датчика температуры
rgb = RGBLed(pin_r, pin_g, pin_b)



#Иницилизация клиента
mqtt = MQTT(client_id="1")
mqtt.client.set_callback(cb)
topic, msg = mqtt.sub('PashaSyr/feeds/break_time') #стандартное время без включания будильника
break_time = int(msg)
topic, msg = mqtt.sub('PashaSyr/feeds/target_temp') #пороговая температура для включения будильника
target_temp = int(msg)

while True:
    try:
        temp = round(temp.get_temp(),1) #проверка температуры
        mqtt.pub('PashaSyr/feeds/temp', str(temp)) #публикация температуры
        if temp <= target_temp and break_time == 0: #если температура меньше целевой и время без будильника истекло
            topic, msg = mqtt.sub('PashaSyr/feeds/break_time') #стандартное время без включания будильника
            break_time = int(msg)
            print("Beep on") #включаем будильник
            mqtt.pub('PashaSyr/feeds/beep', "Включить") #запускаем будильник
            get_temp_time = 110 #переменная для проверки температуры при включенном будильнике 
            while True: #бесконечный цикл
                if get_temp_time == 0: #если время проверки температуры истекло
                    temp = round(temp.get_temp(),1) #проверяем температуру
                    mqtt.pub('PashaSyr/feeds/temp', str(temp)) #публикация температуры
                    get_temp_time = 110 #устанавливаем время в начальное состояние
                    if temp >  target_temp: #если температура за это время повысилась выше целевой, 
                        mqtt.pub('PashaSyr/feeds/beep', "Выключить") #запускаем будильник #отправляем данные на сервер
                        break
                else: #если время проверки не истекло
                    topic, msg = mqtt.sub('PashaSyr/feeds/beep') #пороговая температура для включения будильника
                    data = str(msg)
                    if data == "Выключить": #если он выключен
                        print("Beep off") #выключаем будильник
                        break
                    else:    #если будильник не выключили
                        get_temp_time -= 1  #отнимаем один из времени проверки 
                        time.sleep(0.5) #засыпаем на полсекунды
        elif temp <= target_temp and break_time>0: #если температура меньше или равна целевой а время без включения не истекло
            break_time -= 1 #уменьшаем время без будильника на 1
        time.sleep(58.5)
        
    except Exception as err:
        try:
            req = urequests.post('https://api.telegram.org/bot399910911:AAEh2Wv3YWKe1XSOW0hXeBmaJfbp1O4VBlk/sendMessage?chat_id=24504089&text={0}'.format(err))
            machine.reset()
        except:
            time.sleep(300)
            machine.reset()
