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

def hands_transport(img, sock):
    results = hands.process(img)
    
    if results.multi_hand_landmarks:
        for handType, hand_landmarks in zip(results.multi_handedness, results.multi_hand_landmarks):
            h = handType.classification[0].label
            if h == 'Right':
                h = 'Left'
            elif h == 'Left':
                h = 'Right'
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append(lm.x)
                landmarks.append(lm.y)
                landmarks.append(lm.z)

            data = {'type': f"{h}_hand", 'landmarks': landmarks}
            udp_send(data, sock)

def pose_transport(img, sock):
    results = pose.process(img)

    landmarks = []
    if results.pose_landmarks:
        for lm in results.pose_landmarks.landmark:
            landmarks.append(lm.x)
            landmarks.append(lm.y)
            landmarks.append(lm.z)
        data = {'type': "Pose", 'landmarks': landmarks}
        udp_send(data, sock)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        ret, frame = cam.read()

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img.flags.writeable = True
        pose_transport(img, sock)
        hands_transport(img, sock)
        img.flags.writeable = False

if __name__ == "__main__":
    main()
