"""
	Description:
			Contains access to hardware information
	Usage:
			from AspireTUI import hw as _hw

	========================================================
	Created on:		2024 Jan. 08
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Self Sustain
#
from AspireTUI import IS_WINDOWS

#
#	Imports
#
import os as _os
import string as _string

#
#	Functions
#
def drive_letters() -> list:
	"""
	List available drives letters on Windows (C, D... Z) or /dev/[sh]d* devices on Unix-like systems.

	Returns:
		list: A list of drive letters (Windows) or device paths (Unix).
	"""
	# Init
	drives = []

	if IS_WINDOWS:
		for drive in _string.ascii_uppercase:
			if _os.path.exists(drive):
				drives.append(drive)
	else:
		# *nix-style systems, like iOS, BSD, Linux
		dev_dir = "/dev"
		for device in _os.listdir(dev_dir):
			if device.startswith("hd", "sd"):
				drives.append(device)
	
	# Return to user
	return drives
