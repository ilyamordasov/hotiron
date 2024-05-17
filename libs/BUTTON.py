from machine import Pin

class BUTTON():
    def __init__(self, pin = 23, out = None):
        self.btn = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.out = out
        self.btn.irq(trigger = Pin.IRQ_FALLING, handler = self.pressed)

    def pressed(self, arg):
        self.out()