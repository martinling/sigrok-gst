from sigrok_gst import *

class Output(GstBase.BaseSink):

    __gstmetadata__ = ('Output', 'Sink', 'sigrok output sink', 'Martin Ling')

    __gsttemplates__ = Gst.PadTemplate.new("sink",
                                           Gst.PadDirection.SINK,
                                           Gst.PadPresence.ALWAYS,
                                           Gst.Caps.new_any())

    format = GObject.Property(type=str, default='bits')

    def __init__(self):
        GstBase.BaseSink.__init__(self)
        fmt = context.output_formats[self.format]
        device = context.create_user_device("Vendor", "Model", "Version")
        self.output = fmt.create_output(device)

    def do_render(self, buf):
        ret, map_info = buf.map(Gst.MapFlags.READ)
        packet = context.create_logic_packet(map_info.data, 2)
        print(self.output.receive(packet), end=None)
        return Gst.FlowReturn.OK

__gstelementfactory__ = ("sigrok_output", Gst.Rank.NONE, Output)
