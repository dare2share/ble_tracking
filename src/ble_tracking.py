#!/usr/bin/env python

import beaconscanner as bs
import beaconlogger as bl
import dare2share_header as d2sh

d2sh.printHeader()

####################
"""
print("TEST #1 (iBeacon scan and info printing)")
myBeaconScanner = bs.BeaconScanner()
myDevices = myBeaconScanner.scan(2.0)
myBeaconData = myBeaconScanner.getBeaconData()
for bd_item in myBeaconData:
	print("")
	print(bd_item)
"""
####################

print("TEST #2 (beacon logger)")
myBeaconLogger = bl.BeaconLogger("data/", station_ID = "myStationID", scan_duration = 3, log_config = bl.bs.bd.BD_LOG_CONFIG_DEFAULT)
myBeaconLogger.run(20)

####################

print("")
