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
			#tui.status(False, "Invalid HKEY")
			return False, _MSG.registry_hkey
	except Exception as e:
		#print(f"Error: {e}")
		return False, f"{_MSG.word_error}: {e}"
