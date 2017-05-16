#!/usr/bin/env python

import bluepy.btle as ble
import beacondata as bd


class BeaconScannerDelegate(ble.DefaultDelegate, object):
	"""
	This class defines how BLE device discoveries by BeaconScanner are
	handled. Currently there is only a print output indicating that a
	device was found.
	This class is derived from the bluepy.btle.DefaultDelegate class.
	"""

	def __init__(self):
		"""
		Initializes the base class.
		"""
		ble.DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		"""
		Defines the behaviour when a signal from a BLE device was received.
		Prints a note whenever a new device was found or new data was received.

		@param	dev:		the bluepy device
		@param	isNewDev:	boolean value whether this discovery is a new one
		@param	isNewData:	boolean value whether this signal is new data
		"""
		if isNewDev:
			print("Discovered device: " + dev.addr)
		elif isNewData:
			print("Received new data from: " + dev.addr)


class BeaconScanner(ble.Scanner, object):
	"""
	This class provides the capabilities to scan for Bluetooth Low Energy
	devices.
	This class is derived from the bluepy.btle.Scanner class.
	"""

	def __init__(self):
		"""
		Initializes the base class and defines BeaconScannerDelegate as
		bluepy delegate class.
		"""
		ble.Scanner.__init__(self)
		self.withDelegate(BeaconScannerDelegate())

	def scan(self, timeout = 10.0):
		"""
		Scans for Bluetooth Low Energy devices for a given period of time.
		Combines the received data and matches the BLE custom data according
		to the iBeacon specifications. Overwrites previous scan results.

		@param	timeout:	the scan time period in seconds
		@return:			the list of discovered bluepy devices
		"""
		self.beacon_data = []

		# actual BLE scan
		devices = super(BeaconScanner, self).scan(timeout)

		# iterate discovered bluepy devices
		for dev in devices:
			name = "unknown device"
			beacon_data_item_generated = False

			# iterate scanned data corresponding to a bluepy device
			for (adtype, description, value) in dev.getScanData():

				# get name of device
				if (adtype == bd.BD_TYPE_NAME):
					name = value
					if beacon_data_item_generated:
						self.beacon_data[-1].setName(name)
				
				# get iBeacon data of device
				if (adtype == bd.BD_TYPE_CUSTOM):
					beacon_data_item_generated = True
					
					self.beacon_data.append(bd.BeaconData(name))
					if self.beacon_data[-1].setData(value):
						self.beacon_data[-1].setDevice(dev.addr, dev.rssi)
					else:
						self.beacon_data.pop()

		return devices

	def getBeaconData(self):
		"""
		Gets the list of discovered devices sending iBeacon advertising data.

		@return:	the list of BeaconData objects discovered during last scan
		"""
		return self.beacon_data
