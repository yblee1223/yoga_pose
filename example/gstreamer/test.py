import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import sys

# GStreamer 초기화
Gst.init(sys.argv)

# GStreamer 파이프라인 생성
pipeline = Gst.parse_launch("playbin uri=https://file-examples.com/storage/fe7b7e0dc465e22bc9e6da8/2017/11/file_example_MP3_700KB.mp3")

# 파이프라인 실행
pipeline.set_state(Gst.State.PLAYING)

# 이벤트 루프 시작
try:
    while True:
        pass
except KeyboardInterrupt:
    # Ctrl+C가 입력되면 재생 중지
    pipeline.set_state(Gst.State.NULL)