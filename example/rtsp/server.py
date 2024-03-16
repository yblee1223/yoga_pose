import gi
import sys

gi.require_version('Gst', '1.0')
gi.require_version('GObject', '2.0')
gi.require_version('GLib', '2.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GObject, GLib, GstRtspServer
# import GObject.GstRtspServer.RTSPMediaFactory
class rtsp:
    def __init__(self):
        Gst.init(sys.argv[1:])
        self.loop = GLib.MainLoop()
        self.server = GstRtspServer.RTSPServer()

        mounts = self.server.get_mount_points()
        factory = GstRtspServer.RTSPMediaFactory.new()

        factory.set_launch("v4l2src ! videoconvert ! video/x-raw,format=I420 ! x264enc tune=zerolatency ! rtph264pay name=pay0 pt=96")

        # factory.set_latency(100)  # 지연 시간을 밀리초 단위로 설정
        # factory.set_buffer_size(0)  # 버퍼 크기를 0으로 설정하여 버퍼를 비활성화

        
        mounts.add_factory('/test', factory)
        del mounts

        self.server.set_service('8554')
        self.server.attach(None)
        
    def run(self):
        self.loop.run()

if __name__ == '__main__':
    server = rtsp()
    server.run()