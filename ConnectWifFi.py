#TO-DO
#Сделать обработку ошибок при неправильном вводе пароля


def connect():
    """Функция для подключения к вай-фай сети"""
    
    
    
    import network
 
    ssid = "WiFiDomRu-6285"
    password =  "Nastya26042015"
 
    station = network.WLAN(network.STA_IF)
 
    if station.isconnected() == True:
        print("Соединение уже установлено")
        return
 
    station.active(True)
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
 
    print("Соединение установлено")
    print(station.ifconfig())