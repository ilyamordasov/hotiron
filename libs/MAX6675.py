from machine import Pin
import utime
from FIR import FIR

class MAX6675():

    def __init__(self, cs = 14, so = 12, sck = 27):

        #Thermocouple
        self.cs = Pin(cs, Pin.OUT)
        self.cs.on()

        self.so = Pin(so, Pin.IN)
        self.so.off()

        self.sck = Pin(sck, Pin.OUT)
        self.sck.off()

        self.last_read_time = 0
        self.last_read_temp = 0
        self.last_error_tc = 0

        self.FIR = FIR(20)

    def read(self):
        #check if new reading should be available
        #if True:
        if utime.ticks_ms() - self.last_read_time > 220:

            #/*
            #  Bring CS pin low to allow us to read the data from
            #  the conversion process
            #*/
            self.cs.off()
            utime.sleep_us(10)

            #/*
            # Read bits 14-3 from MAX6675 for the Temp. Loop for each bit reading
            #   the value and storing the final value in 'temp'
            # */
            value = 0
            for i in range(12):
                self.sck.on()
                utime.sleep_us(1)
                self.sck.off()
                utime.sleep_us(1)
                value += self.so.value() << (11 - i)

            #/* Read the TC Input inp to check for TC Errors */
            self.sck.on()
            utime.sleep_us(1)
            self.sck.off()
            utime.sleep_us(1)
            error_tc = self.so.value()

            # /*
            #   Read the last two bits from the chip, faliure to do so will result
            #   in erratic readings from the chip.
            # */
            for i in range(2):
                self.sck.on()
                utime.sleep_us(1)
                self.sck.off()
                utime.sleep_us(1)

            self.cs.on()

            self.FIR.push(value)
            temp = (value * 0.25)
            self.last_read_time = utime.ticks_ms()
            self.last_read_temp = temp
            self.last_error_tc = error_tc

            return temp, error_tc

        #to soon for new reading
        else:
            return self.last_read_temp, self.last_error_tc