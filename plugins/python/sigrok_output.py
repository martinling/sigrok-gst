from sigrok_gst import *

class Output(GstBase.BaseSink):

    __gstmetadata__ = ('Output', 'Sink', 'sigrok output sink', 'Martin Ling')

    __gsttemplates__ = Gst.PadTemplate.new("sink",
                                           Gst.PadDirection.SINK,
                                           Gst.PadPresence.ALWAYS,
                                           Gst.Caps.new_any())

    format = GObject.Property(type=str, default='bits')

    def do_start(self):
        fmt = context.output_formats[self.format]
        device = context.create_user_device("Vendor", "Model", "Version")
        for i in range(8):
            device.add_channel(i, ChannelType.LOGIC, "D%d" % i)
        self.output = fmt.create_output(device)
        return True

    def do_render(self, buf):
        ret, map_info = buf.map(Gst.MapFlags.READ)
        packet = context.create_logic_packet(map_info.data, 2)
        print(self.output.receive(packet), end=None)
        return Gst.FlowReturn.OK

    def do_stop(self):
        end_packet = context.create_end_packet()
        print(self.output.receive(end_packet))
        return True

__gstelementfactory__ = ("sigrok_output", Gst.Rank.NONE, Output)
