# Home Office Lights
I have WS2812b LED strip in my home office that is controlled by a Raspberry Pi.

This repository contains the code that I use to control the lights from the Pi.

## Crontab Setup

    TZ=Europe/London 
    * * * * * sudo python3 /home/pi/home-office-lights/temp-monitor.py
    0 21 * * * sudo python3 /home/pi/home-office-lights/off.py
