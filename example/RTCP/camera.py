from time import sleep
from threading import Thread
import gi

gi.require_version('Gst', '1.0')

from gi.repository import Gst, GLib

Gst.init(None)
main_loop = GLib.MainLoop()
main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()
main_loop.run()

pipeline = Gst.parse_launch("v4l2src ! videoconvert ! autovideosink")

pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        sleep(0.1)
        print('working......')
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)

main_loop.quit()
main_loop_thread.join()
