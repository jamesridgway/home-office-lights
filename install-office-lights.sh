#!/bin/bash
set -e
cd "$(dirname "$0")"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

echo "Service config"
sudo mkdir -p /var/run/redis
sudo chown -R redis /var/run/redis
cp ./home-office-lights/home-office-lights /etc/init.d/home-office-lights
sudo chmod +x /etc/init.d/home-office-lights
sudo update-rc.d home-office-lights defaults

echo "Restart service"
sudo service home-office-lights restart

echo "Done!"
