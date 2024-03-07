import socket
import cv2

# ------------ UDP -------------
ip = "127.0.0.1"
port = 5000
msg = 'hello world!'

print(f'send the msg: {msg}')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(msg.encode(), (ip, port))