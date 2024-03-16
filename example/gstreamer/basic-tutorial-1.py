#!/usr/bin/env python3

import sys
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')

from gi.repository import Gst, GLib, GObject

pipeline = None
bus = None
message = None

Gst.init(sys.argv[1:])

pipeline = Gst.parse_launch(
    "playbin uri=https://gstreamer.freedesktop.org/data/media/sintel_trailer-480p.webm"
)

pipeline.set_state(Gst.State.PLAYING)

bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(
    Gst.CLOCK_TIME_NONE,
    Gst.MessageType.ERROR | Gst.MessageType.EOS
)

pipeline.set_state(Gst.State.NULL)