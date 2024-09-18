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
import sys as _sys
#import re as _re
#import string as _string
#from pathlib import Path as _Path
import platform as _platform
from . import IS_WINDOWS
from . import _MSG
#
#	Constants / Vars
#
OS_INFO = _platform.uname()
#################################################################################################################
#####                                           Get Directories                                             #####
#################################################################################################################
_dir_user = {
	"Home": "%userprofile%",
	"Config": "%localappdata%",
	"Docs": "%userprofile%/Documents",
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

def _isGUI():
	"""
	Check if the script is running in a GUI environment.
	"""
	if IS_WINDOWS:
		# Check if running in Windows console
		#return _os.getenv("TERM_PROGRAM") is not None 	# Maybe later useful
		return _os.name == 'nt'
	else:
		# Check if running in a non-Windows environment
		return any(_os.getenv(var) for var in ["XDG_CURRENT_DESKTOP", "DESKTOP_SESSION", "XAUTHORITY", "TERM"]) is not None

# Assign the function to variable (as this wont change during runtime)
IS_GUI = _isGUI()

def isVerOS(minimal=None, bDual=False):
	"""
	Checks if the OS version is at least "minimal". \n
	If nothing is provided, Win 10 or Kernel 6.x are 'expected' as current system. \n
	When criteria is met, it returns with True. \n

	Use bDual=True if you want to return a bool and a 'uname' with OS information. \n
	For Linux, version must be a one digit float like: 6.1, 5.9, 5.5
	"""
	# Init vars
	global OS_INFO
	doLinux = True
	ret = False
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
			print("# DEBUG TODO: Linux needs to be verified if kernel detection works") # TODO
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
		msg = [
			OS_INFO.system ,
			OS_INFO.release ,
			OS_INFO.version,
			OS_INFO.machine ,
			OS_INFO.processor ,
		]
		return ret, msg
	else:
		return ret

def isVerPy(minimal: float = 3.9, bDual=False):
	"""
	Checks if the Python version is at least "minimal". \n
	If no "minimal" is provided, at least 3.9 is expected.
	"""
	# init
	ret = False
	msg = _MSG.os_not_found_python

	# Check for proper format:
	if not isinstance(minimal, float):
		# Is not just Major.Minor
		raise ValueError(_MSG.cl_log_err_must_float, minimal)
	
	# Prepare for version check
	maj, min = 0, 0
	maj = int(str(minimal).split(".")[0])
	min = int(str(minimal).split(".")[1])
	if _sys.version_info[:2] >= (maj, min):
		# All good
		ret = True
		msg = _sys.version_info[:2]
	# Return to user
	if bDual:
		return ret, msg
	else:
		return ret


def file_lock_on(filename, bVerbose: bool=False):
	"""
	Enable OS wide file lock, cross platform (Unix-likes & Windows)
	
	Must be called after you: `with open(filename, mode, encoding) as file:`
	"""
	# Verify a filename was passed
	if not filename: print("No file-handle passed to OS.file_lock_on") ; return False

	# Lets make messages nice
	import tui as _tui
	ret_bool = False
	size = 0
	
	# Import according to OS
	if IS_WINDOWS:	import msvcrt  ; size = _os.path.getsize(filename)
	else:			import fcntl

	#
	# Try locking file
	#
	try:
		if IS_WINDOWS: 	msvcrt.locking(filename.fileno(), 	msvcrt.LK_LOCK, size)
		else: 			fcntl.flock(filename.fileno(), 		fcntl.LOCK_EX)
		
		# Has not failed yet, lets say it succeeded
		ret_bool = True
	
	# Handle possible exceptions
	except FileNotFoundError:	ret_err_msg = f"Error: File ({filename}) not found."
	except PermissionError:		ret_err_msg = "Error: Permission denied."
	except OSError:				ret_err_msg = "Error: File is corrupted or other OS-related issue."
	except Exception as e:		ret_err_msg = f"Unexpected error: {str(e)}"

	#
	#	Lets handle messaging
	#
	if not ret_bool:
		# It failed, be verbose
		_tui.status(_tui.STATUS.ERROR.value, ret_err_msg)
	elif bVerbose:
		# Success and verbose
		msg_locked = "Locked:"
		_tui.status(ret_bool, msg_locked, filename)
	
	# return to user
	return ret_bool

def file_lock_off(filename, bVerbose: bool=False):
	"""
	Disables the OS wide file lock, cross platform (Unix-likes & Windows)
	
	Must be called after you: `with open(filename, mode, encoding) as file:` ; OS.file_lock_on(file)
	"""
	# Verify a filename was passed
	if not filename: print("No file-handle passed to OS.file_lock_on") ; return False

	# Lets make messages nice
	import tui as _tui
	ret_bool = False
	size = 0

	# Import according to OS
	if IS_WINDOWS:	import msvcrt  ; size = _os.path.getsize(filename)
	else:			import fcntl

	#
	# Try locking file
	#
	try:
		if IS_WINDOWS: 	msvcrt.locking(filename.fileno(), 	msvcrt.LK_UNLCK, size)
		else: 			fcntl.flock(filename.fileno(), 		fcntl.LOCK_UN)
		
		# Has not failed yet, lets say it succeeded
		ret_bool = True

	# Handle possible exceptions
	except FileNotFoundError:	ret_err_msg = f"Error: File ({filename}) not found."
	except PermissionError:		ret_err_msg = "Error: Permission denied."
	except OSError:				ret_err_msg = "Error: File is corrupted or other OS-related issue."
	except Exception as e:		ret_err_msg = f"Unexpected error: {str(e)}"

	#
	#	Lets handle messaging
	#
	if not ret_bool:
		# It failed, be verbose
		_tui.status(_tui.STATUS.ERROR.value, ret_err_msg)
	elif bVerbose:
		# Success and verbose
		msg_unlocked = "Unlocked:"
		_tui.status(ret_bool, msg_unlocked, filename)
	
	# return to user
	return ret_bool
