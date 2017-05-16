#!/usr/bin/env python

import codecs
import bitstring

# Bluetooth Low Energy Specification
BLE_LENGTH = 0x02						# 1 byte [0]
BLE_TYPE_FLAGS = 0x01					# 1 byte [1]
BLE_VALUE_TYPICAL_FLAGS = 0x06			# 1 byte [2]

# iBeacon Specification by Apple
BD_LENGTH = 0x1a						# 1 byte [3]
BD_TYPE_NAME = 0x09						# 1 byte [4]
BD_TYPE_CUSTOM = 0xff					# 1 byte [4]
BD_MANUFACTURER_ID_APPLE = 0x4c00		# 2 bytes [5-6]
BD_SUBTYPE_IBEACON = 0x02				# 1 byte [7]
BD_SUBTYPE_LENGTH = 0x15				# 1 byte [8]
BD_PROXIMITY_UUID = b'0000000000000000'	# 16 bytes [9-24]
BD_MAJOR = 0x00							# 2 bytes [25-26]
BD_MINOR = 0x00							# 2 bytes [27-28]
BD_SIGNAL_POWER = 0x00					# 1 byte [29]

# Device Specific Data
DEV_MAC_ADDRESS = u'00:00:00:00:00:00'	# given or random MAC address
DEV_RSSI = 0							# receive signal strength indicator in dB

# Class Settings
BD_LOG_CONFIG_DEFAULT = "0b1110001111"


class BeaconData(object):
	"""
	This class provides a data structure to store iBeacon data.
	"""

	def __init__(self, name = "Undefined beacon data", log_config = BD_LOG_CONFIG_DEFAULT):
		"""
		Null-initializes its member variables.

		@param	name:		an identifier name specifying this particular beacon data
		@param	log_config:	bit string specifying which data should be saved to file, bit field:
							| name | MAC address | RSSI | manufacturer ID | subtype |
							| subtype length | proximity UUID | major | minor | signal power |
		"""
		self.name = name
		self.manufacturer_ID = 0x0000
		self.subtype = 0x00
		self.subtype_length = 0x00
		self.proximity_UUID = BD_PROXIMITY_UUID
		self.major = BD_MAJOR
		self.minor = BD_MINOR
		self.signal_power = BD_SIGNAL_POWER

		self.mac = DEV_MAC_ADDRESS
		self.rssi = DEV_RSSI

		self.log_config = bitstring.BitArray(log_config)

	def __str__(self):
		"""
		The string output overload prints the identifier name and appends its member
		variable descriptions and values with indent.

		@return:	the string output to be printed
		"""
		ret = self.name + "\n"
		ret += "  > MAC address: " + self.mac + "\n"
		ret += "  > RSSI: " + str(self.rssi) + " dB\n"
		ret += "  > manufacturer ID: " + hex(self.manufacturer_ID) + "\n"
		ret += "  > subtype: " + hex(self.subtype) + "\n"
		ret += "  > subtype length: " + hex(self.subtype_length) + "\n"
		ret += "  > proximity UUID: 0x" + self.proximity_UUID.encode("hex") + "\n"
		ret += "  > major: " + hex(self.major) + "\n"
		ret += "  > minor: " + hex(self.minor) + "\n"
		ret += "  > signal power: " + hex(self.signal_power)
		return ret

	def set_name(self, new_name):
		"""
		Sets the identifier name.

		@param	new_name:	the new identifier name
		"""
		self.name = new_name

	def set_log_config(self, log_config):
		"""
		Sets the bit array which defines which data items are saved to file (True == 1 == save,
		False == 0 == do not save). The bit field is defined as follows:
		| name | MAC address | RSSI | manufacturer ID | subtype |
		| subtype length | proximity UUID | major | minor | signal power |

		@param	log_config:	the bit string specifying the log configuration
							e.g. "0b1010000000" logs only name and RSSI
		"""
		self.log_config = bitstring.BitArray(log_config)

	def set_device(self, mac, rssi):
		"""
		Sets device specific data.

		@param	mac		the corresponding (unicode) MAC address
		@param	rssi	the received signal strength indicator in dB
		"""
		self.mac = mac
		self.rssi = rssi

	def set_data(self, new_data, check_if_beacon = True):
		"""
		Converts a (unicode) byte array of the 30-byte beacon data into the iBeacon
		structure specified by Apple. This data is then stored in the internal member
		variables.

		@param	new_data:			the (unicode) byte array of beacon data to be saved
		@param	check_if_beacon:	a boolean flag whether the passed data should be
									checked if the specifications are met
		@return:					returns whether data conversion was successful,
									always returns true if check_if_beacon is set to False
		"""
		ret = True

		byte_data = new_data.encode("ascii", errors = "backslashreplace").decode("hex")
		if check_if_beacon and len(byte_data) != 25:
			print(self.name + ": data size does not correspond to iBeacon specification")
			ret = False
			return ret

		self.manufacturer_ID = int(codecs.encode(byte_data[0:2], "hex"), 16)
		self.subtype = int(codecs.encode(byte_data[2:3], "hex"), 16)
		self.subtype_length = int(codecs.encode(byte_data[3:4], "hex"), 16)
		self.proximity_UUID = codecs.encode(byte_data[4:20], "hex")
		self.major = int(codecs.encode(byte_data[20:22], "hex"), 16)
		self.minor = int(codecs.encode(byte_data[22:24], "hex"), 16)
		self.signal_power = int(codecs.encode(byte_data[24:25], "hex"), 16)

		if check_if_beacon:
			if self.subtype != BD_SUBTYPE_IBEACON or self.subtype_length != BD_SUBTYPE_LENGTH:
				print(self.name + ": data content does not correspond to iBeacon specification")
				ret = False

		return ret

	def get_log_list(self):
		"""
		Gets a list of values which should be logged. The choice of values is defined by the
		log configuration bit array set with set_log_config().

		@return:	the log list
		"""
		ret = []
		if self.log_config[0]: ret.append(self.name)
		if self.log_config[1]: ret.append(self.mac)
		if self.log_config[2]: ret.append(self.rssi)
		if self.log_config[3]: ret.append(self.manufacturer_ID)
		if self.log_config[4]: ret.append(self.subtype)
		if self.log_config[5]: ret.append(self.subtype_length)
		if self.log_config[6]: ret.append(self.proximity_UUID)
		if self.log_config[7]: ret.append(self.major)
		if self.log_config[8]: ret.append(self.minor)
		if self.log_config[9]: ret.append(self.signal_power)
		return ret
