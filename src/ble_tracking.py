#!/usr/bin/env python

import beacondata as bd
import beaconscanner as bs
import dare2share_header as d2sh

d2sh.printHeader()

####################

print("TEST #1 (iBeacon scan and info printing)")
myBeaconScanner = bs.BeaconScanner()
myDevices = myBeaconScanner.scan(2.0)
myBeaconData = myBeaconScanner.getBeaconData()
for bd_item in myBeaconData:
	print("")
	print(bd_item)

####################

print("")
