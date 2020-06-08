import tkinter as tk
from tkinter import messagebox
import picamera
import os, socket
import threading

root = tk.Tk()
root.title("Photo upload")
root.geometry("630x300+100+100")

foldername = "tmp"

mirrorOn=False

def Exit():
    global root
    root.destroy()

def Mirror():
    global root
    global image
    global imageScreen
    global filename
    global foldername
    global mirrorOn
    camera = picamera.PiCamera()# camera initialize
    camera.resolution = (320,240)
    
    while(mirrorOn == True):
        
        

        camera.capture("tmp" + '/'+"tmp"+".png")
        image = tk.PhotoImage(file = "tmp"+'/'+"tmp"+".png")# show on the screean
        imageScreen = tk.Label(root, image = image)
        imageScreen.place(   x=300 , y=10 ) 
    
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

shotButton.place(    x=125 , y=100 )
exitButton.place(    x=125 , y=250 )


root.mainloop()