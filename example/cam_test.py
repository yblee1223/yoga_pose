import cv2
# 카메라 영상을 받아오기 위한 모듈
import numpy as np
# 이미지를 처리하기 위한 모듈


cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("cam is not working")

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1080//2, 1980//2))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
# 카메라를 실행시키고 영상을 받아오는 코드입니다.
    
cam.release()