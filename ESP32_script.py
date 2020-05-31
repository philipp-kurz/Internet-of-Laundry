from mqttclient import MQTTClient
from machine import Pin, ADC, Neopixel
from board import ADC5
import time
import network

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

# Set up ADC for ACS712 sensor
acs712 = ADC(Pin(ADC5))
acs712.atten(ADC.ATTN_11DB)

# Capture start time
startTime = round(time.time())

# Check network connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    for _ in range(10):
        np.set(0,R,0,0)
        time.sleep(0.1)
        np.set(0,0,0,0)
        time.sleep(0.1)

    sys.exit()
else:
    print("connected to WiFi at IP", ip)


# Connect to MQTT broker
BROKER = "internetoflaundry.xyz"
topic = "data"
print("Connecting to MQTT broker", BROKER, "...", end="")
try:
    mqtt = MQTTClient(BROKER)
except:
    print("Could not connect to MQTT")
    for _ in range(10):
        np.set(0,Y,0,0)
        time.sleep(0.1)
        np.set(0,0,0,0)
        time.sleep(0.1)
print("Connected!")

# Start running
while True:
    min = 10000
    max = 0
    measurements = 3000

    # Capture data
    for _ in range(measurements):
        voltage = acs712.read()
        if voltage > max:
            max = voltage
        if voltage < min:
            min = voltage


    milliAmps = round((max - min) * 1000 * 0.707 / 2 / 66) - 2000
    if milliAmps < 0:
        milliAmps = 0
    
    # Send data
    data = "{} {}".format(round(time.time()), milliAmps)
    print("send topic='{}' data='{}'".format(topic, data))
    try:
        mqtt.publish(topic, data)
    except:
        print("Failed to publish MQTT")
        for _ in range(10):
            np.set(0,P,0,0)
            time.sleep(0.1)
            np.set(0,0,0,0)
            time.sleep(0.1)

    # Wait
    for i in range (0,25):
        np.set(0, 2 * i, 0, 0)
        time.sleep(0.03)
    for i in range (26,100):
        np.set(0, 2 * i, 0, 0)
        time.sleep(0.0033)
    np.set(0,0,0,0)

mqtt.disconnect()
acs712.deinit()

























