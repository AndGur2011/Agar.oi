import socket
import random
from threading import Thread
import time as time2
#пр!!!
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создаем сервер
server.bind(("localhost", 2711)) #привязываем сервер к порту
server.setblocking(False) #делаем сокет неблокирующим
server.listen(5) #начинаем прослушивание порта
clients = {} #словарь для хранения клиентов
client_id = 0 #идентификатор клиента
#принитяе данных от клиента
print("Rabota")
igroki = []
def accept_sms():
    while True:
        time2.sleep(0.01)
        try:
            #получение и дешифровка данных
            for connect1 in list(clients):
                data_client = connect1.recv(1024)
                if data_client == "GOOSE":
                    del clients[connect1]
                    connect1.close()
                    continue
                if data_client:
                    data = data_client.decode()
                    #разделение данных
                    parts = data.split(",")

                    data_id,data_x,data_y,data_radius = map(int,parts[0:4])
                    data_nick = parts[4]

                    # сохраняем данные в словарь
                    clients[connect1] = {
                    "id":data_id,
                    "x":data_x,
                    "y":data_y,
                    "radius":data_radius,
                    "nick":data_nick
                    }
                    #пишем полученные данные
                    #print(clients)

                    packet= ""
                    for keys,znach in clients.items():
                        if keys != connect1:
                            danie = f'{znach["id"]},{znach["x"]},{znach["y"]},{znach["radius"]},{znach["nick"]}'
                            packet += danie + "|"
                    connect1.send(packet.encode())

        except:
            pass
Thread(target=accept_sms).start()
while True:
    try:
            connect,ip =server.accept()  #приймаємо клінта
            connect.setblocking(False)
            print("До моне доєднався:", ip)
            #данные клиента                
            x=random.randint(0,1000)
            y=random.randint(0,1000)
            clients[connect] = {
                "id":client_id,
                "x":x,
                "y":y,
                "radius":10,
                "nick":None
            }
            #отправка данных(айди,х,н,размер,имя)
            connect.send(f"{client_id},{x},{y},{10},{None}".encode())
            client_id += 1
    except:
        pass
