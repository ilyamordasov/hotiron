from ST7735 import ST7735, TFTColor
from sysfont import sysfont

class TFT():
    
    def __init__(self):
        
        self.tft = ST7735()
        self.tft.rotation(3)
        self.tft.initr()
        self.tft.rgb(True)
        self.tft.fill(ST7735.BLACK)
        self.old_state = {
            'state': '0',
            'temp_next': '0',
            'temp_now': '0',
            'time': '0',
            'percentage': '0'
        }

    def clear(self):
        self.tft.fill(ST7735.BLACK)

    def print(self, cmd, string):
        if cmd == 'state' and self.old_state[cmd] != string:
            self.tft.text((10, 10), self.old_state[cmd], ST7735.BLACK, sysfont, 1, nowrap = True)
            self.tft.text((10, 10), string, ST7735.WHITE, sysfont, 1, nowrap = True)
            self.old_state[cmd] = string

        elif cmd == 'temp_next' and self.old_state[cmd] != string:
            #print(cmd, self.old_state[cmd] is not string, self.old_state[cmd], string)
            self.tft.text((125, 10), '{}\xF7'.format(self.old_state[cmd]), ST7735.BLACK, sysfont, 1, nowrap = True)
            self.tft.text((125, 10), '{}'.format(string) if string is "" else '{}\xF7'.format(string), ST7735.WHITE, sysfont, 1, nowrap = True)
            self.old_state[cmd] = string

        elif cmd == 'temp_now' and self.old_state[cmd] != string:
            _x1 = int(160 / 2 - ((sysfont["Width"] * 3) * (1 + len(self.old_state[cmd]))) / 2)
            _x2 = int(160 / 2 - ((sysfont["Width"] * 3) * (1 + len(string))) / 2)
            coeff = float(string) if float(string) < 100 else 100
            self.tft.text((60, int(128 / 2 - (sysfont["Height"] * 3) / 2)), '{}\xF7'.format(float(self.old_state[cmd])), ST7735.BLACK, sysfont, 3, nowrap = True)
            self.tft.text((60, int(128 / 2 - (sysfont["Height"] * 3) / 2)), '{}\xF7'.format(string), TFTColor(0x00 + int(coeff * (0xFF / 100)), 0x00, 0xFF - int(coeff * (0xFF / 100))), sysfont, 3, nowrap = True)
            self.old_state[cmd] = string

        elif cmd == 'time' and self.old_state[cmd] != string:
            self.tft.text((10, 128 - 10 - sysfont["Height"]), '{}s'.format(self.old_state[cmd]), ST7735.BLACK, sysfont, 1, nowrap = True)
            self.tft.text((10, 128 - 10 - sysfont["Height"]), '' if float(string) is 0.0 else '{}s'.format(string), ST7735.WHITE, sysfont, 1, nowrap = True)
            self.old_state[cmd] = string

        elif cmd == 'percentage' and self.old_state[cmd] != string:
            self.tft.text((125, 128 - 10 - sysfont["Height"]), '{}%'.format(self.old_state[cmd]), ST7735.BLACK, sysfont, 1, nowrap = True)
            self.tft.text((125, 128 - 10 - sysfont["Height"]), '{}'.format(string) if string is "" else '{}%'.format(string), ST7735.WHITE, sysfont, 1, nowrap = True)
            self.old_state[cmd] = string