import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

def on_gst_message(bus, message, loop):
    if message.type == Gst.MessageType.ERROR:
        err, debug_info = message.parse_error()
        print("Error received from element %s: %s" % (message.src.get_name(), err), debug_info)
        loop.quit()
    elif message.type == Gst.MessageType.WARNING:
        err, debug_info = message.parse_warning()
        print("Warning received from element %s: %s" % (message.src.get_name(), err), debug_info)
    elif message.type == Gst.MessageType.INFO:
        err, debug_info = message.parse_info()
        print("Info received from element %s: %s" % (message.src.get_name(), err), debug_info)
    return True

class GstRTSPServerExample:
    def __init__(self):
        Gst.init(None)
        Gst.debug_set_active(True)
        Gst.debug_set_default_threshold(Gst.DebugLevel.INFO)

        self.loop = GLib.MainLoop()
        self.server = GstRtspServer.RTSPServer()

        mounts = self.server.get_mount_points()
        factory = GstRtspServer.RTSPMediaFactory.new()
        factory.set_launch("( "
            "v4l2src ! "
            "video/x-raw,width=1920,height=1080,framerate=30/1 ! "
            "videoconvert ! x264enc tune=zerolatency ! "
            "rtph264pay name=pay0 pt=96 "
            ")")
        mounts.add_factory("/test", factory)
        del mounts

        # Select a suitable port for RTSP server
        self.server.set_service("8510")
        self.server.attach(None)
        print('working...')

    def __del__(self):
        self.server.unref()

    def run(self):
        self.loop.run()

if __name__ == '__main__':
    server = GstRTSPServerExample()
    # bus = server.server.get_bus().add_signal_watch()
    # bus.connect("message", on_gst_message, server.loop)
    server.run()
