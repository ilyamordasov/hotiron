#https://github.com/B3AU/micropython

import sys
import utime
import micropython
import math
sys.path.append("./libs")

from MAX6675 import MAX6675
from PDM import PDM
from TFT import TFT
from PID import PID
from BUTTON import BUTTON

micropython.alloc_emergency_exception_buf(100)

state = [("OFF", 0.0), ("PREHEAT", 50.0), ("REFLOW", 250.0), ("COOLING", 0.0)]
state_idx = 0

pdm = PDM()
tc = MAX6675()
tft = TFT()

def btn_pressed():
    global state_idx, state
    utime.sleep(0.3)
    state_idx += 1
    state_idx = 0 if state_idx >= len(state) else state_idx
    updateScreen()


btn = BUTTON(out = btn_pressed)
btn_r = BUTTON(pin = 32, out = btn_pressed)

pdm.set_output(0.7)

def updateScreen():
    global state, state_idx, tc, pid
    temp, tc_err = tc.read()
    pid.set_point = state[state_idx][1]
    pid.update()
    avg_temp = tc.FIR.get_value() * 0.25
    avg_temp = str(avg_temp)

    tft.print('temp_now', str(int(float(avg_temp))))
    tft.print('temp_next', str(state[state_idx][1]))
    _pid = "O: " + str(pid.output) + " P: " + str(pid.P_value) + " I: " + str(pid.I_value) + " D: " + str(pid.D_value)
    tft.print('time', str(pid.output))
    tft.print('percentage', str(int(100 / len(state) * (state_idx+1))))
    tft.print('state', str(state[state_idx][0]))#str(pid.I_value)[:5])

    if float(avg_temp) > state[state_idx][1]:
        if state_idx != 0: btn_pressed()
    else: pdm.on()
    # print(float(pid.set_point), float(avg_temp), float(pid.output))

    utime.sleep_ms(50)

def get_temp():
    global tc
    return tc.FIR.get_value() * 0.25

pid = PID(get_temp, pdm.set_output, P = 1.4, I = 0.4, D = 64.0)
pid.set_point = 0

def init():
    global tft
    tft.clear()
    while True:#sw_state:
        updateScreen()

init()