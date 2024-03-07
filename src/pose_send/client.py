import socket
import pickle
import cv2
import numpy as np

ip = "127.0.0.1"
port = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((ip, port)) 

print(f'start listitening to {ip}: {port}')

img = np.ones((1080, 1980, 3), dtype=np.uint8) * 255

h, w, c = img.shape

while True:
    data, addr = sock.recvfrom(1024)
    data = pickle.loads(data)
    if data['type'] == 'Pose':
        x, y = data['landmarks'][0]* w, data['landmarks'][1]* h
        # cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
        print(f'pose = x: {x}, y: {y}')
    elif data['type'] == 'Right_hand':
        x, y = data['landmarks'][0]* w, data['landmarks'][1]* h
        # cv2.circle(img, (x, y), 10, (255, 0, 0), -1)
    elif data['type'] == 'Left_hand':
        x, y = data['landmarks'][0]* w, data['landmarks'][1]* h
        # cv2.circle(img, (x, y), 10, (0, 255, 0), -1)
    # print(data)
    cv2.imshow('frame', img)