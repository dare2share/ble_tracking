#!/usr/bin/env python

import beaconscanner as bs
import beaconlogger as bl
import argparse
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
"""
print("TEST #2 (beacon logger)")
myBeaconLogger = bl.BeaconLogger("/home/pi/data/", station_ID = "myStationID", scan_duration = 3, log_config = bl.bs.bd.BD_LOG_CONFIG_DEFAULT)
myBeaconLogger.run()
"""
####################

parser = argparse.ArgumentParser()
parser.add_argument("stationID", help = "unique name of the sharing station")
parser.add_argument("-d", "--scanDuration", help = "scan duration in seconds", nargs = 1, type = int, default = [3])
args = parser.parse_args()
stationID = args.stationID
scanDuration = args.scanDuration[0]
print("Initiating tracking as station \"" + stationID + "\" with scan duration " + str(scanDuration) + "s")

beaconLogger = bl.BeaconLogger("data/", station_ID = stationID, scan_duration = scanDuration, log_config = bl.bs.bd.BD_LOG_CONFIG_DEFAULT)
beaconLogger.run()

####################

print("")
