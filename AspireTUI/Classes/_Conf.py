# TODO: Put "msg_" strings to _MSG.english
"""
This file provides the Conf class only.

Read the description of the class and its functions upon using them in your code.

========================================================

Created on:		2024 Jan. 04

Rewritten on:	2024 Sept. 15

Created by:		Simon Arjuna Erat

License:		MIT

URL:			https://www.github.com/sri-arjuna/ASPIRE

Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Imports for filetype wrappers
#
from io import TextIOWrapper
from collections import OrderedDict
from typing import Union
# Use Union to specify that it can be either str or bytes
StrOrBytesPath = Union[str, bytes]

#
#	Imports
#
from .._MESSAGES import current as _MSG		# Partial used for bVerbose
from .. import tui as _tui
from .. import OS as _OS
from .. import Path as _Path
#from .. import Lists as _Lists
from .. import Strings as _stew


#################################################################################################################
#####                                           Class: Conf                                                 #####
#################################################################################################################
# Main Section
class Conf:
	def __init__(self, 
			filename: str=None,
			bVerbose: bool=True,
			comment: str=None,
			bForceRead: bool=False,
			bForceSave: bool=False,
			encoding: str="UTF-8",
			bAspire: bool=True
			):
		"""
# Configuration Handler

*Reading and writing config files, preserving comments*

Provided functions:\n
* get(section, key) - returns value, use bDual:bool to get ret_bool and ret_str
* set(section, key, value) - sets value, returns True on success, this will also allow to create a new section, use bDual:bool to get ret_bool and ret_str
* list_sections(bool: bString) - Returns a list, or string if bString is True
* list_keys(section) - Returns a list, or string if bString is True
* read() - Also used for reloading, returns False if no filename is provided (in case you want a runtime/cache use only)
* save() - Saves cache to file, returns False if no filename was provided (in case you want a runtime/cache use only)

Arguments:\n
* filename: str or bytes = Expects either "absolute path" or None, if None, read/save and thus bForceRead/ForceWrite will be disabled for "runtime/cache" use only, this includes bAspire.
* bVerbose: bool = Will print a message to user about the function its success or failure
* bForceRead: bool = This will toggle to reload/read the file as a whole upon every call of get()
* bForceSave: bool = This will toggle to save the whole cache to file upon every call of set()
* bAspire: bool = This will toggle Theme handling as provided by AspireTUI
* comment: str or list = This allows for multiline comments (either list entries or using \n) at the top of the file.
* encoding: str = Change this if your file is not compatible with UTF-8. TODO: needs validation to verify proper encoding strings (like latin1, or whatever is passed)

# TLDR: \n
By default, it will read() the file once upon init and only save the file upon calling save()

Instead of get/set, you can also use:

myConf = Classes.Conf()

val = myConf["Section"]["Key"]

# Usage:

#Minimal runtime config only\n
myConf = Classes.Conf()

#All default values changed\n
myConf = Classes.Conf(filename, bVerbose=True, comment="My config file header", bForceRead=True, bForceSave=False, encode="Latin-1", bAspire=False)

## Usage:

val = myConf.get(Section, Key)

myConf.set(Section, Key, Value)

