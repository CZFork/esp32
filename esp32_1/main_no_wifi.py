from libs import *
buz = ActiveBuzzer(17) #подключение пищалки
temp = Temperature(18) #подключение датчика температуры
but = Button(2) #Подключение кнопки

buz.beep(50, 2) #после завершениыя настройки звуковой сигнал


while True:
    n_t = temp.get_temp() #проверка температуры
    if n_t < 17:
        buz.on()
        but.change_mode()
        while but.mode != 0 and n_t <= 17:
            but.but_pressed()
        else:
            print("Кнопка нажата или температура стала выше")
            buz.off()
        