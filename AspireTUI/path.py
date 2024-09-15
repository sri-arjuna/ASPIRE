"""
	Description:
					Public functions to easy several tasks with Files and Path
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
from . import Strings as _stew
from . import _MSG
#from . import Classes as _Classes
#from . import strings as _stew
from . import tui as _tui
from . import OS as _OS
from typing import Union as _Union
import glob as _glob
import fnmatch as _fnmatch
#
#	Paths = Simple access for dirs
#
_HOME = _os.path.expanduser("~").replace('\\','/')
DIRS_DICT = {
	"home": _HOME,
	"docs": _HOME+"/Documents",
	"games_my":  _HOME+"/Documents/My Games",
	"games_saved":  _HOME+"/Saved Games",
	"localappdata": _os.path.expandvars("%localappdata%").replace('\\','/'),
	
}
################################################################################################################
#####                                            Basic Checks                                              #####
################################################################################################################
def dir_cur():
	"""
	Returns the absolute current working directory
	"""
	return _os.path.abspath(_os.getcwd()).replace("\\","/")

def dir_app():
	"""
	Returns the absolute path of the app that is running / calling this function.
	"""
	if hasattr(__file__, 'read'):
		# We're in an interactive session
		return _os.path.abspath(_os.getcwd()).replace("\\","/")
	else:
		return _pathlib.Path(_os.path.abspath(__file__)).parent.replace("\\","/")

# FileDescriptorOrPath
def exists(filename: str=None, bVerbose=False, bDual=False, bShowFull=False):
	"""
	Returns True if filename exists, or both, bool and message.
	
	Examples:

		if _Path.exists(filename):
		
			# Do stuff

			pass
		
		ret_bool, ret_msg = _Path.exists(filename, bDual=True)

	"""
	# Init vars
	fn = None
	ret_bool = False
	ret_msg = f"{_MSG.word_found} "
	ret_err = f"AspireTUI.Path.exists(filename={filename}, bVerbose={bVerbose}, bDual={bDual}, bShowFull={bShowFull}) requires at least 1 argument (filename)."

	# Most important
	if filename is None:
		# Output?
		if bVerbose:
			_tui.status(ret_bool, ret_err)
		# Exit
		if bDual:
			return ret_bool, ret_err
		else:
			return ret_bool
	
	fn_abs = f"{_os.path.abspath(str(filename))}"
	if _os.path.exists(fn_abs):
		ret_bool = True
	
	# Get details
	if ret_bool:
		fn = _os.path.basename(fn_abs)
		ret_type = None
		if isDir(fn_abs, bVerbose=False):
			ret_type = f"{_MSG.word_filesystem_dir}"
		elif isFile(fn_abs, bVerbose=False):
			ret_type = f"{_MSG.word_filesystem_file}"
		elif isLink(fn_abs, bVerbose=False):
			ret_type = f"{_MSG.word_filesystem_link}"
		elif isMount(fn_abs, bVerbose=False):
			ret_type = f"{_MSG.word_filesystem_mount}"
		ret_msg += f"{ret_type}" # '{filename}'"
		
	if bShowFull:
		# Absolute full path
		ret_msg = f"{ret_msg}: '{fn_abs}'"
	else:
		# Currently: - theoreticly the last part
		# Eventualy: The last part (just filename or last/deepest dir)
		ret_msg = f"{ret_msg}: '{fn}'"

	if bVerbose:
		_tui.status(ret_bool, ret_msg)

	if bDual:
		return ret_bool, ret_msg
	else:
		return ret_bool


def isFile(filename: str, bVerbose=False, bDual=False):
	"""
	Returns True if it is a file.
	"""
	# Init vars
	ret_bool = False

	# Most important
	if filename is None:
		ret_msg = f"isFile(filename={filename}) requires an argument."
		# Output?
		if bVerbose:
			_tui.status(ret_bool, ret_msg)
		# Exit
		if bDual:
			return ret_bool, ret_msg
		else:
			return ret_bool
	
	# Main check
	if _os.path.isfile(filename):
		# Its a file
		ret_bool = True
	
		fn = _os.path.basename(filename)
		
		ret_msg = f"{_MSG.word_found} {_MSG.word_filesystem_file}: {fn}"
	
	# Display things, if desired
	if bVerbose:
		_tui.status(ret_bool, ret_msg, fn)
	# Return 
	if bDual:
		return ret_bool, ret_msg
	else:
		return ret_bool

def isDir(filename: str=None, bVerbose=False, bDual=False):
	"""
	Returns True if it is a direcctory.
	"""
	# Init vars
	ret_bool = False

	# Most important
	if filename is None:
		ret_msg = f"isDir(filename={filename}) requires an argument."
		# Output?
		if bVerbose:
			_tui.status(ret_bool, ret_msg)
		# Exit
		if bDual:
			return ret_bool, ret_msg
		else:
			return ret_bool
	
	# Main task
	if _os.path.isdir(filename):
		# Its a dir
		ret_bool = True

	# Check is done, lets prepare output message
	fn = _os.path.basename(filename)
	if fn == "" or None:
		# Got too short
		fn = filename
	ret_msg = f"{_MSG.word_found} {_MSG.word_filesystem_dir}: {fn}"
	
	# is Verbose?
	if bVerbose:
		_tui.status(ret_bool, ret_msg)
	# Return
	if bDual:
		return ret_bool, ret_msg
	else:
		return ret_bool

def isLink(filename: str=None, bVerbose=False, bDual=False):
	"""
	Returns True if it is a link.
	"""
	# Init vars
	ret_bool = False

	# Most important
	if filename is None:
		ret_msg = f"isDir(filename={filename}) requires an argument."
		# Output?
		if bVerbose:
			_tui.status(ret_bool, ret_msg)
		# Exit
		if bDual:
			return ret_bool, ret_msg
		else:
			return ret_bool
	
	# Main task
	if _os.path.islink(filename):
		# Its a dir
		ret_bool = True

	# Check is done, lets prepare output message
	fn = _os.path.basename(filename)
	ret_msg = f"{_MSG.word_found} {_MSG.word_filesystem_link}: {fn}"

	# is Verbose?
	if bVerbose:
		_tui.status(ret_bool, ret_msg)
	# Return
	if bDual:
		return ret_bool, ret_msg
	else:
		return ret_bool

def isMount(filename: str=None, bVerbose=False, bDual=False):
	"""
	Returns True if it is a direcctory.
	"""
	# Init vars
	ret_bool = False

	# Most important
	if filename is None:
		ret_msg = f"isDir(filename={filename}) requires an argument."
		# Output?
		if bVerbose:
			_tui.status(ret_bool, ret_msg)
		# Exit
		if bDual:
			return ret_bool, ret_msg
		else:
			return ret_bool
	
	# Main task
	if _os.path.ismount(filename):
		# Its a dir
		ret_bool = True

	# Check is done, lets prepare output message
	fn = _os.path.basename(filename)
	ret_msg = f"{_MSG.word_found} {_MSG.word_filesystem_mount}: {fn}"

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


def hasFiles(pattern, path='.', bDual=False):
	"""
	Looks for pattern in path and returns bool if found.

	if bDual is true, it retuns {bool list} like: True, [a,b,c]
	"""
	#return [f for f in _os.listdir(path) if _fnmatch.fnmatch(f, '*.' + extension)]
	ret_bool = False
	ret_list = []
	ret_list = [f for f in _os.listdir(path) if _fnmatch.fnmatch(f, pattern)]
	if ret_list: ret_bool = True
	if bDual:
		return ret_bool, ret_list
	else:
		return ret_bool

def gen_filename(fn_base: str=None, fn_ext: str=None, bPath:bool = False, bDaily: bool=False, bUnique: bool=False, bVerbose=False):
	"""
	Generates/return basename of filename : {fn_base}.{fn_ext}

	Use 'bDaily = True' to return with current date: {fn_base}-{date}.{fn_ext}

	Use 'bPath = True' to return asolute path using *nix style '/' instead of windows '\\'

	Use 'bUnique = True' to create a new filename like: {fn_base}({count}).{fn_ext}

	__Attention__: 'bPath' only works properly if the file was created already, otherwise current path is used.
	
	Also, 'bPath' must be enabled if you pass an absolute directory as filename_base. (bad example: gen_filename("C:\\pagefile", "sys")
	"""
	# Make sure possible return values are None
	this_fn = None
	this_path = None

	# Check for valid args
	if not fn_base or not fn_ext:
		# Either FN or EXT is missing
		_tui.status(False, f"Must provide both, filename ({fn_base}) and extension ({fn_ext}).")
		return None
	
	# Return FN with/out date?
	if bDaily:
		t = _stew.date().replace(".","_")
		this_fn = f"{fn_base}-{t}.{fn_ext}"
	else:
		this_fn = f"{fn_base}.{fn_ext}"
	
	# With full path or not?
	if bPath:
		if exists(this_fn, bVerbose=bVerbose):
			# File exists, lets gets its absolute
			this_path =  _os.path.abspath(this_fn).replace("\\","/")
		else:
			# File does not exist, use current path
			this_path = f"{dir_cur()}/{this_fn}"
		
		# Return result after changing \ to /
		this_path = this_path.replace("\\","/")
	else:
		# Nope just simple (basename)
		this_path = _os.path.basename(this_fn)

	# Final checks for unqiue:
	if bUnique:
		# asdf
		if exists(this_path):
			# Exists, adjust filename
			count = 0
			raw_left, raw_ext = this_path.split(".")
			while True:
				this_check = f"{raw_left}({count}).{fn_ext}"
				if exists(this_check):
					count += 1
				else:
					this_path = this_check
					if bVerbose: _tui.print(_MSG.path_genfn_unique, this_path)
					break
	# Return result
	return this_path
