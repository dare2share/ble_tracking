# dare2share - Tracking Software

This repository contains software which enables Bluetooth Low Energy tracking of umbrellas provided by the project [dare2share](https://www.jungeakademie.tum.de/dare2share) to demonstrate the potential of sharing economy on campus.

This project is part of the scholarship programme [TUM: Junge Akademie](https://www.jungeakademie.tum.de) of the [Technical University of Munich](https://www.tum.de). This projected is supported by the [TUM Universitatsstiftung](https://www.tum-universitaetsstiftung.de).


## Dependencies

This code is written in Python 2.7 and depends on the Linux Bluetooth stack BlueZ as it is expected to run on a Raspberry Pi Zero. The python interface used to access Bluetooth Low Energy is [bluepy](https://www.github.com/IanHarvey/bluepy).

To install the required libraries run the following commands:
```sh
sudo apt-get install python-pip libglib2.0-dev
sudo pip install bluepy
```


## Application

As this application requires access to the Bluetooth interface, it has to be started with root privileges. The main python file is located at `src/ble_tracking.py`. Assuming the working directory to be this repository's root directory, the application can be run with:
```sh
cd src
sudo python ./ble_tracking.py
```


## Affiliation

![dare2share - Junge Akademie - Universitatsstiftung - Technical University of Munich](https://rawgit.com/dare2share/ble_tracking/master/doc/affiliation_logos.svg)
