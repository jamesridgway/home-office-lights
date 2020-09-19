#!/bin/bash
set -e
cd "$(dirname "$0")"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

echo "Service config"
cp ./home-office-lights/home-office-lights.service /lib/systemd/system/home-office-lights.service

echo "Restart service"
sudo systemctl daemon-reload
sudo systemctl enable home-office-lights.service
sudo systemctl restart home-office-lights.service

echo "Status"
sudo systemctl status home-office-lights.service

echo "Done!"
