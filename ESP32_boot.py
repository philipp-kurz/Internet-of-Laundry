from network import WLAN, STA_IF
import time
from machine import Pin, Neopixel, RTC

# Shortcuts to neopixel colors
R = Neopixel.RED
G = Neopixel.GREEN
B = Neopixel.BLUE
P = Neopixel.PURPLE
Y = Neopixel.YELLOW

######################################
# 2x BLUE: Script started
# blinking PUPRLE: Connecting to WiFi
# 1st GREEN: WiFi connected
# blinking YELLOW: syncing time
# 4x GREEN: boot process done
######################################

# Set up neopixel and turn off
np = Neopixel(Pin(26), 1, 0)
np.set(0,0,0,0)

for _ in range(2):
        np.set(0,B,0,0)
        time.sleep(0.1)
        np.set(0,0,0,0)

# Activate Wifi connection
wlan = WLAN(STA_IF)
wlan.active(True)

wlan.connect("Philipp", "Philipp123", 5000)

while not wlan.isconnected():
    if wlan.isconnected():
        break
    print("Waiting for wlan connection")
    np.set(0,P,0,0)
    time.sleep(0.5)
    np.set(0,0,0,0)
    time.sleep(0.5)

print("WiFi connected at", wlan.ifconfig()[0])

np.set(0,G,0,0)
time.sleep(1)
np.set(0,0,0,0)

# Sync RTC
print("inquire RTC time")
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

while not rtc.synced():
    if rtc.synced():
        break
    if not wlan.isconnected():
        print("Lost WiFi connection")
        for _ in range(10):
            np.set(0,R,0,0)
            time.sleep(0.1)
            np.set(0,0,0,0)
            time.sleep(0.1)
        sys.exit()
    print("Waiting for rtc time")
    np.set(0,Y,0,0)
    time.sleep(0.5)
    np.set(0,0,0,0)
    time.sleep(0.5)

if rtc.synced():
    print(time.strftime("%c", time.localtime()))
else:
    print("could not get NTP time")

for _ in range(4):
        np.set(0,G,0,0)
        time.sleep(0.1)
        np.set(0,0,0,0)
        time.sleep(0.1)

np.deinit()

