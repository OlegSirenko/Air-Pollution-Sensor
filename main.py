import network  # библиотека для открытия точки доступа
import gc  # сбощик мусора
from machine import Pin
import time
import uselect as select


try:
    import usocket as socket  # импортируем библиотеку сокета из Micropython
except ImportError:
    import socket


def data_send():
    data = b'1'
    return data


def data_collect():
    print("Collecting...")
    led = Pin(4, Pin.OUT)
    led.on()
    time.sleep(0.4)
    led.off()


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
    r, w, err = select.select((server,), (), (), 1)
    if r:
        for readable in r:
            conn, addr = server.accept()  # Нужно учитывать, что это блокирующая функция
            print('Got a connection from %s' % str(addr))  # Принтим коннектион

            data_collect()
            request = conn.recvfrom(512)  # Указываем буфер УЧИТЫВАТЬ ЧТО ЭТО блокирующая функция
            print('Content = %s' % str(request))  #
            conn.send(b"Some data (Next it will be file)")  # Отправляем
    else:
        data_collect()

server.close()


