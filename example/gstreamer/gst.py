import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

def main():
    Gst.init(None)

    source = Gst.ElementFactory.make("v4l2src", "source")
    convert = Gst.ElementFactory.make("videoconvert", "convert")
    encoder = Gst.ElementFactory.make("x264enc", "encoder")
    payloader = Gst.ElementFactory.make("rtph264pay", "payloader")
    sink = Gst.ElementFactory.make("udpsink", "sink")

    pipeline = Gst.Pipeline.new("video-stream-pipeline")
    if not pipeline or not source or not convert or not encoder or not payloader or not sink:
        print("Not all elements could be created.")
        return -1

    # Set "buffer-size" property for udpsrc
    


    pipeline.add(source)
    pipeline.add(convert)
    pipeline.add(encoder)
    pipeline.add(payloader)
    pipeline.add(sink)

    if not source.link(convert) or not convert.link(encoder) or not encoder.link(payloader) or not payloader.link(sink):
        print("Elements could not be linked.")
        return -1

    sink.set_property("host", "192.168.1.80")
    sink.set_property("port", 5034)

    udpsrc = sink.get_static_pad("sink").get_parent_element()
    udpsrc.set_property("buffer-size", 524288)
    encoder.set_property("tune", "zerolatency")

    
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Unable to set the pipeline to the playing state.")
        return -1

    bus = pipeline.get_bus()
    msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

    if msg:
        msg.unref()

    pipeline.set_state(Gst.State.NULL)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
