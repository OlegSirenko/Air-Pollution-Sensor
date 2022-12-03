import network  # библиотека для открытия точки доступа
import gc  # сбощик мусора

try:
    import usocket as socket  # импортируем библиотеку сокета из Micropython
except ImportError:
    import socket


def web_page():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
              <body><h1>Hello, World!</h1></body></html>"""
    return html


gc.collect()  # Коллектим мусор

ssid = 'Polution Sensor'

ap = network.WLAN(network.AP_IF)  # режим работы антены вай-фая -- точка доступа
ap.active(True)  # запускаем точку доступа
ap.config(essid=ssid)  # Ставим название точки доступа

print("Starting access point...", end="")
while not ap.active():  # пока точка доступа не запустится, сидим в цикле
    print(".", end="")

print('\nAccess Point Started!')
print(ap.ifconfig())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(2)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(4096)
    print('Content = %s' % str(request))
    response = web_page()
    conn.send(response)
    conn.close()
