import socket
import cv2
import mediapipe as mp
import pickle

cam = cv2.VideoCapture(0)

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands 

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)


# ------------ UDP -------------
ip = "127.0.0.1"
port = 5000
# -----------------------------

def udp_send(data, sock):
    data = pickle.dumps(data)
    sock.sendto(data, (ip, port))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        ret, frame = cam.read()

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # img udp send
        data = {'type': 'img', 'img': img}
        udp_send(data, sock)

if __name__ == "__main__":
    main()
