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
import os
import sys
import re
import string
from datetime import datetime as _datetime
from AspireTUI import MESSAGE as _MSG
# 
#	Cross Platform & Advanced usage
#
import platform
import msvcrt
import shutil
import subprocess
import winreg as _winreg
import configparser as _configparser
#
#	Prepare data structures
#
from collections import namedtuple as _namedtuple
from dataclasses import dataclass as _dataclass
from enum import Enum as _Enum
from enum import EnumMeta as _EnumMeta

#################################################################################################################
#####                                           String Utils (stew)                                         #####
#################################################################################################################
def date():
	current_date = _datetime.now()
	formatted_date = current_date.strftime("%Y.%m.%d")
	return formatted_date

def time():
	current_time = _datetime.now()
	formatted_time = current_time.strftime("%H:%M:%S")
	return formatted_time

def now(clean=False, sep="/"):
	if clean:
		return f"{date()} {time()}"
	else:
		return f"{date()} {sep} {time()}"

#################################################################################################################
#####                                           Get registry value                                          #####
#################################################################################################################
# Registry access map
_HKEY_MAP = {
	"HKEY_CLASSES_ROOT": _winreg.HKEY_CLASSES_ROOT,
	"HKEY_CURRENT_USER": _winreg.HKEY_CURRENT_USER,
	"HKEY_LOCAL_MACHINE": _winreg.HKEY_LOCAL_MACHINE,
	"HKEY_USERS": _winreg.HKEY_USERS,
	"HKEY_CURRENT_CONFIG": _winreg.HKEY_CURRENT_CONFIG
}
def reg_value_get(hive_key, key_path, value_name):
	"""
	Attempts to read passed arguments and returns the according value.	\n
	Recommended:\n
	 		success, message = reg_value_get("HKEY_CURRENT_USER", "path/in/HKCU/", "VarName")	\n
			tui.status(success, message)
	"""
	try:
		if hive_key in _HKEY_MAP:
			hkey = _HKEY_MAP[hive_key]
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
		if hive_key in _HKEY_MAP:
			hkey = _HKEY_MAP[hive_key]
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
		if hive_key in _HKEY_MAP:
			hkey = _HKEY_MAP[hive_key]
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
		if hive_key in _HKEY_MAP:
			hkey = _HKEY_MAP[hive_key]
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
