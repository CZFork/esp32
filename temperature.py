class Temperature():
    
    def __init__(self, port):
        self.port = port
        
    def get_temp(self)
        adc = ADC(self.port) #порт соединения 0
        reading = adc.read()
        celsius_temp = reading/10
        print("TMP36 reading {}\nDegrees Celsius {}".format(reading, celsius_temp))
        return celsius_temp