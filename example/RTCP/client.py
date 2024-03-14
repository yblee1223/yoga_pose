import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def pad_added_handler(src, new_pad, sink):
    sink_pad = sink.get_static_pad("sink")
    if sink_pad.is_linked():
        return
    new_pad.link(sink_pad)
    print("Link succeeded (type 'video/x-h264').")

def error_cb(bus, msg, loop):
    err, debug_info = msg.parse_error()
    print("Error received from element {}: {}".format(msg.src.get_name(), err))
    print("Debugging information: {}".format(debug_info if debug_info else "none"))
    loop.quit()

def eos_cb(bus, msg, loop):
    print("End-Of-Stream reached.")
    loop.quit()

def main():
    Gst.init(None)

    main_loop = GLib.MainLoop()

    source = Gst.ElementFactory.make("rtspsrc", "source")
    depayloader = Gst.ElementFactory.make("rtph264depay", "depayloader")
    decoder = Gst.ElementFactory.make("avdec_h264", "decoder")
    convert = Gst.ElementFactory.make("videoconvert", "convert")
    sink = Gst.ElementFactory.make("autovideosink", "sink")

    pipeline = Gst.Pipeline.new("rtsp-client-pipeline")
    if not pipeline or not source or not depayloader or not decoder or not convert or not sink:
        print("Not all elements could be created.")
        return -1

    source.set_property("location", "rtsp://localhost:8510/test")
    source.set_property("latency", 0)

    source.connect("pad-added", pad_added_handler, depayloader)

    pipeline.add(source)
    pipeline.add(depayloader)
    pipeline.add(decoder)
    pipeline.add(convert)
    pipeline.add(sink)

    depayloader.link(decoder)
    decoder.link(convert)
    convert.link(sink)

    sink.set_property("sync", False)

    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Unable to set the pipeline to the playing state.")
        return -1

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message::error", error_cb, main_loop)
    bus.connect("message::eos", eos_cb, main_loop)

    try:
        main_loop.run()
    except KeyboardInterrupt:
        pipeline.set_state(Gst.State.NULL)
        main_loop.quit()

if __name__ == '__main__':
    main()
