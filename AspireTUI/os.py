"""
	Description:
					Public functions for OS related values. \n
					Such as: directories
	Provides:
					from AspireTUI import ConfigUtills as cu
					ret_bool, ret_str = cu.reg_value_get(file,key,var)
					
	========================================================
	Created on:		2024 Jan. 04
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Essential imports
#
import os as _os
#import sys as _sys
#import re as _re
#import string as _string
#from pathlib import Path as _Path
import platform as _platform
from . import IS_WINDOWS
#################################################################################################################
#####                                           Get Directories                                             #####
#################################################################################################################
_dir_user = {
	"Home": "%userprofile%",
	"Config": "%localappdata%",
	"Docs": "%userprofile%",
}
_dir_os = {
	"system": "%systemroot%",
	
}
def get_dir_OS(bVerbose=True, bMinimal=False):
	"""
	Returns a dict with OS related paths.	\n
	Example:	\n
		DIR_OS = get_dir_OS()	\n
		for key, path in DIR_OS.items():	\n
			print(f"{key}: {path}")	\n
	"""
	# Init variables
	dir_os = []
	if bMinimal:
		task_list = []
	else:
		task_list = []
	# Start the job
	for task in task_list:
		if IS_WINDOWS:
			pass
		else:
			# Its a *nix based system
			# TODO
			pass
	pass

def isGUI():
	"""
	Check if the script is running in a GUI environment.
	"""
	if IS_WINDOWS:
		# Check if running in Windows console
		return _os.getenv("TERM_PROGRAM") is not None
	else:
		# Check if running in a non-Windows environment
		return _os.getenv("TERM") is None

def isVerOS(minimal=None, bDual=False):
	"""
	Checks if the OS version is at least "minimal". \n
	If nothing is provided, Win 10 or Kernel 6.x are 'expected' as current system. \n
	When criteria is met, it returns with True. \n

	Use bDual=True if you want to return a bool and a 'uname' with OS information. \n
	For Linux, version must be a one digit float like: 6.1, 5.9, 5.5
	"""
	# Init vars
	doLinux = True
	if minimal is None:
		if IS_WINDOWS:
			minimal = 10
			doLinux = False
		else:
			minimal = 6.1
	elif isinstance(minimal, int):
		doLinux = False
	# Do the check
		if doLinux:
			print("# TODO: Linux needs to be verified if kernel detection works") # TODO
			if int(_platform.release().split('.')[0]) >= str(minimal).split('.')[0]:
				if int(_platform.release().split('.')[1]) >= str(minimal).split('.')[1]:
					ret = True
				else:
					ret = False
			else:
				ret = False
		else:
			if int(_platform.release().split('.')[0]) >= minimal:
				ret = True
			else:
				ret = False
	# Return to user
	if bDual:
		return ret, _os.uname()
	else:
		return ret
