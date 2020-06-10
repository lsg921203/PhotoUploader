import threading, socket, picamera
import tkinter as tk
from functools import partial

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('800x600+100+100')#윈도우창 크기 1600*900, 위치:100,100
        self.master.resizable(True, True)
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):     
        self.img1 = tk.PhotoImage(file="imgtest/1.png")
        self.img_me = tk.Label(self.master, image=self.img1)
        self.img_me.pack(side='left')
        
        self.img2 = tk.PhotoImage(file="imgtest/2.png")
        self.img_other = tk.Label(self.master, image=self.img2)
        self.img_other.pack(side='right')
        
        self.chatt_box = tk.Label(self, width=30, height=10, font=60, text='chatting content\n')
        self.chatt_box.pack(side='top')
        self.msgs = ['','','','','','']
        self.msg_cnt = 0
        
        self.input = tk.Entry(self, width=30)#입력창
        self.input.pack()
        self.send = tk.Button(self, width=10, font=60, text='send msg')
        self.send.pack()
        
root = tk.Tk()
app = Application(master=root)

def th_me(soc, stop):
    c = picamera.PiCamera()
    c.resolution=(320, 240)
    while True:
        if stop():
            break
        path = 'myVideo/frame.png'
        c.capture(path)
        app.img1 = tk.PhotoImage(file=path)
        app.img_me['image'] = app.img1
        soc.sendall(app.img1)
    c.close()
    soc.close()
    print('stop camera')
    
def th_oth(soc, stop):
    while True:
        if stop():
            break
        app.img2 = soc.recv(320, 240)
        app.img_other['image'] = app.img2
    soc.close()
    print('stop recv image')
    
def th_msg(soc, stop):
    while True:
        if stop():
            break
        msg = soc.recv(1024)
        print(msg)
    
    
def send_event(soc):
    
def main():
    HOST = '192.168.103.70'  #server ip
    PORT = [1111, 2222, 3333]         #server port
    soc = [0,0,0]
    client_soc = [0,0,0]
    th = [0,0,0]
    func = [th_me, th_oth, th_msg]
    flag = False
    
    for i in range(0, len(soc)):
        soc[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc[i].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc[i].bind((HOST, PORT[i]))
        soc[i].listen()
        
    for i in range(0, len(soc)):
        client_soc[i] = soc[i].accept()
        th[i] = threading.Thread(target=func[i], args=(client_soc[i], lambda:flag))
        th[i].start()
        
    app.send.bind('<Button-1>', partial:(send_event, client_soc[2]))
    app.mainloop()
    
main()