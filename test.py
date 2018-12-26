from __future__ import print_function
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)
source = Gst.ElementFactory.make("audiotestsrc_py", None)
if not source:
    print("Failed to create source block")
else:
    print("Created source block:")
    print(source)
