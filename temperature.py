def temp(value):
    return value/10

def get_temp()
    
    from machine import ADC
    adc = ADC(0) #порт соединения 0
    reading = adc.read()
    celsius_temp = temp(reading)
    print("TMP36 reading {}\nDegrees Celsius {}".format(reading, celsius_temp))