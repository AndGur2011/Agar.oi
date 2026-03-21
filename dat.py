import customtkinter as ctk

app = ctk.CTk()
app.geometry("500x600")
app.title("Agario Battle")

title = ctk.CTkLabel(app, text="⚡ AGARIO BATTLE ⚡", font=("Arial", 36, "bold"))
title.place(x=60, y=80)

entry_name = ctk.CTkEntry(app, placeholder_text="Ваш никнейм", width=300, height=40)
entry_name.place(x=100, y=200)

entry_ip = ctk.CTkEntry(app, placeholder_text="IP сервера", width=300, height=40)
entry_ip.place(x=100, y=260)

entry_port = ctk.CTkEntry(app, placeholder_text="Порт сервера", width=300, height=40)
entry_port.place(x=100, y=320)

button = ctk.CTkButton(app, text="🚀 Старт гри!", width=200, height=45)
button.place(x=150, y=420)

app.mainloop()