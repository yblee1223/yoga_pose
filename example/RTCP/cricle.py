#!/usr/bin/env python3


import os
from gi.repository import Gst, GLib
import sys

import gi
gi.require_version('Gst', '1.0')

gi.require_version('GLib', '2.0')


def on_message(bus: Gst.Bus, message: Gst.Message, loop: GLib.MainLoop):
    msg = message.type

    if msg == Gst.MessageType.EOS:
        print("on_message : End Of Stream")
        loop.quit()

    elif msg == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        print("on_message : Warnning -", err, debug)

    elif msg == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("on_message : Error -", err, debug)
        loop.quit()

    return True


def graph_pipeline(pipeline):
    Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL,
                              "pipeline")
    try:
        os.system("dot -Tpng -o ./pipeline.png ./pipeline.dot")
    except Exception as e:
        print(e)


def main():
    Gst.init(sys.argv)

    # set gst pipeline with videotestsrc (ball pattern)
    pipeline = Gst.parse_launch(
        "videotestsrc pattern=18 num-buffers=300 ! autovideosink") # pattern=18 : ball pattern, num-buffers=300 : 300 frames, autovideosink : display
    pipeline.set_state(Gst.State.PLAYING)

    loop = GLib.MainLoop()

    # connect bus to catch signal from the pipeline
    # bus : pipeline의 상태 변화, 메시지 등을 받아서 처리하는 역할
    bus = pipeline.get_bus() # 
    bus.add_signal_watch()
    bus.connect("message", on_message, loop) # message signal을 받아서 on_message 함수를 실행

    # run
    loop.run()

    graph_pipeline(pipeline)

    # if fails, then clean
    pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    main()