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

# TODO : Once all functions had been tested and are considered functionaly stable, change to: Filename as StrOrBytesPath

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
import glob as _glob
import fnmatch as _fnmatch

from typing import Union as _Union
# Define the type hint
StrOrBytesPath = _Union[str, bytes]

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
	Returns the absolute current working directory in *nix-style format (/)

	Returns path in *nix style format: C:/././
	"""
	return _os.path.abspath(_os.getcwd()).replace("\\","/")

def dir_app(myApp: __file__):
	"""
	Returns the absolute path of the app that is running / calling this function.

	Returns path in *nix style format: C:/././
	"""
	if not myApp:
		_tui.status(False, "AspireTUI.Path.dir_app: Must pass '__file__' for proper detection.")
		return None
	if hasattr(myApp, 'read'):
		# We're in an interactive session
		return _os.path.abspath(_os.getcwd()).replace("\\","/")
	else:
		#return _pathlib.Path(_os.path.abspath(__file__)).parent.replace("\\","/")
		return _os.path.abspath(myApp).replace("\\","/")

# FileDescriptorOrPath
def exists(filename: StrOrBytesPath=None, bVerbose=False, bDual=False, bShowFull=False) -> StrOrBytesPath:
	"""
Returns True if filename exists

Use 'bVerbose = True' to print various status messages

Use 'bDual = True' to get: ret_bool and ret_msg

Use 'bShowFull = True' this will print absoltue filename to console (and set Verbose=True)

Usage:

	if _Path.exists(filename): tui.print("yes")

	if _Path.exist(filename, Verbose=True): tui.print("...")

	ret_bool, ret_msg = _Path.exists(filename, bDual=True)
"""
	#
	#	Init vars
	#
	ret_bool = False
	fn = None
	fn_abs = None
	fn_out = None
	ret_type = None
	ret_msg = ""
	ret_found = _MSG.word_found
	
	# Error messages for developers are always english
	ret_err = f"AspireTUI.Path.exists(filename={filename}, bVerbose={bVerbose}, bDual={bDual}, bShowFull={bShowFull}) requires at least 1 argument (filename)."

	# Convience
	if bShowFull: bVerbose=True
	
	#
	#	Most important
	#	Make sure required argument filename is passed
	#
	if filename is None:
		# Print output?
		if bVerbose: _tui.status(ret_bool, ret_err)
		
		# Exit with error
		if bDual:
			return ret_bool, ret_err
		else:
			return ret_bool
	
	#
	#	Prepare short and abs strings
	#	These we work with
	#
	#fn = StrOrBytesPath(		_os.path.basename(filename) )
	#fn_abs = StrOrBytesPath(	_os.path.abspath(filename) )
	fn = _os.path.basename(filename)
	fn_abs = _os.path.abspath(filename)


	# Verify proper path:


	#
	#	Check for existing and prepare ret_msg
	#
	if _os.path.exists(fn_abs) or _os.path.exists(fn): 
		ret_bool = True
		#
		#	Now we can work properly
		#	Get type of "filename"
		# 	since bVerbose is handles by exists, lets not spam the user
		#
		if isDir(fn_abs, bVerbose=False):
			ret_type = _MSG.word_filesystem_dir
		elif isFile(fn_abs, bVerbose=False):
			ret_type = _MSG.word_filesystem_file
		elif isLink(fn_abs, bVerbose=False):
			ret_type = _MSG.word_filesystem_link
		elif isMount(fn_abs, bVerbose=False):
			ret_type = _MSG.word_filesystem_mount
		
		# Prepare message
		ret_msg += f"{ret_found} {ret_type}"
	else:
		ret_msg = f"{ret_found}"
	
	#
	#	Prepare output
	#
	if bShowFull:
		# Absolute full path for filename
		ret_msg = f"{ret_msg}: {fn_abs}"
	else:
		# Just the short (basename) of filename
		ret_msg = f"{ret_msg}: {fn}"

	# Show to user?
	if bVerbose: _tui.status(ret_bool, ret_msg)

	# Return dual?
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


def hasFiles(pattern, path: StrOrBytesPath='.', bDual=False):
	"""
	Looks for pattern in path and returns bool if found.

	if bDual is true, it retuns {bool list} like: True, [a,b,c]
	"""
	#return [f for f in _os.listdir(path) if _fnmatch.fnmatch(f, '*.' + extension)]

	"""
		if isinstance(path, bytes):
			path = path.decode("utf-8")  # Ensure path is a string

		ret_bool = False
		ret_list = [f for f in _os.listdir(path) if _fnmatch.fnmatch(f, pattern)]

	"""

	ret_bool = False
	ret_list = []
	if _os.path.exists(path):
		ret_list = [f for f in _os.listdir(path) if _fnmatch.fnmatch(f, pattern)]
	else:
		_tui.status(False, _MSG.dir_not_found, path)
	if ret_list: ret_bool = True
	if bDual:
		return ret_bool, ret_list
	else:
		return ret_bool

def gen_filename(fn_base: StrOrBytesPath=None, fn_ext: str=None, bPath:bool = False, bDaily: bool=False, bUnique: bool=False, bVerbose=False):
	"""
