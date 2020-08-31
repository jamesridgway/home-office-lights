# Home Office Lights
I have WS2812b LED strip in my home office that is controlled by a Raspberry Pi.

This repository contains the code that I use to control the lights from the Pi.

## Setup

All of the following steps should be run on the Raspberry Pi controlling the lights. This codebase assumes that the lights are running off of GPIO-18.

1. Install redis using: `sudo ./install-redis.sh`

## Crontab Setup

    TZ=Europe/London 
    * * * * * sudo python3 /home/pi/home-office-lights/temp-monitor.py
    0 21 * * * sudo python3 /home/pi/home-office-lights/off.py
