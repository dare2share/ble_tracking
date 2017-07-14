#!/usr/bin/env python

import os
import datetime
import json
import beaconscanner as bs

# Constant Definitions
BL_RUN_DURATION_INFINITE = -1
SECONDS_PER_DAY = 24 * 60 * 60


class BeaconLogger(bs.BeaconScanner, object):
	"""
	This class provides all functionalities to automatically log the
	advertising data of nearby iBeacons. The data received is saved to
	a JSON file.
	This class is derived from the BeaconScanner class to have access
	to BLE scanning.
	"""

	def __init__(self, data_folder_path,
			station_ID = "undefined_station",
			scan_duration = 10.0,
			log_config = bs.bd.BD_LOG_CONFIG_DEFAULT):
		"""
		Initializes the base class and sets logging configuration and
		metadata.

		@param	data_folder_path:	the (relative) folder (not file!) path
									where the logging data is saved to
		@param	station_ID:			the identifier name of the logging station
		@param	scan_duration:		the time period each scan lasts (in seconds)
		@param	log_config:			the log configuration bit array, for details
									see documentation of the BeaconScanner class
		"""
		bs.BeaconScanner.__init__(self, log_config)
		self.set_station_ID(station_ID)
		self.set_scan_duration(scan_duration)
		self.set_log_config(log_config)

		self.update_time()
		self.data_folder_path = data_folder_path
		self.data_is_saved = False

	def set_station_ID(self, station_ID):
		"""
		Sets the station's identifier name

		@param	station_ID:	the identifier name
		"""
		self.station_ID = station_ID

	def set_scan_duration(self, scan_duration):
		"""
		Sets the time period each scan lasts. The longer this time is set, the less
		beacons will be overlooked. However, a long scan time reduces temporal resolution.

		@param	scan_duration:	the scan duration in seconds
		"""
		self.scan_duration = scan_duration

	def update_time(self):
		"""
		Updates the member time variable to the current system time.
		"""
		self.time = datetime.datetime.now()

	def get_timestamp(self, mode = "s"):
		"""
		Gets the string format of the member time variable. Depending on the specified mode,
		the time precision returned will be different.

		@param	mode:	the mode specifying the return format
		@return:		mode = "s": YYYY-MM-DD--HH-MM-SS
						mode = "m": YYYY-MM-DD--HH-MM
						mode = "h": YYYY-MM-DD-HHh
		"""
		if mode == "s":
			return "{:%Y-%m-%d--%H-%M-%S}".format(self.time)
		elif mode == "m":
			return "{:%Y-%m-%d--%H-%M}".format(self.time)
		elif mode == "h":
			return "{:%Y-%m-%d-%Hh}".format(self.time)
		else:
			print("Timestamp mode error")
			return "{:%Y-%m-%d}".format(self.time)

	def get_file_path(self):
		"""
		Assembles and returns the current log file path.
		It has the format <log folder>/d2s.data.<stationID>.<time>.json.

		@return:	the log file path
		"""
		return self.data_folder_path + "d2s.data." + self.station_ID + "." + self.get_timestamp("h") + ".json"

	def open_file(self):
		"""
		Creates the log folder and log files (if applicable) and opens the log file. If the file is newly creates,
		a header will be written.

		@return:	returns true upon file opening success
		"""
		write_header = False
		
		# check for directory/file existence
		if not os.path.exists(self.data_folder_path):
			os.makedirs(self.data_folder_path)
		if os.path.exists(self.get_file_path()):
			file = open(self.get_file_path(), "r")
			if json.loads(file.readline())["log_config"] != self.log_config:
				write_header = True
			file.close()
		else:
			write_header = True
		
		# open and prepare log file
		self.file = open(self.get_file_path(), "a")
		if write_header:
			self.file.write(json.dumps({"log_config": self.log_config}) + "\n")

		return True

	def close_file(self):
		"""
		Closes the log file.

		@return:	returns true
		"""
		self.file.close()
		return True

	def write_data_to_file(self):
		"""
		Iterates the beacon data list (scan results) and writes a list of timestamp and
		log data (as specified by the log configuration) into a JSON file.

		@return:	returns true if writing process was successful
		"""
		if self.data_is_saved:
			print("Data has been written to file already")
			return False
		
		self.open_file()
		for dat in self.beacon_data:
			write_string = json.dumps([self.get_timestamp("s")] + dat.get_log_list()) + "\n"
			self.file.write(write_string)
		self.close_file()

		self.data_is_saved = True
		return True

	def scan(self):
		"""
		Performs the BLE scan process.
		"""
		super(BeaconLogger, self).scan(self.scan_duration)
		self.data_is_saved = False

	def run(self, run_duration = BL_RUN_DURATION_INFINITE):
		"""
		Starts a loop which repeatedly scans for iBeacon advertising data and saves
		the scan results to the file. This process lasts a specified duration.

		@param	run_duration:	the total duration of the monitoring process in seconds
								if set to -1, this process will not stop
		"""
		run_duration_days = run_duration // SECONDS_PER_DAY
		run_duration_seconds = run_duration % SECONDS_PER_DAY
		self.update_time()
		run_time_end = self.time + datetime.timedelta(run_duration_days, run_duration_seconds)

		# TODO: launch loop in thread
		while run_duration == BL_RUN_DURATION_INFINITE or self.time < run_time_end:
			self.scan()
			if not self.write_data_to_file():
				print("Error writing to file")
			self.update_time()
			
