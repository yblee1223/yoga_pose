import cv2
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# GStreamer 초기화
Gst.init(None)

# 웹캠 캡처 설정
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# GStreamer 파이프라인 생성
pipeline_str = f"appsrc name=source is-live=true do-timestamp=true ! videoconvert ! video/x-raw,format=BGR,width={width},height={height},framerate={fps}/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=127.0.0.1 port=5000"
pipeline = Gst.parse_launch(pipeline_str)
appsrc = pipeline.get_by_name("source")

# 파이프라인 실행
pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        # 웹캠에서 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임을 GStreamer에 전송
        data = frame.tostring()
        buf = Gst.Buffer.new_wrapped(data)
        appsrc.emit("push-buffer", buf)

        # 화면에 출력
        cv2.imshow('Sender', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    pass

# 파이프라인 상태 변경 및 종료
pipeline.set_state(Gst.State.NULL)
cap.release()
cv2.destroyAllWindows()
