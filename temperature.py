class Temperature():
    #Класс для датчика температуры DS18B20
    
    def __init__(self, port):
        """Иницилизация класса"""
        self.port = port
        self.addr = []
        self.get_addr()
        
    def get_addr(self):
        """Функция получения адреса датчика"""
        self.dat = DS18B20(OneWire(Pin(self.port)))
        try_id = 1
        while len(self.addr)<1:
            print("Попытка номер {0} найти адрес датчика".format(try_id))
            self.addr = self.dat.scan()[0]
            time.sleep_ms(750)
            try_id += 1
        print("Соединения с датчиком установлено")

    def get_temp(self):
        self.dat.convert_temp()
        time.sleep_ms(750)
        self.temp = self.read_temp(rom)
        print("Текущая температура {0} градусов Цельсия".format(self.temp))
        return self.temp