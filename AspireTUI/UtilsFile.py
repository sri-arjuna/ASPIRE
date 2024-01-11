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
import sys as _sys
#import re as _re
#import string as _string
from AspireTUI._MESSAGES import current as _MSG
from AspireTUI import Classes as _Classes
from AspireTUI import StringUtils as _stew
from . import tui as _tui
from typing import Union as _Union
################################################################################################################
#####                                            Basic Checks                                              #####
################################################################################################################
# FileDescriptorOrPath
def exists(filename: FileDescriptorOrPath, bVerbose=False, bDual=False):
	"""
	Returns True if filename exists, or both, bool and message.
	
	Examples:
		if _Files.file_exists(filename):
			# Do stuff
			pass
		
		ret_bool, ret_msg = _Files.file_exists(filename, bDual=True)

	"""
	ret_bool, ret_msg  = False, None
	is_file	= False
	ret_bool = _os.path.exists(filename)


	# Prepare output
	if is(filename, filesystem.reference.)
		is_file = True
	if ret_bool:
		ret_msg = _MSG.file_exists
	else:
		ret_msg = _MSG.file_not_found
	
	# Display things, if desired
	if bVerbose:
		_tui.status(ret_bool, ret_msg, _os.fspath(filename)[0])
	
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
	ret_msg = f"{_MSG.word_found}: {_MSG.word_filesystem_file}"
	# Start checking
	if exists(filename, bVerbose=bVerbose):
		if _os.path.isfile(filename):
			# Its a file
			ret_bool = True
	else:
		raise TypeError(filename)

def isdir(filename: str, bVerbose=False, bDual=False):
	"""
	Returns True if it is a direcctory.
	"""
	# Init vars
	ret_bool = False
	ret_msg = f"{_MSG.word_found}: {_MSG.word_filesystem_dir}"
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
	ret_msg = f"{_MSG.word_found}: {_MSG.word_filesystem_link}"
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
	ret_msg = f"{_MSG.word_found}: {_MSG.word_filesystem_mount}"
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
