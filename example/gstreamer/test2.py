import gi
from threading import Thread
import time

gi.require_version('Gst', '1.0')
# gi.require_version('GstApp', '1.0')

from gi.repository import Gst, GLib, GstApp

ip = "0"

# _ = GstApp

Gst.init()

main_loop = GLib.MainLoop()
main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()

# pipeline_str = (
#     "v4l2src device=/dev/video0 ! videoconvert ! video/x-raw,format=I420 ! "
#     "x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! "
#     "video/x-h264,profile=baseline ! h264parse ! rtph264pay ! udpsink host=127.0.0.1 port=8000 async=false"
# )

pipeline = Gst.parse_launch("v4l2src ! decodebin ! videoconvert ! autovideosink")
# pipeline = Gst.parse_launch("v4l2src ! videoconvert ! x264enc tune=zerolatency bitrate=1000 speed-preset=superfast ! video/x-h264,profile=baseline ! h264parse ! queue ! decodebin ! videoconvert ! autovideosink")



pipeline.set_state(Gst.State.PLAYING)
try: 
    while True:
        time.sleep(0.1)
        # sample = appsink.try_pull_sample(Gst.SECOND)
        # if sample is None:
        #     continue
        # print(" I got a sample! ")
except KeyboardInterrupt:
    pass


pipeline.set_state(Gst.State.NULL)
main_loop.quit()
main_loop_thread.join()