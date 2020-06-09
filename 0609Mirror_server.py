import cv2, socket, threading
import tkinter as tk

exitCheck = False
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
        img = client_socket.recv(640*480)
        cv2.imshow('preview',img)
        if cv2.waitKey(10) >= 0 :
            exitCheck = True
            break
    client_socket.close()

HOST = 'localhost'#'192.168.103.61'  #server ip
PORT = 8888         #server port

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