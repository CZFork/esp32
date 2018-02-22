#Файл служит для автоматического выполнения скриптов на плате


#Подключение к вай-фай
import ConnectWiFi
ConnectWiFi.connect()

import temperature
temperature.get_temp() #получить температуру