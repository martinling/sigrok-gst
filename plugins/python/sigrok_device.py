from sigrok_gst import *

class Device(Gst.Element):

    __gstmetadata__ = ('Device', 'Src', 'sigrok device source', 'Martin Ling')

    src_template = Gst.PadTemplate.new("src",
                                       Gst.PadDirection.SRC,
                                       Gst.PadPresence.ALWAYS,
                                       Gst.Caps.new_any())

    driver = GObject.Property(type=str, default='fx2lafw')

    def __init__(self):
        Gst.Element.__init__(self)
        self.src = Gst.Pad.new_from_template(self.src_template)
        self.add_pad(self.src)
        driver = context.drivers[self.driver]
        devices = driver.scan()
        self.device = devices[0]

    def do_change_state(self, transition):
        if transition == Gst.StateChange.READY_TO_PAUSED:
            return Gst.StateChangeReturn.NO_PREROLL
        elif transition == Gst.StateChange.PAUSED_TO_PLAYING:
            self.start()
        return Gst.StateChangeReturn.SUCCESS

    def datafeed_callback(self, device, packet):
        if packet.type == PacketType.LOGIC:
            buf = Gst.Buffer.new_wrapped(bytes(packet.payload.data))
            self.src.push(buf)
        elif packet.type == PacketType.END:
            self.session.stop()
            self.src.push_event(Gst.Event.new_eos())

    def start(self):
        self.device.open()
        self.device.config_set(ConfigKey.LIMIT_SAMPLES, 10)
        self.task = Gst.Task.new(self.run)
        self.mutex = GLib.RecMutex()
        self.task.set_lock(self.mutex)
        self.src.set_active(True)
        self.task.start()

    def run(self):
        self.session = context.create_session()
        self.session.add_device(self.device)
        self.session.add_datafeed_callback(self.datafeed_callback)
        self.session.start()
        self.session.run()
        self.task.stop()

__gstelementfactory__ = ("sigrok_device", Gst.Rank.NONE, Device)
