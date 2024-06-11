"""
	Description:
					Public functions to easy several tasks with strings (or math)
	Provides:
					from AspireTUI import StringUtills as stew
					stew.date() , stew.time()
					
	========================================================
	Created on:		2023 Nov. 09
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Essential imports
#
#import os as _os
#import sys as _sys
import re as _re
#import string as _string
from datetime import datetime as _datetime
# 
#	Cross Platform & Advanced usage
#
#import platform as _platform
#import msvcrt as _msvcrt
#import shutil as _shutil
#import subprocess as _subprocess

#
#	Prepare data structures
#
#from collections import namedtuple as _namedtuple
#from dataclasses import dataclass as _dataclass
from typing import Union as _Union
import winreg as _winreg
import configparser as _configparser
#
#	Internal imports
#
from ._MESSAGES import current as _MSG
from .ColorAndText import cat
"""
def _ClassDate():
	date = date()
	time = time()
	now = now()
	logtime = logtime()
def _ClassChange():
	esc2hex = esc2hex()
	conf2dict = conf2dict()
	sec2time = sec2time()
def Menu():
	datetime = _ClassDate()
	change = _ClassChange()
"""
#################################################################################################################
#####                                           String Utils (stew)                                         #####
#################################################################################################################
def date(bNames=False) -> str:
	"""
	Returns date like:
	2024.12.30
	"""
	current_date = _datetime.now()
	formatted_date = current_date.strftime("%Y.%m.%d")
	if bNames:
		formatted_date += f" {current_date.strftime('%A, %B')}"
	return formatted_date

def time(bLong=False) -> str:
	"""
	Returns time like:
	15:30
	"""
	current_time = _datetime.now()
	formatted_time = current_time.strftime("%H:%M:%S")
	if bLong:
		formatted_time += f":{current_time.strftime('%S')}"
	return formatted_time

def now(clean=False, sep="/", bLong=False, bNames=False) -> str:
	"""
	Returns date and time like: \n
	2024.12.30 / 15:45
	"""
	if clean:
		return f"{date(bNames)} {time(bLong)}"
	else:
		return f"{date(bNames)} {sep} {time(bLong)}"

def logtime() -> str:
	"""
	Returns a string to be used for safe-file-names.
	"""
	current_time = _datetime.now()
	formatted_time = current_time.strftime("%Y.%m.%d_%H.%M.%S")
	return formatted_time

def close_html_tags(html_string: str, exclude="") -> str:
	"""
	Close open HTML tags in the provided string.
	Exclude closing "<div>" tags.
	"""
	# Match open tags
	open_tags = _re.findall(r'<([^/][^>]*)>', html_string)

	# Check for open tags from the end of the string
	for tag in reversed(open_tags):
		if exclude:
			if not tag.startswith(exclude):
				# Close the tag
				html_string += f'</{tag}>'
		else:
			html_string += f'</{tag}>'
	# No treatment required 
	return html_string

def esc2hex(strESC:str) -> str:
	"""
	Transforms internal color codes to web-hex-colors. \n
	Returns an empty string if it didnt find something to close. \n
	Example: colorA = esc2hex(cat.fg.white)
	"""
	#from AspireTUI.strings import cat
	if strESC == cat.reset:
		# Handle special case for cat.reset
		return close_html_tags(strESC)
	elif _re.match(r'<color=[^>]+>', strESC):
			# Fallback: Close color tags
			return _re.sub(r'<color=[^>]+>', '</color>', strESC)
	return ""

def conf2dict(config_string) -> dict:
	"""
	Splits the content of a conf file, or env/set outputs to a dictionary
	"""
	tmp_dict = {}
	for line in config_string.split('\n'):
		if '=' in line:
			key, value = line.split('=', 1)
			tmp_dict[key] = value
	return tmp_dict

def sec2time(sec:_Union[int, float], format=None) -> str:
	"""
	Transforms given seconds to proper HH:MM:SS format.
	"""
	if isinstance(sec, int):
		# Default, basic seconds
		format_fmt = "%H:%M:%S"
	elif isinstance(sec, float):
		# It is microseconds
		format_fmt = "%H:%M:%S.%f"
	else:
		# Unsupported
		raise ValueError(_MSG.word_error, _MSG.cl_log_err_must_int, _MSG.cl_log_err_must_float)

	# Prefer passed format over default
	if format is None:
		# halfway to new python way....
		return _datetime.utcoffset(sec).strftime(format)
		#return _datetime.utcfromtimestamp(sec).strftime(format)
	else:
		format = format_fmt
		# halfway to new python way....
		return _datetime.fromtimestamp(sec).strftime(format)
		#return _datetime.utcfromtimestamp(sec).strftime(format)

	# Return passed seconds as time according to format
	#return _datetime.utcfromtimestamp(sec).strftime(format)	#old
	#return _datetime.fromtimestamp(_datetime.utcnow).strftime(format)	# new not proper
from datetime import timedelta

def sec2time(sec):
	"""
	Transforms given seconds to proper HH:MM:SS format.
	"""
	result = None
	if isinstance(sec, int):
		# Default, basic seconds
		doMili = False
	elif isinstance(sec, float):
		# It is microseconds
		doMili = True
	else:
		# Unsupported
		raise ValueError(_MSG.word_error, _MSG.cl_log_err_must_int, _MSG.cl_log_err_must_float)

	# Create a timedelta object from the seconds
	delta = timedelta(seconds=sec)

	# Extract hours, minutes, and seconds from the timedelta
	total_seconds = int(delta.total_seconds())
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)

	#
	#	Prepare dynamic output
	#
	if hours == 0 and minutes == 0:
		# Its just seconds, present simple:
		result = seconds
	elif hours != 0:
		# Max length, with proper format
		result = f"{hours:02}:{minutes:02}:{seconds:02}"
	else:
		# Duration is within minutes range
		result = f"{minutes:02}:{seconds:02}"
	
	# Was it a float and thus requires mili seconds?
	if doMili:
		result = f"{result}.{int(delta.microseconds / 1000):03}"

	return result

def num2roman(num: int) -> str:
	"""
	Converts an integer to Roman numeral
	"""
	if not 0 < num:
		raise ValueError("Input must be a positive integer")
	
	from AspireTUI import Lists as _lists
	roman_numerals = _lists.roman_num2roman
	result = ''
	for value, numeral in roman_numerals.items():
		count = num // value
		result += numeral * count
		num %= value

	return result

def roman2num(roman: str) -> int:
	"""
	Converts Roman numeral to integer
	"""
	from AspireTUI import Lists as _lists
	roman_numerals = _lists.roman_roman2num

	result = 0
	prev_value = 0

	for numeral in reversed(roman):
		value = roman_numerals[numeral]
		if value < prev_value:
			result -= value
		else:
			result += value
		prev_value = value

	return result

def char2morse(input_data) -> str:
	"""
	Converts characters or a multiline string to Morse code.
	"""
	from AspireTUI.Lists import morse_code as _MORSE_CODE_DICT
	if isinstance(input_data, str):
		input_data = input_data.upper().splitlines()
	return '\n'.join([' '.join([_MORSE_CODE_DICT[char] if char in _MORSE_CODE_DICT else char for char in line]) for line in input_data])

def morse2char(input_data) -> str:
	"""
	Converts Morse code to characters.
	"""
	from AspireTUI.Lists import morse_code as _MORSE_CODE_DICT
	if isinstance(input_data, str):
		input_data = input_data.splitlines()
	morse_dict_reverse = {value: key for key, value in _MORSE_CODE_DICT.items()}
	return '\n'.join([''.join([morse_dict_reverse[code] if code in morse_dict_reverse else code for code in line.split()]) for line in input_data])

def num2alpha(number: int) -> str:
	"""
	Convert an integer to alphabetical representation.
	Example:
	1 -> 'a', 2 -> 'b', ..., 26 -> 'z', 27 -> 'aa', 28 -> 'ab', ..., 52 -> 'zz', and so on.
	"""
	result = ""
	while number > 0:
		number, remainder = divmod(number - 1, 26)
		result = chr(65 + remainder) + result
	return result.lower()

def alpha2num(AlphaNum: str) -> int:
	"""
	Convert alphabetical representation to an integer.
	Example:
	'a' -> 1, 'b' -> 2, ..., 'z' -> 26, 'aa' -> 27, 'ab' -> 28, ..., 'zz' -> 52, and so on.
	"""
	result = 0
	for char in AlphaNum.lower():
		result = result * 26 + ord(char) - 96
	return result

#
#	"String" related bools
#
def isList(this, bDual=False) -> bool:
	"""
	Simple bool. \n

	"""
	# Init
	bRet = False
	sList = None
	# Check
	if isinstance(this, list):
		bRet = True
		try:
			sList = list(this)
		except TypeError(list, this):
			sList = _MSG.cl_log_err_must_list
			bRet = False
	# Return
	if bDual:
		return bRet, sList
	else:
		return bRet

#################################################################################################################
#####                                           Get registry value                                          #####
#################################################################################################################
# Registry access map
_HKEY = {
	"CLASSES_ROOT": _winreg.HKEY_CLASSES_ROOT,
	"CURRENT_USER": _winreg.HKEY_CURRENT_USER,
	"LOCAL_MACHINE": _winreg.HKEY_LOCAL_MACHINE,
	"USERS": _winreg.HKEY_USERS,
	"CURRENT_CONFIG": _winreg.HKEY_CURRENT_CONFIG
}
def reg_value_get(hive_key, key_path, value_name) -> str:
	"""
	Attempts to read passed arguments and returns the according value.	\n
	Recommended:\n
	 		success, message = reg_value_get("HKEY_CURRENT_USER", "path/in/HKCU/", "VarName")	\n
			tui.status(success, message)
	"""
	try:
		if hive_key in _HKEY:
			hkey = _HKEY[hive_key]
			# Open the specified registry key
			with _winreg.OpenKey(hkey, key_path) as key:
				# Read the value of the specified name
				value, value_type = _winreg.QueryValueEx(key, value_name)
				return True, f"{value}"
		else:
			return False, _MSG.registry_hkey
	except Exception as e:
		return False, f"{_MSG.word_error}: {e}"

def reg_value_set(hive_key, key_path, value_name, value, value_type=_winreg.REG_SZ):
	"""
	Attempts to set passed value and returns a bool.	\n
	Recommended:\n
	 		success, message = reg_value_set("HKEY_CURRENT_USER", "path/in/HKCU/", "VarName", "value")	\n
			tui.status(success, message)
	"""
	try:
		if hive_key in _HKEY:
			hkey = _HKEY[hive_key]
			with _winreg.OpenKey(hkey, key_path, 0, _winreg.KEY_SET_VALUE) as key:
				_winreg.SetValueEx(key, value_name, 0, value_type, value)
			return True, _MSG.registry_success
		else:
			return False,  _MSG.registry_hkey
	except Exception as e:
		return False, f"{_MSG.word_error}: {e}"

def reg_value_list_key(hive_key, key_path):
	"""
	Attempts to list all key inside passed key_path, returns them as list.	\n
	Recommended:\n
	 		success, message = reg_value_list_key("HKEY_CURRENT_USER", "path/in/HKCU/")	\n
			tui.status(success, message)
	"""
	try:
		if hive_key in _HKEY:
			hkey = _HKEY[hive_key]
			with _winreg.OpenKey(hkey, key_path) as key:
				subkeys_count, _, _ = _winreg.QueryInfoKey(key)
				subkeys = [_winreg.EnumKey(key, i) for i in range(subkeys_count)]
				return True, subkeys
		else:
			return False,  _MSG.registry_hkey
	except Exception as e:
		return False, f"{_MSG.word_error}: {e}"

def reg_value_list_var(hive_key, key_path):
	"""
	Attempts to list all variable names inside passed key_path, returns them as list.	\n
	Recommended:\n
	 		success, message = reg_value_list_var("HKEY_CURRENT_USER", "path/in/HKCU/")	\n
			tui.status(success, message)
	"""
	try:
		if hive_key in _HKEY:
			hkey = _HKEY[hive_key]
			with _winreg.OpenKey(hkey, key_path) as key:
				values_count, _, _ = _winreg.QueryInfoKey(key)
				values = [_winreg.EnumValue(key, i)[0] for i in range(values_count)]
				return True, values
		else:
			return False,  _MSG.registry_hkey
	except Exception as e:
		return False, f"{_MSG.word_error}: {e}"

#################################################################################################################
#####                                           Config (ini) files                                          #####
#################################################################################################################
def ini_read(c_file, c_key, c_variable):
	"""
	Reads c_file as ini file, looks for c_keys (section) and returns the value of c_variable. \n
	Usage: \n
			value = ini_read("path/to/filename", "section_name", "variable_name")
	"""
	config = _configparser.ConfigParser()
	try:
		config.read(c_file)
		if c_key in config and c_variable in config[c_key]:
			return config[c_key][c_variable]
		return None
	except FileNotFoundError as e:
		return False, f"{_MSG.word_error}:\n{_MSG.file_not_found}: {e}"

def ini_write(c_file, c_key, c_variable, c_value):
	"""
	Reads c_file as ini file, looks for c_keys (section) and returns the value of c_variable. \n
	Usage: \n
			if ini_write("path/to/filename", "section_name", "variable_name", "value"):
				tui.status(True, "Success message")
	"""
	config = _configparser.ConfigParser()
	try:
		config.read(c_file)
		if not config.has_section(c_key):
			config.add_section(c_key)
		config.set(c_key, c_variable, c_value)
		with open(c_file, 'w') as config_file:
			config.write(config_file)
		return True
	except Exception as e:
		return False, f"{_MSG.word_error}: {e}"

def ini_list_keys(c_file):
	"""
	Reads c_file as an ini file and returns a list of all section names.
	Usage:
		keys = ini_list_keys("path/to/filename.ini")
	"""
	config = _configparser.ConfigParser()
	try:
		config.read(c_file)
		return config.sections()
	except FileNotFoundError as e:
		return False, f"{_MSG.word_error}:\n{_MSG.file_not_found}: {e}"

def ini_list_vars(c_file, c_key):
	"""
	Reads c_file as an ini file, looks for c_key (section), and returns a list of all variable names in that section.
	Usage:
		vars = ini_list_vars("path/to/filename.ini", "section_name")
	"""
	config = _configparser.ConfigParser()
	try:
		config.read(c_file)
		if c_key in config:
			return config.options(c_key)
		return None
	except FileNotFoundError as e:
		return False, f"{_MSG.word_error}:\n{_MSG.file_not_found}: {e}"
