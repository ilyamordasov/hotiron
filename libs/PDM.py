from machine import Pin, Timer

class PDM():
    def __init__(self, pout = 15, tim = 4, freq = 50):
        """
        :param pout: output pin nr
        :param tim:  timer number
        :param freq: frequency of the bitstream
        """
        self.max = 2**24-1#2**31-1 crashes with larger ints? 24bit resolution is fine enough ;)

        self.pout = Pin(pout, Pin.OUT)
        self.pout.off()

        self.err = 0 # error accumulator
        self.output = 0

        self.freq = int(1 / freq * 1000)

        self.tim = Timer(tim)
        self.tim.init(period = freq, callback = lambda t: self.call_me())

    def set_output(self, out):
        """
        :param out: desired output as a value between 0 and 1
        """
        #print ('setting output to ' + str(out))
        self.tim.deinit()

        self.output = int(self.max * out)

        self.tim.init(period = self.freq, callback = lambda t: self.call_me())

    def on(self): self.pout.on()
    def off(self): self.pout.off()

    def call_me(self):
        if self.err >= 0:
            self.pout.off()
            self.err -= self.output
        else:
            self.pout.on()
            self.err += self.max
            self.err -= self.output