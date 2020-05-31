import machine
import time
np = machine.Neopixel(machine.Pin(26), 1, 0)

np.set(0,255,0,0)
# np.setHSB(0, 0.1, 0.1, 0.05)
while True:
	for i in range (0,100):
		np.set(0, 2*i, 0, 0)
		time.sleep(0.01)
