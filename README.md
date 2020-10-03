# Home Office Lights
I have [WS2812b LED strip in my home office](https://www.jamesridgway.co.uk/using-a-raspberry-pi-to-make-my-office-desk-glow/) that is controlled by a Raspberry Pi.

This repository contains the code that I use to control the lights from the Pi.

`home_office_lights.py` is designed to run as a service via systemctl. This will respond to messages on a Redis queue,
translating each message into `rpi_ws281x` commands. This has been designed this way so that the light strip can 
easily be controlled by other devices by publishing messages to the redis queue.

## Setup

All of the following steps should be run on the Raspberry Pi controlling the lights. This codebase assumes that the 
lights are running off of GPIO-18.

1. Checkout this repository to `/srv/home-office-lights`
2. Install redis using: `sudo ./install-redis.sh`
3. Install `home_office_lights.py` as a service using: `sudo ./install-office-lights.sh 192.168.1.10`. The IP address should be the IP of your Raspberry Pi.

That's it, the service (`home-office-lights.service`) is up and running and is controlled by `systemctl`.

## Issuing commands
On any machine running python3 with PyRSMQ installed you can run any of these examples:

    REDIS=192.168.1.10 python3 home_office_lights.py '{"type": "solid-colour","r": 255, "g": 64, "b": 0}'
    REDIS=192.168.1.10 python3 home_office_lights.py '{"type": "alert","r": 128, "g": 0, "b": 128}'
    REDIS=192.168.1.10 python3 home_office_lights.py '{"type": "off"}'
    REDIS=192.168.1.10 python3 home_office_lights.py '{"type": "on"}'

## Basic Scripts
The following basic scripts are designed to be run on the Raspberry Pi and execute commands via `rpi_ws281x`.

* **off.py**<br />
  Turns the light strip off
* **orange.py**<br />
  Sets the light strip to a solid orange colour
* **temp-monitor.py**<br />
  Logs out temperature readings periodically to a file assuming you have a DHT22 using GPIO pin 17 for data.

**Sample Crontab Setup**<br />
Monitor temperature every minute. Turn the lights on orange at 08:00 and turn them off at 21:00 everyday.

    TZ=Europe/London 
    * * * * * sudo python3 /home/pi/home-office-lights/temp-monitor.py
    0 8 * * * sudo python3 /home/pi/home-office-lights/orange.py
    0 21 * * * sudo python3 /home/pi/home-office-lights/off.py
