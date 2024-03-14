#!/usr/bin/env python3
import gi

gi.require_version('Gst', '1.0')
# gi.require_version('GstRtspServer', '1.0')
gi.require_version('GLib', '2.0')

from gi.repository import Gst, GLib
from gi.repository import GstRtspServer

def main():
    # GStreamer 초기화
    Gst.init(None)

    # 메인 이벤트 루프 생성
    loop = GLib.MainLoop()

    # RTSP 서버 인스턴스 생성
    server = GstRtspServer.RTSPServer.new()

    # 서버의 마운트 포인트 가져오기
    mounts = server.get_mount_points()

    # 미디어 팩토리 생성 및 설정
    factory = GstRtspServer.RTSPMediaFactory.new()
    factory.set_launch("( "
        "v4l2src ! " # DirectShow 비디오 소스 선택
        "video/x-raw,width=640,height=480,framerate=30/1 ! " # 비디오 포맷 설정
        "videoconvert ! x264enc tune=zerolatency ! " # H.264 인코더 설정
        "rtph264pay name=pay0 pt=96 " # RTP 페이로더 설정
        ")")

    # 마운트 포인트에 미디어 팩토리 추가
    mounts.add_factory("/test", factory)

    # 더 이상 마운트 포인트 참조 불필요
    mounts.unref()

    # 서버 포트 설정 (옵션)
    server.set_service("554")

    # 서버 시작
    server.attach(None)

    # 메인 이벤트 루프 실행
    loop.run()

if __name__ == "__main__":
    main()
