import network  # библиотека для открытия точки доступа
import gc  # сбощик мусора
from machine import Pin, SoftI2C
import ssd1306
import time
import neopixel
import uselect as select
import BME280
import json

try:
    import usocket as socket  # импортируем библиотеку сокета из Micropython
except ImportError:
    import socket


np = neopixel.NeoPixel(Pin(5), 8)
led_in = Pin(2, Pin.OUT)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

dataToSend = {"temp": [], "hum": [], "pres": []}

json_to_send = {}

bme = BME280.BME280(i2c=i2c)
oled_width = 128
oled_height = 32

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def data_send():
    data = b'1'
    return data


def data_collect():
    oled.fill(0)
    led_in.on()
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
    time.sleep(0.5)
    led_in.off()

    np[0] = (255, 0, 0)
    np[3] = (125, 204, 223)
    np[7] = (120, 153, 23)

    oled.text("T:"+str(temp), 0, 0, 1)
    oled.text("H:"+str(hum), 66, 0, 1)
    oled.text("P:"+str(pres), 0, 20, 1)
    oled.show()
    return temp, hum, pres


gc.collect()  # Коллектим мусор

ssid = 'Polution Sensor'

ap = network.WLAN(network.AP_IF)  # режим работы антены вай-фая -- точка доступа
ap.active(True)  # запускаем точку доступа
ap.config(essid=ssid)  # Ставим название точки доступа

print("Starting access point...")
while not ap.active():  # пока точка доступа не запустится, сидим в цикле
    print(".", end="")

print('\nAccess Point Started!')
print(ap.ifconfig())  # выводим информацию о точке доступа

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # открываем  сокет, при подключении порт не нужен
server.bind(("", 80))  # биндим его
server.listen(1)  # ставим максимальное число подключившихся

print("Wait for connection...")

while True:
    r, w, err = select.select((server,), (), (), 30)  # кадую секунду слушаем срвер на подключение
    if r:
        for readable in r:
            conn, addr = server.accept()  # Нужно учитывать, что это блокирующая функция
            print('Got a connection from %s' % str(addr))  # Принтим коннектион
            request = conn.recvfrom(512)  # Указываем буфер УЧИТЫВАТЬ ЧТО ЭТО блокирующая функция
            print('Content = %s' % str(request))  #
            conn.send(json_to_send)  # Отправляем файл

            # conn.close()
    else:
        dataToSend["temp"].append(data_collect()[0])
        dataToSend["hum"].append(data_collect()[1])
        dataToSend["pres"].append(data_collect()[2])
        json_to_send = json.dumps(dataToSend)
        print(dataToSend)
