#!/bin/bash
set -e
cd "$(dirname "$0")"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

echo "Creating temp directory"
mkdir -p /tmp/redis-download

echo "Downloading redis-stable.tar.gz"
wget http://download.redis.io/redis-stable.tar.gz -O /tmp/redis-download/redis-stable.tar.gz >/dev/null 2>&1

echo "Extracting redis-stable.tar.gz"
tar xzf /tmp/redis-download/redis-stable.tar.gz -C /tmp/redis-download

echo "Running make"
( cd /tmp/redis-download/redis-stable && sudo make)

echo "Make install"
( cd /tmp/redis-download/redis-stable && sudo make install PREFIX=/usr)
sudo mkdir /etc/redis
sudo cp ./redis/redis.conf /etc/redis/

echo "Create redis user"
sudo adduser --system --group --disabled-login redis --no-create-home --shell /bin/nologin --quiet

echo "Service config"
sudo mkdir -p /var/run/redis
sudo chown -R redis /var/run/redis
cp ./redis/redis-server /etc/init.d/redis-server
sudo chmod +x /etc/init.d/redis-server
sudo update-rc.d redis-server defaults

echo "Restart service"
sudo service redis-server restart

echo "Redis version"
redis-server -v

echo "Done!"
