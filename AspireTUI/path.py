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
import pathlib as _pathlib
#import sys as _sys
import re as _re
#import string as _string
from . import _MSG
#from . import Classes as _Classes
#from . import strings as _stew
from . import tui as _tui
from typing import Union as _Union
import glob as _glob
################################################################################################################
#####                                            Basic Checks                                              #####
################################################################################################################
def dir_cur():
	"""
	Returns the absolute current working directory
	"""
	return _os.path.abspath(_os.getcwd())

def dir_app():
	"""
	Returns the absolute path of the app that is running / calling this function.
	"""
	if hasattr(__file__, 'read'):
		# We're in an interactive session
		return _os.path.abspath(_os.getcwd())
	else:
		return _pathlib.Path(_os.path.abspath(__file__)).parent

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

def list_content(location: str=None, 
				root: str=None, 
				EXTENSION: _Union[list, str]=None, 
				FILTER: _Union[list, str, _re.Pattern]=None, 
				HIDE: _Union[list, str, _re.Pattern]=None, 
				bDual: bool=False, 
				bRecursive=False
			):
	"""
	Returns a pre-sorted "container" to acccess: dirs, files, hidden files (leading '.' on *nix systems and/or hidden attribute on Windows systems).

	Usage:
	- content = list_content(str_path) // for dir in content.dirs // for file in content.files

	
	Arguments:
	- location:   Expects a path(lib) object or a string, if None is passed, CWD (.) is used.
	- root:       If provided, only relative paths to content of location will be listed. (This part is cut off)
	- EXTENSION:  Expects string or a list of strings containing the file extension only (txt, md, py - without a dot)
	              This has no impact on dirs.
	- FILTER:     String or list of strings and regex'
	- HIDE:       String or list of strings/regex to hide (move to 'hide' group)
	- bDual:      Returns returnvalue (bool) and content.
	- bRecursive: By default, it is only listing items of the current dir, this will work recursivly.
	"""
	#
	#	Init
	#
	output = ""
	ret = False
	this_dirs, this_files, this_hide = [], [], []
	result = None
	#
	#	Prepare input
	#
	if location:
		if _tui._put._OS.isdir(location):
			# TODO: Change to dir:
			_tui._put._OS.cd(location)
		else:
			msg = _MSG.cl_log_err_must_path
			
	
	if EXTENSION:
		# Get first results based on all passed extensions
		result = _glob.glob(f'**/*.{EXTENSION}', recursive=bRecursive, include_hidden=True )
	else:
		# Get all the dirs and files
		result = _glob.glob(f'**/**', recursive=bRecursive, include_hidden=True)
	#
	#	Work with data
	#
	if FILTER:
		# Filter is active, so lets remove some entries
		for f in FILTER:
			if isinstance(f, _re.Pattern):
				# TODO: Do regex things
				for item in result:
					if f in item:
						result.remove(item)
			elif isinstance(f, str):
				for item in result:
					if f in item:
						result.remove(item)


	#
	#	Final output
	#
	if bDual:
		return ret, output
	else:
		return output
