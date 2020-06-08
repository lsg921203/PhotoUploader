import tkinter as tk
from tkinter import messagebox
from tkinter import Canvas
import picamera
import os, socket
import threading
import time

root = tk.Tk()
root.title("Photo upload")
root.geometry("630x300+100+100")

foldername = "tmp"

mirrorOn=False

def Exit():
    global root
    global mirrorOn
    if(mirrorOn==True):
        mirrorOn = False
        time.sleep(0.5)
    root.destroy()

def Mirror():
    global root
    global image
    global imageScreen
    global filename
    global foldername
    global mirrorOn
    global canvas
    camera = picamera.PiCamera()# camera initialize
    camera.resolution = (320,240)
    
    while(mirrorOn == True):
        
        

        camera.capture("tmp" + '/'+"tmp"+".gif")
        image = tk.PhotoImage(file = "tmp"+'/'+"tmp"+".gif")# show on the screean
        
        #canvas.image = photo
        canvas.create_image(0,0,anchor='nw',image=image)
        canvas.image = image
    
    camera.close()
    
    
    
def Shot():
    global root
    global image
    global imageScreen
    global filename
    global foldername
    global mirrorOn
    
    if(mirrorOn==False):
        mirrorOn = True
        t1 = threading.Thread(target=Mirror)
        t1.start()
    else:
        mirrorOn = False
    
    #close the GUI 
    

def mk_dir():
    
    if not os.path.isdir(foldername):
        print(foldername + '디렉토리 생성')
        os.mkdir(foldername)

mk_dir()

foldername = tk.StringVar()
filename = tk.StringVar()
effectnum = tk.IntVar()
resolutionnum = tk.IntVar()

effect = ['negative','colorswap','film','blur','pastel','sketch','watercolor']
resolution = [(320,240),(640,480),(1024,768)]# 1.320X240 2.640X480 3.1024X768

shotButton = tk.Button(root, text="Shot!", command = Shot)
exitButton = tk.Button(root, text="Exit", command = Exit)

canvas = Canvas(height=240, width=320)


shotButton.place(    x=125 , y=100 )
exitButton.place(    x=125 , y=200 )
canvas.place(   x=300 , y=10 ) 

root.mainloop()