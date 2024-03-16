#!bin/python3
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

class GstRTSPServerExample:
    def __init__(self):
        Gst.init(None)
        self.loop = GLib.MainLoop()
        self.server = GstRtspServer.RTSPServer()

        mounts = self.server.get_mount_points()
        factory = GstRtspServer.RTSPMediaFactory.new()

        factory.set_launch("( "
            "v4l2src ! " # DirectShow 비디오 소스 선택
            "video/x-raw,width=640,height=480,framerate=30/1 ! " # 비디오 포맷 설정
            "videoconvert ! x264enc tune=zerolatency ! " # 인코딩 속도와 비트레이트 조정
            "rtph264pay name=pay0 pt=96 " # RTP 페이로더 설정
            ")")

        mounts.add_factory("/test", factory)
        del mounts

        self.server.set_service("8554")
        self.server.attach(None)
        print('working......')
        # factory.set_state(Gst.State.PLAYING)
        
    def run(self):
        self.loop.run()

if __name__ == '__main__':
    server = GstRTSPServerExample()
    server.run()