myConf.save()
		"""
		#
		#	Internal data structures
		#
		class __InternalSettings():
			filename: str=None
			bVerbose: bool=True
			comment: str=None
			bForceRead: bool=False
			bForceSave: bool=False
			encoding: str="UTF-8"
			bAspire: bool=True
			isBytes: bool=False
			isString: bool=False
		class __FileData():
			cache: dict=None
			comments: dict=None
			raw: list=None
			# This will get detected/overwritten in/by read() as some shells require " = "
			separator: str  = "="
			
		#
		#	Main structure / internal data handling
		#	Just blindly apply provided entries
		#
		self._data = __FileData()
		self._internal = __InternalSettings()
		self._internal.filename = filename
		self._internal.bVerbose = bVerbose
		self._internal.comment = comment
		self._internal.bForceRead = bForceRead
		self._internal.bForceSave = bForceSave
		# Verify encoding
		if _stew.verify_encoding_name(encoding):
			self._internal.encoding = encoding
		else:
			raise ValueError(f"Provided encoding ({encoding}) is invalid or unkown.")
			return False
		self._internal.bAspire = bAspire

		#
		#	Disable settings if no filename is provided
		#
		if not filename:
			self._internal.bAspire = False
			self._internal.bForceRead = False
			self._internal.bForceSave = False
		else:
			#
			#	filename was passed
			# 	verify filename is valid
			#
			if isinstance(filename, bytes):
				self._internal.isBytes = True
			elif isinstance(filename, str):
				self._internal.isString = True
			else:
				raise TypeError(f"Provided filename ({filename}) is neither bytes nor string.")
				return False
		
		#
		#	Lets fill the data containers
		#	If a filename was provided that is
		#
		if self._internal.filename: self.read()

	
	###############################################################################################################
	####                                 Conf functions - Read                                                 ####
	###############################################################################################################
	def read(cls):
		"""
		Reads the configuration file and applies internals settings (incl theme)
		"""
		#
		#	Lets just make a security check if read is even required
		# 	if filename is None, then nothing to do, so return False
		#
		if not cls._internal.filename: return False
		
		#
		# 	Get important and relevant values
		#
		filename = cls._internal.filename
		encoding = cls._internal.encoding
		bAspire = cls._internal.bAspire
		bVerbose = cls._internal.bVerbose
		# Internal handlers
		SEP = None
		isNew = False
		
		#
		#	Make sure the file exist
		#
		if not _Path.exists(filename):
			# File does not exists
			# Lets verify if path exists
			bn = _OS._os.path.basename(filename)
			path_only = filename[:bn]

			# TODO: Yes, currently expecting an absolute path, will not work properly with only filename
			if _Path.exists(path_only):
				msg_ret = "Provided filename ({filename}) does not exist, and will be created."
				isNew = True
				# Only show message if bVerbose
				if cls._internal.bVerbose: _tui.status(_tui.STATUS.Info.value , msg_ret)
			else:
				# This is fatal, show message regardless of bVerbose
				msg_ret = "Neither filename ({filename}) nor its path does not exist"
				raise ValueError(msg_ret)
				return False
		#
		# 	Mini function
		#
		def has_sep_spaces(line: str=None):
			"""
			This is an internal function to check for the seperator style (either: '=' or ' = ')
			
			It updates the class internal value and returns it for current use as well.
			"""
			if " = " in line:
				cls._data.separator = " = "
			elif "=" in line:
				cls._data.separator = "="
			# Return seperator for easy use
			return cls._data.separator
		
		#
		#	Start reading the file
		#
		if isNew:
			#
			#	Well, file does not exist yet, create default data
			#
			# Top comment?
			top_com = cls._internal.comment
			if top_com:
				# its not empty
				if isinstance(top_com, str):
					# we need a line split
					top_com_multi = top_com.split("\n")
					cls._data.comments[None] = top_com_multi
				elif isinstance(top_com, list):
					cls._data.comments[None] = top_com
				else:
					raise ValueError(f"Provided comment for file '{filename}' is neither str nor list.")

			# Theme handling
			if bAspire:
				cls._data.comments["Theme"][None].append("")
				cls._data.comments["Theme"][None].append("")
				cls._data.cache["Theme"]["THEME"] = "Default"
				cls._data.cache["Theme"]["THEME_COLOR"] = "None"
				cls._data.cache["Theme"]["THEME_STYLE"] = "None"
		else:
			# Init error message for except
			ret_err_msg = None
			# File exists, read it
			try:
				with open(filename, 'r') as file:
					# Lock file for exclusive file handling
					_OS.file_lock_on(file, bVerbose=bVerbose)
					
					# Init vars
					cur_sec = None
					cur_key = None
					section_comments = {}

					# Start parsing
					for line in file:
						# Preserve absolute raw content:
						cls._data.raw.append(line)
						
						# Lets make workable-line
						stripped_line = line.strip()

						# Preserve exact file strucutre
						if not stripped_line:
							continue

						# Handle comments
						if stripped_line.startswith("#"):
							# Preserve multiline comments
							section_comments[cur_sec] = f"{section_comments[cur_sec]}\n{line.rstrip()}"
						
						# Handle sections
						if stripped_line.startswith('[') and stripped_line.endswith(']'):
							current_section = stripped_line[1:-1]
							cls._data.cache[current_section] = OrderedDict()
							cls._data.comments[current_section] = current_comments[:]
							current_comments = []  # Reset comments after section
							continue
					
						# Prepare key handling
						if not SEP: SEP = has_sep_spaces(line)
						
						# Handle keys
						if SEP in stripped_line:
							key, value = map(str.strip, stripped_line.split(SEP, 1))
							# Store key-value in the current section
							if cur_sec:
								cls._data.cache[cur_sec][key] = value
								cls._data.comments[cur_sec][key] = current_comments[:]
								current_comments = []
			
			# Handle possible exceptions
			except FileNotFoundError:	ret_err_msg = f"Error: File ({file}) not found."
			except PermissionError:		ret_err_msg = "Error: Permission denied."
			except OSError:				ret_err_msg = "Error: File is corrupted or other OS-related issue."
			except Exception as e:		ret_err_msg = f"Unexpected error: {str(e)}"
			
			finally:
				# Release file
				_OS.file_lock_off(file, bVerbose=bVerbose)

				if ret_err_msg:
					_tui.status(False, ret_err_msg)
					return False

		return True

	###############################################################################################################
	####                                 Conf functions - Serialize                                            ####
	###############################################################################################################
	def _serialize(cls):
		"""
		Returns a single string that can be written by save()

		Handles comments:
		* at the top of the file
		* before sections
		* before keys
		"""
		#
		#	Init variables for lazy access
		#	
		#
		output = []
		cache = dict(cls._data.cache)
		comments = dict(cls._data.comments)
		
		#
		#	Handle top level comment
		#
		top_level_comments = comments.get(None, [])
		for comment in top_level_comments: output.append(comment)
		# Add empty line after top level comments for readabilty
		if top_level_comments: output.append("")

		#
		# 	Iterate through sections in the config
		#
		for section in cache:
			# Print section-level comments (if any)
			section_comments = comments.get(section, {}).get(None, [])
			for comment in section_comments: output.append(comment)
			
			# Print the section header (e.g., [section1])
			output.append(f'[{section}]')
			
			# Print key-level comments and key-value pairs
			for key, value in cache[section].items():
				# Print comments for the key (if any)
				key_comments = comments.get(section, {}).get(key, [])
				for comment in key_comments: output.append(comment)
				
				# Print the key-value pair
				output.append(f'{key} = {value}')
			
			# Add an empty line between sections
			output.append("")
		
		# Return to user
		return '\n'.join(output)
	
	###############################################################################################################
	####                                 Conf functions - Save                                                 ####
	###############################################################################################################
	def save(cls):
		"""
		Saves data to conf file.
		"""
		# Nothing to do, so havent written anything
		if not cls._internal.filename:
			return False
		
		#
		# 	Values
		#
		filename = cls._internal.filename
		encoding = cls._internal.encoding
		bVerbose = cls._internal.bVerbose
		ret_err_msg = None
		
		#
		#	Attempt to save
		#
		try:
			with open(filename, 'w', encoding=encoding) as file:
				_OS.file_lock_on(file)
				file.write(cls._serialize()) 

		# Handle possible exceptions
		except FileNotFoundError:	ret_err_msg = f"Error: File ({filename}/{file}) not found."
		except PermissionError:		ret_err_msg = "Error: Permission denied."
		except OSError:				ret_err_msg = "Error: File is corrupted or other OS-related issue."
		except Exception as e:		ret_err_msg = f"Unexpected error: {str(e)}"
		
		finally:
			# Release file
			_OS.file_lock_off(file, bVerbose=bVerbose)

			if ret_err_msg:
				_tui.status(False, ret_err_msg)
				return False

		#
		#	Inform user and return
		#
		msg_saved = f"Successfully saved: {filename}"
		if bVerbose: _tui.status(True , msg_saved)
		return True
	
	###############################################################################################################
	####                                 Conf functions - Get                                                  ####
	###############################################################################################################
	def get(cls, Section: str=None, Key: str=None, bVerbose=False):
		"""
		Raturns the value from the 'key' of '[section]'
		"""
		#
		#	Init vars
		#
		msg_error = None
		ret_bool = False

		# Missing args?
		if Section is None or Key is None:
			msg_error = f"'Conf.get()': {_tui._MSG.args_missing} / sec:{Section} / key:{Key}"
		# Valid entries?
		if not Section in cls.list_sections() or not Key in cls.list_keys():
			msg_args_invalid = "Passed arguments were not found."
			msg_error = f"'Conf.get()': {msg_args_invalid} / sec:{Section} / key:{Key} ::"
		
		# Error handling:
		if msg_error:
			_tui.status(False, msg_error)
			return False

		# Forced Read?
		if cls._internal.bForceRead:  cls.read()
		
		# Retrieve value
		out = cls._data.cache.get(Section, {}).get(Key, None)
		# Verify if we got a value
		if out: ret_bool = True

		# Is GET verbose?
		if bVerbose:
			msg_out = f"Found [{Section}] with {Key} as: {out}"
			_tui.status(ret_bool , msg_out)

		# Return to user
		return out
	
	###############################################################################################################
	####                                 Conf functions - Set                                                  ####
	###############################################################################################################
	def set(cls, Section: str=None, Key: str=None, Value = None, bVerbose=False):
		"""
		Returns True if it could set "Value" to "Key" of "[Section]"
		"""
		#
		#	Init vars
		#
		msg_error = None
		ret_bool = False
		SEP = cls._data.separator

		# Missing args?
		if Section is None or Key is None:
			msg_error = f"'Conf.set()': {_tui._MSG.args_missing} / sec:{Section} / key:{Key}"
		# Valid entries?
		if not Section in cls.list_sections() or not Key in cls.list_keys(Section):
			msg_error = f"'Conf.set()' Passed arguments were not found. / sec:{Section} / key:{Key} ::"
		
		# Error handling:
		if msg_error:
			_tui.status(False, msg_error)
			return False
		
		#
		# 	Set value
		#	Check for existing values
		#			
		if not Section in cls.list_sections() or not Key in cls.list_keys(Section):
			# Either Section or Key was NOt found, add new entry:
			cls._data.cache[Section][Key] = Value
			ret_bool = True
			ret_task = "Added"
		else:
			# Entries exist, lets update:
			cls._data.cache[Section][Key] = Value
			ret_bool = True
			ret_task = "Updated"
		
		# Is it forced saved?
		if ret_bool and cls._internal.bForceSave: cls.save()

		if bVerbose:
			msg_out = f"{ret_task}: [{Section}], {Key}{SEP}{Value}"
			_tui.status(ret_bool, msg_out)
		
		# Return to user
		return ret_bool

	###############################################################################################################
	####                                 Conf functions - Lists                                                ####
	###############################################################################################################
	def list_sections(cls, bString=False):
		"""
		Returns a list of all sections in the config.
		
		Returns False if no sections were found
		"""
		# Init section as top holder
		sections = list(cls._data.cache.keys())

		# Return to user according to bString
		if sections:
			# Entries found
			if bString:	return ", ".join(sections)
			else: 		return sections
			# No entries found
		else:			return False

	def list_keys(cls, Section: str = None, bString=False):
		"""
		Returns a list of keys for a given section.
		
		Returns False if Section is none, or no entry for Section could be found.
		"""

		# Ensure the section is specified and exists
		if Section and Section in cls._data.cache:
			# Get all keys for the given section
			keys = list(cls._data.cache[Section].keys())
			
			# Return to user according to bString
			if bString: return ", ".join(keys)
			else:		return keys
		else:
			# Return an empty list if the section does not exist or isn't specified
			return False
