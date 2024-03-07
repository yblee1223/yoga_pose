import cv2
import socket
import struct

ip = '127.0.0.1'
port = 8000

# RTCP로 카메라 이미지를 받아서 계속 출력하는 코드 작성해줘
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

print(f'start listitening to {ip}: {port}')

while True:
    data, addr = sock.recvfrom(65535)
    print(data)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
