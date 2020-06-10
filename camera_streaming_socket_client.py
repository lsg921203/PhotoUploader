import tkinter as tk
from tkinter import messagebox
import picamera
import time, os, socket, threading, queue
from functools import partial

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('400x400+100+100')#윈도우창 크기 1600*900, 위치:100,100
        self.master.resizable(True, True)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.img = tk.PhotoImage(file="")
        self.img_viewer = tk.Label(self.master, image=self.img)
        self.img_viewer.pack()
        
        self.img2 = tk.PhotoImage(file="")
        self.img_viewer2 = tk.Label(self.master, image=self.img2)
        self.img_viewer2.pack()
        
        self.stop = tk.Button(self, width=10, font=60, text='stop')
        self.stop.pack()
        
        self.input = tk.Entry(self, width=30)
        self.input.pack()
        
        self.chatt_box = tk.Label(self, width=30, height=10, font=60, text='chatting content\n')
        self.chatt_box.pack(side='top')
       
root = tk.Tk()
app = Application(master=root)
flag = False

def stop_event():
    global flag
    flag = True

def action(stop, soc):#thread
    c = picamera.PiCamera()
    c.resolution=(150, 100)
    while True:
        if stop():
            break
        path = 'myVideo/frame.png'
        c.capture(path)
        app.img = tk.PhotoImage(file=path)
        app.img_viewer['image'] = app.img
        f = open(path, 'rb')
        body = f.read()
        f.close()
        soc.sendall(body)
        
    c.close()
    print('stop thread')
    
def action2(stop, soc):#thread
    
    while True:
        if stop():
            break
        path = 'myVideo/trans2.png'
        data = soc.recv(50000)
        f = open(path, 'wb')
        f.write(data)       
        f.close()
        app.img2 = tk.PhotoImage(file=path)
        app.img_viewer2['image'] = app.img2
        
    print('stop thread')

def action3(stop, soc):
    while True:
        if stop():
            break
        data = soc.recv(1024)
        msg = data.decode()
        app.chatt_box.configure(text=msg)
        
def key_event(soc, e):
    msg = app.input.get()
    soc.sendall(msg.encode())
    app.chatt_box.configure(text=msg)
    app.input.delete(0, 'end')

app.stop['command']=stop_event

server_ip = 'localhost'
server_port = 9999
client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_soc.connect((server_ip, server_port))
    
t = threading.Thread(target=action, args=(lambda:flag,client_soc))
t.start()
t2 = threading.Thread(target=action2, args=(lambda:flag,client_soc))
t2.start()

chatt_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chatt_soc.connect((server_ip, server_port))

t3 = threading.Thread(target=action3, args=(lambda:flag,chatt_soc))
t3.start()
app.input.bind('<Return>', partial(key_event,chatt_soc))

app.mainloop()
print('stop main')



