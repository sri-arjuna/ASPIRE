"""
	Description:
					Public functions to easy several tasks with Files
	Provides:
					import AspireTUI.UtilsFile as UF
					ret_bool, ret_str = cu.reg_value_get(file,key,var)
					
	========================================================
	Created on:		2024 Jan. 01
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
from AspireTUI import _MSG
#from . import Classes as _Classes
#from . import strings as _stew
from AspireTUI import tui as _tui
#from typing import Union as _Union
################################################################################################################
#####                                            Basic Checks                                              #####
################################################################################################################
# FileDescriptorOrPath
def exists(filename: str, bVerbose=False, bDual=False):
	"""
	Returns True if filename exists, or both, bool and message.
	
	Examples:
		if _Files.file_exists(filename):
			# Do stuff
			pass
		
		ret_bool, ret_msg = _Files.file_exists(filename, bDual=True)

	"""
	ret_bool = None
	ret_bool = _os.path.exists(filename)
	fn = _os.path.basename(filename)
	ret_msg = f"{_MSG.word_found} {_MSG.word_filesystem_file}: {fn}"

	if ret_bool:
		ret_msg = _MSG.file_exists
	else:
		ret_msg = _MSG.file_not_found
	# Display things, if desired
	if bVerbose:
		_tui.status(ret_bool, ret_msg)
	# Return 
	if bDual:
		return ret_bool, ret_msg
	else:
		return ret_bool

def isfile(filename: str, bVerbose=False, bDual=False):
	"""
	Returns True if it is a file.
	"""
	# Init vars
	ret_bool = False
	fn = _os.path.basename(filename)
	ret_msg = f"{_MSG.word_found} {_MSG.word_filesystem_file}: {fn}"
	# Start checking
	if exists(filename, bVerbose=bVerbose):
		if _os.path.isfile(filename):
			# Its a file
			ret_bool = True
	else:
		raise TypeError(filename)
	# Display things, if desired
	if bVerbose:
		_tui.status(ret_bool, ret_msg, fn)
	# Return 
	if bDual:
		return ret_bool, ret_msg
	else:
		return ret_bool

def isdir(filename: str, bVerbose=False, bDual=False):
	"""
	Returns True if it is a direcctory.
	"""
	# Init vars
	ret_bool = False
	fn = _os.path.basename(filename)
	ret_msg = f"{_MSG.word_found} {_MSG.word_filesystem_dir}: {fn}"
	# Start checking
	if exists(filename, bVerbose=bVerbose):
		if _os.path.isdir(filename):
			# Its a dir
			ret_bool = True
	else:
		raise TypeError(filename)
	# is Verbose?
	if bVerbose:
		_tui.status(ret_bool, ret_msg)
	# Return
	if bDual:
		return ret_bool, ret_msg
	else:
		return ret_bool

def islink(filename: str, bVerbose=False, bDual=False):
	"""
	Returns True if it is a link.
	"""
	# Init vars
	ret_bool = False
	fn = _os.path.basename(filename)
	ret_msg = f"{_MSG.word_found} {_MSG.word_filesystem_link}: {fn}"
	# Start checking
	if exists(filename, bVerbose=bVerbose):
		if _os.path.islink(filename):
			# Its a dir
			ret_bool = True
	else:
		raise TypeError(filename)
	# is Verbose?
	if bVerbose:
		_tui.status(ret_bool, ret_msg)
	# Return
	if bDual:
		return ret_bool, ret_msg
	else:
		return ret_bool

def ismount(filename: str, bVerbose=False, bDual=False):
	"""
	Returns True if it is a direcctory.
	"""
	# Init vars
	ret_bool = False
	fn = _os.path.basename(filename)
	ret_msg = f"{_MSG.word_found} {_MSG.word_filesystem_mount}: {fn}"
	# Start checking
	if exists(filename, bVerbose=bVerbose):
		if _os.path.ismount(filename):
			# Its a dir
			ret_bool = True
	else:
		raise TypeError(filename)
	# is Verbose?
	if bVerbose:
		_tui.status(ret_bool, ret_msg)
	# Return
	if bDual:
		return ret_bool, ret_msg
	else:
		return ret_bool

def is_file_in_use(filename: str):
	"""
	Returns True if file is in use.
	"""
	try:
		with open(filename, 'r') as file:
			pass
		# File is not in use
		return False
	except PermissionError:	# OSError in Python 3.3 and later
		# File is in use
		return True
