"""
	Description:
					Public functions to easy several tasks with strings (or math)
	Provides:
					from AspireTUI import ConfigUtills as cu
					ret_bool, ret_str = cu.reg_value_get(file,key,var)
					
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
#import re as _re
#import string as _string
from AspireTUI._MESSAGES import current as _MSG
# 
#	Cross Platform & Advanced usage
#
#import platform as _platform
#import msvcrt as _msvcrt
#import shutil as _shutil
#import subprocess as _subprocess
import winreg as _winreg
import configparser as _configparser
#
#	Prepare data structures
#
#from enum import Enum as _Enum
#from enum import EnumMeta as _EnumMeta
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
def reg_value_get(hive_key, key_path, value_name):
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
