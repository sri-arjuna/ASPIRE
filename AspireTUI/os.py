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
from AspireTUI import IS_WINDOWS as _IS_WINDOWS
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
		if _IS_WINDOWS:
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
	if _IS_WINDOWS:
		# Check if running in Windows console
		return _os.getenv("TERM_PROGRAM") is not None
	else:
		# Check if running in a non-Windows environment
		return _os.getenv("TERM") is None
