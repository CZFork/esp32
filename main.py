#Файл служит для автоматического выполнения скриптов на плате
from machine import ADC, Pin, PWM
import dht
import time

temp = ADC(Pin(33)) #Температура - аналоговый датчик
temp_d = dht.DHT11(Pin(17)) #Температура - цифровой датчик
pot = ADC(Pin(32)) #Потенциометр
pwm12 = PWM(Pin(12)) #ШИМ

while 1:
    reg = pot.read()/4
    pwm12.duty(reg)
    temp_d.measure()
    t1 = temp_d.temperature()
    t2 = 0
    for i in range(10):
        t2 += temp/4095*5/4*100
        time.sleep_ms(15)
    
    t2 = t2/10
    print(t1,t2)
    time.sleep_ms(10)