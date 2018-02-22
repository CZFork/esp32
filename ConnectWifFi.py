#TO-DO
#Сделать обработку ошибок при неправильном вводе пароля

class WiFi():
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        
    def connect(self):
    """Функция для подключения к вай-фай сети"""
        station = network.WLAN(network.STA_IF)

        if station.isconnected() == True:
            print("Соединение уже установлено")
            return

        station.active(True)
        station.connect(self.ssid, self.password)

        while station.isconnected() == False:
            pass

        print("Соединение установлено")
        print(station.ifconfig())



