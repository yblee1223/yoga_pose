import cv2
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# GStreamer 초기화
Gst.init(None)

# GStreamer 파이프라인 생성
pipeline_str = "udpsrc port=5000 ! application/x-rtp,encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink"
pipeline = Gst.parse_launch(pipeline_str)
appsink = pipeline.get_by_name("appsink")

# 파이프라인 실행
pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        # GStreamer로부터 프레임 가져오기
        sample = appsink.emit("pull-sample")
        buffer = sample.get_buffer()
        caps = sample.get_caps()
        frame = Gst.Buffer.extract_dup(buffer, 0, buffer.get_size()).reshape((caps.get_structure(0).get_value('height'), caps.get_structure(0).get_value('width'), 3))

        # 화면에 출력
        cv2.imshow('Receiver', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    pass

# 파이프라인 상태 변경 및 종료
pipeline.set_state(Gst.State.NULL)
cv2.destroyAllWindows()
