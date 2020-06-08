import tkinter as tk
import os, socket
import time
import threading

root = tk.Tk()
root.title("자료실")
root.geometry("800x600+100+100")

exitCheck = False
imagelist = []
idx = 0
def nextImage():
    
    global imagelist
    global idx
    global image
    global imageScreen
    print(idx)
    if(len(imagelist)>0):
        
        idx +=1
        if(idx>=len(imagelist)):
            idx=0
        print(idx)
        print(imagelist[idx])
        image = tk.PhotoImage(file = "refs/"+imagelist[idx])
        imageScreen = tk.Label(root, image = image)
        imageScreen.place(x=200, y=100)
        filename.set(imagelist[idx])
        
    
def beforeImage():
    global imagelist
    global idx   
    global image
    global imageScreen
    print(idx)
    if(len(imagelist)>0):
        
        idx -=1
        if(idx<0):
            idx=len(imagelist)-1
        print(idx)
        print(imagelist[idx])
        image = tk.PhotoImage(file = "refs/"+imagelist[idx])
        imageScreen = tk.Label(root, image = image)
        imageScreen.place(x=200, y=100)
        filename.set(imagelist[idx])
    
def Exit():
    global root
    global exitCheck
    exitCheck = True
    time.sleep(0.3)
    root.destroy()




#GUI의 mainloop가 돌고 있으면 up, down, stop 을 기다릴 수 없으므로 thread 하나를 돌려야함

#messageWaiting = threading.Thread(target=
def waitClient():
    global exitCheck
    global client_socket
    global server_socket
    
    while exitCheck==False: 
        client_socket, addr = server_socket.accept()
        waitMessage()
    server_socket.close()

def waitMessage():
    global client_socket
    global exitCheck
    while True:
        data = client_socket.recv(1024)
        menu = data.decode()
        print('menu:', menu)
        if menu=='up':
            upload(client_socket)
        elif menu=='down':
            download(client_socket)
        elif menu=='stop':
            break
        if exitCheck==True:
            break

    client_socket.close()

    
def mk_dir():
    if not os.path.isdir('refs'):
        print('refs 디렉토리 생성')
        os.mkdir('refs')

def dir_list():
    return os.listdir('refs')

def upload(soc):
    global imagelist
    global uploadLabel
    data = soc.recv(1024)
    data2 = data.decode()
    k = data2.split('/')
    f_name = k[0]
    f_size = int(k[1])
    print('f_name : ', f_name)
    print('f_size : ', f_size)
    f_list = dir_list()
    for f in f_list:
        if f_name == f:
            s = f_name.split('.')
            f_name = s[0]+'_1.'+s[1]
    f = open('refs/'+f_name, 'wb')#
    data = soc.recv(f_size)
    body = data
    print('body:', body)
    f.write(body)
    
    f.close()

    imagelist = makeImageList(dir_list())
    
   
    uploadfilename.set(f_name+" is uploaded")

def download(soc):
    msg = dir_list()
    str1 = ""
    for idx,l in enumerate(msg):
        str1 += str(idx)+"."+l+"\n"
    data = str1.encode()
    soc.sendall(data)

    data = soc.recv(1024)
    menu = int(data)
    f = open('refs/'+msg[menu], 'rb')

    body = f.read()
    f.close()
    
    soc.sendall((msg[menu].encode()))
    soc.sendall(body)
    
def main():
    global client_socket
    global server_socket
    
    HOST = '192.168.22.127'#'192.168.103.61'  #server ip
    PORT = 9999         #server port

    #server socket open. socket.AF_INET:주소체계(IPV4), socket.SOCK_STREAM:tcp 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #포트 여러번 바인드하면 발생하는 에러 방지
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #바인드:오픈한 소켓에 IP와 PORT 할당
    server_socket.bind((HOST, PORT))

    #이제 accept할 수 있음을 알림
    server_socket.listen()

    t1 = threading.Thread(target=waitClient)
    t1.start()

def makeImageList(imgs):
    n=0
    while len(imgs)>n:
        strs = imgs[n].split(".")
        if(len(strs)==2):
            if(strs[1]!="png"):
                del imgs[n]
            else:
                n+=1
        else:
            del imgs[n]
    return imgs
    

    
mk_dir()

#GUI 배치

imagelist = makeImageList(dir_list())
filename = tk.StringVar()
filename.set("")
uploadfilename = tk.StringVar()
uploadfilename.set("waiting")

if(len(imagelist)>0):
    image = tk.PhotoImage(file = "refs/"+imagelist[0])
    imageScreen = tk.Label(root, image = image)
    imageScreen.place(x=200, y=100)
    filename.set(imagelist[0])


pictureLabel    = tk.Label( root,   textvariable = filename)
pictureLabel.place( x=390,  y=50)
 
nextButton      = tk.Button(root,   text=">",   command=nextImage)
beforeButton    = tk.Button(root,   text="<",   command=beforeImage)

uploadLabel    = tk.Label( root,   textvariable=uploadfilename)
uploadLabel.place( x=390,  y=500)

ExitButton      = tk.Button(root,text="Exit", command=Exit)



nextButton.place(   x=700,  y=300)
beforeButton.place( x=100,  y=300)

ExitButton.place(   x=400,  y=550)

main()
root.mainloop()







    

