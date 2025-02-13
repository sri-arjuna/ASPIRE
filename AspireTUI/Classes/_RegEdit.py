"""
	Description:
			Provides pulic functions to access the Windows Registry, and a class wrapper for a specific path

	Usage:
			from AspireTUI.Classes import RegEdit
			myReg = RegEdit.Class(args)

	========================================================

	Created on:		2024 Jan. 08
	
	Created by:		Simon Arjuna Erat
	
	License:		MIT
	
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Internal imports
#
from AspireTUI import IS_WINDOWS as _IS_WINDOWS
from AspireTUI import tui as _tui
from AspireTUI._MESSAGES import current as _MSG
from AspireTUI.ColorAndText import cat as _cat

#
#	Imports
#
import winreg as _winreg
#import configparser as _configparser

#
#	Variables
#
_HKEY = {
	"CLASSES_ROOT": _winreg.HKEY_CLASSES_ROOT,
	"CURRENT_USER": _winreg.HKEY_CURRENT_USER,
	"LOCAL_MACHINE": _winreg.HKEY_LOCAL_MACHINE,
	"USERS": _winreg.HKEY_USERS,
	"CURRENT_CONFIG": _winreg.HKEY_CURRENT_CONFIG
}

#################################################################################################################
#####                                           Public Functions                                            #####
#################################################################################################################
def get(hive_key, key_path, value_name) -> str:
	"""
	Attempts to read passed arguments and returns the according value.

	Recommended:

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

def set(hive_key, key_path, value_name, value, value_type=_winreg.REG_SZ):
	"""
	Attempts to set passed value and returns a bool.
	
	Recommended:

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

def list_keys(hive_key, key_path):
	"""
	Attempts to list all key inside passed key_path, returns them as list.

	Recommended:

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

def list_vars(hive_key, key_path):
	"""
	Attempts to list all variable names inside passed key_path, returns them as list.

	Recommended:

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
#####                                        Public Class Wrapper                                           #####
#################################################################################################################
class Class:
	"""
	This class is a wrapper for a passed HKEY/Path, it will then make all sub-paths available as "instance.data.<sub-path>"

	This Registry wrapper only works on Windows Machines, and is CaSe-SenSiTiVe while using: "instance.data.*" !!

	You can circumvent CaSe-SenSiTiVe, when using "instance.search('string')" - this will return all occourences of 'string', such as: 'String', 'string' and 'strInG' alike.
	
	"instance.search('string')" will parse "instance.data.*" everything recursivly for any and all occourences.

	"instance.data.list()", more pecicly, "*.list" is available in all sub-paths of the opened path, such as "instance.data.sub1.sub-level2". "*.list()" will only return a list of the current paths content.
	"""
	def __init__(self, hkey: _HKEY=None, path: str=None):
		if not hkey or not path: 
			_tui.status(False, "No 'hkey' or 'path' passed")
			return False
		if _winreg.ConnectRegistry(hkey, path):
			_tui.status(True, f"Established connection: {path}")
		else:
			_tui.status(False, f"Could not find: {hkey}/{path}")
	

	def search(value: str=None) -> list|None:
		"""
		Searches recursivly starting from "instance.data"
		
		Returns result as list, or None
		"""

		# While parsing through all paths/keys... use the flowwing command to indicate "action"
		current_location = current_hkey_path
		_tui.progress(f"Searching in {current_location}", 0, 0, style="dash")



class Registry:
	"""
	A Windows Registry wrapper class that loads all keys & values recursively from the given HKEY path.
	Provides:
		- Attribute-style access to keys (`instance.data.subkey`)
		- `search(value)`: Case-insensitive search in all subkeys & values
	"""

	def __init__(self, hkey_name: str, path: str):
		if hkey_name not in _HKEY:
			_tui.status(False, f"Invalid HKEY: {hkey_name}")
			return

		self.hkey = _HKEY[hkey_name]  # Store actual HKEY
		self.path = path
		self.data = {}  # Store registry keys/values
		self._load_registry_tree(self.hkey, self.path, self.data)

	def _load_registry_tree(self, hkey, path, parent_dict):
		"""Recursively loads registry subkeys and values into `parent_dict`."""
		try:
			with _winreg.OpenKey(hkey, path, 0, _winreg.KEY_READ | _winreg.KEY_WOW64_32KEY) as key:
				values_count, subkeys_count, _ = _winreg.QueryInfoKey(key)

				parent_dict["__values__"] = {}

				# Print debug info
				_tui.progress(f"Loading key: {path} -> {subkeys_count} subkeys, {values_count} values...", 0, 0, style="dash")

				# Load values
				for i in range(values_count):
					try:
						value_name, value_data, _ = _winreg.EnumValue(key, i)
						_tui.progress(f"Loaded value: {value_name} = {value_data}", 0, 0, style="dash")
						parent_dict["__values__"][value_name] = value_data
					except OSError:
						_tui.status(False, f"Error reading value at {path}: {value_name} / {value_data}")

				# Load subkeys (ensuring full path is used)
				for i in range(subkeys_count):
					try:
						subkey_name = _winreg.EnumKey(key, i)  # Get only subkey name
						subkey_path = f"{path}\\{subkey_name}"  # Build FULL path

						_tui.progress(f"Found subkey: {subkey_path} -> Loading...", 0, 0, style="dash")

						parent_dict[subkey_name] = {}  # Ensure subkey is added properly
						self._load_registry_tree(hkey, subkey_path, parent_dict[subkey_name])  # Recursively load
					except OSError:
						_tui.status(False, f"Error reading subkey at {path}")

		except Exception as e:
			_tui.status(False, f"Error reading registry: {path} ->  parent_dict:{parent_dict} ==--> {e}")


	def search(self, value: str) -> list:
		"""Searches recursively starting from `self.data` for any occurrences of `value`."""
		results = []

		def _recursive_search(data, path):
			# Print debug info to check what keys we are searching
			_tui.progress(f"Searching in {path}...", 0, 0, style="dash")

			# Check values in this key
			if "__values__" in data:
				for key, val in data["__values__"].items():
					if isinstance(val, str) and value.lower() in val.lower():
						results.append((path, key, val))  # Match found
						_tui.progress(f"Match found: {path} -> {key} = {val}", 0, 0, style="dash")

			# Recursively search subkeys
			for key, val in data.items():
				if key == "__values__":
					continue  # Skip values key (already searched above)
				_recursive_search(val, f"{path}\\{key}")

		_recursive_search(self.data, self.path)
		return results
