import os
import sys

import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 17

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    write_header = not os.path.exists("temp-data.csv")
    with open("temp-data.csv", "a+") as f:
        if write_header:
            f.write("Temperature (C), Humidity (%)\n")
        f.write("{0:0.1f},{1:0.1f}\n".format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