Generates/return basename of filename : {fn_base}.{fn_ext}

Use 'bDaily = True' to return with current date: {fn_base}-{date}.{fn_ext}

Use 'bPath = True' to return asolute path using *nix style '/' instead of windows '\\'

Use 'bUnique = True' to create a new filename like: {fn_base}({count}).{fn_ext}

# _Attention__

* 'bPath' only works properly if the file was created already, otherwise current path is used. \n
* Also, 'bPath' must be enabled if you pass an absolute directory as filename_base. (bad example: gen_filename("C:\\pagefile", "sys")
* You can only use either bDaily or bUnique, not both
	"""
	# Make sure possible return values are None
	this_fn = None
	this_path = None

	# Check for valid args
	if not fn_base or not fn_ext:
		# Either FN or EXT is missing
		_tui.status(False, f"Must provide both, filename ({fn_base}) and extension ({fn_ext}).")
		return False
	
	if bDaily and bUnique:
		# Cant use both
		_tui.status(False, f"You can not use bDaily ({bDaily}) and bUnique ({bUnique}) at the same time.")
		return False

	#
	#	Check if an absolute path was provided
	#	Or if adjustments for bPath are required
	#
	this_fn = f"{fn_base}.{fn_ext}"
	if _os.path.isabs(this_fn):
		bAdjustPath = False
	else:
		bAdjustPath = True
	
	#
	#	With full path or not?
	#
	if bPath:
		# Yes, full path shall be returned
		if bAdjustPath:
			this_path = f"{dir_cur()}/{this_fn}"
		else:
			this_path = this_fn
	else:
		# Nope, just basename
		this_path = _os.path.basename(this_fn)
	
	#
	#	Check for existence
	#
	if exists(this_path, bVerbose=bVerbose):
		# File exists, lets gets its absolute
		ret_bool = True
	else:
		# File does not exist, use current path
		ret_bool = False
		
	#
	# 	Return result after changing \ to /
	#
	this_path = this_path.replace("\\","/")

	#
	# 	Final checks for unqiue or daily:
	#
	if bDaily:
		# Insert current date
		t = _stew.date().replace(".","_")
		old_name = _os.path.basename(this_fn)

		# Adjust for daily name
		new_name = old_name.split(".")[0]
		new_name = f"{new_name}-{t}.{fn_ext}"

		# Update daily name
		this_path = this_path.replace(old_name , new_name)
		if bVerbose: _tui.print(_MSG.path_genfn_unique, this_path)

	elif ret_bool and bUnique:
		# Needs adjustment for unique filename
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
	#
	# Return result
	#
	return this_path

def make_dir(entry: str=None, bVerbose=False) -> bool:
	"""
	Create a directory at the specified path (absolute or relative).
	If the top-level directory doesn't exist, prompt the user before proceeding.

	Args:
		entry (str): The directory path to create.

	Returns:
		bool: True if the directory was successfully created, False otherwise.
	"""
	# Check for non-empty entry
	if not entry:
		_tui.status(False, "AspireTUI.Path.make_dir: " + _MSG.args_missing)
		return False
	
	# Normalize the path
	entry_path = _pathlib.Path(entry).resolve()  # Resolve handles both absolute and relative paths

	# Check if the directory already exists
	if entry_path.exists():
		if bVerbose: _tui.status(_tui.STATUS.Info, f"{_MSG.file_exists}: {entry_path}")
		return True
	
	# Get the top-level parent directory
	top_level = entry_path
	while top_level.parent != top_level:  # Find the top-most parent
		top_level = top_level.parent
		if top_level.exists():
			break

	# If the top-level parent does not exist, ask the user for confirmation
	if not top_level.exists():
		if not _tui.yesno(f"The top-level directory '{top_level}' does not exist. Create it?"):
			if bVerbose: _tui.status(False, f"Directory creation aborted for: {entry_path}")
			return False
	
	# Try to create path "entry"
	# Attempt to create the directory
	try:
		entry_path.mkdir(parents=True, exist_ok=True)  # Recursively create directories
		if bVerbose: _tui.status(True, f"{_MSG.dir_created}: {entry_path}")
		return True
	except Exception as e:
		_tui.status(False, f"{_MSG.dir_not_created} '{entry_path}': {e}")
		return False
