import cv2

def main():
    # 카메라 장치 번호 또는 비디오 파일 경로
    camera_source = "/dev/video0"  # 로컬 카메라 사용 (카메라 장치 번호)
    camera_source = "//home/whatslab/Repository/yoga_pose/data/dance/solo.mp4"  # 비디오 파일 사용

    # GStreamer RTSP 서버 주소
    rtsp_server_address = "rtsp://192.168.1.51:8554/live"

    # GStreamer pipeline 생성
    pipeline = f"v4l2src device={camera_source} ! videoconvert ! video/x-raw,format=I420 ! x264enc tune=zerolatency bitrate=512 speed-preset=superfast ! rtph264pay config-interval=1 pt=96 ! udpsink host={rtsp_server_address}"
    # pipeline = "v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! videoconvert ! appsink"
    # pipeline = "v4l2src device=/dev/video0 ! videoconvert ! x264enc tune=zerolatency bitrate=512 speed-preset=superfast ! rtph264pay config-interval=1 pt=96 ! udpsink host=127.0.0.1 port=5000"
    # pipeline = "v4l2src device=/dev/video0 ! videoconvert ! udpsink host=127.0.0.1 port=5000" # pass
    # pipeline = "v4l2src device=/dev/video0 ! videoconvert ! video/x-raw,format=I420 ! x264enc tune=zerolatency ! rtph264pay name=pay0 pt=96 ! udpsink host=127.0.0.1 port=5000"
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: 카메라 또는 비디오를 열 수 없습니다.")
        return

    print("RTSP 서버에 연결되었습니다.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: 프레임을 읽을 수 없습니다.")
            break

        # 프레임 표시 (Optional)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 종료 시 정리 작업
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
