import tkinter as tk
import os, socket
import picamera
import time
import RPi.GPIO as GPIO
import requests

SWITCH = 26#GPIO26
RLED = 19
GLED = 13
BLED = 6
#----------------------------------------------
#IO initialize
GPIO.setmode(GPIO.BCM)

GPIO.setup(SWITCH, GPIO.IN)
GPIO.setup(RLED, GPIO.OUT,initial= GPIO.LOW)
GPIO.setup(GLED, GPIO.OUT,initial= GPIO.LOW)
GPIO.setup(BLED, GPIO.OUT,initial= GPIO.LOW)
    
r = GPIO.PWM(RLED,100)
g = GPIO.PWM(GLED,60)
b = GPIO.PWM(BLED,70)
    
rdc = 0.0
gdc = 0.0
bdc = 0.0

r.start(rdc)
g.start(gdc)
b.start(bdc)

#------------------------------------------------
# UI Initialize
root = tk.Tk()
root.title("Photo upload")
root.geometry("630x300+100+100")

foldername = tk.StringVar()
filename = tk.StringVar()
effectnum = tk.IntVar()
resolutionnum = tk.IntVar()

effect = ['negative','colorswap','film','blur','pastel','sketch','watercolor']
resolution = [(320,240),(640,480),(1024,768)]# 1.320X240 2.640X480 3.1024X768 
#-----------------------------------------------


def Exit():
    global root
    
    
    #close the GUI 
    root.destroy()
    
    #close the IO
    GPIO.remove_event_detect(SWITCH)
    GPIO.cleanup()

def ShotBySW(p):
    Shot()
    time.sleep(0.5)

def Shot():
    global root
    global image
    global imageScreen
    global filename
    global foldername
    
    mk_dir()
    
    # take photo and save
    camera = picamera.PiCamera()# camera initialize
    camera.resolution = (320,240)
    camera.image_effect = effect[effectnum.get()]
    
    r.ChangeDutyCycle(100.)# flash on
    g.ChangeDutyCycle(100.)
    b.ChangeDutyCycle(100.)
    time.sleep(0.05)
    camera.capture(foldername.get()+'/'+"tmp"+".png")
    camera.resolution = resolution[resolutionnum.get()]
    #resolution change(      )
    camera.capture(foldername.get()+'/'+filename.get()+".png")# take a photo
    camera.close()
    
    time.sleep(0.05)
    r.ChangeDutyCycle(0.)# flash off
    g.ChangeDutyCycle(0.)
    b.ChangeDutyCycle(0.)
    
    image = tk.PhotoImage(file = foldername.get()+'/'+"tmp"+".png")# show on the screean
    imageScreen = tk.Label(root, image = image)
    imageScreen.place(   x=300 , y=10 ) 
    print(effect[effectnum.get()])
    
def up(soc):
    f_dir = foldername.get()
    f_name = filename.get()+".png"
    f_size = os.path.getsize(f_dir+'/'+f_name)
    f = open(f_dir+'/'+f_name, 'rb')
    body = f.read()
    f.close()
    soc.sendall((f_name+'/'+str(f_size)).encode())
    time.sleep(0.5*(f_size/90000))
    soc.sendall(body)

def webUpload():
    f_dir = foldername.get()
    f_name = filename.get() + ".png"
    files = open(f_dir+"/"+f_name, 'rb')

    upload = {'file': files}

    obj = {"title": f_dir+"/"+f_name, "type": "pc"}

    res = requests.post("http://localhost:7878/helloWeb/upload.jsp", files=upload, data=obj)

def socketUpload():
    
    HOST = '192.168.22.91'#'192.168.22.127'#'192.168.22.127'#'192.168.103.61'  
    PORT = 9999
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall('up'.encode())
    up(client_socket)
    time.sleep(0.5)
    client_socket.sendall('stop'.encode())
    client_socket.close()

def mk_dir():
    global foldername
    if not os.path.isdir(foldername.get()):
        print(foldername.get() + '디렉토리 생성')
        os.mkdir(foldername.get())

GPIO.add_event_detect(SWITCH,GPIO.RISING,ShotBySW,1000)

folderLabel = tk.Label(root, text="folder name")
folderTextBox = tk.Entry(root, width=20, textvariable=foldername)

fileLabel = tk.Label(root, text="file name")
fileTextBox = tk.Entry(root, width=20, textvariable=filename)

shotButton = tk.Button(root, text="Shot!", command = Shot)

effectRadioButton1 = tk.Radiobutton(root,text = "negative"  , value=0, variable = effectnum)
effectRadioButton2 = tk.Radiobutton(root,text = "colorswap" , value=1, variable = effectnum)
effectRadioButton3 = tk.Radiobutton(root,text = "film"      , value=2, variable = effectnum)
effectRadioButton4 = tk.Radiobutton(root,text = "blur"      , value=3, variable = effectnum)
effectRadioButton5 = tk.Radiobutton(root,text = "pastel"    , value=4, variable = effectnum)
effectRadioButton6 = tk.Radiobutton(root,text = "sketch"    , value=5, variable = effectnum)
effectRadioButton7 = tk.Radiobutton(root,text = "watercolor"    , value=6, variable = effectnum)

resolutionRadioButton1 = tk.Radiobutton(root,text = "320x240"   , value=0, variable = resolutionnum)
resolutionRadioButton2 = tk.Radiobutton(root,text = "640x480"   , value=1, variable = resolutionnum)
resolutionRadioButton3 = tk.Radiobutton(root,text = "1024x768"  , value=2, variable = resolutionnum)#resolution control button making

webUploadButton  = tk.Button(root, text="WebUpload", command = webUpload)
socketUploadButton = tk.Button(root, text="SocketUpload", command = socketUpload)

exitButton = tk.Button(root, text="Exit", command = Exit)


folderLabel.place(   x=20  , y=10 )
folderTextBox.place( x=120 , y=10 )

fileLabel.place(     x=20  , y=40 )
fileTextBox.place(   x=120 , y=40 )

shotButton.place(    x=125 , y=100 )

X1   = 10
Xdif = 95
Y1   = 160
Ydif = 30
effectRadioButton1.place(  x=X1+0*Xdif , y=Y1+0*Ydif)
effectRadioButton2.place(  x=X1+0*Xdif , y=Y1+1*Ydif)
effectRadioButton3.place(  x=X1+0*Xdif , y=Y1+2*Ydif)
effectRadioButton7.place(  x=X1+0*Xdif , y=Y1+3*Ydif)
effectRadioButton4.place(  x=X1+1*Xdif , y=Y1+0*Ydif)
effectRadioButton5.place(  x=X1+1*Xdif , y=Y1+1*Ydif)
effectRadioButton6.place(  x=X1+1*Xdif , y=Y1+2*Ydif)

resolutionRadioButton1.place( x=X1+2*Xdif , y=Y1+0*Ydif)
resolutionRadioButton2.place( x=X1+2*Xdif , y=Y1+1*Ydif)
resolutionRadioButton3.place( x=X1+2*Xdif , y=Y1+2*Ydif)



#imageScreen.place(   x=300 , y=10 )
socketUploadButton.place(  x=450 , y=260 ) 

exitButton.place(    x=570 , y=260 )
root.mainloop()
