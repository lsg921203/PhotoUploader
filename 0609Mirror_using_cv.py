import cv2, socket, threading
import tkinter as tk

cap = cv2.VideoCapture(0)

if cap.isOpened() == False:
    exit()

HOST = 'localhost'#'192.168.22.127'#'192.168.22.127'#'192.168.103.61'  
PORT = 8888
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    ret, img = cap.read()
    #encode -> numpy array -> trans
    #cv2.imshow('preview',img)
    print(type(img))
    client_socket.sendall(img)
    
    if cv2.waitKey(10) >= 0 :
        break
    
#disconnect
client_socket.close()
cap.release()
cv2.destroyAllWindows()

#-------------------------------




