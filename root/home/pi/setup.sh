#setup script for raspberry
#(hopefully) idempotent with same parameters
echo run as root
echo Example usage: "bash setup.sh ch", get abbreviations from pi_to_port

#copy correct service file
cp /home/pi/ble_tracking/root/lib/systemd/system/$1.ble_tracking.service /lib/systemd/system/
systemctl enable $1.ble_tracking.service
systemctl start $1.ble_tracking.service

#get correct port from mapping file
port=$(grep -Po "(?<=^$1 ).*" /home/pi/ble_tracking/root/home/pi/pi_to_port)

#write script for ssh-tunneling
cat > /usr/bin/ssh-tunneling << EOL
#!/bin/sh
autossh -M 20000 -f -N di36him@webdev-tum.lrz.de -R $port:localhost:22 -C
EOL

#file for recognizing which host this is
touch ~/$1
