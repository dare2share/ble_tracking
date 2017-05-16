# dare2share - Tracking Software

This repository contains software which enables Bluetooth Low Energy tracking of umbrellas provided by the project [dare2share](jungeakademie.tum.de/dare2share) to demonstrate the potential of sharing economy on campus.

This project is part of the scholarship programme [TUM: Junge Akademie](jungeakademie.tum.de) of the [Technical University of Munich](tum.de).


## Dependencies

This code is written in Python 2.7 and depends on the Linux Bluetooth stack BlueZ as it is expected to run on a Raspberry Pi Zero. The python interface used to access Bluetooth Low Energy is [bluepy](github.com/IanHarvey/bluepy).

To install the required libraries run the following commands:
```sh
sudo apt-get install python-pip libglib2.0-dev
sudo pip install bluepy
```


## Application

As this application requires access to the Bluetooth interface, it has to be started with root privileges. The main python file is located at `src/ble_tracking.py`. Assuming the working directory to be this repository's root directory, the application can be run with:
```sh
cd src
sudo python3 ./ble_tracking.py
```
