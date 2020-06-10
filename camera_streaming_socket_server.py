import tkinter as tk
from tkinter import messagebox
import picamera
import time, os, socket, threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('400x400+100+100')
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

root = tk.Tk()
app = Application(master=root)
flag = False

def stop_event():
    global flag
    flag = True

def action(stop, soc):#thread
    while True:
        if stop():
            break
        path = 'myVideo/transimg.png'
        data = soc.recv(50000)
        f = open(path, 'wb')
        f.write(data)       
        f.close()
        app.img = tk.PhotoImage(file=path)
        app.img_viewer['image'] = app.img
        
    print('stop thread')
    
def action2(stop, soc):#thread
    cnt=0
    while True:
        if stop():
            break
        cnt+=1
        if cnt==6:
            cnt=1
        path = 'myVideo/'+str(cnt)+'.png'
        app.img2 = tk.PhotoImage(file=path)
        app.img_viewer2['image'] = app.img2
        f = open(path, 'rb')
        body = f.read()
        f.close()
        soc.sendall(body)
        time.sleep(1)
        
    print('stop thread')
'''
def action3(stop, soc):
    while True:
        if stop():
            break
        data = soc.recv(1024)
        msg = data.decode()
        app.input.insert(0, msg)
        
def key_event(soc):
    msg = app.input.get()
    soc.sendall(msg.encode())
    app.input.delete(0, 'end')
'''
app.stop['command']=stop_event

server_ip = 'localhost'
server_port = 9999
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind((server_ip, server_port))
soc.listen()
        
client_soc, addr = soc.accept()
    
t = threading.Thread(target=action, args=(lambda:flag,client_soc))
t.start()
t2 = threading.Thread(target=action2, args=(lambda:flag,client_soc))
t2.start()
'''
chatt_soc=soc.accept()
t3 = threading.Thread(target=action3, args=(lambda:flag,chatt_soc))
t3.start()
app.input['command']=lambda:key_event(chatt_soc)
'''
app.mainloop()
print('stop main')




