import tkinter as tk
import os, time, socket, threading, sys

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('500x600+100+100')#윈도우창 크기 1600*900, 위치:100,100
        self.master.resizable(True, True)
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):     
        
        self.title = tk.Label(self, width=30, font=60, text='이미지 전송앱 서버')
        self.title.pack()
        self.init_str = '<접속상태>\nserver ip:192.168.137.1/port:9999\n'
        self.msgs = [self.init_str,'','','','','']
        self.msg_cnt = 1
        
        self.state = tk.Label(self, width=30, font=60, text=self.init_str)
        self.state.pack()

        self.img = tk.PhotoImage(file="")
        self.img_viewer = tk.Label(self.master, image=self.img)
        self.img_viewer.pack()

        self.slide = tk.Button(self, width=10, font=60, text='next')
        self.slide.pack()

        
root = tk.Tk()
app = Application(master=root)

cnt=0
imgs=None

def slide_event():
    global imgs
    global cnt
    
    imgs = os.listdir('imgs')
    size = len(imgs)
    
    app.img = tk.PhotoImage(file='imgs/'+imgs[cnt%size])
    app.img_viewer["image"]=app.img
    cnt+=1

def upload(soc):
    data = soc.recv(1024)#파일명/크기
    data2 = data.decode()
    k = data2.split('/')
    f_name = k[0]       #파일명
    f_size= int(k[1])   #크기
    f = open('imgs/'+f_name, 'wb')
    data = soc.recv(f_size)
    print('size:', f_size)
    f.write(data)
    f.close()
    app.img = tk.PhotoImage(file='imgs/'+f_name)
    app.img_viewer["image"]=app.img
    
    
def server():
    HOST = '192.168.137.1'  #server ip
    PORT = 9999         #server port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    while True:
        client_socket, addr = server_socket.accept()
        app.msgs[app.msg_cnt] = 'client:'+str(addr)+' 접속=>사진업로드\n'
        app.msg_cnt+=1
        if app.msg_cnt==len(app.msgs):
            app.msg_cnt=1
        s=''
        for i in app.msgs:
            s+=i
            
        app.state.configure(text=s)
        upload(client_socket)
    soc.close()

app.slide['command']=slide_event
t = threading.Thread(target=server, args=())
t.start()
app.mainloop()
