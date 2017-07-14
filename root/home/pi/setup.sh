echo run as root
cp /home/pi/ble_tracking/root/lib/systemd/system/$1.ble_tracking.service /lib/systemd/system/
systemctl enable $1.ble_tracking.service
