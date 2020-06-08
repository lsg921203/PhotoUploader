import requests

files = open('sung12.png', 'rb')

upload = {'file':files}

obj = {"title":"sung12.png", "type":"pc"}

res = requests.post("http://localhost:7878/helloWeb/upload.jsp",files = upload,data= obj)#요청 전송

a = res.content

print(a)


