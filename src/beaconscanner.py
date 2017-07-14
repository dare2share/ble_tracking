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

	def __init__(self, log_config = bd.BD_LOG_CONFIG_DEFAULT):
		"""
		Initializes the base class and defines BeaconScannerDelegate as
		bluepy delegate class.
		"""
		ble.Scanner.__init__(self)
		self.withDelegate(BeaconScannerDelegate())
		self.set_log_config(log_config)

	def set_log_config(self, log_config):
		"""
		Sets the bit array which defines which data items are saved to file
		(True == 1 == save, False == 0 == do not save).
		The bit field is defined as follows:
		| name | MAC address | RSSI | manufacturer ID | subtype |
		| subtype length | proximity UUID | major | minor | signal power |

		@param	log_config:	the bit string specifying the log configuration
							e.g. "0b1010000000" logs only name and RSSI
		"""
		self.log_config = log_config		

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
						self.beacon_data[-1].set_name(name)
				
				# get iBeacon data of device
				if (adtype == bd.BD_TYPE_CUSTOM):
					beacon_data_item_generated = True
					
					self.beacon_data.append(bd.BeaconData(name, self.log_config))
					if self.beacon_data[-1].set_data(value, use_uuid_filter = True):
						self.beacon_data[-1].set_device(dev.addr, dev.rssi)
					else:
						self.beacon_data.pop()
						beacon_data_item_generated = False

		return devices

	def getBeaconData(self):
		"""
		Gets the list of discovered devices sending iBeacon advertising data.

		@return:	the list of BeaconData objects discovered during last scan
		"""
		return self.beacon_data
