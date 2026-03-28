from pygame import *
from random import randint
import socket
import random
from threading import Thread
import time as time2
import customtkinter as ctk
init()
WIDTH,HEITH = 800,700                           #Не изменяемые константы


app = ctk.CTk()
app.geometry("500x600")
app.title("Agario Battle")

nick = ""
ip = ""
port = ""


def start_game():
    global nick,ip,port,win
    if nick == "":
        entry_name.configure(placeholder_text="Немає Ім'я")
    elif ip == "":
        entry_ip.configure(placeholder_text="Не вписаний IP")
    elif port == "":
        entry_port.configure(placeholder_text="Не вписаний Порт")
    nick = entry_name.get()
    ip = entry_ip.get()
    port = int(entry_port.get())
    app.destroy()           #создание окна
title = ctk.CTkLabel(app, text="⚡ AGARIO BATTLE ⚡", font=("Arial", 36, "bold"))
title.place(x=60, y=80)

entry_name = ctk.CTkEntry(app, placeholder_text="Ваш никнейм", width=300, height=40)
entry_name.place(x=100, y=200)

entry_ip = ctk.CTkEntry(app, placeholder_text="IP сервера", width=300, height=40)
entry_ip.place(x=100, y=260)

entry_port = ctk.CTkEntry(app, placeholder_text="Порт сервера", width=300, height=40)
entry_port.place(x=100, y=320)

button = ctk.CTkButton(app, text="🚀 Старт гри!", width=200, height=45,command = start_game)
button.place(x=150, y=420)

app.mainloop() 

win = display.set_mode((WIDTH,HEITH))
clock = time.Clock()
#клієнт

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))
data = client.recv(1024)
data_decode = data.decode()           
data_decod = data_decode.split(",")         #разделяем данные
data_id,data_x,data_y,data_radius = map(int,data_decod[0:4])
# nick = data_decod[4]
print(data_id,data_x,data_y,data_radius,nick)
class Food:                                     #класс еды
    def __init__ (self,radius,color,x,y):              #создание круглишков
        self.radius = radius                    #радиус
        self.color = color                      #цвет
        self.x = x                              #икс
        self.y = y                              #игрек
        self.rect = Rect(self.x,self.y,self.radius*2,self.radius*2) #хитбокс для столкновений
    def otrisov(self,big_cam):                          #отрисовка
        rad_new = big_cam * self.radius
        self.rect = Rect(self.rect.x,self.rect.y,self.radius*1.5,self.radius*1.5)
        draw.circle(win,self.color,(self.rect.x,self.rect.y),rad_new)
    def fontic(self,nicknames):                           #рендер
        shrift = font.Font("Orbitron-VariableFont_wght.ttf",20)
        self.text = shrift.render(nicknames,True,(0,0,0))
        win.blit(self.text,(self.rect.x - 40,self.rect.y - 20))


#создание игрока
player = Food(data_radius,(25,255,188),400,350)
#создание еды
foods = []
for i in range (4000):              #создание обекта еды(range -- кол-во еды)
    eda = Food(randint(7,23),(randint(0,255),randint(0,255),randint(0,255)),randint(-3000, 3000),randint(-3000,3000))
    foods.append(eda)               #добавление еды
#переменные
right = False
left = False
up = False
down = False
runin = True
players_vragi = []
#получение данных о игрооках
def accept_danie():
    global players_vragi,runin
    while runin:
        time2.sleep(0.01)
        try:
            data_about_players = client.recv(1024).decode()             #декодируем сообщения

            if data_about_players != "":                                #проверка данных на наличие
                packet_danie = data_about_players.strip("|").split("|") #разделение данных игроков по игрокам
                players_vragi = []                                      #список

                print(players_vragi)
                for element in packet_danie:                            #перебор данных                    
                    spisok_1_player = element.split(",")                #разчленение данных по запятым
                    print(players_vragi)
                    if len(spisok_1_player) == 5:                       #проверка длины списка
                        print(players_vragi)                     

                        vrag_id,vrag_x,vrag_y,vrag_radius = map(int,spisok_1_player [0:4])        #запись id
                        vrag_nick = spisok_1_player[4]
                                    #запись x
                        #запись y#запись radiusa#запись Ника


                        players_vragi.append([vrag_id,vrag_x,vrag_y,vrag_radius,vrag_nick])
                        # players_vragi[vrag_id] = {
                        #     "x": vrag_x,
                        #     "y": vrag_y,
                        #     "radius": vrag_radius,
                        #     "nick": vrag_nick
                        # }
                    print(players_vragi)
        except:
            pass            
Thread(target=accept_danie).start()     #поток
#игровой цикл

while runin:
    scale = max(0.3,min(50/ data_radius, 1.5))
    win.fill("#014E53")
    #проверка действий
    for a in event.get():
        if a.type == QUIT:
            runin = False


        if a.type == KEYDOWN:           #проверка на нажатие  кнопок вправо
            if a.key == K_RIGHT:
                right = True
            elif a.key == K_LEFT:
                left = True
            elif a.key == K_UP:
                up = True
            elif a.key == K_DOWN:       #проверка на нажатие  кнопок вниз
                down = True

        if a.type == KEYUP:
            if a.key == K_RIGHT:
                right = False
            elif a.key == K_LEFT:
                left = False
            elif a.key == K_UP:
                up = False
            elif a.key == K_DOWN:
                down = False
        #отрисовка врага
    for vrag in players_vragi:
        ex = int((vrag[1] - data_x) + WIDTH // 2)
        ey = int((vrag[2] - data_y) + HEITH // 2)

        b = Food(vrag[3], (255,0,0), ex, ey)
        if player.rect.colliderect(b):
            if player.radius < vrag[3]:
                client.send("GOOSE".encode())
                print("Проигрыш")
                runin = False
            elif player.radius > vrag[3]:
                players_vragi.remove(vrag)
                player.radius += 1        #добавление радиуса
                data_radius += 1
        else:
            b.otrisov(scale)
            b.fontic(vrag[4])
        #проверка на косание с едой
    for fo in foods:                    #перебирание еды
        if player.rect.colliderect(fo) and player.radius >= fo.radius: #хитбоксы еды столкнулись с игроком
            foods.remove(fo)            #удалиние Этой едыкоторая кознулась
            player.radius += 1        #добавление радиуса
            data_radius += 1


            # center_right = player.rect.center
            # player.rect.size(player.radius * 2, player.radius * 2)
            # player.rect.center = center_right                  #движение еды
        else:
            fo.otrisov(scale)
    if right == True:

        for ija in foods:                #движение еды если нажато вправо
            ija.rect.x -= 5
        data_x += 5
    if left == True:
        for ija in foods:                 #движение еды если нажато влево
            ija.rect.x += 5
        data_x -=5
    if up == True:                  #движение еды если нажато вверх
        for ija in foods: 
            ija.rect.y += 5
        data_y -= 5
    if down == True:
        for ija in foods:                 #движение еды если нажато вниз
            ija.rect.y -= 5
        data_y += 5
        
    #отрисовка  
    player.otrisov(scale)
    player.fontic(nick)
                                #отсылание данных о игроке
    client.send(f"{data_id},{data_x},{data_y},{data_radius},{nick}".encode())
    display.update()
    clock.tick(60)