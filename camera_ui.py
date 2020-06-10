import tkinter as tk
from tkinter import messagebox
import picamera
import time, os, socket

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('400x600+100+100')#윈도우창 크기 1600*900, 위치:100,100
        self.master.resizable(True, True)
        self.pack()
        self.effect=['negative', 'sketch', 'pastel', 'watercolor']
        self.create_widgets()
        

    def create_widgets(self):     
        self.ra = []
        self.dir_l = tk.Label(self, width=10, font=60, text='폴더경로:')
        self.dir_l.pack()
        self.dir_e = tk.Entry(self, width=30)#입력창
        self.dir_e.pack()
        
        self.file_l = tk.Label(self, width=10, font=60, text='파일명:')
        self.file_l.pack()
        self.file_e = tk.Entry(self, width=30)#입력창
        self.file_e.pack()
        
        self.save_btn = tk.Button(self, width=10, font=60, text='촬영')
        self.save_btn.pack()

        self.effect_l = tk.Label(self, width=10, font=60, text='사진효과')
        self.effect_l.pack()
        
        self.radioval=tk.IntVar()
        for idx, i in enumerate(self.effect):
            self.ra.append(tk.Radiobutton(self, text=i, variable=self.radioval, value=idx))
            self.ra[len(self.ra)-1].pack()
          
        self.img = tk.PhotoImage(file="")
        self.img_viewer = tk.Label(self.master, image=self.img)
        self.img_viewer.pack()
        
        self.fname = tk.Label(self.master, text='')
        self.fname.pack()
        
        self.up_soc = tk.Button(self, width=10, font=60, text='socket upload')
        self.up_soc.pack()
        
        self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        self.up_web.pack()
        
root = tk.Tk()
app = Application(master=root)

def save_event():
    #camera capture
    dir_name = app.dir_e.get()
    file_name = app.file_e.get()
    
    flagf = False
    flagd = os.path.isdir(dir_name)
    if flagd:
        flagf = not os.path.isfile(dir_name+'/'+file_name)
    
    if flagf==False:
        messagebox.showerror("error", "file name error")
        print("error: file name error")
        return
    
    c = picamera.PiCamera()
    c.resolution=(320, 240)
    c.image_effect = app.effect[app.radioval.get()]
    c.start_preview()
    time.sleep(1)
    c.capture(dir_name+'/'+file_name)
    c.stop_preview()
    c.close()
    
    app.img = tk.PhotoImage(file=dir_name+'/'+file_name)
    app.img_viewer['image'] = app.img
    app.fname['text'] = dir_name+'/'+file_name
    
def up_soc_event():
    HOST = '192.168.137.1'  
    PORT = 9999
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    path = app.fname.cget('text')
    f_size = os.path.getsize(path)
    f = open(path, 'rb')
    body = f.read(f_size)
    f.close()
    print(path, 'size:', f_size)
    client_socket.sendall((path.split('/')[1]+'/'+str(f_size)).encode())
    client_socket.sendall(body)
    
app.save_btn['command']=save_event
app.up_soc['command']=up_soc_event
app.mainloop()

