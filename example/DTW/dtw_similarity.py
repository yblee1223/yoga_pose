import cv2
import mediapipe as mp
import numpy as np
import math
from dtaidistance import dtw

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def angle_to_vector(angle):
    # 각도를 라디안으로 변환
    radians = math.radians(angle)
    # 각도를 벡터로 변환
    x = math.cos(radians)
    y = math.sin(radians)
    return (x, y)

def cosine_similarity(vector1, vector2):
    # 두 벡터의 내적 계산
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    # 각 벡터의 크기(norm) 계산
    norm1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    norm2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    # 코사인 유사도 계산
    similarity = dot_product / (norm1 * norm2)
    return similarity

def calculate_cosine_similarity(ref_keypoints, keypoints):
    s = [0]*5
    s[0] = cosine_similarity(ref_keypoints['head'], keypoints['head'])

    part = ['left_arms', 'right_arms', 'left_legs', 'right_legs']
    for i, p in enumerate(part, 1):
        s[i] = cosine_similarity(angle_to_vector(ref_keypoints[p][0]), angle_to_vector(keypoints[p][0]))
        s[i] += cosine_similarity(angle_to_vector(ref_keypoints[p][1]), angle_to_vector(keypoints[p][1]))
        s[i] /= 2.0
    
    return s

def extract_keypoints(results):
    landmarks = results.pose_landmarks.landmark
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

    left_shoulder_angle = calculateAngle(left_elbow, left_shoulder, left_hip)
    right_shoulder_angle = calculateAngle(right_elbow, right_shoulder, right_hip)
    left_elbow_angle = calculateAngle(left_shoulder, left_elbow, left_wrist)
    right_elbow_angle = calculateAngle(right_shoulder, right_elbow, right_wrist)
    left_hip_angle = calculateAngle(left_knee, left_hip, left_shoulder)
    right_hip_angle = calculateAngle(right_knee, right_hip, right_shoulder)
    left_knee_angle = calculateAngle(left_hip, left_knee, left_ankle)
    right_knee_angle = calculateAngle(right_hip, right_knee, right_ankle)

    keypoints = {}
    keypoints['head'] = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
    keypoints['left_arms'] = [left_shoulder_angle, left_elbow_angle]
    keypoints['right_arms'] = [right_shoulder_angle, right_elbow_angle]
    keypoints['left_legs'] = [left_hip_angle, left_knee_angle]
    keypoints['right_legs'] = [right_hip_angle, right_knee_angle]

    return keypoints

def hpk(frame): # hpk = human pose keypoints
    results = pose.process(frame)
    if results.pose_landmarks:
        return extract_keypoints(results)
    else: return None
    
def calculateAngle(a, b, c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    return angle

def putAngle(frame, s):
    fontsize= 0.7
    fontcolor = (0, 255, 255)
    x = 400

    cv2.putText(frame, f'head: {round(s[0], 2)}', (x, 50), cv2.FONT_HERSHEY_SIMPLEX, fontsize, fontcolor, 2, cv2.LINE_AA)
    cv2.putText(frame, f'left_arms: {round(s[1], 2)}', (x, 100), cv2.FONT_HERSHEY_SIMPLEX, fontsize, fontcolor, 2, cv2.LINE_AA)
    cv2.putText(frame, f'right_arms: {round(s[2], 2)}', (x, 150), cv2.FONT_HERSHEY_SIMPLEX, fontsize, fontcolor, 2, cv2.LINE_AA)
    cv2.putText(frame, f'left_legs: {round(s[3], 2)}', (x, 200), cv2.FONT_HERSHEY_SIMPLEX, fontsize, fontcolor, 2, cv2.LINE_AA)
    cv2.putText(frame, f'right_legs: {round(s[4], 2)}', (x, 250), cv2.FONT_HERSHEY_SIMPLEX, fontsize, fontcolor, 2, cv2.LINE_AA)

def main():
    # image
    img = cv2.imread('data/yoga/goddes.jpg')
    ref_keypoints = hpk(img)
    
    # vidio
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: 카메라 또는 비디오를 열 수 없습니다.")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: 프레임을 읽을 수 없습니다.")
            break
        keypoints = hpk(frame)
        if keypoints:
            s = calculate_cosine_similarity(ref_keypoints, keypoints)
            similarity = sum(s) / len(s)
            cv2.putText(frame, f'Similarity: {round(similarity, 2)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            putAngle(frame, s)
            print(similarity)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()