from libs import *
import time
import urequests
import machine

# подключение пищалки
buz = ActiveBuzzer(17)
# подключение кнопки
but = Button(15)
# подключение вай фай
wifi = WiFi("WiFi-DOM.ru-6285", "Nastya26042015")
# подключение датчика температуры
temp = Temperature(2)
# подключение светодиода
rgb = RGBLed(pin_r, pin_g, pin_b)

# Иницилизация клиента
mqtt = MQTT(client_id="1")
mqtt.client.set_callback(cb)
# стандартное время без включания будильника
topic, msg = mqtt.sub('PashaSyr/feeds/break_time')
break_time = int(msg)
# пороговая температура для включения будильника
topic, msg = mqtt.sub('PashaSyr/feeds/target_temp')
target_temp = int(msg)

while True:
    try:
        # проверка температуры
        temp = round(temp.get_temp(), 1)
        # публикация температуры
        mqtt.pub('PashaSyr/feeds/temp', str(temp))
        # если температура меньше целевой и время без будильника истекло
        if temp <= target_temp and break_time == 0:
            # стандартное время без включания будильника
            topic, msg = mqtt.sub('PashaSyr/feeds/break_time')
            break_time = int(msg)
            # включаем будильник
            print("Beep on")
            # запускаем будильник
            mqtt.pub('PashaSyr/feeds/beep', "Включить")
            # переменная для проверки температуры при включенном будильнике
            get_temp_time = 110
            # бесконечный цикл
            while True:
                # если время проверки температуры истекло
                if get_temp_time == 0:
                    # проверяем температуру
                    temp = round(temp.get_temp(),1)
                    # публикация температуры
                    mqtt.pub('PashaSyr/feeds/temp', str(temp))
                    # устанавливаем время в начальное состояние
                    get_temp_time = 110
                    # если температура за это время повысилась выше целевой,
                    if temp > target_temp:
                        # выключаем будильник
                        print("Beep off")
                        # отправляем данные на сервер
                        mqtt.pub('PashaSyr/feeds/beep', "Выключить")
                        break
                else:
                    # если время проверки не истекло
                    # проверка - выключен ли будильник на сайте
                    topic, msg = mqtt.sub('PashaSyr/feeds/beep')
                    data = str(msg)
                    if data == "Выключить":
                        # если он выключен
                        # выключаем будильник
                        print("Beep off")
                        break
                    else:
                        # если будильник не выключили
                        # отнимаем один из времени проверки
                        get_temp_time -= 1
                        # засыпаем на полсекунды
                        time.sleep(0.5)
        elif temp <= target_temp and break_time > 0:
            # если температура меньше или равна целевой а время без включения не истекло
            # уменьшаем время без будильника на 1
            break_time -= 1
        time.sleep(298.5)
        
    except Exception as err:
        if Exception == 'CRC error':
            time.sleep(1)
        elif Exception == 'bytes index out of range':
            time.sleep(1)
        else:
            try:
                req = urequests.post(
                    """https://api.telegram.org/bot399910911:AAEh2Wv3YWKe1XSOW0hXeBmaJfbp1O4VBlk/
                    sendMessage?chat_id=24504089&text={0}""".format(err))
                machine.reset()
            except Exception as err:
                machine.reset()
